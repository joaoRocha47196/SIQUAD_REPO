# Criar um adaptador da fase 0

Escreva um módulo Python que lê uma fonte num formato que ainda não tem adaptador e devolve um inventário. A fase 0 é determinística: o adaptador não chama nenhum LLM, só lê o ficheiro.

## O formato

Nome do adaptador (campo `adaptador` em dominio.json): `{{NOME}}`

{{DESCRICAO}}

## Amostra da fonte

{{AMOSTRA}}

## O inventário

{{INVENTARIO}}

## Classificação das regras

{{CLASSIFICACAO}}

## Exemplo: um adaptador existente

```python
{{EXEMPLO}}
```

## O que responder

Só o código do módulo (ficheiro `{{FICHEIRO}}`), sem texto à volta:

- `NAME = "{{NOME}}"` e `DESCRIPTION = "<uma linha: o formato que lê>"`;
- `def adapt(path) -> Inventory`, com `path` o caminho do ficheiro (ou da pasta) da fonte;
- importações relativas: `from ..inventory import Element, Group, Inventory, SourceRule` e `from ..classification import base_type, classify`;
- um grupo por conjunto de elementos com significado próprio na fonte; um elemento por informação atómica, com descrição, tipo de base, cardinalidade e valores admitidos quando a fonte os dá; uma regra por regra declarada na fonte, com a categoria e a natureza dadas por `classify(texto, expressao)`;
- a origem de cada item (ficheiro e linha ou caminho) em `origin`;
- só a biblioteca padrão.
