"""Ingestão e grafo (ingestion, merge, graph, database, one page per node and edge type) and Vistas (navigation,
one page per kind of view, ViewModels, presentation)."""
import re

from ecv import config
from ecv.graph.model import load_model
from ecv.views.presentation import TRAVERSALS
from ecv.views.viewmodels import REGISTRY

from .. import view_schemas
from ..markdown import convert
from ..page import Diagram, e, io_block, layered_diagram, table
from .common import REPO, ROOT, docstring, link_from, markdown, page, pre, read, without_h1

COLORS = config.COLORS
CRUMBS = [("index.html", "Visão geral")]
GRAPH_SECTION, VIEWS_SECTION = "Ingestão e grafo", "Vistas"


def ingestion_page():
    d = Diagram(1180, 200)
    steps = [("load", "1. Carregar", ["declaration.py"], "#processamento"), ("verify", "2. Verificar", ["verification/", "schema, specs, I1–I13"], "verificacao.html"),
             ("mat", "3. Materializar", ["materialization.py"], "#processamento"), ("plan", "4. Planear a fusão", ["merge.py"], "fusao.html"),
             ("apply", "5. Aplicar", ["memória ou Neo4j"], "fusao.html#aplicar")]
    for i, (k, t, lines, href) in enumerate(steps):
        d.box(k, 20 + i * 232, 60, 200, 80, t, lines, href, COLORS["SM"] if i < 3 else COLORS["HLM"])
        if i:
            d.arrow(steps[i - 1][0], k)
    body = io_block("declarações (ficheiros ou objetos <code>Declaration</code>) e um grafo de destino", "o modelo do grafo e a configuração",
                    "o grafo de destino com os nós e as arestas novos; um <code>IngestionResult</code> por declaração (relatório da verificação e plano da fusão)")
    body += d.render() + without_h1(markdown("ecv/3_ingestion/README.md"))
    return page("ingestao", "Ingestão", body, section=GRAPH_SECTION, menu="Ingestão", mermaid=True, crumbs=CRUMBS,
                summary="Da declaração ao grafo: verificar, materializar e fundir, sem duplicar.")


def merge_page():
    model = load_model()
    body = pre(docstring(ROOT / "ecv/3_ingestion/merge.py"))
    body += table(["No grafo existente", "Resultado"], [["não existe", "novo: o nó entra com todas as arestas de que é dono"],
                                                       ["existe e é igual", "reutilizado: nada se escreve"],
                                                       ["existe e é diferente", "conflito: a declaração é rejeitada, com a diferença exata"]])
    body += "<h2>Dono de cada aresta</h2>" + table(["Aresta", "De → para", "Dono"], [
        [f'<a href="aresta_{e(k)}.html">{e(k)}</a>', e(", ".join(v["de"]) + " → " + ", ".join(v["para"])), e(v.get("dono"))]
        for k, v in model["arestas"].items()])
    body += ('<h2 id="aplicar">Aplicar</h2><p>Em memória: <code>apply_to_memory</code>. No Neo4j: <code>neo4j_store.append</code> (lotes UNWIND, '
             'extremos procurados pela chave). O plano é calculado pela interface <code>Graph</code>, por isso é igual nos dois.</p>')
    return page("fusao", "Fusão", body, section=GRAPH_SECTION, menu="Fusão", sub=True, crumbs=CRUMBS + [("ingestao.html", "Ingestão")])


def _node_colors(model):
    colors = {n: next((g["cor"] for g in model["grupos"].values() if n in g["nos"]), "#555") for n in model["nos"]}
    colors.update({"HLM": COLORS["HLM"], "SM": COLORS["SM"], "USM": COLORS["USM"]})
    return colors


def _edges(model):
    return [(a, b, t) for t, spec in model["arestas"].items() for a in spec["de"] for b in spec["para"]]


ORDER = ["Declaracao", "Perfil", "Projecao", "HLM", "SM", "USM", "Propriedade", "RP", "RIR", "RIC", "Restricao", "CondicaoAplicabilidade",
         "Funcao", "ContextoExterno"]


def graph_page():
    model = load_model()
    colors = _node_colors(model)
    body = layered_diagram([n for n in ORDER if n in model["nos"]], _edges(model), href=lambda n: f"no_{n}.html", color=lambda n: colors[n],
                           sub=lambda n: [f"chave: {model['nos'][n]['chave']}"], width=200, height=40, gx=110, gy=16)
    body += '<p class="note">Cada caixa abre a página do tipo de nó.</p>' + without_h1(markdown("ecv/4_graph/README.md"))
    return page("grafo", "Grafo", body, section=GRAPH_SECTION, menu="Grafo: modelo e armazenamento", mermaid=True, crumbs=CRUMBS,
                summary="Para que serve o grafo, os tipos de nó e de aresta, a interface comum e onde o grafo vive.")


def database_page():
    d = Diagram(1180, 260)
    d.box("ex", 20, 30, 220, 50, "Âmbito: exemplos", ["specs/exemplos/*.ecv.json"], "exemplos.html", COLORS["SM"])
    d.box("dom", 20, 110, 220, 50, "Âmbito: um domínio", ["dominios/<d>/declaracoes/"], "dominios.html", COLORS["SM"])
    d.box("fp", 290, 70, 170, 60, "Impressão digital", ["caminhos e datas", "dos ficheiros"], None, "#444")
    d.box("ing", 510, 70, 160, 60, "Ingestão", ["MemoryGraph"], "ingestao.html")
    d.box("mem", 720, 20, 180, 60, "backend memória", ["o MemoryGraph é a base"], None, COLORS["HLM"])
    d.box("neo", 720, 120, 180, 60, "backend neo4j", ["limpa e carrega;", "consultas em Cypher"], None, "#555")
    d.box("app", 960, 70, 200, 60, "Aplicação web", ["vistas, validação, pesquisa"], "aplicacao.html", "#0072B2")
    d.box("chg", 510, 190, 160, 50, "Módulos 1 e 2", ["alteram os ficheiros"], "transformacao.html", "#8B1E3F")
    for a, b in [("ex", "fp"), ("dom", "fp"), ("fp", "ing"), ("ing", "mem"), ("ing", "neo"), ("mem", "app"), ("neo", "app")]:
        d.arrow(a, b)
    d.arrow("chg", "dom", "o âmbito muda", dashed=True)
    body = io_block("um âmbito: o nome e a lista dos seus ficheiros de declaração", "o backend (memória ou Neo4j, com as credenciais da configuração)",
                    "o grafo do âmbito, que as consultas leem pela interface <code>Graph</code>, e o estado (ficheiros, declarações aceites e rejeitadas, contagens)")
    body += d.render()
    body += ("<p>A base de dados da aplicação web é o grafo das declarações do âmbito ativo. Os ficheiros são a fonte de verdade; a base de dados "
             "existe para as consultas. A cada pedido, a aplicação compara a impressão digital dos ficheiros do âmbito (caminhos e datas de modificação) "
             "com a da última construção; se mudou, ingere de novo. Uma alteração feita pelos passos ou pelas alterações aparece, por isso, no pedido seguinte.</p>"
             "<ul><li><b>memória</b>: o grafo vive no processo do servidor; não precisa de nada instalado.</li>"
             "<li><b>neo4j</b> (<code>python -m ecv servidor --neo4j</code>): a cada construção, os nós ECV são apagados e o grafo é carregado em lotes; "
             "as vistas e a validação leem o Neo4j (<code>Neo4jGraph</code>) e as consultas Cypher equivalentes podem correr-se no Neo4j Browser.</li></ul>"
             "<p>O âmbito escolhe-se no topo de cada página da aplicação. A pré-visualização da fusão (separador Base de dados) compara uma declaração colada "
             "com o grafo do âmbito sem escrever nada: uma declaração só passa a fazer parte da base de dados quando é um ficheiro do âmbito.</p>")
    body += "<h2>Interface (<code>ecv/4_graph/database.py</code>)</h2>" + pre(docstring(ROOT / "ecv/4_graph/database.py"))
    return page("base_dados", "Base de dados da aplicação", body, section=GRAPH_SECTION, menu="Base de dados da aplicação", crumbs=CRUMBS,
                summary="O que suporta a aplicação web: as declarações ingeridas num grafo, em memória ou no Neo4j, reconstruído quando os ficheiros mudam.")


def node_and_edge_pages():
    model = load_model()
    colors = _node_colors(model)
    edges = _edges(model)
    views = view_schemas.catalogue()
    out = []
    for name, spec in model["nos"].items():
        going = [(t, a) for t, a in model["arestas"].items() if name in a["de"]]
        coming = [(t, a) for t, a in model["arestas"].items() if name in a["para"]]
        nodes = sorted({x for a, b, _ in edges if name in (a, b) for x in (a, b)} | {name})
        body = layered_diagram(nodes, [(a, b, t) for a, b, t in edges if name in (a, b)], href=lambda x: f"no_{x}.html",
                               color=lambda x: colors[x], width=170, height=32, gx=150, gy=12)
        body += table(["Campo", "Valor"], [["Grupo", e(spec.get("grupo"))], ["Chave", f"<code>{e(spec['chave'])}</code>"],
                                           ["Rótulos extra", e(", ".join(spec.get("rotulosExtra", [])) or "—")], ["Descrição", e(spec["descricao"])]])
        body += "<h2>Atributos</h2>" + table(["Atributo", "Valor"], [[f"<code>{e(k)}</code>", e(v)] for k, v in spec["atributos"].items()])
        body += "<h2>Arestas que saem</h2>" + table(["Aresta", "Para", "Atributos"], [[f'<a href="aresta_{t}.html">{t}</a>', e(", ".join(a["para"])),
                                                                                       e(", ".join(a["atributos"]))] for t, a in going])
        body += "<h2>Arestas que chegam</h2>" + table(["Aresta", "De", "Atributos"], [[f'<a href="aresta_{t}.html">{t}</a>', e(", ".join(a["de"])),
                                                                                       e(", ".join(a["atributos"]))] for t, a in coming])
        using = [k for k, v in views.items() if name in v["entidades"] or any(name in (x[0], x[2]) for x in v["ligacoes"])]
        body += "<h2>Vistas que usam este nó</h2><p>" + (", ".join(f'<a href="vista_{k}.html">{e(views[k]["titulo"])}</a>' for k in using) or "—") + "</p>"
        body += "<h2>Consulta de exemplo</h2>" + pre(f"MATCH (n:{name}) RETURN n LIMIT 25;")
        out.append(page(f"no_{name}", f"Nó {name}", body, section=GRAPH_SECTION, menu=f"nó {name}", sub=True, crumbs=CRUMBS + [("grafo.html", "Grafo")]))
    for kind, spec in model["arestas"].items():
        body = table(["Campo", "Valor"], [["De", ", ".join(f'<a href="no_{x}.html">{x}</a>' for x in spec["de"])],
                                          ["Para", ", ".join(f'<a href="no_{x}.html">{x}</a>' for x in spec["para"])], ["Dono (fusão)", e(spec.get("dono"))],
                                          ["Cardinalidade", e(spec.get("cardinalidade", "—"))], ["Descrição", e(spec["descricao"])]])
        if spec["atributos"]:
            body += "<h2>Atributos</h2>" + table(["Atributo", "Valor"], [[f"<code>{e(k)}</code>", e(v)] for k, v in spec["atributos"].items()])
        using = [k for k, v in views.items() if any(x[1] == kind for x in v["ligacoes"])]
        body += "<h2>Vistas que percorrem esta aresta</h2><p>" + (", ".join(f'<a href="vista_{k}.html">{e(views[k]["titulo"])}</a>' for k in using) or "—") + "</p>"
        body += "<h2>Consulta de exemplo</h2>" + pre(f"MATCH (a)-[r:{kind}]->(b) RETURN a, r, b LIMIT 25;")
        out.append(page(f"aresta_{kind}", f"Aresta {kind}", body, section=GRAPH_SECTION, menu=f"aresta {kind}", sub=True,
                        crumbs=CRUMBS + [("grafo.html", "Grafo")]))
    return out


# ---------------------------------------------------------------------- views
CONTROLS = {
    "modelo_hlm": ["Propriedades na árvore: mostra ou esconde as propriedades dentro das caixas.",
                   "Expandir tudo / Recolher tudo: abre ou fecha todos os blocos da tabela; ▾/▸ em cada bloco.",
                   "Clicar num SM ou USM: abre a vista do modelo específico; ◆ numa propriedade: abre as dependências."],
    "modelo_regras": ["Agrupar por: modelo, alvo (propriedade restringida) ou natureza.",
                      "Atributos das regras: escolhe os campos mostrados (identificador, onde vive, descrição, condição, restrição, mensagem, conclusão, funções).",
                      "Grupos de RIR: número de regras e ligação à vista de decisão do alvo; até rirInlineMaximo regras aparecem por extenso."],
    "modelo_especifico": ["Usado por: caminhos desde cada HLM.", "Árvore até às folhas; os mesmos controlos da vista com regras."],
    "decisao": ["Tabela ou Árvore: os mesmos dados em matriz ou em árvore.",
                "Cada célula é o valor exigido pela RIR dessa combinação de valores dos fatores discriminantes.",
                "Cores: sem regra (cinzento), gama sem valor comum com a geral (vermelho), conflito (amarelo), linha fora dos plausíveis (vermelho)."],
    "dependencias": ["Seletor de valor: mostra só o fluxo de um valor.",
                     "Resumo: matriz valor × propriedade afetada, com o número de regras que passam a aplicar-se."],
    "regra": ["Subgrafo em duas partes: a regra (horizontal) e os modelos (vertical, até aos HLM)."],
    "validacao": ["Resultado: válida quando não há problemas estruturais nem regras não conformes.",
                  "Estados por regra e ocorrência: não conforme, conforme, conclusão, não aplicável, sem valor, não avaliável, fora da projeção, ausente.",
                  "Contextos externos: a origem de cada valor; instância avaliada: o JSON depois dos valores fixados pelo perfil."],
}
EXAMPLES = {"modelo_hlm": "hlm_Dispositivo", "modelo_regras": "regras_Dispositivo", "modelo_especifico": "usm_Morada", "projecoes": "projecoes_Dispositivo",
            "decisao": "decisao_Medicao_valor", "dependencias": "dependencias_Identificacao_tipoDispositivo", "impacto": "impacto_Identificacao_tipoDispositivo",
            "regra": "regra_RIR-TEMP-REFRIG-CELSIUS", "perfil": "perfil_RefrigeracaoLote", "candidatos_perfil": "candidatos_perfil",
            "validacao": "validacao_fatura_at_com_erros", "coerencia": "coerencia", "lacunas": "lacunas_Dispositivo", "operadores": "operadores", "indice": "index"}
STATIC = REPO + "documentacao/vistas/"


def views_index_page():
    views = view_schemas.catalogue()
    groups = {0: ["indice"], 1: ["modelo_hlm", "modelo_regras", "modelo_especifico", "projecoes", "lacunas"],
              2: ["decisao", "dependencias", "impacto", "regra"], 3: ["perfil", "validacao", "candidatos_perfil", "coerencia", "operadores"]}
    d = Diagram(1180, 520)
    for c, kinds in groups.items():
        for i, k in enumerate(kinds):
            d.box(k, 15 + c * 295, 30 + (460 / len(kinds)) * i + (460 / len(kinds) - 56) / 2, 240, 56, views[k]["titulo"], [views[k]["ficheiro"]],
                  f"vista_{k}.html", "#5a1a2f" if k == "indice" else "#555")
    for k, v in views.items():
        for n in v["navegacao"]:
            if n["para"] in views and k != "indice" and n["para"] != k:
                d.arrow(k, n["para"], None, color="#999")
    body = d.render() + '<p class="note">Cada caixa abre a página do tipo de vista; as setas são as navegações entre vistas.</p>'
    body += without_h1(markdown("ecv/5_views/README.md"))
    body += (f'<h2>Vistas estáticas</h2><p>As vistas das declarações de exemplo estão geradas em <code>documentacao/vistas/</code> '
             f'(<a href="{STATIC}index.html">abrir</a>), para consulta sem a aplicação. Na aplicação web, cada vista é construída a pedido, para o âmbito ativo.</p>')
    body += "<h2>Navegações</h2>" + table(["De", "Para", "Por"], [
        [f'<a href="vista_{a}.html">{e(views[a]["titulo"])}</a>', f'<a href="vista_{n["para"]}.html">{e(views[n["para"]]["titulo"])}</a>', e(n["por"])]
        for a in views for n in views[a]["navegacao"] if n["para"] in views])
    return page("vistas", "Vistas", body, section=VIEWS_SECTION, menu="Vistas: índice e navegação", mermaid=True, crumbs=CRUMBS,
                summary="Que vistas existem, o que cada uma mostra e como se navega entre elas.")


def view_kind_pages():
    views = view_schemas.catalogue()
    vm_readme = read("ecv/5_views/viewmodels/README.md")
    out = []
    for kind, v in views.items():
        example = EXAMPLES.get(kind, "index")
        body = f"<p>{e(v['representa'])}</p>"
        body += table(["Campo", "Valor"], [["Página", f"<code>{e(v['ficheiro'])}</code>"], ["ViewModel", f"<code>{e(v['viewmodel'])}</code>"],
                                           ["Para que serve", e(v["serve"])],
                                           ["Exemplo", f'<a href="{STATIC}{example}.html">{e(example)}.html</a> (estática) · na aplicação: <code>/vistas/{e(example)}.html</code>']])
        body += "<h2>Dados que agrega</h2><ul>" + "".join(f"<li>{e(x)}</li>" for x in v["dados"]) + "</ul>"
        body += "<h2>Como usar</h2><ul>" + "".join(f"<li>{e(x)}</li>" for x in v["uso"] + CONTROLS.get(kind, [])) + "</ul>"
        if v["entidades"]:
            body += "<h2>Entidades do grafo e arestas que percorre</h2>" + view_schemas.entities_diagram(v["entidades"], v["ligacoes"])
        body += "<h2>Navegação</h2>" + view_schemas.navigation_diagram(kind)
        vm = (v["viewmodel"] or "").split(" ")[0]
        if vm in REGISTRY:
            r = REGISTRY[vm]
            body += (f'<h2>ViewModel <code>{e(vm)}</code></h2><p><b>Pergunta:</b> {e(r["pergunta"])}<br><b>Parâmetros:</b> <code>{e(", ".join(r["parametros"]))}</code>'
                     f'<br><b>Percurso no grafo:</b> <code>{e(TRAVERSALS.get(vm, ""))}</code></p>')
            section = re.search(r"(?ms)^### `" + re.escape(vm) + r"`.*?(?=^### |^## )", vm_readme)
            if section:
                body += convert(section.group(0), link_from("ecv/5_views/viewmodels/README.md"))[0]
            cypher = ROOT / "ecv/5_views/viewmodels/cypher" / r["cypher"]
            if cypher.exists():
                body += f"<h3>Consulta Cypher equivalente ({e(r['cypher'])})</h3>" + pre(cypher.read_text(encoding="utf-8"))
        out.append(page(f"vista_{kind}", v["titulo"], body, section=VIEWS_SECTION, menu=v["titulo"], sub=True, crumbs=CRUMBS + [("vistas.html", "Vistas")]))
    return out


def viewmodels_page():
    return page("viewmodels", "ViewModels", without_h1(markdown("ecv/5_views/viewmodels/README.md")), section=VIEWS_SECTION, menu="ViewModels",
                mermaid=True, crumbs=CRUMBS + [("vistas.html", "Vistas")])


def colors_page():
    body = table(["Elemento", "Cor"], [[e(k), f'<span style="display:inline-block;width:40px;height:12px;background:{e(v)}"></span> <code>{e(v)}</code>']
                                       for k, v in COLORS.items()])
    return page("apresentacao", "Cores", body, section=VIEWS_SECTION, menu="Cores", crumbs=CRUMBS + [("vistas.html", "Vistas")])


def pages():
    return ([ingestion_page(), merge_page(), graph_page(), database_page()] + node_and_edge_pages()
            + [views_index_page()] + view_kind_pages() + [viewmodels_page(), colors_page()])
