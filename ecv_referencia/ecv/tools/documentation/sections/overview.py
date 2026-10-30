"""Visão geral: the system and its modules, where the data is, installation, commands, configuration, glossary."""
import json
import re

from ecv import cli, config

from ..page import Diagram, e, table
from .common import markdown, page, text, without_h1

COLORS = config.COLORS
CRUMBS = [("index.html", "Visão geral")]


def modules_diagram():
    d = Diagram(1240, 470)
    d.box("src", 20, 40, 160, 66, "Fontes de dados", ["data/: CIUS-PT, FM,", "Smart Data Models"], "dados.html", "#555")
    d.box("m0", 220, 40, 170, 66, "0 · transformer", ["adaptadores por formato"], "modulo_transformer.html")
    d.box("inv", 430, 40, 150, 66, "Inventário", ["grupos, elementos, regras"], "extracao.html", COLORS["SM"])
    d.box("m1", 620, 30, 200, 86, "1 · ecv_builder", ["geração (G): um pedido com tudo", "revisão por camadas A a F"], "transformacao.html")
    d.box("llm", 620, 160, 200, 56, "Pedidos ao LLM", ["prompt.md → resposta"], "pedidos.html", COLORS["funcao"])
    d.box("m2", 860, 160, 170, 56, "2 · amendments", ["operações, CSV"], "alteracoes.html")
    d.box("decl", 1060, 40, 160, 66, "Declarações ECV", ["dominios/<d>/declaracoes", "specs/exemplos"], "declaracao.html", COLORS["SM"])
    d.box("m3", 1060, 250, 160, 66, "3 · ingestion", ["verificar, materializar,", "fundir"], "ingestao.html")
    d.box("m4", 820, 250, 200, 66, "4 · graph", ["grafo integrado", "memória ou Neo4j"], "grafo.html", COLORS["HLM"])
    d.box("m5", 560, 250, 200, 66, "5 · views", ["ViewModels → HTML"], "vistas.html")
    d.box("m6", 560, 350, 200, 56, "6 · validation", ["instância × regras × perfil"], "modulo_validation.html", COLORS["RP"])
    d.box("m7", 220, 300, 250, 86, "7 · webapp", ["separadores para todas as operações", "rotas, registo do servidor", "vistas construídas a pedido"],
          "aplicacao.html", "#0072B2")
    d.box("cfg", 20, 200, 160, 50, "config", ["ecv.config.json"], "configuracao.html", "#444")
    d.box("spec", 220, 160, 170, 56, "Especificação", ["specs/ → texto interno"], "especificacao_interna.html", "#444")
    for a, b, label in [("src", "m0", None), ("m0", "inv", None), ("inv", "m1", None), ("m1", "llm", "pedido"), ("llm", "m2", "operações"),
                        ("m1", "decl", "geração"), ("m2", "decl", "revisão: alterações"), ("decl", "m3", None), ("m3", "m4", None),
                        ("m4", "m5", None), ("m4", "m6", None), ("m5", "m7", None), ("m6", "m7", None)]:
        d.arrow(a, b, label)
    d.arrow("spec", "m1", None, dashed=True)
    d.arrow("m7", "m1", None, dashed=True)
    d.arrow("m7", "m2", None, dashed=True)
    return d.render() + ('<p class="note">Cada caixa abre a página do componente. Setas a cheio: o caminho dos dados. '
                         'Tracejado: a especificação entra em cada prompt; a aplicação web aciona os módulos 1 e 2.</p>')


def data_diagram():
    d = Diagram(1180, 200)
    d.box("files", 20, 60, 230, 80, "Ficheiros (fonte de verdade)", ["declarações, mapeamento,", "inventários, pedidos", "versionados no repositório"],
          None, COLORS["SM"])
    d.box("ing", 300, 70, 170, 60, "Ingestão", ["verifica e funde"], "ingestao.html")
    d.box("mem", 520, 20, 200, 60, "Grafo em memória", ["MemoryGraph"], "grafo.html")
    d.box("neo", 520, 120, 200, 60, "Neo4j", ["o mesmo grafo, em Cypher"], "base_dados.html", "#555")
    d.box("q", 780, 70, 180, 60, "Interface Graph", ["nodes, node, outgoing, incoming"], "modulo_graph.html", COLORS["HLM"])
    d.box("use", 1000, 70, 160, 60, "Consultas", ["vistas, validação, pesquisa"], "vistas.html")
    d.box("chg", 300, 160, 170, 36, "Módulos 1 e 2", [], "transformacao.html")
    for a, b in [("files", "ing"), ("ing", "mem"), ("ing", "neo"), ("mem", "q"), ("neo", "q"), ("q", "use")]:
        d.arrow(a, b)
    d.arrow("chg", "files", "alteram", dashed=True)
    return d.render()


def commands_table():
    """The commands, from the parser of ecv/cli.py (usage and help of each sub-command)."""
    import argparse
    parser = cli.build_parser()
    action = next(a for a in parser._actions if isinstance(a, argparse._SubParsersAction))
    helps = {c.dest: c.help for c in action._choices_actions}
    rows = []
    for name, sub in action.choices.items():
        usage = re.sub(r"\s+", " ", sub.format_usage().replace("usage: ", "").replace(" [-h]", "")).strip()
        rows.append([f"<code>{e(usage)}</code>", e(helps.get(name, ""))])
    return table(["Comando", "O que faz"], rows)


def index():
    body, _ = text("visao_geral", {"principal": modules_diagram(), "dados": data_diagram()})
    body += "<h2>Linha de comandos</h2><p>A aplicação web faz todas as operações; a linha de comandos faz as mesmas, para scripts e testes.</p>"
    body += commands_table()
    return [page("index", "Documentação técnica da ECV de referência", body, section="Visão geral", menu="O sistema",
                 summary="O que o sistema faz, como está dividido em módulos, onde estão os dados e como se instala.")]


# ---------------------------------------------------------------------- configuration
def _value_html(v):
    if isinstance(v, dict):
        if v and all(isinstance(x, dict) for x in v.values()):
            keys = []
            for x in v.values():
                keys += [k for k in x if k not in keys]
            return table(["Chave"] + [e(k) for k in keys],
                         [[f"<code>{e(k)}</code>"] + [e(json.dumps(x.get(c), ensure_ascii=False) if isinstance(x.get(c), (list, dict)) else x.get(c, ""))
                                                      for c in keys] for k, x in v.items()])
        return table(["Chave", "Valor"], [[f"<code>{e(k)}</code>", e(json.dumps(x, ensure_ascii=False) if isinstance(x, (list, dict)) else x)]
                                          for k, x in v.items()])
    if isinstance(v, list):
        return "<ul>" + "".join(f"<li>{e(json.dumps(x, ensure_ascii=False) if isinstance(x, (dict, list)) else x)}</li>" for x in v) + "</ul>"
    return f"<p><code>{e(v)}</code></p>"


def configuration():
    body = ("<p>Todas as constantes estão em <code>ecv/config/ecv.config.json</code>: o vocabulário fechado (tipos base, formas de valor, "
            "operadores, tipos de regra, cardinalidades), as convenções de nomes, as cores, os caminhos, o Neo4j, os parâmetros da ingestão, "
            "das vistas e do servidor. O pacote <code>ecv.config</code> lê o ficheiro uma vez e expõe cada secção como constante "
            "(<code>config.OPERATORS</code>, <code>config.COLORS</code>) e os caminhos por <code>config.path(nome)</code>. "
            "Nenhum módulo tem estes valores no código. Um teste confirma que os enumerados do JSON Schema da declaração coincidem com a configuração.</p>"
            "<p>Cada caminho pode ser substituído pela variável <code>ECV_CAMINHO_&lt;NOME&gt;</code> (por exemplo, <code>ECV_CAMINHO_DOMINIOS</code>), "
            "o que permite correr um ensaio ou os testes noutra pasta de domínios.</p>")
    for key, value in config.CONFIG.items():
        if key in ("descricao", "versao"):
            continue
        body += f'<h2 id="{e(key)}"><code>{e(key)}</code></h2>' + _value_html(value)
    return [page("configuracao", "Configuração", body, section="Visão geral", crumbs=CRUMBS,
                 summary="Um único ficheiro com todas as constantes, lido por todos os módulos.")]


GLOSSARY = [
    ("ECV", "Estratificação do Conhecimento de Validação: a ECM (estrutura) e a ECR (regras), mais as projeções e os perfis.", "specs.html"),
    ("ECM", "Estratificação Composicional de Modelos: HLM, SM, USM, propriedades e composições.", "entidade_HLM.html"),
    ("ECR", "Estratificação Contextual de Regras: as regras pela natureza, alcance e expressividade.", "entidade_Regra.html"),
    ("HLM", "Modelo de alto nível: a entidade que o domínio instancia; só compõe SM.", "entidade_HLM.html"),
    ("SM", "Submodelo: agrupa USM com uma finalidade; pode ter propriedades residuais; pode ser uma coleção.", "entidade_SM.html"),
    ("USM", "Submodelo universal: informação canónica, reutilizável, dona das suas propriedades.", "entidade_USM.html"),
    ("Composição", "Ligação de um modelo ao que compõe, com papel e cardinalidade.", "entidade_Composicao.html"),
    ("RE", "Regra estrutural: obrigatório, permitido ou excluído numa utilização; exprime-se pela projeção.", "entidade_RE_Projecao.html"),
    ("RP", "Regra de plausibilidade: os valores que a propriedade pode tomar, sempre.", "entidade_RP.html"),
    ("RIR", "Regra de inferência restritiva: condição + restrição.", "entidade_RIR.html"),
    ("RIC", "Regra de inferência conclusiva: condição + conclusão (ação ou estado).", "entidade_RIC.html"),
    ("Fator discriminante", "Propriedade lida numa condição, cujo valor decide que regras se aplicam.", "vista_dependencias.html"),
    ("Função", "Verificação delegada, declarada uma vez e chamada de forma estruturada; avaliada por uma implementação do módulo 6.", "funcoes.html"),
    ("Contexto externo", "Valor de fora do modelo e da regra (a data de hoje, um hash anterior).", "entidade_ContextoExterno.html"),
    ("Projeção", "As propriedades obrigatórias e permitidas de um HLM numa utilização.", "entidade_RE_Projecao.html"),
    ("Perfil", "Cenário de execução: uma projeção e valores fixados antes da execução.", "entidade_Perfil.html"),
    ("Declaração ECV", "O ficheiro JSON de um HLM, completo.", "declaracao.html"),
    ("Domínio", "Uma pasta em dominios/ com as fontes, os inventários, as declarações, o mapeamento e os pedidos de uma transformação.", "dominios.html"),
    ("Inventário", "O formato intermédio de uma fonte (fase 0): grupos, elementos e regras, com a origem.", "extracao.html"),
    ("Mapeamento", "Para cada elemento e regra das fontes, o destino na declaração ou o motivo do descarte.", "transformacao.html"),
    ("Especificação interna", "O texto único, gerado a partir das specs, que entra em todos os prompts.", "especificacao_interna.html"),
    ("Pedido ao LLM", "Uma pasta com o prompt completo de uma tarefa e, quando chega, a resposta.", "pedidos.html"),
    ("Operação", "Uma entrada do vocabulário fechado de alterações, aplicada de forma determinística.", "alteracoes.html"),
    ("Fusão", "Juntar ao grafo o grafo de uma declaração, reutilizando o igual e rejeitando conflitos.", "fusao.html"),
    ("Âmbito", "O conjunto de declarações carregado na base de dados da aplicação: os exemplos ou um domínio.", "base_dados.html"),
    ("Declarações de referência", "Os exemplos e as declarações dos domínios com a geração aceite: o que se reutiliza.", "transformacao.html"),
    ("ViewModel", "Operação sobre o grafo que devolve os dados de uma vista (JSON).", "viewmodels.html"),
]


def glossary():
    body = table(["Termo", "Definição"], [[f'<a href="{h}">{e(t)}</a>', e(d)] for t, d, h in GLOSSARY])
    return [page("glossario", "Glossário", body, section="Visão geral", crumbs=CRUMBS)]


def readme():
    return [page("readme", "README do repositório", without_h1(markdown("README.md")), section="Visão geral", menu="README do repositório",
                 mermaid=True, crumbs=CRUMBS)]


def pages():
    return index() + configuration() + glossary() + readme()
