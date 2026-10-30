"""Navigation in an instance and base-type checks.

An instance is JSON with the shape of the HLM: keys are the roles of the compositions and the names
of the properties; a repeatable composition is a list.
"""
import re

ISO_DATE = re.compile(r"^\d{4}-\d{2}-\d{2}(T\d{2}:\d{2}(:\d{2}(\.\d+)?)?(Z|[+-]\d{2}:\d{2})?)?$")


def join(a, b):
    return f"{a}.{b}" if a else b


def collect(node, segments, path=""):
    """[(concrete path, value)] following the segments; a list gives one value per element ([i]); a missing
    value gives (path, None). An empty list of segments returns the node itself."""
    if not segments:
        return [(path, node)]
    first, rest = segments[0], segments[1:]
    if not isinstance(node, dict) or node.get(first) is None:
        return [(join(path, ".".join(segments)), None)]
    value = node[first]
    if isinstance(value, list):
        out = []
        for i, item in enumerate(value):
            out += collect(item, rest, f"{join(path, first)}[{i}]")
        return out
    return collect(value, rest, join(path, first))


def first_value(node, path):
    values = collect(node, path.split("."))
    return values[0][1] if values else None


def abstract_path(path):
    """'Linhas.Linha[1].valor' -> 'Linhas.Linha.valor'."""
    return re.sub(r"\[\d+\]", "", path)


def deep_copy(x):
    if isinstance(x, dict):
        return {k: deep_copy(v) for k, v in x.items()}
    if isinstance(x, list):
        return [deep_copy(v) for v in x]
    return x


def has_base_type(base_type, v):
    if base_type == "texto":
        return isinstance(v, str)
    if base_type == "inteiro":
        return isinstance(v, int) and not isinstance(v, bool)
    if base_type == "decimal":
        return isinstance(v, (int, float)) and not isinstance(v, bool)
    if base_type == "booleano":
        return isinstance(v, bool)
    if base_type == "data":
        return isinstance(v, str) and bool(ISO_DATE.match(v))
    return True
