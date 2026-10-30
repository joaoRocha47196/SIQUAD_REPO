"""Views of projections, profile, profile candidates, gaps and operators."""
from .. import links as L
from .html import chip, e, table, value_text

STATE_CLASS = {"sempre aplicável": "b-always", "nunca aplicável": "b-never", "dinâmica": "b-dynamic",
               "não avaliável": "b-not-evaluable", "alvo fora da projeção": "b-outside", "avaliada": "b-always",
               "fora da projeção": "b-outside", "verdadeiro": "b-true", "falso": "b-false",
               "dinâmico": "b-dynamic", "indisponível": "b-unavailable"}
PROFILE_STATE_ORDER = ["sempre aplicável", "dinâmica", "não avaliável", "nunca aplicável", "alvo fora da projeção", "avaliada",
                       "fora da projeção"]


def badge(state):
    return f'<span class="badge {STATE_CLASS.get(state, "")}">{e(state)}</span>'


def _fixed_text(f):
    if "caminho" in f:
        return (f'<code>{e(f["caminho"])}</code> = {e(value_text(f["valor"]))}'
                + ("" if f.get("projetada") else ' <span class="note">(não projetada: valor conhecido)</span>'))
    return f'contexto <b>{e(f["contexto"])}</b> = {e(value_text(f["valor"]))}'


def projections(vm):
    names = [p["nome"] for p in vm["projecoes"]]
    mark = {"O": '<span class="mandatory">obrigatória</span>', "P": '<span class="permitted">permitida</span>', "-": '<span class="excluded">—</span>'}
    head = "".join(f"<th>{e(n)}</th>" for n in names)
    rows = "".join(f'<tr class="{"differs" if r["difere"] else ""}"><td class="row-label"><code>{e(r["caminho"])}</code></td>'
                   + "".join(f"<td>{mark[r['celulas'][n]]}</td>" for n in names) + "</tr>" for r in vm["linhas"])
    body = (f'<table class="matrix"><thead><tr><th class="row-label">Propriedade</th>{head}</tr></thead><tbody>{rows}</tbody></table>'
            '<div class="legend">Sombreado: propriedades em que as projeções diferem. — : excluída (proibida) nessa projeção.</div>')
    body += "<h2>Projeções</h2>" + table(["Projeção", "Descrição"], [[e(p["nome"]), e(p["descricao"])] for p in vm["projecoes"]])
    if vm["perfis"]:
        rows = [[L.link(L.profile_page(p["perfil"]), p["perfil"]), e(p["projecao"]), e(p["descricao"]),
                 "<br>".join(_fixed_text(f) for f in p["fixa"]) or '<span class="note">nenhum valor fixado (seleção dinâmica)</span>']
                for p in vm["perfis"]]
        body += "<h2>Perfis de execução e valores fixados</h2>" + table(["Perfil", "Projeção", "Descrição", "Fixa"], rows)
    return body


def gaps(vm):
    body = "<h2>Propriedades sem regras</h2>"
    if vm["semRegras"]:
        body += "<p>" + " ".join(
            L.property_link(p["propriedade"], f'{p["dono"]}.{p["nome"]}')
            + (f' <span class="note">(só lida em termos de {e(", ".join(p["lidaEmTermos"]))})</span>' if p["lidaEmTermos"] else "")
            for p in vm["semRegras"]) + "</p>"
    else:
        body += '<p class="ok">Todas as propriedades têm regras.</p>'
    body += f'<h2>Propriedades nunca projetadas</h2><p class="note">Projeções consideradas: {e(", ".join(vm["projecoesConsideradas"]))}</p>'
    body += ("<p>" + " ".join(f'<span class="chip neutral" style="border-style:dashed">{e(p["caminho"])}</span>'
                              for p in vm["nuncaProjetadas"]) + "</p>") if vm["nuncaProjetadas"] else \
        '<p class="ok">Todas as propriedades são usadas por pelo menos uma projeção.</p>'
    return body


def operators(vm):
    body = "<h2>Propriedades tratadas como enumerados (RP com IN)</h2>"
    body += table(["Propriedade", "Valores plausíveis"], [[L.property_link(x["propriedade"]), e(", ".join(map(str, x["valores"])))]
                                                         for x in vm["enumerados"]])
    for op in vm["operadores"]:
        body += f'<h2>{e(op["operador"])} <span class="note">({len(op["restricoes"])} restrições, {len(op["termos"])} termos)</span></h2>'
        if op["restricoes"]:
            body += "<h3>Restrições</h3><ul>" + "".join(f'<li>{L.link(L.rule_page(x["regra"]), x["regra"])}: <code>{e(x["texto"])}</code></li>'
                                                       for x in op["restricoes"]) + "</ul>"
        if op["termos"]:
            body += "<h3>Termos de condições</h3><ul>" + "".join(f'<li>{L.link(L.rule_page(x["regra"]), x["regra"])}: <code>{e(x["texto"])}</code></li>'
                                                                for x in op["termos"]) + "</ul>"
    return body


def profile(vm):
    fixed = "<br>".join(f'<code>{e(f["caminho"])}</code> = {e(value_text(f["valor"]))}'
                        + ("" if f["projetada"] else ' <span class="note">(não projetada)</span>') for f in vm["fixados"]) or "—"
    contexts = "<br>".join(f'<b>{e(c["nome"])}</b> = {e(value_text(c["valor"]))}' for c in vm["contextos"]) or "— (obtidos pelo motor)"
    body = (f'<div class="box"><div class="fields"><span class="key">Projeção</span><span>{e(vm["projecao"])} (HLM {e(vm["hlm"])})</span>'
            f'<span class="key">Propriedades fixadas</span><span>{fixed}</span>'
            f'<span class="key">Contextos externos fixados</span><span>{contexts}</span></div></div>')
    body += "<p>" + " ".join(f"{badge(k)} {v}" for k, v in vm["resumo"].items()) + "</p>"
    for state in PROFILE_STATE_ORDER:
        rules = [r for r in vm["regras"] if r["estado"] == state]
        if not rules:
            continue
        body += f"<h2>{badge(state)} {len(rules)} regra(s)</h2>"
        rows = []
        for r in rules:
            terms = "<br>".join(f'{badge(t["estado"])} {e(t["texto"])}' + (f' <span class="note">(fixado: {e(value_text(t["valorFixado"]))})</span>'
                                                                         if t.get("valorFixado") is not None else "")
                                for t in r["termos"]) or '<span class="note">sem condição</span>'
            ctx = ", ".join(f'{c["nome"]} ({c["origem"]})' for c in r["contextos"])
            rows.append([chip(r["tipo"], r["regra"], href=L.href(L.rule_page(r["regra"]))), f'<code>{e(r["ocorrencia"] or "(HLM)")}</code>', terms,
                         e(r.get("restricao") or r["descricao"]), e(ctx)])
        body += table(["Regra", "Ocorrência", "Termos da condição", "Restrição / descrição", "Contextos externos"], rows)
    body += ('<div class="legend">Termo: verdadeiro/falso = resolvido pelo perfil; dinâmico = o valor vem da instância; '
             'indisponível = nem projetado nem fixado. Regra: sempre aplicável (todos os termos resolvidos verdadeiros), '
             'nunca aplicável (um termo falso), dinâmica, não avaliável (um termo indisponível), alvo fora da projeção.</div>')
    return body


def profile_candidates(vm):
    body = table(["Alvo da restrição", "Regras", "Propriedades na aplicabilidade"],
                 [[L.link(L.decision_page(r["alvo"]), r["nome"], css="prop"), " ".join(L.link(L.rule_page(x), x) for x in r["regras"]),
                   e(", ".join(r["propriedades"]))] for r in vm["linhas"]])
    body += f'<p><b>Candidatas a fixar num perfil:</b> {e(", ".join(vm["candidatas"]))}</p>'
    return body
