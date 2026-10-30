# Catálogo: tipos base, operadores e forma dos valores

O catálogo é o vocabulário fechado da linguagem de verificações tipificadas. É a mesma linguagem da restrição e de cada termo da condição. Com um vocabulário fechado, qualquer regra pode ser verificada antes de ser usada, seja qual for a sua origem, incluindo regras geradas por um LLM. A fonte única é [ecv/config/ecv.config.json](../../../ecv/config/ecv.config.json), lida diretamente pelo código (`ecv/config/__init__.py`).

## Tipos base

| Tipo | Valor | Notas |
|---|---|---|
| `texto` | cadeia de caracteres | Um enumerado é um texto com uma RP `IN`. |
| `inteiro` | número inteiro | |
| `decimal` | número | |
| `data` | `AAAA-MM-DD` ou data e hora ISO 8601 | Compara-se por ordem; `RANGE`, `LT` e outros aceitam datas. |
| `booleano` | `true` / `false` | |

## Operadores

| Operador | Uso | Valor esperado | Exemplo |
|---|---|---|---|
| `EQUALS` | igual a um valor | valor simples | `tipoDispositivo EQUALS TEMPERATURA` |
| `NOT_EQUALS` | diferente de um valor | valor simples | `Cliente.Entidade.nif NOT_EQUALS 999999990` |
| `IN` | pertence a um conjunto (um só desses valores) | lista não vazia | `tipoDocumento IN [FT, FS, FR, NC, ND]` |
| `RANGE` | num intervalo, inclusive | `[mín, máx]`, mín ≤ máx | `latitude RANGE [-90, 90]` |
| `LT`, `LTE`, `GT`, `GTE` | comparação | número (ou data) | `totalFatura LTE 1000`; `dataUltimaManutencao GTE 2000-01-01` |
| `PATTERN` | expressão regular | regex válida | `codigoPostal PATTERN ^[1-9][0-9]{3}-[0-9]{3}$` |
| `CONTAINS`, `STARTS_WITH`, `ENDS_WITH` | parte de um texto | texto | `numero STARTS_WITH FS`; `email ENDS_WITH @companhiax.com` |
| `LENGTH` | comprimento | inteiro, ou `[mín, máx]` | `fabricante LENGTH [2, 50]` |
| `FUNCTION` | chamada a uma função que só usa valores do modelo e da regra | `chamada` | `somaIgualA(Linhas.Linha.valor, Cabecalho.totalFatura)` |
| `EXT_FUNCTION` | chamada a uma função que usa também contextos externos | `chamada` | `excedeDiasDesdeHoje(dataUltimaManutencao, 7)` |

Os operadores organizam-se em cinco grupos:

- **Igualdade e pertença:** enumerados.
- **Intervalo e comparação:** gamas e limites.
- **Padrão:** formatos.
- **Texto:** partes e comprimento.
- **Função:** delegação.

Num termo que compara com um contexto externo, o operador é `EQUALS`, `NOT_EQUALS`, `LT`, `LTE`, `GT` ou `GTE`.

## Operadores admissíveis por tipo base (I5)

| Tipo base | Verificações aplicáveis |
|---|---|
| texto | EQUALS, NOT_EQUALS, IN, PATTERN, LENGTH, CONTAINS, STARTS_WITH, ENDS_WITH |
| inteiro, decimal | EQUALS, NOT_EQUALS, IN, RANGE, LT, LTE, GT, GTE; PATTERN sobre a representação (por exemplo, casas decimais) |
| data | EQUALS, NOT_EQUALS, RANGE, LT, LTE, GT, GTE |
| booleano | EQUALS |
| qualquer tipo | FUNCTION, EXT_FUNCTION (a função não tem alvo próprio) |

## Nas declarações de exemplo

<!-- gerar:tabela-operadores -->
| Operador | Grupo | Forma do valor | Tipos base | Restrições nos exemplos | Termos nos exemplos |
|---|---|---|---|---|---|
| EQUALS | igualdade e pertença | valor | texto, inteiro, decimal, data, booleano | 5 | 188 |
| NOT_EQUALS | igualdade e pertença | valor | texto, inteiro, decimal, data | 1 | 0 |
| IN | igualdade e pertença | lista | texto, inteiro, decimal | 13 | 0 |
| RANGE | intervalo e comparação | intervalo | inteiro, decimal, data | 45 | 4 |
| LT | intervalo e comparação | numero | inteiro, decimal, data | 0 | 1 |
| LTE | intervalo e comparação | numero | inteiro, decimal, data | 1 | 0 |
| GT | intervalo e comparação | numero | inteiro, decimal, data | 0 | 1 |
| GTE | intervalo e comparação | numero | inteiro, decimal, data | 4 | 0 |
| PATTERN | padrão | padrao | texto, inteiro, decimal | 36 | 0 |
| CONTAINS | texto | texto | texto | 0 | 0 |
| STARTS_WITH | texto | texto | texto | 1 | 0 |
| ENDS_WITH | texto | texto | texto | 2 | 0 |
| LENGTH | texto | comprimento | texto | 1 | 0 |
| FUNCTION | função | chamada | qualquer tipo | 8 | 1 |
| EXT_FUNCTION | função | chamada | qualquer tipo | 7 | 1 |
<!-- /gerar -->

## Navegação por tipo de verificação

Ter a terminologia do lado da solução permite questionar o conhecimento por tipo de verificação. Por exemplo: todas as regras IN (os enumerados), todas as STARTS_WITH, ou as gamas RANGE sobre uma propriedade, para detetar incoerências. Ver as vistas `operadores`, `decisao` e `coerencia`.
