"""Reading and indexing an ECV declaration.

The declaration is kept as the dictionaries read from JSON (with the Portuguese keys of the format);
this class only adds indexes and traversals. It never changes or completes the declaration.
"""
import json
from dataclasses import dataclass
from pathlib import Path

from ecv import config

SECTIONS = ("contextosExternos", "funcoes", "usm", "sm", "hlm", "projecoes", "perfis")
CHILD_LEVEL = {"HLM": "SM", "SM": "USM"}
PARENT_LEVEL = {"SM": "HLM", "USM": "SM"}


@dataclass(frozen=True)
class RuleSite:
    """Where a rule is declared: the model (and the property, when the rule lives on one)."""
    rule: dict
    level: str                  # "HLM", "SM" or "USM"
    model: str                  # model name
    prop: dict | None = None          # the property, when the rule lives on one

    @property
    def id(self):
        return self.rule.get("id")

    @property
    def type(self):
        """RP, RIR or RIC, from the rule's nature."""
        return config.NATURES.get(self.rule.get("natureza"))

    @property
    def scope(self):
        """Short text of where the rule lives (e.g. 'USM Medicao.valor')."""
        base = f"{self.level} {self.model}"
        return f"{base}.{self.prop['nome']}" if self.prop else base


class Declaration:
    def __init__(self, data, origin=None):
        self.data = data
        self.origin = origin
        self.usm = self._index("usm")
        self.sm = self._index("sm")
        self.hlm = self._index("hlm")
        self.functions = self._index("funcoes")
        self.contexts = self._index("contextosExternos")
        self.projections = self._index("projecoes")
        self.profiles = self._index("perfis")

    def _index(self, section):
        return {x["nome"]: x for x in self.data.get(section, []) if "nome" in x}

    @classmethod
    def load(cls, path):
        path = Path(path)
        with path.open(encoding="utf-8") as f:
            return cls(json.load(f), origin=str(path))

    @property
    def name(self):
        return self.origin or self.data.get("declaracao", {}).get("nome", "declaração")

    @property
    def hlm_name(self):
        """The HLM the declaration describes (one declaration, one HLM)."""
        return (self.data.get("declaracao") or {}).get("hlm") or next(iter(self.hlm), None)

    # ------------------------------------------------------------------ models
    def models(self, level):
        return {"HLM": self.hlm, "SM": self.sm, "USM": self.usm}[level]

    def model(self, level, name):
        return self.models(level).get(name)

    def all_models(self):
        for level in config.LEVELS:
            for name, m in self.models(level).items():
                yield level, name, m

    def compositions(self, level, name):
        """Compositions of a model as (role, child level, child name, cardinality)."""
        m = self.model(level, name) or {}
        out = []
        for c in m.get("composicao", []):
            if "sm" in c:
                child_level, child = "SM", c["sm"]
            elif "usm" in c:
                child_level, child = "USM", c["usm"]
            else:
                continue
            out.append((c.get("papel", child), child_level, child, c.get("cardinalidade", "1..1")))
        return out

    def properties(self, level, name):
        """Properties of a USM, or residual properties of a SM. A HLM has none."""
        m = self.model(level, name) or {}
        return m.get("propriedades", []) if level in ("SM", "USM") else []

    def get_property(self, level, name, prop):
        return next((p for p in self.properties(level, name) if p.get("nome") == prop), None)

    def parents(self, level, name):
        """Models that compose (level, name) directly."""
        above = PARENT_LEVEL.get(level)
        if not above:
            return []
        return [(above, n) for n in self.models(above)
                if any(child == name and cl == level for _, cl, child, _ in self.compositions(above, n))]

    # ------------------------------------------------------------------ rules
    def rules(self):
        """All rules, with the site where each one lives."""
        for level, name, m in self.all_models():
            for r in m.get("regras", []):
                yield RuleSite(r, level, name)
            for p in m.get("propriedades", []):
                for r in p.get("regras", []):
                    yield RuleSite(r, level, name, p)

    def rule(self, rule_id):
        return next((site for site in self.rules() if site.id == rule_id), None)

    # ------------------------------------------------------------------ scenarios
    def projections_of(self, hlm):
        return [p for p in self.projections.values() if p.get("hlm") == hlm]

    def profiles_of(self, projection):
        return [p for p in self.profiles.values() if p.get("projecao") == projection]

    def to_json(self, indent=2):
        return json.dumps(self.data, ensure_ascii=False, indent=indent)
