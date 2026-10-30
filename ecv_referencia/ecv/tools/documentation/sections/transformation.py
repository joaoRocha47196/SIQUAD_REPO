"""Transformação: the generation (prompting scheme, response) and the review by layers; the internal specification; the
requests to the LLM; one page per review layer; the amendments (natural language, operations, CSV) with a worked example; the
extraction and the inventory; the source data; the domains."""
import copy
import shutil
import tempfile
from dataclasses import fields
from pathlib import Path

from ecv import config
from ecv.amendments import DeclarationSet, apply_operations, operations_from_csv, vocabulary
from ecv.ecv_builder import specs_bundle
from ecv.ecv_builder.build_process import STEP_CATEGORIES, cycle, layers, prompt_template, step
from ecv.ingestion import ingest
from ecv.shared.workspace import Workspace
from ecv.transformer import ADAPTERS, CATEGORIES
from ecv.transformer import inventory as inventory_module

from ..page import Diagram, e, io_block, table
from .common import REPO, pre, json_pre, page, read, text

COLORS = config.COLORS
CRUMBS = [("index.html", "Visão geral"), ("transformacao.html", "Transformação")]
SECTION = "Transformação"

LAYER_ITEMS = {
    "A": "os elementos de todas as fontes",
    "B": "as regras de presença e de cardinalidade",
    "C": "as regras de formato, valores e gama, e os valores admitidos dos elementos",
    "D": "as regras condicionais, de exclusão e outras",
    "E": "as regras de cálculo e cruzadas",
    "F": "as utilizações e os cenários do domínio",
}
LAYER_CREATES = {
    "A": "HLM, SM, USM, propriedades e composições",
    "B": "projeções (regras estruturais)",
    "C": "regras de plausibilidade (RP)",
    "D": "regras de inferência (RIR e RIC)",
    "E": "funções, contextos externos e as regras que os chamam",
    "F": "perfis (projeção + valores fixados)",
}


def _layers():
    return layers()


def prompting_diagram():
    d = Diagram(1220, 620)
    d.group(10, 10, 420, 600, "prompt.md: o pedido de geração (fase G)", "#8a6b77")
    parts = [("comum", "Papel e princípios comuns", ["prompts/comum.md, build_process.json"], "#comum", "#444"),
             ("spec", "Especificação da ECV (completa)", ["specs/ecv_specs.md: vocabulário,", "declaração, entidades, verificações"],
              "especificacao_interna.html", COLORS["SM"]),
             ("layers", "Procedimento por camadas A a F", ["princípios e procedimento de cada camada"], "#camadas", "#444"),
             ("exist", "O que já existe", ["modelos e funções de referência"], "#referencia", COLORS["HLM"]),
             ("dom", "Dados do domínio", ["utilizações, cenários, mapeamentos conhecidos"], "dominios.html", "#555"),
             ("decl", "Declarações atuais", ["quando a geração se repete"], "declaracao.html", COLORS["SM"]),
             ("notes", "Notas de revisão", ["notas.md do domínio"], None, "#555"),
             ("inv", "Inventário completo", ["grupos, elementos e regras", "de todas as fontes"], "extracao.html", COLORS["SM"]),
             ("fmt", "Formato da resposta", ["declarações completas,", "mapeamento, notas"], "#geracao", "#444")]
    for i, (k, t, lines, href, color) in enumerate(parts):
        d.box(k, 25, 35 + i * 63, 390, 54, t, lines, href, color)
    d.box("req", 480, 250, 180, 80, "Pedido G", ["dominios/<d>/pedidos/", "<n>-passo-G/prompt.md"], "pedidos.html", "#0072B2", stroke=2.6)
    for k, *_ in parts:
        d.arrow(k, "req", None, color="#bbb")
    d.box("llm", 700, 250, 140, 80, "LLM", ["lê prompt.md"], "pedidos.html", COLORS["funcao"])
    d.box("resp", 880, 110, 170, 80, "resposta.json", ["declarações completas", "+ mapeamento + notas"], "#geracao", COLORS["funcao"])
    d.box("reg", 880, 250, 170, 80, "Registar e verificar", ["cria as declarações;", "todas as verificações"], "#ciclo", "#0072B2")
    d.box("rev", 880, 400, 170, 80, "Revisão por camadas", ["A estrutura … F perfis", "vistas e verificações"], "#camadas", "#8B1E3F")
    d.box("chg", 1080, 400, 130, 80, "Alterações", ["texto, outra fonte,", "operações, CSV"], "alteracoes.html", "#8B1E3F")
    d.box("acc", 880, 530, 170, 60, "Aceitar a camada", ["segue-se a seguinte"], "#ciclo", "#0072B2")
    for a, b in [("req", "llm"), ("llm", "resp"), ("resp", "reg"), ("reg", "rev"), ("rev", "chg"), ("rev", "acc")]:
        d.arrow(a, b)
    d.arrow("chg", "rev", "repetir", dashed=True)
    return d.render()


def _layers_table():
    rows = [[f'<a href="passo_{x["id"]}.html">{e(x["id"])} · {e(x["nome"])}</a>', e(LAYER_CREATES[x["id"]]), e(LAYER_ITEMS[x["id"]]),
             e(", ".join(x.get("alteracoes", [])))] for x in _layers()]
    return table(["Camada", "O que se revê nas declarações", "Itens do inventário cuja cobertura se exige", "Operações mais usadas"], rows)


def _cycle_table():
    c = cycle()
    rows = [[f'<span id="{e(x["id"])}"></span><b>{e(x["nome"])}</b>', e(x.get("fase")), e(x["quem"]), e(x["descricao"]), e(x.get("web")),
             f'<code>{e(x.get("cli"))}</code>'] for x in c["etapas"]]
    return table(["Etapa", "Fase", "Executa", "O que acontece", "Aplicação web", "Linha de comandos"], rows)


def main_page():
    g = step("G")
    body = io_block("os inventários de um domínio (módulo 0) e a sua definição (<code>dominio.json</code>)",
                    "a especificação interna, o processo de construção (fases, camadas, princípios, formato da resposta), as declarações de "
                    "referência e as notas de revisão",
                    "um pedido de geração ao LLM; da resposta, as declarações completas do domínio e o mapeamento; depois, por camada, as verificações e as alterações")
    body += ("<p>O processo de construção tem duas partes. Na <b>geração</b> (fase G), um só pedido ao LLM leva a especificação completa, "
             "todo o inventário do domínio (grupos, elementos e regras de todas as fontes) e o procedimento de cada camada; a resposta são as "
             "declarações completas (estrutura, projeções, regras de plausibilidade e de inferência, funções, contextos externos e perfis) e o "
             "mapeamento de cada item do inventário. Na <b>revisão por camadas</b> (passos A a F), cada camada é revista nas vistas e nas suas "
             "verificações e corrigida ou completada por alterações: pedidos em linguagem natural (que podem levar informação de outra fonte: "
             "uma tabela, um documento), operações escritas ou tabelas CSV. O código faz tudo o que é determinístico: monta o prompt, confirma a "
             "forma da resposta, aplica-a e verifica.</p>")
    body += '<h2 id="geracao">A geração: o esquema de prompting</h2>' + prompting_diagram()
    body += (f"<p><b>Objetivo:</b> {e(g['objetivo'])}</p><p><b>Formato da resposta:</b> {e(g['formatoResposta']['descricao'])}</p>"
             + json_pre(g["formatoResposta"]["exemplo"])
             + f"<p><b>Aplicação:</b> {e(g['aplicacao'])}</p><p><b>Aceitação:</b> {e(g['aceitacao'])}</p>"
             + "<p>Verificações da geração:</p><ul>" + "".join(f"<li>{e(x)}</li>" for x in g["verificacoesDoPasso"]) + "</ul>")
    body += ('<h2 id="camadas">A revisão por camadas</h2><p>Cada camada só é aceite depois da anterior. Uma alteração numa camada aceite '
             'volta a pô-la em revisão. A cobertura de cada camada (os itens do inventário que lhe pertencem, todos no mapeamento, mapeados '
             'ou descartados com motivo) é exigida para a aceitar.</p>' + _layers_table())
    body += ('<h2 id="referencia">Declarações de referência</h2><p>São as declarações de exemplo (<code>specs/exemplos</code>) e as dos outros '
             'domínios com a geração aceite. A geração recebe os modelos e as funções que nelas existem, para os reutilizar com o mesmo nome e '
             'a mesma definição; o código junta ao modelo reutilizado as regras que ele já tem. A verificação funde o domínio com a referência e '
             'assinala os conflitos.</p>')
    body += '<h2 id="ciclo">O ciclo</h2>' + _cycle_table()
    body += '<h2 id="comum">Prompt comum</h2>' + pre(prompt_template("comum.md"))
    body += '<h2>Prompt da geração</h2><p class="note">Os campos {{…}} são preenchidos por <code>ecv/1_ecv_builder/package.py</code>; {{CAMADAS}} é o procedimento de cada camada, lido de <code>build_process.json</code>.</p>' + pre(prompt_template(g["prompt"]))
    return page("transformacao", "Transformação: das fontes às declarações", body, section=SECTION, menu="Geração e revisão por camadas",
                crumbs=CRUMBS[:1], summary="Como o módulo 1 constrói as declarações: um pedido de geração com tudo, e a revisão de cada camada por alterações.")


def internal_spec_page():
    bundle = specs_bundle.text()
    headings = [line for line in bundle.splitlines() if line.startswith("## ") or line.startswith("### ")]
    body = io_block("as specs do repositório (<code>specs/</code>) e o vocabulário da configuração",
                    "—", f"<code>ecv/1_ecv_builder/specs/ecv_specs.md</code> ({len(bundle)} caracteres, cerca de {len(bundle) // 4} tokens)")
    body += ("<p>As specs foram escritas para pessoas: têm diagramas, tabelas, exemplos tirados das declarações de exemplo, ligações e a forma "
             "como cada entidade aparece no grafo. O LLM precisa das regras do formato, não da apresentação. "
             "<code>specs_bundle.py</code> gera, a partir dos mesmos ficheiros, um texto único:</p><ul>"
             "<li>o vocabulário fechado, lido da configuração (tipos, operadores e formas de valor, operadores por tipo, cardinalidades, tipos de regra, "
             "padrões de nomes, o SM de metainformação);</li>"
             "<li>a estrutura da declaração (uma declaração, um HLM; cada secção e cada campo);</li>"
             "<li>cada entidade da ECM e da ECR: descrição, atributos, forma na declaração, o que pode e não pode, pormenores e verificações;</li>"
             "<li>a nomenclatura, os caminhos, o catálogo e os códigos de verificação.</li></ul>"
             "<p>Ficam de fora os diagramas mermaid, as arestas do grafo, as tabelas geradas a partir dos exemplos, as ligações e as partes que só "
             "explicam a tese ou o repositório; as tabelas passam a listas. As specs individuais continuam a ser a documentação; "
             "o texto interno é derivado delas e um teste confirma que está atualizado (<code>python -m ecv specs</code> volta a gerá-lo).</p>")
    body += "<h2>Secções</h2><ul>" + "".join(f"<li>{e(h.lstrip('# '))}</li>" for h in headings if h.startswith("## ")) + "</ul>"
    body += f'<p><a href="{REPO}ecv/1_ecv_builder/specs/ecv_specs.md">Abrir o ficheiro</a></p>'
    return page("especificacao_interna", "Especificação interna (para o LLM)", body, section=SECTION, menu="Especificação interna", crumbs=CRUMBS,
                summary="Um único ficheiro, gerado a partir das specs, com tudo o que o LLM precisa para escrever uma declaração.")


# ---------------------------------------------------------------------- requests to the LLM
def requests_page():
    d = Diagram(1160, 230)
    d.box("app", 20, 80, 180, 70, "Aplicação ou CLI", ["cria o pedido"], "aplicacao.html", "#0072B2")
    d.box("folder", 250, 70, 220, 90, "Pasta do pedido", ["pedido.json · prompt.md", "resposta.json | resposta.py", "resultado.json"], None, "#444")
    d.box("repo", 520, 20, 220, 70, "No repositório", ["o LLM escreve a resposta", "e faz commit"], None, COLORS["funcao"])
    d.box("paste", 520, 140, 220, 70, "Na aplicação web", ["a resposta é colada", "na página do pedido"], "aplicacao.html#pedidos", COLORS["funcao"])
    d.box("reg", 800, 80, 160, 70, "Registar", ["confirma e aplica"], None, "#0072B2")
    d.box("res", 1000, 80, 140, 70, "Resultado", ["aplicado | rejeitado"], None, "#444")
    for a, b in [("app", "folder"), ("folder", "repo"), ("folder", "paste"), ("repo", "reg"), ("paste", "reg"), ("reg", "res")]:
        d.arrow(a, b)
    body = d.render()
    body += ("<p>A aplicação nunca chama um LLM. Cada tarefa que precisa de um torna-se um pedido: uma pasta com o prompt completo. "
             "O pedido é respondido de uma de duas formas, com o mesmo resultado:</p><ol>"
             "<li><b>No repositório.</b> O LLM (por exemplo, o Claude Code a trabalhar neste repositório) lê <code>prompt.md</code>, escreve "
             "<code>resposta.json</code> na mesma pasta e faz commit. Depois de <code>git pull</code>, a aplicação mostra o pedido como respondido.</li>"
             "<li><b>Na aplicação web.</b> Copia-se o prompt para qualquer LLM e cola-se a resposta na página do pedido.</li></ol>"
             "<p><b>Registar</b> confirma a forma da resposta e aplica-a. Se falhar, nada é gravado, o pedido fica <i>rejeitado</i> com o motivo em "
             "<code>resultado.json</code> e pode ser respondido de novo.</p>")
    body += "<h2>Tipos de pedido</h2>" + table(["Tipo", "Fila", "Criado por", "Resposta", "Aplicada por"], [
        ["<code>passo</code> (G)", "<code>dominios/&lt;d&gt;/pedidos/</code>", "Declaração › G › Preparar pedido", "<code>resposta.json</code>: declarações completas, mapeamento, notas",
         "módulo 1"],
        ["<code>alteracao</code> (A a F)", "<code>dominios/&lt;d&gt;/pedidos/</code>", "Alterações › Linguagem natural (com informação de outra fonte, opcional)", "<code>resposta.json</code>: operações",
         "módulo 2"],
        ["<code>funcao</code>", "<code>pedidos/</code> (global)", "Funções › Pedir implementação", "<code>resposta.py</code>: um módulo Python",
         "módulo 6 (instala em <code>ecv/6_validation/functions/</code>)"],
        ["<code>adaptador</code>", "<code>pedidos/</code> (global)", "Declaração › 1. Extração › pedir um adaptador (formato sem adaptador)",
         "<code>resposta.py</code>: um módulo com <code>NAME</code>, <code>DESCRIPTION</code> e <code>adapt(path)</code>",
         "módulo 0 (instala em <code>ecv/0_transformer/adapters/a_&lt;nome&gt;.py</code> e experimenta-o na amostra)"],
        ["<code>instancia</code>", "<code>dominios/&lt;d&gt;/pedidos/</code>", "Instâncias › Pedir a instância (cenário e o que testar)",
         "<code>resposta.json</code>: <code>{descricao, perfil | hlm, contextos, instancia}</code>",
         "módulo 6 (grava em <code>dominios/&lt;d&gt;/instancias/</code> e valida)"]])
    body += "<h2>Estados</h2>" + table(["Estado", "Significado"], [
        ["pendente", "o pedido foi criado; ainda não há resposta"], ["respondido", "o ficheiro da resposta existe (escrito no repositório ou colado)"],
        ["aplicado", "a resposta foi registada; <code>resultado.json</code> tem o que foi feito e a verificação"],
        ["rejeitado", "a resposta não pôde ser aplicada; <code>resultado.json</code> tem o motivo"]])
    body += "<h2><code>pedido.json</code></h2>" + json_pre({"id": "001-passo-G", "tipo": "passo", "titulo": "Fase G: Geração da declaração completa", "passo": "G",
                                                             "estado": "pendente", "criado": "2026-10-29T10:00:00", "ficheiroResposta": "resposta.json",
                                                             "dominio": "iot", "tamanho": {"caracteres": 186000, "tokensEstimados": 46000}})
    return page("pedidos", "Pedidos ao LLM", body, section=SECTION, menu="Pedidos ao LLM", crumbs=CRUMBS,
                summary="Como a aplicação e o LLM trocam trabalho: pedidos em pastas, respondidos no repositório ou na aplicação web.")


# ---------------------------------------------------------------------- steps
def layer_page(x):
    sid = x["id"]
    body = io_block("as declarações geradas (fase G), a camada " + e(x["nome"]) + " nas vistas e nas verificações",
                    e(LAYER_ITEMS[sid]) + "; as notas da geração; informação de outras fontes, quando a pessoa a dá",
                    "alterações às declarações (operações aplicadas pelo módulo 2) e a aceitação da camada")
    body += f"<p><b>Objetivo da revisão:</b> {e(x['objetivo'])}</p><p><b>A camada:</b> {e(x['camada'])}</p><p><b>Pergunta:</b> {e(x['pergunta'])}</p>"
    body += "<h2>Princípios</h2><ul>" + "".join(f"<li>{e(p)}</li>" for p in x["principios"]) + "</ul>"
    body += ("<h2>Procedimento (no prompt de geração e nos pedidos de alterações desta camada)</h2><ol>"
             + "".join(f"<li>{e(p)}</li>" for p in x["comoProceder"]) + "</ol>")
    if sid in STEP_CATEGORIES:
        body += f"<p>Categorias das regras do inventário desta camada: {e(', '.join(STEP_CATEGORIES[sid]))}.</p>"
    body += "<h2>Verificações</h2><p>" + ", ".join(f"<code>{e(v)}</code>" for v in x["verificacoes"]) + "</p>"
    body += "<ul>" + "".join(f"<li>{e(v)}</li>" for v in x.get("verificacoesDoPasso", [])) + "</ul>"
    body += f"<h2>Aceitação</h2><p>{e(x['aceitacao'])}</p>"
    body += "<h2>Vistas de revisão</h2><ul>" + "".join(f"<li><code>{e(v)}</code></li>" for v in x["vistas"]) + "</ul>"
    body += "<h2>Perguntas de revisão</h2><ol>" + "".join(f"<li>{e(q)}</li>" for q in x["revisao"]) + "</ol>"
    body += ("<h2>Alterações</h2><p>Operações mais usadas: " + ", ".join(f'<a href="alteracoes.html#{e(o)}"><code>{e(o)}</code></a>' for o in x["alteracoes"])
             + '. Um pedido de alterações desta camada leva a orientação acima, a especificação completa e os itens do inventário da camada ainda '
               'sem mapeamento (ver <a href="alteracoes.html">Alterações</a>).</p>')
    return page(f"passo_{sid}", f"Revisão {sid}: {x['nome']}", body, section=SECTION, menu=f"{sid} · {x['nome']}", sub=True, crumbs=CRUMBS,
                summary=e(x["objetivo"]))


def phase0_page():
    s = step("0")
    body = io_block("os ficheiros das fontes do domínio (em <code>data/</code>, listados em <code>dominio.json</code>)", "um adaptador por formato",
                    "um inventário por fonte em <code>dominios/&lt;d&gt;/inventario/</code>")
    body += f"<p>{e(s['objetivo'])}</p><p>Não usa o LLM. Corre em Declaração › 1. Extração, onde se anexam os documentos e se escolhe o adaptador de cada fonte (ou <code>{e(s.get('comando', ''))}</code>) e fica em revisão até ser aceite.</p>"
    body += '<p>O formato do inventário e a forma de escrever um adaptador estão em <a href="extracao.html">Extração e inventário</a>.</p>'
    return page("passo_0", f"Fase 0: {s['nome']}", body, section=SECTION, menu=f"0 · {s['nome']}", sub=True, crumbs=CRUMBS)


# ---------------------------------------------------------------------- amendments
NL_REQUEST = "Num laboratório, a humidade medida por um dispositivo de humidade, em %, tem de estar entre 30 e 60."
NL_OPERATION = {"op": "adicionar_regra", "onde": {"nivel": "HLM", "modelo": "Dispositivo"},
                "regra": {"id": "RIR-HUM-LABORATORIO", "natureza": "inferencia_restritiva",
                          "condicao": [{"propriedade": "Identificacao.tipoDispositivo", "operador": "EQUALS", "valor": "HUMIDADE"},
                                       {"propriedade": "Leitura.Medicao.unidadeMedida", "operador": "EQUALS", "valor": "%"},
                                       {"propriedade": "Leitura.Instalacao.ambiente", "operador": "EQUALS", "valor": "LABORATORIO"}],
                          "restricao": {"propriedade": "Leitura.Medicao.valor", "operador": "RANGE", "valor": [30, 60],
                                        "mensagem": "Humidade fora da gama de laboratório (30 a 60 %)."}}}
CSV_TABLE = "pais;localidade;codigoPostal\nPT;LISBOA;^1[0-9]{3}-[0-9]{3}$\nPT;PORTO;^4[0-9]{3}-[0-9]{3}$\n"


def _with_examples(operations):
    """Apply operations to a copy of the example declarations; return (lines done, ingestion of the copy)."""
    folder = Path(tempfile.mkdtemp())
    try:
        (folder / "declaracoes").mkdir()
        for f in config.example_declarations():
            shutil.copy(f, folder / "declaracoes" / f.name)
        ds = DeclarationSet.load(folder)
        done = apply_operations(ds, copy.deepcopy(operations))
        ds.save()
        return done, ingest(sorted((folder / "declaracoes").glob("*.ecv.json")))
    finally:
        shutil.rmtree(folder)


def _rule_subgraph(ingestion, rule_id):
    """The edges of a rule in the graph, two levels deep (rule -> restriction/condition -> properties)."""
    g = ingestion.graph
    rule = next((g.node(label, rule_id) for label in ("RP", "RIR", "RIC") if g.node(label, rule_id) is not None), None)
    if rule is None:
        raise RuntimeError(f"{rule_id} não chegou ao grafo: " + "; ".join(r.summary() for r in ingestion.results))
    rows = [[f"<code>{e(rule.id)}</code>", "", "", e(rule.get("descricao"))]]
    for edge in g.outgoing(rule):
        rows.append([f"<code>{e(rule.id)}</code>", f"<code>{e(edge.type)}</code>", f"<code>{e(edge.target.id)}</code>", ""])
        if edge.type in ("RESTRITA_POR", "CONDICIONADA_POR"):
            for sub in g.outgoing(edge.target):
                rows.append([f"<code>{e(edge.target.id)}</code>", f"<code>{e(sub.type)}</code>", f"<code>{e(sub.target.id)}</code>",
                             e(sub.props.get("texto", ""))])
    return table(["Nó", "Aresta", "Para", "Texto"], rows)


def amendments_page():
    voc = vocabulary()
    d = Diagram(1180, 260)
    d.box("nl", 20, 20, 210, 60, "Linguagem natural", ["pedido ao LLM (alteracoes.md)"], "#exemplo-linguagem", "#8B1E3F")
    d.box("form", 20, 100, 210, 60, "Operações", ["escritas (JSON), com", "pré-visualização"], "#vocabulario", "#8B1E3F")
    d.box("csv", 20, 180, 210, 60, "Tabela CSV", ["mapeamentos conhecidos", "→ uma RIR por linha"], "#exemplo-csv", "#8B1E3F")
    d.box("step", 270, 20, 180, 60, "Revisão de uma camada", ["A a F"], "transformacao.html#camadas", "#0072B2")
    d.box("ops", 500, 100, 170, 60, "Lote de operações", ["vocabulário fechado"], "#vocabulario", "#444")
    d.box("eng", 710, 100, 180, 60, "Motor (engine.py)", ["tudo ou nada"], None, "#0072B2")
    d.box("decl", 930, 40, 230, 60, "Declarações do domínio", ["modelos partilhados iguais", "caminhos reescritos"], "declaracao.html", COLORS["SM"])
    d.box("chk", 930, 160, 230, 60, "Verificação e ingestão", ["specs, fusão, cobertura;", "o grafo é reconstruído"], "ingestao.html", COLORS["HLM"])
    for a, b in [("nl", "ops"), ("form", "ops"), ("csv", "ops"), ("step", "ops"), ("ops", "eng"), ("eng", "decl"), ("decl", "chk")]:
        d.arrow(a, b)
    body = io_block("um lote de operações", "as declarações, o reservatório e o mapeamento do domínio",
                    "as declarações alteradas, gravadas só se todas as operações do lote forem válidas")
    body += d.render()
    body += ("<p>Toda a alteração às declarações de um domínio é um lote de operações de um vocabulário fechado. "
             "O motor aplica-as pela ordem e mantém as declarações coerentes:</p><ul>"
             "<li>uma operação sobre um modelo partilhado aplica-se em todas as declarações que o contêm, para ele continuar igual em todas;</li>"
             "<li>compor um modelo numa declaração que ainda não o tem copia-o, com os submodelos, as funções e os contextos de que depende;</li>"
             "<li>renomear um modelo, uma propriedade ou um papel reescreve os caminhos das regras, das projeções, dos perfis e do mapeamento;</li>"
             "<li>no fim, as descrições das regras são derivadas de novo; se uma operação falhar, nada é gravado.</li></ul>"
             "<p>As declarações alteradas são verificadas e a aplicação reconstrói a base de dados a partir dos ficheiros: o resultado aparece nas vistas.</p>")
    # natural language example
    done, ingestion = _with_examples([NL_OPERATION])
    body += '<h2 id="exemplo-linguagem">Exemplo: uma regra de inferência a partir de texto</h2>'
    body += (f"<p><b>Pedido</b> (separador Alterações › Linguagem natural):</p><blockquote>{e(NL_REQUEST)}</blockquote>"
             "<p>A aplicação cria um pedido do tipo <code>alteracao</code>. O prompt junta o pedido, o vocabulário de operações, as declarações e o "
             "mapeamento. A <b>resposta</b> do LLM é a operação:</p>" + json_pre({"operacoes": [NL_OPERATION]}))
    body += (f"<p><b>Registar</b> aplica a operação: <code>{e('; '.join(done))}</code>. A regra fica no HLM Dispositivo, com a descrição derivada. "
             "Na ingestão, a regra passa a estes nós e arestas do grafo:</p>" + _rule_subgraph(ingestion, "RIR-HUM-LABORATORIO"))
    body += ('<p>A vista de decisão de <code>Medicao.valor</code> passa a ter a célula LABORATORIO preenchida, '
             'e a vista da regra mostra o subgrafo acima.</p>')
    # CSV example
    ops = operations_from_csv(CSV_TABLE, "USM", "Morada", "codigoPostal", "PATTERN", "RIR-CP-LOCALIDADE")
    done, ingestion = _with_examples(ops)
    body += '<h2 id="exemplo-csv">Exemplo: regras a partir de uma tabela de mapeamentos (CSV)</h2>'
    body += ("<p>Um conjunto de mapeamentos conhecidos, como o código postal que cada localidade admite, é uma tabela. "
             "Cada linha passa a uma RIR: as colunas são caminhos relativos ao modelo onde as regras vivem; a coluna alvo é a restrição e as "
             "restantes são os termos da condição (EQUALS). As colunas opcionais <code>id</code> e <code>mensagem</code> dão o identificador e "
             "a mensagem de cada regra.</p>" + pre(CSV_TABLE)
             + "<p>Alvo <code>codigoPostal</code>, operador <code>PATTERN</code>, regras no USM <code>Morada</code>. As operações geradas:</p>"
             + json_pre({"operacoes": ops})
             + f"<p>Aplicadas às declarações de exemplo: <code>{e('; '.join(done))}</code>. A Morada é partilhada, por isso as regras entram em "
               "todas as declarações que a contêm. Ingestão: " + e("; ".join(r.summary().splitlines()[0] for r in ingestion.results)) + ".</p>")
    # vocabulary
    body += '<h2 id="vocabulario">Vocabulário de operações</h2>'
    for group, title in voc["grupos"].items():
        rows = [[f'<code id="{e(k)}">{e(k)}</code>', e(", ".join(v["campos"])), e(v["descricao"]),
                 ", ".join(x["id"] for x in _layers() if k in x.get("alteracoes", []))] for k, v in voc["operacoes"].items() if v["grupo"] == group]
        body += f"<h3>{e(title)}</h3>" + table(["Operação", "Campos", "O que faz", "Passos"], rows)
    body += "<h2>Prompt de alterações</h2>" + pre(read("ecv/2_amendments/prompts/alteracoes.md"))
    return page("alteracoes", "Alterações", body, section=SECTION, menu="Alterações (operações, texto, CSV)", crumbs=CRUMBS,
                summary="Como uma alteração chega às declarações: pedido em linguagem natural, operações escritas ou tabela CSV; o motor; um exemplo de cada.")


# ---------------------------------------------------------------------- extraction, data, domains
def extraction_page():
    formats = [("PDF (tabelas)", "cius_pt.guia"), ("schematron (.sch)", "cius_pt.schematron"), ("XML UBL anotado", "cius_pt.ubl"),
               ("classes Dart", "fm.dart"), ("xlsx (registos)", "fm.registos"), ("JSON Schema", "json_schema.smart_data_models"),
               ("texto (Markdown)", "texto.markdown")]
    d = Diagram(1200, 380)
    for i, (fmt, adapter) in enumerate(formats):
        d.box(f"f{i}", 15, 15 + i * 52, 170, 42, fmt, [], "dados.html", "#555")
        d.box(f"a{i}", 235, 15 + i * 52, 230, 42, adapter, ["adaptador"], "modulo_transformer.html")
        d.arrow(f"f{i}", f"a{i}")
    d.box("inv", 540, 105, 210, 110, "Inventário (por fonte)", ["grupos · elementos · regras", "tipos base, cardinalidades,", "categoria de cada regra,",
                                                               "origem de cada item"], "#o-formato-do-inventario", COLORS["SM"], stroke=2.6)
    for i in range(len(formats)):
        d.arrow(f"a{i}", "inv", None, color="#bbb")
    d.box("pa", 820, 70, 170, 70, "Geração (fase G)", ["todo o inventário"], "transformacao.html#geracao")
    d.box("pbe", 820, 180, 170, 70, "Revisão A a F", ["itens por camada"], "transformacao.html#camadas")
    d.box("dec", 1030, 120, 160, 80, "Declarações", ["uma por HLM", "+ mapeamento"], "declaracao.html", COLORS["SM"])
    for a, b in [("inv", "pa"), ("inv", "pbe"), ("pa", "dec"), ("pbe", "dec")]:
        d.arrow(a, b)
    body, _ = text("extracao", {"extracao": d.render()})
    body += "<h2>Referência: os campos do inventário</h2>"
    for cls in (inventory_module.Group, inventory_module.Element, inventory_module.SourceRule):
        keys = cls.KEYS
        body += f"<h3>{cls.__name__}</h3>" + table(["Campo (Python)", "Chave no JSON", "Tipo"],
                                                    [[f"<code>{x.name}</code>", f"<code>{e(keys.get(x.name, x.name))}</code>", e(str(x.type))] for x in fields(cls)])
    body += "<h2>Referência: categorias das regras</h2>" + table(["Categoria", "Natureza provável", "Significado", "Passo"], [
        [f"<code>{k}</code>", e(v[0]), e(v[1]), e(next((p for p, cs in STEP_CATEGORIES.items() if k in cs), ""))] for k, v in CATEGORIES.items()])
    body += "<h2>Referência: adaptadores</h2>" + table(["Nome (dominio.json)", "Função", "O que faz"], [
        [f"<code>{e(k)}</code>", f"<code>{e(f.__module__.split('.')[-1])}.{e(f.__name__)}</code>", e((f.__doc__ or "").strip().split(chr(10))[0])]
        for k, f in ADAPTERS.items()])
    body += ("<h2>Um formato sem adaptador</h2><p>Em Declaração › 1. Extração, ao acrescentar uma fonte, a opção \"não existe: pedir a criação de um adaptador\" "
             "(ou o formulário Pedir um adaptador novo) cria um pedido ao LLM na fila global. O prompt "
             "(<code>ecv/0_transformer/prompts/criar_adaptador.md</code>) leva a descrição do formato, uma amostra do ficheiro, o código do formato do inventário, "
             "as categorias das regras e um adaptador existente como exemplo. Registar a resposta (<code>ecv/0_transformer/adapter_requests.py</code>) "
             "confirma que o módulo compila e define <code>NAME</code> e <code>adapt(path)</code>, grava-o em <code>adapters/a_&lt;nome&gt;.py</code>, "
             "recarrega o registo e corre-o na amostra; se falhar, o módulo anterior é reposto.</p>"
             "<h2>Texto em linguagem natural</h2><p>O adaptador <code>texto.markdown</code> lê uma descrição escrita por uma pessoa: cada secção <code>## Nome</code> "
             "é um grupo, cada item <code>- nome (tipo, obrigatório): descrição. Valores: A, B</code> é um elemento, e cada frase com uma obrigação ou condição "
             "(\"deve\", \"tem de\", \"só\", \"se\", \"no máximo\"…) é uma regra candidata. O texto completo segue no prompt da geração. "
             "Exemplo: <code>dados_teste/biblioteca/descricao_biblioteca.md</code> (domínio <code>biblioteca</code>).</p>")
    return page("extracao", "Extração e inventário", body, section=SECTION, menu="Extração e inventário", crumbs=CRUMBS,
                summary="Como cada fonte, no seu formato, passa ao formato intermédio de onde parte a geração, e como se escreve um adaptador.")


def data_page():
    body, _ = text("dados")
    return page("dados", "Dados de origem: faturação e IoT", body, section=SECTION, menu="Dados de origem", crumbs=CRUMBS,
                summary="De onde vêm os dados, em que formato estão, o que representam e que adaptador os lê.")


def domain_pages():
    workspace = Workspace()
    out, cards = [], ""
    for domain_id in workspace.domain_ids():
        domain = workspace.domain(domain_id)
        definition = domain.definition
        inventories = domain.inventories()

        def count(source, key):
            return inventories.get(source["id"], {}).get("contagens", {}).get(key, "")
        body = f"<p>{e(definition['descricao'])}</p><h2>Fontes</h2>" + table(
            ["Id", "Adaptador", "Caminho", "Papel", "Na geração", "Grupos", "Elementos", "Regras por categoria"],
            [[e(s["id"]), f'<code>{e(s["adaptador"])}</code>', e(s["caminho"]), e(s.get("papel")), e(s.get("passoA", "principal")),
              count(s, "grupos"), count(s, "elementos"), e(", ".join(f"{k} {v}" for k, v in (count(s, "regrasPorCategoria") or {}).items()))]
             for s in definition["fontes"]])
        body += "<h2>Excluídos</h2>" + table(["Caminho", "Motivo"], [[e(x["caminho"]), e(x["motivo"])] for x in definition.get("excluidos", [])])
        body += "<h2>Utilizações</h2><ul>" + "".join(f"<li>{e(x)}</li>" for x in definition.get("utilizacoes", [])) + "</ul>"
        body += "<h2>Cenários</h2><ul>" + "".join(f"<li>{e(x)}</li>" for x in definition.get("cenarios", [])) + "</ul>"
        body += "<h2>Estado</h2>" + table(["Passo", "Estado"], [[e(p), e(s["estado"])] for p, s in domain.state["passos"].items()])
        body += f'<p><a href="{REPO}dominios/{e(domain_id)}/dominio.json">dominio.json</a></p>'
        out.append(page(f"dominio_{domain_id}", f"Domínio: {definition['nome']}", body, section=SECTION, menu=f"Domínio {definition['nome']}",
                        sub=True, crumbs=CRUMBS + [("dominios.html", "Domínios")]))
        cards += f'<div class="card"><h3><a href="dominio_{e(domain_id)}.html">{e(definition["nome"])}</a></h3><p class="note">{e(definition["descricao"][:240])}</p></div>'
    body = ('<div class="cards">' + cards + "</div><h2>Acrescentar um domínio ou uma fonte</h2><ol>"
            "<li>Início › Novo domínio (cria <code>dominios/&lt;d&gt;/dominio.json</code>); as utilizações, os cenários e as exclusões escrevem-se nesse ficheiro.</li>"
            "<li>Declaração › 1. Extração: anexar cada documento (fica em <code>dominios/&lt;d&gt;/fontes/</code>) ou indicar o caminho na raiz dos dados, "
            "com o adaptador e o papel; a fonte é gravada em <code>dominio.json</code>.</li>"
            "<li>Para um formato novo, pedir o adaptador ao LLM (ou escrevê-lo em <code>ecv/0_transformer/adapters/</code> e registá-lo em <code>ADAPTERS</code>).</li>"
            "<li>Extrair inventários, rever em Inventário e aceitar a extração.</li></ol>")
    out.append(page("dominios", "Domínios", body, section=SECTION, menu="Domínios", crumbs=CRUMBS))
    return out


def pages():
    return ([main_page(), internal_spec_page(), requests_page(), phase0_page()] + [layer_page(x) for x in _layers()]
            + [amendments_page(), extraction_page(), data_page()] + domain_pages())
