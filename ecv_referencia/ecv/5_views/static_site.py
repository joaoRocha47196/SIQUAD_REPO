"""Every view of a graph written to a folder: for each view, its ViewModel (.json) and its page (.html),
plus an index. Used for the example views linked from the documentation (documentacao/vistas/); the
web application does not use it: it builds each view on request."""
import json
from pathlib import Path

from . import links as L
from .catalog import catalog
from .presentation import render_page
from .presentation.html import chip, e, page, table
from .viewmodels import build
from .viewmodels import common as K


def generate(g, folder, title="Vistas da ECV", origin=None):
    folder = Path(folder)
    folder.mkdir(parents=True, exist_ok=True)
    entries = catalog(g)
    L.set_existing(entry.page for entry in entries)
    edit_base, L.EDIT_BASE = L.EDIT_BASE, None          # static pages have no edit links
    try:
        return _write(g, folder, entries, title, origin)
    finally:
        L.EDIT_BASE = edit_base


def _write(g, folder, entries, title, origin):
    done = []
    for entry in entries:
        vm = build(g, entry.viewmodel, **entry.params)
        (folder / f"{entry.page}.json").write_text(json.dumps(vm, ensure_ascii=False, indent=2), encoding="utf-8")
        (folder / f"{entry.page}.html").write_text(render_page(vm, f"{entry.page}.json"), encoding="utf-8")
        done.append((entry, vm))
    (folder / "index.html").write_text(index_page(g, done, title, origin), encoding="utf-8")
    return done


def _cards(items):
    return '<div class="grid">' + "".join(
        f'<div class="card"><h3>{L.link(entry.page, entry.title)}</h3><span class="note"><a href="{e(entry.page)}.json">ViewModel (JSON)</a></span></div>'
        for entry, _ in items) + "</div>"


def _hlm_cards(g):
    out = '<h2>Por HLM</h2><div class="grid">'
    for d in sorted(g.nodes("HLM"), key=lambda n: n["nome"]):
        h = d["nome"]
        profiles = sorted({pf["nome"] for pj in g.sources(d, "PROJETA") for pf in g.sources(pj, "USA")})
        out += (f'<div class="card"><h3><span class="tag HLM">HLM</span>{L.link(L.model_page("HLM", h), h, css="n-HLM")}</h3>'
                f'<span class="note">{e(d.get("descricao"))}</span><br>'
                f'{L.link(L.model_page("HLM", h), "modelo")} · {L.link(L.rules_page(h), "modelo com regras")} · '
                f'{L.link(L.projections_page(h), "projeções")} · {L.link(L.gaps_page(h), "lacunas")}'
                + (("<br>perfis: " + ", ".join(L.link(L.profile_page(x), x) for x in profiles)) if profiles else "") + "</div>")
    return out + "</div>"


def _models_table(g):
    rows = []
    for level in ("SM", "USM"):
        for m in sorted(g.nodes(level), key=lambda n: n["nome"]):
            hlms = K.hlms_using(g, m)
            rows.append([f'<span class="tag {level}">{level}</span>' + L.link(L.model_page(level, m["nome"]), m["nome"], css=f"n-{level}"),
                         e(m.get("descricao")), " ".join(L.link(L.model_page("HLM", h), h, css="n-HLM") for h in hlms),
                         "partilhado" if len(hlms) > 1 else ""])
    return "<h2>Modelos (SM e USM)</h2>" + table(["Modelo", "Descrição", "Usado pelos HLM", ""], rows)


def index_page(g, done, title, origin):
    groups = {}
    for entry, vm in done:
        groups.setdefault(entry.group, []).append((entry, vm))
    declarations = sorted(g.nodes("Declaracao"), key=lambda d: d.get("hlm") or "")
    body = "<h2>Declarações ingeridas</h2>"
    body += table(["Declaração", "HLM", "Versão", "Descrição"],
                  [[e(d["nome"]), L.link(L.model_page("HLM", d.get("hlm")), d.get("hlm"), css="n-HLM"), e(d.get("versao")),
                    e(d.get("descricao"))] for d in declarations]) if declarations else f"<p>{e(origin)}</p>"
    body += _hlm_cards(g) + _models_table(g)
    for group in ("Decisão", "Dependências e impacto", "Perfis", "Validação de instâncias", "Verificações transversais"):
        if group in groups:
            body += f"<h2>{e(group)}</h2>" + _cards(groups[group])
    if "Fichas das regras" in groups:
        items = groups["Fichas das regras"]
        body += f"<h2>Fichas das regras ({len(items)})</h2><p>" + " ".join(
            chip(vm["regra"]["categoria"], entry.title, vm["regra"]["descricao"], href=f"{entry.page}.html") for entry, vm in items) + "</p>"
    return page(title, f'<p class="subtitle">{len(done)} vistas geradas a partir do grafo ({e(origin)}).</p>' + body, back=False)
