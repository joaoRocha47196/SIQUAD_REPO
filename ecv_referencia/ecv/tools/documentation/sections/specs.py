"""Specs: the entities, the transversal topics, the declaration, its schema and skeleton, the example declarations."""
import json

from ecv import config
from ecv.ingestion import Declaration

from ..page import e, layered_diagram, table
from .common import REPO, ROOT, markdown, markdown_title, page, json_pre, read, register_markdown, without_h1

COLORS = config.COLORS
CRUMBS = [("index.html", "Visão geral")]
SPECS_CRUMBS = CRUMBS + [("specs.html", "Specs")]

ENTITIES = {"HLM": "ecm/HLM", "SM": "ecm/SM", "USM": "ecm/USM", "Propriedade": "ecm/Propriedade", "Composicao": "ecm/Composicao",
            "Regra": "ecr/Regra", "RP": "ecr/RP", "RIR": "ecr/RIR", "RIC": "ecr/RIC", "Restricao": "ecr/Restricao",
            "CondicaoAplicabilidade": "ecr/CondicaoAplicabilidade", "Funcao": "ecr/Funcao", "ContextoExterno": "ecr/ContextoExterno",
            "RE_Projecao": "ecr/RE_Projecao", "Perfil": "ecr/Perfil"}
LINKS = [("HLM", "Composicao"), ("Composicao", "SM"), ("SM", "Composicao"), ("Composicao", "USM"), ("USM", "Propriedade"), ("SM", "Propriedade"),
         ("Regra", "RP"), ("Regra", "RIR"), ("Regra", "RIC"), ("RP", "Restricao"), ("RIR", "Restricao"), ("RIR", "CondicaoAplicabilidade"),
         ("RIC", "CondicaoAplicabilidade"), ("Restricao", "Funcao"), ("CondicaoAplicabilidade", "Funcao"), ("Funcao", "ContextoExterno"),
         ("RE_Projecao", "HLM"), ("Perfil", "RE_Projecao"), ("Restricao", "Propriedade"), ("CondicaoAplicabilidade", "Propriedade")]
ENTITY_COLOR = {"HLM": COLORS["HLM"], "SM": COLORS["SM"], "USM": COLORS["USM"], "RP": COLORS["RP"], "RIR": COLORS["RIR"], "RIC": COLORS["RIC"],
                "Restricao": COLORS["funcao"], "CondicaoAplicabilidade": COLORS["condicao"], "Funcao": COLORS["externo"],
                "ContextoExterno": COLORS["externo"]}


def register():
    """Register the Markdown files that become pages (before any page converts its links)."""
    for f in sorted((ROOT / "specs/entidades").rglob("*.md")):
        rel = str(f.relative_to(ROOT))
        name = "entidades" if f.name == "README.md" else ("transversal_" if "transversal" in rel else "entidade_") + f.stem
        register_markdown(rel, name)
    for rel, name in [("specs/README.md", "specs"), ("specs/declaracao/README.md", "declaracao"), ("specs/exemplos/README.md", "exemplos"),
                      ("specs/entidades/transversal/Verificacao.md", "verificacao"), ("README.md", "readme"),
                      ("ecv/5_views/viewmodels/README.md", "viewmodels")]:
        register_markdown(rel, name)


def _transversal_files():
    return sorted((ROOT / "specs/entidades/transversal").glob("*.md"))


def overview():
    diagram = layered_diagram(list(ENTITIES), [(a, b, None) for a, b in LINKS], href=lambda n: f"entidade_{n}.html",
                              color=lambda n: ENTITY_COLOR.get(n, "#555"), width=180, height=34, gy=14)
    body = diagram + without_h1(markdown("specs/README.md"))
    rows = [['<a href="entidades.html">Entidades (índice)</a>', "As entidades da ECV, a ordem de cada ficheiro, o mapa e o resumo de atributos e ligações"]]
    rows += [[f'<a href="entidade_{n}.html">{e(n)}</a>', e(markdown_title(f"specs/entidades/{p}.md"))] for n, p in ENTITIES.items()]
    rows += [[f'<a href="transversal_{f.stem}.html">{e(f.stem)}</a>', e(markdown_title(str(f.relative_to(ROOT))))]
             for f in _transversal_files() if f.stem != "Verificacao"]
    rows += [['<a href="verificacao.html">Verificação</a>', "Specs e invariantes I1 a I13"],
             ['<a href="declaracao.html">Declaração ECV</a>', "Estrutura, uma declaração por HLM, possibilidades e razões"],
             ['<a href="esquema.html">JSON Schema</a>', "A forma da declaração"],
             ['<a href="esqueleto.html">Esqueleto</a>', "Uma ocorrência de cada construção"],
             ['<a href="exemplos.html">Exemplos</a>', "As declarações de exemplo (uma por HLM)"],
             ['<a href="especificacao_interna.html">Especificação interna</a>', "O texto único, gerado a partir destas páginas, que entra nos prompts"]]
    body += "<h2>Páginas das specs</h2>" + table(["Página", "Conteúdo"], rows)
    return page("specs", "Specs", body, summary="A especificação da ECV, sem código: entidades, declaração e exemplos.", section="Specs",
                crumbs=CRUMBS, mermaid=True)


def entity_pages():
    out = [page("entidades", markdown_title("specs/entidades/README.md"), without_h1(markdown("specs/entidades/README.md")), section="Specs",
                menu="Entidades (índice)", crumbs=SPECS_CRUMBS, mermaid=True, sub=True)]
    for name, path in ENTITIES.items():
        rel = f"specs/entidades/{path}.md"
        out.append(page(f"entidade_{name}", markdown_title(rel), without_h1(markdown(rel)), section="Specs", menu=name, sub=True,
                        crumbs=SPECS_CRUMBS + [("entidades.html", "Entidades")], mermaid=True))
    for f in _transversal_files():
        rel = str(f.relative_to(ROOT))
        name = "verificacao" if f.stem == "Verificacao" else f"transversal_{f.stem}"
        out.append(page(name, markdown_title(rel), without_h1(markdown(rel)), section="Specs", menu=f.stem, sub=True, crumbs=SPECS_CRUMBS,
                        mermaid=True))
    return out


def declaration_pages():
    out = [page("declaracao", markdown_title("specs/declaracao/README.md"), without_h1(markdown("specs/declaracao/README.md")), section="Specs",
                menu="Declaração ECV", crumbs=SPECS_CRUMBS, mermaid=True),
           page("esquema", "JSON Schema da declaração", json_pre(json.loads(read("specs/declaracao/ecv.schema.json"))), section="Specs",
                menu="JSON Schema", sub=True, crumbs=SPECS_CRUMBS + [("declaracao.html", "Declaração")],
                summary="A forma (sintaxe) da Declaração ECV; o resto (caminhos, tipos, invariantes) é verificado pela ingestão."),
           page("esqueleto", "Esqueleto da declaração", json_pre(json.loads(read("specs/declaracao/esqueleto.ecv.json"))), section="Specs",
                menu="Esqueleto", sub=True, crumbs=SPECS_CRUMBS, summary="Uma ocorrência de cada construção possível, com nomes neutros.")]
    rows = []
    for f in config.example_declarations():
        d = Declaration.load(f)
        kinds = {}
        for site in d.rules():
            kinds[site.type] = kinds.get(site.type, 0) + 1
        rows.append([f'<a href="{REPO}specs/exemplos/{e(f.name)}">{e(f.name)}</a>', e(d.hlm_name), len(d.sm), len(d.usm),
                     ", ".join(f"{v} {k}" for k, v in sorted(kinds.items())), len(d.functions), len(d.projections), len(d.profiles)])
    body = table(["Ficheiro", "HLM", "SM", "USM", "Regras", "Funções", "Projeções", "Perfis"], rows) + without_h1(markdown("specs/exemplos/README.md"))
    out.append(page("exemplos", "Declarações de exemplo", body, section="Specs", menu="Exemplos", crumbs=SPECS_CRUMBS, mermaid=True))
    return out


def pages():
    return [overview()] + entity_pages() + declaration_pages()
