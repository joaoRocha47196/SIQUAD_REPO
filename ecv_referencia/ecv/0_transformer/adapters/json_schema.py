"""JSON Schema adapter (Smart Data Models): models, common definitions, properties and candidate rules.

  smart_data_models(folder) -> one group per model (`<Model>/schema.json`) and per common definition it refers
                               to (GSMA-Commons, Location-Commons, Device-Commons, ...); one element per property,
                               with the base type, the format, the description (without the "Property. Model:..."
                               prefix) and the schema.org model as source type; candidate rules for `enum` (values),
                               `minimum`/`maximum` (range), `format` and `pattern` (format) and `required` (presence).
                               Values the source only lists in the description ("Enum:'a, b'" or "Enum: [A, B]")
                               also count as allowed values.

The common definitions stay as groups of their own because in the source they already are reused sets:
natural USM candidates for step A (but step A decides).
"""
import json
import re
from pathlib import Path

from ..classification import base_type
from ..inventory import Element, Group, Inventory, SourceRule


def _description(text):
    """(description without the prefixes and annotations, schema.org model name)."""
    text = text or ""
    model = re.search(r"Model:\s*'([^']+)'", text)
    clean = re.sub(r"^(Property|Relationship|GeoProperty)\.\s*", "", text)
    clean = re.sub(r"(Enum:\s*('[^']*'|\[[^\]]*\])\.?\s*)|(Model:\s*'[^']*'\.?\s*)|(Units:\s*'[^']*'\.?\s*)", "", clean).strip()
    return clean, (model.group(1).rsplit("/", 1)[-1] if model else None)


def _enum_in_description(text):
    """Enumerated values the source only writes in the description: "Enum:'a, b, c'" or "Enum: [A, B, C]"."""
    m = re.search(r"Enum:\s*(?:'([^']*)'|\[([^\]]*)\])", text or "")
    if not m:
        return None
    values = [v.strip() for v in (m.group(1) or m.group(2)).split(",") if v.strip()]
    return values or None


def _ref_name(ref):
    return ref.split("#/definitions/")[-1] if "#/definitions/" in ref else ref


class _SchemaReader:
    def __init__(self, folder):
        self.folder = Path(folder)
        self.definitions = {}
        for f in ("common-schema.json", "device-schema.json"):
            if (self.folder / f).exists():
                self.definitions.update(json.loads((self.folder / f).read_text(encoding="utf-8")).get("definitions", {}))
        self.inventory = Inventory({"id": "sdm-device", "nome": "Smart Data Models: dataModel.Device",
                                    "tipo": "modelos JSON Schema", "ficheiro": self.folder.name, "adaptador": "json_schema.smart_data_models"})
        self.done = set()
        self.included = {}                    # model group id -> common definitions it includes

    def read_properties(self, group_id, props, origin, required=()):
        group = next(x for x in self.inventory.groups if x.id == group_id)
        for name, p in props.items():
            target = p
            alternatives = p.get("oneOf") or p.get("anyOf")
            if "$ref" in p:
                target = self.definitions.get(_ref_name(p["$ref"]), {})
            if "items" in p and isinstance(p["items"], dict) and "$ref" in p["items"]:
                target = {**p, "tipoItens": _ref_name(p["items"]["$ref"])}
            text, model = _description(p.get("description") or target.get("description"))
            json_type = target.get("type") or (alternatives[0].get("type") if alternatives else None)
            if isinstance(json_type, list):
                json_type = next((t for t in json_type if t != "null"), json_type[0])
            fmt = target.get("format")
            ecv_type = "data" if fmt in ("date-time", "date") else base_type(json_type)
            element = Element(f"{group_id}.{name}", name, description=text, type=ecv_type if json_type not in ("array", "object") else None,
                              source_type=" ".join(x for x in (json_type, f"format={fmt}" if fmt else "", model or "",
                                                               f"itens={target.get('tipoItens')}" if target.get("tipoItens") else "",
                                                               f"ref={_ref_name(p['$ref'])}" if "$ref" in p else "") if x),
                              cardinality="0..*" if json_type == "array" else ("1..1" if name in required else "0..1"),
                              group=group_id,
                              allowed_values=target.get("enum") or (target.get("items") or {}).get("enum")
                              or _enum_in_description(p.get("description") or target.get("description")), origin=origin)
            if json_type == "object" and target.get("properties"):
                element.notes = "objeto com " + ", ".join(target["properties"])
            self.inventory.elements.append(element)
            group.elements.append(element.id)
            self.candidate_rules(element, target, alternatives, origin, name in required)

    def candidate_rules(self, element, target, alternatives, origin, required):
        rules = self.inventory.rules
        if element.allowed_values:
            rules.append(SourceRule(f"{element.id}-ENUM", f"{element.name} é um de {', '.join(map(str, element.allowed_values))}.",
                                    "valores", "RP", context=element.group, elements=[element.id],
                                    expression=f"IN {element.allowed_values}", origin=origin))
        for source in [target] + list(alternatives or []):
            if "minimum" in source or "maximum" in source:
                suffix = "" if source is target else "-" + str((alternatives or []).index(source) + 1)
                rules.append(SourceRule(f"{element.id}-GAMA{suffix}",
                                        f"{element.name} entre {source.get('minimum', '−∞')} e {source.get('maximum', '+∞')}"
                                        + (" (uma das alternativas)" if source is not target else "") + ".",
                                        "gama", "RP", context=element.group, elements=[element.id],
                                        expression=f"RANGE [{source.get('minimum')}, {source.get('maximum')}]", origin=origin))
        if target.get("format") or target.get("pattern"):
            rules.append(SourceRule(f"{element.id}-FORMATO", f"{element.name} segue o formato {target.get('format') or target.get('pattern')}.",
                                    "formato", "RP", context=element.group, elements=[element.id],
                                    expression=target.get("pattern") or f"format={target.get('format')}", origin=origin))
        if required:
            rules.append(SourceRule(f"{element.id}-OBRIGATORIA", f"{element.name} é obrigatória em {element.group}.",
                                    "presenca", "RE", context=element.group, elements=[element.id], expression="required", origin=origin))

    def read_definition(self, name, origin):
        if name in self.done or name not in self.definitions:
            return
        self.done.add(name)
        d = self.definitions[name]
        self.inventory.groups.append(Group(name, name, description=_description(d.get("description"))[0] or f"Definição comum {name}",
                                           source_name=name, origin=origin))
        self.read_properties(name, d.get("properties", {}), origin, d.get("required", ()))

    def read_model(self, f):
        schema = json.loads(f.read_text(encoding="utf-8"))
        name = f.parent.name
        origin = f"{f.parent.name}/{f.name}"
        parts = schema.get("allOf", [schema])
        common = [_ref_name(p["$ref"]) for p in parts if "$ref" in p]
        group = Group(name, schema.get("title") or name, description=_description(schema.get("description"))[0], source_name=name, origin=origin)
        self.inventory.groups.append(group)
        group.description += (" Inclui as definições comuns: " + ", ".join(common) + ".") if common else ""
        for c in common:
            self.read_definition(c, "common-schema.json" if c != "Device-Commons" else "device-schema.json")
        props = {}
        for p in parts:
            props.update(p.get("properties", {}))
        self.read_properties(name, props, origin, schema.get("required", ()))
        self.included[name] = common

    def finish(self):
        """Record, in each model, the common definitions it includes (as a composition hint)."""
        for group in self.inventory.groups:
            if group.id in self.included:
                group.description = group.description.strip()
                group.elements = [f"inclui:{c}" for c in self.included[group.id]] + group.elements
        return self.inventory


def smart_data_models(folder):
    reader = _SchemaReader(folder)
    for f in sorted(Path(folder).glob("*/schema.json")):
        reader.read_model(f)
    return reader.finish()
