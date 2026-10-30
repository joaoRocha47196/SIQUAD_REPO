"""Implementations of the functions declared in ECV declarations.

A function is declared in the declaration (name, parameters, external contexts, "Verdadeira quando…")
and called, structurally, by the rules; the engine needs to know how to run it. Each module of this
package implements a family of functions and registers each one under its declared name:

    @implements("naoPosteriorAHoje")
    def not_after_today(date, *, contexts): ...

An implementation receives the arguments in parameter order and the external contexts as a dict, and
returns True (holds) or False; it raises Unavailable when a value or a context is missing. A declared
function without an implementation makes the rules that call it 'não avaliável'.

Adding a function = adding a decorated function to one of these modules (or a new module here): the
package loads every module it contains.
"""
import importlib
import pkgutil

from .support import Unavailable

REGISTRY = {}          # declared name -> implementation
SOURCES = {}           # declared name -> module that implements it


def implements(name):
    """Register the decorated function as the implementation of the declared function 'name'."""
    def register(fn):
        REGISTRY[name] = fn
        SOURCES[name] = fn.__module__.rsplit(".", 1)[-1]
        return fn
    return register


def load(reload=False):
    """Import every module of this package (each registers its functions). With reload, re-read them from disk."""
    if reload:
        REGISTRY.clear()
        SOURCES.clear()
    # requested implementations (f_*.py, written by function_requests) load last: they replace a previous one
    for info in sorted(pkgutil.iter_modules(__path__), key=lambda m: (m.name.startswith("f_"), m.name)):
        if info.name == "support":
            continue
        module_name = f"{__name__}.{info.name}"
        module = importlib.import_module(module_name)
        if reload:
            importlib.reload(module)


def implemented():
    """Sorted names of the functions that have an implementation."""
    return sorted(REGISTRY)


def call(name, arguments, contexts):
    """(result, reason): result True/False, or None with the reason when the function cannot be evaluated."""
    fn = REGISTRY.get(name)
    if fn is None:
        return None, f"a função {name} não tem implementação no motor (ecv/6_validation/functions)"
    try:
        return bool(fn(*arguments, contexts=contexts)), None
    except Unavailable as e:
        return None, str(e)
    except (TypeError, ValueError) as e:
        return None, f"argumentos inválidos para {name}: {e}"


load()

__all__ = ["REGISTRY", "SOURCES", "Unavailable", "implements", "implemented", "call", "load"]
