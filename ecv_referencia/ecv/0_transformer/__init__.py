"""0 · Transformer: source files in known formats -> inventory (phase 0, deterministic, no LLM).

Receives: the sources of a domain (dominio.json: adapter and path of each one, under the data root).
Produces: one inventory per source (dominios/<d>/inventario/<source>.json): groups, elements and rules,
each with its origin, and the rules classified by category.

    adapters/          one adapter per format (CIUS-PT guide, schematron and UBL; FM Dart and records; JSON Schema;
                       text in natural language; the a_*.py created by a request to the LLM)
    adapter_requests.py  a request to the LLM to create the adapter of a format without one
    inventory.py       the inventory format (Group, Element, SourceRule, Inventory)
    classification.py  rule categories and source type -> base type
    extraction.py      Extractor: runs the adapters of a domain and writes the inventories
"""
from .adapters import ADAPTERS
from .classification import CATEGORIES, base_type, classify
from .extraction import Extractor, extract
from .inventory import Element, Group, Inventory, SourceRule, load

__all__ = ["ADAPTERS", "CATEGORIES", "base_type", "classify", "Extractor", "extract", "Element", "Group", "Inventory",
           "SourceRule", "load"]
