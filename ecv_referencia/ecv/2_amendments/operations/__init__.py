"""The closed vocabulary of operations on the declarations of a domain (operations.json).

Each operation is a JSON object {"op": "<name>", ...fields}. The name and the fields are part of the
vocabulary given to the LLM (Portuguese, like the declarations); each module of this package
implements one group of operations and registers each handler under its name:

    @operation("mover_propriedade")
    def move_property(ds, op, step=None) -> str      # a short description of what was done
"""
import json
from functools import lru_cache

from ecv import config

HANDLERS = {}


def operation(name):
    def register(fn):
        HANDLERS[name] = fn
        return fn
    return register


@lru_cache(maxsize=1)
def vocabulary():
    """operations.json: the groups and, for each operation, its fields, description and group."""
    return json.loads(config.path("operacoes").read_text(encoding="utf-8"))


def describe(allowed=None):
    """The vocabulary as text for a prompt: one line per operation (only the allowed ones, if given)."""
    ops = vocabulary()["operacoes"]
    return "\n".join(f"- `{k}` ({', '.join(v['campos'])}): {v['descricao']}" for k, v in ops.items() if allowed is None or k in allowed)


from . import compositions, definitions, mapping, models, properties, rules, scenarios  # noqa: E402,F401  (register the handlers)
