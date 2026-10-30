"""Model views: the HLM (hlm_<HLM>), with rules (regras_<HLM>) and a specific model (sm_<SM>, usm_<USM>).

Tree (an HTML organisation chart) on top; below, a table by blocks, one block per direct composition,
that expands (one property per row, with description) or collapses (the model and its properties in
one row). With rules: a column with the rules of each node, in separate fields, and two alternative
groupings (by target and by nature).
"""
from ecv import config

from .. import links as L
from .html import checkbox_menu, e, value_text

RULE_ATTRIBUTES = {"id": "Identificador", "home": "Onde vive", "desc": "Descrição (derivada)", "cond": "Condição de aplicabilidade",
                   "restr": "Restrição", "msg": "Mensagem", "concl": "Conclusão (RIC)", "ctx": "Funções e contextos externos"}
DEFAULT_ATTRIBUTES = ("id", "cond", "restr", "msg", "concl", "ctx")


# ---------------------------------------------------------------------- pieces
def model_name(level, name, role=None, card=None):
    role_text = f' <span class="alt">(papel {e(role)})</span>' if role and role != name else ""
    card_text = f' <span class="meta">[{e(card)}]</span>' if card else ""
    return f'<span class="tag {level}">{level}</span>' + L.link(L.model_page(level, name), name, css=f"n-{level}") + role_text + card_text


def discriminating_mark(key):
    h = L.href(L.dependencies_page(key))
    if not h:
        return ""
    return f' <a class="disc" href="{e(h)}" title="fator discriminante: ver a análise de dependências">◆</a>'


def rule_legend():
    """Colour key (acronyms only): the explanation of each nature is in the technical documentation."""
    items = [f'<span><span class="square {t}"></span>{t}</span>' for t in ("RP", "RIR", "RIC")]
    items.append('<span><span class="square FN"></span>restrição por função</span>')
    items.append('<span><span class="square" style="background:#7F7F7F"></span>RE (projeções)</span>')
    return '<div class="rule-legend">' + " ".join(items) + "</div>"


def _term_text(t):
    return e(t.get("texto"))


def rule_card(card, compact=False):
    restriction_form = (card.get("restricao") or {}).get("forma")
    layer = "E" if restriction_form == "funcao" else ("C" if card.get("tipo") == "RP" else "D")
    parts = [f'<span class="attr-id">{L.rule_link(card)}{L.edit_link(layer, "substituir_regra", "alterar a regra", regra=card["id"])}</span>']
    home = card.get("viveEm") or {}
    parts.append(f' <span class="note attr-home">vive em {e(home.get("rotulo"))} {e(home.get("nome"))}</span>')
    if not compact:
        parts.append(f'<span class="rule-field attr-desc"><span class="key">Descrição</span>{e(card.get("descricao"))}</span>')
    if card.get("condicao"):
        parts.append('<span class="rule-field attr-cond"><span class="key">Condição</span>'
                     + " <b>e</b> ".join(f"<code>{_term_text(t)}</code>" for t in card["condicao"]) + "</span>")
    restriction = card.get("restricao")
    if restriction:
        if restriction.get("forma") == "funcao":
            call = restriction.get("chamada") or {}
            parts.append(f'<span class="rule-field attr-restr"><span class="key">Restrição (função, {e(restriction.get("operador"))})</span>'
                         f'<code>{e(call.get("chamada"))}</code></span>')
        else:
            parts.append(f'<span class="rule-field attr-restr"><span class="key">Restrição</span><code>{e(restriction.get("texto"))}</code></span>')
    if card["tipo"] == "RIC":
        parts.append(f'<span class="rule-field attr-msg"><span class="key">Mensagem (a conclusão)</span>{e(card.get("mensagem"))}</span>')
        c = card.get("conclusao") or {}
        parts.append(f'<span class="rule-field attr-concl"><span class="key">Tipo de conclusão</span>'
                     f'{e(config.CONCLUSION_TYPES.get(c.get("tipo"), c.get("tipo")))} <b>{e(c.get("valor"))}</b></span>')
    else:
        parts.append(f'<span class="rule-field attr-msg"><span class="key">Mensagem de não conformidade</span>{e(card.get("mensagem"))}</span>')
    uses = []
    if card.get("funcoes"):
        uses.append("funções: " + ", ".join(card["funcoes"]))
    if card.get("contextosExternos"):
        uses.append("contextos externos: " + ", ".join(card["contextosExternos"]))
    if uses:
        parts.append(f'<span class="rule-field attr-ctx"><span class="key">Usa</span>{e("; ".join(uses))}</span>')
    return f'<div class="rule-card {card["categoria"]}">' + "".join(parts) + "</div>"


def rir_group(group):
    n = len(group["regras"])
    target = L.target_link(group["alvo"], group.get("nome")) if group["alvo"] != "?" else e(group.get("nome") or "função")
    h = L.href(L.decision_page(group["alvo"])) if group.get("decisao") else None
    if h:
        return (f'<div class="rir-group"><span class="square RIR"></span><b>{n} RIR</b> restringe{"m" if n > 1 else ""} {target} · '
                f'<a href="{e(h)}">ver o mapeamento (vista de decisão)</a></div>')
    # without a decision view, the rules are listed (few, or a function target)
    body = "".join(rule_card(c, compact=True) for c in group["regras"])
    return f'<div class="rir-group"><span class="square RIR"></span><b>{n} RIR</b> restringe{"m" if n > 1 else ""} {target}{body}</div>'


def rules_cell(row):
    return "".join([rule_card(c) for c in row.get("regras", [])] + [rir_group(g) for g in row.get("rir", [])])


def rule_count(row):
    return len(row.get("regras", [])) + sum(len(g["regras"]) for g in row.get("rir", []))


# ---------------------------------------------------------------------- tree
def _org_box(node, root=False):
    level = node["nivel"]
    info = []
    if node.get("papel") and node["papel"] != node["nome"]:
        info.append(f'papel {e(node["papel"])}')
    if node.get("cardinalidade"):
        info.append(e(node["cardinalidade"]))
    caption = f'<div class="caption">{" · ".join(info)}</div>' if info else ""
    props = ""
    if node["propriedades"]:
        props = '<ul class="props">' + "".join(
            f'<li><a href="#{L.property_anchor(p["chave"])}" style="color:inherit;text-decoration:none" title="{e(p["descricao"])}">'
            f'{e(p["nome"])}</a> <span class="meta">{e(p["tipo"])}</span>{discriminating_mark(p["chave"]) if p["discriminante"] else ""}</li>'
            for p in node["propriedades"]) + "</ul>"
    users = ""
    if node.get("usadoPor") is not None and not root:
        hlms = node["usadoPor"]
        users = (f'<details><summary>usado por {len(hlms)} HLM</summary>'
                 + "<br>".join(L.link(L.model_page("HLM", h), h, css="n-HLM") for h in hlms) + "</details>")
    children = "<ul>" + "".join(_org_box(c) for c in node["filhos"]) + "</ul>" if node["filhos"] else ""
    return (f'<li><div class="node-box {level}{" current" if root and level != "HLM" else ""}" title="{e(node["descricao"])}">'
            f'<div class="title">{model_name(level, node["nome"])}</div>{caption}{props}{users}</div>{children}</li>')


def org_tree(root):
    return f'<div class="tree-wrap"><ul class="org">{_org_box(root, root=True)}</ul></div>'


# ---------------------------------------------------------------------- table by blocks
def _structure_cell(row, with_toggle=False):
    pad = f'padding-left:{6 + 20 * max(row["profundidade"] - 1, 0)}px'
    toggle = '<span class="toggle"></span>' if with_toggle else ""
    if row["tipo"] == "Propriedade":
        alt = f' <span class="alt">(também: {e(", ".join(row["nomesAlternativos"]))})</span>' if row.get("nomesAlternativos") else ""
        level, owner = row["chave"].split(":", 1)[0], row["chave"].split(":", 1)[1].split(".")[0]
        edit = L.edit_link("A", "alterar_propriedade", "alterar a propriedade", modelo=f"{level}:{owner}", propriedade=row["nome"])
        cell = (f'<span class="prop" id="{L.property_anchor(row["chave"])}">{e(row["nome"])}</span>{edit} <span class="meta">{e(row.get("tipoBase"))}</span>'
                f'{discriminating_mark(row["chave"]) if row.get("discriminante") else ""}{alt}')
    else:
        cell = model_name(row["tipo"], row["nome"], row.get("papel"), row.get("cardinalidade"))
    return f'<td style="{pad}">{toggle}{cell}</td>'


def blocks_table(vm):
    with_rules = vm["comRegras"]
    ncol = 3 if with_rules else 2
    head = ('<thead><tr><th style="width:30%">Estrutura do modelo</th><th style="width:' + ("26%" if with_rules else "70%")
            + '">Descrição</th>' + ('<th>Regras (o que vive neste nó)</th>' if with_rules else "") + "</tr></thead>")
    body = ""
    root = vm["raiz"]
    if with_rules and (root.get("regras") or root.get("rir")):
        body += (f'<tbody class="block open"><tr class="head">{_structure_cell({**root, "profundidade": 1}, True)}'
                 f'<td>{e(root.get("descricao"))}</td><td class="rules">{rules_cell(root)}</td></tr>'
                 f'<tr class="summary-row"><td colspan="{ncol}" class="note">{rule_count(root)} regra(s) no próprio {e(vm["nivel"])}</td></tr></tbody>')
    for block in vm["blocos"]:
        rows = block["linhas"]
        if block.get("proprio"):
            first, rest = None, rows
        else:
            first, rest = rows[0], rows[1:]
        props = ", ".join(block["resumoPropriedades"]) or "—"
        n = sum(rule_count(r) for r in rows) if with_rules else 0
        summary = (f'<tr class="summary-row"><td colspan="{ncol}"><span class="note">propriedades:</span> <span class="prop">{e(props)}</span>'
                   + (f' <span class="note">· {n} regra(s)</span>' if with_rules else "") + "</td></tr>")
        if first is None:
            header = (f'<tr class="head"><td><span class="toggle"></span><b>Propriedades do próprio {e(vm["nivel"])} '
                      f'{e(vm["nome"])}</b></td><td></td>' + ("<td></td>" if with_rules else "") + "</tr>")
        else:
            header = (f'<tr class="head">{_structure_cell(first, True)}<td>{e(first.get("descricao"))}</td>'
                      + (f'<td class="rules">{rules_cell(first)}</td>' if with_rules else "") + "</tr>")
        detail = "".join(f'<tr class="detail-row">{_structure_cell(r)}<td>{e(r.get("descricao"))}</td>'
                         + (f"<td>{rules_cell(r)}</td>" if with_rules else "") + "</tr>" for r in rest)
        body += f'<tbody class="block open">{header}{summary}{detail}</tbody>'
    return f'<table class="model">{head}{body}</table>'


# ---------------------------------------------------------------------- groupings (view with rules)
def by_target(vm):
    groups, order = {}, []
    for card in vm["regras"]:
        key = "(conclusões)" if card["tipo"] == "RIC" else ((card.get("alvo") or {}).get("chave") or "(função)")
        if key not in groups:
            order.append(key)
        groups.setdefault(key, []).append(card)
    tree_keys = [r["chave"] for b in vm["blocos"] for r in b["linhas"] if r["tipo"] == "Propriedade"]
    order.sort(key=lambda k: (tree_keys.index(k) if k in tree_keys else 999, k))
    out = ""
    for key in order:
        cards = groups[key]
        if key.startswith("("):
            title = e(key)
        else:
            name = (cards[0].get("alvo") or {}).get("nome")
            title = L.target_link(key, name) + (discriminating_mark(key) if L.is_property_key(key) else "")
            h = L.href(L.decision_page(key))
            if h:
                title += f' <a class="note" href="{e(h)}">vista de decisão</a>'
        counts = {t: sum(1 for c in cards if c["tipo"] == t) for t in ("RP", "RIR", "RIC")}
        out += (f'<h3>{title} <span class="note">{" · ".join(f"{v} {t}" for t, v in counts.items() if v)}</span></h3>'
                + "".join(rule_card(c) for c in cards))
    return out


def _nature_table(cards):
    rows = ""
    for card in cards:
        restriction = card.get("restricao") or {}
        restriction_text = (restriction.get("chamada") or {}).get("chamada") if restriction.get("forma") == "funcao" else restriction.get("texto")
        c = card.get("conclusao") or {}
        conclusion = f'{config.CONCLUSION_TYPES.get(c.get("tipo"), "")} {c.get("valor")}' if card["tipo"] == "RIC" else ""
        home = card.get("viveEm") or {}
        uses = "; ".join(x for x in (", ".join(card.get("funcoes") or []), ", ".join(card.get("contextosExternos") or [])) if x)
        rows += (f'<tr><td class="attr-id">{L.rule_link(card)}</td><td class="attr-home">{e(home.get("rotulo"))} {e(home.get("nome"))}</td>'
                 f'<td class="attr-desc">{e(card.get("descricao"))}</td>'
                 f'<td class="attr-cond">{"<br>".join("<code>" + _term_text(t) + "</code>" for t in card.get("condicao", [])) or "—"}</td>'
                 f'<td class="attr-restr"><code>{e(restriction_text)}</code></td><td class="attr-msg">{e(card.get("mensagem"))}</td>'
                 f'<td class="attr-concl">{e(conclusion)}</td><td class="attr-ctx">{e(uses)}</td></tr>')
    head = ('<thead><tr><th class="attr-id">Regra</th><th class="attr-home">Vive em</th><th class="attr-desc">Descrição</th>'
            '<th class="attr-cond">Condição</th><th class="attr-restr">Restrição</th><th class="attr-msg">Mensagem</th>'
            '<th class="attr-concl">Conclusão</th><th class="attr-ctx">Usa</th></tr></thead>')
    return f"<table>{head}<tbody>{rows}</tbody></table>"


def _functions_table(functions):
    rows = []
    for f in functions:
        params = ", ".join(f'{p["nome"]}: {p["tipo"]}' + (" (literal)" if p.get("papel") == "parametro" else "")
                           + (" [coleção]" if p.get("colecao") else "") for p in f["parametros"])
        rows.append(f'<tr><td><b>{e(f["nome"])}</b><br><span class="note">{e(f["descricao"])}</span></td>'
                    f'<td><code>{e(params)}</code></td><td>{e(", ".join(f["contextos"]) or "—")}</td>'
                    f'<td>{" ".join(L.link(L.rule_page(r), r) for r in f["regras"])}</td></tr>')
    return ('<h3><span class="square FN"></span>Funções usadas</h3><table><thead><tr><th>Função (verdadeira quando…)</th>'
            '<th>Parâmetros</th><th>Contextos externos</th><th>Regras</th></tr></thead><tbody>' + "".join(rows) + "</tbody></table>")


def _contexts_table(contexts):
    rows = [f'<tr><td><b>{e(c["nome"])}</b> <span class="meta">{e(c["tipo"])}</span><br><span class="note">{e(c["descricao"])}</span></td>'
            f'<td>{e(c["fonte"])}</td><td>{" ".join(L.link(L.rule_page(r), r) for r in c["regras"])}</td>'
            f'<td>{e(", ".join(x["perfil"] + " = " + value_text(x["valor"]) for x in c["fixadoPor"]) or "—")}</td></tr>'
            for c in contexts]
    return ('<h3>Contextos externos</h3><table><thead><tr><th>Contexto</th><th>Fonte</th><th>Regras</th>'
            '<th>Fixado por perfis</th></tr></thead><tbody>' + "".join(rows) + "</tbody></table>")


def by_nature(vm):
    cards = vm["regras"]
    sections = [("RP", "RP tipificadas", [c for c in cards if c["tipo"] == "RP" and not c["funcao"]]),
                ("FN", "RP por função", [c for c in cards if c["tipo"] == "RP" and c["funcao"]]),
                ("RIR", "RIR tipificadas", [c for c in cards if c["tipo"] == "RIR" and not c["funcao"]]),
                ("FN", "RIR por função", [c for c in cards if c["tipo"] == "RIR" and c["funcao"]]),
                ("RIC", "RIC (conclusões)", [c for c in cards if c["tipo"] == "RIC"])]
    out = "".join(f'<h3><span class="square {cat}"></span>{e(title)} ({len(items)})</h3>' + _nature_table(items)
                  for cat, title, items in sections if items)
    if vm.get("funcoes"):
        out += _functions_table(vm["funcoes"])
    if vm.get("contextos"):
        out += _contexts_table(vm["contextos"])
    return out


# ---------------------------------------------------------------------- page
def _path_html(steps):
    parts = []
    for i, step in enumerate(steps):
        role = steps[i - 1].get("papel") if i else None
        text = L.link(L.model_page(step["rotulo"], step["nome"]), step["nome"], css=f"n-{step['rotulo']}")
        if role and role != step["nome"]:
            text += f' <span class="alt">(papel {e(role)})</span>'
        card = steps[i - 1].get("cardinalidade") if i else None
        if card and card != "1..1":
            text += f' <span class="meta">[{e(card)}]</span>'
        parts.append(text)
    return " › ".join(parts)


def _toolbar(vm):
    level, name, with_rules = vm["nivel"], vm["nome"], vm["comRegras"]
    tools = ['<label><input type="checkbox" data-off="hide-props" checked> Propriedades na árvore</label>',
             '<span><button data-blocks="open">Expandir tudo</button> <button data-blocks="close">Recolher tudo</button></span>']
    if with_rules:
        tools.append('<label>Agrupar por <select data-show="data-group"><option value="modelo">modelo (árvore)</option>'
                     '<option value="alvo">alvo (propriedade restringida)</option><option value="natureza">natureza</option></select></label>')
        tools.append(checkbox_menu("Atributos das regras", RULE_ATTRIBUTES, checked=DEFAULT_ATTRIBUTES))
    links = []
    if level == "HLM":
        links.append(L.link(L.rules_page(name), "ver com regras →") if not with_rules else L.link(L.model_page("HLM", name), "← ver sem regras"))
        projections = vm.get("projecoes") or []
        if projections:
            links.append("projeções: " + L.link(L.projections_page(name), ", ".join(p["nome"] for p in projections)))
        links.append(L.link(L.gaps_page(name), "lacunas"))
    return '<div class="toolbar">' + "".join(tools) + (f'<span>{" · ".join(links)}</span>' if links else "") + "</div>"


def render(vm):
    with_rules = vm["comRegras"]
    body = _toolbar(vm)
    if with_rules:
        c = vm["contagem"]
        body += rule_legend() + (f'<p>{c["RP"]} RP, {c["RIR"]} RIR, {c["RIC"]} RIC ({c["FN"]} com restrição por função) '
                                 f'vivem neste {e(vm["nivel"])} e nos modelos que o compõem.</p>')
    if vm.get("especifico"):
        users = vm["usadoPor"]
        paths = "".join(f'<li>{_path_html(p["passos"])}</li>' for p in users["caminhos"]) or "<li>— (não é composto por nenhum modelo)</li>"
        body += (f'<h2>Usado por {len(users["hlm"])} HLM</h2><p>'
                 + " ".join(L.link(L.model_page("HLM", h), h, css="n-HLM") for h in users["hlm"])
                 + f"</p><ul>{paths}</ul><h2>Árvore de dependências até às folhas</h2>")
    else:
        body += "<h2>Árvore do modelo</h2>"
    body += org_tree(vm["arvore"])
    body += ('<div class="legend"><span><span class="tag HLM">HLM</span> modelo de alto nível</span>'
             '<span><span class="tag SM">SM</span> submodelo</span><span><span class="tag USM">USM</span> submodelo universal</span>'
             '<span><span class="disc">◆</span> fator discriminante (lido em condições)</span><span>clicar num modelo abre a sua vista</span></div>')
    body += "<h2>Estrutura" + (" e regras" if with_rules else "") + "</h2>"
    table_html = blocks_table(vm)
    if with_rules:
        body += (f'<div data-group="modelo" class="visible">{table_html}</div>'
                 f'<div data-group="alvo">{by_target(vm)}</div><div data-group="natureza">{by_nature(vm)}</div>')
    else:
        body += table_html
    return body
