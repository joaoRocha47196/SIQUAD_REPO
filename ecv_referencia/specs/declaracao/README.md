# A Declaração ECV: estrutura final

A Declaração ECV é o ficheiro JSON (`*.ecv.json`) que contém todo o conhecimento de validação de **um HLM**: a estrutura (ECM) completa desse HLM, as regras e os elementos de que são feitas (ECR), as projeções e os perfis. É o que se gera (com ou sem LLM), se verifica, se materializa no grafo e de onde saem as vistas.

| Ficheiro | Conteúdo |
|---|---|
| [`esqueleto.ecv.json`](esqueleto.ecv.json) | Uma ocorrência de cada construção possível, com nomes neutros e `notas` a explicar cada uma. É uma declaração válida. |
| [`ecv.schema.json`](ecv.schema.json) | JSON Schema (draft 2020-12) da forma da declaração. |
| este README | A estrutura, onde fica cada coisa, todas as possibilidades e as razões das escolhas. |

## Uma declaração, um HLM

Cada declaração descreve **exatamente um HLM** (`hlm` tem um só elemento e o cabeçalho `declaracao.hlm` diz qual; o verificador dá erro S-DECL caso contrário). É uma exportação completa: tem todos os SM e USM que esse HLM compõe, com todas as suas propriedades e regras, e todas as funções, contextos externos, projeções e perfis que usa. Por isso:

- **os modelos partilhados repetem-se**: o USM `Morada` aparece, igual, nas declarações da Fatura, do Dispositivo e da Ordem de Instalação;
- **cada declaração é autossuficiente**: verifica-se, materializa-se e gera vistas sozinha, e pode ser produzida (por um LLM ou por uma pessoa) sem conhecer as outras;
- **a deduplicação é feita na ingestão**, e não na declaração: ao entrar no grafo, cada entidade é procurada pela sua identidade; o que existe e é igual é reutilizado, o que é novo é acrescentado e o que existe com outra definição é um conflito ([ecv/3_ingestion/README.md](../../ecv/3_ingestion/README.md)).

## Estrutura geral

```json
{
  "$schema": "ecv.schema.json",
  "declaracao":        { "nome", "versao", "descricao", "dominios", "hlm" },
  "contextosExternos": [ ContextoExterno ],
  "funcoes":           [ Funcao ],
  "usm":               [ USM  { propriedades[ Propriedade { regras[] } ], regras[] } ],
  "sm":                [ SM   { composicao[], propriedades[], regras[] } ],
  "hlm":               [ HLM  { composicao[], regras[] } ],     // exatamente um
  "projecoes":         [ Projecao ],
  "perfis":            [ Perfil ]
}
```

A ordem das secções segue a ordem de dependência. Primeiro vem o que é referido por nome (contextos e funções), depois a estrutura de baixo para cima (USM → SM → HLM, com as regras aninhadas onde vivem) e, por fim, o que se define sobre os HLM (projeções e perfis). A ordem dentro de cada lista é livre, mas é preservada nas vistas.

## Onde é definida cada coisa

| Conhecimento | Onde se declara | Como se refere a outras coisas | Detalhe |
|---|---|---|---|
| Cabeçalho da declaração | `declaracao` | `hlm` (nome do HLM descrito) | `nome`, `versao`, `descricao`, `dominios`, `hlm` |
| USM | `usm[]` | — | [USM.md](../entidades/ecm/USM.md) |
| SM | `sm[]` | `composicao[].usm` (nome do USM) | [SM.md](../entidades/ecm/SM.md) |
| HLM | `hlm[]` | `composicao[].sm` (nome do SM) | [HLM.md](../entidades/ecm/HLM.md) |
| Composição, papel e cardinalidade | `composicao[]` do HLM ou SM | nome do modelo composto; `papel` | [Composicao.md](../entidades/ecm/Composicao.md) |
| Propriedade | `propriedades[]` do USM (ou do SM, se residual) | — | [Propriedade.md](../entidades/ecm/Propriedade.md) |
| Regra que vive numa propriedade | `propriedades[].regras[]` | caminhos relativos ao dono da propriedade (só a própria) | [Regra.md](../entidades/ecr/Regra.md) |
| Regra que vive num modelo | `regras[]` do USM, SM ou HLM | caminhos relativos ao modelo | [Regra.md](../entidades/ecr/Regra.md) |
| RP | uma regra com `natureza: plausibilidade` e `restricao` | — | [RP.md](../entidades/ecr/RP.md) |
| RIR | uma regra com `natureza: inferencia_restritiva`, `condicao` e `restricao` | — | [RIR.md](../entidades/ecr/RIR.md) |
| RIC | uma regra com `natureza: inferencia_conclusiva`, `condicao`, `mensagem` e `conclusao` | — | [RIC.md](../entidades/ecr/RIC.md) |
| Restrição | `regra.restricao` | `propriedade` (caminho) ou `chamada.funcao` (nome) | [Restricao.md](../entidades/ecr/Restricao.md) |
| Mensagem de não conformidade | `regra.restricao.mensagem` | — | — |
| Mensagem de conclusão | `regra.mensagem` (só RIC) | — | — |
| Condição de aplicabilidade | `regra.condicao[]` (lista de termos) | `propriedade` (caminho), `contexto` (nome), `chamada.funcao` (nome) | [CondicaoAplicabilidade.md](../entidades/ecr/CondicaoAplicabilidade.md) |
| Função | `funcoes[]` | `contextosExternos[]` (nomes) | [Funcao.md](../entidades/ecr/Funcao.md) |
| Chamada a uma função | `restricao.chamada` ou `termo.chamada` | `funcao` (nome); `argumentos[]`: `{caminho}` ou `{literal}` | [Funcao.md](../entidades/ecr/Funcao.md) |
| Contexto externo | `contextosExternos[]` | — | [ContextoExterno.md](../entidades/ecr/ContextoExterno.md) |
| Projeção (RE) | `projecoes[]` | `hlm` (nome); caminhos a partir do HLM, com `*` | [RE_Projecao.md](../entidades/ecr/RE_Projecao.md) |
| Perfil | `perfis[]` | `projecao` (nome); `fixa[].propriedade` (caminho) ou `fixa[].contexto` (nome) | [Perfil.md](../entidades/ecr/Perfil.md) |
| Descrição de uma regra | `regra.descricao` | derivada | [Regra.md](../entidades/ecr/Regra.md) |
| Comentários | `notas` em qualquer entidade | — | não é conhecimento de validação |

## Todas as possibilidades, secção a secção

### `contextosExternos[]`

```json
{"nome": "dataDeHoje", "tipo": "data", "descricao": "…", "fonte": "…", "notas": "…"}
```

`nome`, `tipo` e `descricao` são obrigatórios; `fonte` e `notas` são opcionais.

### `funcoes[]`

```json
{
  "nome": "contagemInferiorA",
  "descricao": "Verdadeira quando …",
  "parametros": [
    {"nome": "instancias", "tipo": "modelo", "papel": "alvo", "colecao": true, "descricao": "…"},
    {"nome": "n", "tipo": "inteiro", "papel": "parametro"}
  ],
  "contextosExternos": [],
  "retorno": "booleano"
}
```

Possibilidades por parâmetro:

- `papel`: `alvo` (recebe um caminho) ou `parametro` (recebe um literal);
- `colecao: true`: o caminho atravessa uma composição repetível;
- `tipo`: tipo base, `lista<tipo>`, `modelo` ou outro.

`contextosExternos` vazio corresponde a FUNCTION; não vazio, a EXT_FUNCTION.

### `usm[]`

```json
{"nome": "…", "descricao": "…", "propriedades": [ … ], "regras": [ … ], "notas": "…"}
```

Pelo menos uma propriedade; não tem `composicao`.

### `sm[]`

```json
{"nome": "…", "descricao": "…",
 "composicao": [{"usm": "…", "papel": "…", "cardinalidade": "1..1"}],
 "propriedades": [ /* residuais */ ],
 "regras": [ … ]}
```

São admitidas três formas:

- com composição e sem residuais (Leitura);
- com composição e com residuais (Cliente, Localizacao);
- só com residuais, sem composição (Cabecalho, Identificacao, Pedido).

Pode compor o mesmo USM várias vezes, com papéis diferentes, e pode compor uma coleção (`1..*`, `0..*`).

### `hlm[]`

```json
{"nome": "…", "descricao": "…", "composicao": [{"sm": "…", "papel": "…", "cardinalidade": "1..1"}], "regras": [ … ]}
```

Tem exatamente um elemento (uma declaração, um HLM). Nunca tem `propriedades`. Pode compor SM com cardinalidade repetível (OrdemInstalacao → Localizacao `1..*`) e o mesmo SM com papéis diferentes.

### `propriedades[]`

```json
{"nome": "…", "tipo": "texto|inteiro|decimal|data|booleano", "descricao": "…", "nomesAlternativos": ["…"], "regras": [ … ]}
```

### Regras (`regras[]`)

Atributos comuns: `id`, `natureza`, `descricao`, `notas` e `contextosExternos` (derivado). Formas possíveis:

| Natureza | `condicao` | `restricao` | `mensagem` | `conclusao` |
|---|---|---|---|---|
| `plausibilidade` (RP) | ausente ou `[]` | obrigatória | proibida (está na restrição) | proibida |
| `inferencia_restritiva` (RIR) | ≥ 1 termo | obrigatória | proibida (está na restrição) | proibida |
| `inferencia_conclusiva` (RIC) | ≥ 1 termo | proibida | obrigatória | recomendada |

### Restrição (`restricao`)

```json
{"propriedade": "<caminho>", "operador": "<tipificado>", "valor": <forma do operador>, "mensagem": "…"}
{"operador": "FUNCTION|EXT_FUNCTION", "chamada": {"funcao": "…", "argumentos": [{"caminho": "…"}, {"literal": …}]}, "mensagem": "…"}
```

### Termo (`condicao[]`)

```json
{"propriedade": "<caminho>", "operador": "<tipificado>", "valor": <forma do operador>}
{"propriedade": "<caminho>", "operador": "EQUALS|NOT_EQUALS|LT|LTE|GT|GTE", "contexto": "<nome>"}
{"operador": "FUNCTION|EXT_FUNCTION", "chamada": {"funcao": "…", "argumentos": [ … ]}}
```

### Forma do valor por operador

| Operador | `valor` |
|---|---|
| EQUALS, NOT_EQUALS | valor simples (texto, número, booleano, data) |
| IN | lista não vazia de valores simples |
| RANGE | `[mín, máx]` (números, ou datas numa propriedade `data`) |
| LT, LTE, GT, GTE | número (ou data) |
| PATTERN | expressão regular |
| CONTAINS, STARTS_WITH, ENDS_WITH | texto |
| LENGTH | inteiro ≥ 0 ou `[mín, máx]` |

### `projecoes[]`

```json
{"nome": "…", "hlm": "…", "descricao": "…", "obrigatorias": ["X.*", "X.Y.prop"], "permitidas": [ … ]}
```

### `perfis[]`

```json
{"nome": "…", "projecao": "…", "descricao": "…",
 "fixa": [{"propriedade": "<caminho a partir do HLM>", "valor": …}, {"contexto": "<nome>", "valor": …}]}
```

## Razões das escolhas

1. **As regras ficam aninhadas onde vivem.** A posição na declaração é o alcance (eixo E5): uma regra numa propriedade lê só essa propriedade; uma regra num modelo lê a partir dele. Assim, o JSON exprime naturalmente a composição e os níveis, "onde fica cada modelo, cada propriedade e cada regra, que um texto corrido tornaria ambíguo" (tese). O invariante I8 avisa quando a regra podia viver mais abaixo.
2. **As funções e os contextos externos declaram-se à parte, uma vez.** São catálogos partilhados (`contagemInferiorA` é usada por três regras). As regras referem-nos pelo nome. A dependência de cada regra em relação a um sistema externo fica consultável (I13 avisa os não usados).
3. **A mensagem de não conformidade está na restrição, e a de conclusão na RIC.** Corresponde à tese depois da iteração que separou Restrição e Condição como entidades: a mensagem comunica a falha da restrição; numa RIC não há restrição, e a mensagem é a própria conclusão.
4. **A chamada a uma função é estruturada.** `{"funcao", "argumentos": [{caminho}|{literal}]}` em vez do texto `"somaIgualA(Linhas.Linha.valor, …)"` usado nos JSON da tese. Os alvos (caminhos) ficam explícitos e verificáveis, e cada argumento liga-se ao nó certo no grafo (LE). O texto da chamada continua a aparecer na descrição.
5. **A conclusão estruturada na RIC (`conclusao`).** A mensagem continua a transportar a conclusão. `{tipo, valor}` torna o estado ou a ação consultáveis ("que ações pode o sistema produzir?").
6. **`contextosExternos` na regra é derivado.** A tese diz que a regra declara os contextos de que depende. Aqui, isso é derivável dos termos e das funções. Pode ser declarado, por legibilidade, mas tem de coincidir (I11).
7. **A descrição é derivada e guardada.** Fica na declaração para quem lê o JSON, mas é calculada a partir da condição, da restrição e do nó (I12 avisa se divergir). `python -m ecv descricoes --escrever` atualiza-a.
8. **Sem `condicao: []` obrigatório.** Numa RP, a condição pode estar ausente ou vazia. A tese usava `"condicao": []` para tornar visível que não há condição; os dois são aceites.
9. **Os valores enumerados ficam nas RP IN, não num tipo.** Um enumerado é um texto com um Conjunto de Regras de Plausibilidade fechado (tese, Plausibilidade). Os valores plausíveis são os fatores discriminantes (I7).
10. **`papel` só quando é preciso.** Por omissão, o papel é o nome do modelo, como nos caminhos da tese (`Leitura.Medicao.valor`). Declara-se quando o mesmo modelo aparece duas vezes no mesmo nó, ou quando o papel dá o significado (`Requerente`).
11. **A projeção usa caminhos com `*`.** É compacto (`Leitura.*`) e expande-se na materialização (uma aresta por propriedade e por caminho).
12. **Uma declaração por HLM, com os modelos partilhados repetidos.** A declaração é a unidade de geração, de revisão e de versão: corresponde a um HLM e diz tudo o que é preciso para o validar. A partilha (o mesmo USM em vários HLM) não se exprime por referências entre ficheiros, que obrigariam a gerar e a verificar os ficheiros em conjunto; exprime-se no grafo, onde a fusão garante que o USM existe uma só vez e que todas as declarações o descrevem da mesma forma.
13. **`notas` em todas as entidades.** Permite documentar a declaração (anomalias intencionais, correspondência com a tese) sem misturar com o conhecimento de validação.

## Diferenças em relação aos JSON da tese

| Na tese | Na declaração final |
|---|---|
| `"mensagem"` na regra (todas) | na `restricao` (RP, RIR); na regra só em RIC |
| `"valor": "somaIgualA(Linhas.Linha.valor, Cabecalho.totalFatura)"` | `"chamada": {"funcao": "somaIgualA", "argumentos": [{"caminho": …}, …]}` |
| termo com `EXT_FUNCTION` e `"propriedade"` | termo função sem `propriedade`; os alvos são os argumentos |
| um só ficheiro com vários HLM | uma declaração por HLM; os modelos partilhados repetem-se e a ingestão funde-os |
| `contextoExterno` (singular) | `contextosExternos` (derivado) e as listas nas funções |
| identificadores `RI-…` | `RIR-…` e `RIC-…` |
| natureza `inferencia` | `inferencia_restritiva` e `inferencia_conclusiva` |
| funções e contextos sem declaração própria | secções `funcoes` e `contextosExternos` |

## Validar e usar

```bash
python -m ecv verificar specs/declaracao/esqueleto.ecv.json      # specs + invariantes (+ JSON Schema se jsonschema estiver instalado)
python -m ecv descricoes specs/declaracao/esqueleto.ecv.json --escrever
python -m ecv grafo specs/declaracao/esqueleto.ecv.json --cypher /tmp/esqueleto.cypher
python -m ecv vistas specs/declaracao/esqueleto.ecv.json -o /tmp/vistas_esqueleto
```

O esqueleto dá um aviso esperado (I10 no perfil PerfilEstatico), explicado nas suas `notas`.
