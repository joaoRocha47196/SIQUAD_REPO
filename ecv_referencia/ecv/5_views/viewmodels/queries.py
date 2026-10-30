"""Query ViewModels (thesis, section 'Operações orientadas à consulta'): dependencies, impact, gaps and
operators. Each one starts at a node and follows one kind of edge."""
from ecv.graph.base import read_json

from . import common as K
from .evaluation import evaluate

DECIDING_OPERATORS = ("EQUALS", "IN", "NOT_EQUALS")


def _rules_whose_condition_reads(g, prop):
    """Rules whose condition reads the property: through TERMO, or through LE of a function called in a term."""
    found = {}
    for e in g.incoming(prop, "TERMO"):
        rule = K.rule_of_condition(g, e.source)
        if rule is not None:
            found.setdefault(rule["id"], (rule, []))[1].append(e.get("texto"))
    for e in g.incoming(prop, "LE"):
        if e.get("parte") == "termo":
            rule = next((x for x in g.nodes("Regra") if x["id"] == e.get("regra")), None)
            if rule is not None:
                found.setdefault(rule["id"], (rule, []))[1].append(f"{e.source['nome']}(… {e.get('caminho')} …)")
    return list(found.values())


def _rule_targets(g, rule):
    """Properties (or models) the restriction of a rule checks."""
    restriction = K.restriction_of(g, rule)
    if restriction is None:
        return []
    targets = [{"chave": e.target.get("chave"), "nome": e.target.name, "caminho": e.get("caminho")}
               for e in g.outgoing(restriction, "RESTRINGE")]
    for c in K.calls(g, restriction, rule["id"]):
        targets += [{"chave": x["alvo"], "nome": x["nomeAlvo"], "caminho": x["caminho"]} for x in c["argumentos"]]
    return targets


def _is_deciding(term):
    return term["forma"] == "tipificado" and not term.get("contexto") and term["operador"] in DECIDING_OPERATORS


# ---------------------------------------------------------------------- dependencies
def dependencies(g, propriedade):
    """Validity dependency analysis: which restrictions and conclusions does each value of this property imply?

    Propriedade <-TERMO- CondicaoAplicabilidade <-CONDICIONADA_POR- RIR/RIC
    -RESTRITA_POR-> Restricao -RESTRINGE-> Propriedade (or -CHAMA-> Funcao -LE-> targets);
    also Propriedade <-LE {parte: termo}- Funcao (the property is an argument of a function in a term).

    The values come from the property's RP (plausible) and from the terms that read it. For each value, a
    selection term (EQUALS, IN, NOT_EQUALS) says whether the rule applies; the other terms (ranges, contexts,
    functions) go to 'outrosTermos', because the value alone does not decide them.
    """
    prop = K.property_node(g, propriedade)
    key = prop["chave"]
    cards, focus = [], {}
    for rule, _ in _rules_whose_condition_reads(g, prop):
        card = K.rule_card(g, rule)
        focus_terms = []
        for t in card.get("condicao", []):
            if t["forma"] == "tipificado":
                t["foco"] = t.get("propriedade") == key
            else:
                t["foco"] = any(a["alvo"] == key for a in t["chamada"]["argumentos"])
            if t["foco"]:
                focus_terms.append(t)
        card["alvos"] = _rule_targets(g, rule)
        cards.append(card)
        focus[card["id"]] = focus_terms
    cards.sort(key=lambda x: (K.RULE_TYPE_ORDER.get(x["tipo"], 9), x["id"]))

    plausible = K.plausible_values(g, prop) or []
    used = []
    for card in cards:
        for t in focus[card["id"]]:
            if _is_deciding(t):
                for v in (t["valor"] if t["operador"] == "IN" else [t["valor"]]):
                    if v not in used:
                        used.append(v)
    values = list(plausible) + [v for v in used if v not in plausible]

    def applies(card, value):
        """True/False when the focus terms decide the rule for the value; None if one of them is not a selection term."""
        result = True
        for t in focus[card["id"]]:
            if not _is_deciding(t):
                return None
            result = result and bool(evaluate(t["operador"], value, t["valor"]))
        return result

    by_value = []
    for v in values:
        found = [c for c in cards if applies(c, v)]
        affected = []
        for c in found:
            for a in c["alvos"] or [{"chave": None, "nome": "(conclusão)"}]:
                if a not in affected:
                    affected.append(a)
        by_value.append({"valor": v, "plausivel": not plausible or v in plausible, "regras": [c["id"] for c in found],
                         "afetadas": affected, "semRegras": not found})
    others = [c["id"] for c in cards if any(applies(c, v) is None for v in values) or not values]
    affected_all = {}
    for c in cards:
        for a in c["alvos"] or [{"chave": None, "nome": "(conclusão)"}]:
            affected_all.setdefault(a["chave"] or "(conclusão)", {**a, "regras": []})["regras"].append(c["id"])
    return {"vista": "dependencias", "titulo": f"Dependências de validade de {prop['dono']}.{prop['nome']}",
            "propriedade": K.property_info(prop), "plausiveis": plausible,
            "rp": [{"id": r["id"], "texto": r.get("descricao")} for r in g.sources(prop, "ASSOCIADA_A") if r.label == "RP"],
            "valores": by_value, "outrosTermos": others, "regras": cards, "afetadas": list(affected_all.values())}


# ---------------------------------------------------------------------- impact
def impact(g, propriedade):
    """Rules, projections and profiles affected by a change of the property (name, values or position).

    Propriedade <-RESTRINGE- Restricao <-RESTRITA_POR- Regra (target);
    Propriedade <-TERMO- Condicao <-CONDICIONADA_POR- Regra (term);
    Propriedade <-LE- Funcao (argument of a call, with the rule);
    Propriedade <-ASSOCIADA_A- Regra (lives on the property);
    Propriedade <-OBRIGATORIA|PERMITIDA- Projecao; Propriedade <-FIXA- Perfil.
    """
    prop = K.property_node(g, propriedade)
    uses = {}

    def add(rule, role):
        entry = uses.setdefault(rule["id"], {"id": rule["id"], "tipo": rule.label, "descricao": rule.get("descricao"), "papeis": []})
        if role not in entry["papeis"]:
            entry["papeis"].append(role)

    for e in g.incoming(prop, "RESTRINGE"):
        add(K.rule_of_restriction(g, e.source), "alvo da restrição")
    for e in g.incoming(prop, "TERMO"):
        add(K.rule_of_condition(g, e.source), "termo da condição")
    rules_by_id = {r["id"]: r for r in g.nodes("Regra")}
    for e in g.incoming(prop, "LE"):
        add(rules_by_id[e.get("regra")], f"argumento de {e.source['nome']} ({e.get('parte')})")
    for rule in g.sources(prop, "ASSOCIADA_A"):
        add(rule, "vive na propriedade")
    projections = [{"projecao": e.source["nome"], "tipo": e.type.lower(), "caminho": e.get("caminho")}
                   for t in ("OBRIGATORIA", "PERMITIDA") for e in g.incoming(prop, t)]
    profiles = [{"perfil": e.source["nome"], "caminho": e.get("caminho"), "valor": read_json(e.get("valor"))}
                for e in g.incoming(prop, "FIXA")]
    listed = sorted(uses.values(), key=lambda x: (K.RULE_TYPE_ORDER.get(x["tipo"], 9), x["id"]))
    return {"vista": "impacto", "titulo": f"Impacto de uma alteração de {prop['nome']} ({prop['dono']})",
            "propriedade": propriedade, "nome": prop["nome"], "regras": listed,
            "contagem": {t: sum(1 for x in listed if x["tipo"] == t) for t in ("RP", "RIR", "RIC")},
            "projecoes": sorted(projections, key=lambda x: (x["projecao"], x["caminho"])), "perfis": profiles}


# ---------------------------------------------------------------------- gaps
def gaps(g, hlm, projecoes=None):
    """Properties without rules and properties never projected.

    Without rules: no RESTRINGE, ASSOCIADA_A or LE edge reaches the property (it may be read only in terms).
    Never projected: no OBRIGATORIA or PERMITIDA edge of the considered projections reaches the path.
    """
    root = K.hlm_node(g, hlm)
    projs = sorted((p for p in g.sources(root, "PROJETA") if projecoes is None or p["nome"] in projecoes),
                   key=lambda p: p["nome"])
    projected = {e.get("caminho") for p in projs for t in ("OBRIGATORIA", "PERMITIDA") for e in g.outgoing(p, t)}
    without_rules, never, seen = [], [], set()
    for path, prop in K.property_paths(g, hlm):
        if prop.id not in seen:
            seen.add(prop.id)
            if not (g.incoming(prop, "RESTRINGE") or g.incoming(prop, "ASSOCIADA_A") or g.incoming(prop, "LE")):
                in_terms = [K.rule_of_condition(g, e.source)["id"] for e in g.incoming(prop, "TERMO")]
                without_rules.append({"propriedade": prop["chave"], "nome": prop["nome"], "dono": prop["dono"],
                                      "lidaEmTermos": sorted(set(in_terms))})
        if path not in projected:
            never.append({"caminho": path, "propriedade": prop["chave"]})
    return {"vista": "lacunas", "titulo": f"Lacunas do HLM {hlm}", "hlm": hlm,
            "projecoesConsideradas": [p["nome"] for p in projs], "semRegras": without_rules, "nuncaProjetadas": never}


# ---------------------------------------------------------------------- operators
def operators(g):
    """Navigation by kind of check: restrictions and terms grouped by the catalogue operator, and the
    properties treated as enumerations (with an RP IN)."""
    groups = {}

    def group(op):
        return groups.setdefault(op, {"restricoes": [], "termos": []})

    for restriction in g.nodes("Restricao"):
        group(restriction.get("operador"))["restricoes"].append({"regra": restriction.get("regra"), "texto": restriction.get("descricao")})
    for condition in g.nodes("CondicaoAplicabilidade"):
        for e in g.outgoing(condition, "TERMO"):
            group(e.get("operador"))["termos"].append({"regra": condition.get("regra"), "texto": e.get("texto")})
        for e in g.outgoing(condition, "CHAMA"):
            group(e.get("operador"))["termos"].append({"regra": condition.get("regra"), "texto": e.get("chamada")})
    enumerations = []
    for p in sorted(g.nodes("Propriedade"), key=lambda x: x["chave"]):
        values = K.plausible_values(g, p)
        if values is not None:
            enumerations.append({"propriedade": p["chave"], "valores": values})
    ops = [{"operador": op, "restricoes": sorted(x["restricoes"], key=lambda y: (y["regra"], y["texto"])),
            "termos": sorted(x["termos"], key=lambda y: (y["regra"], y["texto"]))} for op, x in sorted(groups.items())]
    return {"vista": "operadores", "titulo": "Verificações por operador e enumerados", "operadores": ops,
            "enumerados": enumerations}
