"""Helpers shared by the sections: pages as dictionaries, Markdown files turned into pages (with their links
rewritten to the site), texts with diagrams, code tables read with ast."""
import ast
import json
import re
from pathlib import Path

from ecv import config

from ..markdown import convert
from ..page import e, table

ROOT = config.ROOT
REPO = "../../"                          # from the site (documentacao/site) to the root of ecv_referencia
MARKDOWN_PAGES = {}                      # relative path of a .md -> page name


def page(name, title, body, summary=None, crumbs=None, mermaid=False, section=None, menu=None, sub=False):
    return {"nome": name, "titulo": title, "corpo": body, "resumo": summary, "migalhas": crumbs, "mermaid": mermaid,
            "secao": section, "menu": menu or title, "sub": sub}


def read(rel):
    return (ROOT / rel).read_text(encoding="utf-8")


def pre(text):
    return f'<pre class="code"><code>{e(text)}</code></pre>'


def json_pre(data):
    return pre(json.dumps(data, ensure_ascii=False, indent=1))


def register_markdown(rel, name):
    MARKDOWN_PAGES[str(Path(rel))] = name


def link_from(rel_md):
    """The link rewriter of a Markdown file: known .md files become pages; other files point into the repository."""
    base = (ROOT / rel_md).parent

    def rewrite(target):
        if re.match(r"^[a-z]+:", target) or target.startswith("#") or re.match(r"^[\w-]+\.html(#.*)?$", target):
            return target                    # external, anchor, or a page of the site
        path, _, frag = target.partition("#")
        try:
            dest = str((base / path).resolve().relative_to(ROOT))
        except ValueError:
            return REPO + "../" + str((base / path).resolve().relative_to(ROOT.parent))
        suffix = f"#{frag}" if frag else ""
        if dest in MARKDOWN_PAGES:
            return MARKDOWN_PAGES[dest] + ".html" + suffix
        return REPO + dest + suffix
    return rewrite


def markdown(rel):
    body, _ = convert(read(rel), link_from(rel))
    return body + f'<p class="note">Fonte: <a href="{REPO}{e(rel)}">{e(rel)}</a></p>'


def markdown_title(rel):
    m = re.search(r"(?m)^# (.+)$", read(rel))
    return m.group(1).strip() if m else Path(rel).stem


def without_h1(html):
    return re.sub(r"^<h2 id=[^>]*>.*?</h2>\n?", "", html, count=1)


def text(name, diagrams=None):
    """A text of documentacao/textos/, with the {{diagrama:x}} marks replaced; returns (html, toc)."""
    rel = f"documentacao/textos/{name}.md"
    source = re.sub(r"\A# .*\n", "", read(rel))              # the title comes from the page
    source = re.sub(r"(?m)^#(#+) ", r"\1 ", source)           # ## becomes <h2>
    html, toc = convert(source, link_from(rel))
    for key, value in (diagrams or {}).items():
        html = html.replace(f"<p>{{{{diagrama:{key}}}}}</p>", value)
    return html, toc


# ---------------------------------------------------------------------- code read with ast
def syntax_tree(path):
    return ast.parse(Path(path).read_text(encoding="utf-8"))


def docstring(path):
    return ast.get_docstring(syntax_tree(path)) or ""


def definitions_table(path):
    """Public functions and classes of a file (with the methods of each class) and the first paragraph of their docstring."""
    rows = []
    for n in syntax_tree(path).body:
        if isinstance(n, ast.FunctionDef) and not n.name.startswith("_"):
            rows.append([f"<code>def {e(n.name)}({e(', '.join(a.arg for a in n.args.args))})</code>",
                         e((ast.get_docstring(n) or "").split("\n\n")[0])])
        elif isinstance(n, ast.ClassDef) and not n.name.startswith("_"):
            rows.append([f"<code>class {e(n.name)}</code>", e((ast.get_docstring(n) or "").split("\n\n")[0])])
            for m in n.body:
                if isinstance(m, ast.FunctionDef) and not m.name.startswith("_"):
                    rows.append([f"&nbsp;&nbsp;<code>.{e(m.name)}({e(', '.join(a.arg for a in m.args.args[1:]))})</code>",
                                 e((ast.get_docstring(m) or "").split("\n\n")[0])])
    return table(["Definição", "Descrição (docstring)"], rows) if rows else ""
