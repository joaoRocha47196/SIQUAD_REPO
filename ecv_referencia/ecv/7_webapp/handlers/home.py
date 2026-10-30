"""Início: the active scope, the database, the domains with the state of their steps, pending requests;
the scope selector; the table of routes; the server log."""
from ecv.ecv_builder.build_process import step_ids
from ecv.shared.llm_requests import RequestQueue

from ..http import Response
from ..pages.components import e, section, state, table
from ..pages import layout


def _pending(queue):
    return [r for r in queue.requests() if r.state in ("pendente", "respondido")]


def _domains_table(app):
    steps = step_ids()
    rows = []
    for domain_id in app.workspace.domain_ids():
        d = app.workspace.domain(domain_id)
        pending = _pending(RequestQueue.for_domain(d))
        rows.append([f'<b>{e(d.id)}</b><br><span class="note">{e(d.name)}</span>', str(len(d.inventory_files())),
                     str(len(d.declaration_files()))]
                    + [state(d.step_state(s)) for s in steps]
                    + [f'<a href="/pedidos?fila={e(d.id)}">{len(pending)}</a>' if pending else "0"])
    return table(["Domínio", "Inventários", "Declarações"] + [f"Passo {s}" if s != "0" else "Fase 0" for s in steps]
                 + ["Pedidos por registar"], rows, "steps")


def overview(app, request):
    db = app.database.status()
    accepted = sum(1 for d in db["declaracoes"] if d["aceite"])
    nodes = sum(db["nos"].values())
    body = section("Âmbito ativo", f'<p><b>{e(db["tituloAmbito"])}</b>: {accepted} de {len(db["declaracoes"])} declarações ingeridas, '
                   f'{nodes} nós, {sum(db["arestas"].values())} arestas '
                   f'(<a href="/base">base de dados</a> · <a href="/vistas">vistas</a> · <a href="/validacao">validação</a>).</p>'
                   + (f'<div class="msg msg-warn">{db["rejeitadas"]} declaração(ões) rejeitada(s) na ingestão: ver <a href="/base">Base de dados</a>.</div>'
                      if db["rejeitadas"] else ""))
    body += section("Domínios", _domains_table(app)
                    + '<p class="note">Cada domínio é uma pasta em dominios/ (dominio.json, inventario/, declaracoes/, mapeamento.json, pedidos/). '
                      'Escolha o domínio no seletor de âmbito para trabalhar nele.</p>')
    body += section("Novo domínio", '<form method="post" action="/declaracao/dominio" class="stack"><p>'
                    '<label>Identificador <input name="id" size="18" placeholder="ex.: biblioteca"></label> '
                    '<label>Nome <input name="nome" size="30"></label></p>'
                    '<p><textarea name="descricao" rows="2" cols="100" placeholder="o que o domínio cobre"></textarea></p>'
                    '<p><button>Criar o domínio</button> <span class="note">cria dominios/&lt;id&gt;/dominio.json; as fontes '
                    'acrescentam-se em Declaração › 1. Extração</span></p></form>')
    global_pending = _pending(RequestQueue.global_queue())
    if global_pending:
        body += section("Fila global", f'<p><a href="/pedidos?fila=global">{len(global_pending)} pedido(s) por registar (funções e adaptadores)</a></p>')
    return Response.html(layout.page(app, "inicio", "Visão geral", body))


def select_scope(app, request):
    form = request.form()
    app.use_scope(form["ambito"])
    back = form.get("voltar") or "/"
    if back.startswith("/vistas/") or back.startswith("/pedidos/"):
        back = back.rsplit("/", 1)[0] if back.startswith("/vistas/") else "/pedidos"
    return Response.redirect(back, note=f"âmbito {form['ambito']}")


def routes_page(app, request):
    from ..routes import ROUTES
    rows = [[e(r.method), f"<code>{e(r.path)}</code>", e(r.description)] for r in ROUTES]
    return Response.html(layout.page(app, "inicio", "Rotas da aplicação", table(["Método", "Caminho", "O que faz"], rows),
                              subtitle="Definidas em ecv/7_webapp/routes.py"))


def log_page(app, request):
    kind = request.get("tipo")
    entries = app.log.recent(400, kind or None)
    filters = " · ".join(f'<a href="/registo{("?tipo=" + k) if k else ""}">{label}</a>'
                         for k, label in (("", "tudo"), ("pedido", "pedidos HTTP"), ("evento", "ações"), ("erro", "erros")))
    rows = [[e(x["time"]), e(x["kind"]), e(x["method"]), f'<code>{e(x["path"])}</code>', e(x["status"] or ""),
             e(f'{x["ms"]:.0f}' if x["ms"] else ""), f'<span class="mono">{e(x["text"])}</span>'] for x in entries]
    body = (f"<p>{filters}</p>" + table(["Hora", "Tipo", "Método", "Caminho", "Estado", "ms", "Detalhe"], rows)
            + '<p class="note">Também na consola do servidor e em registos/servidor.log.</p>')
    return Response.html(layout.page(app, "registo", "Registo do servidor", body))


def log_api(app, request):
    return Response.json(app.log.recent(int(request.get("n", 200)), request.get("tipo")))
