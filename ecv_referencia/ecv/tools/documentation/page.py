"""The page of the documentation site (side menu with every section) and an SVG diagram drawer with
clickable boxes (each box links to the page of the component)."""
import html
import math

from ecv.config import COLORS


def e(x):
    return html.escape("" if x is None else str(x))


MERMAID = ('<script src="https://cdn.jsdelivr.net/npm/mermaid@10.9.1/dist/mermaid.min.js"></script>'
           '<script>if(window.mermaid){mermaid.initialize({startOnLoad:true,securityLevel:"loose"});}</script>')

CSS = """
:root{--hlm:%(HLM)s;--sm:%(SM)s;--usm:%(USM)s;--rp:%(RP)s;--rir:%(RIR)s;--ric:%(RIC)s;--accent:#5a1a2f;--line:#dedede;--soft:#666}
*{box-sizing:border-box}
body{margin:0;font-family:Verdana,"DejaVu Sans",sans-serif;font-size:13.5px;line-height:1.5;color:#1b1b1b;background:#fff;display:flex}
aside{width:270px;min-width:270px;height:100vh;position:sticky;top:0;overflow-y:auto;background:#f7f5f6;border-right:1px solid #e2dcdf;padding:14px 12px;font-size:12.5px}
aside .brand{font-weight:bold;color:var(--accent);font-size:15px;margin-bottom:10px;display:block;text-decoration:none}
aside h4{margin:14px 0 4px;font-size:11px;text-transform:uppercase;letter-spacing:.05em;color:#8a6b77}
aside a{display:block;color:#333;text-decoration:none;padding:1px 4px;border-radius:3px}
aside a:hover{background:#ece4e8}
aside a.current{background:var(--accent);color:#fff}
aside a.sub{padding-left:16px;font-size:12px;color:#555}
aside a.sub.current{color:#fff}
main{flex:1;min-width:0;padding:22px 34px 60px;max-width:1300px}
h1{color:var(--accent);font-size:22px;margin:0 0 6px}
h2{color:var(--accent);font-size:17px;margin:28px 0 8px;border-bottom:1px solid #eee;padding-bottom:3px}
h3{font-size:14.5px;margin:20px 0 6px}
h4,h5,h6{font-size:13.5px;margin:14px 0 4px}
.crumbs{font-size:12px;color:var(--soft);margin-bottom:8px}
.crumbs a{color:var(--soft)}
.summary{font-size:14px;color:#333;background:#faf7f8;border-left:4px solid var(--accent);padding:10px 14px;margin:8px 0 16px}
table{border-collapse:collapse;width:100%%;margin:8px 0 14px;font-size:12.8px}
th,td{border-bottom:1px solid var(--line);padding:4px 8px;text-align:left;vertical-align:top}
thead th{border-bottom:2px solid #444;background:#fff}
code{font-family:"DejaVu Sans Mono",Menlo,monospace;font-size:12px;background:#f4f4f4;padding:0 3px;border-radius:3px}
pre.code{background:#f6f6f6;border:1px solid #e6e6e6;border-radius:6px;padding:10px;overflow:auto;font-size:12px;max-height:520px}
pre.code code{background:none;padding:0}
pre.mermaid{background:#fff;border:1px solid #eee;border-radius:6px;padding:8px;text-align:center}
blockquote{border-left:3px solid #ccc;margin:8px 0;padding:2px 12px;color:#444}
.diagram{overflow-x:auto;border:1px solid #eee;border-radius:8px;padding:6px;background:#fff;margin:8px 0 14px}
.diagram svg a:hover rect{stroke-width:3.2}
.note{color:var(--soft);font-size:12px}
.cards{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:12px;margin:10px 0}
.card{border:1px solid var(--line);border-radius:8px;padding:10px 12px}
.card h3{margin:0 0 4px;font-size:13.5px}
dl.io{display:grid;grid-template-columns:150px 1fr;gap:4px 14px;margin:8px 0 14px;border:1px solid var(--line);border-radius:6px;padding:10px 14px}
dl.io dt{font-weight:bold;color:var(--accent)}dl.io dd{margin:0}
details>summary{cursor:pointer;font-weight:bold;color:var(--accent)}
""" % COLORS


def table(header, rows):
    return ("<table><thead><tr>" + "".join(f"<th>{c}</th>" for c in header) + "</tr></thead><tbody>"
            + "".join("<tr>" + "".join(f"<td>{c}</td>" for c in row) + "</tr>" for row in rows) + "</tbody></table>")


def io_block(receives, needs, produces):
    """The three facts every module and step page starts with."""
    return (f'<dl class="io"><dt>Recebe</dt><dd>{receives}</dd><dt>Precisa de</dt><dd>{needs}</dd>'
            f"<dt>Produz</dt><dd>{produces}</dd></dl>")


def page(name, title, body, menu, summary=None, crumbs=None, mermaid=False):
    side = ['<aside><a class="brand" href="index.html">ECV · documentação técnica</a>']
    for section, items in menu:
        side.append(f"<h4>{e(section)}</h4>")
        for href, text, sub in items:
            css = ("current " if href == name + ".html" else "") + ("sub" if sub else "")
            side.append(f'<a class="{css.strip()}" href="{e(href)}">{e(text)}</a>')
    side.append("</aside>")
    trail = ('<div class="crumbs">' + " › ".join(f'<a href="{e(h)}">{e(t)}</a>' for h, t in crumbs) + "</div>") if crumbs else ""
    lead = f'<div class="summary">{summary}</div>' if summary else ""
    return (f'<!doctype html>\n<html lang="pt"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">'
            f"<title>{e(title)} · documentação ECV</title><style>{CSS}</style></head><body>{''.join(side)}"
            f"<main>{trail}<h1>{e(title)}</h1>{lead}{body}</main>{MERMAID if mermaid else ''}</body></html>\n")


class Diagram:
    """Boxes (title, lines of text, link) and arrows between boxes, in one SVG."""

    def __init__(self, width, height):
        self.width, self.height = width, height
        self.boxes, self.back, self.front = {}, [], []

    def group(self, x, y, w, h, title, color="#bbb"):
        self.back.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="#fcfbfb" stroke="{color}" stroke-dasharray="6,4"/>'
                         f'<text x="{x + 10}" y="{y + 16}" font-size="11.5" fill="{color}" font-weight="bold">{e(title)}</text>')

    def box(self, ident, x, y, w, h, title, lines=(), href=None, color="#5a1a2f", fill="#fff", stroke=1.8):
        self.boxes[ident] = (x, y, w, h)
        parts = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{fill}" stroke="{color}" stroke-width="{stroke}"/>',
                 f'<text x="{x + w / 2}" y="{y + 17}" font-size="12" font-weight="bold" fill="{color}" text-anchor="middle">{e(title)}</text>']
        for i, line in enumerate(lines):
            parts.append(f'<text x="{x + w / 2}" y="{y + 33 + 13 * i}" font-size="10" fill="#444" text-anchor="middle">{e(line)}</text>')
        g = f'<g><title>{e(title)}</title>{"".join(parts)}</g>'
        self.front.append(f'<a href="{e(href)}">{g}</a>' if href else g)

    def _border(self, box, px, py):
        x, y, w, h = box
        cx, cy = x + w / 2, y + h / 2
        dx, dy = px - cx, py - cy
        if dx == 0 and dy == 0:
            return cx, cy
        s = min(abs((w / 2) / dx) if dx else math.inf, abs((h / 2) / dy) if dy else math.inf)
        return cx + dx * s, cy + dy * s

    def arrow(self, a, b, label=None, color="#777", dashed=False):
        ba, bb = self.boxes[a], self.boxes[b]
        x1, y1 = self._border(ba, bb[0] + bb[2] / 2, bb[1] + bb[3] / 2)
        x2, y2 = self._border(bb, ba[0] + ba[2] / 2, ba[1] + ba[3] / 2)
        dash = ' stroke-dasharray="5,4"' if dashed else ""
        self.back.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{color}" stroke-width="1.5" marker-end="url(#m)"{dash}/>')
        if label:
            mx, my = (x1 + x2) / 2, (y1 + y2) / 2
            w = len(label) * 5.6 + 8
            self.front.append(f'<rect x="{mx - w / 2:.1f}" y="{my - 8:.1f}" width="{w:.1f}" height="14" fill="#fff" opacity="0.92"/>'
                              f'<text x="{mx:.1f}" y="{my + 3:.1f}" font-size="9.5" fill="#555" text-anchor="middle">{e(label)}</text>')

    def render(self):
        defs = ('<defs><marker id="m" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
                '<path d="M0,0 L10,5 L0,10 z" fill="#777"/></marker></defs>')
        return (f'<div class="diagram"><svg xmlns="http://www.w3.org/2000/svg" width="{self.width}" height="{self.height}" '
                f'viewBox="0 0 {self.width} {self.height}" style="max-width:100%;height:auto;font-family:Verdana,DejaVu Sans,sans-serif">'
                f'{defs}{"".join(self.back)}{"".join(self.front)}</svg></div>')


def layers(nodes, edges):
    """Layer of each node (longest path from a source), ignoring loops and cycles."""
    layer = {n: 0 for n in nodes}
    for _ in range(len(nodes)):
        changed = False
        for a, b in edges:
            if a != b and a in layer and b in layer and layer[b] < layer[a] + 1 and layer[a] + 1 < len(nodes):
                layer[b] = layer[a] + 1
                changed = True
        if not changed:
            break
    return layer


def layered_diagram(nodes, edges, href=lambda n: None, color=lambda n: "#5a1a2f", sub=lambda n: (), width=190, height=44, gx=70, gy=22,
                    label=None):
    """Automatic left-to-right diagram by layers; nodes = [ids], edges = [(a, b, text)]."""
    layer = layers(nodes, [(a, b) for a, b, *_ in edges])
    columns = {}
    for n in nodes:
        columns.setdefault(layer[n], []).append(n)
    extra = max(len(sub(n)) for n in nodes) if nodes else 0
    box_h = height + 13 * extra
    total_h = max(len(v) for v in columns.values()) * (box_h + gy) + 30 if columns else 60
    d = Diagram(len(columns) * (width + gx) + 20, total_h)
    for k, ns in sorted(columns.items()):
        y0 = (total_h - (len(ns) * (box_h + gy) - gy)) / 2
        for i, n in enumerate(ns):
            d.box(n, 10 + k * (width + gx), y0 + i * (box_h + gy), width, box_h, label(n) if label else n, sub(n), href(n), color(n))
    for a, b, *t in edges:
        if a in d.boxes and b in d.boxes and a != b:
            d.arrow(a, b, t[0] if t else None)
    return d.render()
