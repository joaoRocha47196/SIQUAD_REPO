"""Operations on rules (RP, RIR, RIC): add, replace, remove and move."""
import copy

from ecv.shared.errors import AmendmentError

from . import operation


@operation("adicionar_regra")
def add_rule(ds, op, step=None):
    rule = op["regra"]
    if any(x["id"] == rule["id"] for _, x, _, _ in ds.all_rules()):
        raise AmendmentError(f"a regra {rule['id']} já existe")
    for node in ds.nodes_at(op["onde"]):
        node.setdefault("regras", []).append(copy.deepcopy(rule))
    return f"+ regra {rule['id']}"


@operation("substituir_regra")
def replace_rule(ds, op, step=None):
    replaced = 0
    for holder, rule, _, _ in list(ds.all_rules()):
        if rule["id"] == op["id"]:
            holder[holder.index(rule)] = copy.deepcopy(op["regra"])
            replaced += 1
    if not replaced:
        raise AmendmentError(f"a regra {op['id']} não existe")
    return f"regra {op['id']} substituída"


@operation("remover_regra")
def remove_rule(ds, op, step=None):
    for holder, rule, _, _ in list(ds.all_rules()):
        if rule["id"] == op["id"]:
            holder.remove(rule)
    return f"- regra {op['id']}"


@operation("mover_regra")
def move_rule(ds, op, step=None):
    rule = next((copy.deepcopy(r) for _, r, _, _ in ds.all_rules() if r["id"] == op["id"]), None)
    if rule is None:
        raise AmendmentError(f"a regra {op['id']} não existe")
    remove_rule(ds, {"id": op["id"]})
    add_rule(ds, {"onde": op["para"], "regra": rule})
    target = op["para"]
    return f"regra {op['id']} → {target.get('modelo')}{'.' + target['propriedade'] if target.get('propriedade') else ''}"
