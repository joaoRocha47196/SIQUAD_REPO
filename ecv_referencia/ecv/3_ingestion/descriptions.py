"""The readable description of a rule, derived from what the rule already declares.

It adds no knowledge: it joins three parts of the rule (thesis, section "Condições de aplicabilidade"):
  - the applicability expression, which gives "Se ...", with the terms joined by "e";
  - the link to the model, which prefixes each property with the model where the rule lives;
  - the restriction, which gives "→ ..."; in a RIC, replaced by the conclusion.

Example (RIR-TEMP-REFRIG-CELSIUS, on the HLM Dispositivo):
  Se Identificacao.tipoDispositivo = TEMPERATURA e Leitura.Medicao.unidadeMedida = °C
  e Leitura.Instalacao.ambiente = REFRIGERACAO → Leitura.Medicao.valor entre -30 e 0
"""
from ecv import config

from . import rule_parts as R


def _number(v):
    if isinstance(v, float) and v.is_integer():
        return str(int(v))
    return str(v)


def format_value(v):
    if isinstance(v, bool):
        return "verdadeiro" if v else "falso"
    if isinstance(v, (int, float)):
        return _number(v)
    if isinstance(v, list):
        if v and all(isinstance(x, list) and len(x) == 2 for x in v):
            return "[" + ", ".join(f"({_number(a)}, {_number(b)})" for a, b in v) + "]"
        return "[" + ", ".join(format_value(x) for x in v) + "]"
    return str(v)


def format_call(call_spec, prefix=""):
    args = []
    for a in call_spec.get("argumentos", []):
        if "caminho" in a:
            args.append(prefix + a["caminho"])
        elif "literal" in a:
            args.append(format_value(a["literal"]))
    return f"{call_spec.get('funcao')}({', '.join(args)})"


def format_check(target, operator, value=None, context=None):
    """A typed check in natural language ('valor entre -30 e 0')."""
    value_text = f"{context} (contexto externo)" if context is not None else format_value(value)
    if operator == "IN":
        return f"{target} ∈ {{{', '.join(format_value(x) for x in value)}}}"
    if operator == "RANGE":
        return f"{target} entre {format_value(value[0])} e {format_value(value[1])}"
    if operator == "LENGTH":
        if isinstance(value, list):
            return f"{target} tem entre {value[0]} e {value[1]} caracteres"
        return f"{target} tem {value} caracteres"
    symbol = config.OPERATORS[operator]["simbolo"]
    if operator in ("CONTAINS", "STARTS_WITH", "ENDS_WITH"):
        return f"{target} {symbol} \"{value}\""
    return f"{target} {symbol} {value_text}"


def path_prefix(level, model):
    """Prefix of the paths: the model name, except on the HLM (paths already start there)."""
    return "" if level == "HLM" else f"{model}."


def format_term(term, prefix=""):
    if R.is_function(term):
        return format_call(term["chamada"], prefix)
    return format_check(prefix + term["propriedade"], term["operador"], term.get("valor"), term.get("contexto"))


def format_restriction(restriction, prefix=""):
    if restriction is None:
        return ""
    if R.is_function(restriction):
        return format_call(restriction["chamada"], prefix)
    return format_check(prefix + restriction["propriedade"], restriction["operador"], restriction.get("valor"))


def format_conclusion(rule):
    c = rule.get("conclusao") or {}
    if c:
        return f"informa {config.CONCLUSION_TYPES.get(c.get('tipo'), c.get('tipo'))} {c.get('valor')}"
    return "informa"


def derive(rule, level, model):
    """Description of a rule declared on the model (level, model)."""
    prefix = path_prefix(level, model)
    terms = [format_term(t, prefix) for t in R.condition(rule)]
    if rule.get("natureza") == "inferencia_conclusiva":
        consequence = format_conclusion(rule)
    else:
        consequence = format_restriction(R.restriction(rule), prefix)
    if terms:
        return f"Se {' e '.join(terms)} → {consequence}"
    return consequence
