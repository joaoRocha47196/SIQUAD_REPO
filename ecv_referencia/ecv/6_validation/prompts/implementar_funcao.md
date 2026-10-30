# Implementação de uma função ECV

Uma função ECV é declarada numa declaração (nome, parâmetros, contextos externos e uma descrição da forma
"Verdadeira quando…") e chamada pelas regras. O motor de validação (módulo 6) só a consegue avaliar se
houver uma implementação em Python registada com o nome declarado. Sem implementação, as regras que a
chamam ficam "não avaliável".

## A função a implementar

{{FUNCAO}}

## Regras que a chamam

{{REGRAS}}

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
{{AUXILIARES}}
```

## Exemplo de um módulo existente

```python
{{EXEMPLO}}
```

## Resposta

Responde só com o código Python completo do módulo (sem texto à volta). O código é gravado em
`ecv/6_validation/functions/{{FICHEIRO}}` e carregado pelo motor.
