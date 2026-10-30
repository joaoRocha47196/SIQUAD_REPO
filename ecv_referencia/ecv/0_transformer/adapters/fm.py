"""FM adapters (invoicing and sales system): the Dart classes and the layout of the export records.

  dart(folder)    -> one group per class (and per enum), one element per field, with the Dart type mapped to a base
                     type; a field whose type is another class (or a list of it) keeps `tipoOrigem` = the class: a
                     composition hint for step A.
  records(xlsx)   -> one group per record (VDM, CLI, STK, ...), one element per field, with the length, the record
                     type (C, N(8.2), D, L), the remarks and, when it exists, the matching Dart property (alternative
                     name). The length gives a candidate format rule.

Only the record layout is read: the data files (Dados_Imp.txt) hold personal data and are never read.
"""
import re
import zipfile
from pathlib import Path

from ..classification import base_type
from ..inventory import Element, Group, Inventory, SourceRule

CLASS_LINE = re.compile(r"^(?:abstract\s+)?class\s+(\w+)")
ENUM_BLOCK = re.compile(r"^enum\s+(\w+)\s*\{([^}]*)\}", re.S | re.M)
FIELD_LINE = re.compile(r"^\s{2}(?:final\s+|late\s+)?([A-Za-z_][\w<>?, ]*?)\s+([a-z_]\w*)\s*(?:=\s*[^;]+)?;\s*(?://\s*(.*))?$")


def _dart_type(t):
    """(type, is_list) of a Dart declaration ('List<Article>?' -> ('Article', True))."""
    t = t.strip().rstrip("?")
    m = re.match(r"List<(\w+)\??>", t)
    if m:
        return m.group(1), True
    return t, False


class _DartReader:
    def __init__(self, folder):
        self.folder = Path(folder)
        self.texts = {f: f.read_text(encoding="utf-8", errors="replace") for f in sorted(self.folder.rglob("*.dart"))}
        self.classes = set()
        for text in self.texts.values():
            self.classes |= set(re.findall(r"^(?:abstract\s+)?class\s+(\w+)", text, re.M)) | set(re.findall(r"^enum\s+(\w+)", text, re.M))
        self.inventory = Inventory({"id": "fm-dart", "nome": "Modelos Dart da aplicação FM", "tipo": "modelo de aplicação (classes)",
                                    "ficheiro": self.folder.name, "adaptador": "fm.dart"})

    def read(self):
        for f, text in self.texts.items():
            origin = str(f.relative_to(self.folder.parent))
            self._read_enums(text, origin)
            self._read_classes(text, origin)
        self._mark_required()
        return self.inventory

    def _read_enums(self, text, origin):
        for m in ENUM_BLOCK.finditer(text):
            values = [v.strip() for v in m.group(2).split(",") if v.strip()]
            self.inventory.groups.append(Group(m.group(1), m.group(1), description=f"Enumerado {m.group(1)}: {', '.join(values)}", origin=origin))
            self.inventory.rules.append(SourceRule(f"{m.group(1)}-valores", f"Os valores de {m.group(1)} são {', '.join(values)}.",
                                                   category="valores", nature="RP", origin=origin, context=m.group(1)))

    def _read_classes(self, text, origin):
        current, depth = None, 0
        for line in text.splitlines():
            mc = CLASS_LINE.match(line)
            if mc:
                current = mc.group(1)
                self.inventory.groups.append(Group(current, current, description=f"Classe {current}", origin=origin))
                depth = 0
            if current is None:
                continue
            depth += line.count("{") - line.count("}")
            if depth == 1 and not line.strip().startswith(("static", "const", "//", "@")) and "(" not in line:
                mf = FIELD_LINE.match(line)
                if mf:
                    self._add_field(current, mf, origin)
            if depth <= 0 and "}" in line:
                current = None

    def _add_field(self, class_name, m, origin):
        field_type, is_list = _dart_type(m.group(1))
        name = m.group(2)
        element = Element(f"{class_name}.{name}", name, description=(m.group(3) or "").strip(),
                          type=None if field_type in self.classes else base_type(field_type),
                          source_type=("List<" + field_type + ">") if is_list else field_type,
                          cardinality="0..*" if is_list else None, group=class_name, origin=origin)
        if field_type in self.classes:
            element.notes = f"referência à classe {field_type}" + (" (lista)" if is_list else "")
        self.inventory.elements.append(element)
        next(g for g in self.inventory.groups if g.id == class_name).elements.append(element.id)

    def _mark_required(self):
        """Fields declared 'required this.x' in a constructor are mandatory (1..1)."""
        required = {}
        for text in self.texts.values():
            for m in re.finditer(r"(\w+)\(\{(.*?)\}\);", text, re.S):
                required[m.group(1)] = set(re.findall(r"required\s+this\.(\w+)", m.group(2)))
        for element in self.inventory.elements:
            class_name, name = element.id.split(".", 1)
            if name in required.get(class_name, set()) and element.cardinality is None:
                element.cardinality = "1..1"


def dart(folder):
    return _DartReader(folder).read()


def _xlsx_cells(path):
    """Cells of an xlsx sheet: {(row, column): text}, with the standard library only."""
    z = zipfile.ZipFile(path)
    shared = [''.join(re.findall(r'<t[^>]*>([^<]*)</t>', x)) for x in
              re.findall(r'<si>(.*?)</si>', z.read('xl/sharedStrings.xml').decode(), re.S)]
    sheet = z.read('xl/worksheets/sheet1.xml').decode()
    cells = {}
    for row in re.findall(r'<row r="(\d+)"[^>]*>(.*?)</row>', sheet, re.S):
        for col, attrs, v in re.findall(r'<c r="([A-Z]+)\d+"([^>]*?)(?:/>|>(?:<f>[^<]*</f>)?(?:<v>([^<]*)</v>)?</c>)', row[1]):
            if v == "":
                continue
            if 't="s"' in attrs:
                v = shared[int(v)]
            cells[(int(row[0]), col)] = v.replace("&gt;", ">").replace("&lt;", "<").replace("&amp;", "&").strip()
    return cells


def _column(col, offset):
    """Column letters 'offset' columns to the right of 'col'."""
    n = 0
    for ch in col:
        n = n * 26 + ord(ch) - 64
    n += offset
    s = ""
    while n:
        n, r = divmod(n - 1, 26)
        s = chr(65 + r) + s
    return s


def records(xlsx):
    xlsx = Path(xlsx)
    cells = _xlsx_cells(xlsx)
    inventory = Inventory({"id": "fm-registos", "nome": "Desenho dos registos de exportação FM",
                           "tipo": "formato de ficheiro (registos de largura fixa)", "ficheiro": xlsx.name, "adaptador": "fm.registos"})
    for (row, col), v in sorted(cells.items()):
        m = re.match(r"Registo:\s*(\w+)", v)
        if m:
            _read_record(inventory, cells, xlsx, row, col, m.group(1))
    return inventory


def _read_record(inventory, cells, xlsx, row, col, record):
    title = cells.get((row, _column(col, 2)), "")
    group = Group(record, title or record, description=f"Registo {record}" + (f": {title}" if title else ""), source_name=record, origin=xlsx.name)
    inventory.groups.append(group)
    line = row + 1
    while line < row + 4 and cells.get((line, col)) != "Campo":
        line += 1
    line += 1
    while True:
        field_name = cells.get((line, col))
        if not field_name or field_name.startswith("Registo:"):
            break
        if field_name != "Tipo Registo":
            length, field_type, file_name, remarks = (cells.get((line, _column(col, k))) for k in (1, 2, 3, 4))
            dart_property = cells.get((line, _column(col, 8))) if record == "CLI" else None
            element = Element(f"{record}.{field_name}", field_name, description=field_name, type=base_type(field_type), source_type=field_type,
                              group=record,
                              alternative_names=[x.strip() for x in re.split(r"\+|\(", dart_property or "") if x.strip() and x.strip() != "fallback)"],
                              notes="; ".join(x for x in (f"comprimento {length}" if length else "", f"ficheiro {file_name}" if file_name else "",
                                                          remarks or "") if x),
                              origin=f"{xlsx.name}: registo {record}")
            inventory.elements.append(element)
            group.elements.append(element.id)
            if length and length.isdigit() and (field_type or "C").startswith("C"):
                inventory.rules.append(SourceRule(f"{record}-{len(group.elements)}-COMPRIMENTO", f"{field_name} tem no máximo {length} caracteres.",
                                                  category="formato", nature="RP", context=record, elements=[element.id],
                                                  expression=f"LENGTH [0, {length}]", origin=element.origin))
        line += 1
