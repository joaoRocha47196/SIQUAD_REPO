"""1 · ECV builder: inventory + specification -> complete ECV declarations, then review by layers.

Receives: the inventories of a domain (module 0) and its definition (dominio.json: sources, uses, scenarios).
Needs: the internal specification (specs/ecv_specs.md, built from specs/ by specs_bundle.py), the build process
(build_process.json), the reference declarations (examples and other accepted domains) and the review notes.
Produces: one generation request to the LLM (phase G: the complete declarations and the mapping of every inventory
item); then, for each review layer A to F, the checks of the layer and the change requests that correct or complete it
(applied by module 2).

    build_process.py  phases, layers, principles, procedures, response format
    specs_bundle.py   the single internal specification for the LLM
    context.py        what the generation prompt receives; the uncovered inventory items of a layer
    package.py        the generation prompt and the change prompt of a layer
    reference.py      reference declarations; reused models completed with their rules
    search.py         search and similar models in a graph
    checks.py         the checks after the generation and of each layer
    workflow.py       prepare, register, request changes, accept
"""
from .build_process import process_definition, step, step_ids
from .checks import StepCheck, check_step
from .package import generation_prompt
from .workflow import (accept_step, apply_operations_to_domain, prepare_generation, register_change_response, register_response,
                       register_generation_response, request_changes, verify_step)

__all__ = ["StepCheck", "check_step", "process_definition", "step", "step_ids", "generation_prompt", "accept_step",
           "apply_operations_to_domain", "prepare_generation", "register_change_response", "register_response",
           "register_generation_response", "request_changes", "verify_step"]
