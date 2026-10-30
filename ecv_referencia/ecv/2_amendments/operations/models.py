"""Operations on models: create, remove, rename, change, merge, extract a USM, create and remove a HLM."""
import copy

from ecv.shared.errors import AmendmentError

from ..declaration_set import SECTION
from . import operation
from .compositions import compose


@operation("criar_modelo")
def create_model(ds, op, step=None):
    level, name = op["nivel"], op["nome"]
    if ds.definition(level, name):
        raise AmendmentError(f"{level} {name} já existe")
    model = {"nome": name, "descricao": op["descricao"]}
    if op.get("composicao"):
        model["composicao"] = op["composicao"]
    if op.get("propriedades") is not None or level == "USM":
        model["propriedades"] = op.get("propriedades", [])
    if op.get("declaracoes"):
        for hlm in op["declaracoes"]:
            ds.section_list(ds.declarations[hlm], level).append(copy.deepcopy(model))
    else:
        ds.reservoir[SECTION[level]].append(model)
    return f"criado {level} {name}"


@operation("remover_modelo")
def remove_model(ds, op, step=None):
    level, name = op["nivel"], op["nome"]
    key = SECTION[level] if level != "HLM" else None
    for d in ds.everything():
        d[SECTION[level]] = [m for m in d.get(SECTION[level], []) if m["nome"] != name]
        for section in ("hlm", "sm"):
            for m in d.get(section, []):
                m["composicao"] = [c for c in m.get("composicao", []) if c.get(key) != name]
    return f"removido {level} {name}"


def _rename_hlm(ds, old, new):
    d = ds.declarations.pop(old)
    d["hlm"][0]["nome"] = new
    d["declaracao"]["hlm"] = new
    for projection in d.get("projecoes", []):
        if projection.get("hlm") == old:
            projection["hlm"] = new
    ds.declarations[new] = d
    return f"HLM {old} → {new}"


@operation("renomear_modelo")
def rename_model(ds, op, step=None):
    level, old, new = op["nivel"], op["de"], op["para"]
    ds.require(level, old)
    if level == "HLM":
        return _rename_hlm(ds, old, new)
    key = SECTION[level]
    for m in ds.copies(level, old):
        m["nome"] = new
    for d in ds.everything():
        for section in ("hlm", "sm"):
            for m in d.get(section, []):
                for c in m.get("composicao", []):
                    if c.get(key) == old:
                        c[key] = new
    ds.rewrite_paths(lambda segments, owner: [new if x == old else x for x in segments])
    return f"{level} {old} → {new}"


@operation("alterar_modelo")
def change_model(ds, op, step=None):
    for m in ds.copies(op["nivel"], op["nome"]):
        for k in ("descricao", "notas"):
            if k in op:
                m[k] = op[k]
    return f"alterado {op['nivel']} {op['nome']}"


@operation("fundir_modelos")
def merge_models(ds, op, step=None):
    level, target = op["nivel"], op["para"]
    key = SECTION[level]
    if ds.definition(level, target) is None:
        base = copy.deepcopy(ds.definition(level, op["de"][0]))
        base["nome"] = target
        for d in ds.containing(level, op["de"][0]):
            ds.section_list(d, level).append(copy.deepcopy(base))
    for source in op["de"]:
        if source == target:
            continue
        model = ds.definition(level, source)
        if model is None:
            raise AmendmentError(f"{level} {source} não existe")
        for p in model.get("propriedades", []):
            for props in ds.property_lists(level, target):
                if not any(x["nome"] == p["nome"] for x in props):
                    props.append(copy.deepcopy(p))
        for r in model.get("regras", []):
            for x in ds.copies(level, target):
                if not any(y["id"] == r["id"] for y in x.setdefault("regras", [])):
                    x["regras"].append(copy.deepcopy(r))
        for d in ds.containing(level, source):
            ds.copy_into(d, level, target)
        for d in ds.everything():
            d[SECTION[level]] = [x for x in d.get(SECTION[level], []) if x["nome"] != source]
            for section in ("hlm", "sm"):
                for x in d.get(section, []):
                    for c in x.get("composicao", []):
                        if c.get(key) == source:
                            c[key] = target
    return f"{', '.join(op['de'])} fundidos em {target}"


@operation("extrair_usm")
def extract_usm(ds, op, step=None):
    source, names, new = op["de"], op["propriedades"], op["novo"]
    origin = ds.definition(source["nivel"], source["modelo"])
    if origin is None:
        raise AmendmentError(f"{source['nivel']} {source['modelo']} não existe")
    taken = [copy.deepcopy(p) for p in origin.get("propriedades", []) if p["nome"] in names]
    missing = set(names) - {p["nome"] for p in taken}
    if missing:
        raise AmendmentError(f"propriedades inexistentes em {source['modelo']}: {sorted(missing)}")
    usm = {"nome": new["nome"], "descricao": new["descricao"], "propriedades": taken}
    if ds.definition("USM", new["nome"]) is None:
        for d in ds.containing(source["nivel"], source["modelo"]):
            ds.section_list(d, "USM").append(copy.deepcopy(usm))
    for m in ds.copies(source["nivel"], source["modelo"]):
        m["propriedades"] = [p for p in m.get("propriedades", []) if p["nome"] not in names]
    segment = op.get("papel") or new["nome"]
    roles = ds.roles_of(source["nivel"], source["modelo"])
    owner_model = (source["nivel"], source["modelo"])

    def insert_segment(segments, owner):
        if segments[-1] in names and ((len(segments) == 1 and owner == owner_model) or (len(segments) > 1 and segments[-2] in roles)):
            return segments[:-1] + [segment, segments[-1]]
        return segments

    ds.rewrite_paths(insert_segment)
    compose(ds, {"pai": {"nivel": source["nivel"], "nome": source["modelo"]}, "filho": {"nivel": "USM", "nome": new["nome"]},
                 "cardinalidade": op.get("cardinalidade", "1..1"), "papel": op.get("papel")})
    return f"USM {new['nome']} extraído de {source['modelo']} ({', '.join(names)})"


@operation("criar_hlm")
def create_hlm(ds, op, step=None):
    name = op["nome"]
    if name in ds.declarations:
        raise AmendmentError(f"HLM {name} já existe")
    header = {"nome": f"ECV: {name}", "versao": "0.1.0", "descricao": op["descricao"], "hlm": name}
    header.update(op.get("declaracao") or {})
    ds.declarations[name] = {"$schema": ds.schema_reference(), "declaracao": header, "usm": [], "sm": [],
                             "hlm": [{"nome": name, "descricao": op["descricao"], "composicao": []}]}
    for c in op.get("composicao", []):
        compose(ds, {"pai": {"nivel": "HLM", "nome": name}, "filho": {"nivel": "SM", "nome": c["sm"]},
                     "cardinalidade": c["cardinalidade"], "papel": c.get("papel")})
    return f"criado HLM {name}"


@operation("remover_hlm")
def remove_hlm(ds, op, step=None):
    ds.declarations.pop(op["nome"])
    return f"removido HLM {op['nome']}"
