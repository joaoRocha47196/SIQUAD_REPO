"""Decision view (matrix and tree over the same data) and coherence view."""
from .. import links as L
from .html import COLORS, e, table, value_text
from .svg import Svg


def _extra(cards, rule_id):
    card = cards.get(rule_id, {})
    home = card.get("viveEm") or {}
    return (f'<span class="extra x-id">{L.rule_link(card) if card else e(rule_id)}</span>'
            f'<span class="extra x-msg">{e(card.get("mensagem"))}</span>'
            f'<span class="extra x-desc">{e(card.get("descricao"))}</span>'
            f'<span class="extra x-home">vive em {e(home.get("rotulo"))} {e(home.get("nome"))}</span>')


CELL_CLASS = {"vazia": "c-empty", "incoerente": "c-incoherent", "conflito": "c-conflict", "ok": "c-ok"}


def _cell(c, cards):
    if c["estado"] == "vazia":
        return '<td class="c-empty">—</td>'
    parts = []
    for r in c["regras"]:
        v = f'{e(value_text(r["minimo"]))}<br>{e(value_text(r["maximo"]))}' if r["minimo"] is not None else f'<code>{e(value_text(r["valor"]))}</code>'
        parts.append(f'<span title="{e(r["id"])}: {e(r["mensagem"])}">{v}</span>{_extra(cards, r["id"])}')
    return f'<td class="{CELL_CLASS[c["estado"]]}">' + "<hr>".join(parts) + "</td>"


def _matrix_header(m):
    dims = m["dimensoesColunas"]
    if len(dims) < 2:
        return (f'<tr><th class="row-label">{e(m["dimensaoLinhas"])} \\ {e(" · ".join(dims))}</th>'
                + "".join(f'<th>{e(c["rotulo"])}</th>' for c in m["colunas"]) + "</tr>")
    groups = []
    for c in m["colunas"]:
        first = c["valores"][0]["valor"]
        if groups and groups[-1][0] == first:
            groups[-1][1] += 1
        else:
            groups.append([first, 1])
    head = f'<tr><th class="row-label">{e(dims[0])}</th>' + "".join(
        f'<th colspan="{n}">{e("(qualquer)" if v is None else v)}</th>' for v, n in groups) + "</tr>"
    head += f'<tr><th class="row-label">{e(m["dimensaoLinhas"])} \\ {e(" · ".join(dims[1:]))}</th>' + "".join(
        f'<th>{e(" · ".join("*" if x["valor"] is None else str(x["valor"]) for x in c["valores"][1:]))}</th>'
        for c in m["colunas"]) + "</tr>"
    return head


def _matrix(m, cards):
    if not m["colunas"]:
        return "<p>Nenhuma RIR tipificada com termos de seleção restringe esta propriedade.</p>"
    rows = ""
    for row in m["linhas"]:
        css = "" if row["plausivel"] else "implausible-row"
        label = e(row["rotulo"]) + ("" if row["plausivel"] else ' <span class="note">(fora dos plausíveis)</span>')
        if row["semRegras"]:
            label += ' <span class="note">(sem regras)</span>'
        rows += f'<tr class="{css}"><td class="row-label">{label}</td>' + "".join(_cell(c, cards) for c in row["celulas"]) + "</tr>"
    body = (f'<table class="matrix"><thead>{_matrix_header(m)}</thead><tbody>{rows}</tbody></table>'
            '<div class="legend"><span style="background:#ececec;padding:0 6px">cinzento</span> combinação sem regra; '
            '<span style="background:#f9d6c7;padding:0 6px">vermelho</span> gama sem valor comum com a gama geral (qualquer) da coluna; '
            '<span style="background:#fde3a7;padding:0 6px">amarelo</span> mais de uma regra com valores diferentes; '
            'linha a vermelho: valor fora dos valores plausíveis (a regra nunca se aplica). Gamas: mínimo sobre máximo.</div>')
    if m.get("outras"):
        body += "<h3>RIR com outros termos (não colocadas na matriz)</h3>" + table(
            ["Regra", "Termos", "Restrição"], [[L.rule_link(cards.get(o["id"], {"id": o["id"], "tipo": "RIR"})),
                                                e("; ".join(o.get("termos") or o.get("outrosTermos") or [])), e(o["texto"])]
                                               for o in m["outras"]])
    return body


def _tree_node(node, cards):
    if node["tipo"] == "regras":
        return "".join(f'<li><span class="leaf" title="{e(r["id"])}">{e(r["texto"])}</span> {_extra(cards, r["id"])}</li>'
                       for r in node["regras"])
    items = ""
    for branch in node["ramos"]:
        css = "value any" if branch["valor"] is None else ("value" if branch["plausivel"] else "value implausible")
        extra = "" if branch["plausivel"] else ' <span class="note">valor fora dos plausíveis: a regra nunca se aplica</span>'
        items += f'<li><span class="{css}">{e(branch["rotulo"])}</span>{extra}<ul>{_tree_node(branch["filho"], cards)}</ul></li>'
    without = ""
    if node.get("semRamo"):
        without = f'<li><span class="note">valores plausíveis sem regra: {e(", ".join(map(str, node["semRamo"])))}</span></li>'
    coverage = ""
    if node.get("cobertura") and node["cobertura"]["naoCobertos"]:
        c = node["cobertura"]
        coverage = (f'<li><span class="note" style="color:#9a2c00">valores da gama geral {e(value_text(c["referencia"]))} '
                    f'({e(c["regraReferencia"])}) que nenhum ramo cobre: '
                    f'{e(", ".join("]" + value_text(a) + ", " + value_text(b) + "[" for a, b in c["naoCobertos"]))}</span></li>')
    dim = L.link(L.dependencies_page(node["chave"]), node["propriedade"], css="dim")
    return f'<li>{dim}<ul>{items}{without}{coverage}</ul></li>'


def _range_axis(node):
    ranges = [(b["rotulo"], r) for b in node["ramos"] for r in b["filho"].get("regras", []) if r["minimo"] is not None]
    if not ranges:
        return ""
    low = min(r["minimo"] for _, r in ranges)
    high = max(r["maximo"] for _, r in ranges)
    width, left = 1000, 170
    scale = (width - left - 130) / ((high - low) or 1)
    s = Svg(width, 40 + 22 * len(ranges))
    for i, (label, r) in enumerate(ranges):
        y = 20 + 22 * i
        x1, x2 = left + (r["minimo"] - low) * scale, left + (r["maximo"] - low) * scale
        s.rect(x1, y, max(x2 - x1, 2), 12, fill=COLORS["amarelo"], border="#666")
        s.text(left - 6, y + 10, f"{label}", size=10, anchor="end")
        s.text(x2 + 4, y + 10, f"{value_text(r['minimo'])} a {value_text(r['maximo'])}  {r['id']}", size=9, color="#555", anchor="start")
    for a, b in (node.get("cobertura") or {}).get("naoCobertos", []):
        x1, x2 = left + (a - low) * scale, left + (b - low) * scale
        s.rect(x1, 8, max(x2 - x1, 1), 22 * len(ranges) + 14, fill="none", border=COLORS["erro"], dashed=True)
    return s.render()


def _plausibility(rules):
    if not rules:
        return '<span class="note">sem RP</span>'
    return "<br>".join(f'{L.link(L.rule_page(r["id"]), r["id"], css="chip RP")} <code>{e(r["texto"])}</code>' for r in rules)


def _dimensions_table(vm):
    return table(["Fator discriminante", "Modelo", "Valores plausíveis (RP)", "Valores usados nas RIR", "Regras de plausibilidade",
                  "RIR que o usam"],
                 [[L.link(L.dependencies_page(d["chave"]), d["nome"], css="dim"), e(d["dono"]),
                   " ".join(f'<span class="value">{e(v)}</span>' for v in (d["plausiveis"] or [])) or '<span class="note">não enumerado</span>',
                   " ".join(f'<span class="value{"" if not d["plausiveis"] or v in d["plausiveis"] else " implausible"}">{e(v)}</span>' for v in d["usados"]),
                   _plausibility(d["rp"]), d["frequencia"]] for d in vm["dimensoes"]])


def _tree_section(vm, cards):
    out = ""
    if vm["filtro"]:
        out += "<p>Fixado: " + " ".join(f'<span class="dim">{e(f["propriedade"])}</span> = <span class="value">{e(f["valor"])}</span>'
                                       for f in vm["filtro"]) + "</p>"
    root = vm["arvore"]
    out += f'<ul class="tree">{_tree_node(root, cards)}</ul>'
    if root.get("tipo") == "dimensao":
        axis = _range_axis(root)
        if axis:
            out += "<h3>Gamas no eixo</h3>" + axis + '<div class="legend">Contorno tracejado: valores que nenhuma gama específica cobre.</div>'
    out += ('<div class="legend"><span><span class="dim">propriedade</span> fator discriminante</span>'
            '<span><span class="value">valor</span> ramo</span><span><span class="leaf">restrição</span> o que a RIR exige</span>'
            '<span><span class="value implausible">valor</span> fora dos plausíveis</span></div>')
    return out


def decision(vm):
    cards = {c["id"]: c for c in vm["regras"]}
    p = vm["propriedade"]
    body = (f'<div class="box"><div class="fields"><span class="key">Propriedade restringida</span>'
            f'<span>{L.property_link(p["chave"], p["dono"] + "." + p["nome"])} <span class="meta">{e(p["tipo"])}</span> — {e(p["descricao"])}</span>'
            f'<span class="key">O que pode tomar, sempre (RP)</span><span>{_plausibility(p["rp"])}</span>'
            f'<span class="key">RIR que a restringem</span><span>{len(vm["regras"])}</span></div></div>')
    body += "<h2>Fatores discriminantes e os valores que podem tomar</h2>" + _dimensions_table(vm)
    body += ('<div class="toolbar"><span><label><input type="radio" name="mode" value="tabela" data-show="data-mode" checked> Tabela</label> '
             '<label><input type="radio" name="mode" value="arvore" data-show="data-mode"> Árvore</label></span>'
             '<span>Mais informação em cada célula: '
             '<label><input type="checkbox" data-on="show-id"> regra</label> '
             '<label><input type="checkbox" data-on="show-msg"> mensagem</label> '
             '<label><input type="checkbox" data-on="show-desc"> descrição</label> '
             '<label><input type="checkbox" data-on="show-home"> onde vive</label></span></div>')
    m = vm["matriz"]
    body += (f'<div data-mode="tabela" class="visible"><p>Linhas: <b>{e(m.get("dimensaoLinhas") or "—")}</b>. '
             f'Colunas: <b>{e(" × ".join(m.get("dimensoesColunas") or []) or "—")}</b>.</p>{_matrix(m, cards)}</div>')
    body += f'<div data-mode="arvore">{_tree_section(vm, cards)}</div>'
    body += "<h2>As RIR, com toda a informação</h2>"
    body += table(["Regra", "Vive em", "Condição de aplicabilidade", "Restrição", "Mensagem de não conformidade", "Descrição"],
                  [[L.rule_link(c), e(f"{c['viveEm']['rotulo']} {c['viveEm']['nome']}"),
                    "<br>".join(f"<code>{e(t['texto'])}</code>" for t in c.get("condicao", [])),
                    f"<code>{e((c.get('restricao') or {}).get('texto'))}</code>", e(c.get("mensagem")), e(c.get("descricao"))]
                   for c in vm["regras"]])
    return body


def coherence(vm):
    def rule(rule_id):
        return L.link(L.rule_page(rule_id), rule_id)
    body = "<h2>Termos com valores fora dos valores plausíveis</h2>"
    body += table(["Regra", "Propriedade", "Valores", "Plausíveis"],
                  [[rule(x["regra"]), L.property_link(x["propriedade"]), e(", ".join(map(str, x["valores"]))),
                    e(", ".join(map(str, x["plausiveis"])))] for x in vm["foraDosPlausiveis"]]) if vm["foraDosPlausiveis"] \
        else '<p class="ok">Nenhum.</p>'
    body += "<h2>Regras incompatíveis (aplicam-se à mesma situação e as gamas não têm valor comum)</h2>"
    body += table(["Propriedade", "Regra A", "Regra B"],
                  [[L.property_link(x["propriedade"])] + [f'{rule(y["id"])}<br><span class="note">{e(y["texto"])}</span>'
                                                          for y in x["regras"]] for x in vm["incompativeis"]]) \
        if vm["incompativeis"] else '<p class="ok">Nenhuma.</p>'
    body += "<h2>Regras com a mesma condição de aplicabilidade</h2>"
    body += table(["Condição", "Regras"], [[f'<code>{e(x["condicao"])}</code>', " ".join(rule(i) for i in x["regras"])]
                                          for x in vm["mesmaCondicao"]]) if vm["mesmaCondicao"] else '<p>Nenhuma.</p>'
    return body
