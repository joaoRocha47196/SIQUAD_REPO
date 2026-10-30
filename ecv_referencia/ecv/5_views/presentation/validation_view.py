"""View of the result of validating an instance (ViewModel 'validacao')."""
import json

from .. import links as L
from .html import chip, e, table, value_text

STATE_CLASS = {"não conforme": "b-nonconforming", "conforme": "b-conforming", "conclusão": "b-conclusion",
               "não aplicável": "b-not-applicable", "sem valor": "b-no-value", "não avaliável": "b-not-evaluable",
               "fora da projeção": "b-outside", "ausente": "b-absent", "verdadeiro": "b-true", "falso": "b-false"}
ORDER = ["não conforme", "conclusão", "não avaliável", "sem valor", "conforme", "não aplicável", "ausente", "fora da projeção"]
SHOWN_BY_DEFAULT = {"não conforme", "conclusão", "não avaliável", "sem valor"}


def _badge(state):
    return f'<span class="badge {STATE_CLASS.get(state, "")}">{e(state)}</span>'


def _value(v):
    return json.dumps(v, ensure_ascii=False) if isinstance(v, dict) else value_text(v)


def _slug(state):
    return STATE_CLASS.get(state, "b-x")[2:]


def _terms(row):
    return "<br>".join(f'{_badge(t["resultado"]) if t["resultado"] in STATE_CLASS else e(t["resultado"])} {e(t["texto"])}'
                       + (f' <span class="note">= {e(value_text(t["valor"]))}</span>' if t.get("valor") is not None else "")
                       for t in row.get("termos") or []) or '<span class="note">sem condição</span>'


def _scenario_box(vm):
    profile = L.link(L.profile_page(vm["perfil"]), vm["perfil"]) if vm.get("perfil") else "—"
    fixed = "<br>".join(f'<code>{e(f["caminho"])}</code> = {e(value_text(f["valor"]))}' for f in vm["fixados"]) or "—"
    contexts = "<br>".join(f'<b>{e(c["nome"])}</b> = <code>{e(_value(c["valor"]))}</code> <span class="note">({e(c["origem"])})</span>'
                           if c["valor"] is not None else f'<b>{e(c["nome"])}</b> <span class="badge b-not-evaluable">em falta</span>'
                           for c in vm["contextos"]) or "—"
    fields = ""
    if vm.get("instancia"):
        fields += f'<span class="key">Instância</span><span>{e(vm["instancia"])}</span>'
    if vm.get("descricaoInstancia"):
        fields += f'<span class="key">Descrição</span><span>{e(vm["descricaoInstancia"])}</span>'
    fields += (f'<span class="key">HLM</span><span>{L.link(L.model_page("HLM", vm["hlm"]), vm["hlm"])}</span>'
               f'<span class="key">Perfil</span><span>{profile}</span>'
               f'<span class="key">Projeção</span><span>{e(vm.get("projecao") or "— (todas as propriedades)")}</span>'
               f'<span class="key">Valores fixados pelo perfil</span><span>{fixed}</span>'
               f'<span class="key">Contextos externos</span><span>{contexts}</span>')
    return f'<div class="box"><div class="fields">{fields}</div></div>'


def _structure(vm):
    out = "<h2>Estrutura</h2>"
    if not vm["estrutura"]:
        return out + '<p class="ok">Sem problemas estruturais.</p>'
    out += "<p>" + " ".join(f'<span class="badge b-nonconforming">{e(k)}</span> {v}' for k, v in vm["resumoEstrutura"].items()) + "</p>"
    return out + table(["Problema", "Caminho", "Detalhe"],
                       [[f'<span class="badge b-nonconforming">{e(p["tipo"])}</span>', f'<code>{e(p["caminho"])}</code>', e(p["problema"])]
                        for p in vm["estrutura"]])


def _conclusions(vm):
    if not vm["conclusoes"]:
        return ""
    return "<h2>Conclusões</h2>" + table(
        ["Regra", "Ocorrência", "Conclusão", "Mensagem"],
        [[chip("RIC", c["regra"], c.get("descricao"), L.href(L.rule_page(c["regra"]))), f'<code>{e(c["ocorrencia"])}</code>',
          e(f'{(c.get("conclusao") or {}).get("tipo") or ""} {(c.get("conclusao") or {}).get("valor") or ""}'.strip()), e(c.get("mensagem"))]
         for c in vm["conclusoes"]])


def _rules(vm):
    present = [s for s in ORDER if vm["resumo"].get(s)]
    selector = "".join(f'<label><input type="checkbox" data-off="hide-{_slug(s)}"{" checked" if s in SHOWN_BY_DEFAULT else ""}> '
                       f'{_badge(s)} {vm["resumo"][s]}</label> ' for s in present)
    style = "".join(f"body.hide-{_slug(s)} .state-{_slug(s)}{{display:none}}" for s in present)
    out = f'<h2>Regras</h2><style>{style}</style><p class="toolbar">{selector}</p>'
    for state in present:
        rows = []
        for r in (x for x in vm["regras"] if x["estado"] == state):
            detail = e(r.get("detalhe"))
            if r.get("valor") is not None:
                detail += f'<br><span class="note">valor: <code>{e(value_text(r["valor"]))}</code></span>'
            if r.get("mensagem"):
                detail += f'<br><b>{e(r["mensagem"])}</b>'
            rows.append([chip(r["tipo"], r["regra"], r.get("descricao"), L.href(L.rule_page(r["regra"]))),
                         f'<code>{e(r["ocorrencia"])}</code>', e(r.get("descricao")), _terms(r), detail])
        out += (f'<div class="state-{_slug(state)}"><h3>{_badge(state)} {len(rows)}</h3>'
                + table(["Regra", "Ocorrência", "Regra declarada", "Termos da condição", "Resultado"], rows) + "</div>")
    return out


def validation(vm):
    result = "valid" if vm["valida"] else "invalid"
    body = f'<p><span class="result {result}">{"Instância válida" if vm["valida"] else "Instância inválida"}</span></p>'
    body += _scenario_box(vm) + _structure(vm) + _conclusions(vm) + _rules(vm)
    body += ('<details><summary><b>Instância avaliada</b> (com os valores fixados pelo perfil)</summary>'
             f'<pre class="json">{e(json.dumps(vm["instanciaAvaliada"], ensure_ascii=False, indent=2))}</pre></details>')
    return body
