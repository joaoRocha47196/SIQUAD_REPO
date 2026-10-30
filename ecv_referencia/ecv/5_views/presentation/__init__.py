"""ViewModel -> HTML page (the body of the view).

Each kind of view is drawn by one module (model_view, decision_view, dependency_view, rule_view,
other_views, validation_view). Renderers never go back to the graph: everything they show is in the
ViewModel; links between views come from views/links.py.
"""
from . import decision_view, dependency_view, model_view, other_views, rule_view, validation_view
from .html import e, page

# The graph traversal behind each ViewModel (shown in the documentation of each kind of view).
TRAVERSALS = {
    "modelo": "(modelo)-COMPOSTO_POR*->(SM|USM)-CONTEM->(Propriedade); com regras: (Regra)-ASSOCIADA_A->(nó), Regra-RESTRITA_POR->Restricao-RESTRINGE|CHAMA->, Regra-CONDICIONADA_POR->Condicao-TERMO|CHAMA->; para cima: COMPOSTO_POR inverso até aos HLM; Projecao-PROJETA->HLM.",
    "projecoes": "Projecao -PROJETA-> HLM; Projecao -OBRIGATORIA|PERMITIDA {caminho}-> Propriedade; Perfil -USA-> Projecao; Perfil -FIXA-> Propriedade|ContextoExterno.",
    "decisao": "Propriedade <-RESTRINGE- Restricao <-RESTRITA_POR- RIR -CONDICIONADA_POR-> Condicao -TERMO-> Propriedade (fatores discriminantes); RP -ASSOCIADA_A|RESTRITA_POR/RESTRINGE-> do alvo e dos fatores.",
    "coerencia": "TERMO (valores) vs RP IN da propriedade; pares de RESTRINGE RANGE sobre a mesma propriedade com condições compatíveis; condições com os mesmos TERMO e CHAMA.",
    "dependencias": "Propriedade <-TERMO- Condicao <-CONDICIONADA_POR- RIR/RIC -RESTRITA_POR-> Restricao -RESTRINGE-> Propriedade (ou -CHAMA-> Funcao -LE-> alvos); Propriedade <-LE {parte: termo}- Funcao; RP IN da propriedade.",
    "impacto": "Propriedade <-RESTRINGE|TERMO|LE|ASSOCIADA_A- ... Regra; <-OBRIGATORIA|PERMITIDA- Projecao; <-FIXA- Perfil.",
    "lacunas": "Propriedades sem RESTRINGE, ASSOCIADA_A nem LE a chegar; caminhos sem OBRIGATORIA nem PERMITIDA das projeções do HLM.",
    "operadores": "Restricao.operador; TERMO.operador; CHAMA.operador; RP IN por propriedade.",
    "perfil": "Perfil -USA-> Projecao -PROJETA-> HLM; Perfil -FIXA->; regras da árvore do HLM e os seus TERMO, avaliados com os valores fixados.",
    "candidatos_perfil": "Propriedade <-RESTRINGE- Restricao <-RESTRITA_POR- RIR -CONDICIONADA_POR-> Condicao -TERMO|CHAMA/LE-> Propriedade.",
    "validacao": "Perfil -USA-> Projecao -PROJETA-> HLM, -OBRIGATORIA|PERMITIDA->, Perfil -FIXA->; árvore do HLM (COMPOSTO_POR, CONTEM); cada regra (ASSOCIADA_A) com a Restricao (RESTRINGE, CHAMA) e a Condicao (TERMO, CHAMA), avaliadas sobre os valores da instância.",
    "regra": "Regra -ASSOCIADA_A->, -RESTRITA_POR-> Restricao (-RESTRINGE->, -CHAMA-> Funcao -LE->, -DEPENDE_DE->), -CONDICIONADA_POR-> Condicao (-TERMO->, -CHAMA->, -DEPENDE_DE->); de cada propriedade envolvida: <-CONTEM- modelo <-COMPOSTO_POR- … HLM.",
}

RENDERERS = {"modelo": model_view.render, "projecoes": other_views.projections, "decisao": decision_view.decision,
             "coerencia": decision_view.coherence, "dependencias": dependency_view.dependencies, "impacto": dependency_view.impact,
             "lacunas": other_views.gaps, "operadores": other_views.operators, "perfil": other_views.profile,
             "candidatos_perfil": other_views.profile_candidates, "regra": rule_view.rule, "validacao": validation_view.validation}


def view_kind(vm):
    """Kind of view in the catalogue (documentacao/catalogo_vistas.json)."""
    if vm["vista"] == "modelo":
        return "modelo_especifico" if vm["especifico"] else ("modelo_regras" if vm["comRegras"] else "modelo_hlm")
    return vm["vista"]


def render_body(vm):
    return RENDERERS[vm["vista"]](vm)


def render_page(vm, json_file=None):
    """The page has only the information of the view; its description, use and diagrams are in the documentation."""
    body = render_body(vm)
    if json_file:
        body += f'<p class="note footer">Dados desta vista: <a href="{e(json_file)}">{e(json_file)}</a></p>'
    return page(vm["titulo"], body)
