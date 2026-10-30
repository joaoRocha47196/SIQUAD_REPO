"""The parts of a rule: restriction, applicability condition, function calls and the paths it reads.

Every path of a rule is relative to the model where the rule is declared (for a rule declared on a
property, to the model that holds the property).
"""
from ecv import config


def restriction(rule):
    return rule.get("restricao")


def condition(rule):
    return rule.get("condicao") or []


def is_function(part):
    return part is not None and part.get("operador") in config.FUNCTION_OPERATORS


def call(part):
    return part.get("chamada") if is_function(part) else None


def path_arguments(call_spec):
    """Paths given as arguments of a call, with their position."""
    return [(i, a["caminho"]) for i, a in enumerate(call_spec.get("argumentos", [])) if "caminho" in a]


def restriction_target(rule):
    """The single target of a typed restriction; None for a restriction by function."""
    r = restriction(rule)
    if r is None or is_function(r):
        return None
    return r.get("propriedade")


def restriction_paths(rule):
    r = restriction(rule)
    if r is None:
        return []
    if is_function(r):
        return [p for _, p in path_arguments(r["chamada"])]
    return [r["propriedade"]] if r.get("propriedade") else []


def condition_paths(rule):
    out = []
    for term in condition(rule):
        if is_function(term):
            out.extend(p for _, p in path_arguments(term["chamada"]))
        elif term.get("propriedade"):
            out.append(term["propriedade"])
    return out


def paths_read(rule):
    """Every path the rule reads, with the part where it appears."""
    out = []
    r = restriction(rule)
    if r is not None:
        if is_function(r):
            out += [{"parte": "restricao", "caminho": p, "argumento": i} for i, p in path_arguments(r["chamada"])]
        elif r.get("propriedade"):
            out.append({"parte": "restricao", "caminho": r["propriedade"]})
    for k, term in enumerate(condition(rule)):
        if is_function(term):
            out += [{"parte": "termo", "termo": k, "caminho": p, "argumento": i} for i, p in path_arguments(term["chamada"])]
        elif term.get("propriedade"):
            out.append({"parte": "termo", "termo": k, "caminho": term["propriedade"]})
    return out


def function_calls(rule):
    """[(part, term index or None, call)] for every function the rule calls."""
    out = []
    r = restriction(rule)
    if is_function(r):
        out.append(("restricao", None, r["chamada"]))
    for k, term in enumerate(condition(rule)):
        if is_function(term):
            out.append(("termo", k, term["chamada"]))
    return out


def contexts_used(decl, rule):
    """External contexts the rule depends on: directly in a term, or through the functions it calls."""
    used = []
    for term in condition(rule):
        if term.get("contexto") and term["contexto"] not in used:
            used.append(term["contexto"])
    for _, _, c in function_calls(rule):
        for ctx in decl.functions.get(c.get("funcao"), {}).get("contextosExternos", []):
            if ctx not in used:
                used.append(ctx)
    return used


def message(rule):
    """The message the rule communicates: non-conformity (from the restriction) or conclusion (RIC)."""
    r = restriction(rule)
    if r is not None and r.get("mensagem"):
        return r["mensagem"]
    return rule.get("mensagem")
