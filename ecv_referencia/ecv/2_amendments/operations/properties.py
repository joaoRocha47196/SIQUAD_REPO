"""Operations on properties: add, remove, move, rename and change."""
import copy

from ecv.shared.errors import AmendmentError

from . import operation


@operation("adicionar_propriedade")
def add_property(ds, op, step=None):
    prop = op["propriedade"]
    for props in ds.property_lists(op["nivel"], op["modelo"]):
        if any(x["nome"] == prop["nome"] for x in props):
            raise AmendmentError(f"{op['modelo']}.{prop['nome']} já existe")
        props.append(copy.deepcopy(prop))
    return f"+ {op['modelo']}.{prop['nome']}"


@operation("remover_propriedade")
def remove_property(ds, op, step=None):
    for m in ds.copies(op["nivel"], op["modelo"]):
        m["propriedades"] = [x for x in m.get("propriedades", []) if x["nome"] != op["nome"]]
    return f"- {op['modelo']}.{op['nome']}"


@operation("mover_propriedade")
def move_property(ds, op, step=None):
    source, target, name = op["de"], op["para"], op["nome"]
    origin = ds.definition(source["nivel"], source["modelo"])
    prop = next((x for x in (origin or {}).get("propriedades", []) if x["nome"] == name), None)
    if prop is None:
        raise AmendmentError(f"{source['modelo']}.{name} não existe")
    ds.require(target["nivel"], target["modelo"])
    prop = copy.deepcopy(prop)
    remove_property(ds, {"nivel": source["nivel"], "modelo": source["modelo"], "nome": name})
    for props in ds.property_lists(target["nivel"], target["modelo"]):
        if not any(x["nome"] == name for x in props):
            props.append(copy.deepcopy(prop))
    return f"{source['modelo']}.{name} → {target['modelo']}"


def _rename_in_rules_of(prop, old, new):
    for r in prop.get("regras", []):
        restriction = r.get("restricao") or {}
        if restriction.get("propriedade") == old:
            restriction["propriedade"] = new
        for term in r.get("condicao", []):
            if term.get("propriedade") == old:
                term["propriedade"] = new


@operation("renomear_propriedade")
def rename_property(ds, op, step=None):
    level, model, old, new = op["nivel"], op["modelo"], op["de"], op["para"]
    roles = ds.roles_of(level, model)
    owner_model = (level, model)
    ds.rewrite_paths(lambda segments, owner: segments[:-1] + [new] if segments[-1] == old and
                     ((len(segments) == 1 and owner == owner_model) or (len(segments) > 1 and segments[-2] in roles)) else segments)
    for props in ds.property_lists(level, model):
        for x in props:
            if x["nome"] == old:
                x["nome"] = new
                alternatives = x.setdefault("nomesAlternativos", [])
                if old not in alternatives:
                    alternatives.append(old)
                _rename_in_rules_of(x, old, new)
    return f"{model}.{old} → {new}"


@operation("alterar_propriedade")
def change_property(ds, op, step=None):
    for props in ds.property_lists(op["nivel"], op["modelo"]):
        for x in props:
            if x["nome"] == op["nome"]:
                for k in ("tipo", "descricao", "nomesAlternativos", "notas"):
                    if k in op:
                        x[k] = op[k]
    return f"alterada {op['modelo']}.{op['nome']}"
