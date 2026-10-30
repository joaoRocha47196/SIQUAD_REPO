"""Checks over collections: counts, sums, uniqueness and sequences."""
from . import implements
from .support import Unavailable, present


@implements("contagemInferiorA")
def count_below(instances, n, *, contexts):
    """Verdadeira quando a coleção tem menos de n instâncias."""
    return len(instances or []) < int(n)


@implements("somaIgualA")
def sum_equals(values, total, *, contexts):
    """Verdadeira quando a soma dos valores da coleção, arredondada ao cêntimo, é igual ao total."""
    if total is None:
        raise Unavailable("falta o total")
    return round(sum(float(x) for x in present(values)), 2) == round(float(total), 2)


@implements("valoresUnicos")
def unique_values(values, *, contexts):
    """Verdadeira quando nenhum valor da coleção se repete."""
    v = present(values)
    return len(v) == len(set(v))


@implements("valoresConsecutivos")
def consecutive_values(values, *, contexts):
    """Verdadeira quando os valores da coleção começam em 1 e não têm falhas."""
    v = present(values)
    return sorted(int(x) for x in v) == list(range(1, len(v) + 1))
