"""Declaração (modules 0 and 1), in two steps:
    1. Extração   the sources of the domain (documents attached here or paths under the data root), the adapter of each
                  one (or a request to the LLM to create it), the extraction (phase 0) and its acceptance;
    2. Geração    one request to the LLM for the complete declarations (phase G), registered as often as needed.
The review layers A to F are in Alterações; here only their state is shown. Also: the declaration files and the mapping."""
import os
import re

from ecv import config, ecv_builder, transformer
from ecv.transformer import adapter_requests
from ecv.transformer.adapters import ADAPTERS, CREATED, describe
from ecv.amendments import DeclarationSet
from ecv.ecv_builder.build_process import cycle, layer_ids, step, step_ids
from ecv.shared.errors import DomainError, StepError
from ecv.shared.llm_requests import RequestQueue

from ..http import Response, not_found, url
from ..pages import layout
from ..pages.components import button_form, e, keyvalues, message, pre, section, state, table

STEP_LABEL = {"0": "1. Extração", "G": "2. Geração"}  # A to F: "Camada X" (review, in Alterações)
DECLARATION_STEPS = ("0", "G")
NEW_ADAPTER = "__novo__"
ADAPTER_FORMATS = {"cius_pt.guia": "guia do modelo semântico CIUS-PT (PDF)", "cius_pt.schematron": "schematron (XSLT/SCH) de regras",
                   "cius_pt.ubl": "modelo UBL 2.1 anotado (XML)", "fm.dart": "classes Dart de uma aplicação",
                   "fm.registos": "desenho de registos de exportação (texto de largura fixa)",
                   "json_schema.smart_data_models": "pasta de modelos JSON Schema (Smart Data Models)",
                   "texto.markdown": "descrição em linguagem natural (Markdown ou texto)"}


def _label(s):
    return STEP_LABEL.get(s, f"Camada {s}")


KIND = {"0": "extração (módulo 0, sem LLM)", "G": "geração (um pedido ao LLM)"}


def _steps_table(domain, selected):
    requests = RequestQueue.for_domain(domain).requests()
    rows = []
    for s in DECLARATION_STEPS:
        d = step(s)
        label = e(_label(s))
        rows.append([f'<a href="{url("/declaracao", passo=s)}">{"<b>" + label + "</b>" if s == selected else label}</a>',
                     e(d["nome"]), e(KIND[s]), state(domain.step_state(s)), str(sum(1 for r in requests if r.step == s)),
                     e(domain.state["passos"][s].get("atualizado") or "")])
    layers = " · ".join(f'<a href="{url("/alteracoes", camada=x)}">{e(x)}</a> {state(domain.step_state(x))}' for x in layer_ids())
    rows.append(["Revisão", "Camadas A a F (no separador Alterações)", "alterações (formulários, CSV, pedidos ao LLM)", layers, "", ""])
    return table(["Passo", "Nome", "Tipo", "Estado", "Pedidos", "Atualizado"], rows, "steps")


def _review_views(app, patterns):
    """The step's review views (build process 'vistas': page name patterns like hlm_<HLM>) resolved in the catalogue."""
    pages = app.catalogue()
    out = []
    for pattern in patterns:
        if pattern.startswith("/"):
            path = re.sub(r"/<\w+>$", "", pattern)
            out.append(f'<a href="{e(path)}">{e(path)}</a>')
            continue
        prefix = re.sub(r"<\w+>.*$", "", pattern)
        found = [p for p in pages if p.startswith(prefix)] if prefix != pattern else [p for p in pages if p == pattern]
        if found:
            out.append(" ".join(f'<a href="/vistas/{e(p)}.html">{e(p)}</a>' for p in found[:40])
                       + (f" … (+{len(found) - 40})" if len(found) > 40 else ""))
        else:
            out.append(f'<span class="note">{e(pattern)}: ainda não existe</span>')
    return "<br>".join(out)


def _step_requests(domain, s):
    queue = RequestQueue.for_domain(domain)
    rows = []
    for r in queue.requests():
        if r.step == s:
            rows.append([f'<a href="/pedidos/{e(domain.id)}/{e(r.id)}">{e(r.id)}</a>', e(r.title), state(r.state),
                         e(r.meta.get("criado")), e(r.meta.get("resumo") or "")])
    return table(["Pedido", "Título", "Estado", "Criado", "Resultado"], rows) if rows else '<p class="note">Nenhum pedido.</p>'


def _actions(domain, s):
    st = domain.step_state(s)
    if s == "0":
        actions = button_form("/declaracao/extrair", "Extrair inventários", css="primary",
                              confirm="Reescreve os inventários do domínio a partir das fontes. Continuar?")
        if st == "em revisão":
            actions += button_form("/declaracao/aceitar", "Aceitar a extração", {"passo": "0"})
        return f'<p>{actions} <a href="/inventario">ver os inventários</a></p>'
    out = []
    if s == "G":
        out.append(button_form("/declaracao/preparar", "Preparar pedido de geração ao LLM", {"passo": s}, "primary"))
    out.append(button_form("/declaracao/verificar", "Verificar", {"passo": s}))
    if st in ("em revisão", "em curso") or (s != "G" and st == "por iniciar" and domain.declaration_files()):
        out.append(button_form("/declaracao/aceitar", "Aceitar", {"passo": s},
                               confirm="Aceitar? As perguntas de revisão estão respondidas?"))
    return "<p>" + "".join(out) + "</p>"


def _step_detail(app, domain, s, check_text=None):
    d = step(s)
    rows = [("Estado", state(domain.step_state(s))), ("Objetivo", e(d["objetivo"])), ("Pergunta", e(d["pergunta"]))]
    if d.get("camada"):
        rows.append(("Camada", e(d["camada"])))
    if isinstance(d.get("entradas"), str):
        rows.append(("Itens do inventário" if s != "G" else "Entradas", e(d["entradas"])))
    if d.get("aplicacao"):
        rows.append(("Aplicação da resposta", e(d["aplicacao"])))
    rows += [("Verificações", e(", ".join(d.get("verificacoes", []))) + "<br>" + "<br>".join(e(x) for x in d.get("verificacoesDoPasso", []))),
             ("Aceitação", e(d.get("aceitacao", "—")))]
    body = keyvalues(rows) + _actions(domain, s)
    if check_text:
        body += section("Resultado da verificação", pre(check_text))
    if s == "0":
        return body + _extraction(domain)
    if s == "G":
        body += section("Pedidos de geração", _step_requests(domain, s))
    else:
        body += section("Pedidos de alterações desta camada", _step_requests(domain, s))
    if d.get("vistas"):
        body += section("Vistas de revisão", f"<p>{_review_views(app, d['vistas'])}</p>")
    if d.get("revisao"):
        body += section("Perguntas de revisão", "<ol>" + "".join(f"<li>{e(q)}</li>" for q in d["revisao"]) + "</ol>")
    return body


def _cycle_table():
    c = cycle()
    rows = [[e(x["nome"]), e(x.get("fase")), e(x.get("quem")), e(x["descricao"]), e(x.get("web"))] for x in c["etapas"]]
    return table(["Etapa", "Fase", "Executa", "O que acontece", "Onde, na aplicação"], rows)


def _outputs(domain, name):
    """Links to the Cypher load and the static views of a declaration (or of all, name '*')."""
    static = _static_folder(domain, name)
    links = [f'<a href="/declaracao/cypher/{e(name)}">carga Cypher</a>',
             button_form("/declaracao/estaticas", "gerar vistas estáticas", {"nome": name})]
    if (static / "index.html").exists():
        links.append(f'<a href="/estaticas/{e(domain.id)}/{e(_stem(name))}/index.html" target="_blank">abrir as vistas estáticas</a>')
    return " ".join(links)


def _declarations(domain):
    rows = [[f'<a href="/declaracao/ficheiro/{e(f.name)}">{e(f.name)}</a>', f"{f.stat().st_size // 1024} KB",
             f'<a href="{url("/vistas", ambito=f"{domain.id}::{f.name}")}">vistas desta declaração</a>', _outputs(domain, f.name)]
            for f in domain.declaration_files()]
    if rows:
        rows.append(["<b>todas</b>", "", f'<a href="{url("/vistas", ambito=domain.id)}">vistas de todas</a>', _outputs(domain, ALL)])
    return (table(["Ficheiro", "Tamanho", "Vistas (na aplicação)", "Carga Cypher (Neo4j) e vistas estáticas"], rows)
            + '<p class="note">A carga Cypher é o script que cria, no Neo4j, as restrições de unicidade, os nós e as arestas da declaração (o grafo já integrado pela ingestão). '
              f'As vistas estáticas são as páginas HTML e os ViewModels JSON de todas as vistas, escritos em <code>dominios/{e(domain.id)}/saidas/</code>.</p>'
            if rows else '<p class="note">Ainda não há declarações (a geração, fase G, cria-as).</p>')


# ---------------------------------------------------------------------- outputs of a declaration: Cypher load and static views
ALL = "todas"


def _stem(name):
    return name.replace(".ecv.json", "")


def _static_folder(domain, name):
    return domain.folder / "saidas" / f"vistas_{_stem(name)}"


def _files(domain, name):
    files = domain.declaration_files()
    if name == ALL:
        return files
    f = domain.declarations_folder / name
    if f not in files:
        raise not_found(f"a declaração {name} não existe no domínio")
    return [f]


def cypher_load(app, request):
    """The Cypher script that loads the declaration (or all) into Neo4j; also written to dominios/<d>/saidas/."""
    from ecv.graph.cypher_export import export
    from ecv.ingestion import ingest
    domain = app.require_domain()
    name = request.params["nome"]
    files = _files(domain, name)
    ingestion = ingest(files)
    text = export(ingestion.graph, ", ".join(f.name for f in files))
    target = domain.folder / "saidas" / f"{_stem(name)}.cypher"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text, encoding="utf-8")
    app.log.event(f"{domain.id}: carga Cypher de {name} ({len(text)} caracteres) em {target.relative_to(domain.folder)}")
    return Response.text(text, "text/plain; charset=utf-8", filename=target.name)


def static_views(app, request):
    """Write the static views (HTML + ViewModel JSON) of a declaration (or all) to dominios/<d>/saidas/vistas_<nome>/."""
    from ecv.ingestion import ingest
    from ecv.views import links
    from ecv.views.static_site import generate
    domain = app.require_domain()
    name = request.form()["nome"]
    files = _files(domain, name)
    folder = _static_folder(domain, name)
    try:
        done = generate(ingest(files).graph, folder, title=f"Vistas · {domain.name} · {name}", origin=", ".join(f.name for f in files))
    finally:
        links.set_existing(app.catalogue())            # the links of the application's views again
    app.log.event(f"{domain.id}: {len(done)} vistas estáticas de {name} em {folder.relative_to(domain.folder)}")
    return Response.redirect(url("/declaracao", passo="G", aviso=f"{len(done)} vistas estáticas de {name} escritas em dominios/{domain.id}/saidas/{folder.name}/"))


def static_file(app, request):
    """A file of the static views written by static_views (served as is)."""
    domain = app.workspace.domain(request.params["dominio"])
    folder = domain.folder / "saidas" / f"vistas_{request.params['declaracao']}"
    f = (folder / request.params["pagina"]).resolve()
    if f.parent != folder.resolve() or not f.exists():
        raise not_found(f"{request.params['pagina']} não existe")
    kind = "application/json; charset=utf-8" if f.suffix == ".json" else "text/html; charset=utf-8"
    return Response.text(f.read_text(encoding="utf-8"), kind)


def render(app, request, s=None, check_text=None, notice=None):
    domain = app.require_domain()
    s = s or request.get("passo") or domain.current_step()
    if s in layer_ids():
        s = "G"
    if s not in step_ids():
        raise not_found(f"passo desconhecido: {s}")
    body = message(notice or request.get("aviso"), request.get("tipo", "ok"))
    body += section("Passos da declaração", _steps_table(domain, s))
    body += section(f"{_label(s)} · {step(s)['nome']}", _step_detail(app, domain, s, check_text))
    body += section("Declarações do domínio", _declarations(domain) + '<p><a href="/mapeamento">Mapeamento e cobertura</a></p>')
    body += section("Ciclo", _cycle_table())
    body += _where_box()
    return Response.html(layout.page(app, "declaracao", f"Declaração · {domain.name}", body, request.path,
                                     "1. Extração: as fontes, pelos adaptadores, em inventários. 2. Geração: inventário + especificação → declarações completas. "
                                     "A revisão por camadas (A a F) faz-se em Alterações."))


def page(app, request):
    return render(app, request)


# ---------------------------------------------------------------------- 1. extraction: sources, documents, adapters
def _adapter_select(name, current=None, new=True):
    options = "".join(f'<option value="{e(a)}"{" selected" if a == current else ""}>{e(a)}</option>' for a in sorted(ADAPTERS))
    if new:
        options += f'<option value="{NEW_ADAPTER}">(não existe: pedir a criação de um adaptador)</option>'
    return f'<select name="{e(name)}">{options}</select>'


def _sources(domain):
    inventories = domain.inventories()
    rows = []
    for src in domain.sources():
        inv = inventories.get(src["id"])
        counts = f'{len(inv["grupos"])} / {len(inv["elementos"])} / {len(inv["regras"])}' if inv else "—"
        found = bool(_source_files(src))
        change = (f'<form method="post" action="/declaracao/fonte" class="inline"><input type="hidden" name="id" value="{e(src["id"])}">'
                  f'{_adapter_select("adaptador", src["adaptador"])} <button>Mudar</button></form>')
        rows.append([f'<a href="{url("/inventario", fonte=src["id"])}">{e(src["id"])}</a>' if inv else e(src["id"]), change,
                     f'<code>{e(src["caminho"])}</code>' + ("" if found else ' <span class="state st-rejeitado">não encontrado</span>'),
                     e(src.get("passoA", "principal")), e(src.get("papel")), counts,
                     button_form("/declaracao/fonte/remover", "Remover", {"id": src["id"]}, confirm=f"Remover a fonte {src['id']} de dominio.json?")])
    return (table(["Fonte", "Adaptador", "Caminho (na raiz dos dados)", "Papel na geração", "Descrição", "Grupos / elementos / regras", ""], rows)
            if rows else '<p class="note">O domínio ainda não tem fontes: anexe um documento abaixo.</p>')


def _source_files(src):
    import glob
    return glob.glob(str(config.data_root() / src["caminho"]))


def _attach_form():
    return ('<form method="post" action="/declaracao/fonte" enctype="multipart/form-data" class="stack">'
            '<p><label>Documento <input type="file" name="ficheiro" multiple></label> '
            '<span class="note">ou um caminho já existente na raiz dos dados</span> '
            '<input name="caminho" size="50" placeholder="data/…/ficheiro ou pasta"></p>'
            f'<p><label>Identificador <input name="id" size="24" placeholder="ex.: descricao-biblioteca"></label> '
            f'<label>Adaptador {_adapter_select("adaptador", "texto.markdown")}</label> '
            '<label>Papel <input name="papel" size="50" placeholder="o que esta fonte dá à declaração"></label> '
            '<label><input type="checkbox" name="complementar" value="1"> complementar (só confirma cardinalidades e descrições)</label></p>'
            '<p><button class="primary">Acrescentar a fonte</button></p></form>'
            '<p class="note">O documento fica em <code>dominios/&lt;d&gt;/fontes/</code> e a fonte em <code>dominio.json</code>. '
            'Escolher "pedir a criação de um adaptador" cria um pedido ao LLM com uma amostra do documento.</p>')


def _adapters_table():
    rows = [[f"<code>{e(name)}</code>", e(ADAPTER_FORMATS.get(name) or doc),
             f"<code>ecv/0_transformer/adapters/{e(module)}</code>" + (" (criado por pedido)" if name in CREATED else "")]
            for name, module, doc in describe()]
    form = ('<form method="post" action="/declaracao/adaptador" class="stack"><p>'
            '<label>Nome <input name="nome" size="24" placeholder="formato.variante, ex.: csv.produtos"></label> '
            '<label>Amostra <input name="amostra" size="50" placeholder="caminho de um ficheiro na raiz dos dados (opcional)"></label></p>'
            '<p><textarea name="descricao" rows="3" cols="100" placeholder="o formato: o que é cada parte, onde estão os nomes, os tipos, as regras"></textarea></p>'
            '<p><button>Pedir a criação do adaptador ao LLM</button></p></form>')
    return table(["Adaptador", "Lê", "Módulo"], rows) + "<h3>Pedir um adaptador novo</h3>" + form


def _extraction(domain):
    return (section("Fontes do domínio (dominio.json)", _sources(domain))
            + section("Anexar um documento ou indicar uma fonte", _attach_form())
            + section("Adaptadores disponíveis", _adapters_table()))


def _where_box():
    rows = [("A definição do domínio e as fontes", "<code>dominios/&lt;d&gt;/dominio.json</code>"),
            ("Os documentos anexados", "<code>dominios/&lt;d&gt;/fontes/</code>"),
            ("Os adaptadores (registo ADAPTERS)", "<code>ecv/0_transformer/adapters/__init__.py</code>"),
            ("A extração (fase 0)", "<code>ecv/0_transformer/extraction.py</code>"),
            ("O formato do inventário", "<code>ecv/0_transformer/inventory.py</code>"),
            ("Os inventários extraídos", "<code>dominios/&lt;d&gt;/inventario/&lt;fonte&gt;.json</code>"),
            ("Os pedidos de adaptador", "<code>ecv/0_transformer/adapter_requests.py</code> · fila <code>pedidos/</code>"),
            ("O processo de construção (passos, camadas, verificações)", "<code>ecv/1_ecv_builder/build_process.json</code>"),
            ("O prompt da geração", "<code>ecv/1_ecv_builder/prompts/comum.md</code> + <code>G_geracao.md</code>; especificação <code>ecv/1_ecv_builder/specs/ecv_specs.md</code>"),
            ("O registo da resposta da geração", "<code>ecv/1_ecv_builder/workflow.py</code> · <code>register_generation_response</code>"),
            ("As declarações .ecv.json e o mapeamento", "<code>dominios/&lt;d&gt;/declaracoes/*.ecv.json</code> · <code>dominios/&lt;d&gt;/mapeamento.json</code>"),
            ("O estado dos passos", "<code>dominios/&lt;d&gt;/estado.json</code>"),
            ("Esta página", "<code>ecv/7_webapp/handlers/builder.py</code>")]
    return section("Onde está, no código e nos ficheiros", table(["O quê", "Onde"], [[e(a), b] for a, b in rows]))


def _safe_name(name):
    return re.sub(r"[^A-Za-z0-9._-]+", "_", os.path.basename(name or "")).strip("._") or "documento"


def add_source(app, request):
    """Add or change a source: attached documents (saved in dominios/<d>/fontes/) or a path under the data root."""
    domain = app.require_domain()
    form = request.form()
    files = request.files()
    existing = next((x for x in domain.sources() if x["id"] == form.get("id")), None)
    path = form.get("caminho", "").strip()
    if files:
        domain.uploads_folder.mkdir(parents=True, exist_ok=True)
        saved = []
        for _, filename, data in files:
            target = domain.uploads_folder / _safe_name(filename)
            target.write_bytes(data)
            saved.append(target)
        target = saved[0] if len(saved) == 1 else domain.uploads_folder
        path = os.path.relpath(target, config.data_root())
    adapter = form.get("adaptador", "")
    source_id = form.get("id", "").strip() or (re.sub(r"[^a-z0-9]+", "-", os.path.splitext(os.path.basename(path))[0].lower()).strip("-") if path else "")
    if existing and not path:
        path = existing["caminho"]
    if not source_id or not path:
        raise DomainError("indique o documento (ou o caminho) da fonte")
    if adapter == NEW_ADAPTER:
        name = f"novo.{re.sub(r'[^a-z0-9]+', '_', source_id.lower())}"
        sample = config.data_root() / path
        r = adapter_requests.request_adapter(name, f"Formato da fonte {source_id}: {form.get('papel') or 'ver a amostra'}.", sample)
        domain.set_source({**(existing or {}), "id": source_id, "adaptador": name, "caminho": path, "papel": form.get("papel") or (existing or {}).get("papel", "")})
        app.log.event(f"{domain.id}: fonte {source_id} sem adaptador; pedido {r.id} criado ({name})")
        return Response.redirect(f"/pedidos/global/{r.id}", note=r.id)
    source = {"id": source_id, "adaptador": adapter, "caminho": path}
    if form.get("papel"):
        source["papel"] = form["papel"]
    if form.get("complementar"):
        source["passoA"] = "complementar"
    domain.set_source(source)
    app.log.event(f"{domain.id}: fonte {source_id} ({adapter}, {path}) gravada em dominio.json")
    return Response.redirect(url("/declaracao", passo="0", aviso=f"Fonte {source_id} gravada; extraia os inventários."))


def remove_source(app, request):
    domain = app.require_domain()
    source_id = request.form()["id"]
    domain.remove_source(source_id)
    app.log.event(f"{domain.id}: fonte {source_id} removida de dominio.json")
    return Response.redirect(url("/declaracao", passo="0", aviso=f"Fonte {source_id} removida."))


def request_adapter(app, request):
    form = request.form()
    sample = form.get("amostra", "").strip()
    r = adapter_requests.request_adapter(form.get("nome", "").strip(), form.get("descricao", ""), config.data_root() / sample if sample else None)
    app.log.event(f"pedido {r.id} criado: adaptador {r.meta['adaptador']}")
    return Response.redirect(f"/pedidos/global/{r.id}", note=r.id)


def extract(app, request):
    domain = app.require_domain()
    summary = transformer.extract(domain)
    app.log.event(f"{domain.id}: fase 0 extraída ({'; '.join(summary)})")
    return Response.redirect(url("/declaracao", passo="0", aviso=f"{len(summary)} inventário(s) escritos; reveja-os e aceite a extração"),
                             note="extração")


def create_domain(app, request):
    form = request.form()
    domain = app.workspace.create_domain(form.get("id", "").strip(), form.get("nome", "").strip() or form.get("id", ""), form.get("descricao", "").strip())
    app.use_scope(domain.id)
    app.log.event(f"domínio {domain.id} criado")
    return Response.redirect(url("/declaracao", passo="0", aviso=f"Domínio {domain.id} criado: acrescente as fontes."))


# ---------------------------------------------------------------------- 2. generation and the review layers' checks
def prepare(app, request):
    domain = app.require_domain()
    s = request.form()["passo"]
    if s != "G":
        raise StepError("os passos A a F são de revisão: as correções fazem-se por pedidos de alterações")
    r = ecv_builder.prepare_generation(domain)
    app.log.event(f"{domain.id}: pedido {r.id} criado ({r.meta['tamanho']['caracteres']} caracteres, ~{r.meta['tamanho']['tokensEstimados']} tokens)")
    return Response.redirect(f"/pedidos/{domain.id}/{r.id}", note=r.id)


def verify(app, request):
    domain = app.require_domain()
    form = request.form()
    s = form["passo"]
    check = ecv_builder.verify_step(domain, s)
    app.log.event(f"{domain.id}: verificação do passo {s}: {check.summary()}")
    if form.get("voltar"):
        return Response.redirect(url(form["voltar"], aviso=("Pode ser aceite: " if check.valid else "Não pode ser aceite: ") + check.summary(),
                                     tipo="ok" if check.valid else "warn"))
    return render(app, request, s, check.text(), notice=("Pode ser aceite." if check.valid else "Não pode ser aceite: ver o resultado."))


def accept(app, request):
    domain = app.require_domain()
    form = request.form()
    s = form["passo"]
    try:
        check = ecv_builder.accept_step(domain, s)
    except StepError as err:
        if form.get("voltar"):
            return Response.redirect(url(form["voltar"], aviso=f"Não aceite: {err}", tipo="error"))
        return render(app, request, s, str(err), notice="O passo não foi aceite.")
    app.log.event(f"{domain.id}: {_label(s)} aceite" + (f" ({check.summary()})" if check else ""))
    back = form.get("voltar") or url("/declaracao", passo=s)
    return Response.redirect(url(back, aviso=f"{_label(s)} aceite"), note=f"{s} aceite")


def declaration_file(app, request):
    domain = app.require_domain()
    name = request.params["nome"]
    f = domain.declarations_folder / name
    if f not in domain.declaration_files():
        raise not_found(f"a declaração {name} não existe no domínio")
    return Response.text(f.read_text(encoding="utf-8"), "application/json; charset=utf-8")


def mapping_page(app, request):
    domain = app.require_domain()
    if not domain.declaration_files():
        body = message("Ainda não há mapeamento: a geração (fase G) cria-o.", "info")
    else:
        ds = DeclarationSet.load(domain.folder)
        from ecv.ecv_builder.checks import StepChecker
        rows = []
        for s in step_ids()[1:]:
            missing = StepChecker(domain, s).coverage()
            rows.append([e(_label(s)), str(sum(1 for x in ds.mapping if x.get("passo") == s)), str(len(missing)),
                         e(", ".join(missing[:12])) + (" …" if len(missing) > 12 else "")])
        decision = request.get("decisao")
        entries = [x for x in ds.mapping if not decision or x.get("decisao") == decision]
        decisions = sorted({x.get("decisao") for x in ds.mapping})
        body = section("Cobertura por passo", table(["Passo", "Entradas", "Por mapear", "Exemplos"], rows))
        body += "<p>" + " · ".join(f'<a href="{url("/mapeamento", decisao=d)}">{e(d)}</a>' for d in decisions) + "</p>"
        body += section(f"Entradas ({len(entries)})", table(["Fonte", "Origem", "Decisão", "Destino / motivo", "Passo"],
                        [[e(x["fonte"]), e(x["origem"]), e(x["decisao"]), e(x.get("destino") or x.get("motivo")), e(x.get("passo"))] for x in entries]))
    return Response.html(layout.page(app, "declaracao", f"Mapeamento · {domain.name}", body, request.path,
                                     "Cada elemento e regra das fontes: o seu lugar nas declarações, ou o motivo de ter sido descartado."))


def api(app, request):
    domain = app.require_domain()
    return Response.json({"dominio": domain.id, "passos": domain.state["passos"],
                          "declaracoes": [f.name for f in domain.declaration_files()]})
