"""Readable JSON: one indentation level per object, short lists of simple values on one line (the format of the
declarations, so that diffs read well)."""
import json


def _is_simple(v):
    return isinstance(v, (str, int, float, bool)) or v is None


def _one_line(v):
    return json.dumps(v, ensure_ascii=False)


def dumps(data, indent=2, width=110):
    def fmt(v, level):
        pad = " " * (indent * level)
        pad1 = " " * (indent * (level + 1))
        if isinstance(v, dict):
            if not v:
                return "{}"
            short = _one_line(v)
            if len(short) + len(pad) <= width and all(_is_simple(x) or (isinstance(x, list) and all(_is_simple(y) for y in x)) for x in v.values()) and len(v) <= 4:
                return short
            items = [f"{pad1}{json.dumps(k, ensure_ascii=False)}: {fmt(x, level + 1)}" for k, x in v.items()]
            return "{\n" + ",\n".join(items) + "\n" + pad + "}"
        if isinstance(v, list):
            if not v:
                return "[]"
            short = _one_line(v)
            if len(short) + len(pad) <= width and all(_is_simple(x) or (isinstance(x, list) and all(_is_simple(y) for y in x)) for x in v):
                return short
            items = [f"{pad1}{fmt(x, level + 1)}" for x in v]
            return "[\n" + ",\n".join(items) + "\n" + pad + "]"
        return _one_line(v)

    return fmt(data, 0) + "\n"
