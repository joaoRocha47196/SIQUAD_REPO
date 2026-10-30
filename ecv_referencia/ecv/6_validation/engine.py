"""The validation engine: evaluates one instance of a HLM against the rules of the graph, in the scenario
of a profile, and returns the ViewModel 'validacao'.

    1. Scenario   (scenario.py)   the profile's projection, fixed values and contexts
    2. Structure  (structure.py)  fixed values applied; unknown keys, types, cardinalities, mandatory paths
    3. Rules      (rules.py)      each rule in each concrete occurrence: condition, restriction, conclusion
    4. Result                     valid when there are no structural problems and no non-conforming rule
"""
from .instance import deep_copy
from .rules import STATES, RuleEvaluator
from .scenario import Scenario
from .structure import PROBLEM_TYPES, StructureCheck


def validate(g, instance, profile=None, hlm=None, contexts=None, name=None, description=None):
    """The ViewModel 'validacao': the result of validating the instance in the profile's scenario (or with the HLM only)."""
    scenario = Scenario(g, profile, hlm, contexts)
    evaluated = deep_copy(instance)
    problems = StructureCheck(scenario, evaluated).run()
    rows = RuleEvaluator(scenario, evaluated).run()
    totals = {s: sum(1 for r in rows if r["estado"] == s) for s in STATES}
    valid = not problems and totals["não conforme"] == 0
    title = f"Validação{' de ' + name if name else ''}: {'válida' if valid else 'inválida'}"
    return {"vista": "validacao", "titulo": title, "instancia": name, "descricaoInstancia": description,
            "hlm": scenario.hlm, "perfil": scenario.profile, "projecao": scenario.projection, "valida": valid,
            "fixados": [{"caminho": k, "valor": v} for k, v in sorted(scenario.fixed.items())],
            "contextos": scenario.context_rows(),
            "resumo": {k: v for k, v in totals.items() if v},
            "estrutura": problems,
            "resumoEstrutura": {t: sum(1 for p in problems if p["tipo"] == t) for t in PROBLEM_TYPES if any(p["tipo"] == t for p in problems)},
            "conclusoes": [r for r in rows if r["estado"] == "conclusão"],
            "regras": sorted(rows, key=lambda r: (STATES.index(r["estado"]), r["regra"], r["ocorrencia"])),
            "instanciaAvaliada": evaluated}
