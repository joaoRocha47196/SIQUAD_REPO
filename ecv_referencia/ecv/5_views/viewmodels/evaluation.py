"""Evaluation of the catalogue's typed checks on a value.

Used by the static selection of a profile (a fixed value decides a term), by the dependency analysis
and by the validation engine. Returns True, False, or None when the check does not apply to the value.
"""
import re


def _compare(a, b):
    # numbers with numbers; ISO dates (text) compare lexicographically
    if isinstance(a, (int, float)) and isinstance(b, (int, float)):
        return (a > b) - (a < b)
    a, b = str(a), str(b)
    return (a > b) - (a < b)


def evaluate(operator, value, expected):
    if value is None:
        return None
    if operator == "EQUALS":
        return value == expected
    if operator == "NOT_EQUALS":
        return value != expected
    if operator == "IN":
        return value in expected
    if operator == "RANGE":
        return _compare(value, expected[0]) >= 0 and _compare(value, expected[1]) <= 0
    if operator == "LT":
        return _compare(value, expected) < 0
    if operator == "LTE":
        return _compare(value, expected) <= 0
    if operator == "GT":
        return _compare(value, expected) > 0
    if operator == "GTE":
        return _compare(value, expected) >= 0
    if operator == "PATTERN":
        return re.search(expected, str(value)) is not None
    if operator == "LENGTH":
        n = len(str(value))
        return expected[0] <= n <= expected[1] if isinstance(expected, list) else n == expected
    if operator == "CONTAINS":
        return str(expected) in str(value)
    if operator == "STARTS_WITH":
        return str(value).startswith(str(expected))
    if operator == "ENDS_WITH":
        return str(value).endswith(str(expected))
    return None
