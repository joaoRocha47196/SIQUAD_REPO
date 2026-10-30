"""Text adapter: a description of a domain in natural language (Markdown or plain text).

  markdown(path) -> one group per section (`## Name`), one element per item of a list in that section
                    (`- name (type, cardinality): description. Valores: a, b, c`), one candidate rule per sentence
                    that states an obligation or a condition ("deve", "só", "se ... então", "não pode", ...);
                    the whole text stays in the inventory (fonte.texto), so the generation reads it as written.

Nothing is required of the text: a section without a list is only a group with its description, and a text without
sections is one group. The structure is a hint; the generation (phase G) decides the ECM and the ECR.
"""
import re
from pathlib import Path

from ..classification import base_type, classify
from ..inventory import Element, Group, Inventory, SourceRule

TYPES = {"texto": "texto", "text": "texto", "string": "texto", "inteiro": "inteiro", "integer": "inteiro",
         "decimal": "decimal", "número": "decimal", "numero": "decimal", "data": "data", "date": "data",
         "booleano": "booleano", "boolean": "booleano", "sim/não": "booleano"}
CARDINALITY = {"obrigatório": "1..1", "obrigatoria": "1..1", "obrigatória": "1..1", "obrigatorio": "1..1",
               "opcional": "0..1", "um ou mais": "1..n", "vários": "0..n", "varios": "0..n", "lista": "0..n"}
RULE_WORDS = re.compile(r"\b(deve|devem|tem de|têm de|só|apenas|não pode|não podem|obrigat|se\b|quando|caso|nunca|sempre|"
                        r"no máximo|no mínimo|entre|superior|inferior|formato|must|shall|only|if)\b", re.I)
ITEM = re.compile(r"^\s*[-*]\s+\**([^:(*]+?)\**\s*(?:\(([^)]*)\))?\s*:\s*(.*)$")


def _identifier(text):
    words = re.findall(r"[A-Za-zÀ-ÿ0-9]+", text)
    return (words[0].lower() + "".join(w[:1].upper() + w[1:] for w in words[1:])) if words else "x"


def _element(group, name, attributes, description, origin):
    kind, cardinality = None, None
    for a in [x.strip().lower() for x in (attributes or "").split(",") if x.strip()]:
        kind = kind or TYPES.get(a)
        cardinality = cardinality or CARDINALITY.get(a) or (a if re.fullmatch(r"\d\.\.(\d|n)", a) else None)
    values = re.search(r"valores?\s*(?:admitidos)?\s*:\s*([^.]+)", description, re.I)
    return Element(id=f"{group.id}.{_identifier(name)}", name=name.strip(), description=description.strip(),
                   type=kind or base_type(None), source_type=attributes or None, cardinality=cardinality, group=group.id,
                   allowed_values=[v.strip() for v in values.group(1).split(",")] if values else None, origin=origin)


def markdown(path):
    path = Path(path)
    text = path.read_text(encoding="utf-8")
    title = next((line[2:].strip() for line in text.splitlines() if line.startswith("# ")), path.stem)
    inventory = Inventory({"nome": title, "tipo": "texto (linguagem natural)", "texto": text})
    group = None
    paragraph = []

    def new_group(name, line_no):
        g = Group(id=_identifier(name)[:1].upper() + _identifier(name)[1:], name=name, source_name=name, origin=f"{path.name}:{line_no}")
        inventory.groups.append(g)
        return g

    def flush_paragraph(line_no):
        nonlocal paragraph
        sentences = re.split(r"(?<=[.;!?])\s+", " ".join(paragraph).strip())
        for sentence in (s for s in sentences if s):
            if RULE_WORDS.search(sentence):
                category, nature = classify(sentence)
                inventory.rules.append(SourceRule(id=f"T{len(inventory.rules) + 1}", text=sentence, category=category, nature=nature,
                                                  context=group.id if group else None, origin=f"{path.name}:{line_no}"))
            elif group is not None and not group.description:
                group.description = sentence
        paragraph = []

    for no, line in enumerate(text.splitlines(), 1):
        if line.startswith("## "):
            flush_paragraph(no)
            group = new_group(line[3:].strip(), no)
            continue
        item = ITEM.match(line)
        if item:
            flush_paragraph(no)
            group = group or new_group(title, no)
            element = _element(group, item.group(1), item.group(2), item.group(3), f"{path.name}:{no}")
            inventory.elements.append(element)
            group.elements.append(element.id)
            if RULE_WORDS.search(item.group(3)):
                category, nature = classify(item.group(3))
                inventory.rules.append(SourceRule(id=f"T{len(inventory.rules) + 1}", text=f"{element.name}: {item.group(3).strip()}",
                                                  category=category, nature=nature, context=group.id, elements=[element.id],
                                                  origin=f"{path.name}:{no}"))
        elif line.strip() and not line.startswith("#"):
            paragraph.append(line.strip())
        else:
            flush_paragraph(no)
    flush_paragraph(len(text.splitlines()))
    if not inventory.groups:
        new_group(title, 1)
    return inventory
