"""Instâncias de teste (module 6): instances of a HLM created from the model's structure and a profile.

    choose      the scenario (profile or HLM) and what the instance should test
    skeleton    the instance with every available path, a placeholder per base type and the profile's fixed values
    request     a short prompt to the LLM with only that context (structure, rules, contexts, skeleton)
    save        the instance (edited here or answered by the LLM) in dominios/<d>/instancias/
    validate    each saved instance, with the result of module 6
"""
import json

from ecv.shared.errors import EcvError
from ecv.validation import test_instances as T
from ecv.views.presentation import render_body

from ..http import Response, url
from ..pages import layout
from ..pages.components import button_form, e, field, message, section, select, table, textarea
from .validation import _scenarios


def _scenario_of(value):
    kind, _, name = (value or "").partition(":")
    return (name, None) if kind == "perfil" else (None, name)


def _where_box():
    rows = [("O esqueleto, o prompt, gravar e validar", "<code>ecv/6_validation/test_instances.py</code>"),
            ("O modelo do prompt", "<code>ecv/6_validation/prompts/instancia_teste.md</code>"),
            ("O cenário (perfil, projeção, valores fixados, contextos)", "<code>ecv/6_validation/scenario.py</code>"),
            ("O motor de validação", "<code>ecv/6_validation/engine.py</code>"),
            ("As instâncias gravadas", "<code>dominios/&lt;d&gt;/instancias/&lt;nome&gt;.json</code>"),
            ("Os pedidos ao LLM", "<code>dominios/&lt;d&gt;/pedidos/&lt;id&gt;/</code> (tipo instancia)"),
            ("Esta página", "<code>ecv/7_webapp/handlers/instances.py</code>")]
    return section("Onde está, no código e nos ficheiros", table(["O quê", "Onde"], [[e(a), b] for a, b in rows]))


def page(app, request, values=None, notice=None, kind="ok"):
    domain = app.require_domain()
    g = app.graph
    values = values or {}
    scenario = values.get("cenario") or request.get("cenario") or ""
    scenarios = _scenarios(g)
    body = message(notice or request.get("aviso"), request.get("tipo", kind))
    if not scenarios:
        body += message("O âmbito ativo não tem HLM: gere as declarações (Declaração › 2. Geração) e escolha o domínio no seletor de âmbito.", "info")
        return Response.html(layout.page(app, "instancias", "Instâncias de teste", body + _where_box(), request.path))
    scenario = scenario or scenarios[0][0]
    instance_text = values.get("instancia") or json.dumps(T.skeleton(g, *_scenario_of(scenario)), ensure_ascii=False, indent=1)
    body += section("1. Cenário e o que testar",
                    '<form method="get" action="/instancias">'
                    + field("Cenário", select("cenario", scenarios, scenario).replace("<select ", '<select onchange="this.form.submit()" ', 1)
                            + " <button>Esqueleto deste cenário</button>",
                            "ao mudar o cenário, o esqueleto e os pedidos abaixo passam a usá-lo; o perfil dá a projeção e os valores fixados")
                    + "</form>")
    body += f'<p>Cenário em uso: <b>{e(dict(scenarios).get(scenario, scenario))}</b></p>'
    body += section("2. Pedir a instância ao LLM",
                    '<form method="post" action="/instancias/pedido">'
                    f'<input type="hidden" name="cenario" value="{e(scenario)}">'
                    + field("O que a instância deve testar", textarea("pedido", values.get("pedido", ""), 3,
                            "ex.: uma fatura válida com duas linhas; ou: uma fatura em que o NIF do adquirente falta e a data é futura"))
                    + field("Nome", f'<input name="nome" size="40" value="{e(values.get("nome", ""))}">', "nome do ficheiro em instancias/")
                    + '<p><button class="primary">Criar o pedido</button> <span class="note">o prompt leva só a estrutura do cenário, '
                      'as regras que se aplicam, os contextos e o esqueleto</span></p></form>')
    body += section("3. Ou escrever a instância aqui (começa no esqueleto)",
                    '<form method="post" action="/instancias/gravar">'
                    f'<input type="hidden" name="cenario" value="{e(scenario)}">'
                    + field("Nome", f'<input name="nome" size="40" value="{e(values.get("nome", ""))}">')
                    + field("Instância de teste (JSON)", textarea("instancia", instance_text, 22))
                    + '<p><button name="acao" value="validar">Validar</button> <button class="primary" name="acao" value="gravar">Gravar e validar</button></p></form>')
    saved = T.saved(domain)
    if saved:
        rows = [[e(n), e(x.get("perfil") or x.get("hlm")), e(x.get("descricao")),
                 button_form("/instancias/validar", "Validar", {"nome": n})] for n, x in saved.items()]
        body += section(f"Instâncias gravadas ({len(saved)})", table(["Nome", "Cenário", "Descrição", ""], rows))
    body += _where_box()
    return Response.html(layout.page(app, "instancias", f"Instâncias de teste · {domain.name}", body, request.path,
                                     "Módulo 6: instâncias criadas a partir da estrutura do modelo e do perfil, gravadas e validadas."))


def _result(app, request, vm):
    body = f'<p class="note"><a href="/instancias">← instâncias de teste</a></p>' + render_body(vm)
    return Response.html(layout.page(app, "instancias", vm["titulo"], body, request.path))


def request_instance(app, request):
    domain = app.require_domain()
    form = request.form()
    profile, hlm = _scenario_of(form.get("cenario"))
    r = T.request_instance(domain, app.graph, profile, hlm, form.get("pedido", ""), form.get("nome") or None)
    app.log.event(f"{domain.id}: pedido {r.id} criado (instância de teste)")
    return Response.redirect(f"/pedidos/{domain.id}/{r.id}", note=r.id)


def save(app, request):
    domain = app.require_domain()
    form = request.form()
    profile, hlm = _scenario_of(form.get("cenario"))
    try:
        data = json.loads(form.get("instancia") or "null")
        example = data if isinstance(data, dict) and "instancia" in data else {"instancia": data}
        example.setdefault("perfil" if profile else "hlm", profile or hlm)
        vm = T.validate_saved(app.graph, example, form.get("nome") or None)
        if form.get("acao") == "gravar":
            target = T.save_instance(domain, form.get("nome") or T.instance_name(example.get("descricao")), example)
            app.log.event(f"{domain.id}: instância {target.name} gravada")
    except (ValueError, EcvError) as err:
        return page(app, request, form, f"Não gravada: {err}", "error")
    return _result(app, request, vm)


def validate(app, request):
    domain = app.require_domain()
    name = request.form()["nome"]
    example = T.saved(domain)[name]
    return _result(app, request, T.validate_saved(app.graph, example, name))
