"""Guides for the operations: what has to be chosen for each operation and the operation already filled in.

For every operation of the vocabulary, SELECTORS says which existing entities the person picks (a model, one
of its properties, a rule, a projection, ...); `prefill(ds, op, selection)` returns the operation with the
fields filled from the declarations: the current values to change, the paths of a HLM for a projection, the
JSON of a rule to replace. `options(ds, selector, selection)` lists what can be picked.

Selections use plain strings: modelo 'USM:Morada', propriedade 'codigoPostal', regra 'RP-CP', hlm 'Fatura',
projecao, perfil, funcao, contexto (names) and filho 'SM:Linhas' (a composition of the chosen model).
"""
import copy

from ecv.ingestion import paths as P
from ecv.ingestion.declaration import Declaration

from .operations import vocabulary

SELECTORS = {
    "criar_modelo": [], "remover_modelo": ["modelo"], "renomear_modelo": ["modelo"], "alterar_modelo": ["modelo"],
    "fundir_modelos": ["modelo"], "extrair_usm": ["modelo"], "criar_hlm": [], "remover_hlm": ["hlm"],
    "adicionar_propriedade": ["modelo"], "remover_propriedade": ["modelo", "propriedade"], "mover_propriedade": ["modelo", "propriedade"],
    "renomear_propriedade": ["modelo", "propriedade"], "alterar_propriedade": ["modelo", "propriedade"],
    "compor": ["modelo"], "remover_composicao": ["modelo", "filho"], "alterar_composicao": ["modelo", "filho"],
    "adicionar_regra": ["modelo"], "substituir_regra": ["regra"], "remover_regra": ["regra"], "mover_regra": ["regra"],
    "definir_projecao": ["hlm", "projecao"], "remover_projecao": ["projecao"], "definir_perfil": ["projecao", "perfil"],
    "remover_perfil": ["perfil"], "definir_funcao": ["funcao"], "remover_funcao": ["funcao"], "definir_contexto": ["contexto"],
    "remover_contexto": ["contexto"], "mapear": [],
}
LABELS = {"modelo": "Modelo", "propriedade": "Propriedade", "regra": "Regra", "hlm": "HLM", "projecao": "Projeção",
          "perfil": "Perfil", "funcao": "Função", "contexto": "Contexto externo", "filho": "Composição"}
OPTIONAL = {("adicionar_regra", "propriedade"), ("definir_projecao", "projecao"), ("definir_perfil", "perfil"),
            ("definir_funcao", "funcao"), ("definir_contexto", "contexto")}
LEVELS = ("HLM", "SM", "USM")


def _split(model_key):
    level, _, name = (model_key or "").partition(":")
    return (level, name) if level in LEVELS and name else (None, None)


def _unique(items, key):
    seen, out = set(), []
    for x in items:
        if x[key] not in seen:
            seen.add(x[key])
            out.append(x)
    return out


def section_items(ds, section):
    if ds is None:
        return []
    return _unique([x for d in ds.everything() for x in d.get(section, [])], "nome")


def rules(ds, kinds=None):
    """[(rule, level, model, property name or None)] of every rule (each id once)."""
    seen, out = set(), []
    for d in ds.declarations.values():
        for site in Declaration(d).rules():
            if site.id in seen or (kinds and site.type not in kinds):
                continue
            seen.add(site.id)
            out.append((site.rule, site.level, site.model, site.prop["nome"] if site.prop else None))
    return out


def find_rule(ds, rule_id):
    return next(((r, lv, m, p) for r, lv, m, p in rules(ds) if r["id"] == rule_id), None)


def hlm_paths(ds, hlm):
    """Every property path of a HLM (for a projection)."""
    d = ds.declarations.get(hlm)
    return P.all_property_paths(Declaration(d), "HLM", hlm) if d else []


# ---------------------------------------------------------------------- options of a selector
def options(ds, selector, selection, rule_kinds=None):
    """[(value, text)] that can be picked for the selector, given what is already selected."""
    if selector == "modelo":
        return [(f"{lv}:{m['nome']}", f"{lv} {m['nome']}") for lv in LEVELS for m in section_items(ds, lv.lower())]
    if selector == "hlm":
        return [(h, h) for h in ds.declarations]
    if selector == "propriedade":
        level, name = _split(selection.get("modelo"))
        model = ds.definition(level, name) if level else None
        return [(p["nome"], f"{p['nome']} ({p.get('tipo')})") for p in (model or {}).get("propriedades", [])]
    if selector == "filho":
        level, name = _split(selection.get("modelo"))
        model = ds.definition(level, name) if level else None
        out = []
        for c in (model or {}).get("composicao", []):
            child_level = "SM" if "sm" in c else "USM"
            child = c.get("sm") or c.get("usm")
            out.append((f"{child_level}:{child}:{c.get('papel') or ''}", f"{c.get('papel') or child} → {child_level} {child} [{c.get('cardinalidade')}]"))
        return out
    if selector == "regra":
        return [(r["id"], f"{r['id']} · {lv} {m}{'.' + p if p else ''}") for r, lv, m, p in rules(ds, rule_kinds)]
    if selector == "projecao":
        items = section_items(ds, "projecoes")
        if selection.get("hlm"):
            items = [x for x in items if x.get("hlm") == selection["hlm"]]
        return [(x["nome"], f"{x['nome']} ({x.get('hlm')})") for x in items]
    if selector == "perfil":
        items = section_items(ds, "perfis")
        if selection.get("projecao"):
            items = [x for x in items if x.get("projecao") == selection["projecao"]]
        return [(x["nome"], x["nome"]) for x in items]
    if selector == "funcao":
        return [(x["nome"], x["nome"]) for x in section_items(ds, "funcoes")]
    if selector == "contexto":
        return [(x["nome"], x["nome"]) for x in section_items(ds, "contextosExternos")]
    return []


# ---------------------------------------------------------------------- the operation filled in
def _rule_skeleton(layer, prop):
    target = prop or "<propriedade>"
    if layer == "C":
        return {"id": "RP-<ASSUNTO>", "natureza": "plausibilidade",
                "restricao": {"propriedade": target, "operador": "IN", "valor": [], "mensagem": "<o que falhou e o que se espera>"}}
    if layer == "E":
        return {"id": "RP-<ASSUNTO>", "natureza": "plausibilidade",
                "restricao": {"operador": "FUNCTION", "chamada": {"funcao": "<funcao>", "argumentos": [{"caminho": target}]},
                              "mensagem": "<o que falhou>"}}
    return {"id": "RIR-<ASSUNTO>", "natureza": "inferencia_restritiva",
            "condicao": [{"propriedade": "<fator discriminante>", "operador": "EQUALS", "valor": "<valor>"}],
            "restricao": {"propriedade": target, "operador": "RANGE", "valor": [0, 0], "mensagem": "<o que falhou e o que se espera>"}}


def prefill(ds, op, selection, layer=None):
    """The operation `op` with every field the selection determines filled in (placeholders <…> for the rest)."""
    level, name = _split(selection.get("modelo"))
    model = ds.definition(level, name) if level and ds is not None else None
    prop_name = selection.get("propriedade")
    prop = next((p for p in (model or {}).get("propriedades", []) if p["nome"] == prop_name), None)
    where = {"nivel": level or "<nivel>", "modelo": name or "<modelo>"}
    s = selection
    if op == "criar_modelo":
        return {"op": op, "nivel": "USM", "nome": "<NomeDoModelo>", "descricao": "<descrição>",
                "propriedades": [{"nome": "<nome>", "tipo": "texto", "descricao": "<descrição>"}]}
    if op == "remover_modelo":
        return {"op": op, **where, "nome": name} if model else {"op": op, "nivel": "<nivel>", "nome": "<nome>"}
    if op == "renomear_modelo":
        return {"op": op, "nivel": level, "de": name, "para": "<NovoNome>"}
    if op == "alterar_modelo":
        return {"op": op, "nivel": level, "nome": name, "descricao": (model or {}).get("descricao"), "notas": (model or {}).get("notas", "")}
    if op == "fundir_modelos":
        return {"op": op, "nivel": level, "de": [name], "para": "<modelo que fica>"}
    if op == "extrair_usm":
        return {"op": op, "de": where, "propriedades": [p["nome"] for p in (model or {}).get("propriedades", [])][:2],
                "novo": {"nome": "<NovoUsm>", "descricao": "<descrição>"}, "cardinalidade": "0..1"}
    if op == "criar_hlm":
        return {"op": op, "nome": "<NomeDoHlm>", "descricao": "<descrição>", "composicao": [{"sm": "<SM>", "cardinalidade": "1..1"}]}
    if op == "remover_hlm":
        return {"op": op, "nome": s.get("hlm")}
    if op == "adicionar_propriedade":
        return {"op": op, **where, "propriedade": {"nome": "<nome>", "tipo": "texto", "descricao": "<descrição>"}}
    if op == "remover_propriedade":
        return {"op": op, **where, "nome": prop_name}
    if op == "mover_propriedade":
        return {"op": op, "de": where, "para": {"nivel": "<nivel>", "modelo": "<modelo>"}, "nome": prop_name}
    if op == "renomear_propriedade":
        return {"op": op, **where, "de": prop_name, "para": "<novoNome>"}
    if op == "alterar_propriedade":
        return {"op": op, **where, "nome": prop_name, "tipo": (prop or {}).get("tipo"), "descricao": (prop or {}).get("descricao"),
                "nomesAlternativos": (prop or {}).get("nomesAlternativos", [])}
    if op == "compor":
        return {"op": op, "pai": {"nivel": level, "nome": name}, "filho": {"nivel": "USM", "nome": "<modelo>"},
                "cardinalidade": "0..1", "papel": "<Papel (opcional)>"}
    if op in ("remover_composicao", "alterar_composicao"):
        child_level, child, role = (s.get("filho") or "::").split(":", 2)
        base = {"op": op, "pai": {"nivel": level, "nome": name}, "filho": {"nivel": child_level, "nome": child}}
        if role:
            base["papel"] = role
        if op == "alterar_composicao":
            current = next((c for c in (model or {}).get("composicao", []) if (c.get("sm") or c.get("usm")) == child
                            and (c.get("papel") or "") == role), {})
            base["cardinalidade"] = current.get("cardinalidade")
            base["novoPapel"] = role or child
        return base
    if op == "adicionar_regra":
        return {"op": op, "onde": {**where, **({"propriedade": prop_name} if prop_name else {})},
                "regra": _rule_skeleton(layer, prop_name if layer in ("C", "E") else (prop_name or "<alvo>"))}
    if op in ("substituir_regra", "remover_regra", "mover_regra"):
        found = find_rule(ds, s.get("regra")) if ds is not None else None
        if op == "remover_regra":
            return {"op": op, "id": s.get("regra")}
        if op == "mover_regra":
            return {"op": op, "id": s.get("regra"), "para": {"nivel": found[1] if found else "<nivel>", "modelo": found[2] if found else "<modelo>"}}
        rule = copy.deepcopy(found[0]) if found else {}
        rule.pop("descricao", None)                       # derived by the code
        return {"op": op, "id": s.get("regra"), "regra": rule}
    if op == "definir_projecao":
        existing = next((x for x in section_items(ds, "projecoes") if x["nome"] == s.get("projecao")), None)
        if existing:
            return {"op": op, "projecao": copy.deepcopy(existing)}
        return {"op": op, "projecao": {"nome": "<NomeDaProjecao>", "hlm": s.get("hlm") or "<HLM>", "descricao": "<utilização>",
                                       "obrigatorias": [], "permitidas": []}}
    if op == "remover_projecao":
        return {"op": op, "nome": s.get("projecao")}
    if op == "definir_perfil":
        existing = next((x for x in section_items(ds, "perfis") if x["nome"] == s.get("perfil")), None)
        if existing:
            return {"op": op, "perfil": copy.deepcopy(existing)}
        return {"op": op, "perfil": {"nome": "<NomeDoPerfil>", "projecao": s.get("projecao") or "<Projecao>", "descricao": "<cenário>",
                                     "fixa": [{"propriedade": "<caminho a partir do HLM>", "valor": "<valor>"}]}}
    if op == "remover_perfil":
        return {"op": op, "nome": s.get("perfil")}
    if op == "definir_funcao":
        existing = next((x for x in section_items(ds, "funcoes") if x["nome"] == s.get("funcao")), None)
        return {"op": op, "funcao": copy.deepcopy(existing) if existing else {
            "nome": "<nomeDaFuncao>", "descricao": "Verdadeira quando …", "parametros": [{"nome": "<p>", "tipo": "texto", "papel": "alvo"}],
            "contextosExternos": [], "retorno": "booleano"}}
    if op == "remover_funcao":
        return {"op": op, "nome": s.get("funcao")}
    if op == "definir_contexto":
        existing = next((x for x in section_items(ds, "contextosExternos") if x["nome"] == s.get("contexto")), None)
        return {"op": op, "contexto": copy.deepcopy(existing) if existing else {"nome": "<nomeDoContexto>", "tipo": "data",
                                                                                 "descricao": "<descrição>", "fonte": "<de onde vem>"}}
    if op == "remover_contexto":
        return {"op": op, "nome": s.get("contexto")}
    if op == "mapear":
        return {"op": op, "fonte": "<fonte>", "origem": "<id no inventário>", "decisao": "mapeado", "destino": "HLM:<Hlm>/<caminho>"}
    return {"op": op}


def missing_selection(op, selection):
    """The selectors still to be chosen before the operation can be filled in."""
    return [x for x in SELECTORS.get(op, []) if not selection.get(x) and (op, x) not in OPTIONAL]


def description(op):
    return vocabulary()["operacoes"][op]["descricao"]


# ---------------------------------------------------------------------- context of a change request
def plausible_values(ds, level, model, prop):
    """The values an RP IN on the property admits (or None)."""
    for rule, lv, m, p in rules(ds, ("RP",)):
        r = rule.get("restricao") or {}
        if (lv, m) == (level, model) and prop in (p, r.get("propriedade")) and r.get("operador") == "IN":
            return r.get("valor")
    return None


def model_paths(ds, level, name):
    """Every property reachable from a model, through its composition: [{caminho, tipo, modelo, valores}].
    A rule that lives on the model can use any of these paths (a HLM reaches all of its composition)."""
    decl = next((Declaration(d) for d in ds.declarations.values() if Declaration(d).model(level, name)), None)
    if decl is None:
        return []
    out = []

    def walk(lv, model, prefix, visited):
        if (lv, model) in visited:
            return
        for p in decl.properties(lv, model):
            out.append({"caminho": prefix + p["nome"], "tipo": p.get("tipo"), "modelo": f"{lv} {model}",
                        "valores": plausible_values(ds, lv, model, p["nome"])})
        for role, child_level, child, _ in decl.compositions(lv, model):
            walk(child_level, child, f"{prefix}{role}.", visited | {(lv, model)})
    walk(level, name, "", frozenset())
    return out


def context_of(ds, selection):
    """The entities a selection points to, as they are in the declarations (for a focused change request)."""
    out = {}
    level, name = _split(selection.get("modelo"))
    model = ds.definition(level, name) if level else None
    if model:
        out["modelo"] = {"nivel": level, **model}
        prop = next((p for p in model.get("propriedades", []) if p["nome"] == selection.get("propriedade")), None)
        if prop:
            out["propriedade"] = prop
            values = plausible_values(ds, level, name, prop["nome"])
            if values:
                out["valoresPlausiveis"] = values
        out["regrasNoModelo"] = [{"id": r["id"], "vive": f"{lv} {m}{'.' + p if p else ''}", "restricao": r.get("restricao"),
                                  "condicao": r.get("condicao")} for r, lv, m, p in rules(ds) if (lv, m) == (level, name)]
    if selection.get("regra"):
        found = find_rule(ds, selection["regra"])
        if found:
            out["regra"] = {"vive": f"{found[1]} {found[2]}{'.' + found[3] if found[3] else ''}", **found[0]}
    for key, section in (("projecao", "projecoes"), ("perfil", "perfis"), ("funcao", "funcoes"), ("contexto", "contextosExternos")):
        item = next((x for x in section_items(ds, section) if x["nome"] == selection.get(key)), None)
        if item:
            out[key] = item
    if selection.get("hlm"):
        out["caminhosDoHlm"] = hlm_paths(ds, selection["hlm"])
    return out


def names_index(ds):
    """A compact index of what exists: models with their properties, rules by type, projections, profiles, functions."""
    lines = []
    for lv in LEVELS:
        for m in section_items(ds, lv.lower()):
            props = ", ".join(p["nome"] for p in m.get("propriedades", []))
            parts = ", ".join(f"{c.get('papel') or c.get('sm') or c.get('usm')}:{c.get('sm') or c.get('usm')}" for c in m.get("composicao", []))
            lines.append(f"- {lv} {m['nome']}" + (f" — propriedades: {props}" if props else "") + (f" — compõe: {parts}" if parts else ""))
    by_type = {}
    for rule, lv, m, p in rules(ds):
        by_type.setdefault(rule["id"].split("-")[0], []).append(rule["id"])
    lines += [f"- regras {k}: {', '.join(v)}" for k, v in sorted(by_type.items())]
    for label, section in (("projeções", "projecoes"), ("perfis", "perfis"), ("funções", "funcoes"), ("contextos externos", "contextosExternos")):
        names = [x["nome"] for x in section_items(ds, section)]
        if names:
            lines.append(f"- {label}: {', '.join(names)}")
    return "\n".join(lines)
