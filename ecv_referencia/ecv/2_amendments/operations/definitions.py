"""Operations on the shared definitions: functions and external contexts."""
import copy

from . import operation


def _define_shared(ds, section, entity, declarations):
    """Create or replace the definition in the given declarations (or in those that already have it) and in the reservoir."""
    targets = declarations or [h for h, d in ds.declarations.items() if any(x["nome"] == entity["nome"] for x in d.get(section, []))]
    for hlm in targets:
        d = ds.declarations[hlm]
        d[section] = [x for x in d.get(section, []) if x["nome"] != entity["nome"]] + [copy.deepcopy(entity)]
    ds.reservoir[section] = [x for x in ds.reservoir[section] if x["nome"] != entity["nome"]] + [copy.deepcopy(entity)]


def _remove_shared(ds, section, name):
    for d in ds.everything():
        d[section] = [x for x in d.get(section, []) if x["nome"] != name]


@operation("definir_funcao")
def define_function(ds, op, step=None):
    _define_shared(ds, "funcoes", op["funcao"], op.get("declaracoes"))
    return f"função {op['funcao']['nome']}"


@operation("remover_funcao")
def remove_function(ds, op, step=None):
    _remove_shared(ds, "funcoes", op["nome"])
    return f"- função {op['nome']}"


@operation("definir_contexto")
def define_context(ds, op, step=None):
    _define_shared(ds, "contextosExternos", op["contexto"], op.get("declaracoes"))
    return f"contexto {op['contexto']['nome']}"


@operation("remover_contexto")
def remove_context(ds, op, step=None):
    _remove_shared(ds, "contextosExternos", op["nome"])
    return f"- contexto {op['nome']}"
