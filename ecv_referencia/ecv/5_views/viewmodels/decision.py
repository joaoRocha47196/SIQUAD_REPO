"""Decision ViewModels: the decision view (matrix and tree over the same data) and the coherence between rules.

They start from a restricted property and follow, backwards, the RESTRINGE edges (to the
restrictions), RESTRITA_POR (to the RIR) and from there CONDICIONADA_POR and TERMO (to the
discriminating factors). No decision structure is stored: the matrix and the tree derive from the rules.
"""
from itertools import product

from ecv import config
from ecv.graph.base import read_json

from . import common as K

SELECTION_OPERATORS = config.SELECTION_OPERATORS


def _term_values(term):
    v = term["valor"]
    return list(v) if term["operador"] == "IN" else [v]


def _is_selection(term):
    return term["forma"] == "tipificado" and term["operador"] in SELECTION_OPERATORS and term.get("contexto") is None


def rules_for_target(g, prop, types=("RIR",)):
    """Rules whose typed restriction targets the property, with their selection terms."""
    out = []
    for edge in g.incoming(prop, "RESTRINGE"):
        rule = K.rule_of_restriction(g, edge.source)
        if rule is None or rule.label not in types:
            continue
        condition = K.condition_of(g, rule)
        terms = K.terms(g, condition, rule["id"]) if condition is not None else []
        out.append({"id": rule["id"], "tipo": rule.label, "operador": edge.get("operador"), "valor": read_json(edge.get("valor")),
                    "texto": edge.get("texto"), "minimo": edge.get("minimo"), "maximo": edge.get("maximo"),
                    "selecao": {t["propriedade"]: _term_values(t) for t in terms if _is_selection(t)},
                    "outrosTermos": [t["texto"] for t in terms if not _is_selection(t)],
                    "mensagem": K.restriction_of(g, rule).get("mensagem")})
    return sorted(out, key=lambda x: x["id"])


def _dimensions(g, rules):
    """Properties used in selection terms, from the most to the least frequent."""
    frequency, order = {}, []
    for r in rules:
        for key in r["selecao"]:
            if key not in frequency:
                order.append(key)
            frequency[key] = frequency.get(key, 0) + 1
    dims = []
    for key in sorted(order, key=lambda k: (-frequency[k], order.index(k))):
        node = g.node("Propriedade", key)
        used = []
        for r in rules:
            for v in r["selecao"].get(key, []):
                if v not in used:
                    used.append(v)
        plausible = K.plausible_values(g, node) if node else None
        ordered = [v for v in (plausible or []) if v in used] + [v for v in used if not plausible or v not in plausible]
        dims.append({"chave": key, "nome": node["nome"] if node else key, "frequencia": frequency[key],
                     "plausiveis": plausible, "usados": ordered,
                     "ausenteEm": sum(1 for r in rules if key not in r["selecao"])})
    return dims


def _find_dimension(dims, ref):
    for d in dims:
        if ref in (d["chave"], d["nome"]):
            return d
    raise ValueError(f"'{ref}' não é usado nas condições; dimensões: {[d['nome'] for d in dims]}")


def _disjoint(a, b):
    return a["minimo"] is not None and b["minimo"] is not None and (a["maximo"] < b["minimo"] or b["maximo"] < a["minimo"])


# ---------------------------------------------------------------------- decision matrix
def matrix(g, target, rows=None):
    """Decision matrix of a restricted property: values of one dimension in the rows, combinations of
    the others in the columns and, in each cell, the expected value (the RIR's restriction).

    Flags: cells without a rule (grey), ranges without a common value with the general range of the
    column (red), rows with values outside the plausible ones and plausible rows without any rule.
    """
    prop = K.property_node(g, target)
    rules = rules_for_target(g, prop)
    placed = [r for r in rules if not r["outrosTermos"]]
    dims = _dimensions(g, placed)
    if not dims:
        return {"linhas": [], "colunas": [], "dimensoesColunas": [], "dimensaoLinhas": None, "outras": rules}
    row_dim = max(dims, key=lambda d: (d["ausenteEm"], len(d["usados"]))) if rows is None else _find_dimension(dims, rows)
    col_dims = [d for d in dims if d is not row_dim]

    cells, columns = {}, []          # columns: combinations (value or None) of the other dimensions some rule uses
    for r in placed:
        lists = [r["selecao"].get(d["chave"], [None]) for d in col_dims]
        for combo in product(*lists):
            for row_value in r["selecao"].get(row_dim["chave"], [None]):
                cells.setdefault((row_value, combo), []).append(r)
                if combo not in columns:
                    columns.append(combo)

    def column_order(combo):
        return tuple((-1 if v is None else (d["usados"].index(v) if v in d["usados"] else 999)) for d, v in zip(col_dims, combo))

    columns.sort(key=column_order)
    plausible = row_dim["plausiveis"] or []
    row_values = [None] + list(plausible) + [v for v in row_dim["usados"] if v not in plausible]

    def entry(r):
        return {"id": r["id"], "valor": r["valor"], "texto": r["texto"], "minimo": r["minimo"], "maximo": r["maximo"],
                "mensagem": r["mensagem"]}

    row_list = []
    for row_value in row_values:
        row_cells = []
        for combo in columns:
            found = cells.get((row_value, combo), [])
            state = "vazia" if not found else "ok"
            if len(found) > 1 and len({str(x["valor"]) for x in found}) > 1:
                state = "conflito"
            if found and row_value is not None:
                general = cells.get((None, combo), [])
                if any(_disjoint(r, gr) for r in found for gr in general):
                    state = "incoerente"
            row_cells.append({"estado": state, "regras": [entry(r) for r in found]})
        row_list.append({"valor": row_value, "rotulo": "(qualquer)" if row_value is None else str(row_value),
                         "plausivel": row_value is None or not plausible or row_value in plausible,
                         "semRegras": row_value is not None and all(c["estado"] == "vazia" for c in row_cells),
                         "celulas": row_cells})
    column_list = [{"valores": [{"propriedade": d["nome"], "valor": v} for d, v in zip(col_dims, combo)],
                    "rotulo": " · ".join(str(v) for v in combo if v is not None) or "(qualquer)"} for combo in columns]
    return {"propriedade": prop["nome"], "dimensaoLinhas": row_dim["nome"], "dimensoesColunas": [d["nome"] for d in col_dims],
            "dimensoes": dims, "colunas": column_list, "linhas": row_list,
            "outras": [entry(r) | {"termos": r["outrosTermos"]} for r in rules if r["outrosTermos"]]}


# ---------------------------------------------------------------------- applicability tree
def _union(intervals):
    out = []
    for a, b in sorted(intervals):
        if out and a <= out[-1][1]:
            out[-1][1] = max(out[-1][1], b)
        else:
            out.append([a, b])
    return out


def _gaps(reference, intervals):
    """Parts of the reference interval not covered by the given intervals."""
    missing, start = [], reference[0]
    for a, b in _union(intervals):
        if b < reference[0] or a > reference[1]:
            continue
        if a > start:
            missing.append([start, a])
        start = max(start, b)
    if start < reference[1]:
        missing.append([start, reference[1]])
    return missing


def applicability_tree(g, target, filter_values=None):
    """Decision tree derived from the RIR that restrict the property (thesis, figures 'gamas' and 'pesquisa').

    filter_values: {property name: value}, to fix part of the dimensions (e.g. TEMPERATURA and °C).
    Each dimension branches by the values used; '(qualquer)' gathers the rules that do not condition it.
    Flags values outside the plausible ones (the rule never applies), plausible values without a branch
    and, in a dimension whose branches are ranges, the values of the general range no branch covers.
    """
    prop = K.property_node(g, target)
    rules = [r for r in rules_for_target(g, prop) if not r["outrosTermos"]]
    dims = _dimensions(g, rules)
    filter_values = filter_values or {}
    fixed = []
    for name, value in filter_values.items():
        d = _find_dimension(dims, name)
        rules = [r for r in rules if d["chave"] not in r["selecao"] or value in r["selecao"][d["chave"]]]
        fixed.append({"propriedade": d["nome"], "valor": value})
    dims = [d for d in _dimensions(g, rules) if d["nome"] not in filter_values]

    def leaf(found):
        return [{"id": r["id"], "texto": r["texto"], "minimo": r["minimo"], "maximo": r["maximo"]} for r in found]

    def build(found, remaining):
        remaining = [d for d in remaining if any(d["chave"] in r["selecao"] for r in found)]
        if not remaining:
            return {"tipo": "regras", "regras": leaf(found)}
        d = remaining[0]
        branches = []
        unconditioned = [r for r in found if d["chave"] not in r["selecao"]]
        if unconditioned:
            branches.append({"valor": None, "rotulo": "(qualquer)", "plausivel": True, "filho": build(unconditioned, remaining[1:])})
        used = [v for v in d["usados"] if any(v in r["selecao"].get(d["chave"], []) for r in found)]
        for v in used:
            subset = [r for r in found if v in r["selecao"].get(d["chave"], [])]
            branches.append({"valor": v, "rotulo": str(v), "plausivel": not d["plausiveis"] or v in d["plausiveis"],
                             "filho": build(subset, remaining[1:])})
        node = {"tipo": "dimensao", "propriedade": d["nome"], "chave": d["chave"], "ramos": branches,
                "semRamo": [v for v in (d["plausiveis"] or []) if v not in used]}
        general = [x for x in (branches[0]["filho"].get("regras", []) if unconditioned else []) if x["minimo"] is not None]
        specific = [x for b in branches if b["valor"] is not None and b["plausivel"]
                    for x in b["filho"].get("regras", []) if x["minimo"] is not None]
        if general and specific:          # coverage: general range (qualquer) vs ranges of the plausible branches
            reference = [general[0]["minimo"], general[0]["maximo"]]
            node["cobertura"] = {"referencia": reference, "regraReferencia": general[0]["id"],
                                 "naoCobertos": _gaps(reference, [[x["minimo"], x["maximo"]] for x in specific])}
        return node

    return {"propriedade": prop["nome"], "filtro": fixed, "raiz": build(rules, dims)}


# ---------------------------------------------------------------------- decision view
def _plausibility_rules(g, prop):
    """RP that restrict the property (what it may take, always)."""
    return [{"id": r["id"], "texto": r["texto"], "mensagem": r["mensagem"], "operador": r["operador"], "valor": r["valor"]}
            for r in rules_for_target(g, prop, types=("RP",))]


def decision(g, alvo, linhas=None, filtro=None):
    """Decision view of a property restricted by RIR: the same data as a matrix and as a tree.

    On top, the RP of the target and of the discriminating factors (the values each can take); then the
    matrix (one dimension in the rows, the others in the columns) and the tree (one dimension per level);
    finally each RIR with all its information.
    """
    prop = K.property_node(g, alvo)
    rules = rules_for_target(g, prop)
    rir_nodes = {r["id"]: r for r in g.nodes("RIR")}
    cards = {r["id"]: K.rule_card(g, rir_nodes[r["id"]]) for r in rules}
    dims = []
    for d in _dimensions(g, [r for r in rules if not r["outrosTermos"]]):
        p = g.node("Propriedade", d["chave"])
        dims.append({**d, "dono": p.get("dono"), "descricao": p.get("descricao"), "tipo": p.get("tipo"),
                     "rp": _plausibility_rules(g, p)})
    m = matrix(g, alvo, linhas)
    t = applicability_tree(g, alvo, filtro)
    title = f"Decisão de {prop['dono']}.{prop['nome']}"
    if t["filtro"]:
        title += " (" + ", ".join(f"{f['propriedade']} = {f['valor']}" for f in t["filtro"]) + ")"
    return {"vista": "decisao", "titulo": title, "alvo": alvo,
            "propriedade": {**K.property_info(prop), "rp": _plausibility_rules(g, prop)},
            "dimensoes": dims, "matriz": m, "arvore": t["raiz"], "filtro": t["filtro"],
            "regras": [cards[r["id"]] for r in rules]}


# ---------------------------------------------------------------------- coherence
def _terms_outside_plausible(g):
    out = []
    for condition in g.nodes("CondicaoAplicabilidade"):
        for e in g.outgoing(condition, "TERMO"):
            if e.get("operador") not in SELECTION_OPERATORS or e.get("contexto"):
                continue
            plausible = K.plausible_values(g, e.target)
            values = read_json(e.get("valor"))
            values = values if isinstance(values, list) else [values]
            if plausible is not None:
                outside = [v for v in values if v not in plausible]
                if outside:
                    out.append({"regra": condition["regra"], "propriedade": e.target["chave"], "valores": outside,
                                "plausiveis": plausible})
    return out


def _incompatible_ranges(g):
    out = []
    for prop in g.nodes("Propriedade"):
        ranges = [r for r in rules_for_target(g, prop, types=("RP", "RIR")) if r["minimo"] is not None and not r["outrosTermos"]]
        for i, a in enumerate(ranges):
            for b in ranges[i + 1:]:
                compatible = all(set(a["selecao"][k]) & set(b["selecao"][k]) for k in set(a["selecao"]) & set(b["selecao"]))
                if compatible and _disjoint(a, b):
                    out.append({"propriedade": prop["chave"], "regras": [{"id": x["id"], "texto": x["texto"]} for x in (a, b)]})
    return out


def _same_condition(g):
    groups = {}
    for condition in g.nodes("CondicaoAplicabilidade"):
        signature = tuple(sorted((e.target["chave"], e.get("operador"), str(e.get("valor")), str(e.get("contexto")))
                                 for e in g.outgoing(condition, "TERMO")))
        calls = tuple(sorted(e.get("chamada") for e in g.outgoing(condition, "CHAMA")))
        groups.setdefault((signature, calls), []).append(condition["regra"])
    same = []
    for (signature, calls), ids in groups.items():
        if len(ids) > 1:
            text = " e ".join([f"{k} {o} {v if v != 'None' else c}" for k, o, v, c in signature] + list(calls))
            same.append({"condicao": text, "regras": sorted(ids)})
    return sorted(same, key=lambda x: x["condicao"])


def coherence(g):
    """Coherence problems between rules, detectable without running anything:

    - terms with values outside the plausible values (the rule never applies to those values);
    - pairs of rules that apply to the same situation and require ranges without a common value;
    - rules with exactly the same applicability condition (candidates to review together).
    """
    return {"vista": "coerencia", "titulo": "Coerência entre regras", "foraDosPlausiveis": _terms_outside_plausible(g),
            "incompativeis": _incompatible_ranges(g), "mesmaCondicao": _same_condition(g)}
