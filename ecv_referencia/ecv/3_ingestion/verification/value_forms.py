"""The form each operator expects for its value (configuration: formasValor)."""
import re

from ecv import config


def _is_number(v):
    return isinstance(v, (int, float)) and not isinstance(v, bool)


def _is_date(v):
    return isinstance(v, str) and config.NAME_PATTERNS["data"].match(v) is not None


def _is_simple(v):
    return isinstance(v, (str, int, float, bool))


def form_error(operator, value, base_type):
    """None if the value has the form the operator requires; otherwise the reason."""
    form = config.OPERATORS[operator]["forma"]
    if form == "valor":
        return None if _is_simple(value) else "esperado um valor simples"
    if form == "lista":
        ok = isinstance(value, list) and value and all(_is_simple(x) for x in value)
        return None if ok else "esperada uma lista não vazia de valores"
    if form == "intervalo":
        if not (isinstance(value, list) and len(value) == 2):
            return "esperado [mínimo, máximo]"
        a, b = value
        if base_type == "data":
            return None if _is_date(a) and _is_date(b) and a <= b else "esperadas duas datas, mínimo <= máximo"
        return None if _is_number(a) and _is_number(b) and a <= b else "esperados dois números, mínimo <= máximo"
    if form == "numero":
        if base_type == "data":
            return None if _is_date(value) else "esperada uma data (AAAA-MM-DD)"
        return None if _is_number(value) else "esperado um número"
    if form == "padrao":
        if not isinstance(value, str):
            return "esperada uma expressão regular"
        try:
            re.compile(value)
        except re.error as e:
            return f"expressão regular inválida ({e})"
        return None
    if form == "texto":
        return None if isinstance(value, str) and value else "esperado um texto não vazio"
    if form == "comprimento":
        if isinstance(value, int) and not isinstance(value, bool) and value >= 0:
            return None
        if isinstance(value, list) and len(value) == 2 and all(isinstance(x, int) for x in value) and value[0] <= value[1]:
            return None
        return "esperado um inteiro >= 0 ou [mínimo, máximo]"
    return None
