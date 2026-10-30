"""Operations on the scenarios: projections (structural rules, RE) and execution profiles."""
import copy

from ecv.shared.errors import AmendmentError

from . import operation


@operation("definir_projecao")
def define_projection(ds, op, step=None):
    projection = op["projecao"]
    d = ds.declaration_of(projection["hlm"])
    d["projecoes"] = [x for x in d.get("projecoes", []) if x["nome"] != projection["nome"]] + [copy.deepcopy(projection)]
    return f"projeção {projection['nome']}"


@operation("remover_projecao")
def remove_projection(ds, op, step=None):
    for d in ds.declarations.values():
        d["projecoes"] = [x for x in d.get("projecoes", []) if x["nome"] != op["nome"]]
    return f"- projeção {op['nome']}"


@operation("definir_perfil")
def define_profile(ds, op, step=None):
    profile = op["perfil"]
    hlm = next((x["hlm"] for d in ds.declarations.values() for x in d.get("projecoes", []) if x["nome"] == profile["projecao"]), None)
    if hlm is None:
        raise AmendmentError(f"a projeção {profile['projecao']} não existe")
    d = ds.declarations[hlm]
    d["perfis"] = [x for x in d.get("perfis", []) if x["nome"] != profile["nome"]] + [copy.deepcopy(profile)]
    return f"perfil {profile['nome']}"


@operation("remover_perfil")
def remove_profile(ds, op, step=None):
    for d in ds.declarations.values():
        d["perfis"] = [x for x in d.get("perfis", []) if x["nome"] != op["nome"]]
    return f"- perfil {op['nome']}"
