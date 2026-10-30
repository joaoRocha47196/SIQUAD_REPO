"""Validação (module 6): an instance of a HLM evaluated against the rules of the active graph, in the scenario
of a profile (or of the HLM alone, with every rule)."""
import json

from ecv import validation
from ecv.validation import test_instances
from ecv.views.presentation import render_body

from ..http import Response, bad_request
from ..pages import layout
from ..pages.components import e, field, message, section, select, table, textarea, where_box

FILL_JS = """<script>
(function(){var ex=JSON.parse(document.getElementById('exemplos').textContent);
 var sel=document.getElementById('exemplo'),cen=document.getElementById('cenario');
 function key(x){return x.perfil?'perfil:'+x.perfil:'hlm:'+x.hlm}
 function filter(){Array.prototype.forEach.call(sel.options,function(o){if(o.value)o.hidden=key(ex[o.value])!==cen.value});
  var n=Array.prototype.filter.call(sel.options,function(o){return o.value&&!o.hidden}).length;
  document.getElementById('nexemplos').textContent=n+' instância(s) neste cenário'}
 sel.addEventListener('change',function(){var x=ex[this.value];if(!x)return;
  cen.value=key(x);filter();
  document.getElementById('instancia').value=JSON.stringify(x.instancia,null,2);
  document.getElementById('contextos').value=JSON.stringify(x.contextos||{},null,2);});
 cen.addEventListener('change',function(){sel.value='';filter()});filter();})();
</script>"""


def _examples(app):
    """The example instances (module 6) and the active domain's test instances (Instâncias), whose profile (or HLM)
    exists in the graph. The domain's ones are named 'teste: <name>'."""
    g = app.graph
    found = dict(validation.examples())
    if app.domain is not None:
        found.update({f"teste: {n}": x for n, x in test_instances.saved(app.domain).items()})
    return {n: x for n, x in found.items()
            if (x.get("perfil") and g.node("Perfil", x["perfil"]) is not None) or (x.get("hlm") and g.node("HLM", x["hlm"]) is not None)}


def _scenarios(g):
    out = []
    for p in sorted(g.nodes("Perfil"), key=lambda x: x["nome"]):
        projection = g.first_target(p, "USA")
        hlm = g.first_target(projection, "PROJETA") if projection else None
        out.append((f"perfil:{p['nome']}", f"perfil {p['nome']} ({hlm['nome'] if hlm else '?'})"))
    out += [(f"hlm:{h['nome']}", f"HLM {h['nome']} (sem perfil: todas as regras)") for h in sorted(g.nodes("HLM"), key=lambda x: x["nome"])]
    return out


def page(app, request, values=None, notice=None):
    g = app.graph
    values = values or {}
    examples = _examples(app)
    contexts = ", ".join(sorted(c["nome"] for c in g.nodes("ContextoExterno")))
    body = message(notice, "error")
    body += ('<form method="post" action="/validacao">'
             + field("Exemplo", select("", [("", "—")] + [(n, n) for n in examples], ident="exemplo"), "os exemplos do módulo 6 e as instâncias de teste do domínio (teste: …), filtrados pelo cenário")
             + '<p class="note" id="nexemplos"></p>'
             + field("Cenário", select("cenario", _scenarios(g), values.get("cenario"), ident="cenario"))
             + field("Contextos externos (JSON)", textarea("contextos", values.get("contextos", "{}"), 4, contexts, ident="contextos"))
             + field("Instância (JSON)", textarea("instancia", values.get("instancia", ""), 16, ident="instancia"))
             + '<p><button class="primary">Validar</button></p></form>')
    if examples:
        body += section("Instâncias de exemplo e de teste", table(["Instância", "Cenário", "Descrição"],
                        [[f'<a href="/vistas/validacao_{e(n)}.html">{e(n)}</a>' if not n.startswith("teste: ") else f'<a href="/instancias">{e(n)}</a>',
                          e(x.get("perfil") or x.get("hlm")), e(x.get("descricao"))] for n, x in examples.items()]))
    data = json.dumps(examples, ensure_ascii=False).replace("</", "<\\/")
    body += f'<script type="application/json" id="exemplos">{data}</script>' + FILL_JS
    body += where_box([('O motor (cenário → estrutura → regras)', 'ecv/6_validation/engine.py'), ('O cenário do perfil', 'ecv/6_validation/scenario.py'), ('A avaliação das regras', 'ecv/6_validation/rules.py'), ('As implementações das funções', 'ecv/6_validation/functions/'), ('As instâncias de exemplo', 'ecv/6_validation/examples/'), ('As instâncias de teste do domínio', 'dominios/<d>/instancias/'), ('Esta página', 'ecv/7_webapp/handlers/validation.py')])
    return Response.html(layout.page(app, "validacao", "Validação de uma instância", body, request.path,
                                     "Módulo 6: estrutura da instância e estado de cada regra em cada ocorrência, no cenário do perfil."))


def _validate(app, data):
    if data.get("exemplo"):
        return validation.validate_example(app.graph, data["exemplo"], data.get("contextos"))
    instance = data.get("instancia")
    if not isinstance(instance, dict):
        raise bad_request("a instância tem de ser um objeto JSON")
    return validation.validate(app.graph, instance, profile=data.get("perfil"), hlm=data.get("hlm"),
                               contexts=data.get("contextos") or {}, name=data.get("nome"))


def run(app, request):
    form = request.form()
    try:
        kind, _, name = form.get("cenario", "").partition(":")
        data = {"instancia": json.loads(form.get("instancia") or "null"), "contextos": json.loads(form.get("contextos") or "{}"),
                ("perfil" if kind == "perfil" else "hlm"): name}
        vm = _validate(app, data)
    except ValueError as err:
        return page(app, request, form, f"Não validada: {err}")
    app.log.event(f"validação: {form.get('cenario')}")
    body = '<p class="note"><a href="/validacao">← nova validação</a></p>' + render_body(vm)
    return Response.html(layout.page(app, "validacao", vm["titulo"], body, request.path))


def api(app, request):
    return Response.json(_validate(app, request.json()))
