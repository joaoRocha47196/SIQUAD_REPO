"""The catalogue of views that exist for a graph.

The views are not stored anywhere: they are derived from the graph. Per HLM: the model view, the
view with rules, the projections and the gaps; per SM and USM: the specific model view; per property
restricted by at least 'decisaoMinimoRIR' RIR: the decision view; per discriminating factor: the
dependency analysis and the impact; per profile: the static selection; per example instance whose
profile exists: the validation result; per rule: its card.

Each entry is a ViewEntry: the page name (also the file name in the static site), the ViewModel and
its parameters. The web application builds the ViewModel of an entry only when it is requested.
"""
from dataclasses import dataclass, field

from ecv import config

from . import links as L
from .viewmodels import build
from .viewmodels import common as K
from .viewmodels.decision import rules_for_target
from .viewmodels.model import discriminating_keys

GROUPS = ("HLM", "Modelos", "Decisão", "Dependências e impacto", "Perfis", "Validação de instâncias",
          "Verificações transversais", "Fichas das regras")


@dataclass(frozen=True)
class ViewEntry:
    group: str
    page: str                 # page name: hlm_Fatura, regra_RP-NIF, ...
    viewmodel: str
    params: dict = field(default_factory=dict, hash=False, compare=False)
    title: str = ""


# Example views with fixed parameters (thesis figures); kept only when the graph supports them.
EXTRA_EXAMPLES = [
    ViewEntry("Decisão", "decisao_Medicao_valor_TEMPERATURA_C", "decisao",
              {"alvo": "USM:Medicao.valor", "filtro": {"tipoDispositivo": "TEMPERATURA", "unidadeMedida": "°C"}},
              "Medicao.valor com TEMPERATURA e °C (tese, Figura 'Pesquisa sobre as condições')"),
    ViewEntry("Decisão", "decisao_Morada_codigoPostal_freguesia", "decisao",
              {"alvo": "USM:Morada.codigoPostal", "linhas": "freguesia"}, "Morada.codigoPostal por freguesia (linhas)"),
]


def _hlm_views(g):
    out = []
    for h in sorted(n["nome"] for n in g.nodes("HLM")):
        out += [ViewEntry("HLM", L.model_page("HLM", h), "modelo", {"nivel": "HLM", "nome": h}, f"Modelo {h}"),
                ViewEntry("HLM", L.rules_page(h), "modelo", {"nivel": "HLM", "nome": h, "regras": True}, f"Modelo {h} com regras"),
                ViewEntry("HLM", L.projections_page(h), "projecoes", {"hlm": h}, f"Projeções de {h}"),
                ViewEntry("HLM", L.gaps_page(h), "lacunas", {"hlm": h}, f"Lacunas de {h}")]
    return out


def _model_views(g):
    return [ViewEntry("Modelos", L.model_page(level, m["nome"]), "modelo", {"nivel": level, "nome": m["nome"], "regras": True},
                      f"{level} {m['nome']}")
            for level in ("SM", "USM") for m in sorted(g.nodes(level), key=lambda n: n["nome"])]


def _decision_views(g):
    out, candidates = [], []
    for prop in sorted(g.nodes("Propriedade"), key=lambda n: n["chave"]):
        n = len(rules_for_target(g, prop))
        if n >= config.VIEWS["decisaoMinimoRIR"]:
            out.append(ViewEntry("Decisão", L.decision_page(prop["chave"]), "decisao", {"alvo": prop["chave"]},
                                 f'{prop["dono"]}.{prop["nome"]} ({n} RIR)'))
        if n >= config.VIEWS["candidatosPerfilMinimoRIR"]:
            candidates.append(prop["chave"])
    return out, candidates


def _dependency_views(g):
    out = []
    for key in sorted(discriminating_keys(g)):
        prop = g.node("Propriedade", key)
        out += [ViewEntry("Dependências e impacto", L.dependencies_page(key), "dependencias", {"propriedade": key},
                          f'Dependências de {prop["dono"]}.{prop["nome"]}'),
                ViewEntry("Dependências e impacto", L.impact_page(key), "impacto", {"propriedade": key},
                          f'Impacto de {prop["dono"]}.{prop["nome"]}')]
    return out


def _validation_views(g):
    from ecv import validation
    out = []
    for name, example in validation.examples().items():
        if (example.get("perfil") and g.node("Perfil", example["perfil"]) is not None) or \
                (example.get("hlm") and g.node("HLM", example["hlm"]) is not None):
            out.append(ViewEntry("Validação de instâncias", L.validation_page(name), "validacao", {"exemplo": name},
                                 f'{name} ({example.get("perfil") or example.get("hlm")})'))
    return out


def _supported(g, entry):
    if g.node("Propriedade", entry.params.get("alvo", "")) is None:
        return False
    try:
        build(g, entry.viewmodel, **entry.params)
    except ValueError:
        return False
    return True


def catalog(g, extra=EXTRA_EXAMPLES):
    """Every view that exists for the graph, as a list of ViewEntry."""
    entries = _hlm_views(g) + _model_views(g)
    decisions, candidates = _decision_views(g)
    entries += decisions + _dependency_views(g)
    entries += [ViewEntry("Perfis", L.profile_page(p["nome"]), "perfil", {"perfil": p["nome"]}, f"Perfil {p['nome']}")
                for p in sorted(g.nodes("Perfil"), key=lambda n: n["nome"])]
    if candidates:
        entries.append(ViewEntry("Perfis", "candidatos_perfil", "candidatos_perfil", {"alvos": candidates},
                                 "Candidatas a fixar num perfil"))
    entries += [ViewEntry("Verificações transversais", "coerencia", "coerencia", {}, "Coerência entre regras"),
                ViewEntry("Verificações transversais", "operadores", "operadores", {}, "Verificações por operador e enumerados")]
    entries += _validation_views(g)
    entries += [ViewEntry("Fichas das regras", L.rule_page(r["id"]), "regra", {"id": r["id"]}, r["id"])
                for r in K.order_rules(g.nodes("Regra"))]
    entries += [e for e in extra if _supported(g, e)]
    return entries
