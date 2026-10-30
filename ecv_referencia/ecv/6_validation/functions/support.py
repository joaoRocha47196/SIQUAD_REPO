"""Helpers shared by the function implementations."""
import datetime


class Unavailable(Exception):
    """A value or an external context needed to evaluate the function is missing."""


def as_datetime(value):
    """An ISO date (AAAA-MM-DD) or date-time, as a naive datetime."""
    if value is None:
        raise Unavailable("valor em falta")
    text = str(value)
    try:
        if len(text) == 10:
            return datetime.datetime.fromisoformat(text + "T00:00:00")
        return datetime.datetime.fromisoformat(text.replace("Z", "+00:00")).replace(tzinfo=None)
    except ValueError as e:
        raise Unavailable(f"data inválida: {text}") from e


def context(contexts, name):
    """The value of an external context, or Unavailable when it was not given."""
    if contexts.get(name) is None:
        raise Unavailable(f"falta o contexto externo {name}")
    return contexts[name]


def present(values):
    """The values of a collection that are not missing."""
    return [x for x in (values or []) if x is not None]
