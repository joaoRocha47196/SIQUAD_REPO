"""The catalogue of view kinds (documentacao/catalogo_vistas.json) and its two diagrams per kind: the graph entities
and edges the view walks through, and the navigation to other views."""
import json
from functools import lru_cache

from ecv import config
from ecv.views.presentation.svg import Svg

COLORS = config.COLORS
ENTITY_COLOR = {"HLM": COLORS["HLM"], "SM": COLORS["SM"], "USM": COLORS["USM"], "Propriedade": "#555555",
                "RP": COLORS["RP"], "RIR": COLORS["RIR"], "RIC": COLORS["RIC"], "Regra": "#777777",
                "Restricao": COLORS["funcao"], "CondicaoAplicabilidade": COLORS["condicao"],
                "Funcao": COLORS["externo"], "ContextoExterno": COLORS["externo"],
                "Projecao": COLORS["projecao"], "Perfil": COLORS["projecao"], "Declaracao": "#444444"}


@lru_cache(maxsize=1)
def catalogue():
    return json.loads(config.path("catalogoVistas").read_text(encoding="utf-8"))["vistas"]


def _layers(nodes, edges):
    layer = {n: 0 for n in nodes}
    for _ in range(len(nodes)):
        changed = False
        for a, _, b in edges:
            if a != b and layer[b] < layer[a] + 1 and layer[a] + 1 < len(nodes):
                layer[b] = layer[a] + 1
                changed = True
        if not changed:
            break
    return layer


def entities_diagram(entities, edges):
    """Graph entities (coloured boxes) and the edges the view walks, by layers from left to right."""
    nodes = list(dict.fromkeys(list(entities) + [x for a, _, b in edges for x in (a, b)]))
    layer = _layers(nodes, edges)
    columns = {}
    for n in nodes:
        columns.setdefault(layer[n], []).append(n)
    column_w = 270
    height = max(len(v) for v in columns.values()) * 46 + 30
    s = Svg(column_w * len(columns) + 20, height)
    pos = {}
    for c, ns in sorted(columns.items()):
        for i, n in enumerate(ns):
            pos[n] = (85 + column_w * c, 25 + (height - 50) * (i + 0.5) / len(ns))
    for a, kind, b in edges:
        (x1, y1), (x2, y2) = pos[a], pos[b]
        if a == b:
            s.text(x1, y1 - 17, f"↻ {kind}", 8.5, "#555")
            continue
        dx = 1 if x2 >= x1 else -1
        s.arrow(x1 + dx * 70, y1, x2 - dx * 70, y2, color="#777", label=kind, label_size=8)
    for n, (x, y) in pos.items():
        s.box(x, y, n, border=ENTITY_COLOR.get(n, "#666"), width=140, size=10, stroke_width=2)
    return s.render()


def navigation_diagram(kind):
    view = catalogue()[kind]
    nav = view["navegacao"]
    height = max(len(nav), 1) * 34 + 30
    w = max(170, Svg(1, 1).box_width(view["titulo"], 10))
    s = Svg(w + 500, height)
    yc = height / 2
    s.box(10 + w / 2, yc, view["titulo"], border="#5a1a2f", stroke_width=2.5, width=w, size=10, bold=True)
    for i, n in enumerate(nav):
        y = 22 + (height - 44) * (i + 0.5) / max(len(nav), 1)
        target = catalogue().get(n["para"], {}).get("titulo", n["para"])
        s.arrow(10 + w, yc, w + 255, y, color="#999", dashed=True)
        s.text(w + 130, y - 5 if y < yc else y + 11, n["por"], 8.5, "#666")
        s.box(w + 375, y, target, border="#888", width=230, size=9.5)
    return s.render()
