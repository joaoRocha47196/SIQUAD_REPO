"""Minimal SVG drawing (boxes, arrows, text) for the views drawn as diagrams."""
from .html import e

MONO = ' font-family="DejaVu Sans Mono, Menlo, monospace"'


class Svg:
    def __init__(self, width, height):
        self.width, self.height = width, height
        self.back, self.front = [], []
        self._markers = set()

    @staticmethod
    def _text_width(text, size, mono=False):
        return len(text) * size * (0.62 if mono else 0.6)

    def text(self, x, y, text, size=11, color="#222", anchor="middle", mono=False, bold=False):
        family = MONO if mono else ""
        weight = ' font-weight="bold"' if bold else ""
        self.front.append(f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" fill="{color}" text-anchor="{anchor}"'
                          f'{family}{weight}>{e(text)}</text>')

    def box_width(self, text, size=11, mono=False):
        return max(70, self._text_width(text, size, mono) + 20)

    def box(self, x, y, text, border="#333", fill="#fff", stroke_width=1.4, title=None, bold=False, mono=False,
            width=None, size=11, dashed=False, caption=None, href=None, height=26):
        w = width or self.box_width(text, size, mono)
        dash = ' stroke-dasharray="5,3"' if dashed else ""
        tooltip = f"<title>{e(title)}</title>" if title else ""
        open_a, close_a = (f'<a href="{e(href)}">', "</a>") if href else ("", "")
        family = MONO if mono else ""
        weight = ' font-weight="bold"' if bold else ""
        self.front.append(f'{open_a}<g>{tooltip}<rect x="{x - w / 2:.1f}" y="{y - height / 2:.1f}" width="{w:.1f}" height="{height}" rx="4" '
                          f'fill="{fill}" stroke="{border}" stroke-width="{stroke_width}"{dash}/>'
                          f'<text x="{x:.1f}" y="{y + size * 0.36:.1f}" font-size="{size}" fill="#1b1b1b" '
                          f'text-anchor="middle"{family}{weight}>{e(text)}</text></g>{close_a}')
        if caption:
            self.text(x - w / 2 + 3, y - height / 2 - 3, caption, 8.5, border, anchor="start")
        return w

    def rect(self, x, y, w, h, fill="#eee", border="#333", dashed=False):
        dash = ' stroke-dasharray="4,3"' if dashed else ""
        self.front.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" fill="{fill}" stroke="{border}"{dash}/>')

    def line(self, x1, y1, x2, y2, color="#555", dashed=False, stroke_width=1.2):
        dash = ' stroke-dasharray="4,3"' if dashed else ""
        self.back.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{color}" '
                         f'stroke-width="{stroke_width}"{dash}/>')

    def arrow(self, x1, y1, x2, y2, color="#555", label=None, dashed=False, label_size=9):
        dash = ' stroke-dasharray="4,3"' if dashed else ""
        marker = color.replace("#", "")
        self.back.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{color}" '
                         f'stroke-width="1.3" marker-end="url(#s{marker})"{dash}/>')
        self._markers.add(color)
        if label:
            mx, my = (x1 + x2) / 2, (y1 + y2) / 2
            w = self._text_width(label, label_size) + 6
            self.front.insert(0, f'<rect x="{mx - w / 2:.1f}" y="{my - 7:.1f}" width="{w:.1f}" height="13" fill="#fff" opacity="0.9"/>'
                              f'<text x="{mx:.1f}" y="{my + 3:.1f}" font-size="{label_size}" fill="#444" '
                              f'text-anchor="middle">{e(label)}</text>')

    def render(self):
        defs = "".join(
            f'<marker id="s{c.replace("#", "")}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" '
            f'orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{c}"/></marker>'
            for c in self._markers)
        return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.width:.0f}" height="{self.height:.0f}" '
                f'viewBox="0 0 {self.width:.0f} {self.height:.0f}" style="max-width:100%;height:auto;background:#fff">'
                f"<defs>{defs}</defs>{''.join(self.back)}{''.join(self.front)}</svg>")
