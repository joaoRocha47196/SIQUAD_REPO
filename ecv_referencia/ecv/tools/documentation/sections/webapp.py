"""Aplicação web: the tabs (what each does and which module it calls), the routes, the log, how it reaches the LLM."""
from ecv.webapp.pages.layout import TABS
from ecv.webapp.routes import ROUTES

from ..page import Diagram, e, io_block, table
from .common import page

CRUMBS = [("index.html", "Visão geral")]
SECTION = "Aplicação web"

TAB_DETAILS = {
    "inicio": ("—", "O âmbito ativo e a base de dados; os domínios com o estado da geração e de cada camada; os pedidos por registar."),
    "inventario": ("0 · transformer", "Cada inventário extraído: grupos, elementos e regras, com filtro por categoria e por texto."),
    "declaracao": ("0 · transformer, 1 · ecv_builder", "Dois passos. 1. Extração: as fontes do domínio, anexar documentos, o adaptador de cada fonte, "
                                      "pedir ao LLM um adaptador em falta, extrair e aceitar. 2. Geração: Preparar pedido cria o pedido único ao LLM, registável "
                                      "as vezes que for preciso. O estado das camadas A a F (revistas em Alterações); as declarações, com as vistas de cada uma, e o mapeamento."),
    "alteracoes": ("2 · amendments", "A revisão por camadas A a F: em cada camada, as operações, o formulário guiado (modelo, propriedade, regra…) com o contexto "
                                     "da decisão e a operação já preenchida, o pedido em linguagem natural só com esse contexto, o que existe na camada, "
                                     "Verificar e Aceitar; a tabela CSV de mapeamentos (uma RIR por linha) e o vocabulário. As vistas têm ✎ para abrir aqui a alteração."),
    "vistas": ("5 · views", "O catálogo das vistas do grafo ativo; cada vista é construída a pedido a partir do seu ViewModel. "
                            "O ViewModel de cada vista está também em JSON (/api/vm/<página>)."),
    "validacao": ("6 · validation", "Uma instância (JSON) avaliada num cenário (perfil ou HLM), com os contextos externos; as instâncias de exemplo."),
    "instancias": ("6 · validation", "Instâncias de teste: o esqueleto a partir da estrutura do HLM e do perfil (projeção, valores fixados); um pedido ao LLM só "
                                     "com esse contexto; gravar em dominios/<d>/instancias/ e validar."),
    "pedidos": ("shared · llm_requests", "As filas de pedidos ao LLM (geração, alterações, instâncias, funções, adaptadores); em cada pedido, o prompt (para copiar), "
                                         "a resposta (para colar) e Registar."),
    "funcoes": ("6 · validation", "As funções declaradas no grafo ativo, com o estado da implementação; Pedir implementação cria um pedido na fila global."),
    "base": ("3 · ingestion, 4 · graph", "O backend, o âmbito, as declarações ingeridas (aceites e rejeitadas), as contagens de nós e arestas; "
                                         "reconstruir; pré-visualizar a fusão de uma declaração; pesquisa e modelos semelhantes."),
    "registo": ("—", "Os pedidos HTTP (método, caminho, estado, tempo, tamanho) e as ações (pedido criado, operações aplicadas, base reconstruída), "
                     "também na consola e em registos/servidor.log."),
}


def _architecture():
    d = Diagram(1180, 300)
    d.box("browser", 20, 120, 150, 60, "Navegador", ["páginas e formulários"], None, "#555")
    d.box("server", 220, 110, 200, 80, "server.py", ["Router (routes.py)", "registo de cada pedido"], None, "#0072B2")
    d.box("handlers", 470, 110, 190, 80, "handlers/", ["um módulo por separador"], None, "#0072B2")
    d.box("ctx", 470, 230, 190, 56, "AppContext", ["âmbito, base de dados, catálogo"], None, "#444")
    d.box("mods", 720, 20, 200, 80, "Módulos 0, 1, 2, 6", ["extrair, gerar, alterar,", "validar, funções"], None, "#5a1a2f")
    d.box("db", 720, 130, 200, 60, "GraphDatabase", ["memória ou Neo4j"], "base_dados.html", "#8B1E3F")
    d.box("views", 720, 220, 200, 60, "Módulo 5", ["catálogo, ViewModel, HTML"], "vistas.html", "#5a1a2f")
    d.box("files", 980, 20, 180, 80, "Ficheiros", ["dominios/<d>/…", "pedidos/"], None, "#0E7C7B")
    d.box("llm", 980, 130, 180, 60, "LLM", ["responde aos pedidos"], "pedidos.html", "#6A3D9A")
    for a, b in [("browser", "server"), ("server", "handlers"), ("handlers", "mods"), ("handlers", "ctx"), ("ctx", "db"), ("ctx", "views"),
                 ("mods", "files"), ("files", "db")]:
        d.arrow(a, b)
    d.arrow("files", "llm", "prompt.md", dashed=True)
    d.arrow("llm", "files", None, dashed=True)
    return d.render()


def app_page():
    body = io_block("pedidos HTTP do navegador (páginas e formulários) ou de scripts (<code>/api/…</code>)",
                    "a área de trabalho (<code>dominios/</code>), a base de dados do âmbito ativo e as filas de pedidos ao LLM",
                    "páginas e JSON; as ações alteram os ficheiros dos domínios sempre através dos módulos 0, 1, 2 e 6")
    body += _architecture()
    body += ("<p><code>python -m ecv servidor</code> arranca a aplicação em <code>http://127.0.0.1:8000</code> (o endereço e a porta estão na configuração, "
             "secção <code>servidor</code>); com <code>--neo4j</code>, a base de dados é o Neo4j; com <code>--ambito &lt;dominio&gt;</code>, começa nesse domínio.</p>")
    rows = []
    for tab in TABS:
        if tab is None:
            continue
        ident, label, href = tab
        module, text = TAB_DETAILS.get(ident, ("—", ""))
        rows.append([f'<span id="{e(ident)}"></span><b>{e(label)}</b>', f"<code>{e(href)}</code>", e(module), e(text)])
    body += "<h2>Separadores</h2>" + table(["Separador", "Endereço", "Módulo", "O que permite"], rows)
    body += ("<h2>O trabalho de um domínio, separador a separador</h2><ol>"
             "<li><b>Início</b>: criar o domínio (ou escolhê-lo no seletor de âmbito).</li>"
             "<li><b>Declaração › 1. Extração</b>: anexar os documentos, escolher os adaptadores (ou pedir um), extrair; rever em <b>Inventário</b> e aceitar.</li>"
             "<li><b>Declaração › 2. Geração</b>: Preparar pedido. O pedido abre em <b>Pedidos ao LLM</b>: a resposta é escrita no repositório ou colada; "
             "Registar cria as declarações. As vistas de cada declaração ficam logo disponíveis.</li>"
             "<li><b>Alterações</b>: camada a camada (A a F), corrigir ou completar por formulário guiado, por pedido em linguagem natural "
             "(só com o contexto escolhido), por operações ou por tabela CSV; Verificar e Aceitar a camada. Nas <b>Vistas</b>, ✎ abre a alteração certa.</li>"
             "<li><b>Funções</b>: pedir a implementação das funções declaradas.</li>"
             "<li><b>Instâncias</b>: criar instâncias de teste a partir da estrutura e do perfil; <b>Validação</b>: avaliar instâncias.</li></ol>"
             "<p>Cada página termina com a caixa \"Onde está, no código e nos ficheiros\": o módulo que faz a operação e os ficheiros que lê e escreve.</p>")
    return page("aplicacao", "Aplicação web", body, section=SECTION, menu="Separadores e arquitetura", crumbs=CRUMBS,
                summary="A aplicação que dá acesso a todas as operações dos módulos 0 a 6, sem linha de comandos.")


def routes_page():
    body = ("<p>As rotas estão numa só tabela, <code>ecv/7_webapp/routes.py</code>: método, caminho, função e descrição. "
            "A aplicação mostra a mesma tabela em <code>/rotas</code>. Um caminho com <code>&lt;nome&gt;</code> recebe esse segmento como parâmetro.</p>")
    body += table(["Método", "Caminho", "Função", "O que faz"],
                  [[e(r.method), f"<code>{e(r.path)}</code>", f"<code>{e(r.handler.__module__.split('.')[-1])}.{e(r.handler.__name__)}</code>",
                    e(r.description)] for r in ROUTES])
    body += ("<h2>Registo</h2><p>Cada pedido escreve uma linha (hora, método, caminho, estado, milissegundos, bytes e o que foi feito) na consola, "
             "em <code>registos/servidor.log</code> e numa memória de <code>linhasRegistoEmMemoria</code> linhas mostrada no separador Registo. "
             "As ações (pedido criado, resposta guardada ou aplicada, operações aplicadas, base de dados reconstruída) e os erros, com o traceback, "
             "também ficam registados.</p>"
             "<h2>Erros</h2><p>Um erro que o utilizador pode corrigir (uma camada ainda não permitida, uma operação inválida, uma resposta que não é JSON) "
             "dá uma página com a mensagem e o estado 400, ou <code>{\"erro\": …}</code> na API. Um caminho que não existe dá 404.</p>")
    return page("rotas", "Rotas", body, section=SECTION, menu="Rotas e registo", crumbs=CRUMBS + [("aplicacao.html", "Aplicação web")])


def functions_page():
    body = ("<p>Uma função tem duas partes, em módulos diferentes:</p>"
            + table(["Parte", "Onde", "Como se cria"], [
                ["Declaração: nome, parâmetros, contextos externos, significado (\"Verdadeira quando…\")", "nas declarações (módulo 2)",
                 "operação <code>definir_funcao</code> (separador Alterações) ou a resposta da geração"],
                ["Implementação: como o motor a avalia", "<code>ecv/6_validation/functions/</code>",
                 "Funções › Pedir implementação: um pedido na fila global, respondido com um módulo Python"]])
            + "<p>Uma regra que chama uma função sem implementação fica <i>não avaliável</i> na validação. O prompt do pedido de implementação inclui a "
              "declaração da função, as regras que a chamam, o contrato e um módulo existente como exemplo:</p><ul>"
              "<li>o módulo regista a função com <code>@implements(\"&lt;nome&gt;\")</code>;</li>"
              "<li>recebe os argumentos pela ordem dos parâmetros e os contextos externos em <code>contexts</code>;</li>"
              "<li>devolve verdadeiro ou falso, e levanta <code>Unavailable</code> quando falta um valor ou um contexto;</li>"
              "<li>só usa a biblioteca padrão.</li></ul>"
              "<p>Ao registar, o código confirma que o módulo compila e regista o nome, grava-o em <code>functions/f_&lt;nome&gt;.py</code> e recarrega as "
              "implementações. Uma implementação pedida substitui a anterior com o mesmo nome.</p>")
    return page("funcoes", "Funções: declaração e implementação", body, section=SECTION, menu="Funções", crumbs=CRUMBS + [("aplicacao.html", "Aplicação web")])


def pages():
    return [app_page(), routes_page(), functions_page()]
