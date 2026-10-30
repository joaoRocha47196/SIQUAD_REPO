"""Rule card: every element with all its information, and the subgraph in two parts.

Rule subgraph (on top, horizontal): Regra -> Restricao / CondicaoAplicabilidade -> Funcao -> ContextoExterno.
Model subgraph (below, vertical): the properties involved in the first row and, underneath, the models
that hold them, up to the HLMs. The edges from the rule to the properties are numbered, and the table
of links gives the full text of each edge (nothing is cut).
"""
from ecv import config

from .. import links as L
from .html import COLORS, chip, e, table, value_text
from .svg import Svg

COLOR = {"RP": COLORS["RP"], "RIR": COLORS["RIR"], "RIC": COLORS["RIC"], "Restricao": COLORS["funcao"],
         "CondicaoAplicabilidade": COLORS["condicao"], "Propriedade": "#555555", "USM": COLORS["USM"], "SM": COLORS["SM"],
         "HLM": COLORS["HLM"], "Funcao": COLORS["externo"], "ContextoExterno": COLORS["externo"]}
MODEL_LABELS = ("Propriedade", "USM", "SM", "HLM")


def _node_href(n):
    key = n["chave"]
    if key.startswith("Propriedade:"):
        prop_key = key.split(":", 1)[1]
        return L.href(L.model_page(prop_key.split(":")[0], prop_key.split(":")[1].split(".")[0]), L.property_anchor(prop_key))
    label, _, name = key.partition(":")
    if label in ("HLM", "SM", "USM"):
        return L.href(L.model_page(label, name))
    return None


def _leaf_order(edges, model_nodes):
    """Order of the properties by a depth-first walk from the HLMs (models stay above their children)."""
    children, has_parent = {}, set()
    for edge in edges:
        children.setdefault(edge["de"], []).append(edge["para"])
        has_parent.add(edge["para"])
    order, seen = [], set()

    def descend(k):
        if k in seen:
            return
        seen.add(k)
        if k.startswith("Propriedade:"):
            order.append(k)
        for child in children.get(k, []):
            descend(child)

    for k in sorted(model_nodes, key=lambda k: (not k.startswith("HLM:"), k)):
        if k not in has_parent:
            descend(k)
    return order


class SubgraphDrawing:
    """Layout of the two-part subgraph of a rule."""

    def __init__(self, vm):
        self.rule_part, self.model_part = vm["subgrafoRegra"], vm["subgrafoModelos"]
        self.band = [n for n in self.rule_part["nos"] if n["rotulo"] not in MODEL_LABELS]
        self.band_keys = {n["chave"] for n in self.band}
        self.positions = {}
        self.measure = Svg(10, 10)

    def _layout_rule_band(self):
        depth = {self.band[0]["chave"]: 0}
        changed = True
        while changed:
            changed = False
            for edge in self.rule_part["arestas"]:
                if edge["de"] in depth and edge["para"] in self.band_keys and edge["para"] not in depth:
                    depth[edge["para"]] = depth[edge["de"]] + 1
                    changed = True
        columns = {}
        for n in self.band:
            columns.setdefault(depth.get(n["chave"], 1), []).append(n)
        self.band_widths = {n["chave"]: self.measure.box_width(n["texto"], 10.5) for n in self.band}
        x = 30
        self.band_height = max(len(v) for v in columns.values()) * 62 + 30
        for c in sorted(columns):
            w = max(self.band_widths[n["chave"]] for n in columns[c])
            for i, n in enumerate(columns[c]):
                self.positions[n["chave"]] = (x + w / 2, 30 + (self.band_height - 40) * (i + 0.5) / len(columns[c]))
            x += w + 150
        return x

    def _layout_model_band(self, width):
        children = {}
        for edge in self.model_part["arestas"]:
            children.setdefault(edge["de"], []).append(edge["para"])
        level = {}

        def level_of(k):
            if k not in level:
                level[k] = 0 if k.startswith("Propriedade:") or not children.get(k) else 1 + max(level_of(c) for c in children[k])
            return level[k]

        self.model_nodes = {n["chave"]: n for n in self.model_part["nos"]}
        for k in self.model_nodes:
            level_of(k)
        rows = {}
        for k in self.model_nodes:
            rows.setdefault(level[k], []).append(k)
        self.model_text = {k: (n["chave"].split(":", 1)[1] if n["rotulo"] == "Propriedade" else f'{n["rotulo"]} {n["nome"]}')
                           for k, n in self.model_nodes.items()}
        self.model_widths = {k: self.measure.box_width(t, 10.5, mono=self.model_nodes[k]["rotulo"] == "Propriedade")
                             for k, t in self.model_text.items()}
        self.y0 = self.band_height + 70
        xs = {}
        for lv in sorted(rows):
            keys = rows[lv]
            if lv == 0:
                order = _leaf_order(self.model_part["arestas"], self.model_nodes)
                keys.sort(key=lambda k: order.index(k) if k in order else 99)
                cx = 30
                for k in keys:
                    xs[k] = cx + self.model_widths[k] / 2
                    cx += self.model_widths[k] + 50
            else:
                for k in keys:
                    below = [xs[c] for c in children.get(k, []) if c in xs]
                    xs[k] = sum(below) / len(below) if below else 100
                keys.sort(key=lambda k: xs[k])
                end = 0
                for k in keys:
                    xs[k] = max(xs[k], end + self.model_widths[k] / 2 + 70)
                    end = xs[k] + self.model_widths[k] / 2
            for k in keys:
                self.positions[k] = (xs[k], self.y0 + 95 * lv)
        width = max([width] + [xs[k] + self.model_widths[k] / 2 + 30 for k in xs])
        height = self.y0 + 95 * (max(rows) if rows else 0) + 50
        return width, height

    def draw(self):
        width = self._layout_rule_band()
        width, height = self._layout_model_band(width)
        s = Svg(width, height)
        s.back.insert(0, f'<rect x="4" y="4" width="{width - 8:.1f}" height="{self.band_height + 4:.1f}" fill="#fbfbfb" stroke="#e3e3e3"/>')
        s.text(10, 16, "subgrafo da regra", 9, "#999", anchor="start")
        s.text(10, self.y0 - 34, "subgrafo dos modelos (propriedade → modelo que a contém → … → HLM)", 9, "#999", anchor="start")
        numbered = self._draw_edges(s)
        self._draw_nodes(s)
        return s.render(), numbered

    def _draw_edges(self, s):
        numbered = []
        pos = self.positions
        for edge in self.rule_part["arestas"]:
            if edge["de"] not in pos or edge["para"] not in pos:
                continue
            (x1, y1), (x2, y2) = pos[edge["de"]], pos[edge["para"]]
            if edge["para"] in self.band_keys:
                w1, w2 = self.band_widths[edge["de"]] / 2, self.band_widths[edge["para"]] / 2
                s.arrow(x1 + w1, y1, x2 - w2, y2, color="#666", label=edge["tipo"], label_size=8.5)
            else:
                numbered.append(edge)
                source_label = next((x["rotulo"] for x in self.band if x["chave"] == edge["de"]), "")
                s.arrow(x1, y1 + 13, x2, y2 - 13, color=COLOR.get(source_label, "#888"), label=f"[{len(numbered)}] {edge['tipo']}",
                        label_size=8.5, dashed=edge["tipo"] in ("TERMO", "ASSOCIADA_A"))
        for edge in self.model_part["arestas"]:
            (x1, y1), (x2, y2) = pos[edge["de"]], pos[edge["para"]]
            label = "CONTEM" if edge["tipo"] == "CONTEM" else "COMPOSTO_POR" + (f" {edge['papel']}" if edge.get("papel") else "") + (
                f" [{edge['cardinalidade']}]" if edge.get("cardinalidade") else "")
            s.arrow(x1, y1 - 13, x2, y2 + 13, color="#aaa", label=label, label_size=8)
        return numbered

    def _draw_nodes(self, s):
        for n in self.band:
            x, y = self.positions[n["chave"]]
            s.box(x, y, n["texto"], border=COLOR.get(n["rotulo"], "#666"), width=self.band_widths[n["chave"]], size=10.5,
                  dashed=n["rotulo"] in ("RIR", "CondicaoAplicabilidade"), caption=n["rotulo"], stroke_width=2,
                  title=f'{n["rotulo"]}: {n["texto"]}' + (f' — {n["detalhe"]}' if n.get("detalhe") else ""))
        for k, n in self.model_nodes.items():
            x, y = self.positions[k]
            s.box(x, y, self.model_text[k], border=COLOR.get(n["rotulo"], "#666"), width=self.model_widths[k], size=10.5,
                  mono=n["rotulo"] == "Propriedade", stroke_width=2.5 if n["rotulo"] == "HLM" else 1.6, caption=n["rotulo"],
                  title=f'{self.model_text[k]}: {n.get("descricao")}', href=_node_href(n))


def _parameters_table(f):
    return table(["Parâmetro", "Tipo", "Papel", "Coleção"],
                 [[e(p["nome"]), e(p["tipo"]), e(config.PARAMETER_ROLE_NAMES.get(p.get("papel"), p.get("papel"))),
                   "sim" if p.get("colecao") else ""] for p in f["parametros"]])


def _function_box(fn, call=None):
    contexts = "".join(f'<div class="element ContextoExterno"><h4>Contexto externo {e(c["nome"])} <span class="meta">{e(c["tipo"])}</span></h4>'
                       f'<div class="fields"><span class="key">Descrição</span><span>{e(c["descricao"])}</span>'
                       f'<span class="key">Fonte</span><span>{e(c["fonte"])}</span></div></div>' for c in fn["contextos"])
    args = ""
    if call:
        args = ('<span class="key">Chamada</span><span><code>' + e(call.get("chamada")) + "</code></span>"
                '<span class="key">Argumentos (alvos lidos)</span><span>'
                + ("<br>".join(f'<code>{e(a["caminho"])}</code> → ' + (L.property_link(a["alvo"]) if a["rotuloAlvo"] == "Propriedade"
                                                                     else e(a["alvo"])) + (" (coleção)" if a.get("colecao") else "")
                               for a in call["argumentos"]) or "—") + "</span>")
    return (f'<div class="element Funcao"><h4>Função {e(fn["nome"])}</h4><div class="fields">'
            f'<span class="key">Verdadeira quando</span><span>{e(fn["descricao"])}</span>'
            f'<span class="key">Retorno</span><span>{e(fn["retorno"])}</span>{args}</div>{_parameters_table(fn)}{contexts}</div>')


def _property_text(p):
    return f'{L.property_link(p["chave"], p["chave"])} <span class="meta">{e(p["tipo"])}</span> — {e(p["descricao"])}'


def _operator_text(op):
    d = config.OPERATORS.get(op, {})
    return f'<code>{e(op)}</code> <span class="note">({e(d.get("descricao"))})</span>'


def _fields(pairs):
    return "".join(f'<span class="key">{k}</span><span>{v}</span>' for k, v in pairs)


def _rule_box(vm):
    card = vm["regra"]
    rule_type = config.RULE_TYPES[card["tipo"]]
    home = vm["viveEm"]
    home_text = (_property_text(home) if home["rotulo"] == "Propriedade" else
                 L.link(L.model_page(home["rotulo"], home["nome"]), f'{home["rotulo"]} {home["nome"]}', css=f'n-{home["rotulo"]}')
                 + f' — {e(home.get("descricao"))}')
    fields = [("Identificador", e(card["id"])),
              ("Tipo", chip(card["categoria"], card["tipo"]) + f' {e(rule_type["nome"])}'),
              ("Natureza", e(card["natureza"])), ("Descrição (derivada)", e(card["descricao"])),
              ("Vive em (alcance)", home_text),
              ("Tem efeito nos HLM", " ".join(L.link(L.model_page("HLM", h), h, css="n-HLM") for h in home["hlm"]) or "—")]
    if card["tipo"] == "RIC":
        c = card.get("conclusao") or {}
        fields.append(("Mensagem (a conclusão)", e(card.get("mensagem"))))
        fields.append(("Tipo de conclusão", f'{e(config.CONCLUSION_TYPES.get(c.get("tipo"), c.get("tipo")))} <b>{e(c.get("valor"))}</b>'))
    else:
        fields.append(("Mensagem de não conformidade", e(card.get("mensagem"))))
    if card.get("contextosExternos"):
        fields.append(("Contextos externos (derivados)", e(", ".join(card["contextosExternos"]))))
    if card.get("notas"):
        fields.append(("Notas", e(card["notas"])))
    return f'<div class="box"><h3>Regra</h3><div class="fields">{_fields(fields)}</div></div>'


def _condition_box(condition):
    terms = ""
    for i, t in enumerate(condition["termos"]):
        if t["forma"] == "funcao":
            terms += f'<div class="element Funcao"><h4>Termo {i + 1}: função ({e(t["operador"])})</h4>{_function_box(t["funcao"], t["chamada"])}</div>'
            continue
        info = t.get("contextoInfo") or {}
        compared = (f'contexto externo <b>{e(t["contexto"])}</b> ({e(info.get("descricao"))}; fonte: {e(info.get("fonte"))})'
                    if t.get("contexto") else f'<code>{e(value_text(t.get("valor")))}</code>')
        dep = L.href(L.dependencies_page(t["propriedade"]))
        terms += (f'<div class="element Propriedade"><h4>Termo {i + 1}: <code>{e(t["texto"])}</code>'
                  + (f' <a class="note" href="{e(dep)}">dependências</a>' if dep else "") + '</h4><div class="fields">'
                  + _fields([("Propriedade lida", _property_text(t["alvo"])),
                             ("Caminho (a partir de onde a regra vive)", f'<code>{e(t.get("caminho"))}</code>'),
                             ("Operador", _operator_text(t["operador"])), ("Compara com", compared)]) + "</div></div>")
    return (f'<div class="element CondicaoAplicabilidade"><h4>Condição de aplicabilidade ({len(condition["termos"])} termo(s), todos com E)</h4>'
            f'<div class="fields"><span class="key">Descrição</span><span><code>{e(condition["descricao"])}</code></span></div>{terms}</div>')


def _restriction_box(r, rule_type):
    form = config.RESTRICTION_FORMS.get(r.get("forma"), r.get("forma"))
    fields = [("Forma", f'{e(r.get("forma"))} <span class="note">({e(form)})</span>'), ("Operador", _operator_text(r.get("operador"))),
              ("Descrição", f'<code>{e(r.get("descricao"))}</code>'), ("Mensagem de não conformidade", e(r.get("mensagem")))]
    if r.get("alvo"):
        fields.insert(1, ("Restringe (alvo)", _property_text(r["alvo"])))
        fields.insert(2, ("Caminho", f'<code>{e(r.get("caminho"))}</code>'))
        fields.insert(4, ("Valor esperado", f'<code>{e(value_text(r.get("valor")))}</code>'))
        decision = L.href(L.decision_page(r["alvo"]["chave"]))
        if decision and rule_type == "RIR":
            fields.append(("Vista de decisão do alvo", f'<a href="{e(decision)}">{e(r["alvo"]["nome"])}</a>'))
    return (f'<div class="element Restricao"><h4>Restrição</h4><div class="fields">{_fields(fields)}</div>'
            + (_function_box(r["funcao"], r.get("chamada")) if r.get("funcao") else "") + "</div>")


def rule(vm):
    body = _rule_box(vm)
    if vm.get("condicao"):
        body += _condition_box(vm["condicao"])
    if vm.get("restricao"):
        body += _restriction_box(vm["restricao"], vm["regra"]["tipo"])
    svg, numbered = SubgraphDrawing(vm).draw()
    body += "<h2>Subgrafo da regra e dos modelos</h2>" + f'<div class="svg-wrap">{svg}</div>'
    rows = [[f"[{i + 1}]", e(a["tipo"]), e(a["de"]), e(a["para"]), e(a.get("texto"))] for i, a in enumerate(numbered)]
    rows += [["", e(a["tipo"]), e(a["de"]), e(a["para"]), e(a.get("texto"))] for a in vm["subgrafoRegra"]["arestas"] if a not in numbered]
    rows += [["", e(a["tipo"]), e(a["de"]), e(a["para"]), e(" ".join(x for x in (a.get("papel") or "", a.get("cardinalidade") or "") if x))]
             for a in vm["subgrafoModelos"]["arestas"]]
    body += "<h3>Todas as ligações (texto completo)</h3>" + table(["N.º", "Aresta", "De", "Para", "Texto / atributos"], rows)
    return body
