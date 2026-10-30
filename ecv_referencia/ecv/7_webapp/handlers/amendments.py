"""Alterações (module 2): the review of the declarations, layer by layer (A to F).

Each layer shows, from top to bottom:
    operations     the operations of the layer; choosing one opens its guided form
    guided form    selectors with what exists (model, property, rule, projection, ...), the context for the decision
                   (plausible values, links to the analysis views) and the operation already filled in (JSON), to preview
                   and apply; a projection is chosen with checkboxes over the HLM's paths
    what exists    the entities of the layer, each with a link to change it
Two more sub-tabs: CSV (a table of known mappings becomes one RIR per row) and the vocabulary.
Where everything lives in the code and in the files is shown on each page.
"""
import json
import urllib.parse

from ecv import ecv_builder
from ecv.amendments import DeclarationSet, guides, operations_from_csv, parse_operations, vocabulary
from ecv.amendments.operations import HANDLERS
from ecv.config import OPERATORS
from ecv.ecv_builder.build_process import layers, step
from ecv.shared.errors import EcvError
from ecv.shared.llm_requests import RequestQueue
from ecv.views import links as L

from ..http import Response, url
from ..pages import layout
from ..pages.components import button_form, e, field, keyvalues, message, pre, section, select, state, table, textarea
from . import functions as functions_tab

SELECTION_KEYS = ("modelo", "propriedade", "regra", "hlm", "projecao", "perfil", "funcao", "contexto", "filho")
RULE_KINDS = {"C": ("RP",), "D": ("RIR", "RIC"), "E": ("RP", "RIR", "RIC")}
EXTRA_TABS = [("csv", "Tabela CSV"), ("vocabulario", "Vocabulário")]


# ---------------------------------------------------------------------- shared pieces
def _layer_tabs(current):
    items = [(x["id"], f'{x["id"]} · {x["nome"]}') for x in layers()] + EXTRA_TABS
    return '<div class="subtabs">' + "".join(f'<a href="{url("/alteracoes", camada=k)}" class="{"active" if k == current else ""}">{e(t)}</a>'
                                             for k, t in items) + "</div>"


def _where_box(rows):
    return section("Onde está, no código e nos ficheiros", table(["O quê", "Onde"], [[e(a), b] for a, b in rows]))


def _code(path):
    return f"<code>{e(path)}</code>"


def _handler_location(op):
    fn = HANDLERS.get(op)
    if fn is None:
        return "—"
    module = fn.__module__.split(".")[-1]
    return _code(f"ecv/2_amendments/operations/{module}.py") + f" · função <code>{e(fn.__name__)}</code>"


def _state_query(layer, op, selection):
    return urllib.parse.urlencode({"camada": layer, **({"op": op} if op else {}), **{k: v for k, v in selection.items() if v}})


# ---------------------------------------------------------------------- operations of the layer
def _operations_list(layer_id, op, selection):
    ops = vocabulary()["operacoes"]
    rows = []
    for name in step(layer_id).get("alteracoes", []):
        link = f'<a href="{url("/alteracoes", camada=layer_id, op=name, **{k: v for k, v in selection.items() if v})}">{"<b>" + e(name) + "</b>" if name == op else e(name)}</a>'
        rows.append([link, e(ops[name]["descricao"]), e(", ".join(guides.LABELS[x] for x in guides.SELECTORS.get(name, [])) or "—")])
    return table(["Operação", "O que faz", "O que se escolhe"], rows)


def _selectors_form(ds, layer_id, op, selection):
    parts = [f'<input type="hidden" name="camada" value="{e(layer_id)}">', f'<input type="hidden" name="op" value="{e(op)}">']
    for key in guides.SELECTORS.get(op, []):
        opts = guides.options(ds, key, selection, RULE_KINDS.get(layer_id))
        optional = (op, key) in guides.OPTIONAL
        choices = [("", "— nova —" if optional and key in ("projecao", "perfil", "funcao", "contexto") else "— escolher —")] + opts
        parts.append(field(guides.LABELS[key], select(key, choices, selection.get(key)).replace("<select ", '<select onchange="this.form.submit()" '),
                           f"{len(opts)} disponíveis" + (" · opcional" if optional else "")))
    return '<form method="get" action="/alteracoes">' + "".join(parts) + "<noscript><button>Escolher</button></noscript></form>"


def _decision_context(app, ds, selection):
    """Context for the decision: plausible values and links to the analysis views of what was chosen."""
    rows = []
    level, _, name = (selection.get("modelo") or "").partition(":")
    if level and name:
        page = L.model_page(level, name)
        rows.append(("Vista do modelo", f'<a href="/vistas/{e(page)}.html" target="_blank">{e(level)} {e(name)}</a>'))
        prop = selection.get("propriedade")
        if prop:
            key = f"{level}:{name}.{prop}"
            values = guides.plausible_values(ds, level, name, prop)
            rows.append(("Valores plausíveis (RP IN)", e(", ".join(map(str, values))) if values else "sem lista fechada"))
            pages = app.catalogue()
            for label, page in (("Decisão (RIR que a restringem)", L.decision_page(key)), ("Dependências (regras que a leem)", L.dependencies_page(key)),
                                ("Impacto de a alterar", L.impact_page(key))):
                if page in pages:
                    rows.append((label, f'<a href="/vistas/{e(page)}.html" target="_blank">{e(page)}</a>'))
    if selection.get("regra"):
        rows.append(("Ficha da regra", f'<a href="/vistas/{e(L.rule_page(selection["regra"]))}.html" target="_blank">{e(selection["regra"])}</a>'))
    if selection.get("hlm"):
        rows.append(("Projeções do HLM", f'<a href="/vistas/{e(L.projections_page(selection["hlm"]))}.html" target="_blank">matriz de projeções</a>'))
        rows.append(("Lacunas do HLM", f'<a href="/vistas/{e(L.gaps_page(selection["hlm"]))}.html" target="_blank">propriedades sem regras ou sem projeção</a>'))
    if selection.get("perfil") or selection.get("projecao"):
        rows.append(("Candidatas a fixar", '<a href="/vistas/candidatos_perfil.html" target="_blank">propriedades lidas em muitas RIR</a>'))
    return keyvalues(rows) if rows else ""


PROJECTION_JS = """<script>
document.addEventListener('DOMContentLoaded',function(){var t=document.getElementById('ops');if(!t)return;
 function rebuild(){var o;try{o=JSON.parse(t.value)}catch(x){return}var p=o.operacoes[0].projecao;p.obrigatorias=[];p.permitidas=[];
  document.querySelectorAll('input[data-path]:checked').forEach(function(r){if(r.value==='o')p.obrigatorias.push(r.getAttribute('data-path'));
   else if(r.value==='p')p.permitidas.push(r.getAttribute('data-path'))});
  t.value=JSON.stringify(o,null,1)}
 document.querySelectorAll('input[data-path]').forEach(function(r){r.addEventListener('change',rebuild)});rebuild();});
</script>"""


def _projection_helper(ds, operation):
    """Checkboxes over the HLM's paths: obligatory, permitted or excluded (rebuilds the JSON)."""
    projection = operation["projecao"]
    hlm = projection.get("hlm")
    if not hlm or hlm not in ds.declarations:
        return ""
    mandatory, permitted = set(projection.get("obrigatorias", [])), set(projection.get("permitidas", []))
    others = [x for x in guides.section_items(ds, "projecoes") if x.get("hlm") == hlm and x["nome"] != projection["nome"]]
    rows = []
    for path in guides.hlm_paths(ds, hlm):
        current = "o" if path in mandatory else ("p" if path in permitted else "x")
        cells = [f'<label><input type="radio" name="r-{e(path)}" value="{v}" data-path="{e(path)}" autocomplete="off"{" checked" if current == v else ""}> {t}</label>'
                 for v, t in (("o", "obrigatória"), ("p", "permitida"), ("x", "excluída"))]
        rows.append([f"<code>{e(path)}</code>"] + cells)
    note = ("<p>Outras projeções deste HLM: " + (", ".join(f"<code>{e(x['nome'])}</code>" for x in others) or "nenhuma")
            + ". Uma projeção diz, para uma utilização, que propriedades são obrigatórias e quais são permitidas; o resto fica excluído. "
              "Escolha abaixo; o JSON atualiza-se.</p>")
    return section("Propriedades da projeção", note + table(["Caminho", "", "", ""], rows)) + PROJECTION_JS


def _guided_form(app, ds, layer_id, op, selection):
    body = f"<p><b>{e(op)}</b>: {e(guides.description(op))}</p>" + _selectors_form(ds, layer_id, op, selection)
    missing = guides.missing_selection(op, selection)
    if missing:
        return body + message("Escolha: " + ", ".join(guides.LABELS[x] for x in missing) + ".", "info")
    body += _decision_context(app, ds, selection)
    operation = guides.prefill(ds, op, selection, layer_id)
    if op == "definir_projecao":
        body += _projection_helper(ds, operation)
    if op == "adicionar_regra":
        body += _rule_builder(ds, selection, layer_id)
    state_query = _state_query(layer_id, op, selection)
    body += ('<form method="post" action="/alteracoes/operacoes">'
             f'<input type="hidden" name="estado" value="{e(state_query)}"><input type="hidden" name="passo" value="{e(layer_id)}">'
             + field("Operação (JSON)", textarea("operacoes", json.dumps({"operacoes": [operation]}, ensure_ascii=False, indent=1), 14, ident="ops"),
                     "substitua os valores <…>; a descrição das regras é derivada pelo código")
             + '<p><button name="acao" value="previsualizar">Pré-visualizar</button> <button name="acao" value="aplicar" class="primary">Aplicar</button></p></form>')
    return body


# ---------------------------------------------------------------------- rule builder (adicionar_regra)
RULE_TYPES = [("RP", "plausibilidade", "RP · plausibilidade: só a restrição, sempre aplicável"),
              ("RIR", "inferencia_restritiva", "RIR · inferência restritiva: se a condição se verifica → a restrição aplica-se"),
              ("RIC", "inferencia_conclusiva", "RIC · inferência conclusiva: se a condição se verifica → conclui (informa uma ação ou um estado; não restringe)")]
LAYER_RULE_TYPE = {"C": "RP", "D": "RIR", "E": "RP"}

RULE_JS = """<script>
document.addEventListener('DOMContentLoaded',function(){
 var D=JSON.parse(document.getElementById('rb-data').textContent),t=document.getElementById('ops');if(!t)return;
 var byPath={};D.caminhos.forEach(function(c){byPath[c.caminho]=c});
 var fnByName={};D.funcoes.forEach(function(f){fnByName[f.nome]=f});
 function opt(v,txt,sel){return '<option value="'+v.replace(/"/g,'&quot;')+'"'+(v===sel?' selected':'')+'>'+txt+'</option>'}
 function pathSelect(cls){return '<select class="'+cls+'"><option value="">— propriedade —</option>'+D.caminhos.map(function(c){
   return opt(c.caminho,c.caminho+' ('+(c.tipo||'?')+')')}).join('')+'</select>'}
 function opSelect(){return '<select class="op">'+Object.keys(D.operadores).map(function(o){
   return opt(o,D.operadores[o].simbolo+' · '+o)}).join('')+'</select>'}
 function fnSelect(){return '<select class="fn"><option value="">— função —</option>'+D.funcoes.map(function(f){return opt(f.nome,f.nome)}).join('')+'</select>'}
 function term(row){row.innerHTML=pathSelect('prop')+' '+opSelect()+' <input class="val" size="28" list="'+row.dataset.list+'"> '
   +'<span class="fnpart" style="display:none">'+fnSelect()+' <span class="args"></span></span>'
   +(row.dataset.removable?' <button type="button" class="rm">remover</button>':'')+' <span class="hint note"></span>';
  wire(row)}
 function wire(row){
  row.querySelectorAll('select,input').forEach(function(x){x.addEventListener('change',function(){refresh(row);rebuild()});x.addEventListener('input',rebuild)});
  var rm=row.querySelector('.rm');if(rm)rm.addEventListener('click',function(){row.remove();rebuild()});refresh(row)}
 function refresh(row){var op=row.querySelector('.op').value,isFn=op==='FUNCTION'||op==='EXT_FUNCTION';
  row.querySelector('.prop').style.display=isFn?'none':'';row.querySelector('.val').style.display=isFn?'none':'';
  row.querySelector('.fnpart').style.display=isFn?'':'none';
  var c=byPath[row.querySelector('.prop').value],dl=document.getElementById(row.dataset.list);
  dl.innerHTML=(c&&c.valores?c.valores:[]).map(function(v){return '<option value="'+v+'">'}).join('');
  var f=D.operadores[op].forma,h={lista:'valores separados por vírgulas',intervalo:'mínimo .. máximo',padrao:'expressão regular',comprimento:'n ou mín .. máx'}[f]||'';
  if(c&&c.valores)h+=(h?' · ':'')+'valores plausíveis: '+c.valores.slice(0,12).join(', ')+(c.valores.length>12?' …':'');
  row.querySelector('.hint').textContent=h;
  if(isFn){var fn=fnByName[row.querySelector('.fn').value],args=row.querySelector('.args'),n=fn?fn.parametros.length:0;
   if(args.children.length!==n){args.innerHTML=(fn?fn.parametros:[]).map(function(p){return '<label>'+p.nome+' '+pathSelect('arg')+'</label>'}).join(' ');
    args.querySelectorAll('select').forEach(function(x){x.addEventListener('change',rebuild)})}}}
 function typed(v,path){var c=byPath[path];v=v.trim();if(c&&(c.tipo==='inteiro'||c.tipo==='decimal')&&v!==''&&!isNaN(Number(v)))return Number(v);
  if(c&&c.tipo==='booleano')return v==='true'||v==='verdadeiro';return v}
 function value(row){var op=row.querySelector('.op').value,f=D.operadores[op].forma,path=row.querySelector('.prop').value,v=row.querySelector('.val').value;
  if(f==='lista')return v.split(',').map(function(x){return typed(x,path)}).filter(function(x){return x!==''});
  if(f==='intervalo'||(f==='comprimento'&&v.indexOf('..')>=0))return v.split('..').map(function(x){return typed(x,path)});
  if(f==='comprimento')return Number(v);return typed(v,path)}
 function termJson(row){var op=row.querySelector('.op').value;
  if(op==='FUNCTION'||op==='EXT_FUNCTION'){var fn=row.querySelector('.fn').value;
   return {operador:op,chamada:{funcao:fn||'<funcao>',argumentos:Array.prototype.map.call(row.querySelectorAll('.arg'),function(a){return {caminho:a.value||'<caminho>'}})}}}
  return {propriedade:row.querySelector('.prop').value||'<propriedade>',operador:op,valor:value(row)}}
 var kind=function(){return document.querySelector('input[name=rb-tipo]:checked').value};
 function show(){var k=kind();document.getElementById('rb-cond').style.display=k==='RP'?'none':'';
  document.getElementById('rb-restr').style.display=k==='RIC'?'none':'';document.getElementById('rb-concl').style.display=k==='RIC'?'':'none';
  var id=document.getElementById('rb-id');if(!id.dataset.touched)id.value=k+'-'}
 function rebuild(){var k=kind(),o;try{o=JSON.parse(t.value)}catch(x){o={operacoes:[{op:'adicionar_regra'}]}}
  var idv=document.getElementById('rb-id').value;if(!idv||idv===k+'-')idv=k+'-<ASSUNTO>';var r={id:idv,natureza:D.naturezas[k]};
  if(k!=='RP')r.condicao=Array.prototype.map.call(document.querySelectorAll('#rb-terms .term'),termJson);
  if(k==='RIC'){r.conclusao={tipo:document.getElementById('rb-ctipo').value,valor:document.getElementById('rb-cvalor').value||'<valor>'};
   r.mensagem=document.getElementById('rb-cmsg').value||'<o que se conclui e porquê>'}
  else{r.restricao=termJson(document.getElementById('rb-target'));r.restricao.mensagem=document.getElementById('rb-msg').value||'<o que falhou e o que se espera>'}
  o.operacoes[0]={op:'adicionar_regra',onde:D.onde,regra:r};t.value=JSON.stringify(o,null,1)}
 var n=0;function addTerm(){var row=document.createElement('div');row.className='term';row.dataset.list='rb-l'+(n++);row.dataset.removable='1';
  var dl=document.createElement('datalist');dl.id=row.dataset.list;document.body.appendChild(dl);
  document.getElementById('rb-terms').appendChild(row);term(row);rebuild()}
 document.getElementById('rb-add').addEventListener('click',addTerm);
 var target=document.getElementById('rb-target');var dl=document.createElement('datalist');dl.id=target.dataset.list;document.body.appendChild(dl);term(target);
 document.querySelectorAll('input[name=rb-tipo]').forEach(function(x){x.addEventListener('change',function(){show();rebuild()})});
 ['rb-msg','rb-cvalor','rb-cmsg','rb-ctipo'].forEach(function(i){document.getElementById(i).addEventListener('input',rebuild);document.getElementById(i).addEventListener('change',rebuild)});
 document.getElementById('rb-id').addEventListener('input',function(){this.dataset.touched=1;rebuild()});
 addTerm();show();rebuild()});
</script>"""


def _block(label, control, hint=""):
    """Like field(), but a div: the builder's controls are many per row (a label would forward clicks to the first one)."""
    h = f'<span class="hint">{e(hint)}</span>' if hint else ""
    return f'<div class="field"><span class="label">{e(label)}</span>{control}{h}</div>'


def _rule_builder(ds, selection, layer_id):
    """A form that builds the rule: where it lives, its type (RP, RIR or RIC), the condition terms and the restriction
    or the conclusion, with the properties reachable from the chosen model; the JSON below is filled in as it goes."""
    level, name = guides._split(selection.get("modelo"))
    paths = guides.model_paths(ds, level, name)
    functions = [{"nome": f["nome"], "parametros": f.get("parametros", [])} for f in guides.section_items(ds, "funcoes")]
    data = {"onde": {"nivel": level, "modelo": name}, "caminhos": paths, "funcoes": functions,
            "operadores": {k: {"simbolo": v["simbolo"], "forma": v["forma"]} for k, v in OPERATORS.items()},
            "naturezas": {k: n for k, n, _ in RULE_TYPES}}
    default = LAYER_RULE_TYPE.get(layer_id, "RIR")
    kinds = "<br>".join(f'<label><input type="radio" name="rb-tipo" value="{k}" autocomplete="off"{" checked" if k == default else ""}> {e(t)}</label>'
                        for k, _, t in RULE_TYPES)
    where = (f"<p>A regra vive em <b>{e(level)} {e(name)}</b> e pode usar as <b>{len(paths)}</b> propriedades a que este modelo chega pela sua composição"
             + (" (todas as do HLM)." if level == "HLM" else ". Para usar propriedades de outros modelos do documento, escolha acima o HLM que os contém.")
             + "</p>")
    body = (where + _block("Tipo de regra", f"<div>{kinds}</div>")
            + _block("Identificador", '<input id="rb-id" size="30" autocomplete="off">', "ex.: RIR-PAIS-EMAIL; único em todas as declarações")
            + '<div id="rb-cond">' + _block("Condição (todos os termos)", '<div id="rb-terms"></div><button type="button" id="rb-add">+ termo</button>',
                                           "quando se aplica: os fatores discriminantes e os seus valores") + "</div>"
            + '<div id="rb-restr">' + _block("Restrição", '<div class="term" id="rb-target" data-list="rb-ltarget"></div>',
                                            "a propriedade que é restringida e como; uma função quando a verificação não é tipificada")
            + _block("Mensagem", '<input id="rb-msg" size="80" autocomplete="off">', "o que falhou e o que se espera") + "</div>"
            + '<div id="rb-concl" style="display:none">'
            + _block("Conclusão", '<select id="rb-ctipo"><option>ACAO</option><option>ESTADO</option></select> <input id="rb-cvalor" size="30" placeholder="valor, ex.: MANUTENCAO">',
                    "uma RIC não restringe: informa uma ação ou um estado quando a condição se verifica")
            + _block("Mensagem", '<input id="rb-cmsg" size="80" autocomplete="off">') + "</div>")
    payload = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    script = f'<script type="application/json" id="rb-data">{payload}</script>'
    return section("Construir a regra", body) + script + RULE_JS


# ---------------------------------------------------------------------- what exists in the layer
def _edit(layer_id, op, text="alterar", **selection):
    return f'<a href="{url("/alteracoes", camada=layer_id, op=op, **selection)}">{e(text)}</a>'


def _rule_text(rule):
    r = rule.get("restricao") or {}
    cond = " e ".join(f'{t.get("propriedade") or t.get("contexto") or "função"} {t.get("operador")} {json.dumps(t.get("valor"), ensure_ascii=False)}'
                      for t in rule.get("condicao") or [])
    restriction = (f'{r.get("propriedade") or (r.get("chamada") or {}).get("funcao")} {r.get("operador")} '
                   f'{json.dumps(r.get("valor"), ensure_ascii=False) if "valor" in r else ""}') if r else ""
    return (f"se {cond} → " if cond else "") + restriction


def _existing(app, ds, layer_id):
    if layer_id == "A":
        rows = []
        for level in guides.LEVELS:
            for m in guides.section_items(ds, level.lower()):
                key = f"{level}:{m['nome']}"
                props = " ".join(_edit("A", "alterar_propriedade", p["nome"], modelo=key, propriedade=p["nome"]) for p in m.get("propriedades", []))
                rows.append([f'<span class="tag {level}">{level}</span><a href="/vistas/{e(L.model_page(level, m["nome"]))}.html">{e(m["nome"])}</a>',
                             props or "—", _edit("A", "alterar_modelo", "alterar", modelo=key) + " · " + _edit("A", "adicionar_propriedade", "+ propriedade", modelo=key)])
        return table(["Modelo", "Propriedades (clicar para alterar)", ""], rows)
    if layer_id == "B":
        rows = [[f'<code>{e(x["nome"])}</code>', e(x.get("hlm")), str(len(x.get("obrigatorias", []))), str(len(x.get("permitidas", []))),
                 _edit("B", "definir_projecao", "alterar", hlm=x.get("hlm"), projecao=x["nome"])] for x in guides.section_items(ds, "projecoes")]
        rows += [["", e(h), "", "", _edit("B", "definir_projecao", "+ nova projeção", hlm=h)] for h in ds.declarations]
        return table(["Projeção", "HLM", "Obrigatórias", "Permitidas", ""], rows)
    if layer_id in ("C", "D"):
        rows = [[f'<a href="/vistas/{e(L.rule_page(r["id"]))}.html">{e(r["id"])}</a>', e(f"{lv} {m}{'.' + p if p else ''}"),
                 f"<code>{e(_rule_text(r))}</code>", _edit(layer_id, "substituir_regra", "alterar", regra=r["id"])]
                for r, lv, m, p in guides.rules(ds, RULE_KINDS[layer_id])]
        return f"<p>{len(rows)} regra(s).</p>" + table(["Regra", "Vive em", "Condição → restrição", ""], rows)
    if layer_id == "E":
        rows = [[f'<code>{e(c["nome"])}</code>', e(c.get("tipo")), e(c.get("descricao")), _edit("E", "definir_contexto", "alterar", contexto=c["nome"])]
                for c in guides.section_items(ds, "contextosExternos")]
        return (functions_tab.functions_table(app)
                + "<h3>Contextos externos</h3>" + (table(["Contexto", "Tipo", "Descrição", ""], rows) if rows else '<p class="note">Nenhum.</p>'))
    if layer_id == "F":
        rows = [[f'<a href="/vistas/{e(L.profile_page(x["nome"]))}.html">{e(x["nome"])}</a>', e(x.get("projecao")),
                 e("; ".join(f'{f.get("propriedade") or "contexto " + str(f.get("contexto"))} = {f.get("valor")}' for f in x.get("fixa", []))),
                 _edit("F", "definir_perfil", "alterar", projecao=x.get("projecao"), perfil=x["nome"])] for x in guides.section_items(ds, "perfis")]
        return table(["Perfil", "Projeção", "Valores fixados", ""], rows)
    return ""


# ---------------------------------------------------------------------- pages
def _layer_page(app, request, values, result="", notice=None, kind="ok"):
    domain = app.require_domain()
    layer_id = values.get("camada") or "A"
    op = values.get("op")
    selection = {k: values.get(k) for k in SELECTION_KEYS if values.get(k)}
    layer = step(layer_id)
    body = message(notice or values.get("aviso"), kind) + _layer_tabs(layer_id)
    if not domain.declaration_files():
        return body + message("Ainda não há declarações: a geração (separador Declaração) cria-as.", "warn")
    ds = DeclarationSet.load(domain.folder)
    body += keyvalues([("Camada", e(layer["camada"])), ("Estado", state(domain.step_state(layer_id))),
                       ("Verificação", button_form("/declaracao/verificar", "Verificar a camada", {"passo": layer_id, "voltar": url("/alteracoes", camada=layer_id)})
                        + button_form("/declaracao/aceitar", "Aceitar a camada", {"passo": layer_id, "voltar": url("/alteracoes", camada=layer_id)}))])
    body += result
    body += section("Operações desta camada", _operations_list(layer_id, op, selection))
    if op:
        body += section(f"Operação {op}", _guided_form(app, ds, layer_id, op, selection))
    body += section("O que existe nesta camada", _existing(app, ds, layer_id))
    requests = [r for r in RequestQueue.for_domain(domain).requests() if r.kind == "alteracao" and r.step == layer_id]
    if requests:
        body += section("Pedidos de alterações desta camada", table(["Pedido", "Pedido em linguagem natural", "Estado", "Resultado"],
                        [[f'<a href="/pedidos/{e(domain.id)}/{e(r.id)}">{e(r.id)}</a>', e(r.meta.get("pedido", r.title)[:160]), state(r.state),
                          e(r.meta.get("resumo") or "")] for r in reversed(requests)]))
    body += _where_box([("Declarações (os ficheiros alterados)", _code(f"dominios/{domain.id}/declaracoes/*.ecv.json")),
                        ("Mapeamento", _code(f"dominios/{domain.id}/mapeamento.json")),
                        ("Operação escolhida", _handler_location(op) if op else "—"),
                        ("Vocabulário de operações", _code("ecv/2_amendments/operations.json")),
                        ("Motor (lote tudo ou nada)", _code("ecv/2_amendments/engine.py") + " · <code>apply_operations</code>"),
                        ("Formulários guiados", _code("ecv/2_amendments/guides.py")),
                        ("Prompt do pedido em linguagem natural", _code("ecv/2_amendments/prompts/alteracao_focada.md")),
                        ("Pedidos ao LLM", _code(f"dominios/{domain.id}/pedidos/")),
                        ("Camadas (operações e verificações)", _code("ecv/1_ecv_builder/build_process.json"))])
    return Response.html(layout.page(app, "alteracoes", f"Alterações · {domain.name}", body, request.path,
                                     "Revisão das declarações por camadas: escolher a operação e o que existe, ver o contexto, aplicar."))


def _csv_page(app, request, values, result="", notice=None, kind="ok"):
    domain = app.require_domain()
    operators = [(k, k) for k in OPERATORS if k in ("PATTERN", "EQUALS", "IN", "RANGE", "NOT_EQUALS")]
    model_options = [("", "— escolher —")] + (guides.options(DeclarationSet.load(domain.folder), "modelo", {}) if domain.declaration_files() else [])
    body = message(notice, kind) + _layer_tabs("csv") + result
    body += ("<p>Uma tabela de mapeamentos conhecidos (por exemplo, os códigos postais de cada freguesia) passa a uma RIR por linha. "
             "As colunas são caminhos relativos ao modelo onde as regras vivem; a coluna alvo é a restrição e as restantes são os termos da condição. "
             "Ficheiro de teste: <code>dados_teste/codigos_postais_lisboa.csv</code> (modelo <code>USM:Morada</code>, alvo <code>codigoPostal</code>, operador PATTERN).</p>"
             '<form method="post" action="/alteracoes/csv">'
             + field("Tabela (CSV)", textarea("tabela", values.get("tabela", ""), 10, "localidade;freguesia;codigoPostal\nLISBOA;AJUDA;^1300-[0-9]{3}$"),
                     "separador ; ou , · colunas opcionais: id, mensagem")
             + field("Modelo", select("modelo", model_options, values.get("modelo")), "onde as regras vivem")
             + field("Propriedade", f'<input name="propriedade" value="{e(values.get("propriedade", ""))}">', "opcional")
             + field("Coluna alvo", f'<input name="alvo" value="{e(values.get("alvo", ""))}" placeholder="codigoPostal">')
             + field("Operador", select("operador", operators, values.get("operador", "PATTERN")))
             + field("Prefixo dos ids", f'<input name="prefixo" value="{e(values.get("prefixo", "RIR-CP"))}">')
             + field("Mensagem", f'<input name="mensagem" size="80" value="{e(values.get("mensagem", ""))}">', "opcional: {alvo}, {condicao} e os nomes das colunas")
             + '<p><button name="acao" value="previsualizar">Gerar operações</button> <button name="acao" value="aplicar" class="primary">Gerar e aplicar</button></p></form>')
    body += _where_box([("Conversão da tabela em operações", _code("ecv/2_amendments/csv_rules.py") + " · <code>operations_from_csv</code>"),
                        ("Declarações alteradas", _code(f"dominios/{domain.id}/declaracoes/*.ecv.json"))])
    return Response.html(layout.page(app, "alteracoes", f"Alterações · {domain.name}", body, request.path, "Tabela CSV de mapeamentos conhecidos."))


def _vocabulary_page(app, request):
    v = vocabulary()
    layer_of = {op: x["id"] for x in layers() for op in x.get("alteracoes", [])}
    rows = [[e(layer_of.get(k, "—")), f"<code>{e(k)}</code>", e(", ".join(d["campos"])), e(d["descricao"]), _handler_location(k)] for k, d in v["operacoes"].items()]
    body = _layer_tabs("vocabulario") + table(["Camada", "Operação", "Campos", "O que faz", "Implementação"], rows)
    return Response.html(layout.page(app, "alteracoes", "Alterações · vocabulário", body, request.path, "As operações e onde estão implementadas."))


def page(app, request):
    values = dict(request.query)
    if values.get("camada") == "csv" or values.get("modo") == "csv":
        return _csv_page(app, request, values)
    if values.get("camada") == "vocabulario" or values.get("modo") == "vocabulario":
        return _vocabulary_page(app, request)
    values.setdefault("camada", values.get("passo") or "A")
    return _layer_page(app, request, values)


def _state(form):
    return dict(urllib.parse.parse_qsl(form.get("estado", "")))


def natural_language(app, request):
    domain = app.require_domain()
    form = request.form()
    values = {**_state(form), **{k: v for k, v in form.items() if k in ("texto", "informacao")}}
    if not form.get("texto", "").strip():
        return _layer_page(app, request, values, notice="Escreva o pedido.", kind="warn")
    selection = {k: form[k] for k in SELECTION_KEYS if form.get(k)}
    r = ecv_builder.request_changes(domain, form["texto"], form.get("passo"), form.get("informacao", ""), selection)
    app.log.event(f"{domain.id}: pedido de alterações {r.id} criado (contexto: {', '.join(selection) or 'nenhum'})")
    return Response.redirect(f"/pedidos/{domain.id}/{r.id}", note=r.id)


def _result_block(done, check, applied):
    title = "Aplicadas" if applied else "Pré-visualização (nada foi gravado)"
    out = section(f"{title}: {len(done)} operação(ões)", pre("\n".join(done)))
    if check is not None:
        out += section("Verificação", pre(check.text()))
    return out


def _apply(app, domain, operations, step_id, apply_):
    done, check = ecv_builder.apply_operations_to_domain(domain, operations, step_id, save=apply_)
    if apply_:
        app.log.event(f"{domain.id}: {len(done)} operação(ões) aplicadas na camada {step_id}: {check.summary()}")
    return done, check


def operations(app, request):
    domain = app.require_domain()
    form = request.form()
    values = _state(form)
    apply_ = form.get("acao") == "aplicar"
    try:
        ops = parse_operations(json.loads(form.get("operacoes") or "[]"))
        done, check = _apply(app, domain, ops, form.get("passo"), apply_)
    except (EcvError, ValueError) as err:
        return _layer_page(app, request, values, notice=f"Não aplicadas: {err}", kind="error")
    return _layer_page(app, request, values, _result_block(done, check, apply_), notice="Operações aplicadas e gravadas." if apply_ else None)


def csv_table(app, request):
    domain = app.require_domain()
    form = request.form()
    apply_ = form.get("acao") == "aplicar"
    kwargs = {"message": form["mensagem"]} if form.get("mensagem") else {}
    level, _, model = (form.get("modelo") or "").partition(":")
    try:
        ops = operations_from_csv(form.get("tabela", ""), level, model, form["alvo"].strip(), form["operador"],
                                  form.get("prefixo") or "RIR-", prop=form.get("propriedade") or None, **kwargs)
        done, check = _apply(app, domain, ops, "D", apply_)
    except (EcvError, ValueError, KeyError) as err:
        return _csv_page(app, request, form, notice=f"Não aplicadas: {err}", kind="error")
    generated = section(f"Operações geradas ({len(ops)})", pre(json.dumps({"operacoes": ops}, ensure_ascii=False, indent=1)))
    return _csv_page(app, request, form, generated + _result_block(done, check, apply_),
                     notice=f"{len(ops)} regra(s) acrescentadas." if apply_ else None)


def vocabulary_api(app, request):
    return Response.json(vocabulary())


def operations_api(app, request):
    domain = app.require_domain()
    data = request.json()
    done, check = _apply(app, domain, parse_operations(data), data.get("passo"), bool(data.get("aplicar", True)))
    return Response.json({"feitas": done, "aplicadas": check is not None, "verificacao": check.to_dict() if check else None})
