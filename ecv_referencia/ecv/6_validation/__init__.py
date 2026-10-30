"""6 · Validation: evaluates a concrete instance of a HLM against the rules of the graph, in the scenario
of a profile.

Receives: the graph (memory or Neo4j), an instance (JSON with the shape of the HLM), a profile (or a
HLM) and the values of the external contexts.
Needs: an implementation of every function the rules call (functions/).
Produces: the ViewModel 'validacao' (structure problems, the state of each rule in each occurrence,
the conclusions).

    engine.py       validate(): scenario -> structure -> rules -> result
    scenario.py     the profile's projection, fixed values and contexts
    structure.py    structural checks of the instance
    rules.py        evaluation of RP, RIR and RIC per occurrence
    instance.py     navigation in the instance, base types
    functions/      implementations of the declared functions (registry by decorator)
    examples/       example instances: {descricao, perfil | hlm, contextos, instancia}
    test_instances.py  test instances of a domain: skeleton from the structure and profile, request to the LLM, saved and validated
"""
import json

from ecv import config

from .engine import validate
from .rules import STATES


def examples_folder():
    return config.path("exemplosValidacao")


def examples():
    """{name: example} of the instances in examples/."""
    return {f.stem: json.loads(f.read_text(encoding="utf-8")) for f in sorted(examples_folder().glob("*.json"))}


def validate_example(g, name, contexts=None):
    example = examples()[name]
    merged = {**example.get("contextos", {}), **(contexts or {})}
    return validate(g, example["instancia"], profile=example.get("perfil"), hlm=example.get("hlm"), contexts=merged,
                    name=name, description=example.get("descricao"))


__all__ = ["STATES", "validate", "examples", "validate_example", "examples_folder"]
