"""Applying a batch of operations to the declarations of a domain.

The batch is all or nothing: the operations run on the DeclarationSet in order; the first one that
fails raises AmendmentError (with its position) and the caller does not save. After the batch, the
functions and contexts the rules use are copied where needed, the sections are put in order and
every rule description is derived again.
"""
from ecv.shared.errors import AmendmentError

from .declaration_set import DeclarationSet
from .operations import HANDLERS


def parse_operations(data):
    """Accept {"operacoes": [...]} (the response format) or a bare list of operations."""
    ops = data.get("operacoes", []) if isinstance(data, dict) else data
    if not isinstance(ops, list) or not all(isinstance(x, dict) for x in ops):
        raise AmendmentError("as operações são uma lista de objetos {\"op\": …}")
    return ops


def apply_operations(ds, operations, step=None):
    """Apply the operations to the DeclarationSet (in memory). Returns one line per operation done."""
    done = []
    for i, op in enumerate(operations):
        name = op.get("op")
        handler = HANDLERS.get(name)
        if handler is None:
            raise AmendmentError(f"operação {i + 1}: '{name}' não existe no vocabulário (operations.json)")
        try:
            done.append(handler(ds, op, step) or name)
        except (KeyError, StopIteration) as e:
            raise AmendmentError(f"operação {i + 1} ({name}): campo em falta ou referência inexistente: {e}") from e
        except AmendmentError as e:
            raise AmendmentError(f"operação {i + 1} ({name}): {e}") from e
    ds.refresh()
    ds.log += done
    return done


def apply_to_domain(domain, operations, step=None, save=True):
    """Load the domain's declarations, apply the operations and (unless save=False) write the files.

    Returns (DeclarationSet, lines done). Nothing is written when an operation fails."""
    ds = DeclarationSet.load(domain.folder)
    done = apply_operations(ds, operations, step)
    if save:
        ds.save()
    return ds, done
