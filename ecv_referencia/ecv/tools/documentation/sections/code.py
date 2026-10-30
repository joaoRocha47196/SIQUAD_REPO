"""Código: the modules, what each receives, needs and produces, the dependencies between them, and the files and
public definitions of each (read with ast); the tests."""
import ast

from ecv import MODULES, PACKAGE_DIR

from ..page import Diagram, e, io_block, table
from .common import ROOT, definitions_table, docstring, page, pre, syntax_tree

CRUMBS = [("index.html", "Visão geral"), ("codigo.html", "Código")]
SECTION = "Código"

# What each package receives, needs and produces (the same facts as the first lines of its __init__ docstring).
PACKAGES = {
    "transformer": ("Transforma os ficheiros de origem, cada um no seu formato, num inventário neutro.",
                    "o caminho de cada fonte e o nome do seu adaptador (<code>dominio.json</code>)", "um adaptador por formato; a pasta <code>data/</code>",
                    "um inventário por fonte: grupos, elementos e regras classificadas por categoria, com a origem"),
    "ecv_builder": ("Gera as declarações completas de um domínio num pedido ao LLM e organiza a sua revisão por camadas (A a F).",
                    "os inventários e a definição do domínio",
                    "a especificação interna, o processo de construção, as declarações de referência, as notas de revisão",
                    "o pedido de geração; da resposta, as declarações e o mapeamento; por camada, as verificações e os pedidos de alterações"),
    "amendments": ("Aplica alterações às declarações de um domínio, como operações de um vocabulário fechado.",
                   "operações (de uma resposta do LLM, de um formulário, de uma tabela CSV) ou um pedido em linguagem natural",
                   "as declarações, o reservatório e o mapeamento do domínio",
                   "as declarações alteradas de forma consistente, ou o prompt do pedido de alterações"),
    "ingestion": ("Leva cada declaração ao grafo: verifica, materializa e funde, sem duplicar.", "declarações e um grafo de destino",
                  "o modelo do grafo e a configuração", "o grafo com o que é novo e, por declaração, o relatório e o plano da fusão"),
    "graph": ("Define o modelo do grafo, a interface de leitura e os dois armazenamentos; mantém a base de dados da aplicação.",
              "nós e arestas (da ingestão); um âmbito de declarações (base de dados)", "o driver do Neo4j, quando é o backend",
              "o grafo em memória ou no Neo4j, lido pela mesma interface"),
    "views": ("Calcula os ViewModels (operações sobre o grafo) e desenha as vistas.", "o grafo, o nome de uma vista e os seus parâmetros",
              "o catálogo das vistas (que vistas existem para o grafo)", "o ViewModel em JSON e a página HTML"),
    "validation": ("Avalia uma instância concreta de um HLM contra as regras, no cenário de um perfil; gere as implementações das funções.",
                   "o grafo, a instância (JSON), o perfil ou o HLM e os contextos externos", "uma implementação de cada função chamada pelas regras",
                   "o ViewModel <code>validacao</code>: problemas estruturais, o estado de cada regra em cada ocorrência, as conclusões"),
    "webapp": ("Dá acesso, numa aplicação web, a todas as operações dos módulos 0 a 6.", "pedidos HTTP",
               "a área de trabalho, a base de dados do âmbito ativo e as filas de pedidos", "páginas HTML e JSON"),
}
SUPPORT = {
    "config": ("O ficheiro único de configuração e o seu acesso.", "—", "<code>ecv/config/ecv.config.json</code>", "constantes e caminhos"),
    "shared": ("A área de trabalho dos domínios, a troca de pedidos com o LLM, os erros e o formato JSON.", "—", "a configuração",
               "<code>Workspace</code>, <code>Domain</code>, <code>RequestQueue</code>, <code>LlmRequest</code>"),
    "tools": ("O gerador deste site.", "o repositório (specs, código, configuração, catálogo das vistas)", "—", "<code>documentacao/site/</code>"),
}
ORDER = list(MODULES) + list(SUPPORT)


def _folder(name):
    return PACKAGE_DIR / MODULES.get(name, name)


def _python_files(name):
    return sorted(f for f in _folder(name).rglob("*.py") if "__pycache__" not in f.parts)


def _imports(name):
    """The ecv packages a package imports."""
    found = set()
    for f in _python_files(name):
        for n in ast.walk(syntax_tree(f)):
            if isinstance(n, ast.ImportFrom) and n.module and n.level == 0 and n.module.startswith("ecv."):
                found.add(n.module.split(".")[1])
            elif isinstance(n, ast.ImportFrom) and n.level == 0 and n.module == "ecv":
                found |= {a.name for a in n.names}
    return {x for x in found if x in ORDER and x != name}


def _title(name):
    return f"{MODULES[name].split('_')[0]} · {name}" if name in MODULES else name


def dependency_diagram():
    rows = [["webapp"], ["ecv_builder", "validation"], ["amendments", "views", "transformer"], ["ingestion"], ["graph"], ["config", "shared"]]
    d = Diagram(1100, len(rows) * 95 + 10)
    for i, row in enumerate(rows):
        for j, name in enumerate(row):
            x = 550 - len(row) * 320 / 2 + j * 320 + 40
            d.box(name, x, 15 + i * 95, 240, 52, _title(name), [f"{len(_python_files(name))} ficheiro(s) .py"], f"modulo_{name}.html")
    for name in ORDER:
        if name == "tools":
            continue
        for other in sorted(_imports(name)):
            if other in d.boxes and name in d.boxes:
                d.arrow(name, other, None, color="#aaa")
    return d.render() + '<p class="note">Setas: o módulo importa o outro. A aplicação web e o construtor dependem dos restantes; o grafo e a configuração não dependem de nenhum.</p>'


def overview_page():
    body = ("<p>O código está em <code>ecv/</code>, em inglês; os formatos de dados (as chaves das declarações, do grafo, dos inventários e dos ViewModels), "
            "as mensagens e a interface ficam em português, como a especificação. Os módulos numerados importam-se pelo nome sem número "
            "(<code>import ecv.transformer</code> carrega <code>ecv/0_transformer</code>; a correspondência está em <code>ecv/__init__.py</code>).</p>")
    body += dependency_diagram()
    rows = [[f'<a href="modulo_{n}.html">{e(_title(n))}</a>', e((PACKAGES.get(n) or SUPPORT[n])[0]), str(len(_python_files(n)))] for n in ORDER]
    body += table(["Módulo", "Responsabilidade", "Ficheiros .py"], rows)
    body += "<h2>Linha de comandos</h2>" + pre(docstring(PACKAGE_DIR / "cli.py"))
    return page("codigo", "Código: módulos", body, section=SECTION, menu="Módulos e dependências", crumbs=CRUMBS[:1])


def _module_links(names):
    return ", ".join(f'<a href="modulo_{x}.html">{e(_title(x))}</a>' for x in names) or "—"


def module_page(name):
    purpose, receives, needs, produces = PACKAGES.get(name) or SUPPORT[name]
    body = f"<p>{purpose}</p>" + io_block(receives, needs, produces)
    deps = sorted(_imports(name))
    users = sorted(n for n in ORDER if name in _imports(n))
    body += f"<p><b>Usa:</b> {_module_links(deps)} · <b>Usado por:</b> {_module_links(users)}</p>"
    files = _python_files(name)
    folder = _folder(name)
    body += "<h2>Ficheiros</h2>" + table(["Ficheiro", "O que contém"], [
        [f'<a href="#{e(str(f.relative_to(folder)))}"><code>{e(str(f.relative_to(folder)))}</code></a>', e(docstring(f).split("\n\n")[0])] for f in files])
    body += "<h2>Definições públicas</h2>"
    for f in files:
        rel = str(f.relative_to(folder))
        body += f'<h3 id="{e(rel)}"><code>{e(str(f.relative_to(ROOT)))}</code></h3>'
        doc = docstring(f)
        if doc and "\n" in doc:
            body += pre(doc)
        body += definitions_table(f) or '<p class="note">(sem definições públicas)</p>'
    return page(f"modulo_{name}", f"Código: {_title(name)}", body, section=SECTION, menu=_title(name), sub=True, crumbs=CRUMBS, summary=purpose)


def tests_page():
    rows = []
    for f in sorted((ROOT / "tests").glob("test_*.py")):
        for c in syntax_tree(f).body:
            if isinstance(c, ast.ClassDef):
                for m in c.body:
                    if isinstance(m, ast.FunctionDef) and m.name.startswith("test"):
                        rows.append([e(f.name), e(c.name), f"<code>{e(m.name)}</code>", e(ast.get_docstring(m) or ast.get_docstring(c) or "")])
    body = ("<p>A partir de <code>ecv_referencia</code>: <code>python -m unittest discover -s tests -t .</code>. Os testes com Neo4j correm quando a "
            "variável <code>NEO4J_URI</code> está definida. Os testes da aplicação web arrancam o servidor num porto livre, sobre uma cópia temporária "
            "de um domínio, e percorrem o ciclo completo por HTTP.</p>" + table(["Ficheiro", "Classe", "Teste", "Descrição"], rows))
    return page("testes", f"Testes ({len(rows)})", body, section=SECTION, menu="Testes", crumbs=CRUMBS[:1])


def pages():
    return [overview_page()] + [module_page(n) for n in ORDER] + [tests_page()]
