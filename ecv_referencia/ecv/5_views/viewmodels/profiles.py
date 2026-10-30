"""Profile ViewModels: static/dynamic selection and the search for properties worth fixing."""
from ecv.graph.base import read_json

from . import common as K
from .evaluation import evaluate

STATES = ("sempre aplicável", "dinâmica", "nunca aplicável", "não avaliável", "alvo fora da projeção",
          "avaliada", "fora da projeção")


def profile_scenario(g, name):
    """(profile, projection, HLM, projected paths, fixed property values, fixed context values)."""
    profile = g.node("Perfil", name)
    if profile is None:
        raise ValueError(f"perfil '{name}' não existe")
    projection = g.first_target(profile, "USA")
    hlm = g.first_target(projection, "PROJETA")
    projected = {e.get("caminho") for t in ("OBRIGATORIA", "PERMITIDA") for e in g.outgoing(projection, t)}
    fixed, contexts = {}, {}
    for e in g.outgoing(profile, "FIXA"):
        if e.target.label == "ContextoExterno":
            contexts[e.target["nome"]] = read_json(e.get("valor"))
        else:
            fixed[e.get("caminho")] = read_json(e.get("valor"))
    return profile, projection, hlm, projected, fixed, contexts


def _term_state(term, prefix, projected, fixed, contexts, available):
    """State of one term: verdadeiro/falso (resolved by the profile), dinâmico (from the instance) or indisponível."""
    if term["forma"] == "funcao":
        args = [K.join(prefix, a["caminho"]) for a in term["chamada"]["argumentos"]]
        state = "dinâmico" if all(a in available for a in args) else "indisponível"
        return {"texto": term["texto"], "estado": state, "caminhos": args}
    path = K.join(prefix, term["caminho"])
    if term.get("contexto"):
        if path in fixed and term["contexto"] in contexts:
            state = "verdadeiro" if evaluate(term["operador"], fixed[path], contexts[term["contexto"]]) else "falso"
        else:
            state = "dinâmico" if path in available else "indisponível"
    elif path in fixed:
        state = "verdadeiro" if evaluate(term["operador"], fixed[path], term["valor"]) else "falso"
    else:
        state = "dinâmico" if path in projected else "indisponível"
    return {"texto": term["texto"], "estado": state, "caminhos": [path], "valorFixado": fixed.get(path)}


def _rule_state(rule_type, term_states, target_available):
    if rule_type == "RIC":
        target_available = any(s != "indisponível" for s in term_states)
    if "falso" in term_states:
        return "nunca aplicável"
    if not target_available:
        return "alvo fora da projeção"
    if "indisponível" in term_states:
        return "não avaliável"
    if all(s == "verdadeiro" for s in term_states):
        return "sempre aplicável"
    return "dinâmica"


def profile(g, perfil):
    """Static selection: what the values fixed in the profile decide before execution.

    For each rule of the HLM (in each occurrence of the node where it lives), each term of the condition is:
      resolved by the profile (true/false) when the property is fixed;
      dynamic when the property is in the projection (the value comes from the instance);
      unavailable when it is neither projected nor fixed.
    The rule is then: always applicable, never applicable, dynamic or not evaluable (thesis, figures
    'Seleção estática' and 'Propriedade usada na aplicabilidade mas não projetada').
    """
    node, projection, hlm, projected, fixed, contexts = profile_scenario(g, perfil)
    available = projected | set(fixed)
    rows = []
    for rule, prefixes in K.rules_of_hlm(g, hlm["nome"]):
        summary = K.rule_summary(g, rule)
        for prefix in prefixes:
            targets = []
            restriction = summary.get("restricao")
            if restriction:
                if restriction.get("forma") == "funcao" and restriction.get("chamada"):
                    targets = [K.join(prefix, a["caminho"]) for a in restriction["chamada"]["argumentos"]]
                elif restriction.get("caminho"):
                    targets = [K.join(prefix, restriction["caminho"])]
            target_available = any(t in available for t in targets) if targets else True
            ctx = [{"nome": c, "origem": "fixado no perfil" if c in contexts else "obtido pelo motor",
                    "valor": contexts.get(c)} for c in summary["contextosExternos"]]
            if summary["tipo"] == "RP":
                rows.append({"regra": summary["id"], "tipo": "RP", "ocorrencia": prefix, "descricao": summary["descricao"],
                             "estado": "avaliada" if target_available else "fora da projeção", "termos": [],
                             "alvos": targets, "contextos": ctx})
                continue
            terms = [_term_state(t, prefix, projected, fixed, contexts, available) for t in summary.get("condicao", [])]
            rows.append({"regra": summary["id"], "tipo": summary["tipo"], "ocorrencia": prefix, "descricao": summary["descricao"],
                         "estado": _rule_state(summary["tipo"], [t["estado"] for t in terms], target_available),
                         "termos": terms, "alvos": targets, "contextos": ctx, "restricao": (restriction or {}).get("texto")})
    totals = {s: sum(1 for r in rows if r["estado"] == s) for s in STATES}
    return {"vista": "perfil", "titulo": f"Perfil {perfil}: seleção estática e dinâmica", "perfil": perfil,
            "descricao": node.get("descricao"), "projecao": projection["nome"], "hlm": hlm["nome"],
            "fixados": [{"caminho": k, "valor": v, "projetada": k in projected} for k, v in sorted(fixed.items())],
            "contextos": [{"nome": k, "valor": v} for k, v in sorted(contexts.items())],
            "resumo": {k: v for k, v in totals.items() if v}, "regras": rows}


def profile_candidates(g, alvos):
    """Given the properties to validate, the other properties read in the conditions of the rules that
    restrict them: the candidates to fix in a profile (thesis, table 'Pesquisa das propriedades usadas
    na aplicabilidade')."""
    rows, everything = [], []
    for key in alvos:
        prop = K.property_node(g, key)
        rules, props = [], []
        for e in g.incoming(prop, "RESTRINGE"):
            rule = K.rule_of_restriction(g, e.source)
            if rule is None or rule.label != "RIR":
                continue
            rules.append(rule["id"])
            condition = K.condition_of(g, rule)
            for t in g.outgoing(condition, "TERMO"):
                if t.target["nome"] not in props:
                    props.append(t.target["nome"])
            for c in K.calls(g, condition, rule["id"]):
                for x in c["argumentos"]:
                    if x["nomeAlvo"] not in props:
                        props.append(x["nomeAlvo"])
        rows.append({"alvo": key, "nome": prop["nome"], "regras": sorted(rules), "propriedades": props})
        everything += [p for p in props if p not in everything]
    return {"vista": "candidatos_perfil", "titulo": "Propriedades candidatas a fixar num perfil",
            "linhas": rows, "candidatas": everything}
