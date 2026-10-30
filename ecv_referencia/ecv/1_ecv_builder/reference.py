"""The reference declarations: what a domain reuses instead of creating again.

Reference = the example declarations (specs/exemplos) and the declarations of every other domain whose
generation (phase G) is accepted. They are ingested in memory for the prompt (existing models and functions), for the
conflict check and to complete the models a domain reuses.
"""
import copy
import json
from pathlib import Path

from ecv import config
from ecv.ingestion import ingest
from ecv.shared.workspace import Workspace


def reference_files(exclude=None):
    files = list(config.example_declarations())
    workspace = Workspace()
    for domain_id in workspace.domain_ids():
        if domain_id == exclude:
            continue
        other = workspace.domain(domain_id)
        if other.step_state("G") == "aceite":
            files += other.declaration_files()
    return files


def reference_graph(exclude=None):
    return ingest(reference_files(exclude)).graph


def _without_rules(model):
    """The model without its rules (the part the merge compares to decide whether it is the same model)."""
    x = {k: v for k, v in model.items() if k != "regras"}
    if "propriedades" in x:
        x["propriedades"] = [{k: v for k, v in p.items() if k != "regras"} for p in x["propriedades"]]
    return json.dumps(x, sort_keys=True, ensure_ascii=False)


def complete_reused_models(domain, ds):
    """The models the domain reuses from the reference (same name and same definition) receive the rules they
    have there, and the declarations receive the functions and contexts those rules use.

    A declaration is complete (shared models repeat, identical): without this, the rules of a reused model
    would only show when the domain is ingested together with the reference. Returns the lines done."""
    reference, definitions = {}, {"funcoes": {}, "contextosExternos": {}}
    for f in reference_files(exclude=domain.id):
        data = json.loads(Path(f).read_text(encoding="utf-8"))
        for section in ("usm", "sm"):
            for m in data.get(section, []):
                reference.setdefault((section, m["nome"]), m)
        for section in definitions:
            for x in data.get(section, []):
                definitions[section].setdefault(x["nome"], x)
    done = []
    for d in ds.declarations.values():
        for section in ("usm", "sm"):
            for m in d.get(section, []):
                done += _complete_model(m, reference.get((section, m["nome"])))
    added = {}
    for section, items in definitions.items():         # reference definitions are available only during the sync
        ds.reservoir.setdefault(section, [])
        names = {x["nome"] for x in ds.reservoir[section]}
        added[section] = {n for n in items if n not in names}
        ds.reservoir[section] += [items[n] for n in added[section]]
    ds.refresh()
    for section in definitions:
        ds.reservoir[section] = [x for x in ds.reservoir[section] if x["nome"] not in added[section]]
    return list(dict.fromkeys(done))


def _complete_model(model, ref):
    if ref is None or _without_rules(ref) != _without_rules(model):
        return []
    done = []
    ids = {x["id"] for x in model.get("regras", [])} | {x["id"] for p in model.get("propriedades", []) for x in p.get("regras", [])}
    for rule in ref.get("regras", []):
        if rule["id"] not in ids:
            model.setdefault("regras", []).append(copy.deepcopy(rule))
            done.append(f"{model['nome']}: + {rule['id']}")
    for ref_prop in ref.get("propriedades", []):
        prop = next(p for p in model["propriedades"] if p["nome"] == ref_prop["nome"])
        for rule in ref_prop.get("regras", []):
            if rule["id"] not in ids:
                prop.setdefault("regras", []).append(copy.deepcopy(rule))
                done.append(f"{model['nome']}.{ref_prop['nome']}: + {rule['id']}")
    return done
