"""Graph traversals shared by the ViewModels.

They only use the Graph interface (nodes, node, outgoing, incoming), so they run on the in-memory
graph and on Neo4j. The dictionaries they return use the keys of the ViewModel JSON (Portuguese,
the vocabulary of the views).
"""
from ecv import config
from ecv.graph.base import read_json

RULE_TYPE_ORDER = config.RULE_TYPE_ORDER


def order_rules(rules):
    return sorted(rules, key=lambda r: (RULE_TYPE_ORDER.get(r.label, 9), r.get("id")))


def hlm_node(g, hlm):
    node = g.node("HLM", hlm)
    if node is None:
        raise ValueError(f"HLM '{hlm}' não existe no grafo")
    return node


def property_node(g, key):
    node = g.node("Propriedade", key)
    if node is None:
        raise ValueError(f"propriedade '{key}' não existe (use a chave '<NÍVEL>:<Dono>.<nome>', ex.: 'USM:Medicao.valor')")
    return node


def model_node(g, level, name):
    node = g.node(level, name)
    if node is None:
        raise ValueError(f"{level} '{name}' não existe no grafo")
    return node


# ---------------------------------------------------------------------- structure
def children(g, node):
    """Compositions of a model, in declared order: [(COMPOSTO_POR edge, child node)]."""
    edges = sorted(g.outgoing(node, "COMPOSTO_POR"), key=lambda e: e.get("ordem", 0))
    return [(e, e.target) for e in edges]


def properties(g, node):
    edges = sorted(g.outgoing(node, "CONTEM"), key=lambda e: e.get("ordem", 0))
    return [e.target for e in edges]


def tree(g, hlm):
    """Rows of the tree of a HLM: HLM, SM, USM and properties, in composition order.

    Each row: profundidade, tipo ('HLM'|'SM'|'USM'|'Propriedade'), nome, caminho (from the HLM),
    cardinalidade and papel (for models), and the node under 'no'.
    """
    return tree_from(g, hlm_node(g, hlm))


def tree_from(g, root):
    """Like tree(), from any model (paths are relative to it)."""
    rows = [{"profundidade": 0, "tipo": root.label, "nome": root["nome"], "caminho": "", "no": root,
             "descricao": root.get("descricao")}]

    def descend(node, depth, prefix):
        for p in properties(g, node):
            rows.append({"profundidade": depth, "tipo": "Propriedade", "nome": p["nome"],
                         "caminho": f"{prefix}{p['nome']}", "no": p, "descricao": p.get("descricao"),
                         "tipoBase": p.get("tipo"), "nomesAlternativos": list(p.get("nomesAlternativos") or [])})
        for edge, child in children(g, node):
            role = edge.get("papel") or child["nome"]
            path = f"{prefix}{role}"
            rows.append({"profundidade": depth, "tipo": child.label, "nome": child["nome"], "papel": role,
                         "caminho": path, "cardinalidade": edge.get("cardinalidade"), "no": child,
                         "descricao": child.get("descricao")})
            descend(child, depth + 1, path + ".")

    descend(root, 1, "")
    return rows


def without_node(row):
    """Copy of a tree row without the node reference (to serialise the ViewModel)."""
    return {k: v for k, v in row.items() if k != "no"}


def property_paths(g, hlm):
    return [(r["caminho"], r["no"]) for r in tree(g, hlm) if r["tipo"] == "Propriedade"]


def owner(g, prop):
    """The model that holds the property (USM, or SM for a residual property)."""
    return next(iter(g.sources(prop, "CONTEM")), None)


# ---------------------------------------------------------------------- rules
def rules_on(g, node):
    """Rules that live on a node (ASSOCIADA_A)."""
    return order_rules(g.sources(node, "ASSOCIADA_A"))


def restriction_of(g, rule):
    return g.first_target(rule, "RESTRITA_POR")


def condition_of(g, rule):
    return g.first_target(rule, "CONDICIONADA_POR")


def rule_of_restriction(g, restriction):
    return next(iter(g.sources(restriction, "RESTRITA_POR")), None)


def rule_of_condition(g, condition):
    return next(iter(g.sources(condition, "CONDICIONADA_POR")), None)


def calls(g, source, rule_id):
    """Function calls from a restriction or a condition, with the arguments they read."""
    out = []
    part = "termo" if source.label == "CondicaoAplicabilidade" else "restricao"
    for edge in g.outgoing(source, "CHAMA"):
        function = edge.target
        read = sorted([x for x in g.outgoing(function, "LE") if x.get("regra") == rule_id and x.get("parte") == part],
                      key=lambda x: x.get("posicao", 0))
        out.append({
            "funcao": function["nome"], "chamada": edge.get("chamada"), "operador": edge.get("operador"),
            "termo": edge.get("termo"), "descricaoFuncao": function.get("descricao"),
            "argumentos": [{"caminho": x.get("caminho"), "alvo": x.target.get("chave") or x.target.name,
                            "nomeAlvo": x.target.name, "rotuloAlvo": x.target.label,
                            "colecao": x.get("colecao", False)} for x in read],
            "contextos": [c["nome"] for c in g.targets(function, "DEPENDE_DE")],
        })
    return out


def terms(g, condition, rule_id):
    """Terms of a condition, in order: typed (TERMO) and functions (CHAMA)."""
    out = []
    for e in g.outgoing(condition, "TERMO"):
        out.append({"ordem": e.get("ordem", 0), "forma": "tipificado", "caminho": e.get("caminho"),
                    "propriedade": e.target.get("chave"), "operador": e.get("operador"),
                    "valor": read_json(e.get("valor")), "contexto": e.get("contexto"), "texto": e.get("texto")})
    for c in calls(g, condition, rule_id):
        out.append({"ordem": c["termo"] if c["termo"] is not None else 99, "forma": "funcao",
                    "operador": c["operador"], "texto": c["chamada"], "chamada": c})
    return sorted(out, key=lambda t: t["ordem"])


def rule_summary(g, rule):
    """Everything a rule declares, read from the graph."""
    rule_id = rule["id"]
    summary = {"id": rule_id, "tipo": rule.label, "natureza": rule.get("natureza"), "descricao": rule.get("descricao"),
               "alcance": rule.get("alcance"), "notas": rule.get("notas"),
               "contextosExternos": list(rule.get("contextosExternos") or [])}
    home = g.first_target(rule, "ASSOCIADA_A")
    summary["viveEm"] = {"rotulo": home.label, "nome": home.name} if home else None
    restriction = restriction_of(g, rule)
    if restriction is not None:
        r = {"forma": restriction.get("forma"), "operador": restriction.get("operador"),
             "mensagem": restriction.get("mensagem"), "texto": restriction.get("descricao")}
        if restriction.get("forma") == "funcao":
            found = calls(g, restriction, rule_id)
            r["chamada"] = found[0] if found else None
        else:
            e = next(iter(g.outgoing(restriction, "RESTRINGE")), None)
            if e is not None:
                r.update({"caminho": e.get("caminho"), "propriedade": e.target.get("chave"),
                          "valor": read_json(e.get("valor")), "minimo": e.get("minimo"), "maximo": e.get("maximo")})
        summary["restricao"] = r
    condition = condition_of(g, rule)
    if condition is not None:
        summary["condicao"] = terms(g, condition, rule_id)
    if rule.label == "RIC":
        summary["mensagem"] = rule.get("mensagem")
        summary["conclusao"] = {"tipo": rule.get("conclusaoTipo"), "valor": rule.get("conclusaoValor")}
    else:
        summary["mensagem"] = summary.get("restricao", {}).get("mensagem")
    summary["funcao"] = bool(restriction is not None and restriction.get("forma") == "funcao")
    return summary


def plausible_values(g, prop):
    """Plausible values (RP with IN or EQUALS living on the property), in declared order; None if there are none."""
    values = None
    for rule in g.sources(prop, "ASSOCIADA_A"):
        if rule.label != "RP":
            continue
        restriction = restriction_of(g, rule)
        if restriction is None or restriction.get("forma") != "tipificada":
            continue
        v = read_json(restriction.get("valor"))
        if restriction.get("operador") == "IN":
            values = (values or []) + [x for x in v if x not in (values or [])]
        elif restriction.get("operador") == "EQUALS":
            values = (values or []) + ([v] if v not in (values or []) else [])
    return values


def rule_prefixes(g, hlm, rule):
    """Prefixes (paths from the HLM) of the occurrences of the node where the rule lives."""
    home = g.first_target(rule, "ASSOCIADA_A")
    if home is None:
        return []
    if home.label == "Propriedade":
        home = owner(g, home)
    return [r["caminho"] for r in tree(g, hlm) if r["no"].id == home.id and r["tipo"] != "Propriedade"]


def join(prefix, path):
    return f"{prefix}.{path}" if prefix else path


def rules_of_hlm(g, hlm):
    """Rules that live on any node (or property) of the HLM's tree, each with the prefixes of its occurrences."""
    seen = {}
    for row in tree(g, hlm):
        prefix = row["caminho"] if row["tipo"] != "Propriedade" else row["caminho"].rpartition(".")[0]
        for rule in rules_on(g, row["no"]):
            seen.setdefault(rule["id"], (rule, []))[1].append(prefix)
    return list(seen.values())


# ---------------------------------------------------------------------- reuse (upwards)
def paths_to_hlm(g, node):
    """Composition paths, from each HLM down to the model: [[{rotulo, nome, papel, cardinalidade}, ...]]."""
    paths = []

    def climb(n, tail):
        parents = g.incoming(n, "COMPOSTO_POR")
        if not parents:
            paths.append(list(reversed(tail)))
            return
        for e in parents:
            climb(e.source, tail + [{"rotulo": e.source.label, "nome": e.source["nome"], "papel": e.get("papel"),
                                      "cardinalidade": e.get("cardinalidade")}])

    climb(node, [{"rotulo": node.label, "nome": node["nome"]}])
    return sorted(paths, key=lambda p: [x["nome"] for x in p])


def hlms_using(g, node):
    return sorted({p[0]["nome"] for p in paths_to_hlm(g, node) if p and p[0]["rotulo"] == "HLM"})


def model_chain(g, nodes):
    """Upward closure (CONTEM and COMPOSTO_POR) of a set of properties or models, up to the HLMs.

    Returns (nodes, edges): nodes {chave, rotulo, nome, descricao}, edges {de, para, tipo, papel, cardinalidade}.
    """
    seen, edges, queue = {}, [], list(nodes)
    while queue:
        n = queue.pop(0)
        if n.id in seen:
            continue
        seen[n.id] = n
        incoming = g.incoming(n, "CONTEM") if n.label == "Propriedade" else g.incoming(n, "COMPOSTO_POR")
        for e in sorted(incoming, key=lambda e: (node_key(e.source), e.get("papel") or "")):
            edges.append({"de": node_key(e.source), "para": node_key(n), "tipo": e.type,
                          "papel": e.get("papel"), "cardinalidade": e.get("cardinalidade")})
            queue.append(e.source)
    listed = [{"chave": node_key(n), "rotulo": n.label, "nome": n.name if n.label != "Propriedade" else n["nome"],
               "dono": n.get("dono"), "descricao": n.get("descricao"), "tipoBase": n.get("tipo")} for n in seen.values()]
    unique = []
    for e in edges:
        if e not in unique:
            unique.append(e)
    return listed, unique


def node_key(n):
    """Stable key of a node in the views: 'Propriedade:USM:Morada.pais', 'USM:Morada', 'Funcao:f', ..."""
    if n.label == "Propriedade":
        return f"Propriedade:{n['chave']}"
    return f"{n.label}:{n.name}"


def property_info(prop):
    return {"chave": prop["chave"], "nome": prop["nome"], "dono": prop.get("dono"), "nivelDono": prop.get("nivelDono"),
            "tipo": prop.get("tipo"), "descricao": prop.get("descricao")}


# ---------------------------------------------------------------------- rule card (for tables)
def rule_card(g, rule):
    """rule_summary plus the fields the views show separately: category, restriction target, term property names."""
    card = rule_summary(g, rule)
    restriction = card.get("restricao")
    card["categoria"] = "RIC" if card["tipo"] == "RIC" else ("FN" if card["funcao"] else card["tipo"])
    target = None
    if restriction and restriction.get("propriedade"):
        p = g.node("Propriedade", restriction["propriedade"])
        target = {"chave": p["chave"], "nome": p["nome"], "dono": p.get("dono")}
    elif restriction and restriction.get("chamada"):
        args = list(restriction["chamada"]["argumentos"])
        target = {"chave": args[0]["alvo"] if args else None, "nome": ", ".join(a["nomeAlvo"] for a in args) or None,
                  "funcao": restriction["chamada"]["funcao"]}
    card["alvo"] = target
    for t in card.get("condicao", []):
        if t.get("propriedade"):
            t["nome"] = g.node("Propriedade", t["propriedade"])["nome"]
    home = g.first_target(rule, "ASSOCIADA_A")
    card["viveEm"] = {"rotulo": home.label, "nome": home.name if home.label != "Propriedade" else home["nome"],
                      "chave": node_key(home), "dono": home.get("dono")}
    card["funcoes"] = sorted({c["funcao"] for c in ([restriction["chamada"]] if restriction and restriction.get("chamada") else [])}
                             | {t["chamada"]["funcao"] for t in card.get("condicao", []) if t["forma"] == "funcao"})
    return card
