"""Adapters of phase 0: one per source format. Each one reads a source and returns an Inventory.

ADAPTERS maps the name used in dominios/<d>/dominio.json (field `adaptador`) to the function that
implements it. A source with `nomesDe` receives the English names of the terms taken from another
source (the CIUS-PT guide takes them from the schematron).

Adapters created by a request to the LLM (kind "adaptador", see ../adapter_requests.py) are modules
`a_<name>.py` in this folder with NAME (the name used in dominio.json), DESCRIPTION and adapt(path);
load() registers them next to the built-in ones.
"""
import importlib
from pathlib import Path

from . import cius_pt, fm, json_schema, text

BUILT_IN = {
    "cius_pt.guia": cius_pt.guide,
    "cius_pt.schematron": cius_pt.schematron,
    "cius_pt.ubl": cius_pt.ubl,
    "fm.dart": fm.dart,
    "fm.registos": fm.records,
    "json_schema.smart_data_models": json_schema.smart_data_models,
    "texto.markdown": text.markdown,
}
ADAPTERS = dict(BUILT_IN)
CREATED = {}            # name -> module file of the adapters created by a request

# Functions that derive, from one inventory, the hint another adapter receives ('nomesDe' in dominio.json).
NAME_SOURCES = {"cius_pt.guia": cius_pt.english_names}

FOLDER = Path(__file__).parent


def load(reload=False):
    """Register the created adapters (a_*.py); with reload, read their modules again."""
    for name in list(CREATED):
        ADAPTERS.pop(name, None)
    CREATED.clear()
    for f in sorted(FOLDER.glob("a_*.py")):
        module = importlib.import_module(f"{__name__}.{f.stem}")
        if reload:
            module = importlib.reload(module)
        ADAPTERS[module.NAME] = module.adapt
        CREATED[module.NAME] = f.name


def describe():
    """[(name, module file, first line of the description)] of every adapter."""
    out = []
    for name, fn in sorted(ADAPTERS.items()):
        module = importlib.import_module(fn.__module__)
        doc = getattr(module, "DESCRIPTION", None) or (fn.__doc__ or module.__doc__ or "").strip().splitlines()[0]
        out.append((name, Path(module.__file__).name, doc))
    return out


load()
