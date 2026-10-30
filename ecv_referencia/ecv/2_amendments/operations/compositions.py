"""Operations on compositions: compose, remove and change (cardinality or role)."""
import copy

from ecv.shared.errors import AmendmentError

from . import operation


def _child_key(child):
    return ("sm" if child["nivel"] == "SM" else "usm"), child["nome"]


def _matches(c, key, name, role):
    return c.get(key) == name and (role is None or (c.get("papel") or name) == role)


@operation("compor")
def compose(ds, op, step=None):
    parent, child = op["pai"], op["filho"]
    ds.require(parent["nivel"], parent["nome"])
    ds.require(child["nivel"], child["nome"])
    key, name = _child_key(child)
    composition = {key: name, "cardinalidade": op["cardinalidade"]}
    if op.get("papel") and op["papel"] != name:
        composition["papel"] = op["papel"]
    for d in ds.containing(parent["nivel"], parent["nome"]):
        ds.copy_into(d, child["nivel"], name)
    for m in ds.copies(parent["nivel"], parent["nome"]):
        role = composition.get("papel") or name
        if any(x.get(key) == name and (x.get("papel") or name) == role for x in m.get("composicao", [])):
            raise AmendmentError(f"{parent['nome']} já compõe {name} com o papel {role}")
        m.setdefault("composicao", []).append(copy.deepcopy(composition))
    return f"{parent['nome']} compõe {name} [{op['cardinalidade']}]"


@operation("remover_composicao")
def remove_composition(ds, op, step=None):
    key, name = _child_key(op["filho"])
    for m in ds.copies(op["pai"]["nivel"], op["pai"]["nome"]):
        m["composicao"] = [c for c in m.get("composicao", []) if not _matches(c, key, name, op.get("papel"))]
    return f"{op['pai']['nome']} deixa de compor {name}"


@operation("alterar_composicao")
def change_composition(ds, op, step=None):
    parent = op["pai"]
    key, name = _child_key(op["filho"])
    changed = 0
    for m in ds.copies(parent["nivel"], parent["nome"]):
        for c in m.get("composicao", []):
            if _matches(c, key, name, op.get("papel")):
                if "cardinalidade" in op:
                    c["cardinalidade"] = op["cardinalidade"]
                if "novoPapel" in op:
                    if op["novoPapel"] == name:
                        c.pop("papel", None)
                    else:
                        c["papel"] = op["novoPapel"]
                changed += 1
    if not changed:
        raise AmendmentError(f"{parent['nome']} não compõe {name}")
    if "novoPapel" in op:
        old_role = op.get("papel") or name
        parent_roles = ds.roles_of(parent["nivel"], parent["nome"])
        parent_model = (parent["nivel"], parent["nome"])

        def rename_role(segments, owner):
            return [op["novoPapel"] if x == old_role and (i > 0 and segments[i - 1] in parent_roles or
                                                          i == 0 and (owner is None or owner == parent_model)) else x
                    for i, x in enumerate(segments)]

        ds.rewrite_paths(rename_role)
    return f"composição {parent['nome']} → {name} alterada"
