"""The documentation site (documentacao/site/): static HTML pages, independent of the web application.

    python -m ecv documentacao        writes documentacao/site/ (open index.html)

Each section (sections/*.py) returns pages (dictionaries: name, title, body, summary, crumbs, mermaid); this
module adds the side menu and writes the files. The content comes from the repository itself: the
configuration, the specs (Markdown), the graph model, the view catalogue, the build process, the domains,
the route table, the code (read with ast) and the texts in documentacao/textos/.
"""
import shutil
from pathlib import Path

from ecv import config

from .page import page as render
from .sections import code, common, graph_views, overview, specs, transformation, webapp

SECTIONS = ["Visão geral", "Specs", "Transformação", "Ingestão e grafo", "Vistas", "Aplicação web", "Código"]


def all_pages():
    common.MARKDOWN_PAGES.clear()
    specs.register()                         # the Markdown pages are registered before any link is converted
    for rel, name in [("ecv/3_ingestion/README.md", "ingestao"), ("ecv/4_graph/README.md", "grafo"), ("ecv/5_views/README.md", "vistas")]:
        common.register_markdown(rel, name)
    out = []
    for section in (overview, specs, transformation, graph_views, webapp, code):
        out += section.pages()
    return out


def menu(pages):
    items = {s: [] for s in SECTIONS}
    for p in pages:
        items.setdefault(p["secao"] or "Outras", []).append((f"{p['nome']}.html", p["menu"], p["sub"]))
    return [(s, x) for s, x in items.items() if x]


def generate(folder=None):
    folder = Path(folder or config.path("documentacao") / "site")
    if folder.exists():
        shutil.rmtree(folder)
    folder.mkdir(parents=True)
    pages = all_pages()
    side = menu(pages)
    for p in pages:
        (folder / f"{p['nome']}.html").write_text(
            render(p["nome"], p["titulo"], p["corpo"], side, p.get("resumo"), p.get("migalhas"), p.get("mermaid", False)), encoding="utf-8")
    return folder, len(pages)
