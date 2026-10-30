"""ViewModels: each one is an operation on the graph that returns the data of one view (a JSON object).

They only use the Graph interface, so they run on the in-memory graph and on Neo4j. REGISTRY maps
the name of each ViewModel to its function, its parameters, the question it answers and the
equivalent Cypher query (in cypher/, to run in the Neo4j Browser).
"""
from . import decision, model, profiles, projections, queries, rule


def _validation(g, exemplo=None, instancia=None, perfil=None, hlm=None, contextos=None):
    """The ViewModel of module 6 (validation): an example instance (by name) or a given one, in the profile scenario."""
    from ecv import validation
    if exemplo:
        return validation.validate_example(g, exemplo, contextos)
    return validation.validate(g, instancia, profile=perfil, hlm=hlm, contexts=contextos)


REGISTRY = {
    "modelo": {"funcao": model.model, "parametros": ["nivel", "nome", "regras?"], "cypher": "modelo.cypher",
               "pergunta": "Qual é a estrutura de um modelo até às folhas, quem o usa e (com regras) que regras vivem em cada nó?"},
    "projecoes": {"funcao": projections.projections, "parametros": ["hlm"], "cypher": "projecoes.cypher",
                  "pergunta": "Que propriedades cada projeção exige ou permite, e o que fixa cada perfil?"},
    "decisao": {"funcao": decision.decision, "parametros": ["alvo", "linhas?", "filtro?"], "cypher": "decisao.cypher",
                "pergunta": "Que valor é exigido à propriedade em cada combinação dos fatores discriminantes (em matriz ou em árvore)?"},
    "coerencia": {"funcao": decision.coherence, "parametros": [], "cypher": "coerencia.cypher",
                  "pergunta": "Há regras que nunca se aplicam, gamas incompatíveis ou condições repetidas?"},
    "dependencias": {"funcao": queries.dependencies, "parametros": ["propriedade"], "cypher": "dependencias.cypher",
                     "pergunta": "Que restrições e conclusões implica cada valor desta propriedade, e que propriedades dependem dela?"},
    "impacto": {"funcao": queries.impact, "parametros": ["propriedade"], "cypher": "impacto.cypher",
                "pergunta": "Que regras, projeções e perfis são afetados se a propriedade mudar?"},
    "lacunas": {"funcao": queries.gaps, "parametros": ["hlm", "projecoes?"], "cypher": "lacunas.cypher",
                "pergunta": "Que propriedades não têm regras, e quais nenhuma projeção usa?"},
    "operadores": {"funcao": queries.operators, "parametros": [], "cypher": "operadores.cypher",
                   "pergunta": "Que restrições e termos usam cada operador, e que propriedades são enumerados?"},
    "perfil": {"funcao": profiles.profile, "parametros": ["perfil"], "cypher": "perfil.cypher",
               "pergunta": "Que regras o perfil torna sempre aplicáveis, nunca aplicáveis, dinâmicas ou não avaliáveis?"},
    "candidatos_perfil": {"funcao": profiles.profile_candidates, "parametros": ["alvos"], "cypher": "candidatos_perfil.cypher",
                          "pergunta": "Que propriedades se podem fixar num perfil para validar estas?"},
    "validacao": {"funcao": _validation, "parametros": ["exemplo | instancia", "perfil? | hlm?", "contextos?"], "cypher": "validacao.cypher",
                  "pergunta": "A instância cumpre as regras do HLM no cenário do perfil (estrutura, conformidade e conclusões)?"},
    "regra": {"funcao": rule.rule, "parametros": ["id"], "cypher": "regra.cypher",
              "pergunta": "O que declara uma regra, a que elementos está ligada e por que modelos chega a cada HLM?"},
}


def build(g, viewmodel, /, **params):
    """Build a ViewModel by name with its parameters (the names of REGISTRY[...]['parametros'])."""
    if viewmodel not in REGISTRY:
        raise KeyError(f"ViewModel desconhecido: {viewmodel}; disponíveis: {sorted(REGISTRY)}")
    vm = REGISTRY[viewmodel]["funcao"](g, **params)
    vm.setdefault("parametros", params)
    return vm
