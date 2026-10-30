"""Vistas (module 5): the catalogue of the views of the active graph and each view, built on request.

No page is stored: /vistas/<página>.html looks the page up in the catalogue, builds its ViewModel from
the graph (cached until the database changes) and draws it. /api/vm/<página> returns the same
ViewModel as JSON. The static pages in documentacao/vistas are the same views of the example
declarations, generated once for the documentation.
"""
import json

from ecv.views.catalog import GROUPS
from ecv.views.presentation import render_body
from ecv.views.viewmodels import REGISTRY, build

from ..http import Response, bad_request, not_found, url
from ..pages import layout
from ..pages.components import e, message, section


def _declarations_picker(app):
    """Links to the views of each declaration of the active base scope (the examples or the domain)."""
    from ..context import base_scope
    base = base_scope(app.scope_name)
    links = [f'<a href="{url("/vistas", ambito=base)}">{"<b>todas</b>" if app.scope_name == base else "todas"}</a>']
    for scope in app.declaration_scopes(base):
        label = e(scope.title.replace("Declaração ", ""))
        links.append(f'<a href="{url("/vistas", ambito=scope.name)}">{"<b>" + label + "</b>" if scope.name == app.scope_name else label}</a>')
    return "<p><b>Declarações:</b> " + " · ".join(links) + "</p>"


def _ingestion_notice(app):
    """Why a declaration has no views: the ingestion rejected it (verification errors or merge conflicts)."""
    info = app.database.info
    if not info or not info.rejected:
        return ""
    return message("Declarações não ingeridas (sem vistas até serem corrigidas): " + " | ".join(r.summary() for r in info.rejected), "warn")


def catalogue_page(app, request):
    if request.get("ambito"):
        app.use_scope(request.get("ambito"))
        return Response.redirect("/vistas", note=f"âmbito {request.get('ambito')}")
    entries = app.catalogue()
    by_group = {}
    for entry in entries.values():
        by_group.setdefault(entry.group, []).append(entry)
    body = _declarations_picker(app) + _ingestion_notice(app)
    body += f"<p>{len(entries)} vistas para {e(app.database.scope.title)}.</p>"
    for group in GROUPS:
        items = by_group.get(group, [])
        if items:
            body += section(f"{group} ({len(items)})", "<p>" + " · ".join(
                f'<a href="/vistas/{e(x.page)}.html">{e(x.title or x.page)}</a>' for x in items) + "</p>")
    return Response.html(layout.page(app, "vistas", "Vistas", body, request.path,
                                     "Cada vista é um ViewModel (dados extraídos do grafo) desenhado em HTML no momento em que é pedido."))


def _entry(app, page):
    entry, vm = app.viewmodel(page)
    if entry is None:
        raise not_found(f"a vista {page} não existe para o âmbito ativo (ver /vistas)")
    return entry, vm


def view_page(app, request):
    name = request.params["pagina"]
    page, _, ext = name.rpartition(".")
    if ext == "json":
        return viewmodel_api(app, request, page)
    if ext != "html":
        raise not_found(name)
    entry, vm = _entry(app, page)
    body = render_body(vm) + (f'<p class="note footer">ViewModel <code>{e(entry.viewmodel)}</code> · '
                              f'<a href="/api/vm/{e(page)}">dados (JSON)</a> · <a href="/vistas">catálogo</a></p>')
    return Response.html(layout.page(app, "vistas", vm["titulo"], body, request.path), note=entry.viewmodel)


def catalogue_api(app, request):
    return Response.json({p: {"grupo": x.group, "viewmodel": x.viewmodel, "parametros": x.params, "titulo": x.title}
                          for p, x in app.catalogue().items()})


def viewmodel_api(app, request, page=None):
    _, vm = _entry(app, page or request.params["pagina"])
    return Response.json(vm)


def build_api(app, request):
    data = request.json()
    name = data.get("viewmodel")
    if name not in REGISTRY:
        raise bad_request(f"ViewModel desconhecido: {name} ({', '.join(REGISTRY)})")
    return Response.json(json.loads(json.dumps(build(app.graph, name, **(data.get("parametros") or {})), default=str)))
