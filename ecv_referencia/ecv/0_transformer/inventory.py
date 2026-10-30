"""The inventory: the neutral intermediate format each source is extracted into (phase 0).

An inventory has three lists, each item with its origin (file and location in the source):

  groups    sets of elements with their own meaning in the source (a BG of CIUS-PT, an FM record, a
            Dart class, a Smart Data Models model or common definition);
  elements  the atomic information (a BT, a field, a property): name, description, base type,
            cardinality, owning group and the allowed values when the source lists them;
  rules     what the source declares as rules (schematron assertions, enum, minimum and maximum,
            formats, required), with the text, the elements they mention, the severity, the category
            and the probable ECR nature (RE, RP, RIR, RIC or function), a hint for steps B to E.

The inventory is not ECM yet: the groups are the source's and need not become submodels. Step A
decides the ECM structure from the groups and elements of every source of the domain.

The JSON file keeps the Portuguese keys of the format (read by the prompts and by the web application).
"""
import json
from dataclasses import dataclass, field, fields
from pathlib import Path


def _serialise(item, key_names):
    return {key_names.get(f.name, f.name): getattr(item, f.name) for f in fields(item)}


@dataclass
class Group:
    id: str
    name: str
    description: str = ""
    source_name: str = ""
    parent: str | None = None
    cardinality: str | None = None
    elements: list = field(default_factory=list)
    origin: str = ""

    KEYS = {"name": "nome", "description": "descricao", "source_name": "nomeOrigem", "parent": "pai",
            "cardinality": "cardinalidade", "elements": "elementos", "origin": "origem"}

    def to_dict(self):
        return _serialise(self, self.KEYS)


@dataclass
class Element:
    id: str
    name: str
    description: str = ""
    type: str | None = None
    source_type: str | None = None
    cardinality: str | None = None
    group: str | None = None
    alternative_names: list = field(default_factory=list)
    allowed_values: list | None = None
    rules: list = field(default_factory=list)
    notes: str = ""
    origin: str = ""

    KEYS = {"name": "nome", "description": "descricao", "type": "tipo", "source_type": "tipoOrigem",
            "cardinality": "cardinalidade", "group": "grupo", "alternative_names": "nomesAlternativos",
            "allowed_values": "valoresAdmitidos", "rules": "regras", "notes": "notas", "origin": "origem"}

    def to_dict(self):
        return _serialise(self, self.KEYS)


@dataclass
class SourceRule:
    id: str
    text: str
    category: str = "outra"
    nature: str = "?"
    severity: str | None = None
    context: str | None = None
    elements: list = field(default_factory=list)
    expression: str | None = None
    origin: str = ""

    KEYS = {"text": "texto", "category": "categoria", "nature": "natureza", "severity": "gravidade",
            "context": "contexto", "elements": "elementos", "expression": "expressao", "origin": "origem"}

    def to_dict(self):
        return _serialise(self, self.KEYS)


@dataclass
class Inventory:
    source: dict
    groups: list = field(default_factory=list)
    elements: list = field(default_factory=list)
    rules: list = field(default_factory=list)

    def rules_by_category(self):
        counts = {}
        for r in self.rules:
            counts[r.category] = counts.get(r.category, 0) + 1
        return dict(sorted(counts.items()))

    def to_dict(self):
        return {"fonte": self.source,
                "contagens": {"grupos": len(self.groups), "elementos": len(self.elements), "regras": len(self.rules),
                              "regrasPorCategoria": self.rules_by_category()},
                "grupos": [g.to_dict() for g in self.groups], "elementos": [x.to_dict() for x in self.elements],
                "regras": [r.to_dict() for r in self.rules]}

    def summary(self):
        return f"{len(self.groups)} grupos, {len(self.elements)} elementos, {len(self.rules)} regras"

    def save(self, path):
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        Path(path).write_text(json.dumps(self.to_dict(), ensure_ascii=False, indent=1) + "\n", encoding="utf-8")


def load(path):
    """An inventory file, as the JSON dictionary (keys of the format)."""
    return json.loads(Path(path).read_text(encoding="utf-8"))
