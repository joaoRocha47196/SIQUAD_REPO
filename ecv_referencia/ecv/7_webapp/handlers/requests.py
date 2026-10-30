"""Pedidos ao LLM: the queues of requests (one per domain, plus the global queue for function implementations),
each request with its prompt, its response and what was done with it.

How a request is answered (shared/llm_requests.py):
    1. in the repository: the LLM reads <pasta>/prompt.md and writes <pasta>/resposta.json (or resposta.py) and commits;
       after a pull the request shows as 'respondido';
    2. here: copy the prompt to an LLM and paste the response below.
Then 'Registar' applies the response (module 1 for steps and changes, module 6 for functions).
"""
from ecv import config, ecv_builder
from ecv.shared.errors import EcvError
from ecv.shared.llm_requests import KINDS, RequestQueue
from ecv.transformer.adapter_requests import register_adapter
from ecv.validation.function_requests import register_implementation
from ecv.validation.test_instances import register_instance

from ..http import Response, not_found, url
from ..pages import layout
from ..pages.components import button_form, e, keyvalues, message, pre, section, state, table, where_box

GLOBAL = "global"

PROTOCOL = ("<p>Um pedido é uma pasta com <code>prompt.md</code>. Responde-se de uma de duas formas: no repositório, escrevendo "
            "<code>resposta.json</code> (ou <code>resposta.py</code>, numa função) na pasta do pedido e fazendo commit; ou aqui, colando a resposta. "
            "<b>Registar</b> aplica a resposta: o pedido fica <i>aplicado</i>, ou <i>rejeitado</i> com o motivo (e pode ser respondido de novo).</p>")


def _relative(folder):
    try:
        return folder.relative_to(config.ROOT)
    except ValueError:
        return folder


def _queues(app):
    out = [(d, RequestQueue.for_domain(app.workspace.domain(d))) for d in app.workspace.domain_ids()]
    return out + [(GLOBAL, RequestQueue.global_queue())]


def _queue(app, name):
    if name == GLOBAL:
        return RequestQueue.global_queue()
    return RequestQueue.for_domain(app.workspace.domain(name))


def list_page(app, request):
    selected = request.get("fila")
    only = request.get("estado")
    body = section("Como se responde", PROTOCOL)
    for name, queue in _queues(app):
        if selected and name != selected:
            continue
        items = [r for r in queue.requests() if not only or r.state == only]
        rows = [[f'<a href="/pedidos/{e(name)}/{e(r.id)}">{e(r.id)}</a>', e(KINDS[r.kind]), e(r.title), state(r.state),
                 e(r.meta.get("criado")), e((r.meta.get("resumo") or "")[:140])] for r in reversed(items)]
        title = "Fila global (funções)" if name == GLOBAL else f"Domínio {name}"
        body += section(f"{title} · {_relative(queue.folder)}",
                        table(["Pedido", "Tipo", "Título", "Estado", "Criado", "Resultado"], rows) if rows else '<p class="note">Sem pedidos.</p>')
    filters = " · ".join(f'<a href="{url("/pedidos", fila=selected, estado=s)}">{s or "todos"}</a>' for s in ("", "pendente", "respondido", "aplicado", "rejeitado"))
    body += where_box([('Um pedido: pasta com pedido.json, prompt.md, resposta e resultado.json', 'ecv/shared/llm_requests.py'), ('As filas dos domínios', 'dominios/<d>/pedidos/<id>/'), ('A fila global (funções e adaptadores)', 'pedidos/<id>/'), ('Registar: geração e alterações', 'ecv/1_ecv_builder/workflow.py (register_response)'), ('Registar: funções', 'ecv/6_validation/function_requests.py'), ('Registar: adaptadores', 'ecv/0_transformer/adapter_requests.py'), ('Registar: instâncias de teste', 'ecv/6_validation/test_instances.py'), ('Esta página', 'ecv/7_webapp/handlers/requests.py')])
    return Response.html(layout.page(app, "pedidos", "Pedidos ao LLM", f"<p>{filters}</p>" + body, request.path))


def _get(app, request):
    try:
        return _queue(app, request.params["fila"]).get(request.params["pedido"])
    except EcvError as err:
        raise not_found(str(err)) from err


def detail(app, request, notice=None, kind="ok"):
    r = _get(app, request)
    queue = request.params["fila"]
    base = f"/pedidos/{queue}/{r.id}"
    size = r.meta.get("tamanho") or {}
    body = message(notice or request.get("aviso"), request.get("tipo", kind))
    body += keyvalues([("Tipo", e(KINDS[r.kind])), ("Estado", state(r.state)), ("Passo", e(r.step or "—")), ("Criado", e(r.meta.get("criado"))),
                       ("Pasta", f"<code>{e(r.folder)}</code>"), ("Ficheiro da resposta", f"<code>{e(r.response_file.name)}</code>"),
                       ("Prompt", f'{size.get("caracteres", len(r.prompt()))} caracteres, ~{size.get("tokensEstimados", len(r.prompt()) // 4)} tokens · '
                                  f'<a href="{base}/prompt.md">abrir</a> · <button onclick="ecvCopy(\'prompt\')">copiar</button>')])
    if r.meta.get("pedido"):
        body += section("Pedido em linguagem natural", pre(r.meta["pedido"]))
    body += section("Prompt", f'<textarea id="prompt" rows="14" readonly>{e(r.prompt())}</textarea>')
    response = r.response_text() or ""
    body += section("Resposta", f'<form method="post" action="{base}/resposta"><textarea name="resposta" rows="14" '
                    f'placeholder="cole aqui a resposta do LLM">{e(response)}</textarea>'
                    '<p><button>Guardar resposta</button></p></form>'
                    + (button_form(f"{base}/registar", "Registar (aplicar a resposta)" if r.state != "aplicado" else "Registar de novo (substitui o resultado anterior)",
                                css="primary") if r.has_response() else ""))
    result = r.result()
    if result:
        verification = (result.get("verificacao") or {}).get("texto")
        body += section("Resultado", pre("\n".join(result.get("feitas", [])) or result.get("resumo") or result.get("erro") or "")
                        + (pre(verification) if verification else ""))
        if r.kind in ("passo", "alteracao") and r.state == "aplicado":
            body += f'<p><a href="/declaracao?passo={e(r.step)}">→ o passo {e(r.step)} na Declaração</a> · <a href="/vistas">→ vistas</a></p>'
    return Response.html(layout.page(app, "pedidos", f"Pedido {r.id}", body, request.path, r.title))


def prompt_file(app, request):
    r = _get(app, request)
    return Response.text(r.prompt(), "text/markdown; charset=utf-8", filename=f"{r.id}-prompt.md")


def save_response(app, request):
    r = _get(app, request)
    try:
        r.save_response(request.form().get("resposta", ""))
    except EcvError as err:
        return detail(app, request, f"Resposta não guardada: {err}", "error")
    app.log.event(f"pedido {r.id}: resposta guardada ({r.response_file.stat().st_size} B)")
    return Response.redirect(url(f"/pedidos/{request.params['fila']}/{r.id}", aviso="Resposta guardada. Registe-a para a aplicar."))


def register(app, request):
    r = _get(app, request)
    queue = request.params["fila"]
    try:
        if r.kind == "funcao":
            result = register_implementation(r)
            text = result["resumo"]
        elif r.kind == "adaptador":
            result = register_adapter(r)
            text = result["resumo"]
        elif r.kind == "instancia":
            result = register_instance(app.workspace.domain(queue), r, app.graph)
            text = result["resumo"]
        else:
            done, check = ecv_builder.register_response(app.workspace.domain(queue), r)
            text = f"{len(done)} alteração(ões); {check.summary()}"
    except EcvError as err:
        app.log.event(f"pedido {r.id}: rejeitado: {err}")
        return detail(app, request, f"Resposta rejeitada (nada foi gravado): {err}", "error")
    app.log.event(f"pedido {r.id}: aplicado: {text}")
    return Response.redirect(url(f"/pedidos/{queue}/{r.id}", aviso=f"Aplicado: {text}"), note="aplicado")


def api(app, request):
    return Response.json({name: [r.to_dict() for r in queue.requests()] for name, queue in _queues(app)})
