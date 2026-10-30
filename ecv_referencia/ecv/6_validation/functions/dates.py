"""Dates and clocks."""
from . import implements
from .support import as_datetime, context


@implements("naoPosteriorAHoje")
def not_after_today(date, *, contexts):
    """Verdadeira quando a data indicada não é posterior à data de hoje."""
    return as_datetime(date).date() <= as_datetime(context(contexts, "dataDeHoje")).date()


@implements("excedeDiasDesdeHoje")
def exceeds_days_since_today(date, n, *, contexts):
    """Verdadeira quando passaram mais de n dias desde a data indicada até à data de hoje."""
    return (as_datetime(context(contexts, "dataDeHoje")).date() - as_datetime(date).date()).days > int(n)


@implements("desfasamentoInferiorA")
def skew_below(instant, seconds, *, contexts):
    """Verdadeira quando o instante não está adiantado mais de s segundos em relação ao relógio do servidor."""
    return (as_datetime(instant) - as_datetime(context(contexts, "relogioServidor"))).total_seconds() <= float(seconds)


@implements("naoAnteriorA")
def not_before(date, reference, *, contexts):
    """Verdadeira quando a data não é anterior à data de referência (ou quando alguma das duas falta)."""
    if date is None or reference is None:
        return True
    return as_datetime(date) >= as_datetime(reference)
