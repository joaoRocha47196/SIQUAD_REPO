"""Funções: what a function needs in each module.

    declared      in a declaration (name, parameters, external contexts, meaning) — module 2, operation definir_funcao,
                  or a step response (step E); it is part of the graph
    implemented   in Python, in ecv/6_validation/functions — needed to evaluate the rules that call it
A declared function without implementation makes its rules 'não avaliável'. The implementation is asked
to the LLM as a request of the global queue; registering the response installs the module.
"""
import json

from ecv.validation import functions as registry
from ecv.validation.function_requests import declared_functions, request_implementation as create_request
from ecv.shared.llm_requests import RequestQueue

from ..http import Response, url
from ..pages import layout
from ..pages.components import button_form, e, message, section, state, table


def _open_requests():
    return {r.meta.get("funcao"): r for r in RequestQueue.global_queue().requests() if r.kind == "funcao" and r.state != "rejeitado"}


def functions_table(app):
    """The declared functions of the active graph, with the state of their implementation (also shown in Alterações › E)."""
    declared = declared_functions(app.graph)
    open_requests = _open_requests()
    rows = []
    for f in declared:
        params = ", ".join(f'{p["nome"]}: {p.get("tipo")}{"[]" if p.get("colecao") else ""} ({p.get("papel")})' for p in f["parametros"])
        req = open_requests.get(f["nome"])
        if f["implementada"]:
            impl = f'{state("aplicado")} <code>{e(f["modulo"])}.py</code>'
        elif req:
            impl = f'<a href="/pedidos/global/{e(req.id)}">{e(req.id)}</a> {state(req.state)}'
        else:
            impl = button_form("/funcoes/pedir", "Pedir implementação", {"nome": f["nome"]})
        edit = f'<a href="{url("/alteracoes", camada="E", op="definir_funcao", funcao=f["nome"])}">alterar a declaração</a>'
        rows.append([f'<code>{e(f["nome"])}</code>', e(f["descricao"]), e(params), e(", ".join(f["contextosExternos"])),
                     e(", ".join(f["regras"])), impl + "<br>" + edit])
    return (f"<h3>Funções declaradas ({len(declared)})</h3>"
            + table(["Função", "Descrição", "Parâmetros", "Contextos externos", "Regras que a chamam", "Implementação"], rows)
            + f'<p><a href="{url("/alteracoes", camada="E", op="definir_funcao")}">+ declarar uma função</a> · '
              'implementações em <code>ecv/6_validation/functions/</code>; pedidos de implementação em <code>pedidos/</code></p>')


def page(app, request):
    declared = declared_functions(app.graph)
    names = {f["nome"] for f in declared}
    extra = sorted(n for n in registry.implemented() if n not in names)
    body = message(request.get("aviso"), "ok")
    body += section("Funções do âmbito ativo", functions_table(app))
    if extra:
        body += section("Implementadas, não declaradas no âmbito ativo", "<p>" + ", ".join(f"<code>{e(n)}</code> ({e(registry.SOURCES[n])})" for n in extra) + "</p>")
    return Response.html(layout.page(app, "funcoes", "Funções", body, request.path,
                                     "A declaração diz o que a função significa; a implementação (ecv/6_validation/functions) diz como o motor a avalia."))


def request_implementation(app, request):
    name = request.form()["nome"]
    r = create_request(app.graph, name)
    app.log.event(f"pedido {r.id} criado: implementar {name}")
    return Response.redirect(f"/pedidos/global/{r.id}", note=r.id)


def api(app, request):
    return Response.json(json.loads(json.dumps(declared_functions(app.graph), default=str)))
