"""Small HTML pieces shared by the handlers."""
import json

from ecv.views.presentation.html import chip, e, table

STATE_CLASSES = {"por iniciar": "s-todo", "em curso": "s-doing", "em revisão": "s-review", "aceite": "s-done",
                 "pendente": "s-todo", "respondido": "s-doing", "aplicado": "s-done", "rejeitado": "s-error"}

__all__ = ["e", "chip", "table", "state", "section", "button_form", "code", "json_block", "message", "field", "textarea",
           "select", "pre", "details", "keyvalues"]


def state(text):
    return f'<span class="state {STATE_CLASSES.get(text, "")}">{e(text)}</span>'


def section(title, body, anchor=None):
    a = f' id="{e(anchor)}"' if anchor else ""
    return f"<section{a}><h2>{e(title)}</h2>{body}</section>"


def button_form(action, label, fields=None, css="", confirm=None):
    hidden = "".join(f'<input type="hidden" name="{e(k)}" value="{e(v)}">' for k, v in (fields or {}).items())
    onsubmit = f' onsubmit="return confirm({e(json.dumps(confirm))})"' if confirm else ""
    return f'<form method="post" action="{e(action)}" class="inline"{onsubmit}>{hidden}<button class="{css}">{e(label)}</button></form>'


def code(text):
    return f"<code>{e(text)}</code>"


def pre(text, css=""):
    return f'<pre class="{css}">{e(text)}</pre>'


def json_block(data):
    return pre(json.dumps(data, ensure_ascii=False, indent=1), "json")


def message(text, kind="info"):
    """kind: info | ok | warn | error."""
    return f'<div class="msg msg-{kind}">{e(text)}</div>' if text else ""


def field(label, control, hint=""):
    h = f'<span class="hint">{e(hint)}</span>' if hint else ""
    return f'<label class="field"><span class="label">{e(label)}</span>{control}{h}</label>'


def textarea(name, value="", rows=10, placeholder="", ident=None):
    i = f' id="{e(ident)}"' if ident else ""
    return f'<textarea name="{e(name)}"{i} rows="{rows}" placeholder="{e(placeholder)}">{e(value)}</textarea>'


def select(name, options, selected=None, ident=None):
    """options: [(value, text)]."""
    i = f' id="{e(ident)}"' if ident else ""
    opts = "".join(f'<option value="{e(v)}"{" selected" if v == selected else ""}>{e(t)}</option>' for v, t in options)
    return f'<select name="{e(name)}"{i} autocomplete="off">{opts}</select>'


def details(summary, body, open_=False):
    return f'<details{" open" if open_ else ""}><summary>{e(summary)}</summary>{body}</details>'


def keyvalues(pairs):
    """A two-column list of (label, html value)."""
    return '<dl class="kv">' + "".join(f"<dt>{e(k)}</dt><dd>{v}</dd>" for k, v in pairs) + "</dl>"


def where_box(rows):
    """'Onde está, no código e nos ficheiros': [(what, location)]; locations in <code> unless they already have markup."""
    cells = [[e(a), b if b.startswith(("<code", "<a ")) else f"<code>{e(b)}</code>"] for a, b in rows]
    return section("Onde está, no código e nos ficheiros", table(["O quê", "Onde"], cells))
