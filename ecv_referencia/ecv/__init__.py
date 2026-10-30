"""ECV reference implementation (Validation Knowledge Stratification).

The code is organised in numbered modules, in the order in which data flows through them:

    0_transformer   source files in known formats  ->  inventory (neutral intermediate format)
    1_ecv_builder   inventory + specs              ->  ECV declarations (steps A to F, prompts for the LLM)
    2_amendments    change requests                ->  operations applied to the declarations
    3_ingestion     ECV declaration                ->  verified graph, merged without duplicates
    4_graph         graph model and storage (in memory or Neo4j): the ECV database
    5_views         ViewModels (queries on the graph) and their HTML rendering
    6_validation    validation of a concrete instance against the rules, in the scenario of a profile
    7_webapp        web application: HTTP server, routes, pages

Supporting packages: ``config`` (the single configuration file), ``shared`` (domain workspace,
LLM requests, JSON formatting) and ``tools`` (documentation generator).

A name that starts with a digit cannot be used in an ``import`` statement, so each numbered
directory is importable under its plain name: ``import ecv.transformer`` loads ``ecv/0_transformer``.
MODULES below is the complete mapping; the finder is registered when ``ecv`` is imported.
"""
import importlib.abc
import importlib.util
import sys
from pathlib import Path

PACKAGE_DIR = Path(__file__).resolve().parent

MODULES = {
    "transformer": "0_transformer",
    "ecv_builder": "1_ecv_builder",
    "amendments": "2_amendments",
    "ingestion": "3_ingestion",
    "graph": "4_graph",
    "views": "5_views",
    "validation": "6_validation",
    "webapp": "7_webapp",
}


class NumberedModuleFinder(importlib.abc.MetaPathFinder):
    """Resolves ``ecv.<name>`` to the numbered directory ``ecv/<n>_<name>``."""

    def find_spec(self, fullname, path=None, target=None):
        parent, _, name = fullname.partition(".")
        if parent != __name__ or name not in MODULES:
            return None
        directory = PACKAGE_DIR / MODULES[name]
        return importlib.util.spec_from_file_location(
            fullname, directory / "__init__.py", submodule_search_locations=[str(directory)])


if not any(isinstance(finder, NumberedModuleFinder) for finder in sys.meta_path):
    sys.meta_path.insert(0, NumberedModuleFinder())
