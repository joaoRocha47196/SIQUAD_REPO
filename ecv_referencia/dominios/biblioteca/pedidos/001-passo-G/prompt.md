# Papel

És um especialista em modelação de dados e em conhecimento de validação. Trabalhas com a ECV (Estratificação do Conhecimento de Validação): a ECM organiza a estrutura em HLM, SM e USM; a ECR organiza as regras pela natureza (RE, RP, RIR, RIC), pelo alcance (onde vivem) e pela expressividade (catálogo ou função). Produzes Declarações ECV a partir de fontes de dados existentes.

# Domínio

Biblioteca municipal: Obras, exemplares, leitores, empréstimos e reservas de uma biblioteca municipal, descritos em linguagem natural (sem esquema de origem): serve para testar se um LLM gera a declaração ECV a partir só de texto.

# Princípios comuns

- A fonte interpreta-se, não se copia: extrai-se a lógica de estruturação e de validação, sem depender do formato (XML, schematron, JSON Schema, classes, registos) nem dos nomes técnicos.
- A modularização da fonte não é para seguir à regra: os grupos da fonte são pistas, não submodelos.
- Cada decisão fica rastreável: cada elemento e cada regra da fonte têm, no mapeamento, o destino na declaração ou o motivo por que foram descartados.
- Antes de criar, procura-se: um modelo, uma propriedade, uma função ou um contexto que já exista no grafo (ou noutra declaração do domínio) reutiliza-se.
- Uma declaração descreve um só HLM e é completa: os modelos partilhados repetem-se, iguais, em cada declaração que os usa.
- Nomes em português, sem acentos: modelos em PascalCase, propriedades, funções e contextos em camelCase, regras TIPO-ASSUNTO[-QUALIFICADOR]; os nomes da fonte ficam em nomesAlternativos.
- Só se usa o vocabulário fechado da configuração (tipos base, operadores, cardinalidades, tipos de regra).

# Especificação

A especificação completa da ECV (vocabulário fechado, estrutura da declaração, entidades, caminhos, nomes e verificações) está na secção "Especificação da ECV". Tudo o que produzes tem de a cumprir: o código verifica cada resposta antes de a aplicar.

# Geração da declaração completa

## Objetivo

Produzir, num só pedido, as declarações completas do domínio (estrutura, projeções, regras de plausibilidade e de inferência, funções, contextos externos e perfis) e o mapeamento de cada elemento e de cada regra das fontes.

Pergunta a que respondes: Que declarações ECV descrevem o domínio, e onde fica cada item do inventário?

Recebes todo o inventário do domínio: os grupos e os elementos de cada fonte e todas as regras que as fontes declaram. Cada item tem um lugar na declaração, ou um motivo para ficar de fora. A revisão que se segue (por camadas) corrige e completa o que fizeres, mas a resposta tem de ser já uma declaração completa e válida.

## Como proceder, camada a camada

Constrói as declarações por esta ordem; cada camada usa as anteriores.

### A · Estrutura (ECM)

Decidir os HLM, SM e USM do domínio, as propriedades de cada modelo e as composições (papel e cardinalidade), submodularizando em modelos atómicos e reutilizáveis; acrescentar aos HLM principais o SM de metainformação.

Princípios:
- HLM: a entidade que o domínio instancia e trata como um todo (uma fatura, uma nota de crédito, um dispositivo). Só compõe SM; não tem propriedades.
- USM: informação canónica, igual em qualquer domínio (morada, contacto, identificação fiscal, coordenadas, montante com moeda). É dono das suas propriedades. Um grupo da fonte que se repete em vários contextos (morada do fornecedor, do cliente, de entrega) é UM USM, composto várias vezes com papéis diferentes.
- SM: agrupa USM com uma finalidade no domínio (Fornecedor, Cliente, Linhas, Totais). Pode ter propriedades residuais (as que só fazem sentido ali). Uma lista da fonte (0..N, 1..N) é uma composição repetível de um SM de coleção ou de um USM.
- Propriedade: atómica, com tipo base; o significado vem da descrição da fonte, reescrita em português claro; os nomes da fonte que valem em qualquer ocorrência ficam em nomesAlternativos; os códigos que identificam uma ocorrência (BT-27, BT-44) ficam no mapeamento, por caminho.
- Atomicidade: um USM tem uma só razão para existir; se um grupo da fonte mistura conceitos (identificação + morada + contacto), divide-se.
- Reutilização: antes de criar um USM, procurar no grafo um com as mesmas propriedades (pela pesquisa de semelhantes); se existir, reutiliza-se, mesmo que venha de outro domínio.
- Fontes que se completam: elementos de fontes diferentes com o mesmo significado (BT-44 'Nome do cliente' e Client.name do FM) são UMA propriedade; a diferença fica em nomesAlternativos.
- Metainformação: cada HLM principal compõe o SM Metainformacao (0..1, propriedades da configuração), com a origem do modelo de dados.

Procedimento:
1. Compreensão global: lê os grupos e os elementos de todas as fontes; identifica que entidades cada fonte descreve e como os grupos se relacionam (contenção, repetição, referência); nota onde fontes diferentes descrevem a mesma informação.
2. Agrupamento semântico: junta os elementos por conceito (identificação, morada, contacto, montante, período, referência a outro documento), atravessando grupos e fontes; um elemento pertence a um só conceito.
3. USM atómicos e reutilizáveis: cada conceito canónico é um USM; o mesmo conceito em vários contextos (morada do fornecedor, do cliente, de entrega) é UM USM, composto várias vezes com papéis diferentes. Antes de criar um USM, procura nos modelos existentes um equivalente e reutiliza-o com o mesmo nome e a mesma definição.
4. SM com finalidade: os conjuntos com papel no domínio (Fornecedor, Cliente, Linhas, Totais, Pagamento) são SM que compõem USM; as propriedades que só fazem sentido ali são residuais do SM; uma coleção de linhas é um SM de coleção (no plural) que compõe o USM da linha com 1..*.
5. HLM: só as entidades de topo que o domínio instancia; cada HLM tem a sua declaração.
6. Composições: a cardinalidade (da fonte; na dúvida, a mais permissiva) e o papel (quando o mesmo modelo aparece mais de uma vez no mesmo nó, ou quando o papel dá o significado).
7. Metainformação: cada HLM principal compõe o SM Metainformacao (0..1), com as propriedades do vocabulário.
8. Propriedades: nome em camelCase português, tipo base, descrição reescrita; em nomesAlternativos os nomes da fonte que valem em qualquer ocorrência; os códigos que identificam uma ocorrência (BT-27, BT-44) ficam no mapeamento. Um modelo reutilizado não recebe nomes alternativos novos.
9. Mapeamento de cada elemento: mapeado (destino HLM:<Hlm>/<caminho>), fundido (o mesmo significado que outro elemento já mapeado) ou descartado (com o motivo).

### B · Projeções (RE)

Declarar as utilizações de cada HLM (projeções) com as propriedades obrigatórias e permitidas: as regras estruturais.

Princípios:
- A obrigatoriedade de uma propriedade numa utilização exprime-se na projeção, não numa regra.
- Uma projeção por utilização real (fatura eletrónica CIUS-PT, nota de crédito, exportação FM); não se inventam utilizações.
- Caminhos a partir do HLM; X.* para tudo abaixo de X; um caminho não pode ser obrigatório e permitido ao mesmo tempo.
- Regras de presença condicionais ('se existir X, então Y é obrigatório') não são projeções: são RIR (com uma função de presença).

Procedimento:
1. Para cada HLM, uma projeção por utilização real do domínio (as utilizações estão nos dados).
2. Cada regra de presença ou de cardinalidade da fonte torna a propriedade obrigatória (OBRIGATORIA) numa ou mais projeções; o que não é obrigatório mas pode estar presente é permitido; o resto fica excluído (não se declara).
3. Caminhos a partir do HLM; X.* quando tudo abaixo de X tem o mesmo tratamento.
4. Uma regra de presença condicional ("se…, então… é obrigatório") não é uma projeção: é uma RIR com uma função de presença (ver funções).
5. Mapeamento de cada regra tratada: destino Projecao:<Nome>/<caminho>, ou descartada com o motivo.

### C · Plausibilidade (RP)

Declarar os valores que cada propriedade pode tomar, sempre: formatos, listas de valores, gamas.

Princípios:
- Uma RP vive na propriedade que restringe e só a lê.
- Um enumerado é uma RP IN; um formato é PATTERN ou LENGTH; uma gama é RANGE (ou LT/GT).
- Se a lista ou a gama depende de outra propriedade, não é plausibilidade: é uma RIR (na RP fica só o conjunto de todos os valores possíveis).
- A mensagem de não conformidade está na restrição, em português, e diz o que falhou e o que se espera.
- Uma regra de formato que é igual em várias propriedades do mesmo USM declara-se uma vez em cada propriedade; uma regra igual em vários USM é sinal de um USM a reutilizar.

Procedimento:
1. Para cada regra de formato, de valores ou de gama, e para cada elemento com valores admitidos, encontra a propriedade a que se refere.
2. Se a regra vale sempre, é uma RP na propriedade: restrição com o operador do catálogo (IN, PATTERN, LENGTH, RANGE, LT, GT, …), o valor na forma que o operador exige e a mensagem de não conformidade em português. Se depende de outra informação, é uma RIR (e a RP fica com o conjunto de todos os valores possíveis).
3. Junta regras da fonte que dizem o mesmo sobre a mesma propriedade numa só RP (registando todas no mapeamento).
4. Identificador RP-<ASSUNTO>[-<QUALIFICADOR>], único. Não escrevas a descrição: é derivada.
5. Mapeamento de cada regra: destino Regra:<id>, ou descartada com o motivo.

### D · Inferência (RIR e RIC)

Declarar as regras que só se aplicam quando outra informação tem um dado valor (RIR) e as que concluem um estado ou uma ação (RIC), incluindo os mapeamentos conhecidos (tabelas de decisão).

Princípios:
- Uma RIR tem condição (termos com E) e uma restrição com um só alvo; não há OU entre termos (usa-se IN, ou regras separadas).
- A condição não lê o alvo da restrição.
- A regra vive no menor nó que contém tudo o que lê (alcance).
- Os valores dos termos têm de ser plausíveis (I7): se a RP não os admite, corrigir a RP ou a regra.
- Uma regra que, satisfeita a condição, comunica um estado ou uma ação, e não restringe nada, é uma RIC.
- Um mapeamento conhecido (tabela de decisão) dá uma RIR por combinação: confirma-se na vista de decisão.
- Uma regra condicional cuja restrição não cabe num operador do catálogo (presença de uma propriedade, comparação entre duas propriedades, contagem) usa uma função: um termo e/ou uma restrição por função.

Procedimento:
1. Para cada regra condicional ou de exclusão, identifica os fatores discriminantes (o que decide se a regra se aplica) e o alvo (o que é restringido).
2. RIR: condição (termos com E; vários valores do mesmo fator com IN) + restrição com um só alvo; uma regra com OU entre fatores diferentes divide-se em várias RIR.
3. RIC: satisfeita a condição, comunica um estado ou uma ação: condição + mensagem + conclusão {tipo: ACAO | ESTADO, valor}.
4. A regra vive no menor nó que contém tudo o que lê; os caminhos são relativos a esse nó.
5. Os valores dos termos pertencem aos valores plausíveis da propriedade (as RP).
6. Um mapeamento conhecido (tabela de decisão do domínio) dá uma RIR por combinação de valores.
7. Se a restrição não cabe num operador do catálogo ("então Y tem de existir", "Y maior que Z", contagens), usa uma função (ver funções).
8. Mapeamento de cada regra: destino Regra:<id>, ou descartada com o motivo.

### E · Funções e contextos externos

Declarar as verificações que não se exprimem com o catálogo (somas, totais, coerência entre coleções, dígitos de controlo, comparações com valores externos) como funções declaradas, os contextos externos de que dependem e as regras que as chamam.

Princípios:
- Uma função declara-se uma vez (nome, 'Verdadeira quando…', parâmetros alvo e literais, contextos externos, retorno booleano) e chama-se de forma estruturada.
- Uma função genérica (somaIgualA, contagemInferiorA) reutiliza-se em várias regras e domínios; procurar antes de criar.
- Um argumento que atravessa uma coleção tem de passar por uma composição repetível.
- EXT_FUNCTION só para funções com contextos externos; FUNCTION para as restantes.
- Um contexto externo (a data de hoje, o hash anterior, uma tabela externa) declara-se com tipo, descrição e fonte.
- As regras condicionais que não cabem no catálogo (presença condicional, comparação entre propriedades) exprimem-se com uma função: a RIR tem um termo e/ou uma restrição por função.

Procedimento:
1. Para cada regra de cálculo ou cruzada (somas, totais, contagens, coerência entre linhas e totais, dígitos de controlo, comparações com valores externos) e para cada regra condicional que não cabe no catálogo, decide a função que a exprime.
2. Procura primeiro nas funções existentes: uma função genérica reutiliza-se. Só depois declara uma nova: nome em camelCase, descrição "Verdadeira quando…", parâmetros (alvo, com coleção quando atravessa uma lista; ou literal), contextos externos, retorno booleano.
3. Declara os contextos externos de que as funções dependem (tipo, descrição, fonte).
4. A regra que chama a função é uma RP (restrição por função) ou uma RIR (termo e/ou restrição por função), no menor nó que contém os alvos; operador EXT_FUNCTION se a função tem contextos externos, FUNCTION se não.
5. Mapeamento de cada regra.

### F · Perfis de execução

Declarar os cenários de utilização: que projeção se usa e que valores (propriedades e contextos externos) são conhecidos antes da execução, para tornar a seleção estática.

Princípios:
- Um perfil usa uma projeção e fixa valores conhecidos antes da execução.
- Fixar um fator discriminante torna estática a seleção das regras que dele dependem; os valores fixados têm de ser plausíveis.
- Uma regra cuja condição lê propriedades nem projetadas nem fixadas não é avaliável no perfil (I10): corrigir a projeção ou o perfil.

Procedimento:
1. Para cada cenário real do domínio (nos dados), um perfil que usa a projeção da utilização.
2. Fixa no perfil os valores conhecidos antes de validar (o tipo de documento, a moeda, o país, o ambiente de instalação, a data de referência): propriedades (caminho a partir do HLM) e contextos externos.
3. Prefere fixar as propriedades lidas nas condições de muitas RIR: a seleção das regras fica estática.
4. Nenhuma regra fica não avaliável: se a condição lê uma propriedade nem projetada nem fixada, fixa-a ou acrescenta-a à projeção.

## Antes de responder

- Nenhum HLM tem propriedades; nenhum USM compõe outros modelos; os nomes são únicos e estão no formato certo.
- Os modelos partilhados são iguais em todas as declarações que os usam; as funções e os contextos externos que as regras de uma declaração usam estão nessa declaração.
- Cada regra vive no menor nó que contém tudo o que lê; os valores dos termos são plausíveis; nenhuma regra fica não avaliável num perfil.
- Cada elemento e cada regra de cada fonte tem uma entrada no mapeamento.
- O que é duvidoso, e o que ficou de fora por falta de informação, fica em notas: a pessoa vê-as na revisão.

## Especificação da ECV (completa)

# Especificação da ECV (versão para o LLM)

Este texto é gerado a partir das specs do repositório (specs/) por ecv/1_ecv_builder/specs_bundle.py. Contém as regras completas do formato da Declaração ECV: o vocabulário fechado, a estrutura da declaração, cada entidade (ECM e ECR), os caminhos, os nomes e as verificações que o código faz a cada resposta. Tudo o que se produz tem de as cumprir.

## Vocabulário fechado

Tipos base: texto, inteiro, decimal, data, booleano.
Cardinalidades das composições: 0..1, 1..1, 0..*, 1..*.

Operadores (forma do valor; tipos base em que se admitem):
- EQUALS: o valor é igual ao esperado. Valor: um valor simples (texto, número, data ou booleano). Tipos: texto, inteiro, decimal, data, booleano. Pode comparar com um contexto externo.
- NOT_EQUALS: o valor é diferente do indicado. Valor: um valor simples (texto, número, data ou booleano). Tipos: texto, inteiro, decimal, data. Pode comparar com um contexto externo.
- IN: o valor é um dos da lista. Valor: lista não vazia de valores simples. Tipos: texto, inteiro, decimal.
- RANGE: o valor está entre o mínimo e o máximo (inclusive). Valor: [mínimo, máximo], com mínimo <= máximo. Tipos: inteiro, decimal, data.
- LT: o valor é menor. Valor: um número (ou uma data, sobre propriedades do tipo data). Tipos: inteiro, decimal, data. Pode comparar com um contexto externo.
- LTE: o valor é menor ou igual. Valor: um número (ou uma data, sobre propriedades do tipo data). Tipos: inteiro, decimal, data. Pode comparar com um contexto externo.
- GT: o valor é maior. Valor: um número (ou uma data, sobre propriedades do tipo data). Tipos: inteiro, decimal, data. Pode comparar com um contexto externo.
- GTE: o valor é maior ou igual. Valor: um número (ou uma data, sobre propriedades do tipo data). Tipos: inteiro, decimal, data. Pode comparar com um contexto externo.
- PATTERN: o valor segue a expressão regular. Valor: expressão regular. Tipos: texto, inteiro, decimal.
- CONTAINS: o texto contém o indicado. Valor: texto não vazio. Tipos: texto.
- STARTS_WITH: o texto começa pelo indicado. Valor: texto não vazio. Tipos: texto.
- ENDS_WITH: o texto termina no indicado. Valor: texto não vazio. Tipos: texto.
- LENGTH: o texto tem o comprimento indicado (ou dentro do intervalo). Valor: inteiro >= 0, ou [mínimo, máximo]. Tipos: texto.
- FUNCTION: verificação delegada numa função declarada, sem contexto externo. Valor: {"funcao": nome, "argumentos": [{"caminho": …} | {"literal": …}]}. Tipos: qualquer (função).
- EXT_FUNCTION: verificação delegada numa função que depende de contextos externos. Valor: {"funcao": nome, "argumentos": [{"caminho": …} | {"literal": …}]}. Tipos: qualquer (função).

Tipos de regra:
- RE (regra estrutural; natureza expressa pela projeção): Diz que propriedades são obrigatórias, permitidas ou excluídas numa utilização. Não é declarada como regra: exprime-se pelas projeções.
- RP (regra de plausibilidade; natureza plausibilidade): Valores que a propriedade pode tomar, sempre, sem depender de outras propriedades. Tem uma restrição e não tem condição.
- RIR (regra de inferência restritiva; natureza inferencia_restritiva): Restrição que só se aplica quando a condição de aplicabilidade se verifica (os fatores discriminantes). Tem condição e restrição.
- RIC (regra de inferência conclusiva; natureza inferencia_conclusiva): Quando a condição se verifica, produz uma conclusão (ação ou estado) com a sua mensagem. Não restringe: não há não conformidade.

Tipos de conclusão de uma RIC: ACAO (Ação), ESTADO (Estado).
Papéis dos parâmetros de uma função: alvo (argumento que é um caminho na instância), parametro (argumento literal).

Nomes (expressões regulares):
- modelo: `^[A-Z][A-Za-z0-9]*$`
- propriedade: `^[a-z][A-Za-z0-9]*$`
- funcao: `^[a-z][A-Za-z0-9]*$`
- contexto: `^[a-z][A-Za-z0-9]*$`
- regra: `^(RP|RIR|RIC)-[A-Z0-9]+(-[A-Z0-9]+)*$`

SM de metainformação: Metainformacao (0..1), composto pelos HLM principais, com as propriedades:
- origemModelo (texto): Fonte do modelo de dados (norma, sistema ou repositório)
- versaoOrigem (texto): Versão da fonte usada
- referenciaOrigem (texto): Identificador da entidade na fonte (ex.: BG-0 Invoice, Device)
- utilizacao (texto): Finalidade ou contexto de utilização do modelo
- dominio (texto): Domínio a que o modelo pertence
- observacoes (texto): Outra metainformação relevante sobre o modelo

## A declaração ECV

### Uma declaração, um HLM

Cada declaração descreve **exatamente um HLM** (`hlm` tem um só elemento e o cabeçalho `declaracao.hlm` diz qual; o verificador dá erro S-DECL caso contrário). É uma exportação completa: tem todos os SM e USM que esse HLM compõe, com todas as suas propriedades e regras, e todas as funções, contextos externos, projeções e perfis que usa. Por isso:

- **os modelos partilhados repetem-se**: o USM `Morada` aparece, igual, nas declarações da Fatura, do Dispositivo e da Ordem de Instalação;
- **cada declaração é autossuficiente**: verifica-se, materializa-se e gera vistas sozinha, e pode ser produzida (por um LLM ou por uma pessoa) sem conhecer as outras;
- **a deduplicação é feita na ingestão**, e não na declaração: ao entrar no grafo, cada entidade é procurada pela sua identidade; o que existe e é igual é reutilizado, o que é novo é acrescentado e o que existe com outra definição é um conflito (ecv/3_ingestion/README.md).

### Estrutura geral

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

### Todas as possibilidades, secção a secção

#### `contextosExternos[]`

```json
{"nome": "dataDeHoje", "tipo": "data", "descricao": "…", "fonte": "…", "notas": "…"}
```

`nome`, `tipo` e `descricao` são obrigatórios; `fonte` e `notas` são opcionais.

#### `funcoes[]`

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

#### `usm[]`

```json
{"nome": "…", "descricao": "…", "propriedades": [ … ], "regras": [ … ], "notas": "…"}
```

Pelo menos uma propriedade; não tem `composicao`.

#### `sm[]`

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

#### `hlm[]`

```json
{"nome": "…", "descricao": "…", "composicao": [{"sm": "…", "papel": "…", "cardinalidade": "1..1"}], "regras": [ … ]}
```

Tem exatamente um elemento (uma declaração, um HLM). Nunca tem `propriedades`. Pode compor SM com cardinalidade repetível (OrdemInstalacao → Localizacao `1..*`) e o mesmo SM com papéis diferentes.

#### `propriedades[]`

```json
{"nome": "…", "tipo": "texto|inteiro|decimal|data|booleano", "descricao": "…", "nomesAlternativos": ["…"], "regras": [ … ]}
```

#### Regras (`regras[]`)

Atributos comuns: `id`, `natureza`, `descricao`, `notas` e `contextosExternos` (derivado). Formas possíveis:

- `plausibilidade` (RP) — `condicao`: ausente ou `[]`; `restricao`: obrigatória; `mensagem`: proibida (está na restrição); `conclusao`: proibida
- `inferencia_restritiva` (RIR) — `condicao`: ≥ 1 termo; `restricao`: obrigatória; `mensagem`: proibida (está na restrição); `conclusao`: proibida
- `inferencia_conclusiva` (RIC) — `condicao`: ≥ 1 termo; `restricao`: proibida; `mensagem`: obrigatória; `conclusao`: recomendada

#### Restrição (`restricao`)

```json
{"propriedade": "<caminho>", "operador": "<tipificado>", "valor": <forma do operador>, "mensagem": "…"}
{"operador": "FUNCTION|EXT_FUNCTION", "chamada": {"funcao": "…", "argumentos": [{"caminho": "…"}, {"literal": …}]}, "mensagem": "…"}
```

#### Termo (`condicao[]`)

```json
{"propriedade": "<caminho>", "operador": "<tipificado>", "valor": <forma do operador>}
{"propriedade": "<caminho>", "operador": "EQUALS|NOT_EQUALS|LT|LTE|GT|GTE", "contexto": "<nome>"}
{"operador": "FUNCTION|EXT_FUNCTION", "chamada": {"funcao": "…", "argumentos": [ … ]}}
```

#### Forma do valor por operador

- EQUALS, NOT_EQUALS — `valor`: valor simples (texto, número, booleano, data)
- IN — `valor`: lista não vazia de valores simples
- RANGE — `valor`: `[mín, máx]` (números, ou datas numa propriedade `data`)
- LT, LTE, GT, GTE — `valor`: número (ou data)
- PATTERN — `valor`: expressão regular
- CONTAINS, STARTS_WITH, ENDS_WITH — `valor`: texto
- LENGTH — `valor`: inteiro ≥ 0 ou `[mín, máx]`

#### `projecoes[]`

```json
{"nome": "…", "hlm": "…", "descricao": "…", "obrigatorias": ["X.*", "X.Y.prop"], "permitidas": [ … ]}
```

#### `perfis[]`

```json
{"nome": "…", "projecao": "…", "descricao": "…",
 "fixa": [{"propriedade": "<caminho a partir do HLM>", "valor": …}, {"contexto": "<nome>", "valor": …}]}
```

## Modelos (ECM)

### HLM: High Level Model (modelo de alto nível)

#### Descrição

O HLM é o nível de topo da ECM: a entidade que o domínio instancia e a que chama "um modelo", como uma fatura, um dispositivo ou uma ordem de instalação. É o nível de maior especificidade contextual. Um HLM não declara propriedades próprias. É exclusivamente uma composição de submodelos (SM).

#### Atributos

- `nome` — tipo: texto, PascalCase; obrigatório: sim; descrição: Identificador do HLM, único entre os HLM.
- `descricao` — tipo: texto (≥ 10 caracteres); obrigatório: sim; descrição: O que o modelo representa, em linguagem natural. Aparece nas vistas.
- `composicao` — tipo: lista de composições (≥ 1); obrigatório: sim; descrição: Os SM que compõe; ver Composicao.md.
- `regras` — tipo: lista de regras; obrigatório: não; descrição: Regras que vivem no HLM (o alcance é o HLM).
- `notas` — tipo: texto; obrigatório: não; descrição: Comentário livre; não é conhecimento de validação.

#### Exemplos

##### Esboço na declaração

Na lista `hlm` da declaração:

```json
"hlm": [
  {
    "nome": "NomeDoHLM",
    "descricao": "O que o modelo representa.",
    "composicao": [
      {"sm": "SubmodeloA", "cardinalidade": "1..1"},
      {"sm": "SubmodeloB", "papel": "OutroPapel", "cardinalidade": "0..1"},
      {"sm": "SubmodeloColecao", "cardinalidade": "1..*"}
    ],
    "regras": [ /* RP, RIR, RIC que leem mais do que um SM */ ]
  }
]
```

#### Pode e não pode

- Compor um ou mais SM, cada um com a sua cardinalidade (`1..1`, `0..1`, `1..*`, `0..*`) — não pode: Declarar propriedades (`propriedades` é proibido)
- Compor o mesmo SM mais de uma vez, com papéis diferentes — não pode: Compor USM diretamente
- Ter regras que leem propriedades de mais de um SM (RP, RIR, RIC) — não pode: Ter regras que só leem dentro de um SM não repetível (deviam viver nesse SM, aviso I8)
- Ser alvo de projeções (só o HLM é projetado) — não pode: Ser composto por outro modelo
- Reutilizar SM de outros HLM (Cliente, Localizacao)

##### Como saber se um modelo é um HLM

Um modelo é um HLM quando responde "sim" a todas estas perguntas:

- É o que um sistema recebe, guarda ou envia como um todo, com identidade de negócio própria? — exemplo (sim): Fatura, Dispositivo, OrdemInstalacao; contraexemplo (não): Morada (é sempre parte de outra coisa)
- É a unidade sobre a qual faz sentido dizer "esta utilização precisa destas partes" (uma projeção)? — exemplo (sim): FaturaSimplificada e FaturaAT sobre Fatura; contraexemplo (não): Linha (não se projeta sozinha)
- Toda a sua informação cabe em grupos com finalidade (SM)? — exemplo (sim): Fatura = Cabecalho + Emitente + Cliente + Linhas
- Não existe só para reunir uma coleção? — contraexemplo (não): "Linhas" é um SM, não um HLM

Se alguma informação parecer pertencer ao HLM diretamente, como o número da fatura, pertence a um SM: aqui, ao SM Cabecalho, que só tem propriedades residuais.

#### Detalhes

##### Contextos de utilização

- **Ponto de entrada da validação.** Uma instância é sempre de um HLM. O perfil, através da projeção, diz qual.
- **Âncora das projeções.** Só o HLM tem a visão completa do modelo.
- **Sítio das regras que cruzam SM.** Por exemplo, a soma das linhas igual ao total da fatura (RP-SOMA), ou o tipo de dispositivo e a unidade da medição (RIR-TEMP-C).

#### Verificações

- **S-MOD:** nome em PascalCase; descrição com pelo menos 10 caracteres; pelo menos uma composição; sem `propriedades`.
- **S-COMP:** cada composição tem `sm`, nunca `usm`; a cardinalidade é uma das quatro; os papéis são únicos.
- **I2:** os SM compostos estão declarados.
- **I8 (aviso):** uma regra do HLM que só lê dentro de um SM não repetível poderia viver nesse SM.

### SM: Sub Model (submodelo)

#### Descrição

O SM é o nível intermédio da ECM. Agrupa informação canónica (USM) com uma finalidade determinada: é aqui que um conjunto de USM deixa de ser matéria-prima e passa a representar algo que o negócio reconhece, como o cliente, a leitura ou as linhas do documento. Um SM compõe USM e pode declarar propriedades residuais, as que só fazem sentido naquele agrupamento.

Um SM pode ser reutilizado por vários HLM quando a finalidade se repete noutro domínio. Por exemplo, `Cliente` é usado pela Fatura e pela OrdemInstalacao.

#### Atributos

- `nome` — tipo: texto, PascalCase; obrigatório: sim; descrição: Único entre os SM. Plural se reúne uma coleção.
- `descricao` — tipo: texto (≥ 10); obrigatório: sim; descrição: A finalidade do agrupamento.
- `composicao` — tipo: lista de `{usm, papel?, cardinalidade}`; obrigatório: sim, ou `propriedades`; descrição: Os USM que compõe.
- `propriedades` — tipo: lista de propriedades; obrigatório: sim, ou `composicao`; descrição: Propriedades residuais.
- `regras` — tipo: lista de regras; obrigatório: não; descrição: Regras que vivem no SM.
- `notas` — tipo: texto; obrigatório: não; descrição: Comentário livre.

#### Exemplos

##### Esboço na declaração

```json
"sm": [
  {
    "nome": "NomeDoSM",
    "descricao": "Finalidade do agrupamento.",
    "composicao": [
      {"usm": "UsmCanonico", "cardinalidade": "1..1"},
      {"usm": "OutroUsm", "papel": "PapelEspecifico", "cardinalidade": "0..1"}
    ],
    "propriedades": [ /* residuais */ ],
    "regras": [ /* regras que leem mais de um USM deste SM, ou a coleção */ ]
  }
]
```

#### Pode e não pode

- Compor USM, cada um com cardinalidade e, se preciso, papel — não pode: Compor outros SM ou HLM
- Compor o mesmo USM duas vezes, com papéis diferentes (`Origem`, `Destino`) — não pode: Repetir um papel
- Declarar propriedades residuais — não pode: Ter uma propriedade com o mesmo nome de um papel
- Ser composto por vários HLM (reutilização) — não pode: Ficar sem composição e sem propriedades
- Ter regras sobre a coleção (RP com funções sobre `Linha`)
- Ter regras que relacionam os seus USM (RIR-EMAIL-CX, RIR-LX-LOCALIDADE)

##### Como saber se um modelo é um SM (e não um USM ou um HLM)

- Junta informação canónica para uma finalidade (quem compra, onde está o equipamento)? — se sim: É um SM.; exemplo: `Cliente` = Entidade + Morada
- Existe para reunir uma coleção (as linhas, os locais)? — se sim: É um SM de coleção, com nome no plural.; exemplo: `Linhas` compõe `Linha [1..*]`
- Tem informação que só faz sentido neste agrupamento e em nenhum outro? — se sim: São propriedades residuais deste SM.; exemplo: `Cliente.consentimentoComercial`, `Localizacao.indicacaoAcesso`
- A informação significa o mesmo em qualquer domínio? — se sim: Então é um USM, não um SM.; exemplo: Morada
- É o que o domínio instancia como um todo? — se sim: Então é um HLM.; exemplo: Fatura

**Teste da propriedade residual (tese, Secção ECM).** Altere-se a finalidade do SM mantendo os mesmos USM. Se a propriedade desaparecesse, é residual. Se sobrevivesse, pertence a um USM e está no sítio errado. O consentimento para comunicações comerciais não é canónico, porque uma pessoa existe sem ele. Também não é do HLM, porque é de quem compra e não da fatura. É, por isso, residual do SM Cliente.

#### Detalhes

##### Três formas de SM

- **SM de composição** — quando: Junta USM com uma finalidade; exemplos: `Emitente` (Entidade, Morada, Contacto), `Cliente`, `Leitura`, `Localizacao`, `Diagnostico`
- **SM de coleção** — quando: Reúne `1..*` ou `0..*` instâncias de um USM; nome no plural; exemplos: `Linhas` (USM `Linha [1..*]`)
- **SM só com propriedades residuais** — quando: Informação própria do domínio, sem nenhum USM canónico; exemplos: `Cabecalho` (número, série, tipo, data, total), `Identificacao`, `Pedido`

##### Contextos de utilização

- **Dar finalidade à informação canónica.** O mesmo USM Morada é a morada fiscal no Emitente e a morada da instalação na Localizacao.
- **Coleções.** As regras sobre o conjunto (números únicos, consecutivos, número máximo) precisam de um nó onde viver. Esse nó é o SM da coleção, e não uma propriedade "linhas" (tese, Secção Coleções).
- **Reutilização entre HLM.** Um SM pensado para a faturação (Cliente) serve a ordem de instalação sem adaptação.

##### SM de metainformação

Um HLM principal pode compor um SM genérico de metainformação, `Metainformacao` (cardinalidade `0..1`, papel `Metainformacao`). Não descreve o domínio: descreve o próprio modelo (de onde vem, que versão da fonte, que entidade da fonte representa, para que é usado). É um SM só com propriedades residuais; as propriedades recomendadas estão em ecv/config/ecv.config.json (`metainformacao`):

- `origemModelo` — tipo: texto; significado: Fonte do modelo de dados (norma, sistema ou repositório), ex.: `CIUS-PT 2.1.1`, `Smart Data Models Device`
- `versaoOrigem` — tipo: texto; significado: Versão da fonte
- `referenciaOrigem` — tipo: texto; significado: Identificador da entidade na fonte (ex.: `BG-0 Invoice`, `Device`)
- `utilizacao` — tipo: texto; significado: Finalidade ou contexto de utilização
- `dominio` — tipo: texto; significado: Domínio a que o modelo pertence
- `observacoes` — tipo: texto; significado: Outra metainformação

Por ser igual em todos os HLM que o usam, a fusão guarda-o uma só vez; os valores (a origem concreta de cada HLM) são dados da instância ou valores fixados num perfil, não estrutura.

#### Verificações

- **S-MOD:** PascalCase; descrição ≥ 10; tem composição ou propriedades; não compõe SM.
- **S-COMP:** papéis únicos; cardinalidade válida.
- **S-PROP:** nomes de propriedades únicos e diferentes dos papéis.
- **I8 (aviso):** uma regra do SM que só lê dentro de um USM não repetível poderia viver nesse USM.

### USM: Universal Sub Model (submodelo universal)

#### Descrição

O USM é o nível de base da ECM: informação canónica, pura, independente do domínio e do uso que dela se faça. Uma morada é uma morada, quer sirva para faturar, quer sirva para localizar um sensor. O USM é o dono da identidade das propriedades que contém: cada propriedade tem uma única definição, no USM, e é reutilizada em todos os caminhos que o compõem. As regras que vivem no USM e nas suas propriedades acompanham-no para todo o lado.

#### Atributos

- `nome` — tipo: texto, PascalCase; obrigatório: sim; descrição: Único entre os USM.
- `descricao` — tipo: texto (≥ 10); obrigatório: sim; descrição: O que a informação é, independentemente do uso.
- `propriedades` — tipo: lista (≥ 1); obrigatório: sim; descrição: Ver Propriedade.md.
- `regras` — tipo: lista; obrigatório: não; descrição: Regras que vivem no USM.
- `notas` — tipo: texto; obrigatório: não; descrição: Comentário livre.

#### Exemplos

##### Esboço na declaração

```json
"usm": [
  {
    "nome": "NomeDoUSM",
    "descricao": "O que a informação é.",
    "propriedades": [
      {"nome": "umaPropriedade", "tipo": "texto", "descricao": "…", "nomesAlternativos": ["…"], "regras": [ /* RP */ ]}
    ],
    "regras": [ /* RIR, RIC ou RP com função que leem várias propriedades do USM */ ]
  }
]
```

#### Pode e não pode

- Ter propriedades (pelo menos uma) — não pode: Compor outros modelos
- Ter regras que leem várias das suas propriedades (RIR-CP-PT, RIC-MANUT, RP-AREA) — não pode: Ter regras que leem fora de si (iriam para o SM ou o HLM)
- Ser composto por vários SM, por caminhos diferentes — não pode: Repetir nomes de propriedades
- Ser composto com cardinalidade repetível (elemento de uma coleção: Linha)

##### Como saber se um modelo é um USM

- Significa o mesmo em qualquer domínio (faturação, monitorização, redes)? — se sim: É candidato a USM.
- Pode ser composto por SM de domínios diferentes sem adaptação? — se sim: É um USM.
- Contém alguma propriedade que só faz sentido para uma finalidade? — se sim: Essa propriedade não é deste USM: é residual de um SM.
- Precisa de outra informação para não ser ambíguo? — se sim: Essa informação faz parte do USM. O sistema de referência pertence a `InformacaoGeografica`, porque uma coordenada sem ele é ambígua.

São USM típicos uma pessoa ou entidade, uma morada, uma coordenada geográfica, um intervalo temporal ou um montante com moeda. Também o são a medição de um sensor, uma assinatura digital ou uma linha de documento.

#### Detalhes

##### Contextos de utilização

- **Definir uma vez, usar em todo o lado.** `Morada` aparece em cinco caminhos e três HLM. As regras do código postal valem em todos (tese, Secção ECM e operação "reutilização").
- **Validação dentro da informação canónica.** O formato do código postal por país (RIR-CP-PT/ES/GB) só lê a morada, logo vive na morada.
- **Elemento de coleção.** `Linha` é composto `1..*` por `Linhas`; as regras de cada linha (IVA) vivem na `Linha`.

#### Verificações

- **S-MOD:** PascalCase; descrição ≥ 10; pelo menos uma propriedade; sem composição.
- **I3:** os caminhos das regras resolvem a partir do USM.
- **I8 (aviso):** uma regra do USM que só lê uma propriedade poderia viver nessa propriedade.

### Propriedade

#### Descrição

A propriedade é a informação atómica de um modelo. Tem uma única definição, no modelo que a contém, e é reutilizada em todas as ocorrências desse modelo. Além do nome, tem informação complementar que não altera o que a propriedade representa, mas condiciona a forma como é reconhecida e interpretada (tese, Secção ECM):

- **Tipo base:** a natureza do valor (texto, inteiro, decimal, data, booleano). Determina o que pode ser guardado e que verificações fazem sentido.
- **Nomes alternativos:** as formas sob as quais a mesma propriedade aparece nas fontes (`zipCode`, `postalCode`, `CP` para `codigoPostal`). Permitem reconhecer a propriedade na ingestão sem um mapeamento por fonte.
- **Descrição:** o significado e as particularidades da interpretação. Tem de ser precisa: uma descrição vaga (por exemplo, só "Valor") aparece como tal nas vistas.

#### Atributos

- `nome` — tipo: texto, camelCase; obrigatório: sim; descrição: Único no modelo.
- `tipo` — tipo: `texto` · `inteiro` · `decimal` · `data` · `booleano`; obrigatório: sim; descrição: Tipo base. Limita os operadores possíveis (Catalogo.md).
- `descricao` — tipo: texto (≥ 5); obrigatório: sim; descrição: Significado e particularidades.
- `nomesAlternativos` — tipo: lista de texto; obrigatório: não; descrição: Nomes nas fontes.
- `regras` — tipo: lista; obrigatório: não; descrição: RP (ou RIC) que vivem na propriedade.
- `notas` — tipo: texto; obrigatório: não; descrição: Comentário livre.

Tipos base e o que admitem:

- `texto` — valores: cadeia de caracteres; exemplo: `"PT"`, `"1000-001"`
- `inteiro` — valores: número inteiro; exemplo: `3`
- `decimal` — valores: número; exemplo: `-12.5`
- `data` — valores: `AAAA-MM-DD` (ou data e hora ISO 8601); exemplo: `"2026-09-01"`, `"2026-09-30T12:00:00Z"`
- `booleano` — valores: `true` / `false`; exemplo: `true`

Um enumerado não é um tipo próprio: é uma propriedade `texto` cujo Conjunto de Regras de Plausibilidade é uma lista fechada (uma RP com `IN`). Ver RP.md.

#### Exemplos

##### Esboço na declaração

Na lista `propriedades` de um USM (ou de um SM, para as residuais):

```json
{
  "nome": "codigoPostal",
  "tipo": "texto",
  "descricao": "Código postal da morada",
  "nomesAlternativos": ["zipCode", "postalCode", "CP"],
  "regras": [ { "id": "RP-…", "natureza": "plausibilidade", "descricao": "…", "restricao": { … } } ]
}
```

#### Pode e não pode

- Ter regras de plausibilidade (RP) que só leem a própria propriedade — não pode: Ter uma RIR (a condição não pode ler o alvo da restrição, I6)
- Ter uma RP cuja restrição é uma função com a propriedade como único alvo (RP-NIF-DC, RP-RELOGIO) — não pode: Ter regras que leem outras propriedades (I3: vão para o modelo)
- Ter uma RIC cuja condição só lê a propriedade (RIC-MED-DIFERIDA) — não pode: Ter um tipo fora dos cinco tipos base
- Ser alvo de restrições, termos e argumentos de funções de regras que vivem acima — não pode: Ter o mesmo nome que outra propriedade ou papel do mesmo modelo
- Ter vários nomes alternativos

#### Detalhes

##### Onde pode viver

- Num USM — quando: Quase sempre: informação canónica; exemplo: `Morada.codigoPostal`, `Medicao.valor`
- Num SM (residual) — quando: Só faz sentido naquele agrupamento; exemplo: `Cliente.consentimentoComercial`, `Cabecalho.totalFatura`
- Num HLM — quando: Nunca

##### Contextos de utilização

- **Identidade partilhada.** Há uma só definição de `codigoPostal`, com as suas regras, em todas as moradas.
- **Reconhecimento na ingestão.** `reading` é reconhecido como `valor` pelos nomes alternativos.
- **Fator discriminante.** `tipoDispositivo`, `unidadeMedida` e `ambiente` decidem que gama se aplica a `valor`.

#### Verificações

- **S-PROP:** camelCase; tipo válido; descrição ≥ 5; `nomesAlternativos` é uma lista; sem repetidos.
- **I3:** uma regra declarada na propriedade só lê essa propriedade.
- **I5:** os operadores das regras que a usam são admissíveis para o tipo.

### Composição (com papel e cardinalidade)

#### Descrição

A composição liga um modelo ao modelo que ele compõe: um HLM compõe SM, um SM compõe USM. A cardinalidade é declarada na composição, e não no modelo composto. Indica quantas instâncias a composição admite, no formato mínimo..máximo. O papel é o nome com que o modelo composto é alcançado, ou seja, o segmento do caminho. Por omissão, o papel é o nome do modelo composto.

"O papel é atribuído pela composição, e não pela definição" (tese, Secção ECM). O mesmo USM Morada é a morada do emitente, a do cliente ou a da instalação, consoante o SM que o compõe.

#### Atributos

- `sm` ou `usm` — tipo: nome do modelo; obrigatório: um dos dois; descrição: `sm` num HLM, `usm` num SM.
- `papel` — tipo: texto, PascalCase; obrigatório: não; descrição: Segmento do caminho; por omissão, o nome do modelo.
- `cardinalidade` — tipo: `0..1` · `1..1` · `0..*` · `1..*`; obrigatório: sim; descrição: Quantas instâncias.

#### Pode e não pode

- HLM → SM; SM → USM — não pode: HLM → USM; SM → SM; USM → qualquer modelo
- Ter papel diferente do nome do modelo — não pode: Repetir um papel no mesmo nó
- Cardinalidade `0..1`, `1..1`, `0..*`, `1..*` — não pode: Outras cardinalidades (por exemplo `2..5`); usam-se funções (`contagemInferiorA`)
- Formar caminhos pelos quais o mesmo modelo é alcançado várias vezes — não pode: Formar ciclos (I1)

#### Detalhes

##### Cardinalidades

- `1..1` — leitura: singular e obrigatória; exemplo: Fatura → Cabecalho
- `0..1` — leitura: singular e opcional; exemplo: Dispositivo → Diagnostico; Leitura → Assinatura
- `1..*` — leitura: repetível, pelo menos uma (coleção); exemplo: Linhas → Linha; OrdemInstalacao → Localizacao
- `0..*` — leitura: repetível, pode ser vazia; exemplo: (não usada nos exemplos)

##### Coleções

Uma coleção é uma composição com máximo `*`. As consequências são as seguintes (tese, Secção Coleções):

- **Nomenclatura.** Quando um SM existe para reunir uma coleção, o seu nome está no plural (`Linhas`) e o elemento no singular (`Linha`). Um HLM nunca existe só para reunir uma coleção: compõe o SM repetido com o seu nome, e a cardinalidade indica a repetição (`OrdemInstalacao → Localizacao [1..*]`).
- **Porque não uma propriedade "linhas".** Primeiro, o HLM não tem propriedades. Segundo, as regras sobre o conjunto precisam de um nó onde viver (o SM `Linhas`). Terceiro, o SM com as suas regras é reutilizável. Quarto, a consulta distingue diretamente as regras de cada linha, do conjunto e da relação com o documento.
- **Caminhos através de uma coleção.** `Linhas.Linha.valor` (a partir do HLM Fatura) é a lista dos valores de todas as linhas. `Linhas.Linha` é a coleção de instâncias. Só funções podem ler coleções (`somaIgualA`, `contagemInferiorA`): uma restrição tipificada tem um único alvo, que não pode ser uma coleção.

##### Papéis

O papel distingue duas ocorrências do mesmo modelo no mesmo nó e dá nome à ocorrência:

```json
"composicao": [
  {"usm": "UsmB", "papel": "Origem",  "cardinalidade": "1..1"},
  {"usm": "UsmB", "papel": "Destino", "cardinalidade": "0..1"}
]
```

Os caminhos passam a ser `Origem.estado` e `Destino.estado` (ver o esqueleto). Nas declarações de exemplo, a OrdemInstalacao compõe o SM `Cliente` com o papel `Requerente`: `Requerente.Entidade.nif`.

#### Verificações

- **S-COMP:** exatamente um de `sm` ou `usm`, coerente com o nível; cardinalidade válida; papel em PascalCase e único.
- **I1:** composição acíclica.
- **I2:** o modelo composto está declarado.
- **Funções com parâmetros de coleção:** um parâmetro `colecao: true` só recebe um caminho que atravessa uma composição repetível, e um parâmetro simples nunca recebe uma coleção.

## Regras (ECR)

### Regra (o que é comum a RP, RIR e RIC)

#### Descrição

Uma regra é conhecimento de validação declarado fora do modelo que valida e fora do mecanismo que a avalia (eixo E2). A ECR caracteriza cada regra em três dimensões paralelas:

- **Natureza** — pergunta: Que conhecimento expressa esta validade?; na declaração: `natureza` (e o prefixo do `id`)
- **Alcance** — pergunta: Onde vive a regra?; na declaração: o sítio onde a regra é declarada (o nó ou a propriedade)
- **Expressividade** — pergunta: Como é escrita, para ser lida por pessoas e avaliada pelo motor?; na declaração: `restricao` e `condicao` (verificações tipificadas e funções), `descricao` e mensagens

#### Atributos

- `id` — tipo: texto `TIPO-ASSUNTO[-QUALIFICADOR]`; obrigatório: sim; descrição: Único na declaração. O prefixo (RP, RIR, RIC) é coerente com a natureza.
- `natureza` — tipo: `plausibilidade` · `inferencia_restritiva` · `inferencia_conclusiva`; obrigatório: sim; descrição: O tipo de conhecimento.
- `descricao` — tipo: texto; obrigatório: sim; descrição: Derivada da condição, da restrição (ou conclusão) e do nó; ver abaixo.
- `restricao` — tipo: Restrição; obrigatório: RP, RIR; descrição: Ver Restricao.md.
- `condicao` — tipo: lista de termos; obrigatório: RIR, RIC; descrição: Ver CondicaoAplicabilidade.md.
- `mensagem` — tipo: texto (≥ 10); obrigatório: só RIC; descrição: A mensagem de conclusão. Numa RP ou RIR, a mensagem está na restrição.
- `conclusao` — tipo: `{tipo: ACAO; obrigatório: ESTADO, valor}`; descrição: só RIC (recomendado)
- `contextosExternos` — tipo: lista de nomes; obrigatório: não (derivado); descrição: Contextos de que a regra depende; se presente, tem de coincidir com os usados (I11).
- `notas` — tipo: texto; obrigatório: não; descrição: Comentário livre.

#### Detalhes

##### Os quatro tipos de conhecimento

- **RE** — nome: regra estrutural; resultado da avaliação: presença, tipo e cardinalidade, expressos pela projeção (RE_Projecao.md)
- **RP** — nome: regra de plausibilidade; restrição: sim (uma); condição de aplicabilidade: **nunca**; mensagem: de não conformidade, na restrição; resultado da avaliação: cumprida / não cumprida
- **RIR** — nome: regra de inferência restritiva; restrição: sim (uma); condição de aplicabilidade: sim (uma, com 1..N termos); mensagem: de não conformidade, na restrição; resultado da avaliação: não aplicável / cumprida / não cumprida
- **RIC** — nome: regra de inferência conclusiva; restrição: **não**; condição de aplicabilidade: sim (uma, com 1..N termos); mensagem: de conclusão, na própria regra; resultado da avaliação: não aplicável / conclusão

A RP e a RIR partilham a restrição: o que as distingue é a condição, que só a RIR tem. A RIR e a RIC partilham a condição: o que as distingue é a restrição, que só a RIR tem. As naturezas são níveis progressivos de conhecimento: **Estrutural → Plausibilidade → Inferência**.

Correspondência com a literatura (tese, Natureza): RE e RP correspondem às asserções estruturais e às regras definicionais; a RIR às asserções de ação e às regras operativas, que podem ser violadas; a RIC às derivações, que produzem conhecimento novo (Business Rules Group; SBVR).

##### Alcance: onde vive a regra

**Princípio de posicionamento:** uma regra vive no nível mais baixo da estrutura que contenha toda a informação de que precisa para ser avaliada, tanto na condição como na restrição.

- Só uma propriedade — vive em: na propriedade; exemplo: RP-LAT (`latitude`), RIC-MED-DIFERIDA (`dataMedicao`)
- Várias propriedades do mesmo USM — vive em: no USM; exemplo: RIR-CP-PT (`Morada`), RIC-MANUT (`Diagnostico`), RP-AREA (`InformacaoGeografica`)
- Propriedades de vários USM do mesmo SM, ou residuais do SM — vive em: no SM; exemplo: RIR-EMAIL-CX (`Emitente`), RIR-FS (`Cabecalho`)
- Todas as instâncias de uma coleção — vive em: no SM da coleção; exemplo: RP-LIN-NUM (`Linhas`)
- Propriedades de vários SM — vive em: no HLM; exemplo: RP-SOMA, RIR-TEMP-REFRIG-CELSIUS

A regra declara o seu alcance pelo sítio onde é escrita na declaração (aninhada no nó ou na propriedade). No grafo, a aresta `ASSOCIADA_A` aponta para esse nó. Os caminhos da regra são relativos a esse nó. Numa regra declarada numa propriedade, são relativos ao modelo que contém a propriedade.

Uma regra que vive num USM reutilizado vale em todas as ocorrências: as RIR do código postal valem para a morada do emitente, do cliente e da instalação.

##### Nomenclatura dos identificadores

A forma é `tipo-assunto-qualificador`, em maiúsculas, com hífens:

- tipo — exemplos: `RP`, `RIR`, `RIC`
- assunto — exemplos: `TEMP` (temperatura), `CP` (código postal), `IVA`, `FS` (fatura simplificada), `LIN` (linhas), `MANUT` (manutenção)
- qualificador — exemplos: `REFRIG-CELSIUS`, `PT`, `ISE`, `NUM`, `LX-AJUDA`

Por exemplo, `RIR-TEMP-REFRIG-CELSIUS` é a RIR da temperatura em refrigeração em °C, e `RIR-FS-NUM` é a RIR das faturas simplificadas sobre o número. A tese usava `RI-` antes de separar RIR de RIC; essa forma já não existe.

##### Descrição derivada e mensagens

A descrição não acrescenta conhecimento: resulta de três partes que a regra já contém.

1. **"Se …":** os termos da condição ligados por "e". Não existe numa RP.
2. **Prefixo do modelo:** cada caminho é prefixado pelo nome do nó onde a regra vive (exceto no HLM).
3. **"→ …":** a restrição. Numa RIC é substituída por "informa Ação|Estado VALOR".

Exemplos:

- `Se Identificacao.tipoDispositivo = TEMPERATURA e Leitura.Medicao.unidadeMedida = °C e Leitura.Instalacao.ambiente = REFRIGERACAO → Leitura.Medicao.valor entre -30 e 0`
- `Se Diagnostico.nivelBateria entre 0 e 10 e excedeDiasDesdeHoje(Diagnostico.dataUltimaManutencao, 7) → informa Ação MANUTENCAO`

`python -m ecv descricoes <ficheiro> --escrever` recalcula-as. O invariante I12 avisa quando uma descrição não coincide com a derivada.

A regra lê-se completamente em linguagem natural pela descrição e pela mensagem, juntas. A descrição diz o que é exigido e quando. A mensagem diz o que é comunicado:

- numa RP ou numa RIR, a mensagem de não conformidade, atributo da restrição;
- numa RIC, a mensagem de conclusão, atributo da regra.

#### Verificações

**S-REGRA**, **I3**, **I4**, **I5**, **I6**, **I7**, **I8**, **I11** e **I12**; ver Verificacao.md.

### RP: Regra de Plausibilidade

#### Descrição

A plausibilidade representa o espaço de possibilidades admissíveis de uma propriedade: o que pode constituir um código postal, que unidades podem representar uma medição, que formas válidas tem um email. As RP de uma propriedade formam o seu **Conjunto de Regras de Plausibilidade**. Funcionam como tipos refinados: a ECM diz que a propriedade existe e qual é o tipo base; as RP dizem o que ela pode representar.

Uma RP tem **sempre uma restrição** e **nunca tem condição de aplicabilidade**: aplica-se sempre, em qualquer utilização.

#### Atributos

Os atributos comuns a todas as regras (`id`, `natureza`, `descricao`, `contextosExternos`, `notas`) estão em Regra.md; aqui ficam os próprios deste tipo.

Os atributos comuns estão em Regra.md. Na RP: `natureza: "plausibilidade"`, `restricao` obrigatória, sem `condicao` (ou `[]`).

#### Exemplos

##### Esboço na declaração

Na propriedade (forma mais comum):

```json
{
  "nome": "latitude", "tipo": "decimal", "descricao": "…",
  "regras": [
    {
      "id": "RP-LAT",
      "natureza": "plausibilidade",
      "descricao": "InformacaoGeografica.latitude entre -90 e 90",
      "restricao": {"propriedade": "latitude", "operador": "RANGE", "valor": [-90, 90],
                    "mensagem": "A latitude tem de estar entre -90 e 90."}
    }
  ]
}
```

No modelo, quando a restrição é uma função que lê várias propriedades ou uma coleção:

```json
"regras": [
  {
    "id": "RP-SOMA", "natureza": "plausibilidade", "descricao": "somaIgualA(Linhas.Linha.valor, Cabecalho.totalFatura)",
    "restricao": {"operador": "FUNCTION",
                  "chamada": {"funcao": "somaIgualA", "argumentos": [{"caminho": "Linhas.Linha.valor"}, {"caminho": "Cabecalho.totalFatura"}]},
                  "mensagem": "O total da fatura não corresponde à soma dos valores das linhas."}
  }
]
```

#### Pode e não pode

- Ter exatamente uma restrição — não pode: Ter condição de aplicabilidade (I4)
- Ser tipificada (um alvo) ou ser uma função (alvos = argumentos) — não pode: Ter `mensagem` ao nível da regra (a mensagem é da restrição)
- Viver numa propriedade ou num modelo, conforme o que lê — não pode: Ter `conclusao`
- Depender de contextos externos, através de uma função EXT_FUNCTION

##### Como saber se é uma RP (e não uma RIR)

- A validade decide-se só pelo valor e pelo conjunto de possibilidades da propriedade? — se sim: RP
- Depende de outra propriedade, do momento da avaliação ou do cenário? — se sim: RIR (ou RIC)
- Uma gama isolada (por exemplo `[0, 100]`) significaria algo diferente consoante a unidade ou o tipo? — se sim: Não é plausibilidade: é uma inferência (RIR). Na RP fica só o conjunto das gamas fisicamente possíveis.
- O formato depende do país? — se sim: A RP admite todos os formatos possíveis (PT, ES, GB); a escolha do formato é uma RIR (RIR-CP-PT).
- É uma verificação sobre toda uma coleção, sempre executada (números únicos)? — se sim: RP, cuja restrição é uma função, e que vive no SM da coleção

#### Detalhes

##### Formas de uma RP

- **Tipificada na propriedade** — vive em: a propriedade; restrição: `{propriedade, operador, valor, mensagem}`; exemplos: RP-LAT, RP-PAIS, RP-CP, RP-NIF
- **Função com um alvo** — vive em: a propriedade; restrição: `{operador: FUNCTION/EXT_FUNCTION, chamada, mensagem}`; exemplos: RP-NIF-DC, RP-RELOGIO, RP-MANUT-FUTURA
- **Função com vários alvos** — vive em: o nó mais baixo que contém os alvos; restrição: idem; exemplos: RP-AREA (USM), RP-HASH (SM Cabecalho), RP-ASSINATURA (USM)
- **Sobre uma coleção** — vive em: o SM da coleção; restrição: função cujos argumentos atravessam a composição repetível; exemplos: RP-LIN-NUM, RP-LIN-SEQ, RP-LIN-MAX
- **Coleção e documento** — vive em: o HLM; restrição: função; exemplos: RP-SOMA, RP-ORDEM-MAX

Uma propriedade de texto cujo Conjunto de Regras de Plausibilidade é uma lista fechada (uma RP com `IN`) é, na prática, um **enumerado**, sem ser preciso um tipo de dados próprio. Os valores dessa lista são os **valores plausíveis** e os candidatos a **fatores discriminantes** nas condições das RIR (invariante I7).

#### Verificações

- **I4:** tem restrição e não tem condição.
- **I5:** o operador é admissível para o tipo do alvo; a forma do valor é a do operador.
- **I3:** numa propriedade, só lê essa propriedade.
- **S-RESTR:** a mensagem tem pelo menos 10 caracteres.

### RIR: Regra de Inferência Restritiva

#### Descrição

As regras de inferência fazem inferências sobre o domínio: a partir dos valores de outras propriedades, do momento da avaliação ou de informação externa, inferem como o domínio se comporta. Uma RIR usa uma **condição de aplicabilidade** para decidir se a sua **restrição** é avaliada. A condição decide se a regra se aplica; a restrição decide se o dado é válido. Se a condição não é satisfeita, o resultado é "não aplicável", e não "inválido".

Exemplo da tese: num ambiente de refrigeração, uma temperatura em °C tem de estar entre -30 e 0 (RIR-TEMP-REFRIG-CELSIUS).

#### Atributos

Os atributos comuns a todas as regras (`id`, `natureza`, `descricao`, `contextosExternos`, `notas`) estão em Regra.md; aqui ficam os próprios deste tipo.

- `id` — papel: texto · chave · RIR-ASSUNTO-QUALIFICADOR
- `natureza` — papel: = inferencia_restritiva
- `descricao` — papel: texto derivado · Se … → …
- `condicao` — papel: lista de termos · **ligação** · obrigatória
- `restricao` — papel: Restricao · **ligação** · obrigatória
- `contextosExternos` — papel: lista · derivada · **ligação**
- `notas` — papel: texto

#### Exemplos

##### Esboço na declaração

```json
{
  "id": "RIR-TEMP-REFRIG-CELSIUS",
  "natureza": "inferencia_restritiva",
  "descricao": "Se … → Leitura.Medicao.valor entre -30 e 0",
  "condicao": [
    {"propriedade": "Identificacao.tipoDispositivo", "operador": "EQUALS", "valor": "TEMPERATURA"},
    {"propriedade": "Leitura.Medicao.unidadeMedida", "operador": "EQUALS", "valor": "°C"},
    {"propriedade": "Leitura.Instalacao.ambiente", "operador": "EQUALS", "valor": "REFRIGERACAO"}
  ],
  "restricao": {"propriedade": "Leitura.Medicao.valor", "operador": "RANGE", "valor": [-30, 0],
                "mensagem": "Temperatura fora da gama de refrigeração (-30 a 0 °C)."}
}
```

Declara-se no `regras` do nó mais baixo que contém tudo o que lê (aqui, o HLM Dispositivo).

#### Pode e não pode

- Ter uma condição (1..N termos, com E) e uma restrição — não pode: Não ter condição (seria uma RP) ou não ter restrição (seria uma RIC)
- Ter termos tipificados, termos com contexto externo e termos com função — não pode: Ler o alvo da restrição na condição
- Restringir uma propriedade ou chamar uma função — não pode: Ter `mensagem` ou `conclusao` ao nível da regra
- Viver no nó mais baixo que contém tudo o que lê — não pode: Viver numa propriedade (leria pelo menos duas: termo e alvo)

##### Como saber se é uma RIR

- A exigência só se aplica quando outras propriedades têm certos valores? — se sim: RIR
- Quando a condição se verifica, há um valor que pode falhar (uma restrição)? — se sim: RIR (se não houver nada a falhar, mas só algo a comunicar, é uma RIC)
- A exigência vale sempre, seja qual for o contexto? — se sim: RP

#### Detalhes

##### Partes (tese, Tabela "Partes de uma regra de inferência")

- Condição de aplicabilidade — descrição: Um ou mais termos, combinados com E; rir-temp-c: tipoDispositivo = TEMPERATURA E unidadeMedida = °C
- Restrição — descrição: O que o dado deve satisfazer quando a condição é satisfeita; rir-temp-c: valor ∈ [-60, 1300]
- Falha — descrição: A mensagem de não conformidade da restrição; rir-temp-c: "Uma temperatura em °C tem de estar entre -60 e 1300."

##### Regras de construção

- **Uma condição por regra, uma restrição por regra.** A mesma restrição com duas condições dá duas regras (RIR-HUM e RIR-VEL-MS, ambas [0, 100]). A mesma condição com duas restrições também dá duas regras (RIR-FS e RIR-FS-NUM, ambas para `tipoDocumento = FS`).
- **Sem OU entre propriedades.** Entre termos, o único operador é o E. As razões são três: a legibilidade (não há precedência), a navegação (cada regra é um caminho na árvore de decisão) e o significado (duas condições ligadas por OU são, em regra, conhecimento diferente). A disjunção dentro da mesma propriedade continua possível com `IN`.
- **A condição nunca lê o alvo da restrição (I6).** "Se valor > 100 então valor ≤ 200" exprime-se como `valor ≤ 200`.
- **Os valores da condição são valores plausíveis (I7).** Uma regra com `ambiente = CAMARA_FRIGORIFICA` nunca se aplica (anomalia intencional RIR-TEMP-CAMARA-CELSIUS).
- **Coerência entre regras.** A responsabilidade é de quem as define: duas RIR podem aplicar-se à mesma leitura e ter gamas sem valor comum (RIR-PRES-BAR e RIR-PRES-EXTERIOR-BAR). As vistas `decisao`, `arvore` e `coerencia` tornam isto visível.
- **Mapeamentos conhecidos são RIR.** Uma tabela de referência (gamas por tipo, unidade e ambiente; códigos postais por freguesia) declara-se como uma RIR por linha. A matriz de decisão reconstrói a tabela a partir das regras.

##### Formas

- Condição tipificada, restrição tipificada — exemplos: RIR-TEMP-REFRIG-CELSIUS, RIR-CP-PT, RIR-IVA-RED, RIR-FS, RIR-EMAIL-CX
- Condição com GT/RANGE — exemplos: RIR-FT-NIF (`totalFatura > 1000`)
- Condição com IN (disjunção numa propriedade) — exemplos: (esqueleto: RIR-A-CODIGO-Y)
- Condição tipificada, restrição por função — exemplos: RIR-FS-LIN (`contagemInferiorA(Linhas.Linha, 11)`)
- Condição com função — exemplos: RIR-LX-LOCALIDADE (`dentroDe(…, limites de Lisboa)`)
- Condição com função e contexto externo — exemplos: (esqueleto: RIR-B-FECHO, `excedeDias(dataEvento, 30)`)

#### Verificações

**I4**, **I5**, **I6**, **I7** (aviso), **I8** (aviso), **I10** (aviso, por perfil) e **S-RESTR / S-TERMO**.

### RIC: Regra de Inferência Conclusiva

#### Descrição

Uma RIC é uma regra de inferência cuja condição de aplicabilidade não identifica uma restrição a avaliar. Quando a condição é satisfeita, a própria regra comunica uma **conclusão** sobre o domínio: um estado derivado ou uma ação. Não valida um valor: conclui. "RIC-MANUT não diz se a leitura é válida; acrescenta conhecimento sobre o dispositivo e propõe uma ação" (tese).

O estado derivado não é mais uma entidade do sistema. É informação sobre a avaliação. Se o modelo tem uma propriedade que o recebe, ou se outro sistema age consoante esse estado, isso é responsabilidade de quem implementa, e não da ECR.

#### Atributos

Os atributos comuns a todas as regras (`id`, `natureza`, `descricao`, `contextosExternos`, `notas`) estão em Regra.md; aqui ficam os próprios deste tipo.

- `mensagem` — obrigatório: sim; descrição: A mensagem de conclusão: transporta o estado ou a ação e o motivo. Pertence à regra (numa RP ou RIR, a mensagem pertence à restrição).
- `conclusao` — obrigatório: recomendado; descrição: `{"tipo": "ACAO"

#### Exemplos

##### Esboço na declaração

```json
{
  "id": "RIC-MANUT",
  "natureza": "inferencia_conclusiva",
  "descricao": "Se Diagnostico.nivelBateria entre 0 e 10 e excedeDiasDesdeHoje(Diagnostico.dataUltimaManutencao, 7) → informa Ação MANUTENCAO",
  "condicao": [
    {"propriedade": "nivelBateria", "operador": "RANGE", "valor": [0, 10]},
    {"operador": "EXT_FUNCTION", "chamada": {"funcao": "excedeDiasDesdeHoje",
      "argumentos": [{"caminho": "dataUltimaManutencao"}, {"literal": 7}]}}
  ],
  "mensagem": "Ação MANUTENCAO: o nível de bateria está baixo e o dispositivo não recebe manutenção há mais de 7 dias.",
  "conclusao": {"tipo": "ACAO", "valor": "MANUTENCAO"},
  "contextosExternos": ["dataDeHoje"]
}
```

#### Pode e não pode

- Ter condição (1..N termos) e mensagem de conclusão — não pode: Ter restrição (I4)
- Ter `conclusao: {tipo: ACAO — não pode: ESTADO, valor}`
- Usar termos com função e contexto externo (RIC-MANUT)
- Usar um termo que compara uma propriedade com um contexto externo (RIC-MED-DIFERIDA)
- Viver numa propriedade, quando a condição só lê essa propriedade

##### Como saber se é uma RIC

- Quando a condição se verifica, há algo a comunicar, e não um valor a verificar? — se sim: RIC
- O resultado é um estado (NAO_FIAVEL, DIFERIDA) ou uma ação (MANUTENCAO)? — se sim: RIC
- O resultado é "o valor X tem de estar em Y"? — se sim: RIR

#### Verificações

**I4** (condição, mensagem, sem restrição), **S-REGRA** (`conclusao` só em RIC), **I5**, **I7**, **I11**.

### Restrição

#### Descrição

A restrição é o que o dado tem de cumprir. Usam-na a **RP** e a **RIR**. Tem quatro elementos (tese, Figura "Tipos de regra e elementos que cada um usa"):

1. **alvo:** exatamente uma propriedade, a que é validada;
2. **operador:** um tipo de verificação do catálogo;
3. **valores esperados:** com a forma que o operador exige;
4. **mensagem de não conformidade:** comunicada quando a verificação falha.

O operador e os valores formam uma **verificação tipificada**. Quando nenhuma verificação do catálogo exprime o que se quer verificar (uma soma, a unicidade numa coleção, uma geometria, um hash), a restrição é uma **função**. A função ocupa o lugar da verificação e tem o mesmo papel: verificar e, se falhar, dar lugar à mensagem. Os alvos passam a ser os argumentos da função, lidos a partir do nó onde a regra vive.

#### Atributos

- `propriedade` — papel: caminho do alvo · **ligação** · forma tipificada
- `operador` — papel: operador do catálogo
- `valor` — papel: valores esperados · forma tipificada
- `chamada` — papel: funcao e argumentos · **ligação** · forma função
- `mensagem` — papel: texto · mensagem de não conformidade

#### Exemplos

##### Esboço na declaração

No atributo `restricao` da regra (RP ou RIR):

```json
"restricao": {"propriedade": "codigoPostal", "operador": "PATTERN", "valor": "^[1-9][0-9]{3}-[0-9]{3}$",
              "mensagem": "O código postal português tem de ter o formato 0000-000, sem começar por zero."}
```

```json
"restricao": {"operador": "EXT_FUNCTION",
              "chamada": {"funcao": "hashEncadeadoValido",
                          "argumentos": [{"caminho": "numero"}, {"caminho": "dataEmissao"}, {"caminho": "totalFatura"}, {"caminho": "hash"}]},
              "mensagem": "O hash do documento não corresponde ao encadeamento com o documento anterior."}
```

Nota sobre a tese: nos JSON da tese, a mensagem estava na regra e a chamada era um texto (`"valor": "somaIgualA(…)"`). Na declaração final, a mensagem está na restrição, como no grafo do Capítulo 4, e a chamada está estruturada (`chamada.funcao`, `chamada.argumentos`). Assim, os alvos ficam explícitos e podem ser verificados. O texto da chamada continua a aparecer na descrição.

#### Pode e não pode

- Ter um alvo (tipificada) ou ser uma chamada (função) — não pode: Ter dois alvos numa verificação tipificada
- Ter um alvo a qualquer profundidade do nó da regra (`Cliente.Entidade.nif`) — não pode: Ter como alvo um modelo (só funções leem coleções e instâncias)
- Passar literais declarados na regra a uma função (a área autorizada, `7` dias) — não pode: Ter um alvo lido pela condição da mesma regra (I6)
- Depender de contextos externos, através de uma função EXT_FUNCTION — não pode: Existir sem mensagem

#### Detalhes

##### Duas formas

- **Tipificada** — declaração: `{"propriedade", "operador", "valor", "mensagem"}`; alvos: exatamente 1 (`propriedade`); exemplo: `valor RANGE [-30, 0]`
- **Função** — declaração: `{"operador": "FUNCTION" ou "EXT_FUNCTION", "chamada": {"funcao", "argumentos"}, "mensagem"}`; alvos: os argumentos `{caminho}` (0..N); os `{literal}` são parâmetros; exemplo: `somaIgualA(Linhas.Linha.valor, Cabecalho.totalFatura)`

Uma regra que precise de verificar duas propriedades declara duas restrições, uma em cada regra. A exceção é uma função que as relacione (RP-SOMA, RP-AREA).

##### Operadores e valores

O catálogo completo está em Catalogo.md. Em resumo:

- igualdade e pertença — operadores: `EQUALS`, `NOT_EQUALS`, `IN`; valor esperado: um valor; uma lista
- intervalo e comparação — operadores: `RANGE`, `LT`, `LTE`, `GT`, `GTE`; valor esperado: `[mín, máx]`; um número (ou uma data)
- padrão — operadores: `PATTERN`; valor esperado: expressão regular
- texto — operadores: `CONTAINS`, `STARTS_WITH`, `ENDS_WITH`, `LENGTH`; valor esperado: texto; inteiro ou `[mín, máx]`
- função — operadores: `FUNCTION`, `EXT_FUNCTION`; valor esperado: `chamada`

O operador tem de ser admissível para o tipo base do alvo (I5): `RANGE` sobre texto é rejeitado. `FUNCTION` é usado quando a função só lê valores do modelo e da regra; `EXT_FUNCTION` quando a função declara contextos externos.

#### Verificações

**S-RESTR** (operador do catálogo; um alvo, exceto numa função; mensagem ≥ 10), **S-VALOR** (forma do valor), **S-CHAMADA** (função declarada; número e tipo dos argumentos; coleções), **I5**, **I6**.

### Condição de aplicabilidade (e termos)

#### Descrição

A condição de aplicabilidade decide se uma regra de inferência se aplica. Usam-na a **RIR**, para decidir se a restrição é avaliada, e a **RIC**, para decidir se a conclusão é comunicada. É composta por um ou mais **termos**, combinados por conjunção:

```
condição = termo1 E termo2 E … E termoN
```

Cada termo tem exatamente a forma de uma verificação tipificada: um alvo (a propriedade que lê), um operador e um valor. O valor de um termo é o **fator discriminante**. A condição não existe de forma autónoma: é uma parte da regra, e cada regra tem uma única condição. Não há uma estrutura de decisões à parte: a árvore e a tabela de decisão derivam das regras (vistas `arvore` e `decisao`).

#### Atributos

- `propriedade` — papel: caminho · **ligação** · termo tipificado ou com contexto
- `operador` — papel: operador do catálogo
- `valor` — papel: valor ou lista · termo tipificado
- `contexto` — papel: nome · **ligação** · termo com contexto
- `chamada` — papel: funcao e argumentos · **ligação** · termo função

#### Exemplos

##### Esboço na declaração

No atributo `condicao` da regra, como uma lista (a ordem é irrelevante):

```json
"condicao": [
  {"propriedade": "nivelBateria", "operador": "RANGE", "valor": [0, 10]},
  {"operador": "EXT_FUNCTION", "chamada": {"funcao": "excedeDiasDesdeHoje", "argumentos": [{"caminho": "dataUltimaManutencao"}, {"literal": 7}]}}
]
```

#### Pode e não pode

- Ter 1..N termos (alvos), sobre propriedades a qualquer profundidade do nó da regra — não pode: Estar vazia numa RIR ou RIC (I4)
- Misturar termos tipificados, com contexto e com função — não pode: Ter OU entre termos
- Usar valores fora dos valores plausíveis (por exemplo `nivelBateria ∈ [0, 10]` é um limite próprio) — não pode: Ler o alvo da restrição da mesma regra (I6)
- Ser parcialmente resolvida por um perfil (seleção estática) — não pode: Existir fora de uma regra, ou ser partilhada por duas regras

Sobre os valores: usar um valor fora dos valores plausíveis numa seleção (`EQUALS` ou `IN`) dá o aviso I7, porque a regra nunca se aplicaria a esse valor.

#### Detalhes

##### Formas de termo

- **Tipificado** — declaração: `{"propriedade", "operador", "valor"}`; exemplo: `{"propriedade": "Leitura.Instalacao.ambiente", "operador": "EQUALS", "valor": "REFRIGERACAO"}`
- **Com contexto externo** — declaração: `{"propriedade", "operador", "contexto"}`: compara a propriedade com o valor de um contexto; exemplo: `{"propriedade": "dataMedicao", "operador": "LT", "contexto": "dataDeHoje"}` (RIC-MED-DIFERIDA)
- **Função** — declaração: `{"operador": "FUNCTION" ou "EXT_FUNCTION", "chamada": {…}}`; exemplo: `excedeDiasDesdeHoje(dataUltimaManutencao, 7)` (RIC-MANUT); `dentroDe(lat, lon, limitesDeLisboa)` (RIR-LX-LOCALIDADE)

Os operadores mais usados nos termos são:

- `EQUALS`, quando seleciona um único valor (`tipoDispositivo = TEMPERATURA`). Um valor simples, e não um conjunto: o dispositivo é de temperatura, e não "de um dos tipos da lista".
- `IN`, quando seleciona vários valores da mesma propriedade (`ambiente ∈ {REFRIGERACAO, ESTUFA}`). É a única disjunção admitida.
- `RANGE` e as comparações, quando seleciona um intervalo (`nivelBateria entre 0 e 10`, `totalFatura > 1000`).

Num termo com contexto, o operador é `EQUALS`, `NOT_EQUALS`, `LT`, `LTE`, `GT` ou `GTE`, e o tipo do contexto tem de ser o da propriedade.

##### Porque não há OU entre termos

1. **Legibilidade.** "tipoDispositivo = HUMIDADE e unidadeMedida = % ou tipoDispositivo = VELOCIDADE e unidadeMedida = m/s" só se lê com regras de precedência e admite duas leituras.
2. **Navegação.** Com termos apenas conjuntivos, cada regra é um único caminho na árvore de decisão, e a árvore deriva das regras. Com OU, uma regra ocuparia vários ramos.
3. **Significado.** Duas condições ligadas por OU representam, em regra, conhecimento diferente que só coincide na restrição (RIR-HUM e RIR-VEL-MS) e devem ser duas regras.

O OU não desaparece. Perguntar "que condições levam à restrição valor ∈ [0, 100]" devolve as duas regras, e a sua reunião é a disjunção. Dentro da mesma propriedade, a disjunção faz-se com `IN`.

##### Seleção estática e dinâmica

Os termos são avaliados com os valores da instância (seleção dinâmica) ou com os valores fixados no perfil (seleção estática). Um termo sobre uma propriedade fixada fica resolvido antes da execução: verdadeiro ou falso. Um termo sobre uma propriedade que nem está na projeção nem está fixada é indisponível, e a regra não é avaliável (aviso I10). Ver Perfil.md e a vista `perfil_<nome>.html`.

#### Verificações

**S-TERMO**, **I4**, **I5** (operador e tipo; contexto comparável), **I6**, **I7** (aviso) e **I10** (aviso, por perfil).

### Função

#### Descrição

As funções ocupam o espaço onde quase nunca há conhecimento partilhado sobre a forma como os dados são validados: somar uma coleção, verificar unicidade, calcular sobre uma geometria, validar um hash, uma assinatura ou o dígito de controlo de um NIF. A regra delega a verificação em quem a sabe fazer: uma função declarada.

Uma função é declarada com:

- um **nome**;
- uma **descrição**, que diz quando é verdadeira;
- os **parâmetros**, que são os **alvos** (propriedades ou coleções que lê do modelo) e os **literais** (valores declarados na regra);
- os **contextos externos** de que depende;
- o **retorno**, sempre `booleano`.

Na declaração, a função só é declarada: a implementação vive no motor de avaliação. Na tese, as funções são geradas por um LLM a partir da declaração, testadas, revistas e só depois registadas no motor.

#### Atributos

- `nome` — tipo: camelCase; obrigatório: sim
- `descricao` — tipo: texto (≥ 10): "Verdadeira quando …"; obrigatório: sim
- `parametros` — tipo: lista (≥ 1); obrigatório: sim
- `contextosExternos` — tipo: lista de nomes (pode ser vazia); obrigatório: sim
- `retorno` — tipo: `"booleano"`; obrigatório: sim
- `notas` — tipo: texto; obrigatório: não

#### Exemplos

##### Esboço na declaração

As funções declaram-se uma vez, na lista `funcoes`, e são chamadas pelo nome nas regras:

```json
"funcoes": [
  {
    "nome": "excedeDiasDesdeHoje",
    "descricao": "Verdadeira quando passaram mais de n dias desde a data indicada até à data de hoje.",
    "parametros": [
      {"nome": "data", "tipo": "data", "papel": "alvo"},
      {"nome": "n", "tipo": "inteiro", "papel": "parametro"}
    ],
    "contextosExternos": ["dataDeHoje"],
    "retorno": "booleano"
  }
]
```

Na regra:

```json
{"operador": "EXT_FUNCTION", "chamada": {"funcao": "excedeDiasDesdeHoje", "argumentos": [{"caminho": "dataUltimaManutencao"}, {"literal": 7}]}}
```

#### Pode e não pode

- Ser usada por várias regras, com argumentos diferentes (`contagemInferiorA` em RP-LIN-MAX, RIR-FS-LIN e RP-ORDEM-MAX) — não pode: Devolver outra coisa que não um booleano
- Ler propriedades, listas de valores de uma coleção ou instâncias de um modelo — não pode: Aceder a contextos externos que não declare
- Depender de contextos externos (só com EXT_FUNCTION) — não pode: Ser chamada com um número de argumentos diferente do de parâmetros
- Receber literais declarados na regra — não pode: Ter efeitos laterais ou repetir verificações de presença (regra de geração)

#### Detalhes

##### Onde pode ser usada

- **Numa restrição** (RP ou RIR) — operador: `FUNCTION` ou `EXT_FUNCTION`; efeito: A função é a verificação; se falha, comunica-se a mensagem da restrição; exemplos: RP-SOMA, RP-AREA, RP-HASH, RIR-FS-LIN
- **Num termo de uma condição** (RIR ou RIC) — operador: `FUNCTION` ou `EXT_FUNCTION`; efeito: A função decide (com os outros termos) se a regra se aplica; exemplos: RIC-MANUT (`excedeDiasDesdeHoje`), RIR-LX-LOCALIDADE (`dentroDe` Lisboa)

O operador é `FUNCTION` quando a função só usa valores do modelo e da regra, e `EXT_FUNCTION` quando usa também contextos externos (I5).

##### Parâmetros

- `nome` — valores: texto; significado: Nome do parâmetro (posição na chamada).
- `tipo` — valores: tipo base, `lista<tipo>`, `modelo`, ou outro (`poligono`); significado: O que a função recebe.
- `papel` — valores: `alvo` · `parametro`; significado: `alvo` recebe um caminho do modelo (`{"caminho": …}`); `parametro` recebe um literal da regra (`{"literal": …}`).
- `colecao` — valores: booleano; significado: O argumento atravessa uma composição repetível (lista de valores ou de instâncias).
- `descricao` — valores: texto; significado: Opcional.

O que é literal e o que é contexto. A área autorizada de RP-AREA não está no modelo, mas também não é um contexto externo: é informação da própria regra, como os limites de um RANGE, e passa-se como literal. A data de hoje é um contexto externo: não pertence ao modelo nem à regra.

#### Verificações

**S-FUNC** (declaração), **S-CHAMADA** (função declarada; número de argumentos; caminho ou literal conforme o papel; coleções), **I5** (FUNCTION vs EXT_FUNCTION) e **I13** (aviso: função declarada mas não usada).

### Contexto externo

#### Descrição

Parte da informação de que uma regra precisa não pertence ao modelo nem à regra: a data atual, a chave com que um dispositivo assina as mensagens, o relógio do servidor, as séries comunicadas à AT, o hash do último documento emitido. Chama-se a isto contexto externo (a tese marca-o com ᵉˣᵗ).

A dependência da validação em relação a um contexto tem de estar num sítio consultável (eixos E7 e E9). O contexto declara-se uma vez e liga-se a quem o usa. Assim, é possível perguntar que regras dependem de um sistema externo e que contextos têm de estar disponíveis para avaliar.

#### Atributos

- `nome` — tipo: camelCase; obrigatório: sim; descrição: Único.
- `tipo` — tipo: tipo base; obrigatório: sim; descrição: Para comparar com propriedades num termo.
- `descricao` — tipo: texto (≥ 10); obrigatório: sim; descrição: O que é o valor.
- `fonte` — tipo: texto; obrigatório: não (recomendado); descrição: De onde o motor o obtém.
- `notas` — tipo: texto; obrigatório: não; descrição: Comentário livre.

A regra pode ainda declarar `contextosExternos` (lista de nomes): é derivável (dos termos e das funções). Se estiver presente, tem de coincidir com os contextos usados (aviso I11).

#### Exemplos

##### Esboço na declaração

```json
"contextosExternos": [
  {"nome": "dataDeHoje", "tipo": "data", "descricao": "Data atual no momento da avaliação (AAAA-MM-DD).",
   "fonte": "Relógio do motor de avaliação; pode ser fixada por um perfil."}
]
```

#### Pode e não pode

- Ser usado por várias funções e termos — não pode: Ser passado como argumento de uma chamada (as funções acedem-lhe pela interface do motor)
- Ser comparado com uma propriedade do mesmo tipo — não pode: Ser comparado com uma propriedade de outro tipo (I5)
- Ser fixado por perfis — não pode: Ser confundido com um literal da regra (a área autorizada é um literal)

#### Detalhes

##### Como é usado

- **Por uma função** — declaração: a função lista-o em `contextosExternos`; a regra usa `EXT_FUNCTION`; exemplo: `excedeDiasDesdeHoje` usa `dataDeHoje` (RIC-MANUT)
- **Diretamente num termo** — declaração: `{"propriedade", "operador", "contexto"}`; exemplo: `dataMedicao < dataDeHoje` (RIC-MED-DIFERIDA)
- **Fixado por um perfil** — declaração: `{"contexto": "dataDeHoje", "valor": "2026-09-30"}` em `perfis[].fixa`; exemplo: AuditoriaSetembro2026, TesteRefrigeracao

O motor obtém o valor no momento da avaliação, a partir da fonte, ou recebe-o já fixado pelo perfil. Fixá-lo torna a avaliação reprodutível: uma auditoria avaliada "como se hoje fosse" 2026-09-30.

#### Verificações

**S-CTX** (nome, tipo, descrição), **S-FUNC** (contextos das funções declarados), **S-TERMO** (contexto de um termo declarado), **I5** (tipo comparável) e **I13** (aviso: declarado mas não usado).

### RE (regra estrutural) e Projeção

#### Descrição

As condições estruturais são a presença, o tipo e a cardinalidade (notNull, isString, isInteger, …). Não se declaram regra a regra. O tipo já está na propriedade e a cardinalidade na composição (eixo E4). O que varia de utilização para utilização é que partes do modelo devem estar presentes. Isso exprime-se pela **projeção**.

Uma projeção é definida sobre um HLM e distingue, para uma utilização:

- **obrigatórias:** propriedades que têm de estar presentes e respeitar a estrutura;
- **permitidas:** propriedades que podem estar presentes e são avaliadas quando existem;
- **proibidas:** todas as restantes, implicitamente (não se declaram).

A projeção não cria regras sobre as propriedades nem escolhe que regras correm. Define o âmbito estrutural da avaliação para uma utilização concreta. Estrutura e regras não se confundem (eixo E2).

#### Atributos

- `nome` — tipo: texto, PascalCase; obrigatório: sim; descrição: Único entre as projeções.
- `hlm` — tipo: nome de HLM; obrigatório: sim; descrição: O HLM projetado.
- `descricao` — tipo: texto; obrigatório: não (recomendado); descrição: A utilização.
- `obrigatorias` — tipo: lista de caminhos; obrigatório: sim (pode ser vazia); descrição: A partir do HLM; aceita `X.*`.
- `permitidas` — tipo: lista de caminhos; obrigatório: sim (pode ser vazia); descrição: Idem.
- `notas` — tipo: texto; obrigatório: não; descrição: Comentário livre.

Os caminhos partem do HLM (`Leitura.Medicao.*`, `Identificacao.estado`). `X.*` expande para todas as propriedades, a qualquer profundidade, abaixo de X. Um caminho sem `*` tem de terminar numa propriedade.

#### Exemplos

##### Esboço na declaração

Na lista `projecoes`:

```json
{
  "nome": "NomeDaProjecao",
  "hlm": "NomeDoHLM",
  "descricao": "Para que utilização.",
  "obrigatorias": ["SmA.*", "SmB.UsmX.propriedade"],
  "permitidas": ["SmC.*"]
}
```

#### Pode e não pode

- Incidir sobre um único HLM — não pode: Incidir sobre um SM ou USM
- Usar `X.*` para todas as propriedades abaixo de X — não pode: Ter a mesma propriedade (caminho) obrigatória e permitida (I9)
- Selecionar uma ocorrência específica pelo caminho (`Localizacao.Morada.pais`) — não pode: Selecionar um caminho que não existe (I9)
- Coexistir com outras projeções sobre o mesmo HLM — não pode: Conter regras ou valores fixados (os valores são do perfil)

##### Como saber se é uma projeção (e não uma regra)

- "Para esta utilização, o NIF do cliente tem de vir" — o que usar: Projeção (obrigatória)
- "O NIF tem nove algarismos" — o que usar: RP
- "Acima de 1000 euros, o NIF do cliente não pode ser o de consumidor final" — o que usar: RIR
- "Na fatura simplificada não vem o cliente" — o que usar: Projeção (FaturaSimplificada não inclui `Cliente.*`)

#### Detalhes

##### Contextos de utilização

- Estruturas diferentes por utilização do mesmo modelo (CA5): uma fatura simplificada e uma fatura para a AT; um dispositivo em testes e em produção.
- A pesquisa inversa "em que projeções é usada esta propriedade" (vista `impacto`) e a matriz de projeções (vista `projecoes`).
- Juntamente com o perfil, decide se uma regra é avaliável: se a condição lê uma propriedade que a projeção não inclui e o perfil não fixa, a regra não é avaliável (I10).

#### Verificações

**S-PROJ** (nome; HLM declarado; listas) e **I9** (caminhos existem; obrigatórias ∩ permitidas = ∅).

### Perfil de execução

#### Descrição

O perfil liga o conhecimento de validação a um cenário concreto. Indica a **projeção** usada (e, por ela, o HLM). Fixa os **valores conhecidos antes da execução**: propriedades do modelo e contextos externos. O perfil não contém regras. Define o cenário em que as regras já declaradas vão ser avaliadas.

A diferença entre **seleção estática** e **seleção dinâmica** não está na regra nem na condição. Está na origem dos valores usados para avaliar a condição: o perfil (estática) ou a instância (dinâmica).

- Estática — os valores vêm de: `fixa` do perfil; efeito: Os termos ficam resolvidos antes da execução: a regra fica sempre aplicável ou nunca aplicável; exemplo: RefrigeracaoLote: RIR-TEMP-REFRIG-CELSIUS sempre aplicável, RIR-TEMP-ESTUFA-CELSIUS nunca aplicável
- Dinâmica — os valores vêm de: a instância; efeito: A condição é avaliada instância a instância; as propriedades da condição têm de estar na projeção; exemplo: LeiturasIndustriais (nada fixado)

Uma propriedade fixada pode não fazer parte da projeção: o seu valor já é conhecido, e a instância não precisa de o trazer (TesteRefrigeracao fixa `ambiente`, que DispositivoTeste não projeta). Se uma condição lê uma propriedade que não está na projeção nem está fixada, a regra não é avaliável. O motor assinala isto quando o perfil é criado (aviso I10, perfil TesteLaboratorio).

#### Atributos

- `nome` — tipo: PascalCase; obrigatório: sim; descrição: Único.
- `projecao` — tipo: nome de projeção; obrigatório: sim; descrição: A projeção usada.
- `descricao` — tipo: texto; obrigatório: não (recomendado); descrição: O cenário.
- `fixa` — tipo: lista de `{propriedade, valor}` ou `{contexto, valor}`; obrigatório: sim (pode ser vazia); descrição: Valores conhecidos antes da execução.
- `hlm` — tipo: nome de HLM; obrigatório: não; descrição: Redundante (vem da projeção); se presente, tem de coincidir.
- `notas` — tipo: texto; obrigatório: não; descrição: Comentário livre.

#### Exemplos

##### Esboço na declaração

```json
"perfis": [
  {
    "nome": "RefrigeracaoLote",
    "projecao": "DispositivoProducao",
    "descricao": "Lote de sensores de temperatura em câmaras de refrigeração, em °C.",
    "fixa": [
      {"propriedade": "Identificacao.tipoDispositivo", "valor": "TEMPERATURA"},
      {"propriedade": "Leitura.Instalacao.ambiente", "valor": "REFRIGERACAO"},
      {"propriedade": "Leitura.Medicao.unidadeMedida", "valor": "°C"},
      {"contexto": "dataDeHoje", "valor": "2026-09-30"}
    ]
  }
]
```

#### Pode e não pode

- Usar exatamente uma projeção — não pode: Conter regras
- Fixar propriedades (por caminho a partir do HLM) com valores plausíveis — não pode: Fixar um valor não plausível (I9)
- Fixar contextos externos — não pode: Fixar um caminho que não existe (I9)
- Não fixar nada (seleção dinâmica) — não pode: Ter um HLM diferente do da projeção

#### Detalhes

##### Como construir um perfil estático

Faz-se a pesquisa "candidatos a fixar": dadas as propriedades a validar, obtêm-se as outras propriedades usadas nas condições das regras que as restringem. Para `valor` e `unidadeMedida`, são `tipoDispositivo`, `unidadeMedida` e `ambiente` (vista `candidatos_perfil`).

##### Observações (tese, Seleção estática e dinâmica)

1. O conhecimento não muda com o cenário: só o perfil muda.
2. A seleção é declarada, e não escondida em código.
3. O que fica de fora é consultável antes de executar.
4. O perfil lê-se como uma regra.
5. A fronteira com o exterior é explícita: os contextos são fixados no perfil ou obtidos pelo motor.

#### Verificações

**S-PERFIL** (projeção declarada; cada fixação tem `propriedade` ou `contexto` e `valor`), **I9** (caminhos existem; valores plausíveis) e **I10** (aviso: regras não avaliáveis).

## Convenções e verificação

### Nomenclatura

- HLM, SM, USM — regra: PascalCase, sem acentos, singular; exemplos: `Fatura`, `InformacaoGeografica`, `Linha`; verificação: S-MOD
- SM de coleção — regra: plural do elemento; exemplos: `Linhas` (elemento `Linha`); verificação: (convenção)
- Papel de composição — regra: PascalCase; por omissão, o nome do modelo; exemplos: `Requerente`, `Origem`, `Destino`; verificação: S-COMP
- Propriedade — regra: camelCase, sem acentos; exemplos: `codigoPostal`, `dataUltimaManutencao`, `tipoIVA`; verificação: S-PROP
- Nome alternativo — regra: o nome tal como aparece na fonte; exemplos: `zipCode`, `postalCode`, `CP`, `deviceId`, `reading`
- Regra — regra: `TIPO-ASSUNTO[-QUALIFICADOR]`, maiúsculas e algarismos com hífens; o tipo é `RP`, `RIR` ou `RIC` e coincide com a natureza; exemplos: `RP-LAT`, `RIR-TEMP-REFRIG-CELSIUS`, `RIC-MANUT`, `RIR-CP-LX-AJUDA`; verificação: S-REGRA
- Natureza — regra: `plausibilidade`, `inferencia_restritiva`, `inferencia_conclusiva`; verificação: S-REGRA
- Valores enumerados — regra: MAIÚSCULAS, sem acentos, `_` entre palavras; exemplos: `REFRIGERACAO`, `NAO_FIAVEL`, `AVENIDAS_NOVAS`; verificação: (convenção)
- Conclusão de uma RIC — regra: `tipo`: `ACAO` ou `ESTADO`; `valor` em maiúsculas; exemplos: `ACAO` `MANUTENCAO`; `ESTADO` `DIFERIDA`; verificação: S-REGRA
- Função — regra: camelCase; um predicado ("verdadeira quando …"); exemplos: `somaIgualA`, `dentroDe`, `excedeDiasDesdeHoje`; verificação: S-FUNC
- Contexto externo — regra: camelCase; exemplos: `dataDeHoje`, `chaveDispositivo`, `seriesComunicadasAT`; verificação: S-CTX
- Projeção — regra: PascalCase, nome da utilização; exemplos: `FaturaSimplificada`, `DispositivoProducao`; verificação: S-PROJ
- Perfil — regra: PascalCase, nome do cenário; exemplos: `RefrigeracaoLote`, `EmissaoSimplificada`; verificação: S-PERFIL
- Ficheiro de declaração — regra: `<hlm em snake_case>.ecv.json`; exemplos: `ordem_instalacao.ecv.json`

#### Assuntos usados nos identificadores das regras

- `TEMP`, `HUM`, `PRES`, `VEL` — significado: temperatura, humidade, pressão, velocidade
- `UN` — significado: unidade de medida
- `REFRIG`, `ESTUFA`, `ARMAZEM`, `SERVIDORES`, `EXTERIOR`, `INCIN`, `CAMARA` — significado: ambiente de instalação
- `CELSIUS`, `KELVIN`, `FAHRENHEIT` (ou `C`, `K`, `F`), `HPA`, `BAR`, `MS`, `KMH` — significado: unidade
- `CP` — significado: código postal; `LX` Lisboa
- `IVA` (`ISE`, `RED`, `INT`, `NOR`) — significado: tipo de IVA
- `FS`, `FT` — significado: fatura simplificada, fatura
- `LIN` — significado: linhas
- `MANUT`, `REDE`, `MED` — significado: manutenção, rede, medição

#### Mensagens e descrições

- A **mensagem de não conformidade** (na restrição) é autocontida: diz o que falhou e o que é esperado, sem identificadores. Exemplo: "O código postal português tem de ter o formato 0000-000, sem começar por zero."
- A **mensagem de conclusão** (numa RIC) começa pela conclusão e explica o motivo. Exemplo: "Ação MANUTENCAO: o nível de bateria está baixo e …".
- A **descrição** da regra é derivada (ver Regra.md).
- A **descrição de modelos e propriedades** é precisa. Uma descrição vaga ("Valor", "Dados") aparece como tal nas vistas, e é aí que se corrige.

### Caminhos

Um caminho refere uma propriedade (ou um modelo) a partir de um nó. É formado pelos **papéis** das composições a percorrer, separados por pontos, seguidos opcionalmente do **nome de uma propriedade**.

#### De onde parte o caminho

- Regra que vive num HLM — relativo a: o HLM; exemplo: `Leitura.Medicao.valor`, `Cabecalho.totalFatura`, `Linhas.Linha`
- Regra que vive num SM — relativo a: o SM; exemplo: `Morada.localidade`, `InformacaoGeografica.latitude`, `Linha.numero` (SM Linhas)
- Regra que vive num USM — relativo a: o USM; exemplo: `pais`, `codigoPostal`
- Regra que vive numa propriedade — relativo a: o modelo dono da propriedade; exemplo: `latitude` (só pode ler a própria propriedade)
- Projeção — relativo a: o HLM; exemplo: `Identificacao.estado`, `Leitura.Medicao.*`
- Perfil (`fixa`) — relativo a: o HLM da projeção; exemplo: `Leitura.Instalacao.ambiente`

#### Segmentos

- Cada segmento intermédio é o **papel** de uma composição. Por omissão, o papel é o nome do modelo composto. Com `papel` explícito, usa-se o papel: `Requerente.Entidade.nif` (OrdemInstalacao compõe Cliente com o papel Requerente).
- O último segmento é uma propriedade ou um papel. Se for um papel, o caminho termina num modelo. Isto só é admitido em argumentos de funções (instâncias de uma coleção: `Linhas.Linha`, `Localizacao`).
- Um caminho que atravessa uma composição repetível (`1..*`, `0..*`) é uma **coleção**: `Linhas.Linha.valor` é a lista dos valores de todas as linhas.

#### Na descrição das regras

Na descrição derivada, os caminhos aparecem prefixados com o nome do nó onde a regra vive, exceto no HLM: `Morada.pais`, `Diagnostico.nivelBateria`, mas `Identificacao.tipoDispositivo` numa regra do HLM Dispositivo. É a "ligação ao modelo" da tese.

#### Nas projeções: `*`

- `X.*` — expande para: todas as propriedades, a qualquer profundidade, abaixo de X
- `*` — expande para: todas as propriedades do HLM
- `X.Y.prop` — expande para: só essa propriedade, nesse caminho

`X.*` sobre um caminho que termina numa propriedade é um erro; um caminho sem `*` tem de terminar numa propriedade.

#### Ocorrências

O mesmo modelo pode ser alcançado por vários caminhos no mesmo HLM. Por exemplo, na Fatura, Morada é alcançada por `Emitente.Morada` e `Cliente.Morada`. Cada caminho é uma **ocorrência**. A propriedade é a mesma (o mesmo nó no grafo), mas a projeção e o perfil referem ocorrências: as arestas `OBRIGATORIA`, `PERMITIDA` e `FIXA` guardam o `caminho`. Uma regra que vive num modelo reutilizado aplica-se em cada ocorrência. A vista `perfil` avalia-a por ocorrência.

#### Chaves no grafo

- Propriedade — chave: `<nível do dono>:<dono>.<nome>`; exemplo: `USM:Medicao.valor`, `SM:Cabecalho.totalFatura`
- Restrição — chave: `<id da regra>#restricao`; exemplo: `RP-LAT#restricao`
- Condição — chave: `<id da regra>#condicao`; exemplo: `RIR-FS#condicao`
- Restantes — chave: `nome` (modelos, funções, contextos, projeções, perfis) ou `id` (regras); exemplo: `Morada`, `RIC-MANUT`

#### Implementação

`ecv/3_ingestion/paths.py` contém as funções `resolver` (resolve um caminho a partir de um nó, com os passos, a propriedade final, se é coleção e o tipo), `expandir` (o `*` das projeções), `ocorrencias` (os caminhos de todos os nós de um HLM) e `chave_propriedade`.

### Catálogo: tipos base, operadores e forma dos valores

O catálogo é o vocabulário fechado da linguagem de verificações tipificadas. É a mesma linguagem da restrição e de cada termo da condição. Com um vocabulário fechado, qualquer regra pode ser verificada antes de ser usada, seja qual for a sua origem, incluindo regras geradas por um LLM. A fonte única é ecv/config/ecv.config.json, lida diretamente pelo código (`ecv/config/__init__.py`).

#### Tipos base

- `texto` — valor: cadeia de caracteres; notas: Um enumerado é um texto com uma RP `IN`.
- `inteiro` — valor: número inteiro
- `decimal` — valor: número
- `data` — valor: `AAAA-MM-DD` ou data e hora ISO 8601; notas: Compara-se por ordem; `RANGE`, `LT` e outros aceitam datas.
- `booleano` — valor: `true` / `false`

#### Operadores

- `EQUALS` — uso: igual a um valor; valor esperado: valor simples; exemplo: `tipoDispositivo EQUALS TEMPERATURA`
- `NOT_EQUALS` — uso: diferente de um valor; valor esperado: valor simples; exemplo: `Cliente.Entidade.nif NOT_EQUALS 999999990`
- `IN` — uso: pertence a um conjunto (um só desses valores); valor esperado: lista não vazia; exemplo: `tipoDocumento IN [FT, FS, FR, NC, ND]`
- `RANGE` — uso: num intervalo, inclusive; valor esperado: `[mín, máx]`, mín ≤ máx; exemplo: `latitude RANGE [-90, 90]`
- `LT`, `LTE`, `GT`, `GTE` — uso: comparação; valor esperado: número (ou data); exemplo: `totalFatura LTE 1000`; `dataUltimaManutencao GTE 2000-01-01`
- `PATTERN` — uso: expressão regular; valor esperado: regex válida; exemplo: `codigoPostal PATTERN ^[1-9][0-9]{3}-[0-9]{3}$`
- `CONTAINS`, `STARTS_WITH`, `ENDS_WITH` — uso: parte de um texto; valor esperado: texto; exemplo: `numero STARTS_WITH FS`; `email ENDS_WITH @companhiax.com`
- `LENGTH` — uso: comprimento; valor esperado: inteiro, ou `[mín, máx]`; exemplo: `fabricante LENGTH [2, 50]`
- `FUNCTION` — uso: chamada a uma função que só usa valores do modelo e da regra; valor esperado: `chamada`; exemplo: `somaIgualA(Linhas.Linha.valor, Cabecalho.totalFatura)`
- `EXT_FUNCTION` — uso: chamada a uma função que usa também contextos externos; valor esperado: `chamada`; exemplo: `excedeDiasDesdeHoje(dataUltimaManutencao, 7)`

Os operadores organizam-se em cinco grupos:

- **Igualdade e pertença:** enumerados.
- **Intervalo e comparação:** gamas e limites.
- **Padrão:** formatos.
- **Texto:** partes e comprimento.
- **Função:** delegação.

Num termo que compara com um contexto externo, o operador é `EQUALS`, `NOT_EQUALS`, `LT`, `LTE`, `GT` ou `GTE`.

#### Operadores admissíveis por tipo base (I5)

- texto — verificações aplicáveis: EQUALS, NOT_EQUALS, IN, PATTERN, LENGTH, CONTAINS, STARTS_WITH, ENDS_WITH
- inteiro, decimal — verificações aplicáveis: EQUALS, NOT_EQUALS, IN, RANGE, LT, LTE, GT, GTE; PATTERN sobre a representação (por exemplo, casas decimais)
- data — verificações aplicáveis: EQUALS, NOT_EQUALS, RANGE, LT, LTE, GT, GTE
- booleano — verificações aplicáveis: EQUALS
- qualquer tipo — verificações aplicáveis: FUNCTION, EXT_FUNCTION (a função não tem alvo próprio)

#### Navegação por tipo de verificação

Ter a terminologia do lado da solução permite questionar o conhecimento por tipo de verificação. Por exemplo: todas as regras IN (os enumerados), todas as STARTS_WITH, ou as gamas RANGE sobre uma propriedade, para detetar incoerências. Ver as vistas `operadores`, `decisao` e `coerencia`.

### Verificação: specs e invariantes

A verificação antecede a materialização (tese, Secção "Verificação da declaração"). Faz-se em dois níveis:

1. **Specs:** cada entidade isolada (atributos obrigatórios, forma, nomes). Inclui a validação contra o JSON Schema quando o pacote `jsonschema` está instalado.
2. **Invariantes:** o que só se verifica com todas as entidades carregadas.

Um **erro** impede a materialização. Um **aviso** não a impede, mas é apresentado.

```
python -m ecv verificar          # todas as declarações de specs/exemplos
```

#### Specs

- S-SCHEMA — entidade: toda a declaração; verifica: Forma contra `specs/declaracao/ecv.schema.json`
- S-DECL — entidade: declaração; verifica: exatamente um HLM (e o cabeçalho `declaracao.hlm` indica-o); `usm` existe e não está vazia; nomes únicos em cada secção
- S-MOD — entidade: HLM, SM, USM; verifica: PascalCase; descrição ≥ 10; o HLM sem propriedades e com composição; o USM com propriedades e sem composição; o SM com composição ou propriedades
- S-COMP — entidade: composição; verifica: Um de `sm` ou `usm`, coerente com o nível; cardinalidade válida; papel em PascalCase e único
- S-PROP — entidade: propriedade; verifica: camelCase; tipo base; descrição ≥ 5; nomes únicos e diferentes dos papéis
- S-REGRA — entidade: regra; verifica: Natureza válida; id `TIPO-…` coerente com a natureza; descrição; mensagem na restrição (RP, RIR) ou na regra (RIC); `conclusao` só em RIC
- S-RESTR — entidade: restrição; verifica: Operador do catálogo; um alvo (exceto numa função); mensagem ≥ 10
- S-TERMO — entidade: termo; verifica: Operador do catálogo; propriedade (exceto numa função); contexto declarado
- S-VALOR — entidade: restrição e termo; verifica: Forma do valor exigida pelo operador (lista, intervalo, regex válida, …)
- S-CHAMADA — entidade: chamada; verifica: Função declarada; número de argumentos; caminho para alvos e literal para parâmetros; coleções
- S-FUNC — entidade: função; verifica: camelCase; descrição; parâmetros com papel e tipo; contextos declarados; retorno booleano
- S-CTX — entidade: contexto externo; verifica: camelCase; tipo base; descrição
- S-PROJ — entidade: projeção; verifica: PascalCase; HLM declarado; listas
- S-PERFIL — entidade: perfil; verifica: PascalCase; projeção declarada; HLM coerente; cada fixação tem `propriedade` ou `contexto` e `valor`

#### Invariantes

- I1 — invariante: A composição é acíclica.; gravidade: erro; origem: tese
- I2 — invariante: Todos os modelos compostos estão declarados.; gravidade: erro; origem: tese
- I3 — invariante: Todos os caminhos de uma regra (termos e argumentos) resolvem a partir do nó onde a regra vive; uma regra declarada numa propriedade só lê essa propriedade.; gravidade: erro; origem: tese
- I4 — invariante: Uma RP tem restrição e não tem condição; uma RIR tem condição e restrição; uma RIC tem condição e mensagem de conclusão, sem restrição.; gravidade: erro; origem: tese
- I5 — invariante: O operador é admissível para o tipo base; EXT_FUNCTION só para funções com contextos externos (e FUNCTION para as restantes); um contexto comparado é do tipo da propriedade.; gravidade: erro; origem: tese
- I6 — invariante: A condição não lê o alvo da restrição da mesma regra.; gravidade: erro; origem: tese
- I7 — invariante: Os valores usados numa condição (EQUALS, IN) pertencem aos valores plausíveis da propriedade; senão, a regra nunca se aplica.; gravidade: aviso; origem: tese
- I8 — invariante: Uma regra de um SM ou HLM que só lê um filho não repetível poderia viver nesse filho; uma regra de um modelo que só lê uma propriedade poderia viver nela.; gravidade: aviso; origem: tese
- I9 — invariante: Os caminhos das projeções e dos perfis existem no HLM; uma propriedade não é obrigatória e permitida ao mesmo tempo; os valores fixados são plausíveis.; gravidade: erro; origem: tese
- I10 — invariante: Num perfil, uma regra cuja condição lê propriedades nem projetadas nem fixadas não é avaliável.; gravidade: aviso; origem: tese (Seleção, Figura "Propriedade usada na aplicabilidade mas não projetada")
- I11 — invariante: Os `contextosExternos` declarados numa regra coincidem com os que ela usa.; gravidade: aviso; origem: esta versão
- I12 — invariante: A descrição de uma regra coincide com a derivada.; gravidade: aviso; origem: esta versão
- I13 — invariante: Funções e contextos declarados são usados.; gravidade: aviso; origem: esta versão

#### Avisos esperados nos exemplos

A declaração do Dispositivo tem exatamente dois avisos, ambos intencionais; as restantes não têm nenhum (ver exemplos):

- **I7:** RIR-TEMP-CAMARA-CELSIUS usa `ambiente = CAMARA_FRIGORIFICA`, que não é plausível.
- **I10:** o perfil TesteLaboratorio deixa 28 RIR não avaliáveis, porque não projeta nem fixa `ambiente`.


## O que já existe (reutilizar antes de criar)

Um modelo reutiliza-se com o MESMO nome e fica IGUAL ao que está aqui: a mesma descrição e as mesmas propriedades (nome, tipo, descrição, nomes alternativos, notas) e composições, porque a fusão compara tudo isto e rejeita diferenças. Reutilizar traz também as regras que já vivem nele (regrasQueVivemNele): o código junta-as à declaração, não as repitas, mas confirma que valem para este domínio. Se o modelo ou as suas regras não servem tal e qual, cria-se outro, com outro nome, e regista-se a razão numa nota. Os nomes dos HLM existentes também estão ocupados. As funções reutilizam-se pelo nome, com os mesmos parâmetros.

### Modelos
```json
[
{"nivel":"HLM","nome":"Dispositivo","descricao":"Dispositivo IoT: identificação, leitura, localização e diagnóstico.","notas":"As gamas seguem o mapeamento conhecido do Capítulo 4 (matriz de decisão): RIR-TEMP-C é a gama física [-60, 1300] (no texto do Capítulo 3 usou-se [-50, 100], ilustrativa).","composicao":["SM Identificacao [1..1]","SM Leitura [1..1]","SM Localizacao [1..1]","SM Diagnostico [0..1]"],"regrasQueVivemNele":["RIR-HUM","RIR-HUM-ARMAZEM","RIR-HUM-ESTUFA","RIR-HUM-EXTERIOR","RIR-HUM-REFRIG","RIR-HUM-SERVIDORES","RIR-HUM-UN","RIR-PRES-BAR","RIR-PRES-EXTERIOR-BAR","RIR-PRES-EXTERIOR-HPA","RIR-PRES-HPA","RIR-PRES-UN","RIR-TEMP-ARMAZEM-CELSIUS","RIR-TEMP-ARMAZEM-FAHRENHEIT","RIR-TEMP-ARMAZEM-KELVIN","RIR-TEMP-C","RIR-TEMP-CAMARA-CELSIUS","RIR-TEMP-ESTUFA-CELSIUS","RIR-TEMP-ESTUFA-FAHRENHEIT","RIR-TEMP-ESTUFA-KELVIN","RIR-TEMP-EXTERIOR-CELSIUS","RIR-TEMP-EXTERIOR-FAHRENHEIT","RIR-TEMP-EXTERIOR-KELVIN","RIR-TEMP-F","RIR-TEMP-INCIN-CELSIUS","RIR-TEMP-INCIN-FAHRENHEIT","RIR-TEMP-INCIN-KELVIN","RIR-TEMP-K","RIR-TEMP-REFRIG-CELSIUS","RIR-TEMP-REFRIG-FAHRENHEIT","RIR-TEMP-REFRIG-KELVIN","RIR-TEMP-SERVIDORES-CELSIUS","RIR-TEMP-SERVIDORES-FAHRENHEIT","RIR-TEMP-SERVIDORES-KELVIN","RIR-TEMP-UN","RIR-VEL-EXTERIOR-KMH","RIR-VEL-EXTERIOR-MS","RIR-VEL-KMH","RIR-VEL-MS","RIR-VEL-UN"]},
{"nivel":"HLM","nome":"Fatura","descricao":"Documento fiscal de venda: cabeçalho, emitente, cliente e linhas.","composicao":["SM Cabecalho [1..1]","SM Emitente [1..1]","SM Cliente [1..1]","SM Linhas [1..1]"],"regrasQueVivemNele":["RIR-FS-LIN","RIR-FT-NIF","RP-SOMA"]},
{"nivel":"HLM","nome":"OrdemInstalacao","descricao":"Ordem de instalação de equipamento: quem a pede e onde instalar.","notas":"Exemplo da Secção ECM: reutiliza o SM Cliente da Fatura (com o papel Requerente, atribuído pela composição) e o SM Localizacao do Dispositivo, com cardinalidade 1..*.","composicao":["SM Pedido [1..1]","SM Cliente [1..1] papel Requerente","SM Localizacao [1..*]"],"regrasQueVivemNele":["RP-ORDEM-MAX"]},
{"nivel":"USM","nome":"Assinatura","descricao":"Assinatura digital de uma mensagem enviada por um dispositivo.","propriedades":[{"nome":"mensagem","tipo":"texto","descricao":"Conteúdo assinado, tal como enviado pelo dispositivo","nomesAlternativos":["payload"]},{"nome":"assinatura","tipo":"texto","descricao":"Assinatura HMAC-SHA256 da mensagem, em hexadecimal","nomesAlternativos":["signature"]}],"composicao":[],"regrasQueVivemNele":["RP-ASSIN-FORMA","RP-ASSINATURA"],"usadoPor":["Leitura"]},
{"nivel":"USM","nome":"Contacto","descricao":"Contacto eletrónico de uma entidade.","propriedades":[{"nome":"email","tipo":"texto","descricao":"Endereço de correio eletrónico","nomesAlternativos":["eMail","correioEletronico"]}],"composicao":[],"regrasQueVivemNele":["RP-EMAIL"],"usadoPor":["Emitente"]},
{"nivel":"USM","nome":"Diagnostico","descricao":"Estado técnico do dispositivo: bateria, manutenção e rede.","propriedades":[{"nome":"nivelBateria","tipo":"decimal","descricao":"Nível de bateria (%)","nomesAlternativos":["battery"]},{"nome":"dataUltimaManutencao","tipo":"data","descricao":"Data da última manutenção","nomesAlternativos":["lastMaintenance"]},{"nome":"sinalRede","tipo":"decimal","descricao":"Intensidade do sinal de rede (dBm)","nomesAlternativos":["rssi"]},{"nome":"latencia","tipo":"decimal","descricao":"Latência da comunicação (ms)","nomesAlternativos":["latency"]},{"nome":"taxaRececao","tipo":"decimal","descricao":"Taxa de receção de mensagens (%)","nomesAlternativos":["receptionRate"]}],"composicao":[],"regrasQueVivemNele":["RIC-MANUT","RIC-REDE","RP-BATERIA","RP-LATENCIA","RP-MANUT-DATA","RP-MANUT-FUTURA","RP-RECECAO","RP-SINAL"],"usadoPor":["Diagnostico"]},
{"nivel":"USM","nome":"Entidade","descricao":"Pessoa singular ou coletiva identificada pelo NIF.","propriedades":[{"nome":"nif","tipo":"texto","descricao":"Número de identificação fiscal","nomesAlternativos":["taxId","VATNumber"]},{"nome":"nome","tipo":"texto","descricao":"Nome ou denominação social","nomesAlternativos":["name","denominacao"]}],"composicao":[],"regrasQueVivemNele":["RP-NIF","RP-NIF-DC"],"usadoPor":["Cliente","Emitente"]},
{"nivel":"USM","nome":"InformacaoGeografica","descricao":"Coordenadas geográficas de um ponto e o respetivo sistema de referência.","propriedades":[{"nome":"latitude","tipo":"decimal","descricao":"Latitude, em graus decimais","nomesAlternativos":["lat"]},{"nome":"longitude","tipo":"decimal","descricao":"Longitude, em graus decimais","nomesAlternativos":["lon","lng"]},{"nome":"altitude","tipo":"decimal","descricao":"Altitude, em metros","nomesAlternativos":["alt","elevation"]},{"nome":"sistemaReferencia","tipo":"texto","descricao":"Sistema de referência das coordenadas","nomesAlternativos":["crs","datum"]}],"composicao":[],"regrasQueVivemNele":["RP-ALT","RP-AREA","RP-LAT","RP-LON","RP-SRC"],"usadoPor":["Localizacao"]},
{"nivel":"USM","nome":"Instalacao","descricao":"Local de instalação do dispositivo, caracterizado pelo ambiente.","propriedades":[{"nome":"ambiente","tipo":"texto","descricao":"Ambiente onde o dispositivo está instalado","nomesAlternativos":["environment"]}],"composicao":[],"regrasQueVivemNele":["RP-AMBIENTE"],"usadoPor":["Leitura"]},
{"nivel":"USM","nome":"Linha","descricao":"Linha de um documento: um bem ou serviço, com valor e IVA.","propriedades":[{"nome":"numero","tipo":"inteiro","descricao":"Número da linha no documento","nomesAlternativos":["lineNumber"]},{"nome":"descricao","tipo":"texto","descricao":"Descrição do bem ou serviço","nomesAlternativos":["description"]},{"nome":"valor","tipo":"decimal","descricao":"Valor da linha, em euros","nomesAlternativos":["amount"]},{"nome":"tipoIVA","tipo":"texto","descricao":"Tipo de taxa de IVA aplicada à linha","nomesAlternativos":["taxType"]},{"nome":"taxaIVA","tipo":"decimal","descricao":"Taxa de IVA aplicada à linha (%)","nomesAlternativos":["taxPercentage"]}],"composicao":[],"regrasQueVivemNele":["RIR-IVA-INT","RIR-IVA-ISE","RIR-IVA-NOR","RIR-IVA-RED","RP-LIN-DESC","RP-LIN-NUMPOS","RP-TAXAIVA","RP-TAXAIVA-DEC","RP-TIPOIVA","RP-VALOR","RP-VALOR-DEC"],"usadoPor":["Linhas"]},
{"nivel":"USM","nome":"Medicao","descricao":"Leitura de um sensor: unidade, valor medido e instante da medição.","propriedades":[{"nome":"unidadeMedida","tipo":"texto","descricao":"Unidade de medida associada ao valor medido","nomesAlternativos":["unit"]},{"nome":"valor","tipo":"decimal","descricao":"Valor medido, na unidade indicada","nomesAlternativos":["value","reading"]},{"nome":"dataMedicao","tipo":"data","descricao":"Instante em que a medição foi feita (data e hora ISO 8601)","nomesAlternativos":["timestamp","measuredAt"]}],"composicao":[],"regrasQueVivemNele":["RIC-MED-DIFERIDA","RP-RELOGIO","RP-UNIDADE","RP-VALOR-FISICO"],"usadoPor":["Leitura"]},
{"nivel":"USM","nome":"Morada","descricao":"Morada postal: arruamento, código postal, localidade, freguesia e país.","propriedades":[{"nome":"rua","tipo":"texto","descricao":"Arruamento e número de porta"},{"nome":"codigoPostal","tipo":"texto","descricao":"Código postal da morada","nomesAlternativos":["zipCode","postalCode","CP"]},{"nome":"localidade","tipo":"texto","descricao":"Localidade da morada (em maiúsculas, sem acentos)"},{"nome":"freguesia","tipo":"texto","descricao":"Freguesia da morada (só para moradas em Lisboa)"},{"nome":"pais","tipo":"texto","descricao":"País da morada (código ISO de duas letras)","nomesAlternativos":["country","countryCode"]}],"composicao":[],"regrasQueVivemNele":["RIR-CP-ES","RIR-CP-GB","RIR-CP-LX-AJUDA","RIR-CP-LX-ALCANTARA","RIR-CP-LX-ALVALADE","RIR-CP-LX-AREEIRO","RIR-CP-LX-ARROIOS","RIR-CP-LX-AVENIDAS-NOVAS","RIR-CP-LX-BEATO","RIR-CP-LX-BELEM","RIR-CP-LX-BENFICA","RIR-CP-LX-CAMPO-DE-OURIQUE","RIR-CP-LX-CAMPOLIDE","RIR-CP-LX-CARNIDE","RIR-CP-LX-ESTRELA","RIR-CP-LX-LUMIAR","RIR-CP-LX-MARVILA","RIR-CP-LX-MISERICORDIA","RIR-CP-LX-OLIVAIS","RIR-CP-LX-PARQUE-DAS-NACOES","RIR-CP-LX-PENHA-DE-FRANCA","RIR-CP-LX-SANTA-CLARA","RIR-CP-LX-SANTA-MARIA-MAIOR","RIR-CP-LX-SANTO-ANTONIO","RIR-CP-LX-SAO-DOMINGOS-DE-BENFICA","RIR-CP-LX-SAO-VICENTE","RIR-CP-PT","RP-CP","RP-FREGUESIA","RP-PAIS"],"usadoPor":["Cliente","Emitente","Localizacao"]},
{"nivel":"SM","nome":"Cabecalho","descricao":"Cabeçalho do documento: identificação, série, tipo, data, total e encadeamento.","notas":"SM só com propriedades residuais (não compõe USM): o cabeçalho só faz sentido no documento fiscal.","propriedades":[{"nome":"numero","tipo":"texto","descricao":"Número do documento (série/sequência)","nomesAlternativos":["invoiceNo"]},{"nome":"serie","tipo":"texto","descricao":"Série do documento, comunicada à AT","nomesAlternativos":["series"]},{"nome":"atcud","tipo":"texto","descricao":"Código único do documento (ATCUD)","nomesAlternativos":["ATCUD"]},{"nome":"tipoDocumento","tipo":"texto","descricao":"Tipo de documento fiscal","nomesAlternativos":["invoiceType"]},{"nome":"dataEmissao","tipo":"data","descricao":"Data de emissão do documento","nomesAlternativos":["invoiceDate"]},{"nome":"totalFatura","tipo":"decimal","descricao":"Total do documento, em euros","nomesAlternativos":["grossTotal"]},{"nome":"hash","tipo":"texto","descricao":"Hash do documento, encadeado com o anterior da série","nomesAlternativos":["hashDocumento"]}],"composicao":[],"regrasQueVivemNele":["RIR-FS","RIR-FS-NUM","RP-ATCUD","RP-DATAEMISSAO","RP-HASH","RP-TIPODOC","RP-TOTAL"],"usadoPor":["Fatura"]},
{"nivel":"SM","nome":"Cliente","descricao":"Quem adquire os bens ou serviços (cliente comprador).","notas":"Na Secção ECM da tese corresponde ao 'SM Cliente Comprador', reutilizado pela Fatura e pela Ordem de Instalação.","propriedades":[{"nome":"consentimentoComercial","tipo":"booleano","descricao":"Consentimento do cliente para comunicações comerciais","nomesAlternativos":["marketingConsent"],"notas":"Propriedade residual: não é canónica (uma pessoa existe sem consentimento) nem é do HLM (é de quem compra)."}],"composicao":["USM Entidade [1..1]","USM Morada [1..1]"],"usadoPor":["Fatura","OrdemInstalacao"]},
{"nivel":"SM","nome":"Diagnostico","descricao":"Diagnóstico técnico do dispositivo.","propriedades":[],"composicao":["USM Diagnostico [1..1]"],"usadoPor":["Dispositivo"]},
{"nivel":"SM","nome":"Emitente","descricao":"Quem emite o documento: identificação, morada e contacto.","propriedades":[],"composicao":["USM Entidade [1..1]","USM Morada [1..1]","USM Contacto [1..1]"],"regrasQueVivemNele":["RIR-EMAIL-CX","RIR-EMAIL-CY"],"usadoPor":["Fatura"]},
{"nivel":"SM","nome":"Identificacao","descricao":"Identificação do dispositivo: identificador, fabricante, estado e grandeza medida.","notas":"SM só com propriedades residuais: a identificação do equipamento é informação própria do domínio IoT.","propriedades":[{"nome":"identificador","tipo":"texto","descricao":"Identificador do dispositivo","nomesAlternativos":["deviceId"]},{"nome":"fabricante","tipo":"texto","descricao":"Fabricante do dispositivo","nomesAlternativos":["manufacturer"]},{"nome":"estado","tipo":"texto","descricao":"Estado operacional do dispositivo","nomesAlternativos":["status"]},{"nome":"tipoDispositivo","tipo":"texto","descricao":"Grandeza medida pelo dispositivo","nomesAlternativos":["deviceType"]}],"composicao":[],"regrasQueVivemNele":["RP-ESTADO","RP-FABRICANTE","RP-IDENT","RP-TIPODISP"],"usadoPor":["Dispositivo"]},
{"nivel":"SM","nome":"Leitura","descricao":"Uma leitura: a medição, o local onde foi feita e, se existir, a assinatura da mensagem.","propriedades":[],"composicao":["USM Medicao [1..1]","USM Instalacao [1..1]","USM Assinatura [0..1]"],"usadoPor":["Dispositivo"]},
{"nivel":"SM","nome":"Linhas","descricao":"Coleção das linhas do documento.","notas":"SM que existe para reunir uma coleção: nome no plural; o elemento (USM Linha) no singular.","propriedades":[],"composicao":["USM Linha [1..*]"],"regrasQueVivemNele":["RP-LIN-MAX","RP-LIN-NUM","RP-LIN-SEQ"],"usadoPor":["Fatura"]},
{"nivel":"SM","nome":"Localizacao","descricao":"Localização de um equipamento: coordenadas, morada e indicação de acesso.","notas":"Na Secção ECM da tese corresponde ao 'SM Localização de Equipamento', reutilizado pelo Dispositivo e pela Ordem de Instalação.","propriedades":[{"nome":"indicacaoAcesso","tipo":"texto","descricao":"Indicação de acesso ao local (texto livre, ex.: portão lateral, chave no cofre)","nomesAlternativos":["accessNotes"],"notas":"Propriedade residual: só faz sentido porque a finalidade do SM é situar equipamento."}],"composicao":["USM InformacaoGeografica [1..1]","USM Morada [1..1]"],"regrasQueVivemNele":["RIR-LX-LOCALIDADE"],"usadoPor":["Dispositivo","OrdemInstalacao"]},
{"nivel":"SM","nome":"Pedido","descricao":"Dados do pedido de instalação: número e data.","propriedades":[{"nome":"numeroOrdem","tipo":"texto","descricao":"Número da ordem de instalação","nomesAlternativos":["orderId"]},{"nome":"dataPedido","tipo":"data","descricao":"Data em que a instalação foi pedida","nomesAlternativos":["requestDate"]}],"composicao":[],"regrasQueVivemNele":["RP-ORDEM-DATA","RP-ORDEM-NUM"],"usadoPor":["OrdemInstalacao"]}
]
```

### Funções e contextos externos
```json
{
 "funcoes": [
  {
   "nome": "assinaturaValida",
   "descricao": "Verdadeira quando a assinatura (HMAC-SHA256) corresponde à mensagem e à chave do dispositivo.",
   "parametros": [
    {
     "nome": "mensagem",
     "tipo": "texto",
     "papel": "alvo"
    },
    {
     "nome": "assinatura",
     "tipo": "texto",
     "papel": "alvo"
    }
   ],
   "contextosExternos": [
    "chaveDispositivo"
   ]
  },
  {
   "nome": "atcudValido",
   "descricao": "Verdadeira quando o ATCUD pertence a uma série comunicada à AT e corresponde ao seu código de validação.",
   "parametros": [
    {
     "nome": "atcud",
     "tipo": "texto",
     "papel": "alvo"
    },
    {
     "nome": "serie",
     "tipo": "texto",
     "papel": "alvo"
    }
   ],
   "contextosExternos": [
    "seriesComunicadasAT"
   ]
  },
  {
   "nome": "contagemInferiorA",
   "descricao": "Verdadeira quando a coleção tem menos de n instâncias.",
   "parametros": [
    {
     "nome": "instancias",
     "tipo": "modelo",
     "papel": "alvo",
     "colecao": true,
     "descricao": "Instâncias de um modelo composto com cardinalidade repetível."
    },
    {
     "nome": "n",
     "tipo": "inteiro",
     "papel": "parametro",
     "descricao": "Limite exclusivo do número de instâncias."
    }
   ],
   "contextosExternos": []
  },
  {
   "nome": "dentroDe",
   "descricao": "Verdadeira quando o ponto (latitude, longitude) está dentro da área, um polígono de vértices (latitude, longitude).",
   "parametros": [
    {
     "nome": "latitude",
     "tipo": "decimal",
     "papel": "alvo"
    },
    {
     "nome": "longitude",
     "tipo": "decimal",
     "papel": "alvo"
    },
    {
     "nome": "area",
     "tipo": "poligono",
     "papel": "parametro",
     "descricao": "Lista de vértices [latitude, longitude], declarada na regra."
    }
   ],
   "contextosExternos": []
  },
  {
   "nome": "desfasamentoInferiorA",
   "descricao": "Verdadeira quando o instante indicado não está adiantado mais de s segundos em relação ao relógio do servidor.",
   "parametros": [
    {
     "nome": "instante",
     "tipo": "data",
     "papel": "alvo",
     "descricao": "Instante da leitura (data e hora)."
    },
    {
     "nome": "s",
     "tipo": "inteiro",
     "papel": "parametro",
     "descricao": "Tolerância, em segundos."
    }
   ],
   "contextosExternos": [
    "relogioServidor"
   ]
  },
  {
   "nome": "digitoControloValido",
   "descricao": "Verdadeira quando o dígito de controlo (módulo 11) do NIF está correto.",
   "parametros": [
    {
     "nome": "nif",
     "tipo": "texto",
     "papel": "alvo"
    }
   ],
   "contextosExternos": []
  },
  {
   "nome": "excedeDiasDesdeHoje",
   "descricao": "Verdadeira quando passaram mais de n dias desde a data indicada até à data de hoje.",
   "parametros": [
    {
     "nome": "data",
     "tipo": "data",
     "papel": "alvo",
     "descricao": "Data a comparar com a data de hoje."
    },
    {
     "nome": "n",
     "tipo": "inteiro",
     "papel": "parametro",
     "descricao": "Número de dias."
    }
   ],
   "contextosExternos": [
    "dataDeHoje"
   ]
  },
  {
   "nome": "hashEncadeadoValido",
   "descricao": "Verdadeira quando o hash do documento deriva do número, da data, do total e do hash do documento anterior da série.",
   "parametros": [
    {
     "nome": "numero",
     "tipo": "texto",
     "papel": "alvo"
    },
    {
     "nome": "dataEmissao",
     "tipo": "data",
     "papel": "alvo"
    },
    {
     "nome": "totalFatura",
     "tipo": "decimal",
     "papel": "alvo"
    },
    {
     "nome": "hash",
     "tipo": "texto",
     "papel": "alvo"
    }
   ],
   "contextosExternos": [
    "hashAnterior"
   ]
  },
  {
   "nome": "naoPosteriorAHoje",
   "descricao": "Verdadeira quando a data indicada não é posterior à data de hoje.",
   "parametros": [
    {
     "nome": "data",
     "tipo": "data",
     "papel": "alvo",
     "descricao": "Data que não pode estar no futuro."
    }
   ],
   "contextosExternos": [
    "dataDeHoje"
   ]
  },
  {
   "nome": "somaIgualA",
   "descricao": "Verdadeira quando a soma dos valores da coleção, arredondada ao cêntimo, é igual ao total.",
   "parametros": [
    {
     "nome": "valores",
     "tipo": "lista<decimal>",
     "papel": "alvo",
     "colecao": true,
     "descricao": "Valores a somar."
    },
    {
     "nome": "total",
     "tipo": "decimal",
     "papel": "alvo",
     "descricao": "Total declarado."
    }
   ],
   "contextosExternos": []
  },
  {
   "nome": "valoresConsecutivos",
   "descricao": "Verdadeira quando os valores da coleção começam em 1 e não têm falhas.",
   "parametros": [
    {
     "nome": "valores",
     "tipo": "lista<inteiro>",
     "papel": "alvo",
     "colecao": true,
     "descricao": "Valores de uma propriedade em todas as instâncias da coleção."
    }
   ],
   "contextosExternos": []
  },
  {
   "nome": "valoresUnicos",
   "descricao": "Verdadeira quando nenhum valor da coleção se repete.",
   "parametros": [
    {
     "nome": "valores",
     "tipo": "lista<inteiro>",
     "papel": "alvo",
     "colecao": true,
     "descricao": "Valores de uma propriedade em todas as instâncias da coleção."
    }
   ],
   "contextosExternos": []
  }
 ],
 "contextosExternos": [
  {
   "nome": "chaveDispositivo",
   "tipo": "texto",
   "descricao": "Chave secreta com que cada dispositivo assina as suas mensagens (HMAC-SHA256).",
   "fonte": "Cofre de chaves da plataforma IoT, consultado pelo identificador do dispositivo."
  },
  {
   "nome": "dataDeHoje",
   "tipo": "data",
   "descricao": "Data atual no momento da avaliação (AAAA-MM-DD).",
   "fonte": "Relógio do motor de avaliação; pode ser fixada por um perfil para tornar a avaliação reprodutível."
  },
  {
   "nome": "hashAnterior",
   "tipo": "texto",
   "descricao": "Hash do último documento emitido na mesma série, que encadeia o documento atual.",
   "fonte": "Sistema de faturação do emitente."
  },
  {
   "nome": "relogioServidor",
   "tipo": "data",
   "descricao": "Instante atual do servidor que recebe as leituras (data e hora ISO 8601).",
   "fonte": "Relógio do servidor da plataforma IoT."
  },
  {
   "nome": "seriesComunicadasAT",
   "tipo": "texto",
   "descricao": "Séries de documentos comunicadas à AT, cada uma com o respetivo código de validação.",
   "fonte": "Portal das Finanças (AT), sincronizado pelo sistema de faturação."
  }
 ]
}
```

## Dados do domínio (utilizações, cenários, mapeamentos conhecidos)

```json
{}
```

## Declarações atuais do domínio

(ainda não há declarações)

## Notas de revisão

(nenhuma)

## Inventário (todas as fontes: grupos, elementos e regras)

### Fonte descricao-biblioteca: Biblioteca municipal: empréstimos e reservas (texto (linguagem natural))

Papel: descrição do domínio em linguagem natural: entidades, propriedades e regras

Texto da fonte, tal como está escrito:

# Biblioteca municipal: empréstimos e reservas

Uma biblioteca municipal regista as obras do seu catálogo, os exemplares de cada obra, os leitores, os empréstimos e as reservas. Os dados servem o balcão de atendimento (empréstimos e devoluções), o portal do leitor (reservas) e a troca de registos com a rede de bibliotecas do concelho.

## Obra

Uma obra é um título do catálogo, independente do número de exemplares.

- isbn (texto, opcional): número ISBN-13 da obra, sem hífenes. Deve ter 13 algarismos e começar por 978 ou 979.
- titulo (texto, obrigatório): título da obra.
- autores (texto, um ou mais): nome de cada autor, na forma "Apelido, Nome".
- anoEdicao (inteiro, opcional): ano da edição. Não pode ser posterior ao ano corrente.
- editora (texto, opcional): nome da editora.
- tipo (texto, obrigatório): tipo de obra. Valores: LIVRO, REVISTA, DVD, AUDIOLIVRO, MAPA.
- classificacao (texto, obrigatório): cota segundo a Classificação Decimal Universal, por exemplo 821.134.3-31.

Uma revista não tem ISBN; nesse caso o ISSN é obrigatório.

- issn (texto, opcional): número ISSN, na forma 0000-0000.

## Exemplar

Cada exemplar é uma cópia física de uma obra.

- codigoBarras (texto, obrigatório): código de barras do exemplar, com 10 algarismos.
- estado (texto, obrigatório): estado do exemplar. Valores: DISPONIVEL, EMPRESTADO, RESERVADO, EM_REPARACAO, ABATIDO.
- dataAquisicao (data, obrigatório): data em que o exemplar entrou na biblioteca.
- localizacao (texto, opcional): sala e estante.
- consultaLocal (booleano, obrigatório): verdadeiro quando o exemplar só pode ser consultado na biblioteca.

Um exemplar de consulta local nunca pode ser emprestado. Um exemplar abatido não pode ter empréstimos nem reservas.

## Leitor

- numeroLeitor (texto, obrigatório): número do cartão de leitor, na forma L seguido de 6 algarismos.
- nome (texto, obrigatório): nome completo.
- dataNascimento (data, obrigatório): data de nascimento.
- email (texto, opcional): endereço de correio eletrónico.
- telefone (texto, opcional): número de telefone com 9 algarismos.
- morada: rua, código postal, localidade e país.
- categoria (texto, obrigatório): categoria do leitor. Valores: ADULTO, JUVENIL, INFANTIL, SENIOR.
- dataValidade (data, obrigatório): data até à qual o cartão é válido.

O leitor tem de indicar pelo menos um contacto: o email ou o telefone. Um leitor com menos de 12 anos é da categoria INFANTIL e entre 12 e 17 anos é JUVENIL. Um leitor infantil ou juvenil tem de ter um responsável, com nome e contacto.

## Emprestimo

- numero (texto, obrigatório): número do empréstimo.
- dataEmprestimo (data, obrigatório): data em que o exemplar foi levantado.
- dataPrevistaDevolucao (data, obrigatório): data em que deve ser devolvido.
- dataDevolucao (data, opcional): data em que foi devolvido.
- renovacoes (inteiro, obrigatório): número de renovações já feitas.
- leitor e exemplar: o leitor que levou o exemplar.

A data prevista de devolução é posterior à data do empréstimo e no máximo 30 dias depois; para DVD o prazo é de 7 dias. A data de devolução, quando existe, não pode ser anterior à data do empréstimo. Um empréstimo pode ser renovado no máximo 2 vezes. O cartão do leitor tem de estar válido na data do empréstimo. Um leitor INFANTIL só pode ter 3 empréstimos em simultâneo; os outros, 6.

## Reserva

- dataReserva (data, obrigatório): data em que a reserva foi feita.
- estado (texto, obrigatório): Valores: ATIVA, SATISFEITA, CANCELADA, EXPIRADA.
- dataLimiteLevantamento (data, opcional): data até à qual o leitor pode levantar o exemplar.
- leitor e obra: quem reserva e o quê.

Uma reserva SATISFEITA tem de ter a data limite de levantamento, que é no máximo 5 dias depois de o exemplar ficar disponível. Só se reserva uma obra sem exemplares disponíveis.

## Troca com a rede de bibliotecas

Os registos enviados à rede levam a obra, os exemplares e o código da biblioteca, com 4 algarismos. O portal do leitor só mostra a obra e os exemplares disponíveis, sem dados dos leitores.

Grupos (6):
```json
[
{"id":"Obra","nome":"Obra","nomeOrigem":"Obra","descricao":"Uma obra é um título do catálogo, independente do número de exemplares.","elementos":["Obra.isbn","Obra.titulo","Obra.autores","Obra.anoedicao","Obra.editora","Obra.tipo","Obra.classificacao","Obra.issn"]},
{"id":"Exemplar","nome":"Exemplar","nomeOrigem":"Exemplar","descricao":"Cada exemplar é uma cópia física de uma obra.","elementos":["Exemplar.codigobarras","Exemplar.estado","Exemplar.dataaquisicao","Exemplar.localizacao","Exemplar.consultalocal"]},
{"id":"Leitor","nome":"Leitor","nomeOrigem":"Leitor","elementos":["Leitor.numeroleitor","Leitor.nome","Leitor.datanascimento","Leitor.email","Leitor.telefone","Leitor.morada","Leitor.categoria","Leitor.datavalidade"]},
{"id":"Emprestimo","nome":"Emprestimo","nomeOrigem":"Emprestimo","descricao":"para DVD o prazo é de 7 dias.","elementos":["Emprestimo.numero","Emprestimo.dataemprestimo","Emprestimo.dataprevistadevolucao","Emprestimo.datadevolucao","Emprestimo.renovacoes","Emprestimo.leitorEExemplar"]},
{"id":"Reserva","nome":"Reserva","nomeOrigem":"Reserva","elementos":["Reserva.datareserva","Reserva.estado","Reserva.datalimitelevantamento","Reserva.leitorEObra"]},
{"id":"TrocaComARedeDeBibliotecas","nome":"Troca com a rede de bibliotecas","nomeOrigem":"Troca com a rede de bibliotecas","descricao":"Os registos enviados à rede levam a obra, os exemplares e o código da biblioteca, com 4 algarismos."}
]
```

Elementos (31):
```json
[
{"id":"Obra.isbn","nome":"isbn","descricao":"número ISBN-13 da obra, sem hífenes. Deve ter 13 algarismos e começar por 978 ou 979.","tipo":"texto","tipoOrigem":"texto, opcional","cardinalidade":"0..1","grupo":"Obra"},
{"id":"Obra.titulo","nome":"titulo","descricao":"título da obra.","tipo":"texto","tipoOrigem":"texto, obrigatório","cardinalidade":"1..1","grupo":"Obra"},
{"id":"Obra.autores","nome":"autores","descricao":"nome de cada autor, na forma \"Apelido, Nome\".","tipo":"texto","tipoOrigem":"texto, um ou mais","cardinalidade":"1..n","grupo":"Obra"},
{"id":"Obra.anoedicao","nome":"anoEdicao","descricao":"ano da edição. Não pode ser posterior ao ano corrente.","tipo":"inteiro","tipoOrigem":"inteiro, opcional","cardinalidade":"0..1","grupo":"Obra"},
{"id":"Obra.editora","nome":"editora","descricao":"nome da editora.","tipo":"texto","tipoOrigem":"texto, opcional","cardinalidade":"0..1","grupo":"Obra"},
{"id":"Obra.tipo","descricao":"tipo de obra. Valores: LIVRO, REVISTA, DVD, AUDIOLIVRO, MAPA.","tipo":"texto","tipoOrigem":"texto, obrigatório","cardinalidade":"1..1","grupo":"Obra","valoresAdmitidos":["LIVRO","REVISTA","DVD","AUDIOLIVRO","MAPA"]},
{"id":"Obra.classificacao","nome":"classificacao","descricao":"cota segundo a Classificação Decimal Universal, por exemplo 821.134.3-31.","tipo":"texto","tipoOrigem":"texto, obrigatório","cardinalidade":"1..1","grupo":"Obra"},
{"id":"Obra.issn","nome":"issn","descricao":"número ISSN, na forma 0000-0000.","tipo":"texto","tipoOrigem":"texto, opcional","cardinalidade":"0..1","grupo":"Obra"},
{"id":"Exemplar.codigobarras","nome":"codigoBarras","descricao":"código de barras do exemplar, com 10 algarismos.","tipo":"texto","tipoOrigem":"texto, obrigatório","cardinalidade":"1..1","grupo":"Exemplar"},
{"id":"Exemplar.estado","descricao":"estado do exemplar. Valores: DISPONIVEL, EMPRESTADO, RESERVADO, EM_REPARACAO, ABATIDO.","tipo":"texto","tipoOrigem":"texto, obrigatório","cardinalidade":"1..1","grupo":"Exemplar","valoresAdmitidos":["DISPONIVEL","EMPRESTADO","RESERVADO","EM_REPARACAO","ABATIDO"]},
{"id":"Exemplar.dataaquisicao","nome":"dataAquisicao","descricao":"data em que o exemplar entrou na biblioteca.","tipo":"data","tipoOrigem":"data, obrigatório","cardinalidade":"1..1","grupo":"Exemplar"},
{"id":"Exemplar.localizacao","nome":"localizacao","descricao":"sala e estante.","tipo":"texto","tipoOrigem":"texto, opcional","cardinalidade":"0..1","grupo":"Exemplar"},
{"id":"Exemplar.consultalocal","nome":"consultaLocal","descricao":"verdadeiro quando o exemplar só pode ser consultado na biblioteca.","tipo":"booleano","tipoOrigem":"booleano, obrigatório","cardinalidade":"1..1","grupo":"Exemplar"},
{"id":"Leitor.numeroleitor","nome":"numeroLeitor","descricao":"número do cartão de leitor, na forma L seguido de 6 algarismos.","tipo":"texto","tipoOrigem":"texto, obrigatório","cardinalidade":"1..1","grupo":"Leitor"},
{"id":"Leitor.nome","descricao":"nome completo.","tipo":"texto","tipoOrigem":"texto, obrigatório","cardinalidade":"1..1","grupo":"Leitor"},
{"id":"Leitor.datanascimento","nome":"dataNascimento","descricao":"data de nascimento.","tipo":"data","tipoOrigem":"data, obrigatório","cardinalidade":"1..1","grupo":"Leitor"},
{"id":"Leitor.email","nome":"email","descricao":"endereço de correio eletrónico.","tipo":"texto","tipoOrigem":"texto, opcional","cardinalidade":"0..1","grupo":"Leitor"},
{"id":"Leitor.telefone","nome":"telefone","descricao":"número de telefone com 9 algarismos.","tipo":"texto","tipoOrigem":"texto, opcional","cardinalidade":"0..1","grupo":"Leitor"},
{"id":"Leitor.morada","nome":"morada","descricao":"rua, código postal, localidade e país.","grupo":"Leitor"},
{"id":"Leitor.categoria","descricao":"categoria do leitor. Valores: ADULTO, JUVENIL, INFANTIL, SENIOR.","tipo":"texto","tipoOrigem":"texto, obrigatório","cardinalidade":"1..1","grupo":"Leitor","valoresAdmitidos":["ADULTO","JUVENIL","INFANTIL","SENIOR"]},
{"id":"Leitor.datavalidade","nome":"dataValidade","descricao":"data até à qual o cartão é válido.","tipo":"data","tipoOrigem":"data, obrigatório","cardinalidade":"1..1","grupo":"Leitor"},
{"id":"Emprestimo.numero","nome":"numero","descricao":"número do empréstimo.","tipo":"texto","tipoOrigem":"texto, obrigatório","cardinalidade":"1..1","grupo":"Emprestimo"},
{"id":"Emprestimo.dataemprestimo","nome":"dataEmprestimo","descricao":"data em que o exemplar foi levantado.","tipo":"data","tipoOrigem":"data, obrigatório","cardinalidade":"1..1","grupo":"Emprestimo"},
{"id":"Emprestimo.dataprevistadevolucao","nome":"dataPrevistaDevolucao","descricao":"data em que deve ser devolvido.","tipo":"data","tipoOrigem":"data, obrigatório","cardinalidade":"1..1","grupo":"Emprestimo"},
{"id":"Emprestimo.datadevolucao","nome":"dataDevolucao","descricao":"data em que foi devolvido.","tipo":"data","tipoOrigem":"data, opcional","cardinalidade":"0..1","grupo":"Emprestimo"},
{"id":"Emprestimo.renovacoes","nome":"renovacoes","descricao":"número de renovações já feitas.","tipo":"inteiro","tipoOrigem":"inteiro, obrigatório","cardinalidade":"1..1","grupo":"Emprestimo"},
{"id":"Emprestimo.leitorEExemplar","nome":"leitor e exemplar","descricao":"o leitor que levou o exemplar.","grupo":"Emprestimo"},
{"id":"Reserva.datareserva","nome":"dataReserva","descricao":"data em que a reserva foi feita.","tipo":"data","tipoOrigem":"data, obrigatório","cardinalidade":"1..1","grupo":"Reserva"},
{"id":"Reserva.estado","nome":"estado","descricao":"Valores: ATIVA, SATISFEITA, CANCELADA, EXPIRADA.","tipo":"texto","tipoOrigem":"texto, obrigatório","cardinalidade":"1..1","grupo":"Reserva","valoresAdmitidos":["ATIVA","SATISFEITA","CANCELADA","EXPIRADA"]},
{"id":"Reserva.datalimitelevantamento","nome":"dataLimiteLevantamento","descricao":"data até à qual o leitor pode levantar o exemplar.","tipo":"data","tipoOrigem":"data, opcional","cardinalidade":"0..1","grupo":"Reserva"},
{"id":"Reserva.leitorEObra","nome":"leitor e obra","descricao":"quem reserva e o quê.","grupo":"Reserva"}
]
```

Regras (18):
```json
[
{"id":"T1","texto":"isbn: número ISBN-13 da obra, sem hífenes. Deve ter 13 algarismos e começar por 978 ou 979.","categoria":"outra","natureza":"?","contexto":"Obra","elementos":["Obra.isbn"]},
{"id":"T2","texto":"anoEdicao: ano da edição. Não pode ser posterior ao ano corrente.","categoria":"outra","natureza":"?","contexto":"Obra","elementos":["Obra.anoedicao"]},
{"id":"T3","texto":"nesse caso o ISSN é obrigatório.","categoria":"condicional","natureza":"RIR","contexto":"Obra"},
{"id":"T4","texto":"consultaLocal: verdadeiro quando o exemplar só pode ser consultado na biblioteca.","categoria":"condicional","natureza":"RIR","contexto":"Exemplar","elementos":["Exemplar.consultalocal"]},
{"id":"T5","texto":"Um exemplar de consulta local nunca pode ser emprestado.","categoria":"outra","natureza":"?","contexto":"Exemplar"},
{"id":"T6","texto":"Um exemplar abatido não pode ter empréstimos nem reservas.","categoria":"outra","natureza":"?","contexto":"Exemplar"},
{"id":"T7","texto":"O leitor tem de indicar pelo menos um contacto: o email ou o telefone.","categoria":"outra","natureza":"?","contexto":"Leitor"},
{"id":"T8","texto":"Um leitor com menos de 12 anos é da categoria INFANTIL e entre 12 e 17 anos é JUVENIL.","categoria":"gama","natureza":"RP","contexto":"Leitor"},
{"id":"T9","texto":"Um leitor infantil ou juvenil tem de ter um responsável, com nome e contacto.","categoria":"outra","natureza":"?","contexto":"Leitor"},
{"id":"T10","texto":"dataPrevistaDevolucao: data em que deve ser devolvido.","categoria":"outra","natureza":"?","contexto":"Emprestimo","elementos":["Emprestimo.dataprevistadevolucao"]},
{"id":"T11","texto":"A data prevista de devolução é posterior à data do empréstimo e no máximo 30 dias depois;","categoria":"cardinalidade","natureza":"RE","contexto":"Emprestimo"},
{"id":"T12","texto":"A data de devolução, quando existe, não pode ser anterior à data do empréstimo.","categoria":"condicional","natureza":"RIR","contexto":"Emprestimo"},
{"id":"T13","texto":"Um empréstimo pode ser renovado no máximo 2 vezes.","categoria":"cardinalidade","natureza":"RE","contexto":"Emprestimo"},
{"id":"T14","texto":"O cartão do leitor tem de estar válido na data do empréstimo.","categoria":"outra","natureza":"?","contexto":"Emprestimo"},
{"id":"T15","texto":"Um leitor INFANTIL só pode ter 3 empréstimos em simultâneo;","categoria":"outra","natureza":"?","contexto":"Emprestimo"},
{"id":"T16","texto":"Uma reserva SATISFEITA tem de ter a data limite de levantamento, que é no máximo 5 dias depois de o exemplar ficar disponível.","categoria":"cardinalidade","natureza":"RE","contexto":"Reserva"},
{"id":"T17","texto":"Só se reserva uma obra sem exemplares disponíveis.","categoria":"outra","natureza":"?","contexto":"Reserva"},
{"id":"T18","texto":"O portal do leitor só mostra a obra e os exemplares disponíveis, sem dados dos leitores.","categoria":"outra","natureza":"?","contexto":"TrocaComARedeDeBibliotecas"}
]
```

## Formato da resposta

Um objeto JSON com as declarações completas (uma por HLM, com todas as secções: contextosExternos, funcoes, usm, sm, hlm, projecoes, perfis), o mapeamento de cada elemento e de cada regra das fontes, e notas para a revisão.

```json
{
 "declaracoes": [
  {
   "declaracao": {
    "nome": "…",
    "versao": "0.1.0",
    "descricao": "…",
    "dominios": [
     "…"
    ],
    "hlm": "Fatura"
   },
   "contextosExternos": [],
   "funcoes": [],
   "usm": [],
   "sm": [],
   "hlm": [],
   "projecoes": [],
   "perfis": []
  }
 ],
 "mapeamento": [
  {
   "fonte": "cius-pt-guia",
   "origem": "BT-27",
   "decisao": "mapeado",
   "destino": "HLM:Fatura/Fornecedor.Entidade.nome",
   "nota": ""
  },
  {
   "fonte": "fm-dart",
   "origem": "Article.internalId",
   "decisao": "descartado",
   "motivo": "identificador técnico da aplicação"
  },
  {
   "fonte": "cius-pt-schematron",
   "origem": "BR-CO-10",
   "decisao": "mapeado",
   "destino": "Regra:RP-SOMA-LINHAS"
  }
 ],
 "notas": [
  "…o que a pessoa deve confirmar na revisão (decisões duvidosas, regras descartadas por falta de informação)"
 ]
}
```

Responde só com o JSON, sem texto à volta.
