# Criar uma instância de teste

Escreva uma instância JSON de um modelo de dados para testar a validação. A instância segue a estrutura abaixo (as chaves são os nomes das propriedades e os papéis das composições; uma composição repetível é uma lista). Use só as propriedades listadas e respeite os valores fixados.

## Cenário

{{CENARIO}}

## O que se pretende

{{PEDIDO}}

## Estrutura (caminho: tipo, estado na projeção)

{{ESTRUTURA}}

## Regras que se aplicam

{{REGRAS}}

## Contextos externos

{{CONTEXTOS}}

## Esqueleto (a completar)

```json
{{ESQUELETO}}
```

## O que responder

Só o JSON, com a forma do esqueleto: `{"descricao": "<o que a instância testa>", "perfil" ou "hlm", "contextos": {...}, "instancia": {...}}`. Se o pedido é uma instância com erros, diga na descrição que regras devem falhar e porquê.
