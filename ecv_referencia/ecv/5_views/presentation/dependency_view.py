"""Validity dependency analysis (per value of the property) and impact of a change."""
from .. import links as L
from .html import chip, e, table, value_text


def _affected(a):
    if not a.get("chave"):
        return chip("RIC", a.get("nome") or "(conclusão)")
    if L.is_property_key(a["chave"]):
        decision = L.href(L.decision_page(a["chave"]))
        return L.property_link(a["chave"], a.get("nome")) + (f' <a class="note" href="{e(decision)}">decisão</a>' if decision else "")
    return e(a.get("nome"))


def _rule_detail(card, focus_name, open_=False):
    terms = "".join(f'<span class="term{" focus" if t.get("foco") else ""}">'
                    f'{"termo " + str(i + 1) + ": "}<code>{e(t.get("texto"))}</code>'
                    f'{" ← o termo sobre " + e(focus_name) if t.get("foco") else ""}</span>'
                    for i, t in enumerate(card.get("condicao", [])))
    restriction = card.get("restricao") or {}
    if card["tipo"] == "RIC":
        c = card.get("conclusao") or {}
        effect = f'<b>Conclusão</b> {e(c.get("tipo"))} {e(c.get("valor"))} · <b>Mensagem</b> {e(card.get("mensagem"))}'
        summary = f'conclui {e(c.get("valor"))}'
    else:
        text = (restriction.get("chamada") or {}).get("chamada") if restriction.get("forma") == "funcao" else restriction.get("texto")
        effect = f'<b>Restrição</b> <code>{e(text)}</code><br><b>Mensagem de não conformidade</b> {e(card.get("mensagem"))}'
        summary = f'<code>{e(text)}</code>'
    affected = " ".join(_affected(a) for a in card.get("alvos") or []) or '<span class="note">nenhuma (conclusão)</span>'
    home = card.get("viveEm") or {}
    return (f'<details class="step"{" open" if open_ else ""}><summary><span class="flow">{L.rule_link(card)} '
            f'<span class="arrow">→</span> {summary}</span></summary>'
            f'<div class="fields"><span class="key">Condição de aplicabilidade (completa)</span><span>{terms}</span>'
            f'<span class="key">Efeito</span><span>{effect}</span>'
            f'<span class="key">Propriedades afetadas</span><span>{affected}</span>'
            f'<span class="key">Vive em</span><span>{e(home.get("rotulo"))} {e(home.get("nome"))}</span></div></details>')


def _value_matrix(vm, p):
    targets = list(vm["afetadas"])
    head = "".join(f"<th>{_affected(a)}</th>" for a in targets)
    rows = ""
    for v in vm["valores"]:
        cells = ""
        for a in targets:
            ids = [r for r in v["regras"] if r in a["regras"]]
            cells += f'<td title="{e(", ".join(ids))}">{len(ids) if ids else "—"}</td>'
        css = "" if v["plausivel"] else ' class="implausible-row"'
        rows += f'<tr{css}><td class="row-label"><span class="value">{e(v["valor"])}</span></td>{cells}</tr>'
    return ("<h2>Resumo: que propriedades cada valor condiciona</h2>"
            f'<table class="matrix"><thead><tr><th class="row-label">{e(p["nome"])} = \\ afeta</th>{head}</tr></thead>'
            f'<tbody>{rows}</tbody></table>')


def dependencies(vm):
    p = vm["propriedade"]
    cards = {c["id"]: c for c in vm["regras"]}
    body = (f'<div class="box"><div class="fields"><span class="key">Propriedade</span>'
            f'<span>{L.property_link(p["chave"], p["dono"] + "." + p["nome"])} <span class="meta">{e(p["tipo"])}</span> — {e(p["descricao"])}</span>'
            f'<span class="key">Valores plausíveis (RP)</span><span>'
            + (" ".join(f'<span class="value">{e(v)}</span>' for v in vm["plausiveis"]) or '<span class="note">não enumerada</span>')
            + (" " + " ".join(L.link(L.rule_page(r["id"]), r["id"], css="chip RP") for r in vm["rp"]) if vm["rp"] else "")
            + f'</span><span class="key">Regras cuja condição a lê</span><span>{len(vm["regras"])}</span>'
            f'<span class="key">Outras vistas</span><span>{L.link(L.impact_page(p["chave"]), "impacto de uma alteração")}</span></div></div>')
    if vm["valores"]:
        body += _value_matrix(vm, p)
    options = '<option value="*">todos</option>' + "".join(f'<option value="v{i}">{e(v["valor"])}</option>' for i, v in enumerate(vm["valores"]))
    body += ('<h2>Fluxo: valor → condição → regras → propriedades afetadas</h2>'
             f'<div class="toolbar"><label>Valor de {e(p["nome"])} <select data-show="data-value">{options}</select></label>'
             '<span><button data-blocks="open">Expandir tudo</button> <button data-blocks="close">Recolher tudo</button></span></div>')
    for i, v in enumerate(vm["valores"]):
        affected = " ".join(_affected(a) for a in v["afetadas"]) or '<span class="note">nenhuma</span>'
        rules = "".join(_rule_detail(cards[r], p["nome"]) for r in v["regras"]) or '<p class="note">Nenhuma regra se aplica com este valor.</p>'
        warning = "" if v["plausivel"] else ' <span class="note" style="color:#9a2c00">(fora dos valores plausíveis)</span>'
        body += (f'<div data-value="v{i}" class="visible"><details class="step"><summary><span class="flow">'
                 f'<span class="prop">{e(p["nome"])}</span><span class="arrow">=</span><span class="value large">{e(v["valor"])}</span>{warning}'
                 f'<span class="arrow">→</span><b>{len(v["regras"])} regra(s)</b><span class="arrow">→</span>{affected}</span></summary>'
                 f'{rules}</details></div>')
    if vm["outrosTermos"]:
        body += ("<h2>Regras em que o termo sobre a propriedade não é de seleção</h2>"
                 + "".join(_rule_detail(cards[r], p["nome"]) for r in vm["outrosTermos"]))
    body += "<h2>Propriedades afetadas (todas as regras)</h2>" + table(
        ["Propriedade", "N.º de regras", "Regras"], [[_affected(a), len(a["regras"]), " ".join(L.rule_link(cards[r]) for r in a["regras"])]
                                                     for a in vm["afetadas"]])
    return body


def impact(vm):
    c = vm["contagem"]
    body = (f'<div class="box"><b>Impacto:</b> alterar {L.property_link(vm["propriedade"], vm["nome"])} (nome, valores plausíveis '
            f'ou posição) afeta {c["RP"]} RP, {c["RIR"]} RIR e {c["RIC"]} RIC, {len(vm["projecoes"])} ocorrência(s) em '
            f'projeções e {len(vm["perfis"])} fixação(ões) em perfis. '
            f'{L.link(L.dependencies_page(vm["propriedade"]), "ver a análise de dependências")}</div>')
    body += "<h2>Regras</h2>" + table(["Regra", "Papel da propriedade", "Descrição"],
                                     [[L.link(L.rule_page(r["id"]), r["id"], css=f"chip {r['tipo']}"), e("; ".join(r["papeis"])),
                                       e(r["descricao"])] for r in vm["regras"]])
    body += "<h2>Projeções</h2>" + (table(["Projeção", "Caminho", ""], [[e(p["projecao"]), f'<code>{e(p["caminho"])}</code>', e(p["tipo"])]
                                                                     for p in vm["projecoes"]]) if vm["projecoes"] else "<p>Nenhuma.</p>")
    body += "<h2>Perfis</h2>" + (table(["Perfil", "Caminho", "Valor fixado"],
                                       [[L.link(L.profile_page(p["perfil"]), p["perfil"]), f'<code>{e(p["caminho"])}</code>', e(value_text(p["valor"]))]
                                        for p in vm["perfis"]]) if vm["perfis"] else "<p>Nenhum.</p>")
    return body
