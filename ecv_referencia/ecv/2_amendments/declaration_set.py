"""The set of declarations of a domain, as the operations see it.

The declarations of a domain (one per HLM) live in dominios/<d>/declaracoes/. A shared model exists,
identical, in every declaration that uses it; so an operation on a model applies to every declaration
that contains it, and composing a model into a declaration that does not have it yet copies it (with
the submodels, functions and contexts it depends on). A model, function or context created without a
declaration stays in the domain's reservoir (reservatorio.json) until something composes or calls it.
"""
import copy
import json
import os
import re
from pathlib import Path

from ecv import config
from ecv.ingestion import rule_parts as R
from ecv.ingestion.declaration import Declaration
from ecv.ingestion.descriptions import derive
from ecv.shared.errors import AmendmentError
from ecv.shared.json_format import dumps

SECTION = {"HLM": "hlm", "SM": "sm", "USM": "usm"}
SECTION_ORDER = ["$schema", "declaracao", "contextosExternos", "funcoes", "usm", "sm", "hlm", "projecoes", "perfis"]


def file_name(hlm):
    """'OrdemInstalacao' -> 'ordem_instalacao.ecv.json'."""
    out = ""
    for i, ch in enumerate(hlm):
        out += ("_" if ch.isupper() and i else "") + ch.lower()
    return out + ".ecv.json"


def empty_reservoir():
    return {"usm": [], "sm": [], "funcoes": [], "contextosExternos": []}


class DeclarationSet:
    def __init__(self, folder, declarations, reservoir, mapping):
        self.folder = Path(folder)
        self.declarations = declarations          # HLM name -> declaration data
        self.reservoir = reservoir                # {"usm": [], "sm": [], "funcoes": [], "contextosExternos": []}
        self.mapping = mapping                    # [{fonte, origem, decisao, destino|motivo, passo}]
        self.log = []

    # ------------------------------------------------------------------ files
    @classmethod
    def load(cls, domain_folder):
        folder = Path(domain_folder)
        declarations = {}
        for f in sorted((folder / "declaracoes").glob("*.ecv.json")):
            d = json.loads(f.read_text(encoding="utf-8"))
            declarations[(d.get("declaracao") or {}).get("hlm") or d["hlm"][0]["nome"]] = d
        reservoir_file = folder / "reservatorio.json"
        reservoir = json.loads(reservoir_file.read_text(encoding="utf-8")) if reservoir_file.exists() else {}
        for k in ("usm", "sm", "funcoes", "contextosExternos"):
            reservoir.setdefault(k, [])
        mapping_file = folder / "mapeamento.json"
        mapping = json.loads(mapping_file.read_text(encoding="utf-8")) if mapping_file.exists() else []
        return cls(folder, declarations, reservoir, mapping)

    @classmethod
    def empty(cls, domain_folder):
        return cls(domain_folder, {}, empty_reservoir(), [])

    def save(self):
        folder = self.folder / "declaracoes"
        folder.mkdir(parents=True, exist_ok=True)
        existing = {f.name for f in folder.glob("*.ecv.json")}
        written = set()
        for hlm, d in self.declarations.items():
            name = file_name(hlm)
            (folder / name).write_text(dumps(d), encoding="utf-8")
            written.add(name)
        for name in existing - written:
            (folder / name).unlink()
        (self.folder / "reservatorio.json").write_text(dumps(self.reservoir), encoding="utf-8")
        (self.folder / "mapeamento.json").write_text(json.dumps(self.mapping, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")

    def schema_reference(self):
        """The '$schema' of a declaration written in this domain: the schema path relative to declaracoes/."""
        return os.path.relpath(config.path("esquemaDeclaracao"), self.folder / "declaracoes").replace(os.sep, "/")

    def copy(self):
        """An independent copy (to try operations without touching the files)."""
        return DeclarationSet(self.folder, copy.deepcopy(self.declarations), copy.deepcopy(self.reservoir), copy.deepcopy(self.mapping))

    def everything(self):
        """The declarations and the reservoir, the places where models, rules and definitions can live."""
        return list(self.declarations.values()) + [self.reservoir]

    # ------------------------------------------------------------------ lookups
    @staticmethod
    def section_list(d, level):
        return d.setdefault(SECTION[level], [])

    @staticmethod
    def model_in(d, level, name):
        return next((m for m in d.get(SECTION[level], []) if m["nome"] == name), None)

    def containing(self, level, name):
        """Declarations (data) that contain the model."""
        return [d for d in self.declarations.values() if self.model_in(d, level, name)]

    def definition(self, level, name):
        for d in self.declarations.values():
            m = self.model_in(d, level, name)
            if m:
                return m
        return next((m for m in self.reservoir.get(SECTION[level], []) if m["nome"] == name), None)

    def require(self, level, name):
        if self.definition(level, name) is None:
            raise AmendmentError(f"{level} {name} não existe")

    def copies(self, level, name):
        """Every copy of the model (declarations and reservoir)."""
        return [m for d in self.everything() for m in d.get(SECTION[level], []) if m["nome"] == name]

    def property_lists(self, level, model):
        lists = [m.setdefault("propriedades", []) for m in self.copies(level, model)]
        if not lists:
            raise AmendmentError(f"{level} {model} não existe")
        return lists

    def nodes_at(self, where):
        """The copies of the model (or of its property) named by {nivel, modelo, propriedade?}."""
        models = self.copies(where["nivel"], where["modelo"])
        if not models:
            raise AmendmentError(f"{where['nivel']} {where['modelo']} não existe")
        if not where.get("propriedade"):
            return models
        out = []
        for m in models:
            prop = next((x for x in m.get("propriedades", []) if x["nome"] == where["propriedade"]), None)
            if prop is None:
                raise AmendmentError(f"{where['modelo']}.{where['propriedade']} não existe")
            out.append(prop)
        return out

    def all_rules(self):
        """(list holding the rule, rule, declaration data, (level, model) where it lives)."""
        for d in self.everything():
            for section in ("usm", "sm", "hlm"):
                for m in d.get(section, []):
                    for r in m.get("regras", []):
                        yield m["regras"], r, d, (section.upper(), m["nome"])
                    for p in m.get("propriedades", []):
                        for r in p.get("regras", []):
                            yield p["regras"], r, d, (section.upper(), m["nome"])

    def declaration_of(self, hlm):
        if hlm not in self.declarations:
            raise AmendmentError(f"HLM {hlm} não existe")
        return self.declarations[hlm]

    def roles_of(self, level, name):
        """The path segments that reach the model: its name and the roles of the compositions that refer to it."""
        key = SECTION[level]
        out = {name}
        for d in self.everything():
            for section in ("hlm", "sm"):
                for m in d.get(section, []):
                    for c in m.get("composicao", []):
                        if c.get(key) == name:
                            out.add(c.get("papel") or name)
        return out

    # ------------------------------------------------------------------ paths
    def rewrite_paths(self, transform):
        """Apply transform(segments, owner) -> segments to every path: projections, profiles and mapping destinations
        (from the HLM; owner None) and rules (relative to their model; owner = (level, model) where the rule lives)."""
        def rewrite(path, owner=None):
            if not isinstance(path, str) or not path:
                return path
            tail = ".*" if path.endswith(".*") else ""
            segments = path[:-2].split(".") if tail else path.split(".")
            return ".".join(transform(segments, owner)) + tail

        for d in self.everything():
            for projection in d.get("projecoes", []):
                for key in ("obrigatorias", "permitidas"):
                    projection[key] = [rewrite(x) for x in projection.get(key, [])]
            for profile in d.get("perfis", []):
                for fx in profile.get("fixa", []):
                    if "propriedade" in fx:
                        fx["propriedade"] = rewrite(fx["propriedade"])
        for entry in self.mapping:                    # mapping destinations: HLM:<Hlm>/<path from the HLM>
            m = re.match(r"^(HLM:\w+/)(.+)$", entry.get("destino") or "")
            if m:
                entry["destino"] = m.group(1) + rewrite(m.group(2))
        for _, rule, _, owner in self.all_rules():
            restriction = rule.get("restricao") or {}
            if restriction.get("propriedade"):
                restriction["propriedade"] = rewrite(restriction["propriedade"], owner)
            for part in [restriction] + list(rule.get("condicao", [])):
                if part.get("propriedade") and part is not restriction:
                    part["propriedade"] = rewrite(part["propriedade"], owner)
                for a in (part.get("chamada") or {}).get("argumentos", []):
                    if "caminho" in a:
                        a["caminho"] = rewrite(a["caminho"], owner)

    # ------------------------------------------------------------------ copying between declarations
    def copy_into(self, d, level, name):
        """Make sure the model (and the submodels it composes) exists in declaration d."""
        if self.model_in(d, level, name):
            return
        m = self.definition(level, name)
        if m is None:
            raise AmendmentError(f"{level} {name} não existe em nenhuma declaração nem no reservatório")
        self.section_list(d, level).append(copy.deepcopy(m))
        for c in m.get("composicao", []):
            self.copy_into(d, "SM" if "sm" in c else "USM", c.get("sm") or c.get("usm"))
        if level != "HLM":
            self.reservoir[SECTION[level]] = [x for x in self.reservoir.get(SECTION[level], []) if x["nome"] != name]

    def _shared_definition(self, section, name):
        for d in self.declarations.values():
            found = next((f for f in d.get(section, []) if f["nome"] == name), None)
            if found:
                return found
        return next((f for f in self.reservoir.get(section, []) if f["nome"] == name), None)

    def sync_functions_and_contexts(self):
        """Each declaration gets the functions and contexts its rules use (copied from another declaration or the reservoir)."""
        for d in self.declarations.values():
            used, contexts = set(), set()
            for site in Declaration(d).rules():
                used |= {c["funcao"] for _, _, c in R.function_calls(site.rule)}
                contexts |= {t["contexto"] for t in R.condition(site.rule) if t.get("contexto")}
            for profile in d.get("perfis", []):
                contexts |= {fx["contexto"] for fx in profile.get("fixa", []) if "contexto" in fx}
            for name in used:
                if not any(x["nome"] == name for x in d.get("funcoes", [])):
                    definition = self._shared_definition("funcoes", name)
                    if definition is None:
                        raise AmendmentError(f"a função {name} é chamada mas não está definida (definir_funcao)")
                    d.setdefault("funcoes", []).append(copy.deepcopy(definition))
            for f in d.get("funcoes", []):
                contexts |= set(f.get("contextosExternos", []))
            for name in contexts:
                if not any(x["nome"] == name for x in d.get("contextosExternos", [])):
                    definition = self._shared_definition("contextosExternos", name)
                    if definition is None:
                        raise AmendmentError(f"o contexto externo {name} é usado mas não está definido (definir_contexto)")
                    d.setdefault("contextosExternos", []).append(copy.deepcopy(definition))

    @staticmethod
    def order_sections(d):
        ordered = {k: d[k] for k in SECTION_ORDER if k in d and (d[k] or k in ("usm", "hlm", "declaracao"))}
        ordered.update({k: v for k, v in d.items() if k not in ordered and k not in SECTION_ORDER})
        d.clear()
        d.update(ordered)

    def refresh(self):
        """After a batch of operations: functions and contexts in sync, sections in order, rule descriptions re-derived."""
        self.sync_functions_and_contexts()
        for d in self.declarations.values():
            self.order_sections(d)
            for site in Declaration(d).rules():
                site.rule["descricao"] = derive(site.rule, site.level, site.model)
