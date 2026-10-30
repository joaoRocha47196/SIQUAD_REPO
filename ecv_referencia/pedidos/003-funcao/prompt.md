# Implementação de uma função ECV

Uma função ECV é declarada numa declaração (nome, parâmetros, contextos externos e uma descrição da forma
"Verdadeira quando…") e chamada pelas regras. O motor de validação (módulo 6) só a consegue avaliar se
houver uma implementação em Python registada com o nome declarado. Sem implementação, as regras que a
chamam ficam "não avaliável".

## A função a implementar

```json
{
 "nome": "nenhumPresente",
 "descricao": "Verdadeira quando nenhum dos dois valores indicados está presente.",
 "parametros": [
  {
   "nome": "primeiro",
   "tipo": "valor",
   "papel": "alvo"
  },
  {
   "nome": "segundo",
   "tipo": "valor",
   "papel": "alvo"
  }
 ],
 "retorno": "booleano",
 "contextosExternos": []
}
```

## Regras que a chamam

- RIR-DECOMP-SEM-ISENCAO: Se DecomposicaoIva.CategoriaIva.codigoCategoria ∈ {S, NOR, AA, RED, INT} → nenhumPresente(DecomposicaoIva.CategoriaIva.motivoIsencao, DecomposicaoIva.CategoriaIva.codigoMotivoIsencao)
- RIR-LIN-SEM-ISENCAO: Se LinhaDocumento.CategoriaIva.codigoCategoria ∈ {S, NOR, AA, RED, INT} → nenhumPresente(LinhaDocumento.CategoriaIva.motivoIsencao, LinhaDocumento.CategoriaIva.codigoMotivoIsencao)

## Contrato

- O módulo regista a função com o decorador `@implements("<nome declarado>")`, importado de `ecv.validation.functions`.
- A implementação recebe os argumentos pela ordem dos parâmetros declarados e os contextos externos como
  argumento nomeado `contexts` (um dicionário nome → valor).
- Devolve `True` quando a função é verdadeira e `False` caso contrário.
- Quando falta um valor ou um contexto externo necessário, levanta `Unavailable` (de `ecv.validation.functions.support`):
  a regra fica "não avaliável" em vez de falhar.
- Um parâmetro marcado como coleção recebe uma lista (pode conter `None`).
- Só biblioteca padrão. Sem acesso a rede nem a ficheiros.
- A docstring da função repete a descrição declarada.

## Auxiliares disponíveis (ecv/6_validation/functions/support.py)

```python
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

```

## Exemplo de um módulo existente

```python
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

```

## Resposta

Responde só com o código Python completo do módulo (sem texto à volta). O código é gravado em
`ecv/6_validation/functions/f_nenhum_presente.py` e carregado pelo motor.
