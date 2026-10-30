"""2 · Amendments: changes to the declarations of a domain, as operations of a closed vocabulary.

Receives: operations ({"op": ..., fields}), from an LLM response (steps B to F, change requests), a file,
the web form or a CSV of known mappings.
Needs: the declarations, reservoir and mapping of the domain.
Produces: the declarations changed consistently (a shared model changes in every declaration; renaming
rewrites the paths of projections, profiles, rules and mapping), with descriptions derived again.

    operations.json      the vocabulary (names, fields, description, group)
    declaration_set.py   DeclarationSet: the domain's declarations as the operations see them
    operations/          one handler per operation, by group
    engine.py            apply a batch (all or nothing)
    change_requests.py   natural language -> prompt for the LLM
    csv_rules.py         table of known mappings -> RIR operations
"""
from .change_requests import change_prompt
from .csv_rules import operations_from_csv
from .declaration_set import DeclarationSet, file_name
from .engine import apply_operations, apply_to_domain, parse_operations
from .operations import HANDLERS, describe, vocabulary

__all__ = ["DeclarationSet", "file_name", "apply_operations", "apply_to_domain", "parse_operations", "HANDLERS", "describe",
           "vocabulary", "change_prompt", "operations_from_csv"]
