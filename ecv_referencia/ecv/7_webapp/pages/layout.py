"""The page of the web application: header with the scope selector, the tabs, the content.

Tabs, in the order of the work:
    Início · Inventário · Declaração · Alterações · Vistas · Validação · Instâncias | Pedidos ao LLM · Funções · Base de dados · Registo
"""
from ecv.views.presentation.html import CSS, JS, e

TABS = [("inicio", "Início", "/"), ("inventario", "Inventário", "/inventario"), ("declaracao", "Declaração", "/declaracao"),
        ("alteracoes", "Alterações", "/alteracoes"), ("vistas", "Vistas", "/vistas"), ("validacao", "Validação", "/validacao"),
        ("instancias", "Instâncias", "/instancias"), None,
        ("pedidos", "Pedidos ao LLM", "/pedidos"), ("funcoes", "Funções", "/funcoes"), ("base", "Base de dados", "/base"),
        ("registo", "Registo", "/registo")]

APP_CSS = """
header.app{background:#5a1a2f;color:#fff;padding:8px 26px;display:flex;align-items:center;gap:18px;flex-wrap:wrap}
header.app .brand{font-weight:bold;font-size:15px;color:#fff;text-decoration:none}
header.app form{margin:0;display:flex;align-items:center;gap:6px}
header.app select{font-size:12px}
header.app .db{font-size:11px;opacity:.85;margin-left:auto}
nav.tabs{display:flex;gap:2px;padding:0 26px;background:#f1ebee;border-bottom:1px solid #d8c9cf;flex-wrap:wrap}
nav.tabs a{padding:7px 12px;text-decoration:none;color:#5a1a2f;border-bottom:3px solid transparent}
nav.tabs a.active{border-bottom-color:#5a1a2f;font-weight:bold;background:#fff}
nav.tabs .sep{width:14px}
section{margin-bottom:8px}
form.inline{display:inline;margin:0 4px 0 0}
button{font-size:12px;padding:3px 10px;cursor:pointer}
button.primary{background:#5a1a2f;color:#fff;border:1px solid #5a1a2f;border-radius:3px}
a.button{display:inline-block;font-size:12px;padding:2px 10px;border:1px solid #5a1a2f;border-radius:3px;text-decoration:none;margin-right:4px}
textarea{width:100%;font-family:"DejaVu Sans Mono",Menlo,monospace;font-size:12px}
label.field{display:grid;grid-template-columns:200px 1fr;gap:8px;align-items:start;margin:6px 0}
label.field .label{font-weight:bold;padding-top:3px}
label.field .hint{grid-column:2;color:#666;font-size:11px}
dl.kv{display:grid;grid-template-columns:220px 1fr;gap:3px 12px;margin:6px 0}
dl.kv dt{color:#555}dl.kv dd{margin:0}
pre{background:#f7f8fa;border:1px solid #e2e2e2;padding:8px;overflow:auto;max-height:520px;font-size:12px;white-space:pre-wrap}
.msg{padding:7px 10px;border-radius:3px;margin:8px 0;border:1px solid}
.msg-info{background:#eef5fb;border-color:#b9d4ea}.msg-ok{background:#eef8ee;border-color:#a9d5a9}
.msg-warn{background:#fff8e5;border-color:#ecd38a}.msg-error{background:#fdeeee;border-color:#e3a5a5}
.state{display:inline-block;padding:0 6px;border-radius:9px;font-size:11px;border:1px solid #bbb;white-space:nowrap}
.s-todo{background:#f4f4f4}.s-doing{background:#e6f0fb;border-color:#9cc0e6}.s-review{background:#fff4d6;border-color:#e3c46b}
.s-done{background:#e5f4e5;border-color:#8cc48c}.s-error{background:#fbe3e3;border-color:#d99}
.subtabs{display:flex;gap:6px;margin:10px 0}
.subtabs a{padding:3px 10px;border:1px solid #d8c9cf;border-radius:3px;text-decoration:none}
.subtabs a.active{background:#5a1a2f;color:#fff}
td.num,th.num{text-align:right}
.steps td{white-space:nowrap}
"""

COPY_JS = """
function ecvCopy(id){var t=document.getElementById(id);navigator.clipboard.writeText(t.value!==undefined?t.value:t.textContent);}
"""


def _scope_selector(app, current_path):
    def option(scope, text):
        return f'<option value="{e(scope.name)}"{" selected" if scope.name == app.scope_name else ""}>{e(text)}</option>'
    groups = []
    for scope in app.scopes():
        items = [option(scope, f"{scope.title} (todas as declarações)")]
        items += [option(d, f"· {d.title}") for d in app.declaration_scopes(scope.name)]
        groups.append(f'<optgroup label="{e(scope.title)}">' + "".join(items) + "</optgroup>")
    options = "".join(groups)
    return (f'<form method="post" action="/ambito"><label for="ambito">Âmbito</label>'
            f'<select id="ambito" name="ambito" onchange="this.form.submit()">{options}</select>'
            f'<input type="hidden" name="voltar" value="{e(current_path)}"><noscript><button>Mudar</button></noscript></form>')


def _database_badge(app):
    db = app.database
    rejected = f" · {len(db.info.rejected)} rejeitada(s)" if db.info and db.info.rejected else ""
    where = f"Neo4j {db.neo4j['uri']}" if db.backend == "neo4j" else "memória"
    return f'<span class="db">base de dados: {e(where)} · versão {db.version}{e(rejected)}</span>'


def _tabs(active):
    out = []
    for tab in TABS:
        if tab is None:
            out.append('<span class="sep"></span>')
            continue
        ident, label, href = tab
        out.append(f'<a href="{href}" class="{"active" if ident == active else ""}">{e(label)}</a>')
    return '<nav class="tabs">' + "".join(out) + "</nav>"


def page(app, tab, title, body, path="/", subtitle=""):
    sub = f'<p class="subtitle">{e(subtitle)}</p>' if subtitle else ""
    return (f'<!doctype html>\n<html lang="pt"><head><meta charset="utf-8">'
            f'<meta name="viewport" content="width=device-width, initial-scale=1">'
            f"<title>{e(title)} · ECV</title><style>{CSS}{APP_CSS}</style></head><body>"
            f'<header class="app"><a class="brand" href="/">ECV</a>{_scope_selector(app, path)}{_database_badge(app)}</header>'
            f"{_tabs(tab)}<main><h1>{e(title)}</h1>{sub}{body}</main>"
            f"<script>{JS}{COPY_JS}</script></body></html>\n")


def error_page(app, status, message):
    title = {404: "Não existe", 405: "Método não permitido", 500: "Erro interno"}.get(status, "Pedido não concluído")
    return page(app, "", title, f'<div class="msg msg-error">{e(message)}</div>'
                f'<p class="note">O registo do servidor (separador Registo) tem o detalhe.</p>')
