"""CIUS-PT adapters: the semantic model guide (PDF), the schematron and the annotated UBL models.

  guide(pdf)          -> groups (BG) and elements (BT) of the semantic model, with the Portuguese name, the type,
                         the CIUS-PT cardinality (the standard's goes to the notes) and the rules mentioned by each
                         field. It is the main source of the structure: semantic, independent of the XML syntax.
  schematron(folder)  -> rules: each assertion (assert/report) with the text, the severity, the context (the group),
                         the expression (the parameter of the UBL binding) and the elements it mentions (BT-n, BG-n).
  ubl(xml)            -> syntactic groups and elements of the annotated UBL model (invoice, credit note, status
                         message): Portuguese description and cardinality of each element.

The PDF is read with `pdftotext -layout` (poppler). The English names of the terms (Seller name, Invoice
number…) are taken from the rule messages and become alternative names.
"""
import re
import shutil
import subprocess
import xml.etree.ElementTree as ET
from pathlib import Path

from ..classification import base_type, classify, term_ids
from ..inventory import Element, Group, Inventory, SourceRule

CARDINALITY = r"(\d)\s?\.\.?\s?([\dN])"
RULE_IDS = re.compile(r"(BR-CIUS-PT-\d+|BR-CO-\d+|BR-[A-Z]{1,2}-\d+|BR-\d+|DT-CIUS-PT-[\d.]+)")
SCHEMATRON = "{http://purl.oclc.org/dsdl/schematron}"


def _cardinality(low, high):
    return f"{low}..{'*' if high in ('N', 'n') else high}"


def pdf_text(pdf):
    if not shutil.which("pdftotext"):
        raise RuntimeError("falta o pdftotext (poppler-utils) para ler o guia CIUS-PT")
    return subprocess.run(["pdftotext", "-layout", str(pdf), "-"], capture_output=True, text=True, check=True).stdout


# ------------------------------------------------------------------------------------------ guide
class _GuideReader:
    """Reads the two tables of the guide: the groups (BG) and the fields (BT)."""

    FIELD_ROW = re.compile(r"^\s*(BT-\d+)\s+(.+?)\s{2,}([TIDCAUPQBO])\s{2,}" + CARDINALITY + r"\d*\s+" + CARDINALITY + r"\s*(.*)$")
    GROUP_ROW = re.compile(r"^\s*(BG-\d+)\s+(.+?)\s{3,}" + CARDINALITY + r"\s+" + CARDINALITY)

    def __init__(self, pdf, english_names=None):
        self.pdf = Path(pdf)
        self.lines = pdf_text(pdf).splitlines()
        self.english_names = english_names or {}
        self.groups, self.elements = {}, {}
        self.extra = {}                       # element id -> {"standard", "columns", "notes"} while reading

    def read_group_table(self):
        """BG-n, the standard's name, the CIUS-PT designation and the BT it contains."""
        current = None
        for i, line in enumerate(self.lines):
            m = re.match(r"^\s*(BG-\d+)\s{2,}([A-Z][A-Z0-9 \-/]+?)\s{2,}(.+?)\s{2,}(.+?)\s{2,}(BT-\d+)?", line)
            if m and "group of business terms" in line:
                current = m.group(1)
                self.groups[current] = Group(current, m.group(4).strip(), source_name=m.group(2).strip(),
                                             origin=f"{self.pdf.name}: tabela de grupos")
            if not current:
                continue
            if re.match(r"^\s*(BG-\d+)\s", line) and not line.lstrip().startswith(current):
                if "group of business terms" not in line:
                    current = None
                    continue
            for bt in re.findall(r"(BT-\d+)\s*(?:SIM)?\s*$", line):
                if bt not in self.groups[current].elements:
                    self.groups[current].elements.append(bt)
            if re.search(r"Página \d+", line) or line.lstrip().startswith("ID BG"):
                continue
            if i > 0 and re.match(r"^\s*[A-Z]\S.*", line) and "Business Term" in line:
                current = None

    def read_field_table(self):
        """BT-n rows (and the BG-n rows that give the group cardinality), with their continuation lines."""
        element, group = None, None
        for line in self.lines:
            m, mg = self.FIELD_ROW.match(line), self.GROUP_ROW.match(line)
            if m:
                element = self._start_element(m, group)
                continue
            if mg:
                group = mg.group(1)
                g = self.groups.setdefault(group, Group(group, mg.group(2).strip(), origin=f"{self.pdf.name}: tabela de campos"))
                g.cardinality = _cardinality(mg.group(5), mg.group(6))
                element = None
                continue
            if element is None or not line.strip() or "Página" in line or "eSPap" in line:
                if "Página" in line:
                    element = None
                continue
            self._continue_element(element, line)

    def _start_element(self, m, group):
        element = self.elements.setdefault(m.group(1), Element(
            m.group(1), m.group(2).strip(), description=m.group(2).strip(), source_type=m.group(3), type=base_type(m.group(3)),
            cardinality=_cardinality(m.group(6), m.group(7)), group=group, origin=f"{self.pdf.name}: tabela de campos"))
        extra = self.extra.setdefault(element.id, {})
        extra["standard"] = _cardinality(m.group(4), m.group(5))
        extra["columns"] = (m.start(2), m.start(3), m.start(8))
        element.rules += [x for x in RULE_IDS.findall(m.group(8)) if x not in element.rules]
        extra["notes"] = [RULE_IDS.sub("", m.group(8)).strip()]
        return element

    def _continue_element(self, element, line):
        start, end, rules_column = self.extra[element.id]["columns"]
        if len(line) - len(line.lstrip()) < start - 4:      # text at the margin: a footnote, not the table
            return
        piece = line[start:end].strip() if len(line) > start else ""
        if piece and not re.match(r"^(BT|BG)-\d+", piece):
            element.description += " " + piece
        self.extra[element.id]["notes"].append(RULE_IDS.sub("", line[rules_column - 2:]).strip())
        for x in RULE_IDS.findall(line[end:]):
            if x not in element.rules:
                element.rules.append(x)

    def finish_elements(self):
        for element in self.elements.values():
            extra = self.extra.pop(element.id)
            element.description = re.sub(r"(\s+[A-Z])+$", "", re.sub(r"\s+", " ", element.description).strip()).strip()
            element.notes = re.sub(r"\s+", " ", " ".join(x for x in extra["notes"] if x)).strip()
            element.notes = re.sub(r"\s-\s(?=[a-záéíóúâêôãõç])", "\n- ", element.notes)
            m = re.search(r"valores admitidos:\s*([^.\n]+)", element.notes)
            if m and "lista" not in m.group(1):
                element.allowed_values = [v.strip() for v in m.group(1).split(",") if v.strip()]
            if extra.get("standard"):              # the EN 16931 cardinality is a note, not an alternative name
                element.notes = (element.notes + "\n" if element.notes else "") + f"cardinalidade na norma EN 16931: {extra['standard']}"
            element.name = element.description.split(".")[0][:120]
            element.alternative_names = [x for x in element.alternative_names if not x.startswith("cardinalidade")] + \
                                        ([self.english_names[element.id]] if element.id in self.english_names else [])
            element.rules = [r.rstrip(".") for r in element.rules if not r.endswith("-")]
            if element.group is None:
                element.group = next((g.id for g in self.groups.values() if element.id in g.elements), None)

    def complete_membership(self):
        """Add each field to the group where it appears in the field table; the fields without a group go to BG-0."""
        for element in self.elements.values():
            if element.group in self.groups and element.id not in self.groups[element.group].elements:
                self.groups[element.group].elements.append(element.id)
        if "BG-0" not in self.groups:
            self.groups["BG-0"] = Group("BG-0", "Documento de faturação", source_name="INVOICE",
                                        description="Raiz do modelo semântico: os campos sem grupo pertencem diretamente ao documento.",
                                        origin="EN 16931 (raiz implícita)")
        for element in self.elements.values():
            if element.group is None:
                element.group = "BG-0"
                self.groups["BG-0"].elements.append(element.id)


def guide(pdf, english_names=None):
    reader = _GuideReader(pdf, english_names)
    inventory = Inventory({"id": "cius-pt-guia", "nome": "Guia do modelo de dados semântico CIUS-PT (v1.1)",
                           "tipo": "norma semântica", "ficheiro": Path(pdf).name, "adaptador": "cius_pt.guia"})
    reader.read_group_table()
    reader.read_field_table()
    reader.finish_elements()
    reader.complete_membership()
    inventory.groups = sorted(reader.groups.values(), key=lambda g: int(g.id[3:]))
    inventory.elements = sorted(reader.elements.values(), key=lambda x: int(x.id[3:]))
    return inventory


# ------------------------------------------------------------------------------------------ schematron
def _parameters(folder):
    params = {}
    for f in sorted(Path(folder).rglob("*.sch")):
        for x in ET.parse(f).getroot().iter(f"{SCHEMATRON}param"):
            params[x.get("name")] = x.get("value")
    return params


def schematron(folder):
    folder = Path(folder)
    params = _parameters(folder)
    inventory = Inventory({"id": "cius-pt-schematron", "nome": "Schematron CIUS-PT 2.1.1 (urn:feap.gov.pt)",
                           "tipo": "regras de validação", "ficheiro": folder.name, "adaptador": "cius_pt.schematron"})
    seen = set()
    for f in sorted(folder.rglob("*.sch")):
        root = ET.parse(f).getroot()
        if root.tag.endswith("schema"):
            continue
        for rule in root.iter(f"{SCHEMATRON}rule"):
            ctx = rule.get("context") or ""
            ctx_name = ctx[1:] if ctx.startswith("$") else ctx
            ctx_path = params.get(ctx_name, ctx) if ctx.startswith("$") else ctx
            for assertion in list(rule):
                tag = assertion.tag.split("}")[-1]
                if tag not in ("assert", "report"):
                    continue
                rule_id = assertion.get("id")
                if (rule_id, ctx_path) in seen:
                    continue
                seen.add((rule_id, ctx_path))
                text = re.sub(r"\s+", " ", "".join(assertion.itertext())).strip()
                text = re.sub(r"^\[[^\]]+\]-?", "", text).strip()
                test = assertion.get("test") or ""
                expression = params.get(test[1:], test) if test.startswith("$") else test
                category, nature = classify(text, expression)
                inventory.rules.append(SourceRule(
                    id=rule_id if rule_id not in {r.id for r in inventory.rules} else f"{rule_id}@{ctx_name}", text=text,
                    category=category, nature=nature,
                    severity={"fatal": "erro", "warning": "aviso"}.get(assertion.get("flag"), assertion.get("flag")),
                    context=ctx_name, elements=term_ids(text),
                    expression=("report (dispara quando verdadeiro): " if tag == "report" else "") + (expression or ""),
                    origin=f"{f.relative_to(folder)}"))
    return inventory


STOP_WORDS = {"shall", "have", "has", "contain", "contains", "be", "is", "are", "an", "a", "the", "if", "when", "and", "or",
              "that", "where", "in", "case", "each", "should", "not", "provided", "filled", "equal", "than", "to", "with",
              "at", "least", "one", "only", "same", "as", "either", "both", "there", "within", "on", "by", "from", "per"}


def english_names(rules_inventory):
    """'the Seller name (BT-27)' -> {'BT-27': 'Seller name'}, from the texts of the rules (the most frequent name)."""
    counts = {}
    for r in rules_inventory.rules:
        for m in re.finditer(r"\((B[TG]-\d+)\)", r.text):
            before = re.findall(r"[A-Za-z][A-Za-z\-]*", r.text[:m.start()])[-8:]
            name = []
            for token in reversed(before):
                if token.lower() in STOP_WORDS:
                    break
                name.insert(0, token)
            if name and name[0][0].isupper() and len(name) <= 7:
                key = " ".join(name)
                counts.setdefault(m.group(1), {}).setdefault(key, 0)
                counts[m.group(1)][key] += 1
    return {bt: max(c, key=lambda k: (c[k], -len(k))) for bt, c in counts.items()}


# ------------------------------------------------------------------------------------------ annotated UBL
def _local(tag):
    return tag.split("}")[-1] if isinstance(tag, str) else None


def _ubl_cardinality(parent, child):
    """Cardinality from the comment inside the element (first child) or right after it."""
    siblings = list(parent)
    i = siblings.index(child)
    inside = [c for c in child if c.tag is ET.Comment]
    if inside and inside[0] is next(iter(child), None):
        m = re.search(CARDINALITY, inside[0].text or "")
        if m:
            return _cardinality(m.group(1), m.group(2))
    if i + 1 < len(siblings) and siblings[i + 1].tag is ET.Comment:
        m = re.search(CARDINALITY, siblings[i + 1].text or "")
        if m:
            return _cardinality(m.group(1), m.group(2))
    return None


def ubl(xml):
    xml = Path(xml)
    root = ET.parse(xml, parser=ET.XMLParser(target=ET.TreeBuilder(insert_comments=True))).getroot()
    document = re.sub(r"\s*CIUS-PT.*", "", xml.stem)
    inventory = Inventory({"id": "cius-pt-ubl-" + re.sub(r"\W+", "-", document.lower()).strip("-"),
                           "nome": f"Modelo UBL 2.1 CIUS-PT anotado: {document}", "tipo": "modelo sintático (XML anotado)",
                           "ficheiro": xml.name, "adaptador": "cius_pt.ubl"})

    def descend(node, path, group):
        for child in list(node):
            if child.tag is ET.Comment:
                continue
            name = _local(child.tag)
            child_path = f"{path}/{name}"
            sub_elements = [c for c in child if c.tag is not ET.Comment]
            text = re.sub(r"\s+", " ", (child.text or "")).strip()
            mandatory = "[OBRIGAT" in text.upper()
            description = re.sub(r"\[OBRIGAT[^\]]*\]\s*", "", text, flags=re.I).strip()
            card = _ubl_cardinality(node, child)
            if sub_elements:
                inventory.groups.append(Group(child_path, name, description=description, parent=group, cardinality=card, origin=xml.name))
                descend(child, child_path, child_path)
            else:
                notes = ("atributos no modelo: " + ", ".join(f"{k}={v}" for k, v in child.attrib.items())) if child.attrib else ""
                inventory.elements.append(Element(child_path, name, description=description,
                                                  cardinality=card or ("1..1" if mandatory else None), group=group,
                                                  origin=xml.name, notes=notes))
                if group:
                    next(g for g in inventory.groups if g.id == group).elements.append(child_path)

    root_id = "/" + _local(root.tag)
    inventory.groups.append(Group(root_id, _local(root.tag), description=f"Documento UBL {_local(root.tag)}", cardinality="1..1", origin=xml.name))
    descend(root, root_id, root_id)
    return inventory
