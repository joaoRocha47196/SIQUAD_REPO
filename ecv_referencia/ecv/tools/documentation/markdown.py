"""A minimal Markdown to HTML converter (standard library only), to bring the specs and the README files into the
documentation site: headings (with anchors), paragraphs, bold, code, links, lists, tables, code blocks (mermaid
blocks stay as diagrams, drawn by the mermaid library in the browser), quotes and horizontal rules. Links are
rewritten by the given function (a known .md file becomes its HTML page)."""
import html
import re

LIST_ITEM = re.compile(r"^\s*([-*]|\d+\.)\s+")
TABLE_RULE = re.compile(r"^\s*\|[\s\-:|]+\|\s*$")
BLOCK_START = re.compile(r"^(#{1,6}\s|```|\s*\||\s*([-*]|\d+\.)\s|>)")


def anchor(text):
    t = re.sub(r"<[^>]+>|`", "", text).strip().lower()
    t = t.translate(str.maketrans("áàâãéêíóôõúçÁÀÂÃÉÊÍÓÔÕÚÇ", "aaaaeeiooouc" + "aaaaeeiooouc"))
    return re.sub(r"[^a-z0-9]+", "-", t).strip("-")


def inline(text, link):
    out = []
    for part in re.split(r"(`[^`]+`)", text):
        if part.startswith("`") and part.endswith("`") and len(part) > 1:
            out.append(f"<code>{html.escape(part[1:-1])}</code>")
            continue
        part = html.escape(part, quote=False)
        part = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", part)
        part = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", lambda m: f'<a href="{html.escape(link(m.group(2)))}">{m.group(1)}</a>', part)
        out.append(part)
    return "".join(out)


class _Converter:
    def __init__(self, text, link):
        self.lines = re.sub(r"<!--.*?-->", "", text, flags=re.S).splitlines()
        self.link = link
        self.i = 0
        self.out = []
        self.toc = []

    @property
    def line(self):
        return self.lines[self.i]

    def more(self):
        return self.i < len(self.lines)

    def run(self):
        while self.more():
            line = self.line
            if line.startswith("```"):
                self.code_block()
            elif re.match(r"^(#{1,6})\s+(.*)$", line):
                self.heading()
            elif line.strip().startswith("|") and self.i + 1 < len(self.lines) and TABLE_RULE.match(self.lines[self.i + 1]):
                self.table()
            elif LIST_ITEM.match(line):
                self.list_block()
            elif line.startswith(">"):
                self.quote()
            elif re.match(r"^\s*(---|\*\*\*)\s*$", line):
                self.out.append("<hr>")
                self.i += 1
            elif not line.strip():
                self.i += 1
            else:
                self.paragraph()
        return "\n".join(self.out), self.toc

    def code_block(self):
        lang = self.line[3:].strip()
        self.i += 1
        block = []
        while self.more() and not self.line.startswith("```"):
            block.append(self.line)
            self.i += 1
        self.i += 1
        content = html.escape("\n".join(block))
        self.out.append(f'<pre class="mermaid">{content}</pre>' if lang == "mermaid" else f'<pre class="code"><code>{content}</code></pre>')

    def heading(self):
        m = re.match(r"^(#{1,6})\s+(.*)$", self.line)
        level, title = len(m.group(1)), m.group(2)
        a = anchor(title)
        self.toc.append((level, title, a))
        tag = f"h{min(level + 1, 6)}"
        self.out.append(f'<{tag} id="{a}">{inline(title, self.link)}</{tag}>')
        self.i += 1

    def table(self):
        header = [c.strip() for c in self.line.strip().strip("|").split("|")]
        self.i += 2
        rows = []
        while self.more() and self.line.strip().startswith("|"):
            cells = re.split(r"(?<!\\)\|", self.line.strip().strip("|"))
            rows.append([c.strip().replace("\\|", "|") for c in cells])
            self.i += 1
        self.out.append("<table><thead><tr>" + "".join(f"<th>{inline(c, self.link)}</th>" for c in header) + "</tr></thead><tbody>"
                        + "".join("<tr>" + "".join(f"<td>{inline(c, self.link)}</td>" for c in r) + "</tr>" for r in rows) + "</tbody></table>")

    def list_block(self):
        ordered = bool(re.match(r"^\s*\d+\.", self.line))
        base = len(self.line) - len(self.line.lstrip())
        items = []                       # [text, sub-list ordered, [sub-items]]
        while self.more() and (LIST_ITEM.match(self.line) or (self.line.startswith("   ") and self.line.strip())):
            line = self.line
            indent = len(line) - len(line.lstrip())
            if LIST_ITEM.match(line):
                text = LIST_ITEM.sub("", line)
                if indent > base + 1 and items:
                    if not items[-1][2]:
                        items[-1][1] = bool(re.match(r"^\s*\d+\.", line))
                    items[-1][2].append(text)
                else:
                    items.append([text, False, []])
            elif items[-1][2]:
                items[-1][2][-1] += " " + line.strip()
            else:
                items[-1][0] += " " + line.strip()
            self.i += 1
        tag = "ol" if ordered else "ul"
        self.out.append(f"<{tag}>" + "".join(self._item(x) for x in items) + f"</{tag}>")

    def _item(self, item):
        text, sub_ordered, subs = item
        sub = ""
        if subs:
            tag = "ol" if sub_ordered else "ul"
            sub = f"<{tag}>" + "".join(f"<li>{inline(y, self.link)}</li>" for y in subs) + f"</{tag}>"
        return f"<li>{inline(text, self.link)}{sub}</li>"

    def quote(self):
        block = []
        while self.more() and self.line.startswith(">"):
            block.append(self.line[1:].strip())
            self.i += 1
        self.out.append(f"<blockquote>{inline(' '.join(block), self.link)}</blockquote>")

    def paragraph(self):
        lines = [self.line]
        self.i += 1
        while self.more() and self.line.strip() and not BLOCK_START.match(self.line):
            lines.append(self.line)
            self.i += 1
        self.out.append(f"<p>{inline(' '.join(x.strip() for x in lines), self.link)}</p>")


def convert(text, link=lambda x: x):
    """(html, toc) where toc = [(level, title, anchor)]."""
    return _Converter(text, link).run()
