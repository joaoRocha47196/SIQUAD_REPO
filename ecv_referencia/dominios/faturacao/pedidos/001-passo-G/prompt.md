# Papel

És um especialista em modelação de dados e em conhecimento de validação. Trabalhas com a ECV (Estratificação do Conhecimento de Validação): a ECM organiza a estrutura em HLM, SM e USM; a ECR organiza as regras pela natureza (RE, RP, RIR, RIC), pelo alcance (onde vivem) e pela expressividade (catálogo ou função). Produzes Declarações ECV a partir de fontes de dados existentes.

# Domínio

Faturação: Documentos de faturação em Portugal: fatura, nota de crédito, nota de débito e mensagem de estado segundo o CIUS-PT (modelo semântico EN 16931 e schematron da AT/eSPap), completados com as entidades de uma aplicação real de faturação e vendas (FM): clientes, vendedores, artigos, entregas e o desenho dos registos de exportação. As duas fontes usam-se em conjunto para um cenário completo: o CIUS-PT dá o modelo semântico e as regras legais; o FM dá a informação operacional (vendedores, zonas, stocks, entregas) e o formato de exportação.

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
{
 "utilizacoes": [
  "Emissão de fatura eletrónica CIUS-PT (tipo 380) para entidades públicas",
  "Emissão de nota de crédito (381), incluindo nota de crédito de rappel",
  "Emissão de nota de débito (383), fatura de adiantamento (386) e autofaturação (389)",
  "Mensagem de estado: resposta do adquirente a um documento recebido",
  "Exportação dos registos de vendas, clientes, vendedores e stocks da aplicação FM",
  "Entregas e encomendas da aplicação FM (documento de venda, guia de transporte)"
 ],
 "cenarios": [
  "Emissão em Portugal, em euros, por um fornecedor com NIF português",
  "Fatura isenta de IVA (motivo de isenção obrigatório)",
  "Nota de crédito que referencia a fatura original",
  "Exportação diária de um vendedor (série e prefixo ATCUD conhecidos)"
 ],
 "metainformacao": {
  "dominio": "faturação"
 }
}
```

## Declarações atuais do domínio

(ainda não há declarações)

## Notas de revisão

(nenhuma)

## Inventário (todas as fontes: grupos, elementos e regras)

### Fonte cius-pt-guia: Guia do modelo de dados semântico CIUS-PT (v1.1) (norma semântica)

Papel: modelo semântico: a estrutura principal (BG e BT), independente da sintaxe XML

Grupos (33):
```json
[
{"id":"BG-0","nome":"Documento de faturação","nomeOrigem":"INVOICE","descricao":"Raiz do modelo semântico: os campos sem grupo pertencem diretamente ao documento.","elementos":["BT-1","BT-2","BT-3","BT-5","BT-6","BT-7","BT-8","BT-9","BT-10","BT-11","BT-12","BT-13","BT-14","BT-15","BT-16","BT-17","BT-18","BT-19","BT-20"]},
{"id":"BG-1","nome":"Notas do Documento Faturação","nomeOrigem":"INVOICE NOTE","cardinalidade":"0..*","elementos":["BT-21","BT-22"]},
{"id":"BG-2","nome":"Controlo do Processo","nomeOrigem":"PROCESS CONTROL","cardinalidade":"1..1","elementos":["BT-23","BT-24"]},
{"id":"BG-3","nome":"Referência do Documento Relacionado","nomeOrigem":"PRECEDING INVOICE REFERENCE","cardinalidade":"0..*","elementos":["BT-25","BT-26"]},
{"id":"BG-4","nome":"Identificação do Fornecedor","nomeOrigem":"SELLER","cardinalidade":"1..1","elementos":["BT-27","BT-28","BT-29","BT-30","BT-31","BT-32","BT-33","BT-34"]},
{"id":"BG-5","nome":"Morada do Fornecedor","nomeOrigem":"SELLER POSTAL ADDRESS","cardinalidade":"1..1","elementos":["BT-35","BT-36","BT-162","BT-37","BT-38","BT-39","BT-40"]},
{"id":"BG-6","nome":"Contacto do Fornecedor","nomeOrigem":"SELLER CONTACT","cardinalidade":"0..1","elementos":["BT-41","BT-42","BT-43"]},
{"id":"BG-7","nome":"Identificação do Cliente","nomeOrigem":"BUYER","cardinalidade":"1..1","elementos":["BT-44","BT-45","BT-46","BT-47","BT-48","BT-49"]},
{"id":"BG-8","nome":"Morada do Cliente","nomeOrigem":"BUYER POSTAL ADDRESS","cardinalidade":"1..1","elementos":["BT-50","BT-51","BT-163","BT-52","BT-53","BT-54","BT-55"]},
{"id":"BG-9","nome":"Contacto do Cliente","nomeOrigem":"BUYER CONTACT","cardinalidade":"0..1","elementos":["BT-56","BT-57","BT-58"]},
{"id":"BG-10","nome":"Identificação do Recebedor do Pagamento","nomeOrigem":"PAYEE","cardinalidade":"0..1","elementos":["BT-59","BT-60","BT-61"]},
{"id":"BG-11","nome":"Identificação do Representante Legal do Fornecedor","nomeOrigem":"SELLER TAX REPRESENTATIVE PARTY","cardinalidade":"0..1","elementos":["BT-62","BT-63"]},
{"id":"BG-12","nome":"Morada do Representante Legal do Fornecedor","nomeOrigem":"SELLER TAX REPRESENTATIVE","cardinalidade":"1..1","elementos":["BT-64","BT-65","BT-164","BT-66","BT-67","BT-68","BT-69"]},
{"id":"BG-13","nome":"Local de Entrega","nomeOrigem":"DELIVERY INFORMATION","cardinalidade":"0..*","elementos":["BT-70","BT-71","BT-72"]},
{"id":"BG-14","nome":"Período de Faturação","nomeOrigem":"INVOICING PERIOD","cardinalidade":"0..1","elementos":["BT-73","BT-74"]},
{"id":"BG-15","nome":"Morada do Local de Entrega","nomeOrigem":"DELIVER TO ADDRESS","cardinalidade":"1..*","elementos":["BT-75","BT-76","BT-165","BT-77","BT-78","BT-79","BT-80"]},
{"id":"BG-16","nome":"Dados de Pagamento","nomeOrigem":"PAYMENT INSTRUCTIONS","cardinalidade":"0..1","elementos":["BT-81","BT-82","BT-83"]},
{"id":"BG-17","nome":"Dados de Pagamento - Informação de Transferência Bancária","nomeOrigem":"CREDIT TRANSFER","cardinalidade":"0..*","elementos":["BT-84","BT-85","BT-86"]},
{"id":"BG-18","nome":"Dados de Pagamento - Informação de Cartão Crédito","nomeOrigem":"PAYMENT CARD INFORMATION","cardinalidade":"0..1","elementos":["BT-87","BT-88"]},
{"id":"BG-19","nome":"Dados de Pagamento - Informação de Débito Direto","nomeOrigem":"DIRECT DEBIT","cardinalidade":"0..1","elementos":["BT-89","BT-90","BT-91"]},
{"id":"BG-20","nome":"Informação de Descontos do Documento","nomeOrigem":"DOCUMENT LEVEL ALLOWANCES","cardinalidade":"0..*","elementos":["BT-92","BT-93","BT-94","BT-95","BT-96","BT-97","BT-98"]},
{"id":"BG-21","nome":"Informação de Encargos do Documento","nomeOrigem":"DOCUMENT LEVEL CHARGES","cardinalidade":"0..*","elementos":["BT-99","BT-100","BT-101","BT-102","BT-103","BT-104","BT-105"]},
{"id":"BG-22","nome":"Totais do Documento","nomeOrigem":"DOCUMENT TOTALS","cardinalidade":"1..1","elementos":["BT-106","BT-107","BT-108","BT-109","BT-110","BT-111","BT-112","BT-113","BT-114","BT-115"]},
{"id":"BG-23","nome":"Informação de Impostos","nomeOrigem":"VAT BREAKDOWN","cardinalidade":"1..*","elementos":["BT-116","BT-117","BT-118","BT-119","BT-120","BT-121"]},
{"id":"BG-24","nome":"Documentos de Suporte","nomeOrigem":"ADDITIONAL SUPPORTING","cardinalidade":"0..*","elementos":["BT-122","BT-123","BT-124","BT-125"]},
{"id":"BG-25","nome":"Linha do Documento de Faturação","nomeOrigem":"INVOICE LINE","cardinalidade":"1..*","elementos":["BT-126","BT-127","BT-128","BT-129","BT-130","BT-131","BT-132","BT-133"]},
{"id":"BG-26","nome":"Linha do Documento de Faturação - Período","nomeOrigem":"INVOICE LINE PERIOD","cardinalidade":"0..1","elementos":["BT-134","BT-135"]},
{"id":"BG-27","nome":"Linha do Documento de Faturação - Descontos","nomeOrigem":"INVOICE LINE ALLOWANCES","cardinalidade":"0..*","elementos":["BT-136","BT-137","BT-138","BT-139","BT-140"]},
{"id":"BG-28","nome":"Linha do Documento de Faturação - Encargos","nomeOrigem":"INVOICE LINE CHARGES","cardinalidade":"0..*","elementos":["BT-141","BT-142","BT-143","BT-144","BT-145"]},
{"id":"BG-29","nome":"Linha do Documento de Faturação - Preço","nomeOrigem":"PRICE DETAILS","cardinalidade":"1..1","elementos":["BT-146","BT-147","BT-148","BT-149","BT-150"]},
{"id":"BG-30","nome":"Linha do Documento de Faturação - Impostos","nomeOrigem":"LINE VAT INFORMATION","cardinalidade":"1..1","elementos":["BT-151","BT-152"]},
{"id":"BG-31","nome":"Linha do Documento de Faturação - Detalhe do Bem/Serviço","nomeOrigem":"ITEM INFORMATION","cardinalidade":"1..1","elementos":["BT-153","BT-154","BT-155","BT-156","BT-157","BT-158","BT-159"]},
{"id":"BG-32","nome":"Linha do Documento de Faturação - Propriedades adicionais","nomeOrigem":"ITEM ATTRIBUTES","cardinalidade":"0..*","elementos":["BT-160","BT-161"]}
]
```

Elementos (164):
```json
[
{"id":"BT-1","descricao":"Número de referência do documento, emitido pelo fornecedor.","tipo":"texto","tipoOrigem":"I","cardinalidade":"1..1","grupo":"BG-0","nomesAlternativos":["Invoice number"]},
{"id":"BT-2","descricao":"Data de emissão do documento.","tipo":"data","tipoOrigem":"D","cardinalidade":"1..1","grupo":"BG-0","nomesAlternativos":["Invoice issue date"]},
{"id":"BT-3","descricao":"Código que identifica o tipo funcional do documento.","tipo":"texto","tipoOrigem":"C","cardinalidade":"1..1","grupo":"BG-0","nomesAlternativos":["Invoice type code"],"valoresAdmitidos":["380","381","383","386","389"]},
{"id":"BT-5","descricao":"Moeda na qual os montantes constantes no documento estão indicados.","tipo":"texto","tipoOrigem":"C","cardinalidade":"1..1","grupo":"BG-0","nomesAlternativos":["Invoice currency code"]},
{"id":"BT-6","descricao":"A moeda usada para fins de contabilidade e relatórios de IVA, conforme aceite ou exigida no país do vendedor.","tipo":"texto","tipoOrigem":"C","cardinalidade":"0..1","grupo":"BG-0"},
{"id":"BT-7","descricao":"A data em que o IVA se torna aplicável para o Vendedor e para o Comprador na medida em que essa data pode ser determinada e difere da data de emissão da fatura, de acordo com a diretiva do IVA","tipo":"data","tipoOrigem":"D","cardinalidade":"0..1","grupo":"BG-0","nomesAlternativos":["Value added tax point date"]},
{"id":"BT-8","descricao":"O código da data em que o IVA se torna aplicável pelo vendedor e pelo comprador.","tipo":"texto","tipoOrigem":"C","cardinalidade":"0..1","grupo":"BG-0","nomesAlternativos":["Value added tax point date code"],"valoresAdmitidos":["3","35","432"]},
{"id":"BT-9","descricao":"Data de vencimento do documento.","tipo":"data","tipoOrigem":"D","cardinalidade":"0..1","grupo":"BG-0","nomesAlternativos":["Payment due date"]},
{"id":"BT-10","descricao":"Referência do Cliente","tipo":"texto","tipoOrigem":"I","cardinalidade":"0..1","grupo":"BG-0"},
{"id":"BT-11","descricao":"Número do Projeto","tipo":"texto","tipoOrigem":"I","cardinalidade":"0..1","grupo":"BG-0","nomesAlternativos":["Project reference"]},
{"id":"BT-12","descricao":"Número do contrato.","tipo":"texto","tipoOrigem":"O","cardinalidade":"0..1","grupo":"BG-0","nomesAlternativos":["Contract reference"]},
{"id":"BT-13","descricao":"Número da nota de encomenda.","tipo":"texto","tipoOrigem":"O","cardinalidade":"0..1","grupo":"BG-0","nomesAlternativos":["Purchase order reference"]},
{"id":"BT-14","descricao":"Número da ordem de venda, emitida pelo fornecedor.","tipo":"texto","tipoOrigem":"O","cardinalidade":"0..1","grupo":"BG-0","nomesAlternativos":["Sales order reference"]},
{"id":"BT-15","descricao":"Número do aviso de recebimento referenciado.","tipo":"texto","tipoOrigem":"O","cardinalidade":"0..1","grupo":"BG-0","nomesAlternativos":["Receiving advice reference"]},
{"id":"BT-16","descricao":"Referência do aviso de envio.","tipo":"texto","tipoOrigem":"O","cardinalidade":"0..1","grupo":"BG-0","nomesAlternativos":["Despatch advice reference"]},
{"id":"BT-17","descricao":"Número do acordo quadro.","tipo":"texto","tipoOrigem":"O","cardinalidade":"0..1","grupo":"BG-0"},
{"id":"BT-18","descricao":"Identificador do processo de registo de entrada do documento. Tipificação do identificador do processo de registo de entrada do documento.","tipo":"texto","tipoOrigem":"I","cardinalidade":"0..1","grupo":"BG-0"},
{"id":"BT-19","descricao":"Número do compromisso.","tipo":"texto","tipoOrigem":"I","cardinalidade":"0..1","grupo":"BG-0"},
{"id":"BT-20","descricao":"Descritivo das condições de pagamento.","tipo":"texto","tipoOrigem":"T","cardinalidade":"0..*","grupo":"BG-0","nomesAlternativos":["Payment terms"]},
{"id":"BT-21","descricao":"Assunto da nota.","tipo":"texto","tipoOrigem":"C","cardinalidade":"0..1","grupo":"BG-1"},
{"id":"BT-22","descricao":"Nota textual, que permite ao fornecedor enviar informação não estruturada relativa ao documento. Tipo da propriedade adicional do documento(name)./Valor da propriedade adicional do documento(value).","tipo":"texto","tipoOrigem":"T","cardinalidade":"1..1","grupo":"BG-1"},
{"id":"BT-23","descricao":"Tipo de Processo de Negócio","tipo":"texto","tipoOrigem":"I","cardinalidade":"0..1","grupo":"BG-2"},
{"id":"BT-24","descricao":"Nome da customização CIUS-PT. Permite ao recetor aplicar a validação do documento de acordo com as regras da sua customização.","tipo":"texto","tipoOrigem":"I","cardinalidade":"1..1","grupo":"BG-2","nomesAlternativos":["Specification identifier"]},
{"id":"BT-25","descricao":"Número de referência do documento, emitido pelo fornecedor, anteriormente enviado.","tipo":"texto","tipoOrigem":"I","cardinalidade":"1..1","grupo":"BG-3","nomesAlternativos":["Preceding Invoice reference"]},
{"id":"BT-26","descricao":"Data de emissão do documento, anteriormente enviado.","tipo":"data","tipoOrigem":"D","cardinalidade":"0..1","grupo":"BG-3"},
{"id":"BT-27","descricao":"O nome formal completo pelo qual o fornecedor está registrado no registo nacional de pessoas jurídicas ou como sujeito passivo ou, de outra forma, negocia como pessoa ou pessoas.","tipo":"texto","tipoOrigem":"T","cardinalidade":"1..1","grupo":"BG-4","nomesAlternativos":["Seller name"]},
{"id":"BT-28","descricao":"Nome comercial do fornecedor.","tipo":"texto","tipoOrigem":"T","cardinalidade":"0..1","grupo":"BG-4","nomesAlternativos":["Seller trading name"]},
{"id":"BT-29","descricao":"Identificação do vendedor (ID Bancário) Tipificação da identificação do vendedor.","tipo":"texto","tipoOrigem":"I","cardinalidade":"0..*","grupo":"BG-4","nomesAlternativos":["Seller identifier"]},
{"id":"BT-30","descricao":"Informação sobre o registo na conservatória. Tipificação da informação sobre o registo na conservatória.","tipo":"texto","tipoOrigem":"T","cardinalidade":"0..1","grupo":"BG-4","nomesAlternativos":["Seller legal registration identifier"]},
{"id":"BT-31","descricao":"Número de identificação fiscal do fornecedor.","tipo":"texto","tipoOrigem":"I","cardinalidade":"1..1","grupo":"BG-4","nomesAlternativos":["Seller VAT Identifier"]},
{"id":"BT-32","descricao":"Identificação do local do fornecedor (definida pelo endereço do fornecedor) para fins fiscais ou uma referência que permita ao fornecedor declarar seu status fiscal registado.","tipo":"texto","tipoOrigem":"I","cardinalidade":"0..1","grupo":"BG-4","nomesAlternativos":["Seller tax registration identifier"]},
{"id":"BT-33","descricao":"Informação sobre o capital social.","tipo":"texto","tipoOrigem":"T","cardinalidade":"0..1","grupo":"BG-4"},
{"id":"BT-34","descricao":"Endereço eletrónico do fornecedor. Tipificação do endereço eletrónico do fornecedor.","tipo":"texto","tipoOrigem":"I","cardinalidade":"0..1","grupo":"BG-4","nomesAlternativos":["Seller electronic address"]},
{"id":"BT-35","descricao":"Linha 1 da morada do fornecedor.","tipo":"texto","tipoOrigem":"T","cardinalidade":"1..1","grupo":"BG-5","nomesAlternativos":["Seller address line"]},
{"id":"BT-36","descricao":"Linha 2 da morada do fornecedor.","tipo":"texto","tipoOrigem":"T","cardinalidade":"0..1","grupo":"BG-5"},
{"id":"BT-37","descricao":"Cidade da morada do fornecedor.","tipo":"texto","tipoOrigem":"T","cardinalidade":"1..1","grupo":"BG-5","nomesAlternativos":["Seller city"]},
{"id":"BT-38","descricao":"Código postal da morada do fornecedor.","tipo":"texto","tipoOrigem":"T","cardinalidade":"1..1","grupo":"BG-5","nomesAlternativos":["Seller post code"]},
{"id":"BT-39","descricao":"Região/Província da morada do fornecedor.","tipo":"texto","tipoOrigem":"T","cardinalidade":"0..1","grupo":"BG-5"},
{"id":"BT-40","descricao":"Código identificador do país da morada do fornecedor.","tipo":"texto","tipoOrigem":"C","cardinalidade":"1..1","grupo":"BG-5","nomesAlternativos":["Seller country code"]},
{"id":"BT-41","descricao":"Ponto de contato do fornecedor.","tipo":"texto","tipoOrigem":"T","cardinalidade":"0..1","grupo":"BG-6","nomesAlternativos":["Seller contact point"]},
{"id":"BT-42","descricao":"Contacto telefónico do fornecedor.","tipo":"texto","tipoOrigem":"T","cardinalidade":"0..1","grupo":"BG-6","nomesAlternativos":["Seller contact telephone number"]},
{"id":"BT-43","descricao":"Correio eletrónico do fornecedor.","tipo":"texto","tipoOrigem":"T","cardinalidade":"0..1","grupo":"BG-6","nomesAlternativos":["Seller contact email address"]},
{"id":"BT-44","descricao":"Nome do cliente.","tipo":"texto","tipoOrigem":"T","cardinalidade":"1..1","grupo":"BG-7","nomesAlternativos":["Buyer name"]},
{"id":"BT-45","descricao":"Nome comercial do cliente.","tipo":"texto","tipoOrigem":"T","cardinalidade":"0..1","grupo":"BG-7","nomesAlternativos":["Buyer trading name"]},
{"id":"BT-46","descricao":"Identificador do cliente. Tipificação do identificador do cliente.","tipo":"texto","tipoOrigem":"I","cardinalidade":"0..1","grupo":"BG-7","nomesAlternativos":["Buyer identifier"]},
{"id":"BT-47","descricao":"Informação sobre o registo na conservatória do cliente. Tipificação da informação sobre o registo na conservatória do cliente.","tipo":"texto","tipoOrigem":"I","cardinalidade":"0..1","grupo":"BG-7"},
{"id":"BT-48","descricao":"Número de identificação fiscal do cliente.","tipo":"texto","tipoOrigem":"I","cardinalidade":"1..1","grupo":"BG-7","nomesAlternativos":["Buyer VAT identifier"]},
{"id":"BT-49","descricao":"Endereço eletrónico do cliente. Tipificação do endereço eletrónico do cliente.","tipo":"texto","tipoOrigem":"I","cardinalidade":"0..1","grupo":"BG-7","nomesAlternativos":["Buyer electronic address"]},
{"id":"BT-50","descricao":"Linha 1 da morada do cliente.","tipo":"texto","tipoOrigem":"T","cardinalidade":"0..1","grupo":"BG-8"},
{"id":"BT-51","descricao":"Linha 2 da morada do cliente.","tipo":"texto","tipoOrigem":"T","cardinalidade":"0..1","grupo":"BG-8"},
{"id":"BT-52","descricao":"Cidade da morada do cliente.","tipo":"texto","tipoOrigem":"T","cardinalidade":"0..1","grupo":"BG-8"},
{"id":"BT-53","descricao":"Código postal da morada do cliente.","tipo":"texto","tipoOrigem":"T","cardinalidade":"0..1","grupo":"BG-8"},
{"id":"BT-54","descricao":"Região/Província da morada do cliente.","tipo":"texto","tipoOrigem":"T","cardinalidade":"0..1","grupo":"BG-8"},
{"id":"BT-55","descricao":"Código identificador do país da morada do cliente.","tipo":"texto","tipoOrigem":"C","cardinalidade":"1..1","grupo":"BG-8","nomesAlternativos":["Buyer country code"]},
{"id":"BT-56","descricao":"Ponto de contato do cliente.","tipo":"texto","tipoOrigem":"T","cardinalidade":"0..1","grupo":"BG-9","nomesAlternativos":["Buyer contact point"]},
{"id":"BT-57","descricao":"Contacto telefónico do cliente.","tipo":"texto","tipoOrigem":"T","cardinalidade":"0..1","grupo":"BG-9","nomesAlternativos":["Buyer contact telephone number"]},
{"id":"BT-58","descricao":"Correio eletrónico do cliente.","tipo":"texto","tipoOrigem":"T","cardinalidade":"0..1","grupo":"BG-9","nomesAlternativos":["Buyer contact email address"]},
{"id":"BT-59","descricao":"Nome da entidade que recebe o pagamento.","tipo":"texto","tipoOrigem":"T","cardinalidade":"1..1","grupo":"BG-10","nomesAlternativos":["Payee name"]},
{"id":"BT-60","descricao":"Identificador do recebedor do pagamento.","tipo":"texto","tipoOrigem":"I","cardinalidade":"0..1","grupo":"BG-10","nomesAlternativos":["Payee identifier"]},
{"id":"BT-61","descricao":"Informação sobre o registo na conservatória do recebedor do pagamento. Tipificação da informação sobre o registo na conservatória do recebedor do pagamento.","tipo":"texto","tipoOrigem":"I","cardinalidade":"0..1","grupo":"BG-10","nomesAlternativos":["Payee legal registration identifier"]},
{"id":"BT-62","descricao":"Nome do representante legal para os temas fiscais.","tipo":"texto","tipoOrigem":"T","cardinalidade":"1..1","grupo":"BG-11","nomesAlternativos":["Seller tax representative name"]},
{"id":"BT-63","descricao":"Número de identificação fiscal do representante legal para os temas fiscais.","tipo":"texto","tipoOrigem":"I","cardinalidade":"1..1","grupo":"BG-11","nomesAlternativos":["Seller tax representative VAT identifier"]},
{"id":"BT-64","descricao":"Linha 1 da morada do representante legal para os temas fiscais.","tipo":"texto","tipoOrigem":"T","cardinalidade":"0..1","grupo":"BG-12"},
{"id":"BT-65","descricao":"Linha 2 da morada do representante legal para os temas fiscais.","tipo":"texto","tipoOrigem":"T","cardinalidade":"0..1","grupo":"BG-12"},
{"id":"BT-66","descricao":"Cidade da morada do representante legal para os temas fiscais.","tipo":"texto","tipoOrigem":"T","cardinalidade":"0..1","grupo":"BG-12"},
{"id":"BT-67","descricao":"Código postal da morada do representante legal para os temas fiscais.","tipo":"texto","tipoOrigem":"T","cardinalidade":"0..1","grupo":"BG-12"},
{"id":"BT-68","descricao":"Região/Província da morada do representante legal para os temas fiscais.","tipo":"texto","tipoOrigem":"T","cardinalidade":"0..1","grupo":"BG-12"},
{"id":"BT-69","descricao":"Código identificador do país da morada do representante legal para os temas fiscais.","tipo":"texto","tipoOrigem":"C","cardinalidade":"1..1","grupo":"BG-12","nomesAlternativos":["Tax representative country code"]},
{"id":"BT-70","descricao":"Nome do local de entrega.","tipo":"texto","tipoOrigem":"T","cardinalidade":"0..1","grupo":"BG-13"},
{"id":"BT-71","descricao":"Identificador do local em que os bens e serviços são entregues.","tipo":"texto","tipoOrigem":"I","cardinalidade":"0..1","grupo":"BG-13"},
{"id":"BT-72","descricao":"Data da entrega.","tipo":"data","tipoOrigem":"D","cardinalidade":"0..1","grupo":"BG-13","nomesAlternativos":["Actual delivery date"]},
{"id":"BT-73","descricao":"A data em que o período de faturação começa.","tipo":"data","tipoOrigem":"D","cardinalidade":"0..1","grupo":"BG-14","nomesAlternativos":["Invoicing period start date"]},
{"id":"BT-74","descricao":"A data em que o período de faturação acaba.","tipo":"data","tipoOrigem":"D","cardinalidade":"0..1","grupo":"BG-14","nomesAlternativos":["Invoicing period end date"]},
{"id":"BT-75","descricao":"Linha 1 da morada do local de entrega.","tipo":"texto","tipoOrigem":"T","cardinalidade":"1..1","grupo":"BG-15","nomesAlternativos":["Seller address line"]},
{"id":"BT-76","descricao":"Linha 2 da morada do local de entrega.","tipo":"texto","tipoOrigem":"T","cardinalidade":"0..1","grupo":"BG-15"},
{"id":"BT-77","descricao":"Cidade da morada do local de entrega.","tipo":"texto","tipoOrigem":"T","cardinalidade":"1..1","grupo":"BG-15","nomesAlternativos":["Seller city"]},
{"id":"BT-78","descricao":"Código postal da morada do local de entrega.","tipo":"texto","tipoOrigem":"T","cardinalidade":"1..1","grupo":"BG-15","nomesAlternativos":["Seller post code"]},
{"id":"BT-79","descricao":"Região/Província da morada do local de entrega.","tipo":"texto","tipoOrigem":"T","cardinalidade":"0..1","grupo":"BG-15"},
{"id":"BT-80","descricao":"Código identificador do país da morada do local de entrega.","tipo":"texto","tipoOrigem":"C","cardinalidade":"1..1","grupo":"BG-15"},
{"id":"BT-81","descricao":"Código identificador do método de pagamento.","tipo":"texto","tipoOrigem":"T","cardinalidade":"1..1","grupo":"BG-16","nomesAlternativos":["Payment means type code"]},
{"id":"BT-82","descricao":"Descrição do detalhe de pagamento do documento por ATM.","tipo":"texto","tipoOrigem":"T","cardinalidade":"0..1","grupo":"BG-16"},
{"id":"BT-83","descricao":"Descrição da referência a pagamento do documento por ATM. Descrição da referência a pagamento do documento por DUC.","tipo":"texto","tipoOrigem":"T","cardinalidade":"0..1","grupo":"BG-16"},
{"id":"BT-84","descricao":"Identificador do pagamento, código IBAN.","tipo":"texto","tipoOrigem":"I","cardinalidade":"1..1","grupo":"BG-17","nomesAlternativos":["Payment account identifier"]},
{"id":"BT-85","descricao":"Identificação da conta, para a qual o pagamento deve ser efetuado.","tipo":"texto","tipoOrigem":"T","cardinalidade":"0..1","grupo":"BG-17","nomesAlternativos":["Payment account name"]},
{"id":"BT-86","descricao":"Código da instituição bancária, código SWIFT.","tipo":"texto","tipoOrigem":"I","cardinalidade":"0..1","grupo":"BG-17","nomesAlternativos":["Payment service provider identifier"]},
{"id":"BT-87","descricao":"Número da conta principal do cartão utilizado no pagamento, PAN.","tipo":"texto","tipoOrigem":"T","cardinalidade":"1..1","grupo":"BG-18","nomesAlternativos":["Payment card primary account number"]},
{"id":"BT-88","descricao":"Nome do titular do cartão de pagamento.","tipo":"texto","tipoOrigem":"T","cardinalidade":"0..1","grupo":"BG-18"},
{"id":"BT-89","descricao":"Identificador exclusivo atribuído pelo Beneficiário para referenciar o mandato de débito direto (Nº Mandato).","tipo":"texto","tipoOrigem":"I","cardinalidade":"0..1","grupo":"BG-19","nomesAlternativos":["Mandate reference identifier"]},
{"id":"BT-90","descricao":"Identificador do credor designado pelo banco.","tipo":"texto","tipoOrigem":"I","cardinalidade":"0..1","grupo":"BG-19","nomesAlternativos":["Bank assigned creditor identifier"]},
{"id":"BT-91","descricao":"A conta a ser debitada pelo débito direto.","tipo":"texto","tipoOrigem":"I","cardinalidade":"0..1","grupo":"BG-19","nomesAlternativos":["Debited account identifier"]},
{"id":"BT-92","descricao":"Montante do desconto, sem impostos.","tipo":"decimal","tipoOrigem":"A","cardinalidade":"1..1","grupo":"BG-20","nomesAlternativos":["Document level allowance amount"]},
{"id":"BT-93","descricao":"Montante base do desconto.","tipo":"decimal","tipoOrigem":"A","cardinalidade":"0..1","grupo":"BG-20","nomesAlternativos":["Document level allowance base amount"]},
{"id":"BT-94","descricao":"Fator multiplicador sobre o montante base do desconto.","tipo":"decimal","tipoOrigem":"P","cardinalidade":"0..1","grupo":"BG-20","nomesAlternativos":["Document level allowance percentage"]},
{"id":"BT-95","descricao":"Código de imposto aplicado ao desconto.","tipo":"texto","tipoOrigem":"C","cardinalidade":"1..1","grupo":"BG-20","nomesAlternativos":["Document level allowance VAT category code"],"valoresAdmitidos":["AA","S","E","RED","INT","NOR","ISE","OUT","NA","Z","AE","IC","G e O"]},
{"id":"BT-96","descricao":"Percentagem de imposto aplicada ao desconto.","tipo":"decimal","tipoOrigem":"P","cardinalidade":"1..1","grupo":"BG-20","nomesAlternativos":["Document level allowance VAT rate"]},
{"id":"BT-97","descricao":"Representação textual do desconto.","tipo":"texto","tipoOrigem":"T","cardinalidade":"0..1","grupo":"BG-20","nomesAlternativos":["Document level allowance reason"]},
{"id":"BT-98","descricao":"Código do motivo, que possa levar a que o montante contemplado no desconto, esteja isento de imposto.","tipo":"texto","tipoOrigem":"C","cardinalidade":"0..1","grupo":"BG-20","nomesAlternativos":["Document level allowance reason code"]},
{"id":"BT-99","descricao":"Montante do encargo.","tipo":"decimal","tipoOrigem":"A","cardinalidade":"1..1","grupo":"BG-21","nomesAlternativos":["Document level charge amount"]},
{"id":"BT-100","descricao":"Montante base do encargo.","tipo":"decimal","tipoOrigem":"A","cardinalidade":"0..1","grupo":"BG-21","nomesAlternativos":["Document level charge base amount"]},
{"id":"BT-101","descricao":"Fator multiplicador sobre o montante base do encargo.","tipo":"decimal","tipoOrigem":"P","cardinalidade":"0..1","grupo":"BG-21","nomesAlternativos":["Document level charge percentage"]},
{"id":"BT-102","descricao":"Código de imposto aplicado ao encargo.","tipo":"texto","tipoOrigem":"C","cardinalidade":"1..1","grupo":"BG-21","nomesAlternativos":["Document level charge VAT category code"],"valoresAdmitidos":["AA","S","E"]},
{"id":"BT-103","descricao":"Percentagem de imposto aplicada ao encargo.","tipo":"decimal","tipoOrigem":"P","cardinalidade":"1..1","grupo":"BG-21","nomesAlternativos":["Document level charge VAT rate"]},
{"id":"BT-104","descricao":"Representação textual do encargo.","tipo":"texto","tipoOrigem":"T","cardinalidade":"0..1","grupo":"BG-21","nomesAlternativos":["Document level charge reason"]},
{"id":"BT-105","descricao":"Código do motivo, que possa levar a que o montante contemplado no encargo, esteja isento de imposto.","tipo":"texto","tipoOrigem":"C","cardinalidade":"0..1","grupo":"BG-21","nomesAlternativos":["Document level charge reason code"]},
{"id":"BT-106","descricao":"Soma dos montantes das linhas do documento (s/imposto).","tipo":"decimal","tipoOrigem":"A","cardinalidade":"1..1","grupo":"BG-22","nomesAlternativos":["Sum of Invoice line net amount"]},
{"id":"BT-107","descricao":"Total de descontos aplicados no documento.","tipo":"decimal","tipoOrigem":"A","cardinalidade":"0..1","grupo":"BG-22"},
{"id":"BT-108","descricao":"Total de encargos aplicados no documento.","tipo":"decimal","tipoOrigem":"A","cardinalidade":"0..1","grupo":"BG-22"},
{"id":"BT-109","descricao":"Total do documento (s/imposto).","tipo":"decimal","tipoOrigem":"A","cardinalidade":"1..1","grupo":"BG-22","nomesAlternativos":["Invoice total amount without VAT"]},
{"id":"BT-110","descricao":"Total de imposto.","tipo":"decimal","tipoOrigem":"A","cardinalidade":"1..1","grupo":"BG-22","nomesAlternativos":["Total VAT amount"]},
{"id":"BT-111","descricao":"Total do IVA expresso na moeda aceite ou exigida no país do Fornecedor","tipo":"decimal","tipoOrigem":"A","cardinalidade":"0..1","grupo":"BG-22"},
{"id":"BT-112","descricao":"Total do documento (c/imposto).","tipo":"decimal","tipoOrigem":"A","cardinalidade":"1..1","grupo":"BG-22","nomesAlternativos":["VAT"]},
{"id":"BT-113","descricao":"Valor pago à-priori. O documento pode conter a soma de todos os montantes pré-pagos, que devem ser deduzidos do pagamento.","tipo":"decimal","tipoOrigem":"A","cardinalidade":"0..1","grupo":"BG-22","nomesAlternativos":["VAT BT- Paid amount"]},
{"id":"BT-114","descricao":"Montante de arredondamento aplicado ao total do documento c/imposto","tipo":"decimal","tipoOrigem":"A","cardinalidade":"0..1","grupo":"BG-22","nomesAlternativos":["VAT BT- Paid amount BT- Rounding amount"]},
{"id":"BT-115","descricao":"Valor a pagar. / Montante a pagamento do ATM. / Montante a pagamento do DUC.","tipo":"decimal","tipoOrigem":"A","cardinalidade":"1..1","grupo":"BG-22","nomesAlternativos":["Amount due for payment"]},
{"id":"BT-116","descricao":"Montante base de incidência para a taxa de imposto aplicada no respetivo subtotal.","tipo":"decimal","tipoOrigem":"A","cardinalidade":"1..1","grupo":"BG-23","nomesAlternativos":["VAT category taxable amount"]},
{"id":"BT-117","descricao":"Montante calculado do imposto sobre o montante base de incidência respetivo.","tipo":"decimal","tipoOrigem":"A","cardinalidade":"1..1","grupo":"BG-23","nomesAlternativos":["VAT category tax amount"]},
{"id":"BT-118","descricao":"Código de imposto respeitante à taxa aplicada no subtotal.","tipo":"texto","tipoOrigem":"C","cardinalidade":"1..1","grupo":"BG-23","nomesAlternativos":["VAT category code"],"valoresAdmitidos":["AA","S","E","RED","INT","NOR","ISE","OUT","NA","Z","AE","IC","G e O"]},
{"id":"BT-119","descricao":"Percentagem de imposto do subtotal.","tipo":"decimal","tipoOrigem":"P","cardinalidade":"1..1","grupo":"BG-23","nomesAlternativos":["VAT category rate"]},
{"id":"BT-120","descricao":"Descrição textual do motivo, que possa levar a que o montante contemplado no subtotal, respetivo, esteja isento de imposto.","tipo":"texto","tipoOrigem":"T","cardinalidade":"0..1","grupo":"BG-23","nomesAlternativos":["VAT exemption reason text"]},
{"id":"BT-121","descricao":"Código do motivo, que possa levar a que o montante contemplado no subtotal, respetivo, esteja isento de imposto.","tipo":"texto","tipoOrigem":"C","cardinalidade":"0..1","grupo":"BG-23","nomesAlternativos":["VAT exemption reason code"]},
{"id":"BT-122","descricao":"Identificador do anexo referenciado.","tipo":"texto","tipoOrigem":"T","cardinalidade":"1..1","grupo":"BG-24","nomesAlternativos":["Supporting document reference"]},
{"id":"BT-123","descricao":"Descrição do documento anexado.","tipo":"texto","tipoOrigem":"T","cardinalidade":"0..1","grupo":"BG-24"},
{"id":"BT-124","descricao":"Endereço para um documento, localizado externamente.","tipo":"texto","tipoOrigem":"T","cardinalidade":"0..1","grupo":"BG-24","nomesAlternativos":["External document location"]},
{"id":"BT-125","descricao":"O documento anexado em formato binário. Tipificação do documento anexado em formato binário.","tipo":"texto","tipoOrigem":"B","cardinalidade":"0..1","grupo":"BG-24","nomesAlternativos":["Attached document"],"valoresAdmitidos":["image/png; image/jpeg; application/pdf; application/msword; application/vnd"]},
{"id":"BT-126","descricao":"Identificador único da linha do documento, atribuído pelo fornecedor.","tipo":"texto","tipoOrigem":"I","cardinalidade":"1..1","grupo":"BG-25","nomesAlternativos":["Invoice line identifier"]},
{"id":"BT-127","descricao":"Texto livre para descrever o item respetivo à linha do documento.","tipo":"texto","tipoOrigem":"T","cardinalidade":"0..1","grupo":"BG-25"},
{"id":"BT-128","descricao":"Identificador para um objeto no qual a linha da fatura é baseada, fornecida pelo fornecedor. tipificação do identificador para um objeto no qual a linha da fatura é baseada, fornecida pelo fornecedor.","tipo":"texto","tipoOrigem":"I","cardinalidade":"0..1","grupo":"BG-25","nomesAlternativos":["Invoice line object identifier"]},
{"id":"BT-129","descricao":"Quantidade, do bem ou serviço, faturada.","tipo":"decimal","tipoOrigem":"Q","cardinalidade":"1..1","grupo":"BG-25","nomesAlternativos":["Invoiced quantity"]},
{"id":"BT-130","descricao":"Tipificação da quantidade, do bem ou serviço, faturada.","tipo":"texto","tipoOrigem":"I","cardinalidade":"1..1","grupo":"BG-25","nomesAlternativos":["Invoiced quantity unit of measure code"]},
{"id":"BT-131","descricao":"Montante da linha (s/imposto). O valor deve incluir os respetivos encargos ou descontos aplicados à linha, desprovidos de imposto e outras taxas (que não sejam de IVA).","tipo":"decimal","tipoOrigem":"A","cardinalidade":"1..1","grupo":"BG-25","nomesAlternativos":["Invoice line net amount"]},
{"id":"BT-132","descricao":"Referência para o item da nota de encomenda do cliente.","tipo":"texto","tipoOrigem":"O","cardinalidade":"0..1","grupo":"BG-25","nomesAlternativos":["Referenced purchase order line reference"]},
{"id":"BT-133","descricao":"Número do compromisso associado à linha do documento.","tipo":"texto","tipoOrigem":"T","cardinalidade":"0..1","grupo":"BG-25"},
{"id":"BT-134","descricao":"A data em que o período começa.","tipo":"data","tipoOrigem":"D","cardinalidade":"0..1","grupo":"BG-26","nomesAlternativos":["Invoice line period start date"]},
{"id":"BT-135","descricao":"A data em que o período acaba.","tipo":"data","tipoOrigem":"D","cardinalidade":"0..1","grupo":"BG-26","nomesAlternativos":["Invoice line period end date"]},
{"id":"BT-136","descricao":"Montante de desconto da linha do documento.","tipo":"decimal","tipoOrigem":"A","cardinalidade":"1..1","grupo":"BG-27","nomesAlternativos":["Invoice line allowance amount"]},
{"id":"BT-137","descricao":"Montante base do desconto da linha do documento.","tipo":"decimal","tipoOrigem":"A","cardinalidade":"0..1","grupo":"BG-27","nomesAlternativos":["Invoice line allowance base amount"]},
{"id":"BT-138","descricao":"Fator multiplicador sobre o montante base do desconto da linha do documento.","tipo":"decimal","tipoOrigem":"P","cardinalidade":"0..1","grupo":"BG-27","nomesAlternativos":["Invoice line allowance percentage"]},
{"id":"BT-139","descricao":"Representação textual do desconto da linha do documento.","tipo":"texto","tipoOrigem":"T","cardinalidade":"0..1","grupo":"BG-27","nomesAlternativos":["Invoice line allowance reason"]},
{"id":"BT-140","descricao":"Código do motivo, que possa levar a que o montante contemplado no desconto, esteja isento de imposto.","tipo":"texto","tipoOrigem":"C","cardinalidade":"0..1","grupo":"BG-27","nomesAlternativos":["Invoice line allowance reason code"]},
{"id":"BT-141","descricao":"Montante de encargo da linha do documento.","tipo":"decimal","tipoOrigem":"A","cardinalidade":"1..1","grupo":"BG-28","nomesAlternativos":["Invoice line charge amount"]},
{"id":"BT-142","descricao":"Montante base do encargo da linha do documento.","tipo":"decimal","tipoOrigem":"A","cardinalidade":"0..1","grupo":"BG-28","nomesAlternativos":["Invoice line charge base amount"]},
{"id":"BT-143","descricao":"Fator multiplicador sobre o montante base do encargo da linha do documento.","tipo":"decimal","tipoOrigem":"P","cardinalidade":"0..1","grupo":"BG-28","nomesAlternativos":["Invoice line charge percentage"]},
{"id":"BT-144","descricao":"Representação textual do encargo da linha do documento.","tipo":"texto","tipoOrigem":"T","cardinalidade":"0..1","grupo":"BG-28","nomesAlternativos":["Invoice line charge reason"]},
{"id":"BT-145","descricao":"Código do motivo, que possa levar a que o montante contemplado no encargo esteja isento de imposto.","tipo":"texto","tipoOrigem":"C","cardinalidade":"0..1","grupo":"BG-28","nomesAlternativos":["Invoice line charge reason code"]},
{"id":"BT-146","descricao":"Montante do item após aplicação do desconto.","tipo":"decimal","tipoOrigem":"U","cardinalidade":"1..1","grupo":"BG-29","nomesAlternativos":["Item net price"]},
{"id":"BT-147","descricao":"Montante do desconto sobre o preço do item da linha do documento.","tipo":"decimal","tipoOrigem":"U","cardinalidade":"0..1","grupo":"BG-29","nomesAlternativos":["Item price discount"]},
{"id":"BT-148","descricao":"Montante base, do preço do item da linha do documento, onde incidirá o desconto.","tipo":"decimal","tipoOrigem":"U","cardinalidade":"0..1","grupo":"BG-29","nomesAlternativos":["Item gross price"]},
{"id":"BT-149","descricao":"Número de quantidades que fazem o montante do preço. Por exemplo, se a quantidade faturada for 1000 litros, o preço pode ser 15€ por 10 litros.","tipo":"decimal","tipoOrigem":"Q","cardinalidade":"0..1","grupo":"BG-29","nomesAlternativos":["Item price base quantity"]},
{"id":"BT-150","descricao":"Tipificação do número de quantidades que fazem o montante do preço. Por exemplo, se a quantidade faturada for 1000 litros, o preço pode ser 15€ por 10 litros.","tipo":"texto","tipoOrigem":"C","cardinalidade":"0..1","grupo":"BG-29"},
{"id":"BT-151","descricao":"Código de imposto respeitante à taxa aplicada no item da linha do documento.","tipo":"texto","tipoOrigem":"C","cardinalidade":"1..1","grupo":"BG-30","nomesAlternativos":["Invoiced item VAT category code"],"valoresAdmitidos":["AA","S","E","RED","INT","NOR","ISE","OUT","NA","Z","AE","IC","G e O"]},
{"id":"BT-152","descricao":"Percentagem de imposto respeitante à taxa aplicada no item da linha do documento.","tipo":"decimal","tipoOrigem":"P","cardinalidade":"1..1","grupo":"BG-30","nomesAlternativos":["Invoiced item VAT rate"]},
{"id":"BT-153","descricao":"Nome do item da linha do documento.","tipo":"texto","tipoOrigem":"T","cardinalidade":"1..1","grupo":"BG-31","nomesAlternativos":["Item name"]},
{"id":"BT-154","descricao":"Descrição do item da linha do documento.","tipo":"texto","tipoOrigem":"T","cardinalidade":"0..*","grupo":"BG-31"},
{"id":"BT-155","descricao":"Código de material usado pelo fornecedor, partner number, para identificar univocamente o item da linha do documento.","tipo":"texto","tipoOrigem":"I","cardinalidade":"0..1","grupo":"BG-31","nomesAlternativos":["Item Seller s identifier"]},
{"id":"BT-156","descricao":"Código de material usado no ERP ou Sistema de Faturação.","tipo":"texto","tipoOrigem":"I","cardinalidade":"0..1","grupo":"BG-31","nomesAlternativos":["Item Buyer s identifier"]},
{"id":"BT-157","descricao":"Identificador do item da linha do documento de acordo com um esquema padrão, EAN. Tipificação do identificador do item da linha do documento de acordo com um esquema padrão, EAN.","tipo":"texto","tipoOrigem":"I","cardinalidade":"0..1","grupo":"BG-31","nomesAlternativos":["Item standard identifier"]},
{"id":"BT-158","descricao":"Código da classificação da mercadoria do item da linha do documento empregue na Administração Pública, CPV. Tipificação do código da classificação da mercadoria do item da linha do documento empregue na Administração Pública, CPV. Versão do código da classificação da mercadoria do item da linha do documento empregue na Administração Pública, CPV.","tipo":"texto","tipoOrigem":"I","cardinalidade":"0..*","grupo":"BG-31","nomesAlternativos":["Item classification identifier"]},
{"id":"BT-159","descricao":"País de origem do item.","tipo":"texto","tipoOrigem":"C","cardinalidade":"0..1","grupo":"BG-31","nomesAlternativos":["Item country of origin"]},
{"id":"BT-160","descricao":"Tipo da propriedade adicional do item da linha do documento.","tipo":"texto","tipoOrigem":"T","cardinalidade":"1..1","grupo":"BG-32","nomesAlternativos":["VAT exemption reason code"]},
{"id":"BT-161","descricao":"Valor da propriedade do item da linha do documento. Estrutura que permite indicar o número de referência da fatura associada à linha do documento. Aplica-se a notas de crédito, quando a referência à fatura é indicada por linha.","tipo":"texto","tipoOrigem":"T","cardinalidade":"1..1","grupo":"BG-32","nomesAlternativos":["Item attribute value"]},
{"id":"BT-162","descricao":"Linha de endereço adicional que pode ser usado para fornecer mais detalhes, complementando a linha principal.","tipo":"texto","tipoOrigem":"T","cardinalidade":"0..1","grupo":"BG-5","nomesAlternativos":["Seller address line"]},
{"id":"BT-163","descricao":"Linha de endereço adicional que pode ser usado para fornecer mais detalhes, complementando a linha principal.","tipo":"texto","tipoOrigem":"T","cardinalidade":"0..1","grupo":"BG-8","nomesAlternativos":["Buyer address line"]},
{"id":"BT-164","descricao":"Linha de endereço adicional que pode ser usado para fornecer mais detalhes, complementando a linha principal.","tipo":"texto","tipoOrigem":"T","cardinalidade":"0..1","grupo":"BG-12","nomesAlternativos":["Tax representative address line"]},
{"id":"BT-165","descricao":"Linha de endereço adicional que pode ser usado para fornecer mais detalhes, complementando a linha principal.","tipo":"texto","tipoOrigem":"T","cardinalidade":"0..1","grupo":"BG-15"}
]
```

### Fonte cius-pt-schematron: Schematron CIUS-PT 2.1.1 (urn:feap.gov.pt) (regras de validação)

Papel: regras de validação da fatura eletrónica (sintaxe, modelo, condições, tipos de dados)

Regras (1154):
```json
[
{"id":"BR-CO-25","texto":"In case the Amount due for payment (BT-115) is positive, either the Payment due date (BT-9) or the Payment terms (BT-20) shall be present.","categoria":"condicional","natureza":"RIR","gravidade":"erro","contexto":"Amount_due ","elementos":["BT-9","BT-20","BT-115"],"expressao":"((. > 0) and (exists(//cbc:DueDate) or exists (//cac:PaymentMeans/cbc:PaymentDueDate) or exists(//cac:PaymentTerms/cbc:Note))) or (. <= 0)"},
{"id":"BR-AA-01","texto":"An Invoice that contains an Invoice line (BG-25), a Document level allowance (BG-20) or a Document level charge (BG-21) where the VAT category code (BT-151, BT-95 or BT-102) is “Lower rate” shall contain in the VATBReakdown (BG-23) at least one VAT category code (BT-118) equal with \"Lower rate\".","categoria":"condicional","natureza":"RIR","gravidade":"erro","contexto":"Invoice ","elementos":["BG-20","BG-21","BG-23","BG-25","BT-95","BT-102","BT-118","BT-151"],"expressao":"((count(//cac:AllowanceCharge/cac:TaxCategory[normalize-space(cbc:ID) = 'AA' or normalize-space(cbc:ID) = 'RED' or normalize-space(cbc:ID) = 'INT']) + count(//cac:ClassifiedTaxCategory[normalize-space(cbc:ID) = 'AA' or normalize-space(cbc:ID) = 'RED' or normalize-space(cbc:ID) = 'INT'])) > 0 and count(cac:TaxTotal/cac:TaxSubtotal/cac:TaxCategory[normalize-space(cbc:ID) = 'AA' or normalize-space(cbc:ID) = 'RED' or normalize-space(cbc:ID) = 'INT']) > 0) or ((count(//cac:AllowanceCharge/cac:TaxCategory[normalize-space(cbc:ID) = 'AA' or normalize-space(cbc:ID) = 'RED' or normalize-space(cbc:ID) = 'INT']) + count(//cac:ClassifiedTaxCategory[normalize-space(cbc:ID) = 'AA' or normalize-space(cbc:ID) = 'RED' or normalize-space(cbc:ID) = 'INT'])) = 0 and count(cac:TaxTotal/cac:TaxSubtotal/cac:TaxCategory[normalize-space(cbc:ID) = 'AA' or normalize-space(cbc:ID) = 'RED' or normalize-space(cbc:ID) = 'INT']) = 0)"},
{"id":"BR-S-01","texto":"An Invoice that contains an Invoice line (BG-25), a Document level allowance (BG-20) or a Document level charge (BG-21) where the VAT category code (BT-151, BT-95 or BT-102) is “Standard rated” shall contain in the VATBReakdown (BG-23) at least one VAT category code (BT-118) equal with \"Standard rated\".","categoria":"condicional","natureza":"RIR","gravidade":"erro","contexto":"Invoice ","elementos":["BG-20","BG-21","BG-23","BG-25","BT-95","BT-102","BT-118","BT-151"],"expressao":"((count(//cac:AllowanceCharge/cac:TaxCategory[normalize-space(cbc:ID) = 'S' or normalize-space(cbc:ID) = 'NOR']) + count(//cac:ClassifiedTaxCategory[normalize-space(cbc:ID) = 'S' or normalize-space(cbc:ID) = 'NOR'])) > 0 and count(cac:TaxTotal/cac:TaxSubtotal/cac:TaxCategory[normalize-space(cbc:ID) = 'S' or normalize-space(cbc:ID) = 'NOR']) > 0) or ((count(//cac:AllowanceCharge/cac:TaxCategory[normalize-space(cbc:ID) = 'S' or normalize-space(cbc:ID) = 'NOR']) + count(//cac:ClassifiedTaxCategory[normalize-space(cbc:ID) = 'S' or normalize-space(cbc:ID) = 'NOR'])) = 0 and count(cac:TaxTotal/cac:TaxSubtotal/cac:TaxCategory[normalize-space(cbc:ID) = 'S' or normalize-space(cbc:ID) = 'NOR']) = 0)"},
{"id":"BR-E-01","texto":"An Invoice that contains an Invoice line (BG-25), a Document level allowance (BG-20) or a Document level charge (BG-21) where the VAT category code (BT-151, BT-95 or BT-102) is “Exempt from VAT” shall contain exactly one VATBReakdown (BG-23) with the VAT category code (BT-118) equal to \"Exempt from VAT\".","categoria":"condicional","natureza":"RIR","gravidade":"erro","contexto":"Invoice ","elementos":["BG-20","BG-21","BG-23","BG-25","BT-95","BT-102","BT-118","BT-151"],"expressao":"((count(//cac:AllowanceCharge/cac:TaxCategory[normalize-space(cbc:ID) = 'E' or normalize-space(cbc:ID) = 'ISE']) + count(//cac:ClassifiedTaxCategory[normalize-space(cbc:ID) = 'E' or normalize-space(cbc:ID) = 'ISE'])) > 0 and count(cac:TaxTotal/cac:TaxSubtotal/cac:TaxCategory[normalize-space(cbc:ID) = 'E' or normalize-space(cbc:ID) = 'ISE']) > 0) or ((count(//cac:AllowanceCharge/cac:TaxCategory[normalize-space(cbc:ID) = 'E' or normalize-space(cbc:ID) = 'ISE']) + count(//cac:ClassifiedTaxCategory[normalize-space(cbc:ID) = 'E' or normalize-space(cbc:ID) = 'ISE'])) = 0 and count(cac:TaxTotal/cac:TaxSubtotal/cac:TaxCategory[normalize-space(cbc:ID) = 'E' or normalize-space(cbc:ID) = 'ISE']) = 0)"},
{"id":"DT-CIUS-PT-165","texto":"Invoice total amount with VAT (BT-112) = Invoice total amount without VAT (BT-109) + Invoice total VAT amount (BT-110), with an acceptance range of 1.00 € (it does not mean that this tolerance is accepted by the customer).","categoria":"calculo","natureza":"FN","gravidade":"erro","contexto":"Invoice ","elementos":["BT-109","BT-110","BT-112"],"expressao":"every $Currency in cbc:DocumentCurrencyCode satisfies ((round( (cac:LegalMonetaryTotal/xs:decimal(cbc:TaxExclusiveAmount) + cac:TaxTotal/xs:decimal(cbc:TaxAmount[@currencyID=$Currency])) * 10 * 10) div 100) <= (cac:LegalMonetaryTotal/xs:decimal(cbc:TaxInclusiveAmount) + 1.00) and (round( (cac:LegalMonetaryTotal/xs:decimal(cbc:TaxExclusiveAmount) + cac:TaxTotal/xs:decimal(cbc:TaxAmount[@currencyID=$Currency])) * 10 * 10) div 100) >= (cac:LegalMonetaryTotal/xs:decimal(cbc:TaxInclusiveAmount) - 1.00))"},
{"id":"DT-CIUS-PT-176","texto":"An Invoice that contains Invoice lines (BG-25) with diferent VAT exemption reason codes, where the VAT category code (BT-151) is “Exempt from VAT”, shall contain exactly one VATBReakdown (BG-23) with the VAT category code (BT-118) equal to \"Exempt from VAT\", for each VAT exemption reason code (BT-121).","categoria":"condicional","natureza":"RIR","gravidade":"erro","contexto":"Invoice ","elementos":["BG-23","BG-25","BT-118","BT-121","BT-151"],"expressao":"every $taxExemptionReasonCode in //cac:InvoiceLine[cac:Item/cac:ClassifiedTaxCategory/cbc:ID = 'E' or cac:Item/cac:ClassifiedTaxCategory/cbc:ID = 'ISE']/cac:Item/cac:AdditionalItemProperty[cbc:Name='#TAXEXEMPTIONREASONCODE@CLASSIFIEDTAXCATEGORY#']/cbc:Value satisfies ( count(//cac:TaxTotal/cac:TaxSubtotal[(cac:TaxCategory/cbc:ID='E' or cac:TaxCategory/cbc:ID='ISE') and cac:TaxCategory/cbc:TaxExemptionReasonCode = $taxExemptionReasonCode]) = 1)"},
{"id":"BR-28","texto":"The Item gross price (BT-148) shall NOT be negative.","categoria":"outra","natureza":"?","gravidade":"erro","contexto":"Invoice_Line ","elementos":["BT-148"],"expressao":"(cac:Price/cac:AllowanceCharge/cbc:BaseAmount) >= 0 or not(exists(cac:Price/cac:AllowanceCharge/cbc:BaseAmount))"},
{"id":"BR-27","texto":"The Item net price (BT-146) shall NOT be negative.","categoria":"outra","natureza":"?","gravidade":"erro","contexto":"Invoice_Line ","elementos":["BT-146"],"expressao":"(cac:Price/cbc:PriceAmount) >= 0"},
{"id":"BR-CO-04","texto":"Each Invoice line (BG-25) shall be categorized with an Invoiced item VAT category code (BT-151).","categoria":"outra","natureza":"?","gravidade":"erro","contexto":"Invoice_Line ","elementos":["BG-25","BT-151"],"expressao":"(cac:Item/cac:ClassifiedTaxCategory/cbc:ID)"},
{"id":"DT-CIUS-PT-157","texto":"The BT-131 must equal the multiplication between the quantity (InvoicedQuantity) and the price (PriceAmount) divided by the base quantity (BaseQuantity) subtracted by the sum of the discounts and added the sum of the charges of the line, with an acceptance range of 1.00 € (it does not mean that this tolerance is accepted by the customer).","categoria":"calculo","natureza":"FN","gravidade":"erro","contexto":"Invoice_Line ","elementos":["BT-131"],"expressao":"((not(exists(cac:Price/cbc:BaseQuantity)) or ((exists(cac:Price/cbc:BaseQuantity)) and cac:Price/xs:decimal(cbc:BaseQuantity) = 0 )) and ((exists(cac:AllowanceCharge[cbc:ChargeIndicator='false']) and exists(cac:AllowanceCharge[cbc:ChargeIndicator='true']) and ((round(xs:decimal(cbc:InvoicedQuantity | cbc:CreditedQuantity) * cac:Price/xs:decimal(cbc:PriceAmount) * 100) div 100) + (round(sum(cac:AllowanceCharge[cbc:ChargeIndicator='true']/xs:decimal(cbc:Amount)) * 10 * 10) div 100) - (round(sum(cac:AllowanceCharge[cbc:ChargeIndicator='false']/xs:decimal(cbc:Amount)) * 10 * 10) div 100)) <= (xs:decimal(cbc:LineExtensionAmount) + 1.00) and ((round(xs:decimal(cbc:InvoicedQuantity | cbc:CreditedQuantity) * cac:Price/xs:decimal(cbc:PriceAmount) * 100) div 100) + (round(sum(cac:AllowanceCharge[cbc:ChargeIndicator='true']/xs:decimal(cbc:Amount)) * 10 * 10) div 100) - (round(sum(cac:AllowanceCharge[cbc:ChargeIndicator='false']/xs:decimal(cbc:Amount)) * 10 * 10) div 100)) >= (xs:decimal(cbc:LineExtensionAmount) - 1.00)) or (not(exists(cac:AllowanceCharge[cbc:ChargeIndicator='false'])) and exists(cac:AllowanceCharge[cbc:ChargeIndicator='true']) and ((round(xs:decimal(cbc:InvoicedQuantity | cbc:CreditedQuantity) * cac:Price/xs:decimal(cbc:PriceAmount) * 100) div 100) + (round(sum(cac:AllowanceCharge[cbc:ChargeIndicator='true']/xs:decimal(cbc:Amount)) * 10 * 10) div 100)) <= (xs:decimal(cbc:LineExtensionAmount) + 1.00) and ((round(xs:decimal(cbc:InvoicedQuantity | cbc:CreditedQuantity) * cac:Price/xs:decimal(cbc:PriceAmount) * 100) div 100) + (round(sum(cac:AllowanceCharge[cbc:ChargeIndicator='true']/xs:decimal(cbc:Amount)) * 10 * 10) div 100)) >= (xs:decimal(cbc:LineExtensionAmount) - 1.00)) or (exists(cac:AllowanceCharge[cbc:ChargeIndicator='false']) and not(exists(cac:AllowanceCharge[cbc:ChargeIndicator='true'])) and  ((round(xs:decimal(cbc:InvoicedQuantity | cbc:CreditedQuantity) * cac:Price/xs:decimal(cbc:PriceAmount) * 100) div 100) - (round(sum(cac:AllowanceCharge[cbc:ChargeIndicator='false']/xs:decimal(cbc:Amount)) * 10 * 10) div 100)) <= (xs:decimal(cbc:LineExtensionAmount) + 1.00) and ((round(xs:decimal(cbc:InvoicedQuantity | cbc:CreditedQuantity) * cac:Price/xs:decimal(cbc:PriceAmount) * 100) div 100) - (round(sum(cac:AllowanceCharge[cbc:ChargeIndicator='false']/xs:decimal(cbc:Amount)) * 10 * 10) div 100)) >= (xs:decimal(cbc:LineExtensionAmount) - 1.00)) or (not(exists(cac:AllowanceCharge[cbc:ChargeIndicator='false'])) and not(exists(cac:AllowanceCharge[cbc:ChargeIndicator='true'])) and  (round(xs:decimal(cbc:InvoicedQuantity | cbc:CreditedQuantity) * cac:Price/xs:decimal(cbc:PriceAmount) * 100) div 100) <= (xs:decimal(cbc:LineExtensionAmount) + 1.00) and  (round(xs:decimal(cbc:InvoicedQuantity | cbc:CreditedQuantity) * cac:Price/xs:decimal(cbc:PriceAmount) * 100) div 100) >= (xs:decimal(cbc:LineExtensionAmount) - 1.00)))) or (exists(cac:Price/cbc:BaseQuantity) and (cac:Price/xs:decimal(cbc:BaseQuantity) > 0) and ((exists(cac:AllowanceCharge[cbc:ChargeIndicator='false']) and exists(cac:AllowanceCharge[cbc:ChargeIndicator='true']) and ((round((xs:decimal(cbc:InvoicedQuantity | cbc:CreditedQuantity) * cac:Price/xs:decimal(cbc:PriceAmount) div cac:Price/xs:decimal(cbc:BaseQuantity)) * 100) div 100) + (round(sum(cac:AllowanceCharge[cbc:ChargeIndicator='true']/xs:decimal(cbc:Amount)) * 10 * 10) div 100) - (round(sum(cac:AllowanceCharge[cbc:ChargeIndicator='false']/xs:decimal(cbc:Amount)) * 10 * 10) div 100)) <= (xs:decimal(cbc:LineExtensionAmount) + 1.00) and ((round((xs:decimal(cbc:InvoicedQuantity | cbc:CreditedQuantity) * cac:Price/xs:decimal(cbc:PriceAmount) div cac:Price/xs:decimal(cbc:BaseQuantity)) * 100) div 100) + (round(sum(cac:AllowanceCharge[cbc:ChargeIndicator='true']/xs:decimal(cbc:Amount)) * 10 * 10) div 100) - (round(sum(cac:AllowanceCharge[cbc:ChargeIndicator='false']/xs:decimal(cbc:Amount)) * 10 * 10) div 100)) >= (xs:decimal(cbc:LineExtensionAmount) - 1.00)) or (not(exists(cac:AllowanceCharge[cbc:ChargeIndicator='false'])) and exists(cac:AllowanceCharge[cbc:ChargeIndicator='true']) and ((round((xs:decimal(cbc:InvoicedQuantity | cbc:CreditedQuantity) * cac:Price/xs:decimal(cbc:PriceAmount) div cac:Price/xs:decimal(cbc:BaseQuantity)) * 100) div 100) + (round(sum(cac:AllowanceCharge[cbc:ChargeIndicator='true']/xs:decimal(cbc:Amount)) * 10 * 10) div 100)) <= (xs:decimal(cbc:LineExtensionAmount) + 1.00) and ((round((xs:decimal(cbc:InvoicedQuantity | cbc:CreditedQuantity) * cac:Price/xs:decimal(cbc:PriceAmount) div cac:Price/xs:decimal(cbc:BaseQuantity)) * 100) div 100) + (round(sum(cac:AllowanceCharge[cbc:ChargeIndicator='true']/xs:decimal(cbc:Amount)) * 10 * 10) div 100)) >= (xs:decimal(cbc:LineExtensionAmount) - 1.00)) or (exists(cac:AllowanceCharge[cbc:ChargeIndicator='false']) and not(exists(cac:AllowanceCharge[cbc:ChargeIndicator='true'])) and ((round((xs:decimal(cbc:InvoicedQuantity | cbc:CreditedQuantity) * cac:Price/xs:decimal(cbc:PriceAmount) div cac:Price/xs:decimal(cbc:BaseQuantity)) * 100) div 100) - (round(sum(cac:AllowanceCharge[cbc:ChargeIndicator='false']/xs:decimal(cbc:Amount)) * 10 * 10) div 100)) <= (xs:decimal(cbc:LineExtensionAmount) + 1.00) and ((round((xs:decimal(cbc:InvoicedQuantity | cbc:CreditedQuantity) * cac:Price/xs:decimal(cbc:PriceAmount) div cac:Price/xs:decimal(cbc:BaseQuantity)) * 100) div 100) - (round(sum(cac:AllowanceCharge[cbc:ChargeIndicator='false']/xs:decimal(cbc:Amount)) * 10 * 10) div 100)) >= (xs:decimal(cbc:LineExtensionAmount) - 1.00)) or (not(exists(cac:AllowanceCharge[cbc:ChargeIndicator='false'])) and not(exists(cac:AllowanceCharge[cbc:ChargeIndicator='true'])) and (round((xs:decimal(cbc:InvoicedQuantity | cbc:CreditedQuantity) * cac:Price/xs:decimal(cbc:PriceAmount) div cac:Price/xs:decimal(cbc:BaseQuantity)) * 100) div 100) <= (xs:decimal(cbc:LineExtensionAmount) + 1.00) and (round((xs:decimal(cbc:InvoicedQuantity | cbc:CreditedQuantity) * cac:Price/xs:decimal(cbc:PriceAmount) div cac:Price/xs:decimal(cbc:BaseQuantity)) * 100) div 100) >= (xs:decimal(cbc:LineExtensionAmount) - 1.00))))"},
{"id":"DT-CIUS-PT-177","texto":"The Item price base quantity (BT-149) shall be greater than zero.","categoria":"gama","natureza":"RP","gravidade":"erro","contexto":"Invoice_Line ","elementos":["BT-149"],"expressao":"((cac:Price/cbc:BaseQuantity) > 0) or not(exists(cac:Price/cbc:BaseQuantity))"},
{"id":"BR-17","texto":"The Payee name (BT-59) shall be provided in the Invoice, if the Payee (BG-10) is different from the Seller (BG-4)","categoria":"condicional","natureza":"RIR","gravidade":"erro","contexto":"Payee ","elementos":["BG-4","BG-10","BT-59"],"expressao":"exists(cac:PartyName/cbc:Name) and (not(cac:PartyName/cbc:Name = ../cac:AccountingSupplierParty/cac:Party/cac:PartyName/cbc:Name) and not(cac:PartyIdentification/cbc:ID = ../cac:AccountingSupplierParty/cac:Party/cac:PartyIdentification/cbc:ID) and not(cac:PartyLegalEntity/cbc:CompanyID = ../cac:AccountingSupplierParty/cac:Party/cac:PartyLegalEntity/cbc:CompanyID))"},
{"id":"UBL-SR-19","texto":"Payee name shall occur maximum once, if the Payee is different from the Seller","categoria":"condicional","natureza":"RIR","gravidade":"aviso","contexto":"Payee ","expressao":"(count(cac:PartyName/cbc:Name) <= 1) and ((cac:PartyName/cbc:Name) != (../cac:AccountingSupplierParty/cac:Party/cac:PartyLegalEntity/cbc:RegistrationName))"},
{"id":"UBL-SR-20","texto":"Payee identifier shall occur maximum once, if the Payee is different from the Seller","categoria":"condicional","natureza":"RIR","gravidade":"aviso","contexto":"Payee ","expressao":"(count(cac:PartyIdentification/cbc:ID) <= 1) and ((cac:PartyName/cbc:Name) != (../cac:AccountingSupplierParty/cac:Party/cac:PartyLegalEntity/cbc:RegistrationName))"},
{"id":"UBL-SR-21","texto":"Payee legal registration identifier shall occur maximum once, if the Payee is different from the Seller","categoria":"condicional","natureza":"RIR","gravidade":"aviso","contexto":"Payee ","expressao":"(count(cac:PartyLegalEntity/cbc:CompanyID) <= 1) and ((cac:PartyName/cbc:Name) != (../cac:AccountingSupplierParty/cac:Party/cac:PartyLegalEntity/cbc:RegistrationName))"},
{"id":"DT-CIUS-PT-164","texto":"Invoice total VAT amount (BT-110) = Σ VAT category tax amount (BT-117), with an acceptance range of 1.00 € (it does not mean that this tolerance is accepted by the customer).","categoria":"calculo","natureza":"FN","gravidade":"erro","contexto":"Tax_Total ","elementos":["BT-110","BT-117"],"expressao":"((round((sum(cac:TaxSubtotal/xs:decimal(cbc:TaxAmount)) * 10 * 10)) div 100) <= (xs:decimal(child::cbc:TaxAmount) + 1.00) and (round((sum(cac:TaxSubtotal/xs:decimal(cbc:TaxAmount)) * 10 * 10)) div 100) >= (xs:decimal(child::cbc:TaxAmount) - 1.00)) or not(cac:TaxSubtotal)"},
{"id":"DT-CIUS-PT-175","texto":"In a VATBReakdown (BG-23) where the VAT category code (BT-118) is \"Exempt from VAT\" the VAT category taxable amount (BT-116) shall equal the sum of Invoice line net amounts (BT-131) minus the sum of Document level allowance amounts (BT-92) plus the sum of Document level charge amounts (BT-99) where the VAT category codes (BT-151, BT-95, BT-102) are “Exempt from VAT\", with an acceptance range of 1.00 € (it does not mean that this tolerance is accepted by the customer).","categoria":"condicional","natureza":"RIR","gravidade":"erro","contexto":"Tax_Total ","elementos":["BG-23","BT-92","BT-95","BT-99","BT-102","BT-116","BT-118","BT-131","BT-151"],"expressao":"(exists(//cac:InvoiceLine) and ((sum(//cac:TaxTotal/cac:TaxSubtotal[normalize-space(cac:TaxCategory/cbc:ID) = 'E' or normalize-space(cac:TaxCategory/cbc:ID) = 'ISE']/xs:decimal(cbc:TaxableAmount)) - 1.00) <= (round((sum(//cac:InvoiceLine[normalize-space(cac:Item/cac:ClassifiedTaxCategory/cbc:ID)='E' or normalize-space(cac:Item/cac:ClassifiedTaxCategory/cbc:ID)='ISE']/xs:decimal(cbc:LineExtensionAmount)) + sum(//cac:AllowanceCharge[cbc:ChargeIndicator='true'][normalize-space(cac:TaxCategory/cbc:ID) = 'E' or normalize-space(cac:TaxCategory/cbc:ID) = 'ISE']/xs:decimal(cbc:Amount)) - sum(//cac:AllowanceCharge[cbc:ChargeIndicator='false'][normalize-space(cac:TaxCategory/cbc:ID) = 'E' or normalize-space(cac:TaxCategory/cbc:ID) = 'ISE']/xs:decimal(cbc:Amount))) * 100) div 100)) and ((sum(//cac:TaxTotal/cac:TaxSubtotal[normalize-space(cac:TaxCategory/cbc:ID) = 'E' or normalize-space(cac:TaxCategory/cbc:ID) = 'ISE']/xs:decimal(cbc:TaxableAmount)) + 1.00) >= (round((sum(//cac:InvoiceLine[normalize-space(cac:Item/cac:ClassifiedTaxCategory/cbc:ID)='E' or normalize-space(cac:Item/cac:ClassifiedTaxCategory/cbc:ID)='ISE']/xs:decimal(cbc:LineExtensionAmount)) + sum(//cac:AllowanceCharge[cbc:ChargeIndicator='true'][normalize-space(cac:TaxCategory/cbc:ID) = 'E' or normalize-space(cac:TaxCategory/cbc:ID) = 'ISE']/xs:decimal(cbc:Amount)) - sum(//cac:AllowanceCharge[cbc:ChargeIndicator='false'][normalize-space(cac:TaxCategory/cbc:ID) = 'E' or normalize-space(cac:TaxCategory/cbc:ID) = 'ISE']/xs:decimal(cbc:Amount))) * 100) div 100))) or  (exists(//cac:CreditNoteLine) and ((sum(//cac:TaxTotal/cac:TaxSubtotal[normalize-space(cac:TaxCategory/cbc:ID) = 'E' or normalize-space(cac:TaxCategory/cbc:ID) = 'ISE']/xs:decimal(cbc:TaxableAmount)) - 1.00) <= (round((sum(//cac:CreditNoteLine[normalize-space(cac:Item/cac:ClassifiedTaxCategory/cbc:ID)='E' or normalize-space(cac:Item/cac:ClassifiedTaxCategory/cbc:ID)='ISE']/xs:decimal(cbc:LineExtensionAmount)) + sum(//cac:AllowanceCharge[cbc:ChargeIndicator='true'][normalize-space(cac:TaxCategory/cbc:ID) = 'E' or normalize-space(cac:TaxCategory/cbc:ID) = 'ISE']/xs:decimal(cbc:Amount)) - sum(//cac:AllowanceCharge[cbc:ChargeIndicator='false'][normalize-space(cac:TaxCategory/cbc:ID) = 'E' or normalize-space(cac:TaxCategory/cbc:ID) = 'ISE']/xs:decimal(cbc:Amount))) * 100) div 100)) and ((sum(//cac:TaxTotal/cac:TaxSubtotal[normalize-space(cac:TaxCategory/cbc:ID) = 'E' or normalize-space(cac:TaxCategory/cbc:ID) = 'ISE']/xs:decimal(cbc:TaxableAmount)) + 1.00) >= (round((sum(//cac:CreditNoteLine[normalize-space(cac:Item/cac:ClassifiedTaxCategory/cbc:ID)='E' or normalize-space(cac:Item/cac:ClassifiedTaxCategory/cbc:ID)='ISE']/xs:decimal(cbc:LineExtensionAmount)) + sum(//cac:AllowanceCharge[cbc:ChargeIndicator='true'][normalize-space(cac:TaxCategory/cbc:ID) = 'E' or normalize-space(cac:TaxCategory/cbc:ID) = 'ISE']/xs:decimal(cbc:Amount)) - sum(//cac:AllowanceCharge[cbc:ChargeIndicator='false'][normalize-space(cac:TaxCategory/cbc:ID) = 'E' or normalize-space(cac:TaxCategory/cbc:ID) = 'ISE']/xs:decimal(cbc:Amount))) * 100) div 100)))"},
{"id":"DT-CIUS-PT-160","texto":"Sum of Invoice line net amount (BT-106) = Σ Invoice line net amount (BT-131), with an acceptance range of 1.00 € (it does not mean that this tolerance is accepted by the customer).","categoria":"calculo","natureza":"FN","gravidade":"erro","contexto":"Document_totals ","elementos":["BT-106","BT-131"],"expressao":"((round(sum(//cac:InvoiceLine/xs:decimal(cbc:LineExtensionAmount)) * 100) div 100) <= (xs:decimal(cbc:LineExtensionAmount) + 1.00) and (round(sum(//cac:InvoiceLine/xs:decimal(cbc:LineExtensionAmount)) * 100) div 100) >= (xs:decimal(cbc:LineExtensionAmount) - 1.00)) or ((round(sum(//cac:CreditNoteLine/xs:decimal(cbc:LineExtensionAmount)) * 100) div 100) <= (xs:decimal(cbc:LineExtensionAmount) + 1.00) and (round(sum(//cac:CreditNoteLine/xs:decimal(cbc:LineExtensionAmount)) * 100) div 100) >= (xs:decimal(cbc:LineExtensionAmount) - 1.00))"},
{"id":"DT-CIUS-PT-161","texto":"Sum of allowances on document level (BT-107) = Σ Document level allowance amount (BT-92), with an acceptance range of 1.00 € (it does not mean that this tolerance is accepted by the customer).","categoria":"calculo","natureza":"FN","gravidade":"erro","contexto":"Document_totals ","elementos":["BT-92","BT-107"],"expressao":"(exists(../cac:AllowanceCharge[cbc:ChargeIndicator='false']) and (round(sum(../cac:AllowanceCharge[cbc:ChargeIndicator='false']/xs:decimal(cbc:Amount)) * 10 * 10) div 100) <= (xs:decimal(cbc:AllowanceTotalAmount) + 1.00) and (round(sum(../cac:AllowanceCharge[cbc:ChargeIndicator='false']/xs:decimal(cbc:Amount)) * 10 * 10) div 100) >= (xs:decimal(cbc:AllowanceTotalAmount) - 1.00)) or (not(exists(../cac:AllowanceCharge[cbc:ChargeIndicator='false'])) and xs:decimal(cbc:AllowanceTotalAmount) = 0.00) or not(cbc:AllowanceTotalAmount)"},
{"id":"DT-CIUS-PT-162","texto":"Sum of charges on document level (BT-108) = Σ Document level charge amount (BT-99), with an acceptance range of 1.00 € (it does not mean that this tolerance is accepted by the customer).","categoria":"calculo","natureza":"FN","gravidade":"erro","contexto":"Document_totals ","elementos":["BT-99","BT-108"],"expressao":"(exists(../cac:AllowanceCharge[cbc:ChargeIndicator='true']) and ((round(sum(../cac:AllowanceCharge[cbc:ChargeIndicator='true']/xs:decimal(cbc:Amount)) * 10 * 10) div 100) <= (xs:decimal(cbc:ChargeTotalAmount) + 1.00) and (round(sum(../cac:AllowanceCharge[cbc:ChargeIndicator='true']/xs:decimal(cbc:Amount)) * 10 * 10) div 100) >= (xs:decimal(cbc:ChargeTotalAmount) - 1.00))) or (not(exists(../cac:AllowanceCharge[cbc:ChargeIndicator='true'])) and xs:decimal(cbc:ChargeTotalAmount) = 0.00) or not(cbc:ChargeTotalAmount)"},
{"id":"DT-CIUS-PT-163","texto":"Invoice total amount without VAT (BT-109) = Σ Invoice line net amount (BT-131) - Sum of allowances on document level (BT-107) + Sum of charges on document level (BT-108), with an acceptance range of 1.00 € (it does not mean that this tolerance is accepted by the customer).","categoria":"calculo","natureza":"FN","gravidade":"erro","contexto":"Document_totals ","elementos":["BT-107","BT-108","BT-109","BT-131"],"expressao":"(exists(../cac:InvoiceLine) and ((cbc:ChargeTotalAmount) and (cbc:AllowanceTotalAmount) and (round((sum(../cac:InvoiceLine/xs:decimal(cbc:LineExtensionAmount)) + xs:decimal(cbc:ChargeTotalAmount) - xs:decimal(cbc:AllowanceTotalAmount)) * 10 * 10) div 100 ) <= (xs:decimal(cbc:TaxExclusiveAmount) + 1.00) and (round((sum(../cac:InvoiceLine/xs:decimal(cbc:LineExtensionAmount)) + xs:decimal(cbc:ChargeTotalAmount) - xs:decimal(cbc:AllowanceTotalAmount)) * 10 * 10) div 100 ) >= (xs:decimal(cbc:TaxExclusiveAmount) - 1.00)) or ( not(cbc:ChargeTotalAmount) and (cbc:AllowanceTotalAmount) and (round((sum(../cac:InvoiceLine/xs:decimal(cbc:LineExtensionAmount)) - xs:decimal(cbc:AllowanceTotalAmount)) * 10 * 10 ) div 100) <= (xs:decimal(cbc:TaxExclusiveAmount) + 1.00) and (round((sum(../cac:InvoiceLine/xs:decimal(cbc:LineExtensionAmount)) - xs:decimal(cbc:AllowanceTotalAmount)) * 10 * 10 ) div 100) >= (xs:decimal(cbc:TaxExclusiveAmount) - 1.00) ) or ( (cbc:ChargeTotalAmount) and not(cbc:AllowanceTotalAmount) and (round((sum(../cac:InvoiceLine/xs:decimal(cbc:LineExtensionAmount)) + xs:decimal(cbc:ChargeTotalAmount)) * 10 * 10 ) div 100) <= (xs:decimal(cbc:TaxExclusiveAmount) + 1.00) and (round((sum(../cac:InvoiceLine/xs:decimal(cbc:LineExtensionAmount)) + xs:decimal(cbc:ChargeTotalAmount)) * 10 * 10 ) div 100) >= (xs:decimal(cbc:TaxExclusiveAmount) - 1.00)) or ( not(cbc:ChargeTotalAmount) and not(cbc:AllowanceTotalAmount) and sum(../cac:InvoiceLine/xs:decimal(cbc:LineExtensionAmount)) <= (xs:decimal(cbc:TaxExclusiveAmount) + 1.00) and sum(../cac:InvoiceLine/xs:decimal(cbc:LineExtensionAmount)) >= (xs:decimal(cbc:TaxExclusiveAmount) - 1.00))) or (exists(../cac:CreditNoteLine) and ((cbc:ChargeTotalAmount) and (cbc:AllowanceTotalAmount) and (round((sum(../cac:CreditNoteLine/xs:decimal(cbc:LineExtensionAmount)) + xs:decimal(cbc:ChargeTotalAmount) - xs:decimal(cbc:AllowanceTotalAmount)) * 10 * 10) div 100 ) <= (xs:decimal(cbc:TaxExclusiveAmount) + 1.00) and (round((sum(../cac:CreditNoteLine/xs:decimal(cbc:LineExtensionAmount)) + xs:decimal(cbc:ChargeTotalAmount) - xs:decimal(cbc:AllowanceTotalAmount)) * 10 * 10) div 100 ) >= (xs:decimal(cbc:TaxExclusiveAmount) - 1.00)) or ( not(cbc:ChargeTotalAmount) and (cbc:AllowanceTotalAmount) and (round((sum(../cac:CreditNoteLine/xs:decimal(cbc:LineExtensionAmount)) - xs:decimal(cbc:AllowanceTotalAmount)) * 10 * 10 ) div 100) <= (xs:decimal(cbc:TaxExclusiveAmount) + 1.00) and (round((sum(../cac:CreditNoteLine/xs:decimal(cbc:LineExtensionAmount)) - xs:decimal(cbc:AllowanceTotalAmount)) * 10 * 10 ) div 100) >= (xs:decimal(cbc:TaxExclusiveAmount) - 1.00) ) or ( (cbc:ChargeTotalAmount) and not(cbc:AllowanceTotalAmount) and (round((sum(../cac:CreditNoteLine/xs:decimal(cbc:LineExtensionAmount)) + xs:decimal(cbc:ChargeTotalAmount)) * 10 * 10 ) div 100) <= (xs:decimal(cbc:TaxExclusiveAmount) + 1.00) and (round((sum(../cac:CreditNoteLine/xs:decimal(cbc:LineExtensionAmount)) + xs:decimal(cbc:ChargeTotalAmount)) * 10 * 10 ) div 100) >= (xs:decimal(cbc:TaxExclusiveAmount) - 1.00)) or ( not(cbc:ChargeTotalAmount) and not(cbc:AllowanceTotalAmount) and sum(../cac:CreditNoteLine/xs:decimal(cbc:LineExtensionAmount)) <= (xs:decimal(cbc:TaxExclusiveAmount) + 1.00) and sum(../cac:CreditNoteLine/xs:decimal(cbc:LineExtensionAmount)) >= (xs:decimal(cbc:TaxExclusiveAmount) - 1.00)))"},
{"id":"DT-CIUS-PT-166","texto":"Amount due for payment (BT-115) = Invoice total amount with VAT (BT-112) -Paid amount (BT-113) +Rounding amount (BT-114), with an acceptance range of 1.00 € (it does not mean that this tolerance is accepted by the customer).","categoria":"calculo","natureza":"FN","gravidade":"erro","contexto":"Document_totals ","elementos":["BT-112","BT-113","BT-114","BT-115"],"expressao":"(xs:decimal(cbc:PrepaidAmount) and not(xs:decimal(cbc:PayableRoundingAmount)) and (round((xs:decimal(cbc:TaxInclusiveAmount) - xs:decimal(cbc:PrepaidAmount)) * 10 * 10) div 100) <= (xs:decimal(cbc:PayableAmount) + 1.00) and (round((xs:decimal(cbc:TaxInclusiveAmount) - xs:decimal(cbc:PrepaidAmount)) * 10 * 10) div 100) >= (xs:decimal(cbc:PayableAmount) - 1.00)) or (not(xs:decimal(cbc:PrepaidAmount)) and not(xs:decimal(cbc:PayableRoundingAmount)) and xs:decimal(cbc:TaxInclusiveAmount) <= (xs:decimal(cbc:PayableAmount) + 1.00) and xs:decimal(cbc:TaxInclusiveAmount) >= (xs:decimal(cbc:PayableAmount) - 1.00)) or (xs:decimal(cbc:PrepaidAmount) and xs:decimal(cbc:PayableRoundingAmount) and ((round((xs:decimal(cbc:PayableAmount) - xs:decimal(cbc:PayableRoundingAmount)) * 10 * 10) div 100) <= ((round((xs:decimal(cbc:TaxInclusiveAmount) - xs:decimal(cbc:PrepaidAmount)) * 10 * 10) div 100) + 1.00)) and ((round((xs:decimal(cbc:PayableAmount) - xs:decimal(cbc:PayableRoundingAmount)) * 10 * 10) div 100) >= ((round((xs:decimal(cbc:TaxInclusiveAmount) - xs:decimal(cbc:PrepaidAmount)) * 10 * 10) div 100) - 1.00))) or (not(xs:decimal(cbc:PrepaidAmount)) and xs:decimal(cbc:PayableRoundingAmount) and (round((xs:decimal(cbc:PayableAmount) - xs:decimal(cbc:PayableRoundingAmount)) * 10 * 10) div 100) <= (xs:decimal(cbc:TaxInclusiveAmount) + 1.00) and (round((xs:decimal(cbc:PayableAmount) - xs:decimal(cbc:PayableRoundingAmount)) * 10 * 10) div 100) >= (xs:decimal(cbc:TaxInclusiveAmount) - 1.00))"},
{"id":"DT-CIUS-PT-159","texto":"The BT-99 must equal the multiplication between the Document level charge base amount (BT-100) and the Document level charge percentage (BT-101), with an acceptance range of 1.00 € (it does not mean that this tolerance is accepted by the customer).","categoria":"calculo","natureza":"FN","gravidade":"erro","contexto":"Document_level_charges ","elementos":["BT-99","BT-100","BT-101"],"expressao":"(not(exists(xs:decimal(cbc:MultiplierFactorNumeric))) and not(exists(xs:decimal(cbc:BaseAmount)))) or (((xs:decimal(cbc:BaseAmount) * (xs:decimal(cbc:MultiplierFactorNumeric) div 100) * 10 * 10) div 100) <= (xs:decimal(cbc:Amount) + 1.00) and ((xs:decimal(cbc:BaseAmount) * (xs:decimal(cbc:MultiplierFactorNumeric) div 100) * 10 * 10) div 100) >= (xs:decimal(cbc:Amount) - 1.00))"},
{"id":"DT-CIUS-PT-158","texto":"The BT-92 must equal the multiplication between the Document level allowance base amount (BT-93) and the Document level allowance percentage (BT-94), with an acceptance range of 1.00 € (it does not mean that this tolerance is accepted by the customer).","categoria":"calculo","natureza":"FN","gravidade":"erro","contexto":"Document_level_allowances ","elementos":["BT-92","BT-93","BT-94"],"expressao":"(not(exists(xs:decimal(cbc:MultiplierFactorNumeric))) and not(exists(xs:decimal(cbc:BaseAmount)))) or (((xs:decimal(cbc:BaseAmount) * (xs:decimal(cbc:MultiplierFactorNumeric) div 100) * 10 * 10) div 100) <= (xs:decimal(cbc:Amount) + 1.00) and ((xs:decimal(cbc:BaseAmount) * (xs:decimal(cbc:MultiplierFactorNumeric) div 100) * 10 * 10) div 100) >= (xs:decimal(cbc:Amount) - 1.00))"},
{"id":"DT-CIUS-PT-167","texto":"VAT category tax amount (BT-117) = VAT category taxable amount (BT-116) x (VAT category rate (BT-119) / 100), rounded to two decimals and with an acceptance range of 1.00 € (it does not mean that this tolerance is accepted by the customer).","categoria":"calculo","natureza":"FN","gravidade":"erro","contexto":"VAT_breakdown ","elementos":["BT-116","BT-117","BT-119"],"expressao":"(round(cac:TaxCategory/xs:decimal(cbc:Percent)) = 0 and (round(xs:decimal(cbc:TaxAmount)) = 0)) or (round(cac:TaxCategory/xs:decimal(cbc:Percent)) != 0 and ((round(xs:decimal(cbc:TaxableAmount) * (cac:TaxCategory/xs:decimal(cbc:Percent) div 100) * 10 * 10) div 100 ) <= (xs:decimal(cbc:TaxAmount) + 1.00)) and ((round(xs:decimal(cbc:TaxableAmount) * (cac:TaxCategory/xs:decimal(cbc:Percent) div 100) * 10 * 10) div 100 ) >= (xs:decimal(cbc:TaxAmount) - 1.00))) or (not(exists(cac:TaxCategory/xs:decimal(cbc:Percent))) and (round(xs:decimal(cbc:TaxAmount)) = 0))"},
{"id":"DT-CIUS-PT-171","texto":"For each different value of VAT category rate (BT-119) where the VAT category code (BT-118) is \"Lower rate\", the VAT category taxable amount (BT-116) in a VATBReakdown (BG-23) shall equal the sum of Invoice line net amounts (BT-131) plus the sum of document level charge amounts (BT-99) minus the sum of document level allowance amounts (BT-92) where the VAT category code (BT-151, BT-102, BT-95) is “Lower rate” and the VAT rate (BT-152, BT-103, BT-96) equals the VAT category rate (BT-119), with an acceptance range of 1.00 € (it does not mean that this tolerance is accepted by the customer).","categoria":"condicional","natureza":"RIR","gravidade":"erro","contexto":"VATAA ","elementos":["BG-23","BT-92","BT-95","BT-96","BT-99","BT-102","BT-103","BT-116","BT-118","BT-119","BT-131","BT-151","BT-152"],"expressao":"every $rate in round(cbc:Percent) satisfies ((exists(//cac:InvoiceLine) and ((round((sum(../../../cac:InvoiceLine[normalize-space(cac:Item/cac:ClassifiedTaxCategory/cbc:ID)='AA' or normalize-space(cac:Item/cac:ClassifiedTaxCategory/cbc:ID)='RED' or  normalize-space(cac:Item/cac:ClassifiedTaxCategory/cbc:ID)='INT'][cac:Item/cac:ClassifiedTaxCategory/cbc:Percent=$rate]/xs:decimal(cbc:LineExtensionAmount)) + sum(../../../cac:AllowanceCharge[cbc:ChargeIndicator='true'][normalize-space(cac:TaxCategory/cbc:ID)='AA' or normalize-space(cac:TaxCategory/cbc:ID)='RED' or normalize-space(cac:TaxCategory/cbc:ID)='INT'][cac:TaxCategory/cbc:Percent=$rate]/xs:decimal(cbc:Amount)) - sum(../../../cac:AllowanceCharge[cbc:ChargeIndicator='false'][normalize-space(cac:TaxCategory/cbc:ID)='AA' or normalize-space(cac:TaxCategory/cbc:ID)='RED' or normalize-space(cac:TaxCategory/cbc:ID)='INT'][cac:TaxCategory/cbc:Percent=$rate]/xs:decimal(cbc:Amount))) * 100) div 100) <= (xs:decimal(../cbc:TaxableAmount) + 1.00) and (round((sum(../../../cac:InvoiceLine[normalize-space(cac:Item/cac:ClassifiedTaxCategory/cbc:ID)='AA' or normalize-space(cac:Item/cac:ClassifiedTaxCategory/cbc:ID)='RED' or normalize-space(cac:Item/cac:ClassifiedTaxCategory/cbc:ID)='INT'][cac:Item/cac:ClassifiedTaxCategory/cbc:Percent=$rate]/xs:decimal(cbc:LineExtensionAmount)) + sum(../../../cac:AllowanceCharge[cbc:ChargeIndicator='true'][normalize-space(cac:TaxCategory/cbc:ID)='AA' or normalize-space(cac:TaxCategory/cbc:ID)='RED' or normalize-space(cac:TaxCategory/cbc:ID)='INT'][cac:TaxCategory/cbc:Percent=$rate]/xs:decimal(cbc:Amount)) - sum(../../../cac:AllowanceCharge[cbc:ChargeIndicator='false'][normalize-space(cac:TaxCategory/cbc:ID)='AA' or normalize-space(cac:TaxCategory/cbc:ID)='RED' or normalize-space(cac:TaxCategory/cbc:ID)='INT'][cac:TaxCategory/cbc:Percent=$rate]/xs:decimal(cbc:Amount))) * 100) div 100) >=(xs:decimal(../cbc:TaxableAmount) - 1.00))) or (exists(//cac:CreditNoteLine) and ( ((round((sum(../../../cac:CreditNoteLine[normalize-space(cac:Item/cac:ClassifiedTaxCategory/cbc:ID)='AA' or normalize-space(cac:Item/cac:ClassifiedTaxCategory/cbc:ID)='RED' or normalize-space(cac:Item/cac:ClassifiedTaxCategory/cbc:ID)='INT'][cac:Item/cac:ClassifiedTaxCategory/cbc:Percent=$rate]/xs:decimal(cbc:LineExtensionAmount)) + sum(../../../cac:AllowanceCharge[cbc:ChargeIndicator='true'][normalize-space(cac:TaxCategory/cbc:ID)='AA' or normalize-space(cac:TaxCategory/cbc:ID)='RED' or normalize-space(cac:TaxCategory/cbc:ID)='INT'][cac:TaxCategory/cbc:Percent=$rate]/xs:decimal(cbc:Amount)) - sum(../../../cac:AllowanceCharge[cbc:ChargeIndicator='false'][normalize-space(cac:TaxCategory/cbc:ID)='AA' or normalize-space(cac:TaxCategory/cbc:ID)='RED' or normalize-space(cac:TaxCategory/cbc:ID)='INT'][cac:TaxCategory/cbc:Percent=$rate]/xs:decimal(cbc:Amount))) * 100) div 100) <= (xs:decimal(../cbc:TaxableAmount) + 1.00) and (round((sum(../../../cac:CreditNoteLine[normalize-space(cac:Item/cac:ClassifiedTaxCategory/cbc:ID)='AA' or normalize-space(cac:Item/cac:ClassifiedTaxCategory/cbc:ID)='RED' or normalize-space(cac:Item/cac:ClassifiedTaxCategory/cbc:ID)='INT'][cac:Item/cac:ClassifiedTaxCategory/cbc:Percent=$rate]/xs:decimal(cbc:LineExtensionAmount)) + sum(../../../cac:AllowanceCharge[cbc:ChargeIndicator='true'][normalize-space(cac:TaxCategory/cbc:ID)='AA' or normalize-space(cac:TaxCategory/cbc:ID)='RED' or normalize-space(cac:TaxCategory/cbc:ID)='INT'][cac:TaxCategory/cbc:Percent=$rate]/xs:decimal(cbc:Amount)) - sum(../../../cac:AllowanceCharge[cbc:ChargeIndicator='false'][normalize-space(cac:TaxCategory/cbc:ID)='AA' or normalize-space(cac:TaxCategory/cbc:ID)='RED' or normalize-space(cac:TaxCategory/cbc:ID)='INT'][cac:TaxCategory/cbc:Percent=$rate]/xs:decimal(cbc:Amount))) * 100) div 100) >=(xs:decimal(../cbc:TaxableAmount) - 1.00)))))"},
{"id":"DT-CIUS-PT-172","texto":"The VAT category tax amount (BT-117) in a VATBReakdown (BG-23) where VAT category code (BT-118) is \"Lower rate\" shall equal the VAT category taxable amount (BT-116) multiplied by the VAT category rate (BT-119), with an acceptance range of 1.00 € (it does not mean that this tolerance is accepted by the customer).","categoria":"calculo","natureza":"FN","gravidade":"erro","contexto":"VATAA ","elementos":["BG-23","BT-116","BT-117","BT-118","BT-119"],"expressao":"((round((xs:decimal(../cbc:TaxableAmount) * (xs:decimal(cbc:Percent) div 100)) * 10 * 10) div 100) <= (xs:decimal(../cbc:TaxAmount) + 1.00) and (round((xs:decimal(../cbc:TaxableAmount) * (xs:decimal(cbc:Percent) div 100)) * 10 * 10) div 100) >= (xs:decimal(../cbc:TaxAmount) - 1.00))"},
{"id":"BR-CIUS-PT-12","texto":"A VATBReakdown (BG-23) with VAT Category code (BT-118) \"Lower rate\" the VAT category rate (BT-119) shall be greater than zero.","categoria":"gama","natureza":"RP","gravidade":"erro","contexto":"VATAA ","elementos":["BG-23","BT-118","BT-119"],"expressao":"(cbc:Percent) > 0"},
{"id":"BR-AA-06","texto":"In a Document level allowance (BG-20) where the Document level allowance VAT category code (BT-95) is \"Lower rate\" the Document level allowance VAT rate (BT-96) shall be greater than zero.","categoria":"condicional","natureza":"RIR","gravidade":"erro","contexto":"VATAA_Allowance ","elementos":["BG-20","BT-95","BT-96"],"expressao":"(cbc:Percent) > 0"},
{"id":"BR-AA-07","texto":"In a Document level charge (BG-21) where the Document level charge VAT category code (BT-102) is \"Lower rate\" the Document level charge VAT rate (BT-103) shall be greater than zero.","categoria":"condicional","natureza":"RIR","gravidade":"erro","contexto":"VATAA_Charge ","elementos":["BG-21","BT-102","BT-103"],"expressao":"(cbc:Percent) > 0"},
{"id":"DT-CIUS-PT-173","texto":"For each different value of VAT category rate (BT-119) where the VAT category code (BT-118) is \"Standard rated\", the VAT category taxable amount (BT-116) in a VATBReakdown (BG-23) shall equal the sum of Invoice line net amounts (BT-131) plus the sum of document level charge amounts (BT-99) minus the sum of document level allowance amounts (BT-92) where the VAT category code (BT-151, BT-102, BT-95) is “Standard rated” and the VAT rate (BT-152, BT-103, BT-96) equals the VAT category rate (BT-119), with an acceptance range of 1.00 € (it does not mean that this tolerance is accepted by the customer).","categoria":"condicional","natureza":"RIR","gravidade":"erro","contexto":"VATS ","elementos":["BG-23","BT-92","BT-95","BT-96","BT-99","BT-102","BT-103","BT-116","BT-118","BT-119","BT-131","BT-151","BT-152"],"expressao":"every $rate in round(cbc:Percent) satisfies ((exists(//cac:InvoiceLine) and ((round((sum(../../../cac:InvoiceLine[normalize-space(cac:Item/cac:ClassifiedTaxCategory/cbc:ID)='S' or normalize-space(cac:Item/cac:ClassifiedTaxCategory/cbc:ID)='NOR'][cac:Item/cac:ClassifiedTaxCategory/cbc:Percent=$rate]/xs:decimal(cbc:LineExtensionAmount)) + sum(../../../cac:AllowanceCharge[cbc:ChargeIndicator='true'][normalize-space(cac:TaxCategory/cbc:ID)='S' or normalize-space(cac:TaxCategory/cbc:ID)='NOR'][cac:TaxCategory/cbc:Percent=$rate]/xs:decimal(cbc:Amount)) - sum(../../../cac:AllowanceCharge[cbc:ChargeIndicator='false'][normalize-space(cac:TaxCategory/cbc:ID)='S' or normalize-space(cac:TaxCategory/cbc:ID)='NOR'][cac:TaxCategory/cbc:Percent=$rate]/xs:decimal(cbc:Amount))) * 100) div 100) <= (xs:decimal(../cbc:TaxableAmount) + 1.00) and (round((sum(../../../cac:InvoiceLine[normalize-space(cac:Item/cac:ClassifiedTaxCategory/cbc:ID)='S' or normalize-space(cac:Item/cac:ClassifiedTaxCategory/cbc:ID)='NOR'][cac:Item/cac:ClassifiedTaxCategory/cbc:Percent=$rate]/xs:decimal(cbc:LineExtensionAmount)) + sum(../../../cac:AllowanceCharge[cbc:ChargeIndicator='true'][normalize-space(cac:TaxCategory/cbc:ID)='S' or normalize-space(cac:TaxCategory/cbc:ID)='NOR'][cac:TaxCategory/cbc:Percent=$rate]/xs:decimal(cbc:Amount)) - sum(../../../cac:AllowanceCharge[cbc:ChargeIndicator='false'][normalize-space(cac:TaxCategory/cbc:ID)='S' or normalize-space(cac:TaxCategory/cbc:ID)='NOR'][cac:TaxCategory/cbc:Percent=$rate]/xs:decimal(cbc:Amount))) * 100) div 100) >=(xs:decimal(../cbc:TaxableAmount) - 1.00))) or (exists(//cac:CreditNoteLine) and ( ((round((sum(../../../cac:CreditNoteLine[normalize-space(cac:Item/cac:ClassifiedTaxCategory/cbc:ID)='S' or normalize-space(cac:Item/cac:ClassifiedTaxCategory/cbc:ID)='NOR'][cac:Item/cac:ClassifiedTaxCategory/cbc:Percent=$rate]/xs:decimal(cbc:LineExtensionAmount)) + sum(../../../cac:AllowanceCharge[cbc:ChargeIndicator='true'][normalize-space(cac:TaxCategory/cbc:ID)='S' or normalize-space(cac:TaxCategory/cbc:ID)='NOR'][cac:TaxCategory/cbc:Percent=$rate]/xs:decimal(cbc:Amount)) - sum(../../../cac:AllowanceCharge[cbc:ChargeIndicator='false'][normalize-space(cac:TaxCategory/cbc:ID)='S' or normalize-space(cac:TaxCategory/cbc:ID)='NOR'][cac:TaxCategory/cbc:Percent=$rate]/xs:decimal(cbc:Amount))) * 100) div 100) <= (xs:decimal(../cbc:TaxableAmount) + 1.00) and (round((sum(../../../cac:CreditNoteLine[normalize-space(cac:Item/cac:ClassifiedTaxCategory/cbc:ID)='S' or normalize-space(cac:Item/cac:ClassifiedTaxCategory/cbc:ID)='NOR'][cac:Item/cac:ClassifiedTaxCategory/cbc:Percent=$rate]/xs:decimal(cbc:LineExtensionAmount)) + sum(../../../cac:AllowanceCharge[cbc:ChargeIndicator='true'][normalize-space(cac:TaxCategory/cbc:ID)='S' or normalize-space(cac:TaxCategory/cbc:ID)='NOR'][cac:TaxCategory/cbc:Percent=$rate]/xs:decimal(cbc:Amount)) - sum(../../../cac:AllowanceCharge[cbc:ChargeIndicator='false'][normalize-space(cac:TaxCategory/cbc:ID)='S' or normalize-space(cac:TaxCategory/cbc:ID)='NOR'][cac:TaxCategory/cbc:Percent=$rate]/xs:decimal(cbc:Amount))) * 100) div 100) >=(xs:decimal(../cbc:TaxableAmount) - 1.00)))))"},
{"id":"DT-CIUS-PT-174","texto":"The VAT category tax amount (BT-117) in a VATBReakdown (BG-23) where VAT category code (BT-118) is \"Standard rated\" shall equal the VAT category taxable amount (BT-116) multiplied by the VAT category rate (BT-119), with an acceptance range of 1.00 € (it does not mean that this tolerance is accepted by the customer).","categoria":"calculo","natureza":"FN","gravidade":"erro","contexto":"VATS ","elementos":["BG-23","BT-116","BT-117","BT-118","BT-119"],"expressao":"((round((xs:decimal(../cbc:TaxableAmount) * (xs:decimal(cbc:Percent) div 100)) * 10 * 10) div 100) <= (xs:decimal(../cbc:TaxAmount) + 1.00) and (round((xs:decimal(../cbc:TaxableAmount) * (xs:decimal(cbc:Percent) div 100)) * 10 * 10) div 100) >= (xs:decimal(../cbc:TaxAmount) - 1.00))"},
{"id":"BR-CIUS-PT-14","texto":"A VATBReakdown (BG-23) with VAT Category code (BT-118) \"Standard rate\" the VAT category rate (BT-119) shall be greater than zero.","categoria":"gama","natureza":"RP","gravidade":"erro","contexto":"VATS ","elementos":["BG-23","BT-118","BT-119"],"expressao":"(cbc:Percent) > 0"},
{"id":"BR-S-06","texto":"In a Document level allowance (BG-20) where the Document level allowance VAT category code (BT-95) is \"Standard rated\" the Document level allowance VAT rate (BT-96) shall be greater than zero.","categoria":"condicional","natureza":"RIR","gravidade":"erro","contexto":"VATS_Allowance ","elementos":["BG-20","BT-95","BT-96"],"expressao":"(cbc:Percent) > 0"},
{"id":"BR-S-07","texto":"In a Document level charge (BG-21) where the Document level charge VAT category code (BT-102) is \"Standard rated\" the Document level charge VAT rate (BT-103) shall be greater than zero.","categoria":"condicional","natureza":"RIR","gravidade":"erro","contexto":"VATS_Charge ","elementos":["BG-21","BT-102","BT-103"],"expressao":"(cbc:Percent) > 0"},
{"id":"BR-E-09","texto":"The VAT category tax amount (BT-117) In a VATBReakdown (BG-23) where the VAT category code (BT-118) equals \"Exempt from VAT\" shall equal 0 (zero).","categoria":"condicional","natureza":"RIR","gravidade":"erro","contexto":"VATE ","elementos":["BG-23","BT-117","BT-118"],"expressao":"../cbc:TaxAmount = 0"},
{"id":"BR-CIUS-PT-16","texto":"A VATBReakdown (BG-23) with VAT Category code (BT-118) \"Exempt from VAT\" the VAT category rate (BT-119) shall be 0 (zero).","categoria":"outra","natureza":"?","gravidade":"erro","contexto":"VATE ","elementos":["BG-23","BT-118","BT-119"],"expressao":"(cbc:Percent = 0)"},
{"id":"BR-E-06","texto":"In a Document level allowance (BG-20) where the Document level allowance VAT category code (BT-95) is \"Exempt from VAT\", the Document level allowance VAT rate (BT-96) shall be 0 (zero).","categoria":"condicional","natureza":"RIR","gravidade":"erro","contexto":"VATE_Allowance ","elementos":["BG-20","BT-95","BT-96"],"expressao":"(cbc:Percent = 0)"},
{"id":"BR-E-07","texto":"In a Document level charge (BG-21) where the Document level charge VAT category code (BT-102) is \"Exempt from VAT\", the Document level charge VAT rate (BT-103) shall be 0 (zero).","categoria":"condicional","natureza":"RIR","gravidade":"erro","contexto":"VATE_Charge ","elementos":["BG-21","BT-102","BT-103"],"expressao":"(cbc:Percent = 0)"},
{"id":"DT-CIUS-PT-169","texto":"The BT-141 must equal the multiplication between the Invoice line charge base amount (BT-142) and the Invoice line charge percentage (BT-143), with an acceptance range of 1.00 € (it does not mean that this tolerance is accepted by the customer).","categoria":"calculo","natureza":"FN","gravidade":"erro","contexto":"Invoice_line_charges ","elementos":["BT-141","BT-142","BT-143"],"expressao":"(not(exists(xs:decimal(cbc:MultiplierFactorNumeric))) and not(exists(xs:decimal(cbc:BaseAmount)))) or (((xs:decimal(cbc:BaseAmount) * (xs:decimal(cbc:MultiplierFactorNumeric) div 100) * 10 * 10) div 100) <= (xs:decimal(cbc:Amount) + 1.00) and ((xs:decimal(cbc:BaseAmount) * (xs:decimal(cbc:MultiplierFactorNumeric) div 100) * 10 * 10) div 100) >= (xs:decimal(cbc:Amount) - 1.00))"},
{"id":"DT-CIUS-PT-168","texto":"The BT-136 must equal the multiplication between the Invoice line allowance base amount (BT-137) and the Invoice line allowance percentage (BT-138), with an acceptance range of 1.00 € (it does not mean that this tolerance is accepted by the customer).","categoria":"calculo","natureza":"FN","gravidade":"erro","contexto":"Invoice_line_allowances ","elementos":["BT-136","BT-137","BT-138"],"expressao":"(not(exists(xs:decimal(cbc:MultiplierFactorNumeric))) and not(exists(xs:decimal(cbc:BaseAmount)))) or (((xs:decimal(cbc:BaseAmount) * (xs:decimal(cbc:MultiplierFactorNumeric) div 100) * 10 * 10) div 100) <= (xs:decimal(cbc:Amount) + 1.00) and ((xs:decimal(cbc:BaseAmount) * (xs:decimal(cbc:MultiplierFactorNumeric) div 100) * 10 * 10) div 100) >= (xs:decimal(cbc:Amount) - 1.00))"},
{"id":"DT-CIUS-PT-170","texto":"The BT-146 must equal the grossPrice (Item gross price) minus the discount (Item price discount), with an acceptance range of 1.00 € (it does not mean that this tolerance is accepted by the customer).","categoria":"outra","natureza":"?","gravidade":"erro","contexto":"Invoice_Line_Price ","elementos":["BT-146"],"expressao":"(not(exists(cac:AllowanceCharge/xs:decimal(cbc:BaseAmount))) and not(exists(cac:AllowanceCharge/xs:decimal(cbc:Amount)))) or ((cac:AllowanceCharge/xs:decimal(cbc:BaseAmount) - (cac:AllowanceCharge/xs:decimal(cbc:Amount))) <= (xs:decimal(cbc:PriceAmount) + 1.00) and (cac:AllowanceCharge/xs:decimal(cbc:BaseAmount) - (cac:AllowanceCharge/xs:decimal(cbc:Amount)))  >= (xs:decimal(cbc:PriceAmount) - 1.00))"},
{"id":"BR-AA-05","texto":"In a Line VAT Information (BG-30) where the Invoiced item VAT category code (BT-151) is \"Lower rate\" the Invoiced item VAT rate (BT-152) shall be greater than zero.","categoria":"condicional","natureza":"RIR","gravidade":"erro","contexto":"VATAA_Line ","elementos":["BG-30","BT-151","BT-152"],"expressao":"(cbc:Percent) > 0"},
{"id":"BR-S-05","texto":"In an Invoice line (BG-25) where the Invoiced item VAT category code (BT-151) is \"Standard rated\" the Invoiced item VAT rate (BT-152) shall be greater than zero.","categoria":"condicional","natureza":"RIR","gravidade":"erro","contexto":"VATS_Line ","elementos":["BG-25","BT-151","BT-152"],"expressao":"(cbc:Percent) > 0"},
{"id":"BR-E-05","texto":"In an Invoice line (BG-25) where the Invoiced item VAT category code (BT-151) is \"Exempt from VAT\", the Invoiced item VAT rate (BT-152) shall be 0 (zero).","categoria":"condicional","natureza":"RIR","gravidade":"erro","contexto":"VATE_Line ","elementos":["BG-25","BT-151","BT-152"],"expressao":"(cbc:Percent = 0)"},
{"id":"BR-52","texto":"Each Additional supporting document (BG-24) shall contain a Supporting document reference (BT-122).","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"Additional_supporting_documents","elementos":["BG-24","BT-122"],"expressao":"exists(cbc:ID)"},
{"id":"BR-CIUS-PT-30","texto":"If Additional Supporting Documents (BG-24) is used, the External document location (BT-124) or the Attached document (BT-125) shall be filled, or both.","categoria":"condicional","natureza":"RIR","gravidade":"erro","contexto":"Additional_supporting_documents","elementos":["BG-24","BT-124","BT-125"],"expressao":"report (dispara quando verdadeiro): exists(cac:Attachment) and (not(cac:Attachment/cbc:EmbeddedDocumentBinaryObject) and not(cac:Attachment/cac:ExternalReference/cbc:URI))"},
{"id":"BR-CIUS-PT-38","texto":"The Buyer identifier (BT-46) shall be filled.","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"Buyer","elementos":["BT-46"],"expressao":"report (dispara quando verdadeiro): exists(cac:Party/cac:PartyIdentification) and not(cac:Party/cac:PartyIdentification/cbc:ID)"},
{"id":"BR-CIUS-PT-39","texto":"The Buyer trading name (BT-45) shall be filled.","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"Buyer","elementos":["BT-45"],"expressao":"report (dispara quando verdadeiro): exists(cac:Party/cac:PartyName) and not(cac:Party/cac:PartyName/cbc:Name)"},
{"id":"BR-CIUS-PT-40","texto":"The Buyer contact point (BT-56) or the Buyer contact telephone number (BT-57) or the Buyer contact email address (BT-58) shall be filled.","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"Buyer","elementos":["BT-56","BT-57","BT-58"],"expressao":"report (dispara quando verdadeiro): exists(cac:Party/cac:Contact) and (not(cac:Party/cac:Contact/cbc:Name) and not(cac:Party/cac:Contact/cbc:Telephone) and not(cac:Party/cac:Contact/cbc:ElectronicMail))"},
{"id":"BR-63","texto":"The Buyer electronic address (BT-49) shall have a Scheme identifier.","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"Buyer_electronic_address","elementos":["BT-49"],"expressao":"exists(@schemeID)"},
{"id":"BR-11","texto":"The Buyer postal address shall contain a Buyer country code (BT-55).","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"Buyer_postal_address","elementos":["BT-55"],"expressao":"exists(cac:Country/cbc:IdentificationCode)"},
{"id":"BR-CIUS-PT-41","texto":"The Buyer address line 3 (BT-163) shall be filled.","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"Buyer_postal_address","elementos":["BT-163"],"expressao":"report (dispara quando verdadeiro): exists(cac:AddressLine) and not(cac:AddressLine/cbc:Line)"},
{"id":"BR-CIUS-PT-29","texto":"The Contract reference (BT-12) shall be filled.","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"Contract_Document_Reference","elementos":["BT-12"],"expressao":"exists(cbc:ID)"},
{"id":"BR-CIUS-PT-46","texto":"The Deliver to party name (BT-70) shall be filled.","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"Delivery","elementos":["BT-70"],"expressao":"report (dispara quando verdadeiro): (exists(cac:DeliveryParty) and not(cac:DeliveryParty/cac:PartyName)) or (exists(cac:DeliveryParty/cac:PartyName) and not(cac:DeliveryParty/cac:PartyName/cbc:Name))"},
{"id":"BR-CIUS-PT-64","texto":"The Actual delivery date (BT-72) or the Deliver to location identifier (BT-71) or the Deliver to Address (BG-15) or the Deliver to party name (BT-70) shall be filled.","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"Delivery","elementos":["BG-15","BT-70","BT-71","BT-72"],"expressao":"exists(cbc:ActualDeliveryDate) or exists(cac:DeliveryParty) or exists(cac:DeliveryLocation/cbc:ID) or exists(cac:DeliveryLocation/cac:Address)"},
{"id":"BR-CIUS-PT-21","texto":"Each Deliver to address (BG-15) shall contain a Seller address line 1 (BT-75).","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"Deliver_to_address","elementos":["BG-15","BT-75"],"expressao":"exists(cbc:StreetName)"},
{"id":"BR-CIUS-PT-22","texto":"Each Deliver to address (BG-15) shall contain a Seller city (BT-77).","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"Deliver_to_address","elementos":["BG-15","BT-77"],"expressao":"exists(cbc:CityName)"},
{"id":"BR-CIUS-PT-23","texto":"Each Deliver to address (BG-15) shall contain a Seller post code (BT-78).","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"Deliver_to_address","elementos":["BG-15","BT-78"],"expressao":"exists(cbc:PostalZone)"},
{"id":"BR-57","texto":"Each Deliver to address (BG-15) shall contain a Deliver to country code (BT-80).","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"Deliver_to_address","elementos":["BG-15","BT-80"],"expressao":"exists(cac:Country/cbc:IdentificationCode)"},
{"id":"BR-CIUS-PT-45","texto":"The Deliver to address line 3 (BT-165) shall be filled.","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"Deliver_to_address","elementos":["BT-165"],"expressao":"report (dispara quando verdadeiro): exists(cac:AddressLine) and not(cac:AddressLine/cbc:Line)"},
{"id":"BR-CIUS-PT-26","texto":"The Despatch advice reference (BT-16) shall be filled.","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"Despatch_Document_Reference","elementos":["BT-16"],"expressao":"exists(cbc:ID)"},
{"id":"BR-31","texto":"Each Document level allowance (BG-20) shall have a Document level allowance amount (BT-92).","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"Document_level_allowances","elementos":["BG-20","BT-92"],"expressao":"exists(cbc:Amount) "},
{"id":"BR-32","texto":"Each Document level allowance (BG-20) shall have a Document level allowance VAT category code (BT-95).","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"Document_level_allowances","elementos":["BG-20","BT-95"],"expressao":"exists(cac:TaxCategory/cbc:ID)"},
{"id":"BR-33","texto":"Each Document level allowance (BG-20) shall have a Document level allowance reason (BT-97) or a Document level allowance reason code (BT-98).","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"Document_level_allowances","elementos":["BG-20","BT-97","BT-98"],"expressao":"exists(cbc:AllowanceChargeReason) or exists(cbc:AllowanceChargeReasonCode)"},
{"id":"BR-CO-21","texto":"Each Document level allowance (BG-20) shall contain a Document level allowance reason (BT-97) or a Document level allowance reason code (BT-98), or both.","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"Document_level_allowances","elementos":["BG-20","BT-97","BT-98"],"expressao":"exists(cbc:AllowanceChargeReason) or exists(cbc:AllowanceChargeReasonCode)"},
{"id":"BR-CIUS-PT-19","texto":"Each Document level allowance (BG-20) shall have a tax scheme.","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"Document_level_allowances","elementos":["BG-20"],"expressao":"exists(cac:TaxCategory/cac:TaxScheme/cbc:ID)"},
{"id":"BR-36","texto":"Each Document level charge (BG-21) shall have a Document level charge amount (BT-99).","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"Document_level_charges","elementos":["BG-21","BT-99"],"expressao":"exists(cbc:Amount)"},
{"id":"BR-37","texto":"Each Document level charge (BG-21) shall have a Document level charge VAT category code (BT-102).","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"Document_level_charges","elementos":["BG-21","BT-102"],"expressao":"exists(cac:TaxCategory/cbc:ID)"},
{"id":"BR-38","texto":"Each Document level charge (BG-21) shall have a Document level charge reason (BT-104) or a Document level charge reason code (BT-105).","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"Document_level_charges","elementos":["BG-21","BT-104","BT-105"],"expressao":"exists(cbc:AllowanceChargeReason) or exists(cbc:AllowanceChargeReasonCode)"},
{"id":"BR-CO-22","texto":"Each Document level charge (BG-21) shall contain a Document level charge reason (BT-104) or a Document level charge reason code (BT-105), or both.","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"Document_level_charges","elementos":["BG-21","BT-104","BT-105"],"expressao":"exists(cbc:AllowanceChargeReason) or exists(cbc:AllowanceChargeReasonCode)"},
{"id":"BR-CIUS-PT-20","texto":"Each Document level charge (BG-21) shall have a tax scheme.","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"Document_level_charges","elementos":["BG-21"],"expressao":"exists(cac:TaxCategory/cac:TaxScheme/cbc:ID)"},
{"id":"BR-12","texto":"An Invoice shall have the Sum of Invoice line net amount (BT-106).","categoria":"calculo","natureza":"FN","gravidade":"erro","contexto":"Document_totals","elementos":["BT-106"],"expressao":"exists(cbc:LineExtensionAmount)"},
{"id":"BR-13","texto":"An Invoice shall have the Invoice total amount without VAT (BT-109).","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"Document_totals","elementos":["BT-109"],"expressao":"exists(cbc:TaxExclusiveAmount)"},
{"id":"BR-14","texto":"An Invoice shall have the Invoice total amount with VAT (BT-112).","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"Document_totals","elementos":["BT-112"],"expressao":"exists(cbc:TaxInclusiveAmount)"},
{"id":"BR-15","texto":"An Invoice shall have the Amount due for payment (BT-115).","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"Document_totals","elementos":["BT-115"],"expressao":"exists(cbc:PayableAmount)"},
{"id":"BR-CIUS-PT-62","texto":"If Document Level Allowances (BG-20) is used, the Sum of allowances on document level (BT-107) shall be filled.","categoria":"condicional","natureza":"RIR","gravidade":"erro","contexto":"Document_totals","elementos":["BG-20","BT-107"],"expressao":"report (dispara quando verdadeiro): exists(/*/cac:AllowanceCharge[cbc:ChargeIndicator='false']) and not(cbc:AllowanceTotalAmount)"},
{"id":"BR-CIUS-PT-63","texto":"If Document Level Charges (BG-21) is used, the Sum of charges on document level (BT-108) shall be filled.","categoria":"condicional","natureza":"RIR","gravidade":"erro","contexto":"Document_totals","elementos":["BG-21","BT-108"],"expressao":"report (dispara quando verdadeiro): exists(/*/cac:AllowanceCharge[cbc:ChargeIndicator='true']) and not(cbc:ChargeTotalAmount)"},
{"id":"BR-01","texto":"An Invoice shall have a Specification identifier (BT-24).","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"Invoice","elementos":["BT-24"],"expressao":"exists(cbc:CustomizationID)"},
{"id":"BR-02","texto":"An Invoice shall have an Invoice number (BT-1).","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"Invoice","elementos":["BT-1"],"expressao":"exists(cbc:ID)"},
{"id":"BR-03","texto":"An Invoice shall have an Invoice issue date (BT-2).","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"Invoice","elementos":["BT-2"],"expressao":"exists(cbc:IssueDate)"},
{"id":"BR-04","texto":"An Invoice shall have an Invoice type code (BT-3).","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"Invoice","elementos":["BT-3"],"expressao":"exists(cbc:InvoiceTypeCode) or exists(cbc:CreditNoteTypeCode)"},
{"id":"BR-05","texto":"An Invoice shall have an Invoice currency code (BT-5).","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"Invoice","elementos":["BT-5"],"expressao":"exists(cbc:DocumentCurrencyCode)"},
{"id":"BR-06","texto":"An Invoice shall contain the Seller name (BT-27).","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"Invoice","elementos":["BT-27"],"expressao":"exists(cac:AccountingSupplierParty/cac:Party/cac:PartyLegalEntity/cbc:RegistrationName)"},
{"id":"BR-CIUS-PT-01","texto":"An Invoice shall contain the Seller VAT identifier (BT-31).","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"Invoice","elementos":["BT-31"],"expressao":"exists(cac:AccountingSupplierParty/cac:Party/cac:PartyTaxScheme/cbc:CompanyID)"},
{"id":"BR-CIUS-PT-02","texto":"An Invoice shall contain the Seller VAT tax scheme (VAT).","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"Invoice","expressao":"(cac:AccountingSupplierParty/cac:Party/cac:PartyTaxScheme/cac:TaxScheme/cbc:ID) = 'VAT'"},
{"id":"BR-07","texto":"An Invoice shall contain the Buyer name (BT-44).","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"Invoice","elementos":["BT-44"],"expressao":"exists(cac:AccountingCustomerParty/cac:Party/cac:PartyLegalEntity/cbc:RegistrationName)"},
{"id":"BR-CIUS-PT-03","texto":"An Invoice shall contain the Buyer VAT identifier (BT-48).","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"Invoice","elementos":["BT-48"],"expressao":"exists(cac:AccountingCustomerParty/cac:Party/cac:PartyTaxScheme/cbc:CompanyID)"},
{"id":"BR-CIUS-PT-04","texto":"An Invoice shall contain the Buyer VAT tax scheme (VAT).","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"Invoice","expressao":"(cac:AccountingCustomerParty/cac:Party/cac:PartyTaxScheme/cac:TaxScheme/cbc:ID) = 'VAT'"},
{"id":"BR-08","texto":"An Invoice shall contain the Seller postal address (BG-5).","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"Invoice","elementos":["BG-5"],"expressao":"exists(cac:AccountingSupplierParty/cac:Party/cac:PostalAddress)"},
{"id":"BR-10","texto":"An Invoice shall contain the Buyer postal address (BG-8).","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"Invoice","elementos":["BG-8"],"expressao":"exists(cac:AccountingCustomerParty/cac:Party/cac:PostalAddress)"},
{"id":"BR-16","texto":"An Invoice shall have at least one Invoice line (BG-25)","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"Invoice","elementos":["BG-25"],"expressao":"exists(cac:InvoiceLine) or exists(cac:CreditNoteLine)"},
{"id":"BR-CIUS-PT-10","texto":"An Invoice shall contain the Document Totals (BG-22).","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"Invoice","elementos":["BG-22"],"expressao":"exists(cac:LegalMonetaryTotal)"},
{"id":"BR-CIUS-PT-11","texto":"An Invoice shall contain the Total VAT amount (BT-110).","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"Invoice","elementos":["BT-110"],"expressao":"exists(cac:TaxTotal/cbc:TaxAmount)"},
{"id":"BR-CIUS-PT-25","texto":"A Credit Note shall contain the Preceding Invoice Reference (BG-3).","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"Invoice","elementos":["BG-3"],"expressao":"report (dispara quando verdadeiro): exists(//cn:CreditNote) and not(cac:BillingReference)"},
{"id":"BR-CO-03","texto":"Value added tax point date (BT-7) and Value added tax point date code (BT-8) are mutually exclusive.","categoria":"exclusao","natureza":"RIR","gravidade":"erro","contexto":"Invoice","elementos":["BT-7","BT-8"],"expressao":"(exists(cbc:TaxPointDate) and not(cac:InvoicePeriod/cbc:DescriptionCode)) or (not(cbc:TaxPointDate) and exists(cac:InvoicePeriod/cbc:DescriptionCode)) or (not(cbc:TaxPointDate) and not(cac:InvoicePeriod/cbc:DescriptionCode))"},
{"id":"BR-CO-18","texto":"An Invoice shall at least have one VATBReakdown group (BG-23).","categoria":"outra","natureza":"?","gravidade":"erro","contexto":"Invoice","elementos":["BG-23"],"expressao":"exists(cac:TaxTotal/cac:TaxSubtotal)"},
{"id":"BR-AA-02","texto":"An Invoice that contains an Invoice line (BG-25) where the Invoiced item VAT category code (BT-151) is “Lower rate” shall contain the Seller VAT Identifier (BT-31), the Seller tax registration identifier (BT-32) and/or the Seller tax representative VAT identifier (BT-63).","categoria":"condicional","natureza":"RIR","gravidade":"erro","contexto":"Invoice","elementos":["BG-25","BT-31","BT-32","BT-63","BT-151"],"expressao":"(exists(//cac:ClassifiedTaxCategory[(normalize-space(cbc:ID) = 'AA' or normalize-space(cbc:ID) = 'RED' or normalize-space(cbc:ID) = 'INT')]) and (exists(//cac:AccountingSupplierParty/cac:Party/cac:PartyTaxScheme/cbc:CompanyID) or exists(//cac:TaxRepresentativeParty/cac:PartyTaxScheme[cac:TaxScheme/cbc:ID = 'VAT']/cbc:CompanyID))) or not(exists(//cac:ClassifiedTaxCategory[(normalize-space(cbc:ID) = 'AA' or normalize-space(cbc:ID) = 'RED' or normalize-space(cbc:ID) = 'INT')]))"},
{"id":"BR-AA-03","texto":"An Invoice that contains a Document level allowance (BG-20) where the Document level allowance VAT category code (BT-95) is “Lower rate” shall contain the Seller VAT Identifier (BT-31), the Seller tax registration identifier (BT-32) and/or the Seller tax representative VAT identifier (BT-63).","categoria":"condicional","natureza":"RIR","gravidade":"erro","contexto":"Invoice","elementos":["BG-20","BT-31","BT-32","BT-63","BT-95"],"expressao":"(exists(//cac:AllowanceCharge[cbc:ChargeIndicator='false']/cac:TaxCategory[(normalize-space(cbc:ID) = 'AA' or normalize-space(cbc:ID) = 'RED' or normalize-space(cbc:ID) = 'INT')]) and (exists(//cac:AccountingSupplierParty/cac:Party/cac:PartyTaxScheme/cbc:CompanyID) or exists(//cac:TaxRepresentativeParty/cac:PartyTaxScheme[cac:TaxScheme/cbc:ID = 'VAT']/cbc:CompanyID))) or not(exists(//cac:AllowanceCharge[cbc:ChargeIndicator='false']/cac:TaxCategory[(normalize-space(cbc:ID) = 'AA' or normalize-space(cbc:ID) = 'RED' or normalize-space(cbc:ID) = 'INT')]))"},
{"id":"BR-AA-04","texto":"An Invoice that contains a Document level charge (BG-21) where the Document level charge VAT category code (BT-102) is “Lower rate” shall contain the Seller VAT Identifier (BT-31), the Seller tax registration identifier (BT-32) and/or the Seller tax representative VAT identifier (BT-63).","categoria":"condicional","natureza":"RIR","gravidade":"erro","contexto":"Invoice","elementos":["BG-21","BT-31","BT-32","BT-63","BT-102"],"expressao":"(exists(//cac:AllowanceCharge[cbc:ChargeIndicator='true']/cac:TaxCategory[(normalize-space(cbc:ID) = 'AA' or normalize-space(cbc:ID) = 'RED' or normalize-space(cbc:ID) = 'INT')]) and (exists(//cac:AccountingSupplierParty/cac:Party/cac:PartyTaxScheme/cbc:CompanyID) or exists(//cac:TaxRepresentativeParty/cac:PartyTaxScheme[cac:TaxScheme/cbc:ID = 'VAT']/cbc:CompanyID))) or not(exists(//cac:AllowanceCharge[cbc:ChargeIndicator='true']/cac:TaxCategory[(normalize-space(cbc:ID) = 'AA' or normalize-space(cbc:ID) = 'RED' or normalize-space(cbc:ID) = 'INT')]))"},
{"id":"BR-S-02","texto":"An Invoice that contains an Invoice line (BG-25) where the Invoiced item VAT category code (BT-151) is “Standard rated” shall contain the Seller VAT Identifier (BT-31), the Seller tax registration identifier (BT-32) and/or the Seller tax representative VAT identifier (BT-63).","categoria":"condicional","natureza":"RIR","gravidade":"erro","contexto":"Invoice","elementos":["BG-25","BT-31","BT-32","BT-63","BT-151"],"expressao":"(exists(//cac:ClassifiedTaxCategory[(normalize-space(cbc:ID) = 'S' or normalize-space(cbc:ID) = 'NOR')]) and (exists(//cac:AccountingSupplierParty/cac:Party/cac:PartyTaxScheme/cbc:CompanyID) or exists(//cac:TaxRepresentativeParty/cac:PartyTaxScheme[cac:TaxScheme/cbc:ID = 'VAT']/cbc:CompanyID))) or not(exists(//cac:ClassifiedTaxCategory[(normalize-space(cbc:ID) = 'S' or normalize-space(cbc:ID) = 'NOR')]))"},
{"id":"BR-S-03","texto":"An Invoice that contains a Document level allowance (BG-20) where the Document level allowance VAT category code (BT-95) is “Standard rated” shall contain the Seller VAT Identifier (BT-31), the Seller tax registration identifier (BT-32) and/or the Seller tax representative VAT identifier (BT-63).","categoria":"condicional","natureza":"RIR","gravidade":"erro","contexto":"Invoice","elementos":["BG-20","BT-31","BT-32","BT-63","BT-95"],"expressao":"(exists(//cac:AllowanceCharge[cbc:ChargeIndicator='false']/cac:TaxCategory[(normalize-space(cbc:ID) = 'S' or normalize-space(cbc:ID) = 'NOR')]) and (exists(//cac:AccountingSupplierParty/cac:Party/cac:PartyTaxScheme/cbc:CompanyID) or exists(//cac:TaxRepresentativeParty/cac:PartyTaxScheme[cac:TaxScheme/cbc:ID = 'VAT']/cbc:CompanyID))) or not(exists(//cac:AllowanceCharge[cbc:ChargeIndicator='false']/cac:TaxCategory[(normalize-space(cbc:ID) = 'S' or normalize-space(cbc:ID) = 'NOR')]))"},
{"id":"BR-S-04","texto":"An Invoice that contains a Document level charge (BG-21) where the Document level charge VAT category code (BT-102) is “Standard rated” shall contain the Seller VAT Identifier (BT-31), the Seller tax registration identifier (BT-32) and/or the Seller tax representative VAT identifier (BT-63).","categoria":"condicional","natureza":"RIR","gravidade":"erro","contexto":"Invoice","elementos":["BG-21","BT-31","BT-32","BT-63","BT-102"],"expressao":"(exists(//cac:AllowanceCharge[cbc:ChargeIndicator='true']/cac:TaxCategory[(normalize-space(cbc:ID) = 'S' or normalize-space(cbc:ID) = 'NOR')]) and (exists(//cac:AccountingSupplierParty/cac:Party/cac:PartyTaxScheme/cbc:CompanyID) or exists(//cac:TaxRepresentativeParty/cac:PartyTaxScheme[cac:TaxScheme/cbc:ID = 'VAT']/cbc:CompanyID))) or not(exists(//cac:AllowanceCharge[cbc:ChargeIndicator='true']/cac:TaxCategory[(normalize-space(cbc:ID) = 'S' or normalize-space(cbc:ID) = 'NOR')]))"},
{"id":"BR-E-02","texto":"An Invoice that contains an Invoice line (BG-25) where the Invoiced item VAT category code (BT-151) is “Exempt from VAT” shall contain the Seller VAT Identifier (BT-31), the Seller tax registration identifier (BT-32) and/or the Seller tax representative VAT identifier (BT-63).","categoria":"condicional","natureza":"RIR","gravidade":"erro","contexto":"Invoice","elementos":["BG-25","BT-31","BT-32","BT-63","BT-151"],"expressao":"(exists(//cac:ClassifiedTaxCategory[(normalize-space(cbc:ID) = 'E' or normalize-space(cbc:ID) = 'ISE')]) and (exists(//cac:AccountingSupplierParty/cac:Party/cac:PartyTaxScheme/cbc:CompanyID) or exists(//cac:TaxRepresentativeParty/cac:PartyTaxScheme[cac:TaxScheme/cbc:ID = 'VAT']/cbc:CompanyID))) or not(exists(//cac:ClassifiedTaxCategory[(normalize-space(cbc:ID) = 'E' or normalize-space(cbc:ID) = 'ISE')]))"},
{"id":"BR-E-03","texto":"An Invoice that contains a Document level allowance (BG-20) where the Document level allowance VAT category code (BT-95) is “Exempt from VAT” shall contain the Seller VAT Identifier (BT-31), the Seller tax registration identifier (BT-32) and/or the Seller tax representative VAT identifier (BT-63).","categoria":"condicional","natureza":"RIR","gravidade":"erro","contexto":"Invoice","elementos":["BG-20","BT-31","BT-32","BT-63","BT-95"],"expressao":"(exists(//cac:AllowanceCharge[cbc:ChargeIndicator='false']/cac:TaxCategory[(normalize-space(cbc:ID) = 'E' or normalize-space(cbc:ID) = 'ISE')]) and (exists(//cac:AccountingSupplierParty/cac:Party/cac:PartyTaxScheme/cbc:CompanyID) or exists(//cac:TaxRepresentativeParty/cac:PartyTaxScheme[cac:TaxScheme/cbc:ID = 'VAT']/cbc:CompanyID))) or not(exists(//cac:AllowanceCharge[cbc:ChargeIndicator='false']/cac:TaxCategory[(normalize-space(cbc:ID) = 'E' or normalize-space(cbc:ID) = 'ISE')]))"},
{"id":"BR-E-04","texto":"An Invoice that contains a Document level charge (BG-21) where the Document level charge VAT category code (BT-102) is “Exempt from VAT” shall contain the Seller VAT Identifier (BT-31), the Seller tax registration identifier (BT-32) and/or the Seller tax representative VAT identifier (BT-63).","categoria":"condicional","natureza":"RIR","gravidade":"erro","contexto":"Invoice","elementos":["BG-21","BT-31","BT-32","BT-63","BT-102"],"expressao":"(exists(//cac:AllowanceCharge[cbc:ChargeIndicator='true']/cac:TaxCategory[(normalize-space(cbc:ID) = 'E' or normalize-space(cbc:ID) = 'ISE')]) and (exists(//cac:AccountingSupplierParty/cac:Party/cac:PartyTaxScheme/cbc:CompanyID) or exists(//cac:TaxRepresentativeParty/cac:PartyTaxScheme[cac:TaxScheme/cbc:ID = 'VAT']/cbc:CompanyID))) or not(exists(//cac:AllowanceCharge[cbc:ChargeIndicator='true']/cac:TaxCategory[(normalize-space(cbc:ID) = 'E' or normalize-space(cbc:ID) = 'ISE')]))"},
{"id":"BR-CIUS-PT-65","texto":"An Invoice with type code equal to 383 or ND shall contain the Preceding Invoice Reference (BG-3).","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"Invoice","elementos":["BG-3"],"expressao":"report (dispara quando verdadeiro): ((cbc:InvoiceTypeCode = '383' or cbc:InvoiceTypeCode = 'ND') and not(cac:BillingReference))"},
{"id":"BR-CIUS-PT-66","texto":"An Invoice shall at least have one Deliver to address group (BG-15).","categoria":"outra","natureza":"?","gravidade":"erro","contexto":"Invoice","elementos":["BG-15"],"expressao":"exists(cac:Delivery/cac:DeliveryLocation/cac:Address)"},
{"id":"BR-21","texto":"Each Invoice line (BG-25) shall have an Invoice line identifier (BT-126).","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"Invoice_Line ","elementos":["BG-25","BT-126"],"expressao":"exists(cbc:ID)"},
{"id":"BR-22","texto":"Each Invoice line (BG-25) shall have an Invoiced quantity (BT-129).","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"Invoice_Line ","elementos":["BG-25","BT-129"],"expressao":"exists(cbc:InvoicedQuantity) or exists(cbc:CreditedQuantity)"},
{"id":"BR-23","texto":"An Invoice line (BG-25) shall have an Invoiced quantity unit of measure code (BT-130).","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"Invoice_Line ","elementos":["BG-25","BT-130"],"expressao":"report (dispara quando verdadeiro): (exists(cbc:InvoicedQuantity) and not(cbc:InvoicedQuantity/@unitCode)) or (exists(cbc:CreditedQuantity) and not(cbc:CreditedQuantity/@unitCode))"},
{"id":"BR-24","texto":"Each Invoice line (BG-25) shall have an Invoice line net amount (BT-131).","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"Invoice_Line ","elementos":["BG-25","BT-131"],"expressao":"exists(cbc:LineExtensionAmount)"},
{"id":"BR-25","texto":"Each Invoice line (BG-25) shall contain the Item name (BT-153).","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"Invoice_Line ","elementos":["BG-25","BT-153"],"expressao":"exists(cac:Item/cbc:Name)"},
{"id":"BR-26","texto":"Each Invoice line (BG-25) shall contain the Item net price (BT-146).","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"Invoice_Line ","elementos":["BG-25","BT-146"],"expressao":"exists(cac:Price/cbc:PriceAmount)"},
{"id":"BR-CIUS-PT-09","texto":"Each Invoice line (BG-25) shall have a tax scheme.","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"Invoice_Line ","elementos":["BG-25"],"expressao":"exists(cac:Item/cac:ClassifiedTaxCategory/cac:TaxScheme/cbc:ID)"},
{"id":"BR-CIUS-PT-51","texto":"The Referenced purchase order line reference (BT-132) shall be filled.","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"Invoice_Line ","elementos":["BT-132"],"expressao":"report (dispara quando verdadeiro): exists(cac:OrderLineReference) and not(cac:OrderLineReference/cbc:LineID)"},
{"id":"BR-CIUS-PT-52","texto":"The Invoice line object identifier (BT-128) shall be filled.","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"Invoice_Line ","elementos":["BT-128"],"expressao":"report (dispara quando verdadeiro): exists(cac:DocumentReference) and not(cac:DocumentReference/cbc:ID)"},
{"id":"BR-41","texto":"Each Invoice line allowance (BG-27) shall have an Invoice line allowance amount (BT-136).","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"Invoice_line_allowances","elementos":["BG-27","BT-136"],"expressao":"exists(cbc:Amount)"},
{"id":"BR-42","texto":"Each Invoice line allowance (BG-27) shall have an Invoice line allowance reason (BT-139) or an Invoice line allowance reason code (BT-140).","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"Invoice_line_allowances","elementos":["BG-27","BT-139","BT-140"],"expressao":"exists(cbc:AllowanceChargeReason) or exists(cbc:AllowanceChargeReasonCode)"},
{"id":"BR-CO-07","texto":"Invoice line allowance reason code (BT-140) and Invoice line allowance reason (BT-139) shall indicate the same type of allowance reason.","categoria":"outra","natureza":"?","gravidade":"erro","contexto":"Invoice_line_allowances","elementos":["BT-139","BT-140"],"expressao":"true()"},
{"id":"BR-CO-23","texto":"Each Invoice line allowance (BG-27) shall contain an Invoice line allowance reason (BT-139) or an Invoice line allowance reason code (BT-140), or both.","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"Invoice_line_allowances","elementos":["BG-27","BT-139","BT-140"],"expressao":"exists(cbc:AllowanceChargeReason) or exists(cbc:AllowanceChargeReasonCode)"},
{"id":"BR-43","texto":"Each Invoice line charge (BG-28) shall have an Invoice line charge amount (BT-141).","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"Invoice_line_charges","elementos":["BG-28","BT-141"],"expressao":"exists(cbc:Amount)"},
{"id":"BR-44","texto":"Each Invoice line charge shall have an Invoice line charge reason or an invoice line allowance reason code.","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"Invoice_line_charges","expressao":"exists(cbc:AllowanceChargeReason) or exists(cbc:AllowanceChargeReasonCode)"},
{"id":"BR-CO-08","texto":"Invoice line charge reason code (BT-145) and Invoice line charge reason (BT144) shall indicate the same type of charge reason.","categoria":"outra","natureza":"?","gravidade":"erro","contexto":"Invoice_line_charges","elementos":["BT-145"],"expressao":"true()"},
{"id":"BR-CO-24","texto":"Each Invoice line charge (BG-28) shall contain an Invoice line charge reason (BT-144) or an Invoice line charge reason code (BT-145), or both.","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"Invoice_line_charges","elementos":["BG-28","BT-144","BT-145"],"expressao":"exists(cbc:AllowanceChargeReason) or exists(cbc:AllowanceChargeReasonCode)"},
{"id":"BR-CIUS-PT-53","texto":"The Item Buyer's identifier (BT-156) shall be filled.","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"Invoice_Line_Item ","elementos":["BT-156"],"expressao":"report (dispara quando verdadeiro): exists(cac:BuyersItemIdentification) and not(cac:BuyersItemIdentification/cbc:ID)"},
{"id":"BR-CIUS-PT-54","texto":"The Item Seller's identifier (BT-155) shall be filled.","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"Invoice_Line_Item ","elementos":["BT-155"],"expressao":"report (dispara quando verdadeiro): exists(cac:SellersItemIdentification) and not(cac:SellersItemIdentification/cbc:ID)"},
{"id":"BR-CIUS-PT-55","texto":"The Item standard identifier (BT-157) shall be filled.","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"Invoice_Line_Item ","elementos":["BT-157"],"expressao":"report (dispara quando verdadeiro): exists(cac:StandardItemIdentification) and not(cac:StandardItemIdentification/cbc:ID)"},
{"id":"BR-CIUS-PT-56","texto":"The Item country of origin (BT-159) shall be filled.","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"Invoice_Line_Item ","elementos":["BT-159"],"expressao":"report (dispara quando verdadeiro): exists(cac:OriginCountry) and not(cac:OriginCountry/cbc:IdentificationCode)"},
{"id":"BR-CIUS-PT-57","texto":"The Item classification identifier (BT-158) shall be filled.","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"Invoice_Line_Item ","elementos":["BT-158"],"expressao":"report (dispara quando verdadeiro): exists(cac:CommodityClassification) and not(cac:CommodityClassification/cbc:ItemClassificationCode)"},
{"id":"BR-CIUS-PT-18","texto":"In an Invoice line (BG-25) where the Invoiced item VAT category code (BT-151) is \"Exempt from VAT\" shall have a VAT exemption reason code (BT-160) or VAT exemption reason text (BT-160).","categoria":"condicional","natureza":"RIR","gravidade":"erro","contexto":"Invoice_Line_Item ","elementos":["BG-25","BT-151","BT-160"],"expressao":"report (dispara quando verdadeiro): ((cac:ClassifiedTaxCategory/cbc:ID) = 'E' or (cac:ClassifiedTaxCategory/cbc:ID) = 'ISE') and not(cac:AdditionalItemProperty)"},
{"id":"BR-30","texto":"If both Invoice line period start date (BT-134) and Invoice line period end date (BT-135) are given then the Invoice line period end date (BT-135) shall be later or equal to the Invoice line period start date (BT-134).","categoria":"condicional","natureza":"RIR","gravidade":"erro","contexto":"Invoice_Line_Period ","elementos":["BT-134","BT-135"],"expressao":"(exists(cbc:EndDate) and exists(cbc:StartDate) and (cbc:EndDate) >= (cbc:StartDate)) or not(exists(cbc:StartDate)) or not(exists(cbc:EndDate))"},
{"id":"BR-CO-20","texto":"If Invoice line period (BG-26) is used, the Invoice line period start date (BT-134) or the Invoice line period end date (BT-135) shall be filled, or both.","categoria":"condicional","natureza":"RIR","gravidade":"erro","contexto":"Invoice_Line_Period ","elementos":["BG-26","BT-134","BT-135"],"expressao":"exists(cbc:StartDate) or exists(cbc:EndDate)"},
{"id":"BR-CIUS-PT-58","texto":"The Item price charge are not allowed at the Price Details (BG-29).","categoria":"outra","natureza":"?","gravidade":"erro","contexto":"Invoice_Line_Price ","elementos":["BG-29"],"expressao":"not(cac:AllowanceCharge[cbc:ChargeIndicator='true'])"},
{"id":"BR-CIUS-PT-59","texto":"The Item price discount (BT-147) shall be filled.","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"Invoice_Line_Price ","elementos":["BT-147"],"expressao":"report (dispara quando verdadeiro): exists(cac:AllowanceCharge[cbc:ChargeIndicator='false']) and not(cac:AllowanceCharge/cbc:Amount)"},
{"id":"BR-29","texto":"If both Invoicing period start date (BT-73) and Invoicing period end date (BT-74) are given then the Invoicing period end date (BT-74) shall be later or equal to the Invoicing period start date (BT-73).","categoria":"condicional","natureza":"RIR","gravidade":"erro","contexto":"Invoice_Period","elementos":["BT-73","BT-74"],"expressao":"(exists(cbc:EndDate) and exists(cbc:StartDate) and (cbc:EndDate) >= (cbc:StartDate)) or not(exists(cbc:StartDate)) or not(exists(cbc:EndDate))"},
{"id":"BR-CO-19","texto":"If Invoicing period (BG-14) is used, the Invoicing period start date (BT-73) or the Invoicing period end date (BT-74) shall be filled, or both.","categoria":"condicional","natureza":"RIR","gravidade":"erro","contexto":"Invoice_Period","elementos":["BG-14","BT-73","BT-74"],"expressao":"exists(cbc:StartDate) or exists(cbc:EndDate)"},
{"id":"BR-54","texto":"Each Item attribute (BG-32) shall contain an Item attribute name (BT-160) and an Item attribute value (BT-161).","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"Item_attributes","elementos":["BG-32","BT-160","BT-161"],"expressao":"exists(cbc:Name) and exists(cbc:Value)"},
{"id":"BR-65","texto":"The Item classification identifier (BT-158) shall have a Scheme identifier.","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"Item_classification_identifier","elementos":["BT-158"],"expressao":"exists(@listID)"},
{"id":"BR-64","texto":"The Item standard identifier (BT-157) shall have a Scheme identifier.","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"Item_standard_identifier","elementos":["BT-157"],"expressao":"exists(@schemeID)"},
{"id":"BR-CIUS-PT-24","texto":"The Purchase order reference (BT-13) or the Sales order reference (BT-14) shall be filled, or both.","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"Order_Reference","elementos":["BT-13","BT-14"],"expressao":"exists(cbc:ID) or exists(cbc:SalesOrderID)"},
{"id":"BR-CIUS-PT-28","texto":"The Tender or lot reference (BT-17) shall be filled.","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"Originator_Document_Reference","elementos":["BT-17"],"expressao":"exists(cbc:ID)"},
{"id":"BR-CIUS-PT-32","texto":"The Payee name (BT-59) shall be filled.","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"Payee","elementos":["BT-59"],"expressao":"report (dispara quando verdadeiro): exists(cac:PartyName) and not(cac:PartyName/cbc:Name)"},
{"id":"BR-CIUS-PT-42","texto":"The Payee identifier (BT-60) or the Bank assigned creditor identifier (BT-90) shall be filled.","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"Payee","elementos":["BT-60","BT-90"],"expressao":"report (dispara quando verdadeiro): exists(cac:PartyIdentification) and not(cac:PartyIdentification/cbc:ID)"},
{"id":"BR-CIUS-PT-43","texto":"The Payee legal registration identifier (BT-61) shall be filled.","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"Payee","elementos":["BT-61"],"expressao":"report (dispara quando verdadeiro): exists(cac:PartyLegalEntity) and not(cac:PartyLegalEntity/cbc:CompanyID)"},
{"id":"BR-50","texto":"A Payment account identifier (BT-84) shall be present if Credit transfer (BG-17) information is provided in the Invoice.","categoria":"condicional","natureza":"RIR","gravidade":"erro","contexto":"Payee_Financial_Account","elementos":["BG-17","BT-84"],"expressao":"exists(cbc:ID)"},
{"id":"BR-49","texto":"A Payment instruction (BG-16) shall specify the Payment means type code (BT-81).","categoria":"outra","natureza":"?","gravidade":"erro","contexto":"Payment_instructions","elementos":["BG-16","BT-81"],"expressao":"exists(cbc:PaymentMeansCode)"},
{"id":"BR-61","texto":"If the Payment means type code (BT-81) means SEPA credit transfer, Local credit transfer or Non-SEPA international credit transfer, the Payment account identifier (BT-84) shall be present.","categoria":"condicional","natureza":"RIR","gravidade":"erro","contexto":"Payment_instructions","elementos":["BT-81","BT-84"],"expressao":"(exists(cac:PayeeFinancialAccount/cbc:ID) and ((normalize-space(cbc:PaymentMeansCode) = '30') or (normalize-space(cbc:PaymentMeansCode) = '58') )) or ((normalize-space(cbc:PaymentMeansCode) != '30') and (normalize-space(cbc:PaymentMeansCode) != '58'))"},
{"id":"BR-CIUS-PT-47","texto":"The Payment account identifier (BT-84) or the Payment account name (BT-85) or the Payment service provider identifier (BT-86) shall be filled.","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"Payment_instructions","elementos":["BT-84","BT-85","BT-86"],"expressao":"report (dispara quando verdadeiro): exists(cac:PayeeFinancialAccount) and (not(cac:PayeeFinancialAccount/cbc:ID) and not(cac:PayeeFinancialAccount/cbc:Name) and not(cac:PayeeFinancialAccount/cac:FinancialInstitutionBranch/cbc:ID))"},
{"id":"BR-CIUS-PT-48","texto":"The Payment service provider identifier (BT-86) shall be filled.","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"Payment_instructions","elementos":["BT-86"],"expressao":"report (dispara quando verdadeiro): exists(cac:PayeeFinancialAccount/cac:FinancialInstitutionBranch) and not(cac:PayeeFinancialAccount/cac:FinancialInstitutionBranch/cbc:ID)"},
{"id":"BR-CIUS-PT-49","texto":"The Mandate reference identifier (BT-89) or the Debited account identifier (BT-91) shall be filled.","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"Payment_instructions","elementos":["BT-89","BT-91"],"expressao":"report (dispara quando verdadeiro): exists(cac:PaymentMandate) and (not(cac:PaymentMandate/cbc:ID) and not(cac:PaymentMandate/cac:PayerFinancialAccount/cbc:ID))"},
{"id":"BR-CIUS-PT-50","texto":"The Debited account identifier (BT-91) shall be filled.","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"Payment_instructions","elementos":["BT-91"],"expressao":"report (dispara quando verdadeiro): exists(cac:PaymentMandate/cac:PayerFinancialAccount) and not(cac:PaymentMandate/cac:PayerFinancialAccount/cbc:ID)"},
{"id":"BR-CIUS-PT-60","texto":"The Payment card primary account number (BT-87) and the card Network identifier shall be filled.","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"Payment_instructions","elementos":["BT-87"],"expressao":"report (dispara quando verdadeiro): exists(cac:CardAccount) and (not(cac:CardAccount/cbc:PrimaryAccountNumberID) or not(cac:CardAccount/cbc:NetworkID))"},
{"id":"BR-CIUS-PT-61","texto":"The Payment terms (BT-20) shall be filled.","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"Payment_terms","elementos":["BT-20"],"expressao":"exists(cbc:Note)"},
{"id":"BR-55","texto":"Each Preceding Invoice reference (BG-3) shall contain a Preceding Invoice reference (BT-25).","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"Preceding_Invoice","elementos":["BG-3","BT-25"],"expressao":"exists(cac:InvoiceDocumentReference/cbc:ID)"},
{"id":"BR-CIUS-PT-33","texto":"The Project reference (BT-11) shall be filled.","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"Project_Reference","elementos":["BT-11"],"expressao":"exists(cbc:ID)"},
{"id":"BR-CIUS-PT-27","texto":"The Receiving advice reference (BT-15) shall be filled.","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"Receipt_Document_Reference","elementos":["BT-15"],"expressao":"exists(cbc:ID)"},
{"id":"BR-CO-26","texto":"In order for the buyer to automatically identify a supplier, the Seller identifier (BT-29), the Seller legal registration identifier (BT-30) and/or the Seller VAT identifier (BT-31) shall be present.","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"Seller","elementos":["BT-29","BT-30","BT-31"],"expressao":"exists(cac:Party/cac:PartyTaxScheme/cbc:CompanyID) or exists(cac:Party/cac:PartyIdentification/cbc:ID) or exists(cac:Party/cac:PartyLegalEntity/cbc:CompanyID)"},
{"id":"BR-CIUS-PT-34","texto":"The Seller identifier (BT-29) or the Bank assigned creditor identifier (BT-90) shall be filled.","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"Seller","elementos":["BT-29","BT-90"],"expressao":"report (dispara quando verdadeiro): exists(cac:Party/cac:PartyIdentification) and not(cac:Party/cac:PartyIdentification/cbc:ID)"},
{"id":"BR-CIUS-PT-35","texto":"The Seller trading name (BT-28) shall be filled.","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"Seller","elementos":["BT-28"],"expressao":"report (dispara quando verdadeiro): exists(cac:Party/cac:PartyName) and not(cac:Party/cac:PartyName/cbc:Name)"},
{"id":"BR-CIUS-PT-36","texto":"The Seller contact point (BT-41) or the Seller contact telephone number (BT-42) or the Seller contact email address (BT-43) shall be filled.","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"Seller","elementos":["BT-41","BT-42","BT-43"],"expressao":"report (dispara quando verdadeiro): exists(cac:Party/cac:Contact) and (not(cac:Party/cac:Contact/cbc:Name) and not(cac:Party/cac:Contact/cbc:Telephone) and not(cac:Party/cac:Contact/cbc:ElectronicMail))"},
{"id":"BR-62","texto":"The Seller electronic address (BT-34) shall have a Scheme identifier.","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"Seller_electronic_address","elementos":["BT-34"],"expressao":"exists(@schemeID)"},
{"id":"BR-CIUS-PT-05","texto":"The Seller postal address (BG-5) shall contain a Seller address line 1 (BT-35).","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"Seller_postal_address","elementos":["BG-5","BT-35"],"expressao":"exists(cbc:StreetName)"},
{"id":"BR-CIUS-PT-06","texto":"The Seller postal address (BG-5) shall contain a Seller city (BT-37).","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"Seller_postal_address","elementos":["BG-5","BT-37"],"expressao":"exists(cbc:CityName)"},
{"id":"BR-CIUS-PT-07","texto":"The Seller postal address (BG-5) shall contain a Seller post code (BT-38).","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"Seller_postal_address","elementos":["BG-5","BT-38"],"expressao":"exists(cbc:PostalZone)"},
{"id":"BR-09","texto":"The Seller postal address (BG-5) shall contain a Seller country code (BT-40).","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"Seller_postal_address","elementos":["BG-5","BT-40"],"expressao":"exists(cac:Country/cbc:IdentificationCode)"},
{"id":"BR-CIUS-PT-37","texto":"The Seller address line 3 (BT-162) shall be filled.","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"Seller_postal_address","elementos":["BT-162"],"expressao":"report (dispara quando verdadeiro): exists(cac:AddressLine) and not(cac:AddressLine/cbc:Line)"},
{"id":"BR-18","texto":"The Seller tax representative name (BT-62) shall be provided in the Invoice, if the Seller (BG-4) has a Seller tax representative party (BG-11)","categoria":"condicional","natureza":"RIR","gravidade":"erro","contexto":"Tax_Representative","elementos":["BG-4","BG-11","BT-62"],"expressao":"exists(cac:PartyName/cbc:Name)"},
{"id":"BR-19","texto":"The Seller tax representative postal address (BG-12) shall be provided in the Invoice, if the Seller (BG-4) has a Seller tax representative party (BG-11).","categoria":"condicional","natureza":"RIR","gravidade":"erro","contexto":"Tax_Representative","elementos":["BG-4","BG-11","BG-12"],"expressao":"exists(cac:PostalAddress)"},
{"id":"BR-56","texto":"Each Seller tax representative party (BG-11) shall have a Seller tax representative VAT identifier (BT-63).","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"Tax_Representative","elementos":["BG-11","BT-63"],"expressao":"exists(cac:PartyTaxScheme[cac:TaxScheme/cbc:ID = 'VAT']/cbc:CompanyID)"},
{"id":"BR-20","texto":"The Seller tax representative postal address (BG-12) shall contain a Tax representative country code (BT-69), if the Seller (BG-4) has a Seller tax representative party (BG-11).","categoria":"condicional","natureza":"RIR","gravidade":"erro","contexto":"Tax_Representative_postal_address","elementos":["BG-4","BG-11","BG-12","BT-69"],"expressao":"exists(cac:Country/cbc:IdentificationCode)"},
{"id":"BR-CIUS-PT-44","texto":"The Tax representative address line 3 (BT-164) shall be filled.","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"Tax_Representative_postal_address","elementos":["BT-164"],"expressao":"report (dispara quando verdadeiro): exists(cac:AddressLine) and not(cac:AddressLine/cbc:Line)"},
{"id":"BR-45","texto":"Each VATBReakdown (BG-23) shall have a VAT category taxable amount (BT-116).","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"VAT_breakdown","elementos":["BG-23","BT-116"],"expressao":"exists(cbc:TaxableAmount)"},
{"id":"BR-46","texto":"Each VATBReakdown (BG-23) shall have a VAT category tax amount (BT-117).","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"VAT_breakdown","elementos":["BG-23","BT-117"],"expressao":"exists(cbc:TaxAmount)"},
{"id":"BR-47","texto":"Each VATBReakdown (BG-23) shall be defined through a VAT category code (BT-118).","categoria":"outra","natureza":"?","gravidade":"erro","contexto":"VAT_breakdown","elementos":["BG-23","BT-118"],"expressao":"exists(cac:TaxCategory/cbc:ID)"},
{"id":"BR-48","texto":"Each VATBReakdown (BG-23) shall have a VAT category rate (BT-119).","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"VAT_breakdown","elementos":["BG-23","BT-119"],"expressao":"exists(cac:TaxCategory/cbc:Percent)"},
{"id":"BR-CIUS-PT-08","texto":"Each VATBReakdown (BG-23) shall have a tax scheme.","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"VAT_breakdown","elementos":["BG-23"],"expressao":"exists(cac:TaxCategory/cac:TaxScheme/cbc:ID)"},
{"id":"BR-AA-10","texto":"A VATBReakdown (BG-23) with VAT Category code (BT-118) \"Lower rate\" shall not have a VAT exemption reason code (BT-121) or VAT exemption reason text (BT-120).","categoria":"outra","natureza":"?","gravidade":"erro","contexto":"VATAA","elementos":["BG-23","BT-118","BT-120","BT-121"],"expressao":"not(cbc:TaxExemptionReason) and not(cbc:TaxExemptionReasonCode)"},
{"id":"BR-CIUS-PT-13","texto":"In an Invoice line (BG-25) where the Invoiced item VAT category code (BT-151) is \"Lower rate\" shall not have a VAT exemption reason code (BT-160) or VAT exemption reason text (BT-160).","categoria":"condicional","natureza":"RIR","gravidade":"erro","contexto":"VATAA_AdditionalLine","elementos":["BG-25","BT-151","BT-160"],"expressao":"not(starts-with(normalize-space(.),'#TAXEXEMPTIONREASONCODE@CLASSIFIEDTAXCATEGORY#')) and not(starts-with(normalize-space(.),'#TAXEXEMPTIONREASON@CLASSIFIEDTAXCATEGORY#'))"},
{"id":"BR-S-10","texto":"A VATBReakdown (BG-23) with VAT Category code (BT-118) \"Standard rate\" shall not have a VAT exemption reason code (BT-121) or VAT exemption reason text (BT-120).","categoria":"outra","natureza":"?","gravidade":"erro","contexto":"VATS","elementos":["BG-23","BT-118","BT-120","BT-121"],"expressao":"not(cbc:TaxExemptionReason) and not(cbc:TaxExemptionReasonCode)"},
{"id":"BR-CIUS-PT-15","texto":"In an Invoice line (BG-25) where the Invoiced item VAT category code (BT-151) is \"Standard rated\" shall not have a VAT exemption reason code (BT-160) or VAT exemption reason text (BT-160).","categoria":"condicional","natureza":"RIR","gravidade":"erro","contexto":"VATS_AdditionalLine","elementos":["BG-25","BT-151","BT-160"],"expressao":"not(starts-with(normalize-space(.),'#TAXEXEMPTIONREASONCODE@CLASSIFIEDTAXCATEGORY#')) and not(starts-with(normalize-space(.),'#TAXEXEMPTIONREASON@CLASSIFIEDTAXCATEGORY#'))"},
{"id":"BR-E-10","texto":"A VATBReakdown (BG-23) with VAT Category code (BT-118) \"Exempt from VAT\" shall have a VAT exemption reason code (BT-121) or a VAT exemption reason text (BT-120).","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"VATE","elementos":["BG-23","BT-118","BT-120","BT-121"],"expressao":"exists(cbc:TaxExemptionReason) or exists(cbc:TaxExemptionReasonCode)"},
{"id":"BR-CIUS-PT-17","texto":"In an Invoice line (BG-25) where the Invoiced item VAT category code (BT-151) is \"Exempt from VAT\" shall have a VAT exemption reason code (BT-160) or VAT exemption reason text (BT-160).","categoria":"condicional","natureza":"RIR","gravidade":"erro","contexto":"VATE_AdditionalLine","elementos":["BG-25","BT-151","BT-160"],"expressao":"$cnt17.1 > 0 or $cnt17.2 > 0"},
{"id":"UBL-SR-33","texto":"Supporting document description shall occur maximum once","categoria":"cardinalidade","natureza":"RE","gravidade":"aviso","contexto":"Additional_supporting_documents","expressao":"(count(cbc:DocumentType) <= 1)"},
{"id":"UBL-DT-06","texto":"Binary object elements shall contain the mime code attribute","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"Binary_object_data_type","expressao":"(@mimeCode)"},
{"id":"UBL-DT-07","texto":"Binary object elements shall contain the file name attribute","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"Binary_object_data_type","expressao":"(@filename)"},
{"id":"UBL-SR-25","texto":"Deliver to party name shall occur maximum once","categoria":"cardinalidade","natureza":"RE","gravidade":"aviso","contexto":"Deliver_to","expressao":"(count(cac:DeliveryParty/cac:PartyName/cbc:Name) <= 1)"},
{"id":"UBL-SR-30","texto":"Document level allowance reason shall occur maximum once","categoria":"cardinalidade","natureza":"RE","gravidade":"aviso","contexto":"Document_level_allowances","expressao":"(count(cbc:AllowanceChargeReason) <= 1)"},
{"id":"UBL-SR-31","texto":"Document level charge reason shall occur maximum once","categoria":"cardinalidade","natureza":"RE","gravidade":"aviso","contexto":"Document_level_charges","expressao":"(count(cbc:AllowanceChargeReason) <= 1)"},
{"id":"UBL-CR-001","texto":"A UBL invoice should not include extensions","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(ext:UBLExtensions)"},
{"id":"UBL-CR-003","texto":"A UBL invoice should not include the ProfileExecutionID","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cbc:ProfileExecutionID)"},
{"id":"UBL-CR-004","texto":"A UBL invoice should not include the CopyIndicator","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cbc:CopyIndicator)"},
{"id":"UBL-CR-005","texto":"A UBL invoice should not include the UUID","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cbc:UUID)"},
{"id":"UBL-CR-006","texto":"A UBL invoice should not include the IssueTime","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cbc:IssueTime)"},
{"id":"UBL-CR-007","texto":"A UBL invoice should not include the PricingCurrencyCode","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cbc:PricingCurrencyCode)"},
{"id":"UBL-CR-008","texto":"A UBL invoice should not include the PaymentCurrencyCode","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cbc:PaymentCurrencyCode)"},
{"id":"UBL-CR-009","texto":"A UBL invoice should not include the PaymentAlternativeCurrencyCode","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cbc:PaymentAlternativeCurrencyCode)"},
{"id":"UBL-CR-010","texto":"A UBL invoice should not include the AccountingCostCode","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cbc:AccountingCostCode)"},
{"id":"UBL-CR-011","texto":"A UBL invoice should not include the LineCountNumeric","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cbc:LineCountNumeric)"},
{"id":"UBL-CR-012","texto":"A UBL invoice should not include the InvoicePeriod StartTime","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoicePeriod/cbc:StartTime)"},
{"id":"UBL-CR-013","texto":"A UBL invoice should not include the InvoicePeriod EndTime","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoicePeriod/cbc:EndTime)"},
{"id":"UBL-CR-014","texto":"A UBL invoice should not include the InvoicePeriod DurationMeasure","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoicePeriod/cbc:DurationMeasure)"},
{"id":"UBL-CR-015","texto":"A UBL invoice should not include the InvoicePeriod Description","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoicePeriod/cbc:Description)"},
{"id":"UBL-CR-016","texto":"A UBL invoice should not include the OrderReference CopyIndicator","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:OrderReference/cbc:CopyIndicator)"},
{"id":"UBL-CR-017","texto":"A UBL invoice should not include the OrderReference UUID","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:OrderReference/cbc:UUID)"},
{"id":"UBL-CR-018","texto":"A UBL invoice should not include the OrderReference IssueDate","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:OrderReference/cbc:IssueDate)"},
{"id":"UBL-CR-019","texto":"A UBL invoice should not include the OrderReference IssueTime","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:OrderReference/cbc:IssueTime)"},
{"id":"UBL-CR-020","texto":"A UBL invoice should not include the OrderReference CustomerReference","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:OrderReference/cbc:CustomerReference)"},
{"id":"UBL-CR-021","texto":"A UBL invoice should not include the OrderReference OrderTypeCode","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:OrderReference/cbc:OrderTypeCode)"},
{"id":"UBL-CR-022","texto":"A UBL invoice should not include the OrderReference DocumentReference","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:OrderReference/cbc:DocumentReference)"},
{"id":"UBL-CR-023","texto":"A UBL invoice should not include the BillingReference CopyIndicator","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:BillingReference/cac:InvoiceDocumentReference/cbc:CopyIndicator)"},
{"id":"UBL-CR-024","texto":"A UBL invoice should not include the BillingReference UUID","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:BillingReference/cac:InvoiceDocumentReference/cbc:UUID)"},
{"id":"UBL-CR-025","texto":"A UBL invoice should not include the BillingReference IssueTime","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:BillingReference/cac:InvoiceDocumentReference/cbc:IssueTime)"},
{"id":"UBL-CR-026","texto":"A UBL invoice should not include the BillingReference DocumentTypeCode","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:BillingReference/cac:InvoiceDocumentReference/cbc:DocumentTypeCode)"},
{"id":"UBL-CR-027","texto":"A UBL invoice should not include the BillingReference DocumentType","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:BillingReference/cac:InvoiceDocumentReference/cbc:DocumentType)"},
{"id":"UBL-CR-028","texto":"A UBL invoice should not include the BillingReference Xpath","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:BillingReference/cac:InvoiceDocumentReference/cbc:Xpath)"},
{"id":"UBL-CR-029","texto":"A UBL invoice should not include the BillingReference LanguageID","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:BillingReference/cac:InvoiceDocumentReference/cbc:LanguageID)"},
{"id":"UBL-CR-030","texto":"A UBL invoice should not include the BillingReference LocaleCode","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:BillingReference/cac:InvoiceDocumentReference/cbc:LocaleCode)"},
{"id":"UBL-CR-031","texto":"A UBL invoice should not include the BillingReference VersionID","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:BillingReference/cac:InvoiceDocumentReference/cbc:VersionID)"},
{"id":"UBL-CR-032","texto":"A UBL invoice should not include the BillingReference DocumentStatusCode","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:BillingReference/cac:InvoiceDocumentReference/cbc:DocumentStatusCode)"},
{"id":"UBL-CR-033","texto":"A UBL invoice should not include the BillingReference DocumenDescription","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:BillingReference/cac:InvoiceDocumentReference/cbc:DocumentDescription)"},
{"id":"UBL-CR-034","texto":"A UBL invoice should not include the BillingReference Attachment","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:BillingReference/cac:InvoiceDocumentReference/cac:Attachment)"},
{"id":"UBL-CR-035","texto":"A UBL invoice should not include the BillingReference ValidityPeriod","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:BillingReference/cac:InvoiceDocumentReference/cac:ValidityPeriod)"},
{"id":"UBL-CR-036","texto":"A UBL invoice should not include the BillingReference IssuerParty","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:BillingReference/cac:InvoiceDocumentReference/cac:IssuerParty)"},
{"id":"UBL-CR-037","texto":"A UBL invoice should not include the BillingReference ResultOfVerification","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:BillingReference/cac:InvoiceDocumentReference/cac:ResultOfVerification)"},
{"id":"UBL-CR-038","texto":"A UBL invoice should not include the BillingReference SelfBilledInvoiceDocumentReference","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:BillingReference/cac:SelfBilledInvoiceDocumentReference)"},
{"id":"UBL-CR-039","texto":"A UBL invoice should not include the BillingReference CreditNoteDocumentReference","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:BillingReference/cac:CreditNoteDocumentReference)"},
{"id":"UBL-CR-040","texto":"A UBL invoice should not include the BillingReference SelfBilledCreditNoteDocumentReference","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:BillingReference/cac:SelfBilledCreditNoteDocumentReference)"},
{"id":"UBL-CR-041","texto":"A UBL invoice should not include the BillingReference DebitNoteDocumentReference","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:BillingReference/cac:DebitNoteDocumentReference)"},
{"id":"UBL-CR-042","texto":"A UBL invoice should not include the BillingReference ReminderDocumentReference","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:BillingReference/cac:ReminderDocumentReference)"},
{"id":"UBL-CR-043","texto":"A UBL invoice should not include the BillingReference AdditionalDocumentReference","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:BillingReference/cac:AdditionalDocumentReference)"},
{"id":"UBL-CR-044","texto":"A UBL invoice should not include the BillingReference BillingReferenceLine","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:BillingReference/cac:BillingReferenceLine)"},
{"id":"UBL-CR-045","texto":"A UBL invoice should not include the DespatchDocumentReference CopyIndicator","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:DespatchDocumentReference/cbc:CopyIndicator)"},
{"id":"UBL-CR-046","texto":"A UBL invoice should not include the DespatchDocumentReference UUID","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:DespatchDocumentReference/cbc:UUID)"},
{"id":"UBL-CR-047","texto":"A UBL invoice should not include the DespatchDocumentReference IssueDate","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:DespatchDocumentReference/cbc:IssueDate)"},
{"id":"UBL-CR-048","texto":"A UBL invoice should not include the DespatchDocumentReference IssueTime","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:DespatchDocumentReference/cbc:IssueTime)"},
{"id":"UBL-CR-049","texto":"A UBL invoice should not include the DespatchDocumentReference DocumentTypeCode","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:DespatchDocumentReference/cbc:DocumentTypeCode)"},
{"id":"UBL-CR-050","texto":"A UBL invoice should not include the DespatchDocumentReference DocumentType","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:DespatchDocumentReference/cbc:DocumentType)"},
{"id":"UBL-CR-051","texto":"A UBL invoice should not include the DespatchDocumentReference Xpath","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:DespatchDocumentReference/cbc:Xpath)"},
{"id":"UBL-CR-052","texto":"A UBL invoice should not include the DespatchDocumentReference LanguageID","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:DespatchDocumentReference/cbc:LanguageID)"},
{"id":"UBL-CR-053","texto":"A UBL invoice should not include the DespatchDocumentReference LocaleCode","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:DespatchDocumentReference/cbc:LocaleCode)"},
{"id":"UBL-CR-054","texto":"A UBL invoice should not include the DespatchDocumentReference VersionID","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:DespatchDocumentReference/cbc:VersionID)"},
{"id":"UBL-CR-055","texto":"A UBL invoice should not include the DespatchDocumentReference DocumentStatusCode","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:DespatchDocumentReference/cbc:DocumentStatusCode)"},
{"id":"UBL-CR-056","texto":"A UBL invoice should not include the DespatchDocumentReference DocumentDescription","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:DespatchDocumentReference/cbc:DocumentDescription)"},
{"id":"UBL-CR-057","texto":"A UBL invoice should not include the DespatchDocumentReference Attachment","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:DespatchDocumentReference/cac:Attachment)"},
{"id":"UBL-CR-058","texto":"A UBL invoice should not include the DespatchDocumentReference ValidityPeriod","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:DespatchDocumentReference/cac:ValidityPeriod)"},
{"id":"UBL-CR-059","texto":"A UBL invoice should not include the DespatchDocumentReference IssuerParty","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:DespatchDocumentReference/cac:IssuerParty)"},
{"id":"UBL-CR-060","texto":"A UBL invoice should not include the DespatchDocumentReference ResultOfVerification","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:DespatchDocumentReference/cac:ResultOfVerification)"},
{"id":"UBL-CR-061","texto":"A UBL invoice should not include the ReceiptDocumentReference CopyIndicator","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:ReceiptDocumentReference/cbc:CopyIndicator)"},
{"id":"UBL-CR-062","texto":"A UBL invoice should not include the ReceiptDocumentReference UUID","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:ReceiptDocumentReference/cbc:UUID)"},
{"id":"UBL-CR-063","texto":"A UBL invoice should not include the ReceiptDocumentReference IssueDate","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:ReceiptDocumentReference/cbc:IssueDate)"},
{"id":"UBL-CR-064","texto":"A UBL invoice should not include the ReceiptDocumentReference IssueTime","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:ReceiptDocumentReference/cbc:IssueTime)"},
{"id":"UBL-CR-065","texto":"A UBL invoice should not include the ReceiptDocumentReference DocumentTypeCode","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:ReceiptDocumentReference/cbc:DocumentTypeCode)"},
{"id":"UBL-CR-066","texto":"A UBL invoice should not include the ReceiptDocumentReference DocumentType","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:ReceiptDocumentReference/cbc:DocumentType)"},
{"id":"UBL-CR-067","texto":"A UBL invoice should not include the ReceiptDocumentReference Xpath","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:ReceiptDocumentReference/cbc:Xpath)"},
{"id":"UBL-CR-068","texto":"A UBL invoice should not include the ReceiptDocumentReference LanguageID","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:ReceiptDocumentReference/cbc:LanguageID)"},
{"id":"UBL-CR-069","texto":"A UBL invoice should not include the ReceiptDocumentReference LocaleCode","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:ReceiptDocumentReference/cbc:LocaleCode)"},
{"id":"UBL-CR-070","texto":"A UBL invoice should not include the ReceiptDocumentReference VersionID","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:ReceiptDocumentReference/cbc:VersionID)"},
{"id":"UBL-CR-071","texto":"A UBL invoice should not include the ReceiptDocumentReference DocumentStatusCode","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:ReceiptDocumentReference/cbc:DocumentStatusCode)"},
{"id":"UBL-CR-072","texto":"A UBL invoice should not include the ReceiptDocumentReference DocumentDescription","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:ReceiptDocumentReference/cbc:DocumentDescription)"},
{"id":"UBL-CR-073","texto":"A UBL invoice should not include the ReceiptDocumentReference Attachment","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:ReceiptDocumentReference/cac:Attachment)"},
{"id":"UBL-CR-074","texto":"A UBL invoice should not include the ReceiptDocumentReference ValidityPeriod","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:ReceiptDocumentReference/cac:ValidityPeriod)"},
{"id":"UBL-CR-075","texto":"A UBL invoice should not include the ReceiptDocumentReference IssuerParty","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:ReceiptDocumentReference/cac:IssuerParty)"},
{"id":"UBL-CR-076","texto":"A UBL invoice should not include the ReceiptDocumentReference ResultOfVerification","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:ReceiptDocumentReference/cac:ResultOfVerification)"},
{"id":"UBL-CR-077","texto":"A UBL invoice should not include the StatementDocumentReference","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:StatementDocumentReference)"},
{"id":"UBL-CR-078","texto":"A UBL invoice should not include the OriginatorDocumentReference CopyIndicator","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:OriginatorDocumentReference/cbc:CopyIndicator)"},
{"id":"UBL-CR-079","texto":"A UBL invoice should not include the OriginatorDocumentReference UUID","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:OriginatorDocumentReference/cbc:UUID)"},
{"id":"UBL-CR-080","texto":"A UBL invoice should not include the OriginatorDocumentReference IssueDate","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:OriginatorDocumentReference/cbc:IssueDate)"},
{"id":"UBL-CR-081","texto":"A UBL invoice should not include the OriginatorDocumentReference IssueTime","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:OriginatorDocumentReference/cbc:IssueTime)"},
{"id":"UBL-CR-082","texto":"A UBL invoice should not include the OriginatorDocumentReference DocumentTypeCode","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:OriginatorDocumentReference/cbc:DocumentTypeCode)"},
{"id":"UBL-CR-083","texto":"A UBL invoice should not include the OriginatorDocumentReference DocumentType","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:OriginatorDocumentReference/cbc:DocumentType)"},
{"id":"UBL-CR-084","texto":"A UBL invoice should not include the OriginatorDocumentReference Xpath","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:OriginatorDocumentReference/cbc:Xpath)"},
{"id":"UBL-CR-085","texto":"A UBL invoice should not include the OriginatorDocumentReference LanguageID","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:OriginatorDocumentReference/cbc:LanguageID)"},
{"id":"UBL-CR-086","texto":"A UBL invoice should not include the OriginatorDocumentReference LocaleCode","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:OriginatorDocumentReference/cbc:LocaleCode)"},
{"id":"UBL-CR-087","texto":"A UBL invoice should not include the OriginatorDocumentReference VersionID","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:OriginatorDocumentReference/cbc:VersionID)"},
{"id":"UBL-CR-088","texto":"A UBL invoice should not include the OriginatorDocumentReference DocumentStatusCode","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:OriginatorDocumentReference/cbc:DocumentStatusCode)"},
{"id":"UBL-CR-089","texto":"A UBL invoice should not include the OriginatorDocumentReference DocumentDescription","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:OriginatorDocumentReference/cbc:DocumentDescription)"},
{"id":"UBL-CR-090","texto":"A UBL invoice should not include the OriginatorDocumentReference Attachment","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:OriginatorDocumentReference/cac:Attachment)"},
{"id":"UBL-CR-091","texto":"A UBL invoice should not include the OriginatorDocumentReference ValidityPeriod","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:OriginatorDocumentReference/cac:ValidityPeriod)"},
{"id":"UBL-CR-092","texto":"A UBL invoice should not include the OriginatorDocumentReference IssuerParty","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:OriginatorDocumentReference/cac:IssuerParty)"},
{"id":"UBL-CR-093","texto":"A UBL invoice should not include the OriginatorDocumentReference ResultOfVerification","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:OriginatorDocumentReference/cac:ResultOfVerification)"},
{"id":"UBL-CR-094","texto":"A UBL invoice should not include the ContractDocumentReference CopyIndicator","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:ContractDocumentReference/cbc:CopyIndicator)"},
{"id":"UBL-CR-095","texto":"A UBL invoice should not include the ContractDocumentReference UUID","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:ContractDocumentReference/cbc:UUID)"},
{"id":"UBL-CR-096","texto":"A UBL invoice should not include the ContractDocumentReference IssueDate","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:ContractDocumentReference/cbc:IssueDate)"},
{"id":"UBL-CR-097","texto":"A UBL invoice should not include the ContractDocumentReference IssueTime","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:ContractDocumentReference/cbc:IssueTime)"},
{"id":"UBL-CR-098","texto":"A UBL invoice should not include the ContractDocumentReference DocumentTypeCode","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:ContractDocumentReference/cbc:DocumentTypeCode)"},
{"id":"UBL-CR-099","texto":"A UBL invoice should not include the ContractDocumentReference DocumentType","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:ContractDocumentReference/cbc:DocumentType)"},
{"id":"UBL-CR-100","texto":"A UBL invoice should not include the ContractDocumentReference Xpath","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:ContractDocumentReference/cbc:Xpath)"},
{"id":"UBL-CR-101","texto":"A UBL invoice should not include the ContractDocumentReference LanguageID","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:ContractDocumentReference/cbc:LanguageID)"},
{"id":"UBL-CR-102","texto":"A UBL invoice should not include the ContractDocumentReference LocaleCode","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:ContractDocumentReference/cbc:LocaleCode)"},
{"id":"UBL-CR-103","texto":"A UBL invoice should not include the ContractDocumentReference VersionID","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:ContractDocumentReference/cbc:VersionID)"},
{"id":"UBL-CR-104","texto":"A UBL invoice should not include the ContractDocumentReference DocumentStatusCode","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:ContractDocumentReference/cbc:DocumentStatusCode)"},
{"id":"UBL-CR-105","texto":"A UBL invoice should not include the ContractDocumentReference DocumentDescription","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:ContractDocumentReference/cbc:DocumentDescription)"},
{"id":"UBL-CR-106","texto":"A UBL invoice should not include the ContractDocumentReference Attachment","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:ContractDocumentReference/cac:Attachment)"},
{"id":"UBL-CR-107","texto":"A UBL invoice should not include the ContractDocumentReference ValidityPeriod","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:ContractDocumentReference/cac:ValidityPeriod)"},
{"id":"UBL-CR-108","texto":"A UBL invoice should not include the ContractDocumentReference IssuerParty","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:ContractDocumentReference/cac:IssuerParty)"},
{"id":"UBL-CR-109","texto":"A UBL invoice should not include the ContractDocumentReference ResultOfVerification","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:ContractDocumentReference/cac:ResultOfVerification)"},
{"id":"UBL-CR-110","texto":"A UBL invoice should not include the AdditionalDocumentReference CopyIndicator","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AdditionalDocumentReference/cbc:CopyIndicator)"},
{"id":"UBL-CR-111","texto":"A UBL invoice should not include the AdditionalDocumentReference UUID","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AdditionalDocumentReference/cbc:UUID)"},
{"id":"UBL-CR-112","texto":"A UBL invoice should not include the AdditionalDocumentReference IssueDate","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AdditionalDocumentReference/cbc:IssueDate)"},
{"id":"UBL-CR-113","texto":"A UBL invoice should not include the AdditionalDocumentReference IssueTime","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AdditionalDocumentReference/cbc:IssueTime)"},
{"id":"UBL-CR-114","texto":"A UBL invoice should not include the AdditionalDocumentReference DocumentType","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AdditionalDocumentReference/cbc:DocumentType)"},
{"id":"UBL-CR-115","texto":"A UBL invoice should not include the AdditionalDocumentReference Xpath","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AdditionalDocumentReference/cbc:Xpath)"},
{"id":"UBL-CR-116","texto":"A UBL invoice should not include the AdditionalDocumentReference LanguageID","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AdditionalDocumentReference/cbc:LanguageID)"},
{"id":"UBL-CR-117","texto":"A UBL invoice should not include the AdditionalDocumentReference LocaleCode","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AdditionalDocumentReference/cbc:LocaleCode)"},
{"id":"UBL-CR-118","texto":"A UBL invoice should not include the AdditionalDocumentReference VersionID","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AdditionalDocumentReference/cbc:VersionID)"},
{"id":"UBL-CR-119","texto":"A UBL invoice should not include the AdditionalDocumentReference DocumentStatusCode","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AdditionalDocumentReference/cbc:DocumentStatusCode)"},
{"id":"UBL-CR-121","texto":"A UBL invoice should not include the AdditionalDocumentReference Attachment External DocumentHash","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AdditionalDocumentReference/cac:Attachment/cac:ExternalReference/cbc:DocumentHash)"},
{"id":"UBL-CR-122","texto":"A UBL invoice should not include the AdditionalDocumentReference Attachment External HashAlgorithmMethod","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AdditionalDocumentReference/cac:Attachment/cac:ExternalReference/cbc:HashAlgorithmMethod)"},
{"id":"UBL-CR-123","texto":"A UBL invoice should not include the AdditionalDocumentReference Attachment External ExpiryDate","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AdditionalDocumentReference/cac:Attachment/cac:ExternalReference/cbc:ExpiryDate)"},
{"id":"UBL-CR-124","texto":"A UBL invoice should not include the AdditionalDocumentReference Attachment External ExpiryTime","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AdditionalDocumentReference/cac:Attachment/cac:ExternalReference/cbc:ExpiryTime)"},
{"id":"UBL-CR-125","texto":"A UBL invoice should not include the AdditionalDocumentReference Attachment External MimeCode","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AdditionalDocumentReference/cac:Attachment/cac:ExternalReference/cbc:MimeCode)"},
{"id":"UBL-CR-126","texto":"A UBL invoice should not include the AdditionalDocumentReference Attachment External FormatCode","categoria":"formato","natureza":"RP","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AdditionalDocumentReference/cac:Attachment/cac:ExternalReference/cbc:FormatCode)"},
{"id":"UBL-CR-127","texto":"A UBL invoice should not include the AdditionalDocumentReference Attachment External EncodingCode","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AdditionalDocumentReference/cac:Attachment/cac:ExternalReference/cbc:EncodingCode)"},
{"id":"UBL-CR-128","texto":"A UBL invoice should not include the AdditionalDocumentReference Attachment External CharacterSetCode","categoria":"formato","natureza":"RP","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AdditionalDocumentReference/cac:Attachment/cac:ExternalReference/cbc:CharacterSetCode)"},
{"id":"UBL-CR-129","texto":"A UBL invoice should not include the AdditionalDocumentReference Attachment External FileName","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AdditionalDocumentReference/cac:Attachment/cac:ExternalReference/cbc:FileName)"},
{"id":"UBL-CR-130","texto":"A UBL invoice should not include the AdditionalDocumentReference Attachment External Descriprion","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AdditionalDocumentReference/cac:Attachment/cac:ExternalReference/cbc:Description)"},
{"id":"UBL-CR-131","texto":"A UBL invoice should not include the AdditionalDocumentReference ValidityPeriod","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AdditionalDocumentReference/cac:ValidityPeriod)"},
{"id":"UBL-CR-132","texto":"A UBL invoice should not include the AdditionalDocumentReference IssuerParty","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AdditionalDocumentReference/cac:IssuerParty)"},
{"id":"UBL-CR-133","texto":"A UBL invoice should not include the AdditionalDocumentReference ResultOfVerification","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AdditionalDocumentReference/cac:ResultOfVerification)"},
{"id":"UBL-CR-134","texto":"A UBL invoice should not include the ProjectReference UUID","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:ProjectReference/cbc:UUID)"},
{"id":"UBL-CR-135","texto":"A UBL invoice should not include the ProjectReference IssueDate","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:ProjectReference/cbc:IssueDate)"},
{"id":"UBL-CR-136","texto":"A UBL invoice should not include the ProjectReference WorkPhaseReference","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:ProjectReference/cac:WorkPhaseReference)"},
{"id":"UBL-CR-137","texto":"A UBL invoice should not include the Signature","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:Signature)"},
{"id":"UBL-CR-138","texto":"A UBL invoice should not include the AccountingSupplierParty CustomerAssignedAccountID","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingSupplierParty/cbc:CustomerAssignedAccountID)"},
{"id":"UBL-CR-139","texto":"A UBL invoice should not include the AccountingSupplierParty AdditionalAccountID","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingSupplierParty/cbc:AdditionalAccountID)"},
{"id":"UBL-CR-140","texto":"A UBL invoice should not include the AccountingSupplierParty DataSendingCapability","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingSupplierParty/cbc:DataSendingCapability)"},
{"id":"UBL-CR-141","texto":"A UBL invoice should not include the AccountingSupplierParty Party MarkCareIndicator","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingSupplierParty/cac:Party/cbc:MarkCareIndicator)"},
{"id":"UBL-CR-142","texto":"A UBL invoice should not include the AccountingSupplierParty Party MarkAttentionIndicator","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingSupplierParty/cac:Party/cbc:MarkAttentionIndicator)"},
{"id":"UBL-CR-143","texto":"A UBL invoice should not include the AccountingSupplierParty Party WebsiteURI","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingSupplierParty/cac:Party/cbc:WebsiteURI)"},
{"id":"UBL-CR-144","texto":"A UBL invoice should not include the AccountingSupplierParty Party LogoReferenceID","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingSupplierParty/cac:Party/cbc:LogoReferenceID)"},
{"id":"UBL-CR-145","texto":"A UBL invoice should not include the AccountingSupplierParty Party IndustryClassificationCode","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingSupplierParty/cac:Party/cbc:IndustryClassificationCode)"},
{"id":"UBL-CR-146","texto":"A UBL invoice should not include the AccountingSupplierParty Party Language","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingSupplierParty/cac:Party/cac:Language)"},
{"id":"UBL-CR-147","texto":"A UBL invoice should not include the AccountingSupplierParty Party PostalAddress ID","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingSupplierParty/cac:Party/cac:PostalAddress/cbc:ID)"},
{"id":"UBL-CR-148","texto":"A UBL invoice should not include the AccountingSupplierParty Party PostalAddress AddressTypeCode","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingSupplierParty/cac:Party/cac:PostalAddress/cbc:AddressTypeCode)"},
{"id":"UBL-CR-149","texto":"A UBL invoice should not include the AccountingSupplierParty Party PostalAddress AddressFormatCode","categoria":"formato","natureza":"RP","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingSupplierParty/cac:Party/cac:PostalAddress/cbc:AddressFormatCode)"},
{"id":"UBL-CR-150","texto":"A UBL invoice should not include the AccountingSupplierParty Party PostalAddress Postbox","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingSupplierParty/cac:Party/cac:PostalAddress/cbc:Postbox)"},
{"id":"UBL-CR-151","texto":"A UBL invoice should not include the AccountingSupplierParty Party PostalAddress Floor","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingSupplierParty/cac:Party/cac:PostalAddress/cbc:Floor)"},
{"id":"UBL-CR-152","texto":"A UBL invoice should not include the AccountingSupplierParty Party PostalAddress Room","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingSupplierParty/cac:Party/cac:PostalAddress/cbc:Room)"},
{"id":"UBL-CR-153","texto":"A UBL invoice should not include the AccountingSupplierParty Party PostalAddress BlockName","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingSupplierParty/cac:Party/cac:PostalAddress/cbc:BlockName)"},
{"id":"UBL-CR-154","texto":"A UBL invoice should not include the AccountingSupplierParty Party PostalAddress BuildingName","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingSupplierParty/cac:Party/cac:PostalAddress/cbc:BuildingName)"},
{"id":"UBL-CR-155","texto":"A UBL invoice should not include the AccountingSupplierParty Party PostalAddress BuildingNumber","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingSupplierParty/cac:Party/cac:PostalAddress/cbc:BuildingNumber)"},
{"id":"UBL-CR-156","texto":"A UBL invoice should not include the AccountingSupplierParty Party PostalAddress InhouseMail","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingSupplierParty/cac:Party/cac:PostalAddress/cbc:InhouseMail)"},
{"id":"UBL-CR-157","texto":"A UBL invoice should not include the AccountingSupplierParty Party PostalAddress Department","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingSupplierParty/cac:Party/cac:PostalAddress/cbc:Department)"},
{"id":"UBL-CR-158","texto":"A UBL invoice should not include the AccountingSupplierParty Party PostalAddress MarkAttention","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingSupplierParty/cac:Party/cac:PostalAddress/cbc:MarkAttention)"},
{"id":"UBL-CR-159","texto":"A UBL invoice should not include the AccountingSupplierParty Party PostalAddress MarkCare","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingSupplierParty/cac:Party/cac:PostalAddress/cbc:MarkCare)"},
{"id":"UBL-CR-160","texto":"A UBL invoice should not include the AccountingSupplierParty Party PostalAddress PlotIdentification","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingSupplierParty/cac:Party/cac:PostalAddress/cbc:PlotIdentification)"},
{"id":"UBL-CR-161","texto":"A UBL invoice should not include the AccountingSupplierParty Party PostalAddress CitySubdivisionName","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingSupplierParty/cac:Party/cac:PostalAddress/cbc:CitySubdivisionName)"},
{"id":"UBL-CR-162","texto":"A UBL invoice should not include the AccountingSupplierParty Party PostalAddress CountrySubentityCode","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingSupplierParty/cac:Party/cac:PostalAddress/cbc:CountrySubentityCode)"},
{"id":"UBL-CR-163","texto":"A UBL invoice should not include the AccountingSupplierParty Party PostalAddress Region","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingSupplierParty/cac:Party/cac:PostalAddress/cbc:Region)"},
{"id":"UBL-CR-164","texto":"A UBL invoice should not include the AccountingSupplierParty Party PostalAddress District","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingSupplierParty/cac:Party/cac:PostalAddress/cbc:District)"},
{"id":"UBL-CR-165","texto":"A UBL invoice should not include the AccountingSupplierParty Party PostalAddress TimezoneOffset","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingSupplierParty/cac:Party/cac:PostalAddress/cbc:TimezoneOffset)"},
{"id":"UBL-CR-166","texto":"A UBL invoice should not include the AccountingSupplierParty Party PostalAddress Country Name","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingSupplierParty/cac:Party/cac:PostalAddress/cac:Country/cbc:Name)"},
{"id":"UBL-CR-167","texto":"A UBL invoice should not include the AccountingSupplierParty Party PostalAddress LocationCoordinate","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingSupplierParty/cac:Party/cac:PostalAddress/cac:LocationCoordinate)"},
{"id":"UBL-CR-168","texto":"A UBL invoice should not include the AccountingSupplierParty Party PhysicalLocation","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingSupplierParty/cac:Party/cac:PhysicalLocation)"},
{"id":"UBL-CR-169","texto":"A UBL invoice should not include the AccountingSupplierParty Party PartyTaxScheme RegistrationName","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingSupplierParty/cac:Party/cac:PartyTaxScheme/cbc:RegistrationName)"},
{"id":"UBL-CR-170","texto":"A UBL invoice should not include the AccountingSupplierParty Party PartyTaxScheme TaxLevelCode","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingSupplierParty/cac:Party/cac:PartyTaxScheme/cbc:TaxLevelCode)"},
{"id":"UBL-CR-171","texto":"A UBL invoice should not include the AccountingSupplierParty Party PartyTaxScheme ExemptionReasonCode","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingSupplierParty/cac:Party/cac:PartyTaxScheme/cbc:ExemptionReasonCode)"},
{"id":"UBL-CR-172","texto":"A UBL invoice should not include the AccountingSupplierParty Party PartyTaxScheme ExemptionReason","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingSupplierParty/cac:Party/cac:PartyTaxScheme/cbc:ExemptionReason)"},
{"id":"UBL-CR-173","texto":"A UBL invoice should not include the AccountingSupplierParty Party PartyTaxScheme RegistrationAddress","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingSupplierParty/cac:Party/cac:PartyTaxScheme/cac:RegistrationAddress)"},
{"id":"UBL-CR-174","texto":"A UBL invoice should not include the AccountingSupplierParty Party PartyTaxScheme TaxScheme Name","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingSupplierParty/cac:Party/cac:PartyTaxScheme/cac:TaxScheme/cbc:Name)"},
{"id":"UBL-CR-175","texto":"A UBL invoice should not include the AccountingSupplierParty Party PartyTaxScheme TaxScheme TaxTypeCode","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingSupplierParty/cac:Party/cac:PartyTaxScheme/cac:TaxScheme/cbc:TaxTypeCode)"},
{"id":"UBL-CR-176","texto":"A UBL invoice should not include the AccountingSupplierParty Party PartyTaxScheme TaxScheme CurrencyCode","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingSupplierParty/cac:Party/cac:PartyTaxScheme/cac:TaxScheme/cbc:CurrencyCode)"},
{"id":"UBL-CR-177","texto":"A UBL invoice should not include the AccountingSupplierParty Party PartyTaxScheme TaxScheme JurisdictionRegionAddress","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingSupplierParty/cac:Party/cac:PartyTaxScheme/cac:TaxScheme/cac:JurisdictionRegionAddress)"},
{"id":"UBL-CR-178","texto":"A UBL invoice should not include the AccountingSupplierParty Party PartyLegalEntity RegistrationDate","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingSupplierParty/cac:Party/cac:PartyLegalEntity/cbc:RegistrationDate)"},
{"id":"UBL-CR-179","texto":"A UBL invoice should not include the AccountingSupplierParty Party PartyLegalEntity RegistrationExpirationDate","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingSupplierParty/cac:Party/cac:PartyLegalEntity/cbc:RegistrationExpirationDate)"},
{"id":"UBL-CR-180","texto":"A UBL invoice should not include the AccountingSupplierParty Party PartyLegalEntity CompanyLegalFormCode","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingSupplierParty/cac:Party/cac:PartyLegalEntity/cbc:CompanyLegalFormCode)"},
{"id":"UBL-CR-181","texto":"A UBL invoice should not include the AccountingSupplierParty Party PartyLegalEntity SoleProprietorshipIndicator","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingSupplierParty/cac:Party/cac:PartyLegalEntity/cbc:SoleProprietorshipIndicator)"},
{"id":"UBL-CR-182","texto":"A UBL invoice should not include the AccountingSupplierParty Party PartyLegalEntity CompanyLiquidationStatusCode","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingSupplierParty/cac:Party/cac:PartyLegalEntity/cbc:CompanyLiquidationStatusCode)"},
{"id":"UBL-CR-183","texto":"A UBL invoice should not include the AccountingSupplierParty Party PartyLegalEntity CorporationStockAmount","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingSupplierParty/cac:Party/cac:PartyLegalEntity/cbc:CorporationStockAmount)"},
{"id":"UBL-CR-184","texto":"A UBL invoice should not include the AccountingSupplierParty Party PartyLegalEntity FullyPaidSharesIndicator","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingSupplierParty/cac:Party/cac:PartyLegalEntity/cbc:FullyPaidSharesIndicator)"},
{"id":"UBL-CR-185","texto":"A UBL invoice should not include the AccountingSupplierParty Party PartyLegalEntity RegistrationAddress","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingSupplierParty/cac:Party/cac:PartyLegalEntity/cac:RegistrationAddress)"},
{"id":"UBL-CR-186","texto":"A UBL invoice should not include the AccountingSupplierParty Party PartyLegalEntity CorporateRegistrationScheme","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingSupplierParty/cac:Party/cac:PartyLegalEntity/cac:CorporateRegistrationScheme)"},
{"id":"UBL-CR-187","texto":"A UBL invoice should not include the AccountingSupplierParty Party PartyLegalEntity HeadOfficeParty","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingSupplierParty/cac:Party/cac:PartyLegalEntity/cac:HeadOfficeParty)"},
{"id":"UBL-CR-188","texto":"A UBL invoice should not include the AccountingSupplierParty Party PartyLegalEntity ShareholderParty","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingSupplierParty/cac:Party/cac:PartyLegalEntity/cac:ShareholderParty)"},
{"id":"UBL-CR-189","texto":"A UBL invoice should not include the AccountingSupplierParty Party Contact ID","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingSupplierParty/cac:Party/cac:Contact/cbc:ID)"},
{"id":"UBL-CR-190","texto":"A UBL invoice should not include the AccountingSupplierParty Party Contact Telefax","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingSupplierParty/cac:Party/cac:Contact/cbc:Telefax)"},
{"id":"UBL-CR-191","texto":"A UBL invoice should not include the AccountingSupplierParty Party Contact Note","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingSupplierParty/cac:Party/cac:Contact/cbc:Note)"},
{"id":"UBL-CR-192","texto":"A UBL invoice should not include the AccountingSupplierParty Party Contact OtherCommunication","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingSupplierParty/cac:Party/cac:Contact/cac:OtherCommunication)"},
{"id":"UBL-CR-193","texto":"A UBL invoice should not include the AccountingSupplierParty Party Person","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingSupplierParty/cac:Party/cac:Person)"},
{"id":"UBL-CR-194","texto":"A UBL invoice should not include the AccountingSupplierParty Party AgentParty","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingSupplierParty/cac:Party/cac:AgentParty)"},
{"id":"UBL-CR-195","texto":"A UBL invoice should not include the AccountingSupplierParty Party ServiceProviderParty","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingSupplierParty/cac:Party/cac:ServiceProviderParty)"},
{"id":"UBL-CR-196","texto":"A UBL invoice should not include the AccountingSupplierParty Party PowerOfAttorney","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingSupplierParty/cac:Party/cac:PowerOfAttorney)"},
{"id":"UBL-CR-197","texto":"A UBL invoice should not include the AccountingSupplierParty Party FinancialAccount","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingSupplierParty/cac:Party/cac:FinancialAccount)"},
{"id":"UBL-CR-198","texto":"A UBL invoice should not include the AccountingSupplierParty DespatchContact","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingSupplierParty/cac:DespatchContact)"},
{"id":"UBL-CR-199","texto":"A UBL invoice should not include the AccountingSupplierParty AccountingContact","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingSupplierParty/cac:AccountingContact)"},
{"id":"UBL-CR-200","texto":"A UBL invoice should not include the AccountingSupplierParty SellerContact","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingSupplierParty/cac:SellerContact)"},
{"id":"UBL-CR-201","texto":"A UBL invoice should not include the AccountingCustomerParty CustomerAssignedAccountID","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingCustomerParty/cbc:CustomerAssignedAccountID)"},
{"id":"UBL-CR-202","texto":"A UBL invoice should not include the AccountingCustomerParty SupplierAssignedAccountID","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingCustomerParty/cbc:SupplierAssignedAccountID)"},
{"id":"UBL-CR-203","texto":"A UBL invoice should not include the AccountingCustomerParty AdditionalAccountID","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingCustomerParty/cbc:AdditionalAccountID)"},
{"id":"UBL-CR-204","texto":"A UBL invoice should not include the AccountingCustomerParty Party MarkCareIndicator","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingCustomerParty/cac:Party/cbc:MarkCareIndicator)"},
{"id":"UBL-CR-205","texto":"A UBL invoice should not include the AccountingCustomerParty Party MarkAttentionIndicator","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingCustomerParty/cac:Party/cbc:MarkAttentionIndicator)"},
{"id":"UBL-CR-206","texto":"A UBL invoice should not include the AccountingCustomerParty Party WebsiteURI","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingCustomerParty/cac:Party/cbc:WebsiteURI)"},
{"id":"UBL-CR-207","texto":"A UBL invoice should not include the AccountingCustomerParty Party LogoReferenceID","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingCustomerParty/cac:Party/cbc:LogoReferenceID)"},
{"id":"UBL-CR-208","texto":"A UBL invoice should not include the AccountingCustomerParty Party IndustryClassificationCode","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingCustomerParty/cac:Party/cbc:IndustryClassificationCode)"},
{"id":"UBL-CR-209","texto":"A UBL invoice should not include the AccountingCustomerParty Party Language","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingCustomerParty/cac:Party/cac:Language)"},
{"id":"UBL-CR-210","texto":"A UBL invoice should not include the AccountingCustomerParty Party PostalAddress ID","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingCustomerParty/cac:Party/cac:PostalAddress/cbc:ID)"},
{"id":"UBL-CR-211","texto":"A UBL invoice should not include the AccountingCustomerParty Party PostalAddress AddressTypeCode","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingCustomerParty/cac:Party/cac:PostalAddress/cbc:AddressTypeCode)"},
{"id":"UBL-CR-212","texto":"A UBL invoice should not include the AccountingCustomerParty Party PostalAddress AddressFormatCode","categoria":"formato","natureza":"RP","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingCustomerParty/cac:Party/cac:PostalAddress/cbc:AddressFormatCode)"},
{"id":"UBL-CR-213","texto":"A UBL invoice should not include the AccountingCustomerParty Party PostalAddress Postbox","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingCustomerParty/cac:Party/cac:PostalAddress/cbc:Postbox)"},
{"id":"UBL-CR-214","texto":"A UBL invoice should not include the AccountingCustomerParty Party PostalAddress Floor","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingCustomerParty/cac:Party/cac:PostalAddress/cbc:Floor)"},
{"id":"UBL-CR-215","texto":"A UBL invoice should not include the AccountingCustomerParty Party PostalAddress Room","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingCustomerParty/cac:Party/cac:PostalAddress/cbc:Room)"},
{"id":"UBL-CR-216","texto":"A UBL invoice should not include the AccountingCustomerParty Party PostalAddress BlockName","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingCustomerParty/cac:Party/cac:PostalAddress/cbc:BlockName)"},
{"id":"UBL-CR-217","texto":"A UBL invoice should not include the AccountingCustomerParty Party PostalAddress BuildingName","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingCustomerParty/cac:Party/cac:PostalAddress/cbc:BuildingName)"},
{"id":"UBL-CR-218","texto":"A UBL invoice should not include the AccountingCustomerParty Party PostalAddress BuildingNumber","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingCustomerParty/cac:Party/cac:PostalAddress/cbc:BuildingNumber)"},
{"id":"UBL-CR-219","texto":"A UBL invoice should not include the AccountingCustomerParty Party PostalAddress InhouseMail","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingCustomerParty/cac:Party/cac:PostalAddress/cbc:InhouseMail)"},
{"id":"UBL-CR-220","texto":"A UBL invoice should not include the AccountingCustomerParty Party PostalAddress Department","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingCustomerParty/cac:Party/cac:PostalAddress/cbc:Department)"},
{"id":"UBL-CR-221","texto":"A UBL invoice should not include the AccountingCustomerParty Party PostalAddress MarkAttention","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingCustomerParty/cac:Party/cac:PostalAddress/cbc:MarkAttention)"},
{"id":"UBL-CR-222","texto":"A UBL invoice should not include the AccountingCustomerParty Party PostalAddress MarkCare","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingCustomerParty/cac:Party/cac:PostalAddress/cbc:MarkCare)"},
{"id":"UBL-CR-223","texto":"A UBL invoice should not include the AccountingCustomerParty Party PostalAddress PlotIdentification","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingCustomerParty/cac:Party/cac:PostalAddress/cbc:PlotIdentification)"},
{"id":"UBL-CR-224","texto":"A UBL invoice should not include the AccountingCustomerParty Party PostalAddress CitySubdivisionName","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingCustomerParty/cac:Party/cac:PostalAddress/cbc:CitySubdivisionName)"},
{"id":"UBL-CR-225","texto":"A UBL invoice should not include the AccountingCustomerParty Party PostalAddress CountrySubentityCode","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingCustomerParty/cac:Party/cac:PostalAddress/cbc:CountrySubentityCode)"},
{"id":"UBL-CR-226","texto":"A UBL invoice should not include the AccountingCustomerParty Party PostalAddress Region","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingCustomerParty/cac:Party/cac:PostalAddress/cbc:Region)"},
{"id":"UBL-CR-227","texto":"A UBL invoice should not include the AccountingCustomerParty Party PostalAddress District","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingCustomerParty/cac:Party/cac:PostalAddress/cbc:District)"},
{"id":"UBL-CR-228","texto":"A UBL invoice should not include the AccountingCustomerParty Party PostalAddress TimezoneOffset","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingCustomerParty/cac:Party/cac:PostalAddress/cbc:TimezoneOffset)"},
{"id":"UBL-CR-229","texto":"A UBL invoice should not include the AccountingCustomerParty Party PostalAddress Country Name","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingCustomerParty/cac:Party/cac:PostalAddress/cac:Country/cbc:Name)"},
{"id":"UBL-CR-230","texto":"A UBL invoice should not include the AccountingCustomerParty Party PostalAddress LocationCoordinate","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingCustomerParty/cac:Party/cac:PostalAddress/cac:LocationCoordinate)"},
{"id":"UBL-CR-231","texto":"A UBL invoice should not include the AccountingCustomerParty Party PhysicalLocation","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingCustomerParty/cac:Party/cac:PhysicalLocation)"},
{"id":"UBL-CR-232","texto":"A UBL invoice should not include the AccountingCustomerParty Party PartyTaxScheme RegistrationName","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingCustomerParty/cac:Party/cac:PartyTaxScheme/cbc:RegistrationName)"},
{"id":"UBL-CR-233","texto":"A UBL invoice should not include the AccountingCustomerParty Party PartyTaxScheme TaxLevelCode","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingCustomerParty/cac:Party/cac:PartyTaxScheme/cbc:TaxLevelCode)"},
{"id":"UBL-CR-234","texto":"A UBL invoice should not include the AccountingCustomerParty Party PartyTaxScheme ExemptionReasonCode","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingCustomerParty/cac:Party/cac:PartyTaxScheme/cbc:ExemptionReasonCode)"},
{"id":"UBL-CR-235","texto":"A UBL invoice should not include the AccountingCustomerParty Party PartyTaxScheme ExemptionReason","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingCustomerParty/cac:Party/cac:PartyTaxScheme/cbc:ExemptionReason)"},
{"id":"UBL-CR-236","texto":"A UBL invoice should not include the AccountingCustomerParty Party PartyTaxScheme RegistrationAddress","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingCustomerParty/cac:Party/cac:PartyTaxScheme/cac:RegistrationAddress)"},
{"id":"UBL-CR-237","texto":"A UBL invoice should not include the AccountingCustomerParty Party PartyTaxScheme TaxScheme Name","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingCustomerParty/cac:Party/cac:PartyTaxScheme/cac:TaxScheme/cbc:Name)"},
{"id":"UBL-CR-238","texto":"A UBL invoice should not include the AccountingCustomerParty Party PartyTaxScheme TaxScheme TaxTypeCode","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingCustomerParty/cac:Party/cac:PartyTaxScheme/cac:TaxScheme/cbc:TaxTypeCode)"},
{"id":"UBL-CR-239","texto":"A UBL invoice should not include the AccountingCustomerParty Party PartyTaxScheme TaxScheme CurrencyCode","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingCustomerParty/cac:Party/cac:PartyTaxScheme/cac:TaxScheme/cbc:CurrencyCode)"},
{"id":"UBL-CR-240","texto":"A UBL invoice should not include the AccountingCustomerParty Party PartyTaxScheme TaxScheme JurisdictionRegionAddress","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingCustomerParty/cac:Party/cac:PartyTaxScheme/cac:TaxScheme/cac:JurisdictionRegionAddress)"},
{"id":"UBL-CR-241","texto":"A UBL invoice should not include the AccountingCustomerParty Party PartyLegalEntity RegistrationDate","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingCustomerParty/cac:Party/cac:PartyLegalEntity/cbc:RegistrationDate)"},
{"id":"UBL-CR-242","texto":"A UBL invoice should not include the AccountingCustomerParty Party PartyLegalEntity RegistrationExpirationDate","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingCustomerParty/cac:Party/cac:PartyLegalEntity/cbc:RegistrationExpirationDate)"},
{"id":"UBL-CR-243","texto":"A UBL invoice should not include the AccountingCustomerParty Party PartyLegalEntity CompanyLegalFormCode","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingCustomerParty/cac:Party/cac:PartyLegalEntity/cbc:CompanyLegalFormCode)"},
{"id":"UBL-CR-244","texto":"A UBL invoice should not include the AccountingCustomerParty Party PartyLegalEntity CompanyLegalForm","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingCustomerParty/cac:Party/cac:PartyLegalEntity/cbc:CompanyLegalForm)"},
{"id":"UBL-CR-245","texto":"A UBL invoice should not include the AccountingCustomerParty Party PartyLegalEntity SoleProprietorshipIndicator","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingCustomerParty/cac:Party/cac:PartyLegalEntity/cbc:SoleProprietorshipIndicator)"},
{"id":"UBL-CR-246","texto":"A UBL invoice should not include the AccountingCustomerParty Party PartyLegalEntity CompanyLiquidationStatusCode","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingCustomerParty/cac:Party/cac:PartyLegalEntity/cbc:CompanyLiquidationStatusCode)"},
{"id":"UBL-CR-247","texto":"A UBL invoice should not include the AccountingCustomerParty Party PartyLegalEntity CorporationStockAmount","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingCustomerParty/cac:Party/cac:PartyLegalEntity/cbc:CorporationStockAmount)"},
{"id":"UBL-CR-248","texto":"A UBL invoice should not include the AccountingCustomerParty Party PartyLegalEntity FullyPaidSharesIndicator","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingCustomerParty/cac:Party/cac:PartyLegalEntity/cbc:FullyPaidSharesIndicator)"},
{"id":"UBL-CR-249","texto":"A UBL invoice should not include the AccountingCustomerParty Party PartyLegalEntity RegistrationAddress","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingCustomerParty/cac:Party/cac:PartyLegalEntity/cac:RegistrationAddress)"},
{"id":"UBL-CR-250","texto":"A UBL invoice should not include the AccountingCustomerParty Party PartyLegalEntity CorporateRegistrationScheme","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingCustomerParty/cac:Party/cac:PartyLegalEntity/cac:CorporateRegistrationScheme)"},
{"id":"UBL-CR-251","texto":"A UBL invoice should not include the AccountingCustomerParty Party PartyLegalEntity HeadOfficeParty","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingCustomerParty/cac:Party/cac:PartyLegalEntity/cac:HeadOfficeParty)"},
{"id":"UBL-CR-252","texto":"A UBL invoice should not include the AccountingCustomerParty Party PartyLegalEntity ShareholderParty","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingCustomerParty/cac:Party/cac:PartyLegalEntity/cac:ShareholderParty)"},
{"id":"UBL-CR-253","texto":"A UBL invoice should not include the AccountingCustomerParty Party Contact ID","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingCustomerParty/cac:Party/cac:Contact/cbc:ID)"},
{"id":"UBL-CR-254","texto":"A UBL invoice should not include the AccountingCustomerParty Party Contact Telefax","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingCustomerParty/cac:Party/cac:Contact/cbc:Telefax)"},
{"id":"UBL-CR-255","texto":"A UBL invoice should not include the AccountingCustomerParty Party Contact Note","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingCustomerParty/cac:Party/cac:Contact/cbc:Note)"},
{"id":"UBL-CR-256","texto":"A UBL invoice should not include the AccountingCustomerParty Party Contact OtherCommunication","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingCustomerParty/cac:Party/cac:Contact/cac:OtherCommunication)"},
{"id":"UBL-CR-257","texto":"A UBL invoice should not include the AccountingCustomerParty Party Person","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingCustomerParty/cac:Party/cac:Person)"},
{"id":"UBL-CR-258","texto":"A UBL invoice should not include the AccountingCustomerParty Party AgentParty","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingCustomerParty/cac:Party/cac:AgentParty)"},
{"id":"UBL-CR-259","texto":"A UBL invoice should not include the AccountingCustomerParty Party ServiceProviderParty","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingCustomerParty/cac:Party/cac:ServiceProviderParty)"},
{"id":"UBL-CR-260","texto":"A UBL invoice should not include the AccountingCustomerParty Party PowerOfAttorney","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingCustomerParty/cac:Party/cac:PowerOfAttorney)"},
{"id":"UBL-CR-261","texto":"A UBL invoice should not include the AccountingCustomerParty Party FinancialAccount","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingCustomerParty/cac:Party/cac:FinancialAccount)"},
{"id":"UBL-CR-262","texto":"A UBL invoice should not include the AccountingCustomerParty DeliveryContact","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingCustomerParty/cac:DeliveryContact)"},
{"id":"UBL-CR-263","texto":"A UBL invoice should not include the AccountingCustomerParty AccountingContact","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingCustomerParty/cac:AccountingContact)"},
{"id":"UBL-CR-264","texto":"A UBL invoice should not include the AccountingCustomerParty BuyerContact","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingCustomerParty/cac:BuyerContact)"},
{"id":"UBL-CR-265","texto":"A UBL invoice should not include the PayeeParty MarkCareIndicator","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:PayeeParty/cbc:MarkCareIndicator)"},
{"id":"UBL-CR-266","texto":"A UBL invoice should not include the PayeeParty MarkAttentionIndicator","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:PayeeParty/cbc:MarkAttentionIndicator)"},
{"id":"UBL-CR-267","texto":"A UBL invoice should not include the PayeeParty WebsiteURI","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:PayeeParty/cbc:WebsiteURI)"},
{"id":"UBL-CR-268","texto":"A UBL invoice should not include the PayeeParty LogoReferenceID","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:PayeeParty/cbc:LogoReferenceID)"},
{"id":"UBL-CR-269","texto":"A UBL invoice should not include the PayeeParty EndpointID","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:PayeeParty/cbc:EndpointID)"},
{"id":"UBL-CR-270","texto":"A UBL invoice should not include the PayeeParty IndustryClassificationCode","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:PayeeParty/cbc:IndustryClassificationCode)"},
{"id":"UBL-CR-271","texto":"A UBL invoice should not include the PayeeParty Language","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:PayeeParty/cac:Language)"},
{"id":"UBL-CR-272","texto":"A UBL invoice should not include the PayeeParty PostalAddress","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:PayeeParty/cac:PostalAddress)"},
{"id":"UBL-CR-273","texto":"A UBL invoice should not include the PayeeParty PhysicalLocation","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:PayeeParty/cac:PhysicalLocation)"},
{"id":"UBL-CR-274","texto":"A UBL invoice should not include the PayeeParty PartyTaxScheme","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:PayeeParty/cac:PartyTaxScheme)"},
{"id":"UBL-CR-275","texto":"A UBL invoice should not include the PayeeParty PartyLegalEntity RegistrationName","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:PayeeParty/cac:PartyLegalEntity/cbc:RegistrationName)"},
{"id":"UBL-CR-276","texto":"A UBL invoice should not include the PayeeParty PartyLegalEntity RegistrationDate","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:PayeeParty/cac:PartyLegalEntity/cbc:RegistrationDate)"},
{"id":"UBL-CR-277","texto":"A UBL invoice should not include the PayeeParty PartyLegalEntity RegistrationExpirationDate","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:PayeeParty/cac:PartyLegalEntity/cbc:RegistrationExpirationDate)"},
{"id":"UBL-CR-278","texto":"A UBL invoice should not include the PayeeParty PartyLegalEntity CompanyLegalFormCode","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:PayeeParty/cac:PartyLegalEntity/cbc:CompanyLegalFormCode)"},
{"id":"UBL-CR-279","texto":"A UBL invoice should not include the PayeeParty PartyLegalEntity CompanyLegalForm","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:PayeeParty/cac:PartyLegalEntity/cbc:CompanyLegalForm)"},
{"id":"UBL-CR-280","texto":"A UBL invoice should not include the PayeeParty PartyLegalEntity SoleProprietorshipIndicator","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:PayeeParty/cac:PartyLegalEntity/cbc:SoleProprietorshipIndicator)"},
{"id":"UBL-CR-281","texto":"A UBL invoice should not include the PayeeParty PartyLegalEntity CompanyLiquidationStatusCode","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:PayeeParty/cac:PartyLegalEntity/cbc:CompanyLiquidationStatusCode)"},
{"id":"UBL-CR-282","texto":"A UBL invoice should not include the PayeeParty PartyLegalEntity CorporationStockAmount","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:PayeeParty/cac:PartyLegalEntity/cbc:CorporationStockAmount)"},
{"id":"UBL-CR-283","texto":"A UBL invoice should not include the PayeeParty PartyLegalEntity FullyPaidSharesIndicator","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:PayeeParty/cac:PartyLegalEntity/cbc:FullyPaidSharesIndicator)"},
{"id":"UBL-CR-284","texto":"A UBL invoice should not include the PayeeParty PartyLegalEntity RegistrationAddress","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:PayeeParty/cac:PartyLegalEntity/cac:RegistrationAddress)"},
{"id":"UBL-CR-285","texto":"A UBL invoice should not include the PayeeParty PartyLegalEntity CorporateRegistrationScheme","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:PayeeParty/cac:PartyLegalEntity/cac:CorporateRegistrationScheme)"},
{"id":"UBL-CR-286","texto":"A UBL invoice should not include the PayeeParty PartyLegalEntity HeadOfficeParty","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:PayeeParty/cac:PartyLegalEntity/cac:HeadOfficeParty)"},
{"id":"UBL-CR-287","texto":"A UBL invoice should not include the PayeeParty PartyLegalEntity ShareholderParty","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:PayeeParty/cac:PartyLegalEntity/cac:ShareholderParty)"},
{"id":"UBL-CR-288","texto":"A UBL invoice should not include the PayeeParty Contact","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:PayeeParty/cac:Contact)"},
{"id":"UBL-CR-289","texto":"A UBL invoice should not include the PayeeParty Person","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:PayeeParty/cac:Person)"},
{"id":"UBL-CR-290","texto":"A UBL invoice should not include the PayeeParty AgentParty","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:PayeeParty/cac:AgentParty)"},
{"id":"UBL-CR-291","texto":"A UBL invoice should not include the PayeeParty ServiceProviderParty","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:PayeeParty/cac:ServiceProviderParty)"},
{"id":"UBL-CR-292","texto":"A UBL invoice should not include the PayeeParty PowerOfAttorney","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:PayeeParty/cac:PowerOfAttorney)"},
{"id":"UBL-CR-293","texto":"A UBL invoice should not include the PayeeParty FinancialAccount","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:PayeeParty/cac:FinancialAccount)"},
{"id":"UBL-CR-294","texto":"A UBL invoice should not include the BuyerCustomerParty","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:BuyerCustomerParty)"},
{"id":"UBL-CR-295","texto":"A UBL invoice should not include the SellerCustomerParty","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:SellerCustomerParty)"},
{"id":"UBL-CR-296","texto":"A UBL invoice should not include the TaxRepresentativeParty MarkCareIndicator","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:TaxRepresentativeParty/cbc:MarkCareIndicator)"},
{"id":"UBL-CR-297","texto":"A UBL invoice should not include the TaxRepresentativeParty MarkAttentionIndicator","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:TaxRepresentativeParty/cbc:MarkAttentionIndicator)"},
{"id":"UBL-CR-298","texto":"A UBL invoice should not include the TaxRepresentativeParty WebsiteURI","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:TaxRepresentativeParty/cbc:WebsiteURI)"},
{"id":"UBL-CR-299","texto":"A UBL invoice should not include the TaxRepresentativeParty LogoReferenceID","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:TaxRepresentativeParty/cbc:LogoReferenceID)"},
{"id":"UBL-CR-300","texto":"A UBL invoice should not include the TaxRepresentativeParty EndpointID","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:TaxRepresentativeParty/cbc:EndpointID)"},
{"id":"UBL-CR-301","texto":"A UBL invoice should not include the TaxRepresentativeParty IndustryClassificationCode","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:TaxRepresentativeParty/cbc:IndustryClassificationCode)"},
{"id":"UBL-CR-302","texto":"A UBL invoice should not include the TaxRepresentativeParty PartyIdentification","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:TaxRepresentativeParty/cac:PartyIdentification)"},
{"id":"UBL-CR-303","texto":"A UBL invoice should not include the TaxRepresentativeParty Language","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:TaxRepresentativeParty/cac:Language)"},
{"id":"UBL-CR-304","texto":"A UBL invoice should not include the TaxRepresentativeParty PostalAddress ID","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:TaxRepresentativeParty/cac:PostalAddress/cbc:ID)"},
{"id":"UBL-CR-305","texto":"A UBL invoice should not include the TaxRepresentativeParty PostalAddress AddressTypeCode","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:TaxRepresentativeParty/cac:PostalAddress/cbc:AddressTypeCode)"},
{"id":"UBL-CR-306","texto":"A UBL invoice should not include the TaxRepresentativeParty PostalAddress AddressFormatCode","categoria":"formato","natureza":"RP","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:TaxRepresentativeParty/cac:PostalAddress/cbc:AddressFormatCode)"},
{"id":"UBL-CR-307","texto":"A UBL invoice should not include the TaxRepresentativeParty PostalAddress Postbox","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:TaxRepresentativeParty/cac:PostalAddress/cbc:Postbox)"},
{"id":"UBL-CR-308","texto":"A UBL invoice should not include the TaxRepresentativeParty PostalAddress Floor","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:TaxRepresentativeParty/cac:PostalAddress/cbc:Floor)"},
{"id":"UBL-CR-309","texto":"A UBL invoice should not include the TaxRepresentativeParty PostalAddress Room","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:TaxRepresentativeParty/cac:PostalAddress/cbc:Room)"},
{"id":"UBL-CR-310","texto":"A UBL invoice should not include the TaxRepresentativeParty PostalAddress BlockName","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:TaxRepresentativeParty/cac:PostalAddress/cbc:BlockName)"},
{"id":"UBL-CR-311","texto":"A UBL invoice should not include the TaxRepresentativeParty PostalAddress BuildingName","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:TaxRepresentativeParty/cac:PostalAddress/cbc:BuildingName)"},
{"id":"UBL-CR-312","texto":"A UBL invoice should not include the TaxRepresentativeParty PostalAddress BuildingNumber","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:TaxRepresentativeParty/cac:PostalAddress/cbc:BuildingNumber)"},
{"id":"UBL-CR-313","texto":"A UBL invoice should not include the TaxRepresentativeParty PostalAddress InhouseMail","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:TaxRepresentativeParty/cac:PostalAddress/cbc:InhouseMail)"},
{"id":"UBL-CR-314","texto":"A UBL invoice should not include the TaxRepresentativeParty PostalAddress Department","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:TaxRepresentativeParty/cac:PostalAddress/cbc:Department)"},
{"id":"UBL-CR-315","texto":"A UBL invoice should not include the TaxRepresentativeParty PostalAddress MarkAttention","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:TaxRepresentativeParty/cac:PostalAddress/cbc:MarkAttention)"},
{"id":"UBL-CR-316","texto":"A UBL invoice should not include the TaxRepresentativeParty PostalAddress MarkCare","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:TaxRepresentativeParty/cac:PostalAddress/cbc:MarkCare)"},
{"id":"UBL-CR-317","texto":"A UBL invoice should not include the TaxRepresentativeParty PostalAddress PlotIdentification","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:TaxRepresentativeParty/cac:PostalAddress/cbc:PlotIdentification)"},
{"id":"UBL-CR-318","texto":"A UBL invoice should not include the TaxRepresentativeParty PostalAddress CitySubdivisionName","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:TaxRepresentativeParty/cac:PostalAddress/cbc:CitySubdivisionName)"},
{"id":"UBL-CR-319","texto":"A UBL invoice should not include the TaxRepresentativeParty PostalAddress CountrySubentityCode","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:TaxRepresentativeParty/cac:PostalAddress/cbc:CountrySubentityCode)"},
{"id":"UBL-CR-320","texto":"A UBL invoice should not include the TaxRepresentativeParty PostalAddress Region","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:TaxRepresentativeParty/cac:PostalAddress/cbc:Region)"},
{"id":"UBL-CR-321","texto":"A UBL invoice should not include the TaxRepresentativeParty PostalAddress District","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:TaxRepresentativeParty/cac:PostalAddress/cbc:District)"},
{"id":"UBL-CR-322","texto":"A UBL invoice should not include the TaxRepresentativeParty PostalAddress TimezoneOffset","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:TaxRepresentativeParty/cac:PostalAddress/cbc:TimezoneOffset)"},
{"id":"UBL-CR-323","texto":"A UBL invoice should not include the TaxRepresentativeParty PostalAddress Country Name","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:TaxRepresentativeParty/cac:PostalAddress/cac:Country/cbc:Name)"},
{"id":"UBL-CR-324","texto":"A UBL invoice should not include the TaxRepresentativeParty PostalAddress LocationCoordinate","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:TaxRepresentativeParty/cac:PostalAddress/cac:LocationCoordinate)"},
{"id":"UBL-CR-325","texto":"A UBL invoice should not include the TaxRepresentativeParty PhysicalLocation","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:TaxRepresentativeParty/cac:PhysicalLocation)"},
{"id":"UBL-CR-326","texto":"A UBL invoice should not include the TaxRepresentativeParty PartyTaxScheme RegistrationName","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:TaxRepresentativeParty/cac:PartyTaxScheme/cbc:RegistrationName)"},
{"id":"UBL-CR-327","texto":"A UBL invoice should not include the TaxRepresentativeParty PartyTaxScheme TaxLevelCode","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:TaxRepresentativeParty/cac:PartyTaxScheme/cbc:TaxLevelCode)"},
{"id":"UBL-CR-328","texto":"A UBL invoice should not include the TaxRepresentativeParty PartyTaxScheme ExemptionReasonCode","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:TaxRepresentativeParty/cac:PartyTaxScheme/cbc:ExemptionReasonCode)"},
{"id":"UBL-CR-329","texto":"A UBL invoice should not include the TaxRepresentativeParty PartyTaxScheme ExemptionReason","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:TaxRepresentativeParty/cac:PartyTaxScheme/cbc:ExemptionReason)"},
{"id":"UBL-CR-330","texto":"A UBL invoice should not include the TaxRepresentativeParty PartyTaxScheme RegistrationAddress","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:TaxRepresentativeParty/cac:PartyTaxScheme/cac:RegistrationAddress)"},
{"id":"UBL-CR-331","texto":"A UBL invoice should not include the TaxRepresentativeParty PartyTaxScheme TaxScheme Name","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:TaxRepresentativeParty/cac:PartyTaxScheme/cac:TaxScheme/cbc:Name)"},
{"id":"UBL-CR-332","texto":"A UBL invoice should not include the TaxRepresentativeParty PartyTaxScheme TaxScheme TaxTypeCode","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:TaxRepresentativeParty/cac:PartyTaxScheme/cac:TaxScheme/cbc:TaxTypeCode)"},
{"id":"UBL-CR-333","texto":"A UBL invoice should not include the TaxRepresentativeParty PartyTaxScheme TaxScheme CurrencyCode","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:TaxRepresentativeParty/cac:PartyTaxScheme/cac:TaxScheme/cbc:CurrencyCode)"},
{"id":"UBL-CR-334","texto":"A UBL invoice should not include the TaxRepresentativeParty PartyTaxScheme TaxScheme JurisdictionRegionAddress","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:TaxRepresentativeParty/cac:PartyTaxScheme/cac:TaxScheme/cac:JurisdictionRegionAddress)"},
{"id":"UBL-CR-335","texto":"A UBL invoice should not include the TaxRepresentativeParty PartyLegalEntity","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:TaxRepresentativeParty/cac:PartyLegalEntity)"},
{"id":"UBL-CR-336","texto":"A UBL invoice should not include the TaxRepresentativeParty Contact","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:TaxRepresentativeParty/cac:Contact)"},
{"id":"UBL-CR-337","texto":"A UBL invoice should not include the TaxRepresentativeParty Person","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:TaxRepresentativeParty/cac:Person)"},
{"id":"UBL-CR-338","texto":"A UBL invoice should not include the TaxRepresentativeParty AgentParty","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:TaxRepresentativeParty/cac:AgentParty)"},
{"id":"UBL-CR-339","texto":"A UBL invoice should not include the TaxRepresentativeParty ServiceProviderParty","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:TaxRepresentativeParty/cac:ServiceProviderParty)"},
{"id":"UBL-CR-340","texto":"A UBL invoice should not include the TaxRepresentativeParty PowerOfAttorney","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:TaxRepresentativeParty/cac:PowerOfAttorney)"},
{"id":"UBL-CR-341","texto":"A UBL invoice should not include the TaxRepresentativeParty FinancialAccount","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:TaxRepresentativeParty/cac:FinancialAccount)"},
{"id":"UBL-CR-342","texto":"A UBL invoice should not include the Delivery ID","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:Delivery/cbc:ID)"},
{"id":"UBL-CR-343","texto":"A UBL invoice should not include the Delivery Quantity","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:Delivery/cbc:Quantity)"},
{"id":"UBL-CR-344","texto":"A UBL invoice should not include the Delivery MinimumQuantity","categoria":"gama","natureza":"RP","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:Delivery/cbc:MinimumQuantity)"},
{"id":"UBL-CR-345","texto":"A UBL invoice should not include the Delivery MaximumQuantity","categoria":"gama","natureza":"RP","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:Delivery/cbc:MaximumQuantity)"},
{"id":"UBL-CR-346","texto":"A UBL invoice should not include the Delivery ActualDeliveryTime","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:Delivery/cbc:ActualDeliveryTime)"},
{"id":"UBL-CR-347","texto":"A UBL invoice should not include the Delivery LatestDeliveryDate","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:Delivery/cbc:LatestDeliveryDate)"},
{"id":"UBL-CR-348","texto":"A UBL invoice should not include the Delivery LatestDeliveryTime","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:Delivery/cbc:LatestDeliveryTime)"},
{"id":"UBL-CR-349","texto":"A UBL invoice should not include the Delivery ReleaseID","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:Delivery/cbc:ReleaseID)"},
{"id":"UBL-CR-350","texto":"A UBL invoice should not include the Delivery TrackingID","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:Delivery/cbc:TrackingID)"},
{"id":"UBL-CR-351","texto":"A UBL invoice should not include the Delivery DeliveryLocation Description","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:Delivery/cac:DeliveryLocation/cbc:Description)"},
{"id":"UBL-CR-352","texto":"A UBL invoice should not include the Delivery DeliveryLocation Conditions","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:Delivery/cac:DeliveryLocation/cbc:Conditions)"},
{"id":"UBL-CR-353","texto":"A UBL invoice should not include the Delivery DeliveryLocation CountrySubentity","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:Delivery/cac:DeliveryLocation/cbc:CountrySubentity)"},
{"id":"UBL-CR-354","texto":"A UBL invoice should not include the Delivery DeliveryLocation CountrySubentityCode","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:Delivery/cac:DeliveryLocation/cbc:CountrySubentityCode)"},
{"id":"UBL-CR-355","texto":"A UBL invoice should not include the Delivery DeliveryLocation LocationTypeCode","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:Delivery/cac:DeliveryLocation/cbc:LocationTypeCode)"},
{"id":"UBL-CR-356","texto":"A UBL invoice should not include the Delivery DeliveryLocation InformationURI","categoria":"formato","natureza":"RP","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:Delivery/cac:DeliveryLocation/cbc:InformationURI)"},
{"id":"UBL-CR-357","texto":"A UBL invoice should not include the Delivery DeliveryLocation Name","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:Delivery/cac:DeliveryLocation/cbc:Name)"},
{"id":"UBL-CR-358","texto":"A UBL invoice should not include the Delivery DeliveryLocation ValidationPeriod","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:Delivery/cac:DeliveryLocation/cac:ValidationPeriod)"},
{"id":"UBL-CR-359","texto":"A UBL invoice should not include the Delivery DeliveryLocation Address ID","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:Delivery/cac:DeliveryLocation/cac:Address/cbc:ID)"},
{"id":"UBL-CR-360","texto":"A UBL invoice should not include the Delivery DeliveryLocation Address AddressTypeCode","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:Delivery/cac:DeliveryLocation/cac:Address/cbc:AddressTypeCode)"},
{"id":"UBL-CR-361","texto":"A UBL invoice should not include the Delivery DeliveryLocation Address AddressFormatCode","categoria":"formato","natureza":"RP","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:Delivery/cac:DeliveryLocation/cac:Address/cbc:AddressFormatCode)"},
{"id":"UBL-CR-362","texto":"A UBL invoice should not include the Delivery DeliveryLocation Address Postbox","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:Delivery/cac:DeliveryLocation/cac:Address/cbc:Postbox)"},
{"id":"UBL-CR-363","texto":"A UBL invoice should not include the Delivery DeliveryLocation Address Floor","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:Delivery/cac:DeliveryLocation/cac:Address/cbc:Floor)"},
{"id":"UBL-CR-364","texto":"A UBL invoice should not include the Delivery DeliveryLocation Address Room","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:Delivery/cac:DeliveryLocation/cac:Address/cbc:Room)"},
{"id":"UBL-CR-365","texto":"A UBL invoice should not include the Delivery DeliveryLocation Address BlockName","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:Delivery/cac:DeliveryLocation/cac:Address/cbc:BlockName)"},
{"id":"UBL-CR-366","texto":"A UBL invoice should not include the Delivery DeliveryLocation Address BuildingName","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:Delivery/cac:DeliveryLocation/cac:Address/cbc:BuildingName)"},
{"id":"UBL-CR-367","texto":"A UBL invoice should not include the Delivery DeliveryLocation Address BuildingNumber","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:Delivery/cac:DeliveryLocation/cac:Address/cbc:BuildingNumber)"},
{"id":"UBL-CR-368","texto":"A UBL invoice should not include the Delivery DeliveryLocation Address InhouseMail","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:Delivery/cac:DeliveryLocation/cac:Address/cbc:InhouseMail)"},
{"id":"UBL-CR-369","texto":"A UBL invoice should not include the Delivery DeliveryLocation Address Department","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:Delivery/cac:DeliveryLocation/cac:Address/cbc:Department)"},
{"id":"UBL-CR-370","texto":"A UBL invoice should not include the Delivery DeliveryLocation Address MarkAttention","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:Delivery/cac:DeliveryLocation/cac:Address/cbc:MarkAttention)"},
{"id":"UBL-CR-371","texto":"A UBL invoice should not include the Delivery DeliveryLocation Address MarkCare","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:Delivery/cac:DeliveryLocation/cac:Address/cbc:MarkCare)"},
{"id":"UBL-CR-372","texto":"A UBL invoice should not include the Delivery DeliveryLocation Address PlotIdentification","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:Delivery/cac:DeliveryLocation/cac:Address/cbc:PlotIdentification)"},
{"id":"UBL-CR-373","texto":"A UBL invoice should not include the Delivery DeliveryLocation Address CitySubdivisionName","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:Delivery/cac:DeliveryLocation/cac:Address/cbc:CitySubdivisionName)"},
{"id":"UBL-CR-374","texto":"A UBL invoice should not include the Delivery DeliveryLocation Address CountrySubentityCode","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:Delivery/cac:DeliveryLocation/cac:Address/cbc:CountrySubentityCode)"},
{"id":"UBL-CR-375","texto":"A UBL invoice should not include the Delivery DeliveryLocation Address Region","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:Delivery/cac:DeliveryLocation/cac:Address/cbc:Region)"},
{"id":"UBL-CR-376","texto":"A UBL invoice should not include the Delivery DeliveryLocation Address District","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:Delivery/cac:DeliveryLocation/cac:Address/cbc:District)"},
{"id":"UBL-CR-377","texto":"A UBL invoice should not include the Delivery DeliveryLocation Address TimezoneOffset","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:Delivery/cac:DeliveryLocation/cac:Address/cbc:TimezoneOffset)"},
{"id":"UBL-CR-378","texto":"A UBL invoice should not include the Delivery DeliveryLocation Address Country Name","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:Delivery/cac:DeliveryLocation/cac:Address/cac:Country/cbc:Name)"},
{"id":"UBL-CR-379","texto":"A UBL invoice should not include the Delivery DeliveryLocation Address LocationCoordinate","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:Delivery/cac:DeliveryLocation/cac:Address/cac:LocationCoordinate)"},
{"id":"UBL-CR-380","texto":"A UBL invoice should not include the Delivery DeliveryLocation SubsidiaryLocation","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:Delivery/cac:DeliveryLocation/cac:SubsidiaryLocation)"},
{"id":"UBL-CR-381","texto":"A UBL invoice should not include the Delivery DeliveryLocation LocationCoordinate","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:Delivery/cac:DeliveryLocation/cac:LocationCoordinate)"},
{"id":"UBL-CR-382","texto":"A UBL invoice should not include the Delivery AlternativeDeliveryLocation","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:Delivery/cac:AlternativeDeliveryLocation)"},
{"id":"UBL-CR-383","texto":"A UBL invoice should not include the Delivery RequestedDeliveryPeriod","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:Delivery/cac:RequestedDeliveryPeriod)"},
{"id":"UBL-CR-384","texto":"A UBL invoice should not include the Delivery PromisedDeliveryPeriod","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:Delivery/cac:PromisedDeliveryPeriod)"},
{"id":"UBL-CR-385","texto":"A UBL invoice should not include the Delivery CarrierParty","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:Delivery/cac:CarrierParty)"},
{"id":"UBL-CR-386","texto":"A UBL invoice should not include the DeliveryParty MarkCareIndicator","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:Delivery/cac:DeliveryParty/cbc:MarkCareIndicator)"},
{"id":"UBL-CR-387","texto":"A UBL invoice should not include the DeliveryParty MarkAttentionIndicator","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:Delivery/cac:DeliveryParty/cbc:MarkAttentionIndicator)"},
{"id":"UBL-CR-388","texto":"A UBL invoice should not include the DeliveryParty WebsiteURI","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:Delivery/cac:DeliveryParty/cbc:WebsiteURI)"},
{"id":"UBL-CR-389","texto":"A UBL invoice should not include the DeliveryParty LogoReferenceID","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:Delivery/cac:DeliveryParty/cbc:LogoReferenceID)"},
{"id":"UBL-CR-390","texto":"A UBL invoice should not include the DeliveryParty EndpointID","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:Delivery/cac:DeliveryParty/cbc:EndpointID)"},
{"id":"UBL-CR-391","texto":"A UBL invoice should not include the DeliveryParty IndustryClassificationCode","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:Delivery/cac:DeliveryParty/cbc:IndustryClassificationCode)"},
{"id":"UBL-CR-392","texto":"A UBL invoice should not include the DeliveryParty PartyIdentification","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:Delivery/cac:DeliveryParty/cac:PartyIdentification)"},
{"id":"UBL-CR-393","texto":"A UBL invoice should not include the DeliveryParty Language","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:Delivery/cac:DeliveryParty/cac:Language)"},
{"id":"UBL-CR-394","texto":"A UBL invoice should not include the DeliveryParty PostalAddress","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:Delivery/cac:DeliveryParty/cac:PostalAddress)"},
{"id":"UBL-CR-395","texto":"A UBL invoice should not include the DeliveryParty PhysicalLocation","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:Delivery/cac:DeliveryParty/cac:PhysicalLocation)"},
{"id":"UBL-CR-396","texto":"A UBL invoice should not include the DeliveryParty PartyTaxScheme","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:Delivery/cac:DeliveryParty/cac:PartyTaxScheme)"},
{"id":"UBL-CR-397","texto":"A UBL invoice should not include the DeliveryParty PartyLegalEntity","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:Delivery/cac:DeliveryParty/cac:PartyLegalEntity)"},
{"id":"UBL-CR-398","texto":"A UBL invoice should not include the DeliveryParty Contact","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:Delivery/cac:DeliveryParty/cac:Contact)"},
{"id":"UBL-CR-399","texto":"A UBL invoice should not include the DeliveryParty Person","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:Delivery/cac:DeliveryParty/cac:Person)"},
{"id":"UBL-CR-400","texto":"A UBL invoice should not include the DeliveryParty AgentParty","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:Delivery/cac:DeliveryParty/cac:AgentParty)"},
{"id":"UBL-CR-401","texto":"A UBL invoice should not include the DeliveryParty ServiceProviderParty","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:Delivery/cac:DeliveryParty/cac:ServiceProviderParty)"},
{"id":"UBL-CR-402","texto":"A UBL invoice should not include the DeliveryParty PowerOfAttorney","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:Delivery/cac:DeliveryParty/cac:PowerOfAttorney)"},
{"id":"UBL-CR-403","texto":"A UBL invoice should not include the DeliveryParty FinancialAccount","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:Delivery/cac:DeliveryParty/cac:FinancialAccount)"},
{"id":"UBL-CR-404","texto":"A UBL invoice should not include the Delivery NotifyParty","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:Delivery/cac:NotifyParty)"},
{"id":"UBL-CR-405","texto":"A UBL invoice should not include the Delivery Despatch","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:Delivery/cac:Despatch)"},
{"id":"UBL-CR-406","texto":"A UBL invoice should not include the Delivery DeliveryTerms","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:Delivery/cac:DeliveryTerms)"},
{"id":"UBL-CR-407","texto":"A UBL invoice should not include the Delivery MinimumDeliveryUnit","categoria":"gama","natureza":"RP","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:Delivery/cac:MinimumDeliveryUnit)"},
{"id":"UBL-CR-408","texto":"A UBL invoice should not include the Delivery MaximumDeliveryUnit","categoria":"gama","natureza":"RP","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:Delivery/cac:MaximumDeliveryUnit)"},
{"id":"UBL-CR-409","texto":"A UBL invoice should not include the Delivery Shipment","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:Delivery/cac:Shipment)"},
{"id":"UBL-CR-410","texto":"A UBL invoice should not include the DeliveryTerms","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:DeliveryTerms)"},
{"id":"UBL-CR-411","texto":"A UBL invoice should not include the PaymentMeans ID","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:PaymentMeans/cbc:ID)"},
{"id":"UBL-CR-412","texto":"A UBL invoice should not include the PaymentMeans PaymentDueDate","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:PaymentMeans/cbc:PaymentDueDate)"},
{"id":"UBL-CR-413","texto":"A UBL invoice should not include the PaymentMeans PaymentChannelCode","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:PaymentMeans/cbc:PaymentChannelCode)"},
{"id":"UBL-CR-414","texto":"A UBL invoice should not include the PaymentMeans InstructionID","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:PaymentMeans/cbc:InstructionID)"},
{"id":"UBL-CR-415","texto":"A UBL invoice should not include the PaymentMeans CardAccount CardTypeCode","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:PaymentMeans/cac:CardAccount/cbc:CardTypeCode)"},
{"id":"UBL-CR-416","texto":"A UBL invoice should not include the PaymentMeans CardAccount ValidityStartDate","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:PaymentMeans/cac:CardAccount/cbc:ValidityStartDate)"},
{"id":"UBL-CR-417","texto":"A UBL invoice should not include the PaymentMeans CardAccount ExpiryDate","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:PaymentMeans/cac:CardAccount/cbc:ExpiryDate)"},
{"id":"UBL-CR-418","texto":"A UBL invoice should not include the PaymentMeans CardAccount IssuerID","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:PaymentMeans/cac:CardAccount/cbc:IssuerID)"},
{"id":"UBL-CR-419","texto":"A UBL invoice should not include the PaymentMeans CardAccount IssuerNumberID","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:PaymentMeans/cac:CardAccount/cbc:IssuerNumberID)"},
{"id":"UBL-CR-420","texto":"A UBL invoice should not include the PaymentMeans CardAccount CV2ID","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:PaymentMeans/cac:CardAccount/cbc:CV2ID)"},
{"id":"UBL-CR-421","texto":"A UBL invoice should not include the PaymentMeans CardAccount CardChipCode","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:PaymentMeans/cac:CardAccount/cbc:CardChipCode)"},
{"id":"UBL-CR-422","texto":"A UBL invoice should not include the PaymentMeans CardAccount ChipApplicationID","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:PaymentMeans/cac:CardAccount/cbc:ChipApplicationID)"},
{"id":"UBL-CR-423","texto":"A UBL invoice should not include the PaymentMeans PayerFinancialAccount","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:PaymentMeans/cac:PayerFinancialAccount)"},
{"id":"UBL-CR-424","texto":"A UBL invoice should not include the PaymentMeans PayeeFinancialAccount AliasName","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:PaymentMeans/cac:PayeeFinancialAccount/cbc:AliasName)"},
{"id":"UBL-CR-425","texto":"A UBL invoice should not include the PaymentMeans PayeeFinancialAccount AccountTypeCode","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:PaymentMeans/cac:PayeeFinancialAccount/cbc:AccountTypeCode)"},
{"id":"UBL-CR-426","texto":"A UBL invoice should not include the PaymentMeans PayeeFinancialAccount AccountFormatCode","categoria":"formato","natureza":"RP","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:PaymentMeans/cac:PayeeFinancialAccount/cbc:AccountFormatCode)"},
{"id":"UBL-CR-427","texto":"A UBL invoice should not include the PaymentMeans PayeeFinancialAccount CurrencyCode","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:PaymentMeans/cac:PayeeFinancialAccount/cbc:CurrencyCode)"},
{"id":"UBL-CR-428","texto":"A UBL invoice should not include the PaymentMeans PayeeFinancialAccount PaymentNote","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:PaymentMeans/cac:PayeeFinancialAccount/cbc:PaymentNote)"},
{"id":"UBL-CR-429","texto":"A UBL invoice should not include the PaymentMeans PayeeFinancialAccount FinancialInstitutionBranch Name","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:PaymentMeans/cac:PayeeFinancialAccount/cac:FinancialInstitutionBranch/cbc:Name)"},
{"id":"UBL-CR-430","texto":"A UBL invoice should not include the PaymentMeans PayeeFinancialAccount FinancialInstitutionBranch FinancialInstitution Name","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:PaymentMeans/cac:PayeeFinancialAccount/cac:FinancialInstitutionBranch/cac:FinancialInstitution/cbc:Name)"},
{"id":"UBL-CR-431","texto":"A UBL invoice should not include the PaymentMeans PayeeFinancialAccount FinancialInstitutionBranch FinancialInstitution Address","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:PaymentMeans/cac:PayeeFinancialAccount/cac:FinancialInstitutionBranch/cac:FinancialInstitution/cac:Address)"},
{"id":"UBL-CR-432","texto":"A UBL invoice should not include the PaymentMeans PayeeFinancialAccount FinancialInstitutionBranch Address","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:PaymentMeans/cac:PayeeFinancialAccount/cac:FinancialInstitutionBranch/cac:Address)"},
{"id":"UBL-CR-433","texto":"A UBL invoice should not include the PaymentMeans PayeeFinancialAccount Country","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:PaymentMeans/cac:PayeeFinancialAccount/cac:Country)"},
{"id":"UBL-CR-434","texto":"A UBL invoice should not include the PaymentMeans CreditAccount","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:PaymentMeans/cac:CreditAccount)"},
{"id":"UBL-CR-435","texto":"A UBL invoice should not include the PaymentMeans PaymentMandate MandateTypeCode","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:PaymentMeans/cac:PaymentMandate/cbc:MandateTypeCode)"},
{"id":"UBL-CR-436","texto":"A UBL invoice should not include the PaymentMeans PaymentMandate MaximumPaymentInstructionsNumeric","categoria":"gama","natureza":"RP","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:PaymentMeans/cac:PaymentMandate/cbc:MaximumPaymentInstructionsNumeric)"},
{"id":"UBL-CR-437","texto":"A UBL invoice should not include the PaymentMeans PaymentMandate MaximumPaidAmount","categoria":"gama","natureza":"RP","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:PaymentMeans/cac:PaymentMandate/cbc:MaximumPaidAmount)"},
{"id":"UBL-CR-438","texto":"A UBL invoice should not include the PaymentMeans PaymentMandate SignatureID","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:PaymentMeans/cac:PaymentMandate/cbc:SignatureID)"},
{"id":"UBL-CR-439","texto":"A UBL invoice should not include the PaymentMeans PaymentMandate PayerParty","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:PaymentMeans/cac:PaymentMandate/cac:PayerParty)"},
{"id":"UBL-CR-440","texto":"A UBL invoice should not include the PaymentMeans PaymentMandate PayerFinancialAccount Name","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:PaymentMeans/cac:PaymentMandate/cac:PayerFinancialAccount/cbc:Name)"},
{"id":"UBL-CR-441","texto":"A UBL invoice should not include the PaymentMeans PaymentMandate PayerFinancialAccount AliasName","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:PaymentMeans/cac:PaymentMandate/cac:PayerFinancialAccount/cbc:AliasName)"},
{"id":"UBL-CR-442","texto":"A UBL invoice should not include the PaymentMeans PaymentMandate PayerFinancialAccount AccountTypeCode","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:PaymentMeans/cac:PaymentMandate/cac:PayerFinancialAccount/cbc:AccountTypeCode)"},
{"id":"UBL-CR-443","texto":"A UBL invoice should not include the PaymentMeans PaymentMandate PayerFinancialAccount AccountFormatCode","categoria":"formato","natureza":"RP","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:PaymentMeans/cac:PaymentMandate/cac:PayerFinancialAccount/cbc:AccountFormatCode)"},
{"id":"UBL-CR-444","texto":"A UBL invoice should not include the PaymentMeans PaymentMandate PayerFinancialAccount CurrencyCode","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:PaymentMeans/cac:PaymentMandate/cac:PayerFinancialAccount/cbc:CurrencyCode)"},
{"id":"UBL-CR-445","texto":"A UBL invoice should not include the PaymentMeans PaymentMandate PayerFinancialAccount PaymentNote","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:PaymentMeans/cac:PaymentMandate/cac:PayerFinancialAccount/cbc:PaymentNote)"},
{"id":"UBL-CR-446","texto":"A UBL invoice should not include the PaymentMeans PaymentMandate PayerFinancialAccount FinancialInstitutionBranch","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:PaymentMeans/cac:PaymentMandate/cac:PayerFinancialAccount/cac:FinancialInstitutionBranch)"},
{"id":"UBL-CR-447","texto":"A UBL invoice should not include the PaymentMeans PaymentMandate PayerFinancialAccount Country","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:PaymentMeans/cac:PaymentMandate/cac:PayerFinancialAccount/cac:Country)"},
{"id":"UBL-CR-448","texto":"A UBL invoice should not include the PaymentMeans PaymentMandate ValidityPeriod","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:PaymentMeans/cac:PaymentMandate/cac:ValidityPeriod)"},
{"id":"UBL-CR-449","texto":"A UBL invoice should not include the PaymentMeans PaymentMandate PaymentReversalPeriod","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:PaymentMeans/cac:PaymentMandate/cac:PaymentReversalPeriod)"},
{"id":"UBL-CR-450","texto":"A UBL invoice should not include the PaymentMeans PaymentMandate Clause","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:PaymentMeans/cac:PaymentMandate/cac:Clause)"},
{"id":"UBL-CR-451","texto":"A UBL invoice should not include the PaymentMeans TradeFinancing","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:PaymentMeans/cac:TradeFinancing)"},
{"id":"UBL-CR-452","texto":"A UBL invoice should not include the PaymentTerms ID","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:PaymentTerms/cbc:ID)"},
{"id":"UBL-CR-453","texto":"A UBL invoice should not include the PaymentTerms PaymentMeansID","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:PaymentTerms/cbc:PaymentMeansID)"},
{"id":"UBL-CR-454","texto":"A UBL invoice should not include the PaymentTerms PrepaidPaymentReferenceID","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:PaymentTerms/cbc:PrepaidPaymentReferenceID)"},
{"id":"UBL-CR-455","texto":"A UBL invoice should not include the PaymentTerms ReferenceEventCode","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:PaymentTerms/cbc:ReferenceEventCode)"},
{"id":"UBL-CR-456","texto":"A UBL invoice should not include the PaymentTerms SettlementDiscountPercent","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:PaymentTerms/cbc:SettlementDiscountPercent)"},
{"id":"UBL-CR-457","texto":"A UBL invoice should not include the PaymentTerms PenaltySurchargePercent","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:PaymentTerms/cbc:PenaltySurchargePercent)"},
{"id":"UBL-CR-458","texto":"A UBL invoice should not include the PaymentTerms PaymentPercent","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:PaymentTerms/cbc:PaymentPercent)"},
{"id":"UBL-CR-459","texto":"A UBL invoice should not include the PaymentTerms Amount","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:PaymentTerms/cbc:Amount)"},
{"id":"UBL-CR-460","texto":"A UBL invoice should not include the PaymentTerms SettlementDiscountAmount","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:PaymentTerms/cbc:SettlementDiscountAmount)"},
{"id":"UBL-CR-461","texto":"A UBL invoice should not include the PaymentTerms PenaltyAmount","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:PaymentTerms/cbc:PenaltyAmount)"},
{"id":"UBL-CR-462","texto":"A UBL invoice should not include the PaymentTerms PaymentTermsDetailsURI","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:PaymentTerms/cbc:PaymentTermsDetailsURI)"},
{"id":"UBL-CR-463","texto":"A UBL invoice should not include the PaymentTerms PaymentDueDate","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:PaymentTerms/cbc:PaymentDueDate)"},
{"id":"UBL-CR-464","texto":"A UBL invoice should not include the PaymentTerms InstallmentDueDate","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:PaymentTerms/cbc:InstallmentDueDate)"},
{"id":"UBL-CR-465","texto":"A UBL invoice should not include the PaymentTerms InvoicingPartyReference","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:PaymentTerms/cbc:InvoicingPartyReference)"},
{"id":"UBL-CR-466","texto":"A UBL invoice should not include the PaymentTerms SettlementPeriod","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:PaymentTerms/cac:SettlementPeriod)"},
{"id":"UBL-CR-467","texto":"A UBL invoice should not include the PaymentTerms PenaltyPeriod","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:PaymentTerms/cac:PenaltyPeriod)"},
{"id":"UBL-CR-468","texto":"A UBL invoice should not include the PaymentTerms ExchangeRate","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:PaymentTerms/cac:ExchangeRate)"},
{"id":"UBL-CR-469","texto":"A UBL invoice should not include the PaymentTerms ValidityPeriod","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:PaymentTerms/cac:ValidityPeriod)"},
{"id":"UBL-CR-470","texto":"A UBL invoice should not include the PrepaidPayment","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:PrepaidPayment)"},
{"id":"UBL-CR-471","texto":"A UBL invoice should not include the AllowanceCharge ID","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AllowanceCharge/cbc:ID)"},
{"id":"UBL-CR-472","texto":"A UBL invoice should not include the AllowanceCharge PrepaidIndicator","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AllowanceCharge/cbc:PrepaidIndicator)"},
{"id":"UBL-CR-473","texto":"A UBL invoice should not include the AllowanceCharge SequenceNumeric","categoria":"valores","natureza":"RP","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AllowanceCharge/cbc:SequenceNumeric)"},
{"id":"UBL-CR-474","texto":"A UBL invoice should not include the AllowanceCharge AccountingCostCode","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AllowanceCharge/cbc:AccountingCostCode)"},
{"id":"UBL-CR-475","texto":"A UBL invoice should not include the AllowanceCharge AccountingCost","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AllowanceCharge/cbc:AccountingCost)"},
{"id":"UBL-CR-476","texto":"A UBL invoice should not include the AllowanceCharge PerUnitAmount","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AllowanceCharge/cbc:PerUnitAmount)"},
{"id":"UBL-CR-477","texto":"A UBL invoice should not include the AllowanceCharge TaxCategory Name","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AllowanceCharge/cac:TaxCategory/cbc:Name)"},
{"id":"UBL-CR-478","texto":"A UBL invoice should not include the AllowanceCharge TaxCategory BaseUnitMeasure","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AllowanceCharge/cac:TaxCategory/cbc:BaseUnitMeasure)"},
{"id":"UBL-CR-479","texto":"A UBL invoice should not include the AllowanceCharge TaxCategory PerUnitAmount","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AllowanceCharge/cac:TaxCategory/cbc:PerUnitAmount)"},
{"id":"UBL-CR-480","texto":"A UBL invoice should not include the AllowanceCharge TaxCategory TaxExemptionReasonCode","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AllowanceCharge/cac:TaxCategory/cbc:TaxExemptionReasonCode)"},
{"id":"UBL-CR-481","texto":"A UBL invoice should not include the AllowanceCharge TaxCategory TaxExemptionReason","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AllowanceCharge/cac:TaxCategory/cbc:TaxExemptionReason)"},
{"id":"UBL-CR-482","texto":"A UBL invoice should not include the AllowanceCharge TaxCategory TierRange","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AllowanceCharge/cac:TaxCategory/cbc:TierRange)"},
{"id":"UBL-CR-483","texto":"A UBL invoice should not include the AllowanceCharge TaxCategory TierRatePercent","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AllowanceCharge/cac:TaxCategory/cbc:TierRatePercent)"},
{"id":"UBL-CR-484","texto":"A UBL invoice should not include the AllowanceCharge TaxCategory TaxScheme Name","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AllowanceCharge/cac:TaxCategory/cac:TaxScheme/cbc:Name)"},
{"id":"UBL-CR-485","texto":"A UBL invoice should not include the AllowanceCharge TaxCategory TaxScheme TaxTypeCode","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AllowanceCharge/cac:TaxCategory/cac:TaxScheme/cbc:TaxTypeCode)"},
{"id":"UBL-CR-486","texto":"A UBL invoice should not include the AllowanceCharge TaxCategory TaxScheme CurrencyCode","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AllowanceCharge/cac:TaxCategory/cac:TaxScheme/cbc:CurrencyCode)"},
{"id":"UBL-CR-487","texto":"A UBL invoice should not include the AllowanceCharge TaxCategory TaxScheme JurisdiccionRegionAddress","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AllowanceCharge/cac:TaxCategory/cac:TaxScheme/cac:JurisdiccionRegionAddress)"},
{"id":"UBL-CR-488","texto":"A UBL invoice should not include the AllowanceCharge TaxTotal","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AllowanceCharge/cac:TaxTotal)"},
{"id":"UBL-CR-489","texto":"A UBL invoice should not include the AllowanceCharge PaymentMeans","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AllowanceCharge/cac:PaymentMeans)"},
{"id":"UBL-CR-490","texto":"A UBL invoice should not include the TaxExchangeRate","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:TaxExchangeRate)"},
{"id":"UBL-CR-491","texto":"A UBL invoice should not include the PricingExchangeRate","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:PricingExchangeRate)"},
{"id":"UBL-CR-492","texto":"A UBL invoice should not include the PaymentExchangeRate","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:PaymentExchangeRate)"},
{"id":"UBL-CR-493","texto":"A UBL invoice should not include the PaymentAlternativeExchangeRate","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:PaymentAlternativeExchangeRate)"},
{"id":"UBL-CR-494","texto":"A UBL invoice should not include the TaxTotal RoundingAmount","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:TaxTotal/cbc:RoundingAmount)"},
{"id":"UBL-CR-495","texto":"A UBL invoice should not include the TaxTotal TaxEvidenceIndicator","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:TaxTotal/cbc:TaxEvidenceIndicator)"},
{"id":"UBL-CR-496","texto":"A UBL invoice should not include the TaxTotal TaxIncludedIndicator","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:TaxTotal/cbc:TaxIncludedIndicator)"},
{"id":"UBL-CR-497","texto":"A UBL invoice should not include the TaxTotal TaxSubtotal CalulationSequenceNumeric","categoria":"valores","natureza":"RP","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:TaxTotal/cac:TaxSubtotal/cbc:CalculationSequenceNumeric)"},
{"id":"UBL-CR-498","texto":"A UBL invoice should not include the TaxTotal TaxSubtotal TransactionCurrencyTaxAmount","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:TaxTotal/cac:TaxSubtotal/cbc:TransactionCurrencyTaxAmount)"},
{"id":"UBL-CR-499","texto":"A UBL invoice should not include the TaxTotal TaxSubtotal Percent","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:TaxTotal/cac:TaxSubtotal/cbc:Percent)"},
{"id":"UBL-CR-500","texto":"A UBL invoice should not include the TaxTotal TaxSubtotal BaseUnitMeasure","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:TaxTotal/cac:TaxSubtotal/cbc:BaseUnitMeasure)"},
{"id":"UBL-CR-501","texto":"A UBL invoice should not include the TaxTotal TaxSubtotal PerUnitAmount","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:TaxTotal/cac:TaxSubtotal/cbc:PerUnitAmount)"},
{"id":"UBL-CR-502","texto":"A UBL invoice should not include the TaxTotal TaxSubtotal TierRange","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:TaxTotal/cac:TaxSubtotal/cbc:TierRange)"},
{"id":"UBL-CR-503","texto":"A UBL invoice should not include the TaxTotal TaxSubtotal TierRatePercent","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:TaxTotal/cac:TaxSubtotal/cbc:TierRatePercent)"},
{"id":"UBL-CR-504","texto":"A UBL invoice should not include the TaxTotal TaxSubtotal TaxCategory Name","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:TaxTotal/cac:TaxSubtotal/cac:TaxCategory/cbc:Name)"},
{"id":"UBL-CR-505","texto":"A UBL invoice should not include the TaxTotal TaxSubtotal TaxCategory BaseUnitMeasure","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:TaxTotal/cac:TaxSubtotal/cac:TaxCategory/cbc:BaseUnitMeasure)"},
{"id":"UBL-CR-506","texto":"A UBL invoice should not include the TaxTotal TaxSubtotal TaxCategory PerUnitAmount","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:TaxTotal/cac:TaxSubtotal/cac:TaxCategory/cbc:PerUnitAmount)"},
{"id":"UBL-CR-507","texto":"A UBL invoice should not include the TaxTotal TaxSubtotal TaxCategory TierRange","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:TaxTotal/cac:TaxSubtotal/cac:TaxCategory/cbc:TierRange)"},
{"id":"UBL-CR-508","texto":"A UBL invoice should not include the TaxTotal TaxSubtotal TaxCategory TierRatePercent","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:TaxTotal/cac:TaxSubtotal/cac:TaxCategory/cbc:TierRatePercent)"},
{"id":"UBL-CR-509","texto":"A UBL invoice should not include the TaxTotal TaxSubtotal TaxCategory TaxScheme Name","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:TaxTotal/cac:TaxSubtotal/cac:TaxCategory/cac:TaxScheme/cbc:Name)"},
{"id":"UBL-CR-510","texto":"A UBL invoice should not include the TaxTotal TaxSubtotal TaxCategory TaxScheme TaxTypeCode","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:TaxTotal/cac:TaxSubtotal/cac:TaxCategory/cac:TaxScheme/cbc:TaxTypeCode)"},
{"id":"UBL-CR-511","texto":"A UBL invoice should not include the TaxTotal TaxSubtotal TaxCategory TaxScheme CurrencyCode","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:TaxTotal/cac:TaxSubtotal/cac:TaxCategory/cac:TaxScheme/cbc:CurrencyCode)"},
{"id":"UBL-CR-512","texto":"A UBL invoice should not include the TaxTotal TaxSubtotal TaxCategory TaxScheme JurisdiccionRegionAddress","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:TaxTotal/cac:TaxSubtotal/cac:TaxCategory/cac:TaxScheme/cac:JurisdiccionRegionAddress)"},
{"id":"UBL-CR-513","texto":"A UBL invoice should not include the WithholdingTaxTotal","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:WithholdingTaxTotal)"},
{"id":"UBL-CR-514","texto":"A UBL invoice should not include the LegalMonetaryTotal PayableAlternativeAmount","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:LegalMonetaryTotal/cbc:PayableAlternativeAmount)"},
{"id":"UBL-CR-515","texto":"A UBL invoice should not include the InvoiceLine UUID","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cbc:UUID)"},
{"id":"UBL-CR-516","texto":"A UBL invoice should not include the InvoiceLine TaxPointDate","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cbc:TaxPointDate)"},
{"id":"UBL-CR-517","texto":"A UBL invoice should not include the InvoiceLine AccountingCostCode","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cbc:AccountingCostCode)"},
{"id":"UBL-CR-518","texto":"A UBL invoice should not include the InvoiceLine PaymentPurposeCode","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cbc:PaymentPurposeCode)"},
{"id":"UBL-CR-519","texto":"A UBL invoice should not include the InvoiceLine FreeOfChargeIndicator","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cbc:FreeOfChargeIndicator)"},
{"id":"UBL-CR-520","texto":"A UBL invoice should not include the InvoiceLine InvoicePeriod StartTime","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:InvoicePeriod/cbc:StartTime)"},
{"id":"UBL-CR-521","texto":"A UBL invoice should not include the InvoiceLine InvoicePeriod EndTime","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:InvoicePeriod/cbc:EndTime)"},
{"id":"UBL-CR-522","texto":"A UBL invoice should not include the InvoiceLine InvoicePeriod DurationMeasure","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:InvoicePeriod/cbc:DurationMeasure)"},
{"id":"UBL-CR-523","texto":"A UBL invoice should not include the InvoiceLine InvoicePeriod DescriptionCode","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:InvoicePeriod/cbc:DescriptionCode)"},
{"id":"UBL-CR-524","texto":"A UBL invoice should not include the InvoiceLine InvoicePeriod Description","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:InvoicePeriod/cbc:Description)"},
{"id":"UBL-CR-525","texto":"A UBL invoice should not include the InvoiceLine OrderLineReference SalesOrderLineID","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:OrderLineReference/cbc:SalesOrderLineID)"},
{"id":"UBL-CR-526","texto":"A UBL invoice should not include the InvoiceLine OrderLineReference UUID","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:OrderLineReference/cbc:UUID)"},
{"id":"UBL-CR-527","texto":"A UBL invoice should not include the InvoiceLine OrderLineReference LineStatusCode","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:OrderLineReference/cbc:LineStatusCode)"},
{"id":"UBL-CR-528","texto":"A UBL invoice should not include the InvoiceLine OrderLineReference OrderReference","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:OrderLineReference/cbc:OrderReference)"},
{"id":"UBL-CR-529","texto":"A UBL invoice should not include the InvoiceLine DespatchLineReference","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:DespatchLineReference)"},
{"id":"UBL-CR-530","texto":"A UBL invoice should not include the InvoiceLine ReceiptLineReference","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:ReceiptLineReference)"},
{"id":"UBL-CR-531","texto":"A UBL invoice should not include the InvoiceLine BillingReference","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:BillingReference)"},
{"id":"UBL-CR-532","texto":"A UBL invoice should not include the InvoiceLine DocumentReference CopyIndicator","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:DocumentReference/cbc:CopyIndicator)"},
{"id":"UBL-CR-533","texto":"A UBL invoice should not include the InvoiceLine DocumentReference UUID","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:DocumentReference/cbc:UUID)"},
{"id":"UBL-CR-534","texto":"A UBL invoice should not include the InvoiceLine DocumentReference IssueDate","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:DocumentReference/cbc:IssueDate)"},
{"id":"UBL-CR-535","texto":"A UBL invoice should not include the InvoiceLine DocumentReference IssueTime","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:DocumentReference/cbc:IssueTime)"},
{"id":"UBL-CR-537","texto":"A UBL invoice should not include the InvoiceLine DocumentReference DocumentType","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:DocumentReference/cbc:DocumentType)"},
{"id":"UBL-CR-538","texto":"A UBL invoice should not include the InvoiceLine DocumentReference Xpath","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:DocumentReference/cbc:Xpath)"},
{"id":"UBL-CR-539","texto":"A UBL invoice should not include the InvoiceLine DocumentReference LanguageID","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:DocumentReference/cbc:LanguageID)"},
{"id":"UBL-CR-540","texto":"A UBL invoice should not include the InvoiceLine DocumentReference LocaleCode","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:DocumentReference/cbc:LocaleCode)"},
{"id":"UBL-CR-541","texto":"A UBL invoice should not include the InvoiceLine DocumentReference VersionID","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:DocumentReference/cbc:VersionID)"},
{"id":"UBL-CR-542","texto":"A UBL invoice should not include the InvoiceLine DocumentReference DocumentStatusCode","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:DocumentReference/cbc:DocumentStatusCode)"},
{"id":"UBL-CR-543","texto":"A UBL invoice should not include the InvoiceLine DocumentReference DocumentDescription","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:DocumentReference/cbc:DocumentDescription)"},
{"id":"UBL-CR-544","texto":"A UBL invoice should not include the InvoiceLine DocumentReference Attachment","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:DocumentReference/cac:Attachment)"},
{"id":"UBL-CR-545","texto":"A UBL invoice should not include the InvoiceLine DocumentReference ValidityPeriod","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:DocumentReference/cac:ValidityPeriod)"},
{"id":"UBL-CR-546","texto":"A UBL invoice should not include the InvoiceLine DocumentReference IssuerParty","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:DocumentReference/cac:IssuerParty)"},
{"id":"UBL-CR-547","texto":"A UBL invoice should not include the InvoiceLine DocumentReference ResultOfVerification","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:DocumentReference/cac:ResultOfVerification)"},
{"id":"UBL-CR-548","texto":"A UBL invoice should not include the InvoiceLine PricingReference","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:PricingReference)"},
{"id":"UBL-CR-549","texto":"A UBL invoice should not include the InvoiceLine OriginatorParty","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:OriginatorParty)"},
{"id":"UBL-CR-550","texto":"A UBL invoice should not include the InvoiceLine Delivery","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:Delivery)"},
{"id":"UBL-CR-551","texto":"A UBL invoice should not include the InvoiceLine PaymentTerms","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:PaymentTerms)"},
{"id":"UBL-CR-552","texto":"A UBL invoice should not include the InvoiceLine AllowanceCharge ID","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:AllowanceCharge/cbc:ID)"},
{"id":"UBL-CR-553","texto":"A UBL invoice should not include the InvoiceLine AllowanceCharge PrepaidIndicator","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:AllowanceCharge/cbc:PrepaidIndicator)"},
{"id":"UBL-CR-554","texto":"A UBL invoice should not include the InvoiceLine AllowanceCharge SequenceNumeric","categoria":"valores","natureza":"RP","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:AllowanceCharge/cbc:SequenceNumeric)"},
{"id":"UBL-CR-555","texto":"A UBL invoice should not include the InvoiceLine AllowanceCharge AccountingCostCode","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:AllowanceCharge/cbc:AccountingCostCode)"},
{"id":"UBL-CR-556","texto":"A UBL invoice should not include the InvoiceLine AllowanceCharge AccountingCost","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:AllowanceCharge/cbc:AccountingCost)"},
{"id":"UBL-CR-557","texto":"A UBL invoice should not include the InvoiceLine AllowanceCharge PerUnitAmount","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:AllowanceCharge/cbc:PerUnitAmount)"},
{"id":"UBL-CR-558","texto":"A UBL invoice should not include the InvoiceLine AllowanceCharge TaxCategory","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:AllowanceCharge/cac:TaxCategory)"},
{"id":"UBL-CR-559","texto":"A UBL invoice should not include the InvoiceLine AllowanceCharge TaxTotal","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:AllowanceCharge/cac:TaxTotal)"},
{"id":"UBL-CR-560","texto":"A UBL invoice should not include the InvoiceLine AllowanceCharge PaymentMeans","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:AllowanceCharge/cac:PaymentMeans)"},
{"id":"UBL-CR-561","texto":"A UBL invoice should not include the InvoiceLine TaxTotal","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:TaxTotal)"},
{"id":"UBL-CR-562","texto":"A UBL invoice should not include the InvoiceLine WithholdingTaxTotal","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:WithholdingTaxTotal)"},
{"id":"UBL-CR-563","texto":"A UBL invoice should not include the InvoiceLine Item PackQuantity","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:Item/cbc:PackQuantity)"},
{"id":"UBL-CR-564","texto":"A UBL invoice should not include the InvoiceLine Item PackSizeNumeric","categoria":"valores","natureza":"RP","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:Item/cbc:PackSizeNumeric)"},
{"id":"UBL-CR-565","texto":"A UBL invoice should not include the InvoiceLine Item CatalogueIndicator","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:Item/cbc:CatalogueIndicator)"},
{"id":"UBL-CR-566","texto":"A UBL invoice should not include the InvoiceLine Item HazardousRiskIndicator","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:Item/cbc:HazardousRiskIndicator)"},
{"id":"UBL-CR-567","texto":"A UBL invoice should not include the InvoiceLine Item AdditionalInformation","categoria":"formato","natureza":"RP","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:Item/cbc:AdditionalInformation)"},
{"id":"UBL-CR-568","texto":"A UBL invoice should not include the InvoiceLine Item Keyword","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:Item/cbc:Keyword)"},
{"id":"UBL-CR-569","texto":"A UBL invoice should not include the InvoiceLine Item BrandName","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:Item/cbc:BrandName)"},
{"id":"UBL-CR-570","texto":"A UBL invoice should not include the InvoiceLine Item ModelName","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:Item/cbc:ModelName)"},
{"id":"UBL-CR-571","texto":"A UBL invoice should not include the InvoiceLine Item BuyersItemIdentification ExtendedID","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:Item/cac:BuyersItemIdentification/cbc:ExtendedID)"},
{"id":"UBL-CR-572","texto":"A UBL invoice should not include the InvoiceLine Item BuyersItemIdentification BareCodeSymbologyID","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:Item/cac:BuyersItemIdentification/cbc:BareCodeSymbologyID)"},
{"id":"UBL-CR-573","texto":"A UBL invoice should not include the InvoiceLine Item BuyersItemIdentification PhysicalAttribute","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:Item/cac:BuyersItemIdentification/cac:PhysicalAttribute)"},
{"id":"UBL-CR-574","texto":"A UBL invoice should not include the InvoiceLine Item BuyersItemIdentification MeasurementDimension","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:Item/cac:BuyersItemIdentification/cac:MeasurementDimension)"},
{"id":"UBL-CR-575","texto":"A UBL invoice should not include the InvoiceLine Item BuyersItemIdentification IssuerParty","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:Item/cac:BuyersItemIdentification/cac:IssuerParty)"},
{"id":"UBL-CR-576","texto":"A UBL invoice should not include the InvoiceLine Item SellersItemIdentification ExtendedID","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:Item/cac:SellersItemIdentification/cbc:ExtendedID)"},
{"id":"UBL-CR-577","texto":"A UBL invoice should not include the InvoiceLine Item SellersItemIdentification BareCodeSymbologyID","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:Item/cac:SellersItemIdentification/cbc:BareCodeSymbologyID)"},
{"id":"UBL-CR-578","texto":"A UBL invoice should not include the InvoiceLine Item SellersItemIdentification PhysicalAttribute","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:Item/cac:SellersItemIdentification/cac:PhysicalAttribute)"},
{"id":"UBL-CR-579","texto":"A UBL invoice should not include the InvoiceLine Item SellersItemIdentification MeasurementDimension","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:Item/cac:SellersItemIdentification/cac:MeasurementDimension)"},
{"id":"UBL-CR-580","texto":"A UBL invoice should not include the InvoiceLine Item SellersItemIdentification IssuerParty","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:Item/cac:SellersItemIdentification/cac:IssuerParty)"},
{"id":"UBL-CR-581","texto":"A UBL invoice should not include the InvoiceLine Item ManufacturersItemIdentification","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:Item/cac:ManufacturersItemIdentification)"},
{"id":"UBL-CR-582","texto":"A UBL invoice should not include the InvoiceLine Item StandardItemIdentification ExtendedID","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:Item/cac:StandardItemIdentification/cbc:ExtendedID)"},
{"id":"UBL-CR-583","texto":"A UBL invoice should not include the InvoiceLine Item StandardItemIdentification BareCodeSymbologyID","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:Item/cac:StandardItemIdentification/cbc:BareCodeSymbologyID)"},
{"id":"UBL-CR-584","texto":"A UBL invoice should not include the InvoiceLine Item StandardItemIdentification PhysicalAttribute","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:Item/cac:StandardItemIdentification/cac:PhysicalAttribute)"},
{"id":"UBL-CR-585","texto":"A UBL invoice should not include the InvoiceLine Item StandardItemIdentification MeasurementDimension","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:Item/cac:StandardItemIdentification/cac:MeasurementDimension)"},
{"id":"UBL-CR-586","texto":"A UBL invoice should not include the InvoiceLine Item StandardItemIdentification IssuerParty","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:Item/cac:StandardItemIdentification/cac:IssuerParty)"},
{"id":"UBL-CR-587","texto":"A UBL invoice should not include the InvoiceLine Item CatalogueItemIdentification","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:Item/cac:CatalogueItemIdentification)"},
{"id":"UBL-CR-588","texto":"A UBL invoice should not include the InvoiceLine Item AdditionalItemIdentification","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:Item/cac:AdditionalItemIdentification)"},
{"id":"UBL-CR-589","texto":"A UBL invoice should not include the InvoiceLine Item CatalogueDocumentReference","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:Item/cac:CatalogueDocumentReference)"},
{"id":"UBL-CR-590","texto":"A UBL invoice should not include the InvoiceLine Item ItemSpecificationDocumentReference","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:Item/cac:ItemSpecificationDocumentReference)"},
{"id":"UBL-CR-591","texto":"A UBL invoice should not include the InvoiceLine Item OriginCountry Name","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:Item/cac:OriginCountry/cbc:Name)"},
{"id":"UBL-CR-592","texto":"A UBL invoice should not include the InvoiceLine Item CommodityClassification NatureCode","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:Item/cac:CommodityClassification/cbc:NatureCode)"},
{"id":"UBL-CR-593","texto":"A UBL invoice should not include the InvoiceLine Item CommodityClassification CargoTypeCode","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:Item/cac:CommodityClassification/cbc:CargoTypeCode)"},
{"id":"UBL-CR-594","texto":"A UBL invoice should not include the InvoiceLine Item CommodityClassification CommodityCode","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:Item/cac:CommodityClassification/cbc:CommodityCode)"},
{"id":"UBL-CR-595","texto":"A UBL invoice should not include the InvoiceLine Item TransactionConditions","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:Item/cac:TransactionConditions)"},
{"id":"UBL-CR-596","texto":"A UBL invoice should not include the InvoiceLine Item HazardousItem","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:Item/cac:HazardousItem)"},
{"id":"UBL-CR-597","texto":"A UBL invoice should not include the InvoiceLine Item ClassifiedTaxCategory Name","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:Item/cac:ClassifiedTaxCategory/cbc:Name)"},
{"id":"UBL-CR-598","texto":"A UBL invoice should not include the InvoiceLine Item ClassifiedTaxCategory BaseUnitMeasure","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:Item/cac:ClassifiedTaxCategory/cbc:BaseUnitMeasure)"},
{"id":"UBL-CR-599","texto":"A UBL invoice should not include the InvoiceLine Item ClassifiedTaxCategory PerUnitAmount","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:Item/cac:ClassifiedTaxCategory/cbc:PerUnitAmount)"},
{"id":"UBL-CR-600","texto":"A UBL invoice should not include the InvoiceLine Item ClassifiedTaxCategory TaxExemptionReasonCode","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:Item/cac:ClassifiedTaxCategory/cbc:TaxExemptionReasonCode)"},
{"id":"UBL-CR-601","texto":"A UBL invoice should not include the InvoiceLine Item ClassifiedTaxCategory TaxExemptionReason","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:Item/cac:ClassifiedTaxCategory/cbc:TaxExemptionReason)"},
{"id":"UBL-CR-602","texto":"A UBL invoice should not include the InvoiceLine Item ClassifiedTaxCategory TierRange","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:Item/cac:ClassifiedTaxCategory/cbc:TierRange)"},
{"id":"UBL-CR-603","texto":"A UBL invoice should not include the InvoiceLine Item ClassifiedTaxCategory TierRatePercent","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:Item/cac:ClassifiedTaxCategory/cbc:TierRatePercent)"},
{"id":"UBL-CR-604","texto":"A UBL invoice should not include the InvoiceLine Item ClassifiedTaxCategory TaxScheme Name","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:Item/cac:ClassifiedTaxCategory/cac:TaxScheme/cbc:Name)"},
{"id":"UBL-CR-605","texto":"A UBL invoice should not include the InvoiceLine Item ClassifiedTaxCategory TaxScheme TaxTypeCode","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:Item/cac:ClassifiedTaxCategory/cac:TaxScheme/cbc:TaxTypeCode)"},
{"id":"UBL-CR-606","texto":"A UBL invoice should not include the InvoiceLine Item ClassifiedTaxCategory TaxScheme CurrencyCode","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:Item/cac:ClassifiedTaxCategory/cac:TaxScheme/cbc:CurrencyCode)"},
{"id":"UBL-CR-607","texto":"A UBL invoice should not include the InvoiceLine Item ClassifiedTaxCategory TaxScheme JurisdiccionRegionAddress","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:Item/cac:ClassifiedTaxCategory/cac:TaxScheme/cac:JurisdiccionRegionAddress)"},
{"id":"UBL-CR-608","texto":"A UBL invoice should not include the InvoiceLine Item AdditionalItemProperty ID","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:Item/cac:AdditionalItemProperty/cbc:ID)"},
{"id":"UBL-CR-609","texto":"A UBL invoice should not include the InvoiceLine Item AdditionalItemProperty NameCode","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:Item/cac:AdditionalItemProperty/cbc:NameCode)"},
{"id":"UBL-CR-610","texto":"A UBL invoice should not include the InvoiceLine Item AdditionalItemProperty TestMethod","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:Item/cac:AdditionalItemProperty/cbc:TestMethod)"},
{"id":"UBL-CR-611","texto":"A UBL invoice should not include the InvoiceLine Item AdditionalItemProperty ValueQuantity","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:Item/cac:AdditionalItemProperty/cbc:ValueQuantity)"},
{"id":"UBL-CR-612","texto":"A UBL invoice should not include the InvoiceLine Item AdditionalItemProperty ValueQualifier","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:Item/cac:AdditionalItemProperty/cbc:ValueQualifier)"},
{"id":"UBL-CR-613","texto":"A UBL invoice should not include the InvoiceLine Item AdditionalItemProperty ImportanceCode","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:Item/cac:AdditionalItemProperty/cbc:ImportanceCode)"},
{"id":"UBL-CR-614","texto":"A UBL invoice should not include the InvoiceLine Item AdditionalItemProperty ListValue","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:Item/cac:AdditionalItemProperty/cbc:ListValue)"},
{"id":"UBL-CR-615","texto":"A UBL invoice should not include the InvoiceLine Item AdditionalItemProperty UsabilityPeriod","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:Item/cac:AdditionalItemProperty/cac:UsabilityPeriod)"},
{"id":"UBL-CR-616","texto":"A UBL invoice should not include the InvoiceLine Item AdditionalItemProperty ItemPropertyGroup","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:Item/cac:AdditionalItemProperty/cac:ItemPropertyGroup)"},
{"id":"UBL-CR-617","texto":"A UBL invoice should not include the InvoiceLine Item AdditionalItemProperty RangeDimension","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:Item/cac:AdditionalItemProperty/cac:RangeDimension)"},
{"id":"UBL-CR-618","texto":"A UBL invoice should not include the InvoiceLine Item AdditionalItemProperty ItemPropertyRange","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:Item/cac:AdditionalItemProperty/cac:ItemPropertyRange)"},
{"id":"UBL-CR-619","texto":"A UBL invoice should not include the InvoiceLine Item ManufacturerParty","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:Item/cac:ManufacturerParty)"},
{"id":"UBL-CR-620","texto":"A UBL invoice should not include the InvoiceLine Item InformationContentProviderParty","categoria":"formato","natureza":"RP","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:Item/cac:InformationContentProviderParty)"},
{"id":"UBL-CR-621","texto":"A UBL invoice should not include the InvoiceLine Item OriginAddress","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:Item/cac:OriginAddress)"},
{"id":"UBL-CR-622","texto":"A UBL invoice should not include the InvoiceLine Item ItemInstance","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:Item/cac:ItemInstance)"},
{"id":"UBL-CR-623","texto":"A UBL invoice should not include the InvoiceLine Item Certificate","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:Item/cac:Certificate)"},
{"id":"UBL-CR-624","texto":"A UBL invoice should not include the InvoiceLine Item Dimension","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:Item/cac:Dimension)"},
{"id":"UBL-CR-625","texto":"A UBL invoice should not include the InvoiceLine Item Price PriceChangeReason","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:Item/cac:Price/cbc:PriceChangeReason)"},
{"id":"UBL-CR-626","texto":"A UBL invoice should not include the InvoiceLine Item Price PriceTypeCode","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:Item/cac:Price/cbc:PriceTypeCode)"},
{"id":"UBL-CR-627","texto":"A UBL invoice should not include the InvoiceLine Item Price PriceType","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:Item/cac:Price/cbc:PriceType)"},
{"id":"UBL-CR-628","texto":"A UBL invoice should not include the InvoiceLine Item Price OrderableUnitFactorRate","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:Item/cac:Price/cbc:OrderableUnitFactorRate)"},
{"id":"UBL-CR-629","texto":"A UBL invoice should not include the InvoiceLine Item Price ValidityPeriod","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:Item/cac:Price/cbc:ValidityPeriod)"},
{"id":"UBL-CR-630","texto":"A UBL invoice should not include the InvoiceLine Item Price PriceList","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:Item/cac:Price/cbc:PriceList)"},
{"id":"UBL-CR-631","texto":"A UBL invoice should not include the InvoiceLine Item Price OrderableUnitFactorRate","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:Item/cac:Price/cbc:OrderableUnitFactorRate)"},
{"id":"UBL-CR-632","texto":"A UBL invoice should not include the InvoiceLine Item Price AllowanceCharge ID","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:Item/cac:Price/cac:AllowanceCharge/cbc:ID)"},
{"id":"UBL-CR-633","texto":"A UBL invoice should not include the InvoiceLine Item Price AllowanceCharge AllowanceChargeReasonCode","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:Item/cac:Price/cac:AllowanceCharge/cbc:AllowanceChargeReasonCode)"},
{"id":"UBL-CR-634","texto":"A UBL invoice should not include the InvoiceLine Item Price AllowanceCharge AllowanceChargeReason","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:Item/cac:Price/cac:AllowanceCharge/cbc:AllowanceChargeReason)"},
{"id":"UBL-CR-635","texto":"A UBL invoice should not include the InvoiceLine Item Price AllowanceCharge MultiplierFactorNumeric","categoria":"calculo","natureza":"FN","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:Item/cac:Price/cac:AllowanceCharge/cbc:MultiplierFactorNumeric)"},
{"id":"UBL-CR-636","texto":"A UBL invoice should not include the InvoiceLine Item Price AllowanceCharge PrepaidIndicator","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:Item/cac:Price/cac:AllowanceCharge/cbc:PrepaidIndicator)"},
{"id":"UBL-CR-637","texto":"A UBL invoice should not include the InvoiceLine Item Price AllowanceCharge SequenceNumeric","categoria":"valores","natureza":"RP","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:Item/cac:Price/cac:AllowanceCharge/cbc:SequenceNumeric)"},
{"id":"UBL-CR-638","texto":"A UBL invoice should not include the InvoiceLine Item Price AllowanceCharge AccountingCostCode","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:Item/cac:Price/cac:AllowanceCharge/cbc:AccountingCostCode)"},
{"id":"UBL-CR-639","texto":"A UBL invoice should not include the InvoiceLine Item Price AllowanceCharge AccountingCost","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:Item/cac:Price/cac:AllowanceCharge/cbc:AccountingCost)"},
{"id":"UBL-CR-640","texto":"A UBL invoice should not include the InvoiceLine Item Price AllowanceCharge PerUnitAmount","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:Item/cac:Price/cac:AllowanceCharge/cbc:PerUnitAmount)"},
{"id":"UBL-CR-641","texto":"A UBL invoice should not include the InvoiceLine Item Price AllowanceCharge TaxCategory","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:Item/cac:Price/cac:AllowanceCharge/cac:TaxCategory)"},
{"id":"UBL-CR-642","texto":"A UBL invoice should not include the InvoiceLine Item Price AllowanceCharge TaxTotal","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:Item/cac:Price/cac:AllowanceCharge/cac:TaxTotal)"},
{"id":"UBL-CR-643","texto":"A UBL invoice should not include the InvoiceLine Item Price AllowanceCharge PaymentMeans","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:Item/cac:Price/cac:AllowanceCharge/cac:PaymentMeans)"},
{"id":"UBL-CR-644","texto":"A UBL invoice should not include the InvoiceLine Item Price PricingExchangeRate","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:Item/cac:Price/cac:PricingExchangeRate)"},
{"id":"UBL-CR-645","texto":"A UBL invoice should not include the InvoiceLine DeliveryTerms","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:DeliveryTerms)"},
{"id":"UBL-CR-646","texto":"A UBL invoice should not include the InvoiceLine SubInvoiceLine","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:SubInvoiceLine)"},
{"id":"UBL-CR-647","texto":"A UBL invoice should not include the InvoiceLine ItemPriceExtension","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:ItemPriceExtension)"},
{"id":"UBL-DT-08","texto":"Scheme name attribute should not be present","categoria":"outra","natureza":"?","gravidade":"aviso","contexto":"Invoice","expressao":"not(//@schemeName)"},
{"id":"UBL-DT-09","texto":"Scheme agency name attribute should not be present","categoria":"outra","natureza":"?","gravidade":"aviso","contexto":"Invoice","expressao":"not(//@schemeAgencyName)"},
{"id":"UBL-DT-10","texto":"Scheme data uri attribute should not be present","categoria":"outra","natureza":"?","gravidade":"aviso","contexto":"Invoice","expressao":"not(//@schemeDataURI)"},
{"id":"UBL-DT-11","texto":"Scheme uri attribute should not be present","categoria":"outra","natureza":"?","gravidade":"aviso","contexto":"Invoice","expressao":"not(//@schemeURI)"},
{"id":"UBL-DT-12","texto":"Format attribute should not be present","categoria":"formato","natureza":"RP","gravidade":"aviso","contexto":"Invoice","expressao":"not(//@format)"},
{"id":"UBL-DT-13","texto":"Unit code list identifier attribute should not be present","categoria":"valores","natureza":"RP","gravidade":"aviso","contexto":"Invoice","expressao":"not(//@unitCodeListIdentifier)"},
{"id":"UBL-DT-14","texto":"Unit code list agency identifier attribute should not be present","categoria":"valores","natureza":"RP","gravidade":"aviso","contexto":"Invoice","expressao":"not(//@unitCodeListAgencyIdentifier)"},
{"id":"UBL-DT-15","texto":"Unit code list agency name attribute should not be present","categoria":"valores","natureza":"RP","gravidade":"aviso","contexto":"Invoice","expressao":"not(//@unitCodeListAgencyName)"},
{"id":"UBL-DT-16","texto":"List agency name attribute should not be present","categoria":"outra","natureza":"?","gravidade":"aviso","contexto":"Invoice","expressao":"not(//@listAgencyName)"},
{"id":"UBL-DT-17","texto":"List name attribute should not be present","categoria":"outra","natureza":"?","gravidade":"aviso","contexto":"Invoice","expressao":"not(//@listName)"},
{"id":"UBL-DT-18","texto":"Name attribute should not be present","categoria":"cardinalidade","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"count(//@name) - count(//cbc:PaymentMeansCode/@name) <= 0"},
{"id":"UBL-DT-19","texto":"Language identifier attribute should not be present","categoria":"outra","natureza":"?","gravidade":"aviso","contexto":"Invoice","expressao":"not(//@languageID)"},
{"id":"UBL-DT-20","texto":"List uri attribute should not be present","categoria":"outra","natureza":"?","gravidade":"aviso","contexto":"Invoice","expressao":"not(//@listURI)"},
{"id":"UBL-DT-21","texto":"List scheme uri attribute should not be present","categoria":"outra","natureza":"?","gravidade":"aviso","contexto":"Invoice","expressao":"not(//@listSchemeURI)"},
{"id":"UBL-DT-22","texto":"Language local identifier attribute should not be present","categoria":"outra","natureza":"?","gravidade":"aviso","contexto":"Invoice","expressao":"not(//@languageLocaleID)"},
{"id":"UBL-DT-23","texto":"Uri attribute should not be present","categoria":"outra","natureza":"?","gravidade":"aviso","contexto":"Invoice","expressao":"not(//@uri)"},
{"id":"UBL-DT-24","texto":"Currency code list version id should not be present","categoria":"valores","natureza":"RP","gravidade":"aviso","contexto":"Invoice","expressao":"not(//@currencyCodeListVersionID)"},
{"id":"UBL-DT-25","texto":"CharacterSetCode attribute should not be present","categoria":"formato","natureza":"RP","gravidade":"aviso","contexto":"Invoice","expressao":"not(//@characterSetCode)"},
{"id":"UBL-DT-26","texto":"EncodingCode attribute should not be present","categoria":"outra","natureza":"?","gravidade":"aviso","contexto":"Invoice","expressao":"not(//@encodingCode)"},
{"id":"UBL-SR-01","texto":"Contract identifier shall occur maximum once.","categoria":"cardinalidade","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"(count(cac:ContractDocumentReference/cbc:ID) <= 1)"},
{"id":"UBL-SR-02","texto":"Receive advice identifier shall occur maximum once","categoria":"cardinalidade","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"(count(cac:ReceiptDocumentReference/cbc:ID) <= 1)"},
{"id":"UBL-SR-03","texto":"Despatch advice identifier shall occur maximum once","categoria":"cardinalidade","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"(count(cac:DespatchDocumentReference/cbc:ID) <= 1)"},
{"id":"UBL-SR-04","texto":"Invoice object identifier shall occur maximum once","categoria":"cardinalidade","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"(count(cac:AdditionalDocumentReference[cbc:DocumentTypeCode='130']/cbc:ID) <= 1)"},
{"id":"UBL-SR-05","texto":"Payment terms shall occur maximum once","categoria":"cardinalidade","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"(count(cac:PaymentTerms/cbc:Note) <= 1)"},
{"id":"UBL-SR-06","texto":"Preceding invoice reference shall occur maximum once","categoria":"cardinalidade","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"(count(cac:InvoiceDocumentReference) <= 1)"},
{"id":"UBL-SR-08","texto":"Invoice period shall occur maximum once","categoria":"cardinalidade","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"(count(cac:InvoicePeriod) <= 1)"},
{"id":"UBL-SR-09","texto":"Seller name shall occur maximum once","categoria":"cardinalidade","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"(count(cac:AccountingSupplierParty/cac:Party/cac:PartyLegalEntity/cbc:RegistrationName) <= 1)"},
{"id":"UBL-SR-10","texto":"Seller trader name shall occur maximum once","categoria":"cardinalidade","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"(count(cac:AccountingSupplierParty/cac:Party/cac:PartyName/cbc:Name) <= 1)"},
{"id":"UBL-SR-11","texto":"Seller legal registration identifier shall occur maximum once","categoria":"cardinalidade","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"(count(cac:AccountingSupplierParty/cac:Party/cac:PartyLegalEntity/cbc:CompanyID) <= 1)"},
{"id":"UBL-SR-12","texto":"Seller VAT identifier shall occur maximum once","categoria":"cardinalidade","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"(count(cac:AccountingSupplierParty/cac:Party/cac:PartyTaxScheme[cac:TaxScheme/cbc:ID='VAT']/cbc:CompanyID) <= 1)"},
{"id":"UBL-SR-13","texto":"Seller tax registration shall occur maximum once","categoria":"cardinalidade","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"(count(cac:AccountingSupplierParty/cac:Party/cac:PartyTaxScheme[cac:TaxScheme/cbc:ID!='VAT']/cbc:ID) <= 1)"},
{"id":"UBL-SR-14","texto":"Seller additional legal information shall occur maximum once","categoria":"formato","natureza":"RP","gravidade":"aviso","contexto":"Invoice","expressao":"(count(cac:AccountingSupplierParty/cac:Party/cac:PartyLegalEntity/cbc:CompanyLegalForm) <= 1)"},
{"id":"UBL-SR-15","texto":"Buyer name shall occur maximum once","categoria":"cardinalidade","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"(count(cac:AccountingCustomerParty/cac:Party/cac:PartyLegalEntity/cbc:RegistrationName) <= 1)"},
{"id":"UBL-SR-16","texto":"Buyer identifier shall occur maximum once","categoria":"cardinalidade","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"(count(cac:AccountingCustomerParty/cac:Party/cac:PartyIdentification/cbc:ID) <= 1)"},
{"id":"UBL-SR-17","texto":"Buyer legal registration identifier shall occur maximum once","categoria":"cardinalidade","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"(count(cac:AccountingCustomerParty/cac:Party/cac:PartyLegalEntity/cbc:CompanyID) <= 1)"},
{"id":"UBL-SR-18","texto":"Buyer VAT identifier shall occur maximum once","categoria":"cardinalidade","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"(count(cac:AccountingCustomerParty/cac:Party/cac:PartyTaxScheme/cbc:CompanyID) <= 1)"},
{"id":"UBL-SR-24","texto":"Deliver to information shall occur maximum once","categoria":"formato","natureza":"RP","gravidade":"aviso","contexto":"Invoice","expressao":"(count(cac:Delivery) <= 1)"},
{"id":"UBL-SR-29","texto":"Bank creditor reference shall occur maximum once","categoria":"cardinalidade","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"(count(cac:PayeeParty/cac:PartyIdentification/cbc:ID) <= 1)"},
{"id":"UBL-SR-39","texto":"Project reference shall occur maximum once.","categoria":"cardinalidade","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"(count(cac:ProjectReference/cbc:ID) <= 1)"},
{"id":"UBL-SR-40","texto":"Buyer trade name shall occur maximum once","categoria":"cardinalidade","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"(count(cac:AccountingCustomerParty/cac:Party/cac:PartyName/cbc:Name) <= 1)"},
{"id":"UBL-SR-34","texto":"Invoice line note shall occur maximum once","categoria":"cardinalidade","natureza":"RE","gravidade":"aviso","contexto":"Invoice_line","expressao":"(count(cbc:Note) <= 1)"},
{"id":"UBL-SR-35","texto":"Referenced purchase order line identifier shall occur maximum once","categoria":"cardinalidade","natureza":"RE","gravidade":"aviso","contexto":"Invoice_line","expressao":"(count(cac:OrderLineReference/cbc:LineID) <= 1)"},
{"id":"UBL-SR-36","texto":"Invoice line period shall occur maximum once","categoria":"cardinalidade","natureza":"RE","gravidade":"aviso","contexto":"Invoice_line","expressao":"(count(cac:InvoicePeriod) <= 1)"},
{"id":"UBL-SR-37","texto":"Item price discount shall occur maximum once","categoria":"cardinalidade","natureza":"RE","gravidade":"aviso","contexto":"Invoice_line","expressao":"(count(cac:Price/cac:AllowanceCharge/cbc:Amount) <= 1)"},
{"id":"UBL-SR-38","texto":"Invoiced item VAT exemption reason text shall occur maximum once","categoria":"cardinalidade","natureza":"RE","gravidade":"aviso","contexto":"Invoice_line","expressao":"(count(cac:Item/cac:ClassifiedTaxCategory/cbc:TaxExemptionReason) <= 1)"},
{"id":"UBL-SR-26","texto":"Payment reference shall occur maximum once","categoria":"cardinalidade","natureza":"RE","gravidade":"aviso","contexto":"Payment_instructions","expressao":"(count(cbc:PaymentID) <= 1)"},
{"id":"UBL-SR-27","texto":"Payment means text shall occur maximum once","categoria":"cardinalidade","natureza":"RE","gravidade":"aviso","contexto":"Payment_instructions","expressao":"(count(cbc:InstructionNote) <= 1)"},
{"id":"UBL-SR-28","texto":"Mandate reference identifier shall occur maximum once","categoria":"cardinalidade","natureza":"RE","gravidade":"aviso","contexto":"Payment_instructions","expressao":"(count(cac:PaymentMandate/cbc:ID) <= 1)"},
{"id":"UBL-SR-07","texto":"If there is a preceding invoice reference, the preceding invoice number shall be present","categoria":"condicional","natureza":"RIR","gravidade":"aviso","contexto":"Preceding_Invoice","expressao":"(cac:InvoiceDocumentReference/cbc:ID)"},
{"id":"UBL-SR-22","texto":"Seller tax representative name shall occur maximum once, if the Seller has a tax representative","categoria":"condicional","natureza":"RIR","gravidade":"aviso","contexto":"Tax_Representative","expressao":"(count(cac:Party/cac:PartyName/cbc:Name) <= 1)"},
{"id":"UBL-SR-23","texto":"Seller tax representative VAT identifier shall occur maximum once, if the Seller has a tax representative","categoria":"condicional","natureza":"RIR","gravidade":"aviso","contexto":"Tax_Representative","expressao":"(count(cac:Party/cac:PartyTaxScheme/cbc:CompanyID) <= 1)"},
{"id":"UBL-SR-32","texto":"VAT exemption reason text shall occur maximum once","categoria":"cardinalidade","natureza":"RE","gravidade":"aviso","contexto":"Tax_subtotal","expressao":"(count(cac:TaxCategory/cbc:TaxExemptionReason) <= 1)"},
{"id":"DT-CIUS-PT-001","texto":"The BT-1 does not meet the defined format: alphanumeric with size between 1 and 50.","categoria":"formato","natureza":"RP","gravidade":"erro","contexto":"//ubl:Invoice/cbc:ID | //cn:CreditNote/cbc:ID","elementos":["BT-1"],"expressao":"matches(.,'^(.{1,50})$')"},
{"id":"DT-CIUS-PT-002","texto":"The BT-2 does not meet the defined format: YYYY-MM-DD.","categoria":"formato","natureza":"RP","gravidade":"erro","contexto":"//ubl:Invoice/cbc:IssueDate | //cn:CreditNote/cbc:IssueDate","elementos":["BT-2"],"expressao":"matches(.,'^((\\d{4})-(\\d{2})-(\\d{2}))$')"},
{"id":"DT-CIUS-PT-003_i","texto":"The BT-3 only allows the following values: 380, 383, 386, 389, FT, FS, FR, ND, RP, RE, CS, LD, RA.","categoria":"valores","natureza":"RP","gravidade":"erro","contexto":"//ubl:Invoice/cbc:InvoiceTypeCode","elementos":["BT-3"],"expressao":"(matches(.,'^([A-Z0-9]{2,3})$') and contains('380,383,386,389,FT,FS,FR,ND,RP,RE,CS,LD,RA,', concat(normalize-space(.), ',')))"},
{"id":"DT-CIUS-PT-003_cn","texto":"The BT-3 only allows the following values: 381, NC.","categoria":"valores","natureza":"RP","gravidade":"erro","contexto":"//cn:CreditNote/cbc:CreditNoteTypeCode","elementos":["BT-3"],"expressao":"(matches(.,'^([A-Z0-9]{2,3})$') and contains('381,NC,', concat(normalize-space(.), ',')))"},
{"id":"DT-CIUS-PT-151","texto":"The BT-5 must be coded using ISO code list 4217 alpha-3.","categoria":"valores","natureza":"RP","gravidade":"erro","contexto":"//ubl:Invoice/cbc:DocumentCurrencyCode | //cn:CreditNote/cbc:DocumentCurrencyCode","elementos":["BT-5"],"expressao":"(not(contains(normalize-space(.), ' ')) and contains(' AED AFN ALL AMD ANG AOA ARS AUD AWG AZN BAM BBD BDT BGN BHD BIF BMD BND BOB BOV BRL BSD BTN BWP BYR BZD CAD CDF CHE CHF CHW CLF CLP CNY COP COU CRC CUC CUP CVE CZK DJF DKK DOP DZD EGP ERN ETB EUR FJD FKP GBP GEL GHS GIP GMD GNF GTQ GYD HKD HNL HRK HTG HUF IDR ILS INR IQD IRR ISK JMD JOD JPY KES KGS KHR KMF KPW KRW KWD KYD KZT LAK LBP LKR LRD LSL LYD MAD MDL MGA MKD MMK MNT MOP MRO MUR MVR MWK MXN MXV MYR MZN NAD NGN NIO NOK NPR NZD OMR PAB PEN PGK PHP PKR PLN PYG QAR RON RSD RUB RWF SAR SBD SCR SDG SEK SGD SHP SLL SOS SRD SSP STD SVC SYP SZL THB TJS TMT TND TOP TRY TTD TWD TZS UAH UGX USD USN UYI UYU UZS VEF VND VUV WST XAF XAG XAU XBA XBB XBC XBD XCD XDR XOF XPD XPF XPT XSU XTS XUA XXX YER ZAR ZMW ZWL ', concat(' ', normalize-space(.), ' ')))"},
{"id":"DT-CIUS-PT-152","texto":"the BT-6 must be coded using ISO code list 4217 alpha-3.","categoria":"valores","natureza":"RP","gravidade":"erro","contexto":"//ubl:Invoice/cbc:TaxCurrencyCode | //cn:CreditNote/cbc:TaxCurrencyCode","elementos":["BT-6"],"expressao":"(not(contains(normalize-space(.), ' ')) and contains(' AED AFN ALL AMD ANG AOA ARS AUD AWG AZN BAM BBD BDT BGN BHD BIF BMD BND BOB BOV BRL BSD BTN BWP BYR BZD CAD CDF CHE CHF CHW CLF CLP CNY COP COU CRC CUC CUP CVE CZK DJF DKK DOP DZD EGP ERN ETB EUR FJD FKP GBP GEL GHS GIP GMD GNF GTQ GYD HKD HNL HRK HTG HUF IDR ILS INR IQD IRR ISK JMD JOD JPY KES KGS KHR KMF KPW KRW KWD KYD KZT LAK LBP LKR LRD LSL LYD MAD MDL MGA MKD MMK MNT MOP MRO MUR MVR MWK MXN MXV MYR MZN NAD NGN NIO NOK NPR NZD OMR PAB PEN PGK PHP PKR PLN PYG QAR RON RSD RUB RWF SAR SBD SCR SDG SEK SGD SHP SLL SOS SRD SSP STD SVC SYP SZL THB TJS TMT TND TOP TRY TTD TWD TZS UAH UGX USD USN UYI UYU UZS VEF VND VUV WST XAF XAG XAU XBA XBB XBC XBD XCD XDR XOF XPD XPF XPT XSU XTS XUA XXX YER ZAR ZMW ZWL ', concat(' ', normalize-space(.), ' ')))"},
{"id":"DT-CIUS-PT-006","texto":"The BT-7 does not meet the defined format: YYYY-MM-DD.","categoria":"formato","natureza":"RP","gravidade":"erro","contexto":"//ubl:Invoice/cbc:TaxPointDate | //cn:CreditNote/cbc:TaxPointDate","elementos":["BT-7"],"expressao":"matches(.,'^((\\d{4})-(\\d{2})-(\\d{2}))$')"},
{"id":"DT-CIUS-PT-007","texto":"The BT-8 only allows the following values: 3, 35, 432.","categoria":"valores","natureza":"RP","gravidade":"erro","contexto":"//ubl:Invoice/cac:InvoicePeriod/cbc:DescriptionCode | //cn:CreditNote/cac:InvoicePeriod/cbc:DescriptionCode","elementos":["BT-8"],"expressao":"(matches(.,'^(\\d{1,3})$') and contains('3,35,432,', concat(normalize-space(.), ',')))"},
{"id":"DT-CIUS-PT-008","texto":"The BT-9 does not meet the defined format: YYYY-MM-DD.","categoria":"formato","natureza":"RP","gravidade":"erro","contexto":"//ubl:Invoice/cbc:DueDate | //cn:CreditNote/cac:PaymentMeans/cbc:PaymentDueDate","elementos":["BT-9"],"expressao":"matches(.,'^((\\d{4})-(\\d{2})-(\\d{2}))$')"},
{"id":"DT-CIUS-PT-009","texto":"The BT-10 does not meet the defined format: alphanumeric with size between 1 and 50.","categoria":"formato","natureza":"RP","gravidade":"erro","contexto":"//ubl:Invoice/cbc:BuyerReference | //cn:CreditNote/cbc:BuyerReference","elementos":["BT-10"],"expressao":"matches(.,'^(.{1,50})$')"},
{"id":"DT-CIUS-PT-010","texto":"The BT-11 does not meet the defined format: alphanumeric with size between 1 and 50.","categoria":"formato","natureza":"RP","gravidade":"erro","contexto":"//ubl:Invoice/cac:ProjectReference/cbc:ID | //cn:CreditNote/cac:ProjectReference/cbc:ID","elementos":["BT-11"],"expressao":"matches(.,'^(.{1,50})$')"},
{"id":"DT-CIUS-PT-011","texto":"The BT-12 does not meet the defined format: alphanumeric with size between 1 and 20.","categoria":"formato","natureza":"RP","gravidade":"erro","contexto":"//ubl:Invoice/cac:ContractDocumentReference/cbc:ID | //cn:CreditNote/cac:ContractDocumentReference/cbc:ID","elementos":["BT-12"],"expressao":"matches(.,'^(.{1,20})$')"},
{"id":"DT-CIUS-PT-012","texto":"The BT-13 does not meet the defined format: alphanumeric with size between 1 and 20.","categoria":"formato","natureza":"RP","gravidade":"erro","contexto":"//ubl:Invoice/cac:OrderReference/cbc:ID | //cn:CreditNote/cac:OrderReference/cbc:ID","elementos":["BT-13"],"expressao":"matches(.,'^(.{1,20})$')"},
{"id":"DT-CIUS-PT-013","texto":"The BT-14 does not meet the defined format: alphanumeric with size between 1 and 20.","categoria":"formato","natureza":"RP","gravidade":"erro","contexto":"//ubl:Invoice/cac:OrderReference/cbc:SalesOrderID | //cn:CreditNote/cac:OrderReference/cbc:SalesOrderID","elementos":["BT-14"],"expressao":"matches(.,'^(.{1,20})$')"},
{"id":"DT-CIUS-PT-014","texto":"The BT-15 does not meet the defined format: alphanumeric with size between 1 and 20.","categoria":"formato","natureza":"RP","gravidade":"erro","contexto":"//ubl:Invoice/cac:ReceiptDocumentReference/cbc:ID | //cn:CreditNote/cac:ReceiptDocumentReference/cbc:ID","elementos":["BT-15"],"expressao":"matches(.,'^(.{1,20})$')"},
{"id":"DT-CIUS-PT-015","texto":"The BT-16 does not meet the defined format: alphanumeric with size between 1 and 20.","categoria":"formato","natureza":"RP","gravidade":"erro","contexto":"//ubl:Invoice/cac:DespatchDocumentReference/cbc:ID | //cn:CreditNote/cac:DespatchDocumentReference/cbc:ID","elementos":["BT-16"],"expressao":"matches(.,'^(.{1,20})$')"},
{"id":"DT-CIUS-PT-016","texto":"The BT-17 does not meet the defined format: alphanumeric with size between 1 and 20.","categoria":"formato","natureza":"RP","gravidade":"erro","contexto":"//ubl:Invoice/cac:OriginatorDocumentReference/cbc:ID | //cn:CreditNote/cac:OriginatorDocumentReference/cbc:ID","elementos":["BT-17"],"expressao":"matches(.,'^(.{1,20})$')"},
{"id":"DT-CIUS-PT-017.1","texto":"The BT-18 and BT-122 does not meet the defined format: alphanumeric with size between 1 and 50.","categoria":"formato","natureza":"RP","gravidade":"erro","contexto":"//ubl:Invoice/cac:AdditionalDocumentReference/cbc:ID | //cn:CreditNote/cac:AdditionalDocumentReference/cbc:ID","elementos":["BT-18","BT-122"],"expressao":"matches(.,'^(.{1,50})$')"},
{"id":"DT-CIUS-PT-017.2","texto":"The BT-18 and BT-122 identification scheme identifier MUST be coded using a restriction of UNTDID 1153.","categoria":"outra","natureza":"?","gravidade":"erro","contexto":"//ubl:Invoice/cac:AdditionalDocumentReference/cbc:ID | //cn:CreditNote/cac:AdditionalDocumentReference/cbc:ID","elementos":["BT-18","BT-122"],"expressao":"report (dispara quando verdadeiro): (exists(@schemeID) and (contains(normalize-space(@schemeID), ' ') or not(contains(' AAA AAB AAC AAD AAE AAF AAG AAH AAI AAJ AAK AAL AAM AAN AAO AAP AAQ AAR AAS AAT AAU AAV AAW AAX AAY AAZ ABA ABB ABC ABD ABE ABF ABG ABH ABI ABJ ABK ABL ABM ABN ABO ABP ABQ ABR ABS ABT ABU ABV ABW ABX ABY ABZ AC ACA ACB ACC ACD ACE ACF ACG ACH ACI ACJ ACK ACL ACN ACO ACP ACQ ACR ACT ACU ACV ACW ACX ACY ACZ ADA ADB ADC ADD ADE ADF ADG ADI ADJ ADK ADL ADM ADN ADO ADP ADQ ADT ADU ADV ADW ADX ADY ADZ AE AEA AEB AEC AED AEE AEF AEG AEH AEI AEJ AEK AEL AEM AEN AEO AEP AEQ AER AES AET AEU AEV AEW AEX AEY AEZ AF AFA AFB AFC AFD AFE AFF AFG AFH AFI AFJ AFK AFL AFM AFN AFO AFP AFQ AFR AFS AFT AFU AFV AFW AFX AFY AFZ AGA AGB AGC AGD AGE AGF AGG AGH AGI AGJ AGK AGL AGM AGN AGO AGP AGQ AGR AGS AGT AGU AGV AGW AGX AGY AGZ AHA AHB AHC AHD AHE AHF AHG AHH AHI AHJ AHK AHL AHM AHN AHO AHP AHQ AHR AHS AHT AHU AHV AHX AHY AHZ AIA AIB AIC AID AIE AIF AIG AIH AII AIJ AIK AIL AIM AIN AIO AIP AIQ AIR AIS AIT AIU AIV AIW AIX AIY AIZ AJA AJB AJC AJD AJE AJF AJG AJH AJI AJJ AJK AJL AJM AJN AJO AJP AJQ AJR AJS AJT AJU AJV AJW AJX AJY AJZ AKA AKB AKC AKD AKE AKF AKG AKH AKI AKJ AKK AKL AKM AKN AKO AKP AKQ AKR AKS AKT AKU AKV AKW AKX AKY AKZ ALA ALB ALC ALD ALE ALF ALG ALH ALI ALJ ALK ALL ALM ALN ALO ALP ALQ ALR ALS ALT ALU ALV ALW ALX ALY ALZ AMA AMB AMC AMD AME AMF AMG AMH AMI AMJ AMK AML AMM AMN AMO AMP AMQ AMR AMS AMT AMU AMV AMW AMX AMY AMZ ANA ANB ANC AND ANE ANF ANG ANH ANI ANJ ANK ANL ANM ANN ANO ANP ANQ ANR ANS ANT ANU ANV ANW ANX ANY AOA AOD AOE AOF AOG AOH AOI AOJ AOK AOL AOM AON AOO AOP AOQ AOR AOS AOT AOU AOV AOW AOX AOY AOZ AP APA APB APC APD APE APF APG APH API APJ APK APL APM APN APO APP APQ APR APS APT APU APV APW APX APY APZ AQA AQB AQC AQD AQE AQF AQG AQH AQI AQJ AQK AQL AQM AQN AQO AQP AQQ AQR AQS AQT AQU AQV AQW AQX AQY AQZ ARA ARB ARC ARD ARE ARF ARG ARH ARI ARJ ARK ARL ARM ARN ARO ARP ARQ ARR ARS ART ARU ARV ARW ARX ARY ARZ ASA ASB ASC ASD ASE ASF ASG ASH ASI ASJ ASK ASL ASM ASN ASO ASP ASQ ASR ASS AST ASU ASV ASW ASX ASY ASZ ATA ATB ATC ATD ATE ATF ATG ATH ATI ATJ ATK ATL ATM ATN ATO ATP ATQ ATR ATS ATT ATU ATV ATW ATX ATY ATZ AU AUA AUB AUC AUD AUE AUF AUG AUH AUI AUJ AUK AUL AUM AUN AUO AUP AUQ AUR AUS AUT AUU AUV AUW AUX AUY AUZ AV AVA AVB AVC AVD AVE AVF AVG AVH AVI AVJ AVK AVL AVM AVN AVO AVP AVQ AVR AVS AVT AVU AVV AVW AVX AVY AVZ AWA AWB AWC AWD AWE AWF AWG AWH AWI AWJ AWK AWL AWM AWN AWO AWP AWQ AWR AWS AWT AWU AWV AWW AWX AWY AWZ AXA AXB AXC AXD AXE AXF AXG AXH AXI AXJ AXK AXL AXM AXN AXO AXP AXQ AXR BA BC BD BE BH BM BN BO BR BT BW CAS CAT CAU CAV CAW CAX CAY CAZ CBA CBB CD CEC CED CFE CFF CFO CG CH CK CKN CM CMR CN CNO COF CP CR CRN CS CST CT CU CV CW CZ DA DAN DB DI DL DM DQ DR EA EB ED EE EI EN EQ ER ERN ET EX FC FF FI FLW FN FO FS FT FV FX GA GC GD GDN GN HS HWB IA IB ICA ICE ICO II IL INB INN INO IP IS IT IV JB JE LA LAN LAR LB LC LI LO LRC LS MA MB MF MG MH MR MRN MS MSS MWB NA NF OH OI ON OP OR PB PC PD PE PF PI PK PL POR PP PQ PR PS PW PY RA RC RCN RE REN RF RR RT SA SB SD SE SEA SF SH SI SM SN SP SQ SRN SS STA SW SZ TB TCR TE TF TI TIN TL TN TP UAR UC UCN UN UO URI VA VC VGR VM VN VON VOR VP VR VS VT VV WE WM WN WR WS WY XA XC XP ZZZ ', concat(' ', normalize-space(@schemeID), ' ')))))"},
{"id":"DT-CIUS-PT-153","texto":"The Document type code only allows the following values: 130.","categoria":"valores","natureza":"RP","gravidade":"erro","contexto":"//ubl:Invoice/cac:AdditionalDocumentReference/cbc:DocumentTypeCode | //cn:CreditNote/cac:AdditionalDocumentReference/cbc:DocumentTypeCode","expressao":"(not(contains(normalize-space(.), ' ')) and contains(' 130 ', concat(' ', normalize-space(.), ' ')))"},
{"id":"DT-CIUS-PT-018","texto":"The BT-19 does not meet the defined format: alphanumeric with size between 1 and 50.","categoria":"formato","natureza":"RP","gravidade":"erro","contexto":"//ubl:Invoice/cbc:AccountingCost | //cn:CreditNote/cbc:AccountingCost","elementos":["BT-19"],"expressao":"matches(.,'^(.{1,50})$')"},
{"id":"DT-CIUS-PT-019","texto":"The BT-20 does not meet the defined format: alphanumeric with size between 1 and 200.","categoria":"formato","natureza":"RP","gravidade":"erro","contexto":"//ubl:Invoice/cac:PaymentTerms/cbc:Note | //cn:CreditNote/cac:PaymentTerms/cbc:Note","elementos":["BT-20"],"expressao":"matches(.,'^(.{1,200})$')"},
{"id":"DT-CIUS-PT-020","texto":"The BT-22 does not meet the defined format: alphanumeric with size between 1 and 500.","categoria":"formato","natureza":"RP","gravidade":"erro","contexto":"//ubl:Invoice/cbc:Note | //cn:CreditNote/cbc:Note","elementos":["BT-22"],"expressao":"matches(.,'^(.{1,500})$','s')"},
{"id":"DT-CIUS-PT-020_2.1","texto":"The BT-22 when prefixed with '#SOURCECURRENCYCODE#', MUST be coded using ISO code list 4217 alpha-3.","categoria":"condicional","natureza":"RIR","gravidade":"erro","contexto":"//ubl:Invoice/cbc:Note | //cn:CreditNote/cbc:Note","elementos":["BT-22"],"expressao":"report (dispara quando verdadeiro): starts-with(normalize-space(.),'#SOURCECURRENCYCODE#') and not((not(contains(normalize-space(substring-before(substring-after(.,'#SOURCECURRENCYCODE#'),'#')), ' ')) and contains(' AED AFN ALL AMD ANG AOA ARS AUD AWG AZN BAM BBD BDT BGN BHD BIF BMD BND BOB BOV BRL BSD BTN BWP BYR BZD CAD CDF CHE CHF CHW CLF CLP CNY COP COU CRC CUC CUP CVE CZK DJF DKK DOP DZD EGP ERN ETB EUR FJD FKP GBP GEL GHS GIP GMD GNF GTQ GYD HKD HNL HRK HTG HUF IDR ILS INR IQD IRR ISK JMD JOD JPY KES KGS KHR KMF KPW KRW KWD KYD KZT LAK LBP LKR LRD LSL LYD MAD MDL MGA MKD MMK MNT MOP MRO MUR MVR MWK MXN MXV MYR MZN NAD NGN NIO NOK NPR NZD OMR PAB PEN PGK PHP PKR PLN PYG QAR RON RSD RUB RWF SAR SBD SCR SDG SEK SGD SHP SLL SOS SRD SSP STD SVC SYP SZL THB TJS TMT TND TOP TRY TTD TWD TZS UAH UGX USD USN UYI UYU UZS VEF VND VUV WST XAF XAG XAU XBA XBB XBC XBD XCD XDR XOF XPD XPF XPT XSU XTS XUA XXX YER ZAR ZMW ZWL ', concat(' ', normalize-space(substring-before(substring-after(.,'#SOURCECURRENCYCODE#'),'#')), ' '))))"},
{"id":"DT-CIUS-PT-020_2.2","texto":"The BT-22 does not meet the defined format: it is mandatory to prefix the value with the following '#SOURCECURRENCYCODE#' and suffice with '#'.","categoria":"formato","natureza":"RP","gravidade":"erro","contexto":"//ubl:Invoice/cbc:Note | //cn:CreditNote/cbc:Note","elementos":["BT-22"],"expressao":"report (dispara quando verdadeiro): starts-with(normalize-space(.),'#SOURCECURRENCYCODE#') and not(matches(.,'^(#(SOURCECURRENCYCODE)#(.+)#)$'))"},
{"id":"DT-CIUS-PT-020_2.3","texto":"The BT-22 when prefixed with '#SOURCECURRENCYCODE#', is mandatory if an element with the prefix '#CALCULATIONRATE#' has been or will be referenced.","categoria":"condicional","natureza":"RIR","gravidade":"erro","contexto":"//ubl:Invoice/cbc:Note | //cn:CreditNote/cbc:Note","elementos":["BT-22"],"expressao":"report (dispara quando verdadeiro): starts-with(normalize-space(.),'#CALCULATIONRATE#') and $cnt20_2 < 1"},
{"id":"DT-CIUS-PT-020_2.4","texto":"The BT-22 when prefixed with '#SOURCECURRENCYCODE#', can only exist once.","categoria":"condicional","natureza":"RIR","gravidade":"erro","contexto":"//ubl:Invoice/cbc:Note | //cn:CreditNote/cbc:Note","elementos":["BT-22"],"expressao":"report (dispara quando verdadeiro): starts-with(normalize-space(.),'#SOURCECURRENCYCODE#') and $cnt20_2 > 1"},
{"id":"DT-CIUS-PT-020_3.1","texto":"The BT-22 when prefixed with '#CALCULATIONRATE#', have to meet the defined format: decimal value with 5 decimal places and 9 unit places.","categoria":"condicional","natureza":"RIR","gravidade":"erro","contexto":"//ubl:Invoice/cbc:Note | //cn:CreditNote/cbc:Note","elementos":["BT-22"],"expressao":"report (dispara quando verdadeiro): starts-with(normalize-space(.),'#CALCULATIONRATE#') and not(matches(normalize-space(substring-before(substring-after(.,'#CALCULATIONRATE#'),'#')),'^(\\d{1,9}\\.\\d{2,5})$'))"},
{"id":"DT-CIUS-PT-020_3.2","texto":"The BT-22 does not meet the defined format: it is mandatory to prefix the value with the following '#CALCULATIONRATE#' and suffice with '#'.","categoria":"formato","natureza":"RP","gravidade":"erro","contexto":"//ubl:Invoice/cbc:Note | //cn:CreditNote/cbc:Note","elementos":["BT-22"],"expressao":"report (dispara quando verdadeiro): starts-with(normalize-space(.),'#CALCULATIONRATE#') and not(matches(.,'^(#(CALCULATIONRATE)#(.+)#)$'))"},
{"id":"DT-CIUS-PT-020_3.3","texto":"The BT-22 when prefixed with '#CALCULATIONRATE#', is mandatory if an element with the prefix '#SOURCECURRENCYCODE#' has been or will be referenced.","categoria":"condicional","natureza":"RIR","gravidade":"erro","contexto":"//ubl:Invoice/cbc:Note | //cn:CreditNote/cbc:Note","elementos":["BT-22"],"expressao":"report (dispara quando verdadeiro): starts-with(normalize-space(.),'#SOURCECURRENCYCODE#') and $cnt20_3 < 1"},
{"id":"DT-CIUS-PT-020_3.4","texto":"The BT-22 when prefixed with '#CALCULATIONRATE#', can only exist once.","categoria":"condicional","natureza":"RIR","gravidade":"erro","contexto":"//ubl:Invoice/cbc:Note | //cn:CreditNote/cbc:Note","elementos":["BT-22"],"expressao":"report (dispara quando verdadeiro): starts-with(normalize-space(.),'#CALCULATIONRATE#') and $cnt20_3 > 1"},
{"id":"DT-CIUS-PT-020_4.1","texto":"The BT-22 when prefixed with '#DESCRIPTION@INVOICEPERIOD#', have to meet the defined format: alphanumeric with size between 1 and 150.","categoria":"condicional","natureza":"RIR","gravidade":"erro","contexto":"//ubl:Invoice/cbc:Note | //cn:CreditNote/cbc:Note","elementos":["BT-22"],"expressao":"report (dispara quando verdadeiro): starts-with(normalize-space(.),'#DESCRIPTION@INVOICEPERIOD#') and not(matches(normalize-space(substring-before(substring-after(.,'#DESCRIPTION@INVOICEPERIOD#'),'#')),'^(.{1,150})$'))"},
{"id":"DT-CIUS-PT-020_4.2","texto":"The BT-22 does not meet the defined format: it is mandatory to prefix the value with the following '#DESCRIPTION@INVOICEPERIOD#' and suffice with '#'.","categoria":"formato","natureza":"RP","gravidade":"erro","contexto":"//ubl:Invoice/cbc:Note | //cn:CreditNote/cbc:Note","elementos":["BT-22"],"expressao":"report (dispara quando verdadeiro): starts-with(normalize-space(.),'#DESCRIPTION@INVOICEPERIOD#') and not(matches(.,'^(#(DESCRIPTION@INVOICEPERIOD)#(.{1,150})#)$'))"},
{"id":"DT-CIUS-PT-020_4.3","texto":"The BT-22 when prefixed with '#DESCRIPTION@INVOICEPERIOD#', can only exist once.","categoria":"condicional","natureza":"RIR","gravidade":"erro","contexto":"//ubl:Invoice/cbc:Note | //cn:CreditNote/cbc:Note","elementos":["BT-22"],"expressao":"report (dispara quando verdadeiro): starts-with(normalize-space(.),'#DESCRIPTION@INVOICEPERIOD#') and $cnt20_4 > 1"},
{"id":"DT-CIUS-PT-020_5.1","texto":"The BT-22 when prefixed with '#ADDITIONALPROPERTY#', have to meet the defined format for name: alphanumeric with size between 1 and 50.","categoria":"condicional","natureza":"RIR","gravidade":"erro","contexto":"//ubl:Invoice/cbc:Note | //cn:CreditNote/cbc:Note","elementos":["BT-22"],"expressao":"report (dispara quando verdadeiro): starts-with(normalize-space(.),'#ADDITIONALPROPERTY#') and not(matches(normalize-space(substring-before(substring-after(.,'#ADDITIONALPROPERTY#'),'#')),'^(.{1,50})$'))"},
{"id":"DT-CIUS-PT-020_5.2","texto":"The BT-22 when prefixed with '#ADDITIONALPROPERTY#', have to meet the defined format for value: alphanumeric with size between 1 and 50.","categoria":"condicional","natureza":"RIR","gravidade":"erro","contexto":"//ubl:Invoice/cbc:Note | //cn:CreditNote/cbc:Note","elementos":["BT-22"],"expressao":"report (dispara quando verdadeiro): starts-with(normalize-space(.),'#ADDITIONALPROPERTY#') and not(matches(normalize-space(substring-before(substring-after(substring-after(.,'#ADDITIONALPROPERTY#'),'#'),'#')),'^(.{1,50})$'))"},
{"id":"DT-CIUS-PT-020_5.3","texto":"The BT-22 does not meet the defined format: it is mandatory to prefix the value with the following '#ADDITIONALPROPERTY#' and suffice with '#'. The value must consist of a first part for the name, separated by \"#\", and for a second part for the value.","categoria":"formato","natureza":"RP","gravidade":"erro","contexto":"//ubl:Invoice/cbc:Note | //cn:CreditNote/cbc:Note","elementos":["BT-22"],"expressao":"report (dispara quando verdadeiro): starts-with(normalize-space(.),'#ADDITIONALPROPERTY#') and not(matches(.,'^(#(ADDITIONALPROPERTY)#(.{1,50})#(.{1,50})#)$'))"},
{"id":"DT-CIUS-PT-020_6.1","texto":"The BT-22 when prefixed with '#NUMBER@ATCERTIFIEDPROGRAM#', have to meet the defined format: alphanumeric with size between 1 and 20.","categoria":"condicional","natureza":"RIR","gravidade":"erro","contexto":"//ubl:Invoice/cbc:Note | //cn:CreditNote/cbc:Note","elementos":["BT-22"],"expressao":"report (dispara quando verdadeiro): starts-with(normalize-space(.),'#NUMBER@ATCERTIFIEDPROGRAM#') and not(matches(normalize-space(substring-before(substring-after(.,'#NUMBER@ATCERTIFIEDPROGRAM#'),'#')),'^(.{1,20})$'))"},
{"id":"DT-CIUS-PT-020_6.2","texto":"The BT-22 does not meet the defined format: it is mandatory to prefix the value with the following '#NUMBER@ATCERTIFIEDPROGRAM#' and suffice with '#'.","categoria":"formato","natureza":"RP","gravidade":"erro","contexto":"//ubl:Invoice/cbc:Note | //cn:CreditNote/cbc:Note","elementos":["BT-22"],"expressao":"report (dispara quando verdadeiro): starts-with(normalize-space(.),'#NUMBER@ATCERTIFIEDPROGRAM#') and not(matches(.,'^(#(NUMBER@ATCERTIFIEDPROGRAM)#(.+)#)$'))"},
{"id":"DT-CIUS-PT-020_6.3","texto":"The BT-22 when prefixed with '#NUMBER@ATCERTIFIEDPROGRAM#', is mandatory if an element with the prefix '#HASHCODE@ATCERTIFIEDPROGRAM#' or '#DESCRIPTION@ATCERTIFIEDPROGRAM#' has been or will be referenced.","categoria":"condicional","natureza":"RIR","gravidade":"erro","contexto":"//ubl:Invoice/cbc:Note | //cn:CreditNote/cbc:Note","elementos":["BT-22"],"expressao":"report (dispara quando verdadeiro): (starts-with(normalize-space(.),'#HASHCODE@ATCERTIFIEDPROGRAM#') or starts-with(normalize-space(.),'#DESCRIPTION@ATCERTIFIEDPROGRAM#')) and $cnt20_6 < 1"},
{"id":"DT-CIUS-PT-020_6.4","texto":"The BT-22 when prefixed with '#NUMBER@ATCERTIFIEDPROGRAM#', can only exist once.","categoria":"condicional","natureza":"RIR","gravidade":"erro","contexto":"//ubl:Invoice/cbc:Note | //cn:CreditNote/cbc:Note","elementos":["BT-22"],"expressao":"report (dispara quando verdadeiro): starts-with(normalize-space(.),'#NUMBER@ATCERTIFIEDPROGRAM#') and $cnt20_6 > 1"},
{"id":"DT-CIUS-PT-020_7.1","texto":"The BT-22 when prefixed with '#HASHCODE@ATCERTIFIEDPROGRAM#', have to meet the defined format: alphanumeric with size between 1 and 20.","categoria":"condicional","natureza":"RIR","gravidade":"erro","contexto":"//ubl:Invoice/cbc:Note | //cn:CreditNote/cbc:Note","elementos":["BT-22"],"expressao":"report (dispara quando verdadeiro): starts-with(normalize-space(.),'#HASHCODE@ATCERTIFIEDPROGRAM#') and not(matches(normalize-space(substring-before(substring-after(.,'#HASHCODE@ATCERTIFIEDPROGRAM#'),'#')),'^(.{1,20})$'))"},
{"id":"DT-CIUS-PT-020_7.2","texto":"The BT-22 does not meet the defined format: it is mandatory to prefix the value with the following '#HASHCODE@ATCERTIFIEDPROGRAM#' and suffice with '#'.","categoria":"formato","natureza":"RP","gravidade":"erro","contexto":"//ubl:Invoice/cbc:Note | //cn:CreditNote/cbc:Note","elementos":["BT-22"],"expressao":"report (dispara quando verdadeiro): starts-with(normalize-space(.),'#HASHCODE@ATCERTIFIEDPROGRAM#') and not(matches(.,'^(#(HASHCODE@ATCERTIFIEDPROGRAM)#(.+)#)$'))"},
{"id":"DT-CIUS-PT-020_7.3","texto":"The BT-22 when prefixed with '#HASHCODE@ATCERTIFIEDPROGRAM#', is mandatory if an element with the prefix '#NUMBER@ATCERTIFIEDPROGRAM#' or '#DESCRIPTION@ATCERTIFIEDPROGRAM#' has been or will be referenced.","categoria":"condicional","natureza":"RIR","gravidade":"erro","contexto":"//ubl:Invoice/cbc:Note | //cn:CreditNote/cbc:Note","elementos":["BT-22"],"expressao":"report (dispara quando verdadeiro): (starts-with(normalize-space(.),'#NUMBER@ATCERTIFIEDPROGRAM#') or starts-with(normalize-space(.),'#DESCRIPTION@ATCERTIFIEDPROGRAM#')) and $cnt20_7 < 1"},
{"id":"DT-CIUS-PT-020_7.4","texto":"The BT-22 when prefixed with '#HASHCODE@ATCERTIFIEDPROGRAM#', can only exist once.","categoria":"condicional","natureza":"RIR","gravidade":"erro","contexto":"//ubl:Invoice/cbc:Note | //cn:CreditNote/cbc:Note","elementos":["BT-22"],"expressao":"report (dispara quando verdadeiro): starts-with(normalize-space(.),'#HASHCODE@ATCERTIFIEDPROGRAM#') and $cnt20_7 > 1"},
{"id":"DT-CIUS-PT-020_8.1","texto":"The BT-22 when prefixed with '#HASHCODE@ATCERTIFIEDPROGRAM#', have to meet the defined format: alphanumeric with size between 1 and 150.","categoria":"condicional","natureza":"RIR","gravidade":"erro","contexto":"//ubl:Invoice/cbc:Note | //cn:CreditNote/cbc:Note","elementos":["BT-22"],"expressao":"report (dispara quando verdadeiro): starts-with(normalize-space(.),'#DESCRIPTION@ATCERTIFIEDPROGRAM#') and not(matches(normalize-space(substring-before(substring-after(.,'#DESCRIPTION@ATCERTIFIEDPROGRAM#'),'#')),'^(.{1,150})$'))"},
{"id":"DT-CIUS-PT-020_8.2","texto":"The BT-22 does not meet the defined format: it is mandatory to prefix the value with the following '#DESCRIPTION@ATCERTIFIEDPROGRAM#' and suffice with '#'.","categoria":"formato","natureza":"RP","gravidade":"erro","contexto":"//ubl:Invoice/cbc:Note | //cn:CreditNote/cbc:Note","elementos":["BT-22"],"expressao":"report (dispara quando verdadeiro): starts-with(normalize-space(.),'#DESCRIPTION@ATCERTIFIEDPROGRAM#') and not(matches(.,'^(#(DESCRIPTION@ATCERTIFIEDPROGRAM)#(.+)#)$'))"},
{"id":"DT-CIUS-PT-020_8.3","texto":"The BT-22 when prefixed with '#DESCRIPTION@ATCERTIFIEDPROGRAM#', can only exist once.","categoria":"condicional","natureza":"RIR","gravidade":"erro","contexto":"//ubl:Invoice/cbc:Note | //cn:CreditNote/cbc:Note","elementos":["BT-22"],"expressao":"report (dispara quando verdadeiro): starts-with(normalize-space(.),'#DESCRIPTION@ATCERTIFIEDPROGRAM#') and $cnt20_8 > 1"},
{"id":"DT-CIUS-PT-020_9.1","texto":"The BT-22 does not meet the defined format: it is mandatory to prefix the value with the following '#WITHHOLDINGTAXDESCRIPTION@WITHHOLDINGTAX-000#' and suffice with '#'. The sub-suffix \"-000\" must be used as a group of elements.","categoria":"formato","natureza":"RP","gravidade":"erro","contexto":"//ubl:Invoice/cbc:Note | //cn:CreditNote/cbc:Note","elementos":["BT-22"],"expressao":"report (dispara quando verdadeiro): starts-with(normalize-space(.),'#WITHHOLDINGTAXDESCRIPTION@WITHHOLDINGTAX-') and not(matches(.,'^(#(WITHHOLDINGTAXDESCRIPTION@WITHHOLDINGTAX)-([0-9]{3})#(.+)#)$'))"},
{"id":"DT-CIUS-PT-020_9.2","texto":"The BT-22 when prefixed with '#WITHHOLDINGTAXDESCRIPTION@WITHHOLDINGTAX-000#', have to meet the defined format: alphanumeric with size between 1 and 150.","categoria":"condicional","natureza":"RIR","gravidade":"erro","contexto":"//ubl:Invoice/cbc:Note | //cn:CreditNote/cbc:Note","elementos":["BT-22"],"expressao":"report (dispara quando verdadeiro): starts-with(normalize-space(.),'#WITHHOLDINGTAXDESCRIPTION@WITHHOLDINGTAX-') and not(matches(normalize-space(substring-before(substring-after(.,$wht20_9),'#')),'^(.{1,150})$'))"},
{"id":"DT-CIUS-PT-020_9.3","texto":"The BT-22 when prefixed with '#WITHHOLDINGTAXDESCRIPTION@WITHHOLDINGTAX-000#' must be unique.","categoria":"condicional","natureza":"RIR","gravidade":"erro","contexto":"//ubl:Invoice/cbc:Note | //cn:CreditNote/cbc:Note","elementos":["BT-22"],"expressao":"report (dispara quando verdadeiro): starts-with(normalize-space(.),$wht20_9) and $cnt20_9 > 1"},
{"id":"DT-CIUS-PT-020_9.4","texto":"The BT-22 when prefixed with '#WITHHOLDINGTAXDESCRIPTION@WITHHOLDINGTAX-000#' is mandatory an element with the prefix '#WITHHOLDINGTAXTYPE@WITHHOLDINGTAX-000#'.","categoria":"condicional","natureza":"RIR","gravidade":"erro","contexto":"//ubl:Invoice/cbc:Note | //cn:CreditNote/cbc:Note","elementos":["BT-22"],"expressao":"report (dispara quando verdadeiro): starts-with(normalize-space(.),$wht20_9) and (every $note in (ancestor::ubl:Invoice/cbc:Note | ancestor::cn:CreditNote/cbc:Note) satisfies (not(starts-with(normalize-space($note),concat('#WITHHOLDINGTAXTYPE@WITHHOLDINGTAX-',normalize-space(substring-before(substring-after(.,'#WITHHOLDINGTAXDESCRIPTION@WITHHOLDINGTAX-'),'#')),'#')))))"},
{"id":"DT-CIUS-PT-020_9.5","texto":"The BT-22 when prefixed with '#WITHHOLDINGTAXDESCRIPTION@WITHHOLDINGTAX-000#' is mandatory an element with the prefix '#WITHHOLDINGTAXAMOUNT@WITHHOLDINGTAX-000#'.","categoria":"condicional","natureza":"RIR","gravidade":"erro","contexto":"//ubl:Invoice/cbc:Note | //cn:CreditNote/cbc:Note","elementos":["BT-22"],"expressao":"report (dispara quando verdadeiro): starts-with(normalize-space(.),$wht20_9) and (every $note in (ancestor::ubl:Invoice/cbc:Note | ancestor::cn:CreditNote/cbc:Note) satisfies (not(starts-with(normalize-space($note),concat('#WITHHOLDINGTAXAMOUNT@WITHHOLDINGTAX-',normalize-space(substring-before(substring-after(.,'#WITHHOLDINGTAXDESCRIPTION@WITHHOLDINGTAX-'),'#')),'#')))))"},
{"id":"DT-CIUS-PT-020_10.1","texto":"The BT-22 does not meet the defined format: it is mandatory to prefix the value with the following '#WITHHOLDINGTAXAMOUNT@WITHHOLDINGTAX-000#' and suffice with '#'. The sub-suffix \"-000\" must be used as a group of elements.","categoria":"formato","natureza":"RP","gravidade":"erro","contexto":"//ubl:Invoice/cbc:Note | //cn:CreditNote/cbc:Note","elementos":["BT-22"],"expressao":"report (dispara quando verdadeiro): starts-with(normalize-space(.),'#WITHHOLDINGTAXAMOUNT@WITHHOLDINGTAX-') and not(matches(.,'^(#(WITHHOLDINGTAXAMOUNT@WITHHOLDINGTAX)-([0-9]{3})#(.+)#)$'))"},
{"id":"DT-CIUS-PT-020_10.2","texto":"The BT-22 when prefixed with '#WITHHOLDINGTAXAMOUNT@WITHHOLDINGTAX-000#', have to meet the defined format: decimal value with 2 decimal places and 13 unit places.","categoria":"condicional","natureza":"RIR","gravidade":"erro","contexto":"//ubl:Invoice/cbc:Note | //cn:CreditNote/cbc:Note","elementos":["BT-22"],"expressao":"report (dispara quando verdadeiro): starts-with(normalize-space(.),'#WITHHOLDINGTAXAMOUNT@WITHHOLDINGTAX-') and not(matches(normalize-space(substring-before(substring-after(.,$wht20_10),'#')),'^([0-9]{1,13}.[0-9]{2})$'))"},
{"id":"DT-CIUS-PT-020_10.3","texto":"The BT-22 when prefixed with '#WITHHOLDINGTAXAMOUNT@WITHHOLDINGTAX-000#' must be unique.","categoria":"condicional","natureza":"RIR","gravidade":"erro","contexto":"//ubl:Invoice/cbc:Note | //cn:CreditNote/cbc:Note","elementos":["BT-22"],"expressao":"report (dispara quando verdadeiro): starts-with(normalize-space(.),$wht20_10) and $cnt20_10 > 1"},
{"id":"DT-CIUS-PT-020_10.4","texto":"The BT-22 when prefixed with '#WITHHOLDINGTAXAMOUNT@WITHHOLDINGTAX-000#' is mandatory an element with the prefix '#WITHHOLDINGTAXTYPE@WITHHOLDINGTAX-000#'.","categoria":"condicional","natureza":"RIR","gravidade":"erro","contexto":"//ubl:Invoice/cbc:Note | //cn:CreditNote/cbc:Note","elementos":["BT-22"],"expressao":"report (dispara quando verdadeiro): starts-with(normalize-space(.),$wht20_10) and (every $note in (ancestor::ubl:Invoice/cbc:Note | ancestor::cn:CreditNote/cbc:Note) satisfies (not(starts-with(normalize-space($note),concat('#WITHHOLDINGTAXTYPE@WITHHOLDINGTAX-',normalize-space(substring-before(substring-after(.,'#WITHHOLDINGTAXAMOUNT@WITHHOLDINGTAX-'),'#')),'#')))))"},
{"id":"DT-CIUS-PT-020_10.5","texto":"The BT-22 when prefixed with '#WITHHOLDINGTAXAMOUNT@WITHHOLDINGTAX-000#' is mandatory an element with the prefix '#WITHHOLDINGTAXDESCRIPTION@WITHHOLDINGTAX-000#'.","categoria":"condicional","natureza":"RIR","gravidade":"erro","contexto":"//ubl:Invoice/cbc:Note | //cn:CreditNote/cbc:Note","elementos":["BT-22"],"expressao":"report (dispara quando verdadeiro): starts-with(normalize-space(.),$wht20_10) and (every $note in (ancestor::ubl:Invoice/cbc:Note | ancestor::cn:CreditNote/cbc:Note) satisfies (not(starts-with(normalize-space($note),concat('#WITHHOLDINGTAXDESCRIPTION@WITHHOLDINGTAX-',normalize-space(substring-before(substring-after(.,'#WITHHOLDINGTAXAMOUNT@WITHHOLDINGTAX-'),'#')),'#')))))"},
{"id":"DT-CIUS-PT-020_11.1","texto":"The BT-22 does not meet the defined format: it is mandatory to prefix the value with the following '#WITHHOLDINGTAXTYPE@WITHHOLDINGTAX-000#' and suffice with '#'. The sub-suffix \"-000\" must be used as a group of elements.","categoria":"formato","natureza":"RP","gravidade":"erro","contexto":"//ubl:Invoice/cbc:Note | //cn:CreditNote/cbc:Note","elementos":["BT-22"],"expressao":"report (dispara quando verdadeiro): starts-with(normalize-space(.),'#WITHHOLDINGTAXTYPE@WITHHOLDINGTAX-') and not(matches(.,'^(#(WITHHOLDINGTAXTYPE@WITHHOLDINGTAX)-([0-9]{3})#(.+)#)$'))"},
{"id":"DT-CIUS-PT-020_11.2","texto":"The BT-22 when prefixed with '#WITHHOLDINGTAXTYPE@WITHHOLDINGTAX-000#', only admits the following values: IRF.","categoria":"condicional","natureza":"RIR","gravidade":"erro","contexto":"//ubl:Invoice/cbc:Note | //cn:CreditNote/cbc:Note","elementos":["BT-22"],"expressao":"report (dispara quando verdadeiro): starts-with(normalize-space(.),'#WITHHOLDINGTAXTYPE@WITHHOLDINGTAX-') and not(contains('IRF,', concat(normalize-space(substring-before(substring-after(.,$wht20_11),'#')), ',')))"},
{"id":"DT-CIUS-PT-020_11.3","texto":"The BT-22 when prefixed with '#WITHHOLDINGTAXTYPE@WITHHOLDINGTAX-000#' must be unique.","categoria":"condicional","natureza":"RIR","gravidade":"erro","contexto":"//ubl:Invoice/cbc:Note | //cn:CreditNote/cbc:Note","elementos":["BT-22"],"expressao":"report (dispara quando verdadeiro): starts-with(normalize-space(.),$wht20_11) and $cnt20_11 > 1"},
{"id":"DT-CIUS-PT-020_11.4","texto":"The BT-22 when prefixed with '#WITHHOLDINGTAXTYPE@WITHHOLDINGTAX-000#' is mandatory an element with the prefix '#WITHHOLDINGTAXDESCRIPTION@WITHHOLDINGTAX-000#'.","categoria":"condicional","natureza":"RIR","gravidade":"erro","contexto":"//ubl:Invoice/cbc:Note | //cn:CreditNote/cbc:Note","elementos":["BT-22"],"expressao":"report (dispara quando verdadeiro): starts-with(normalize-space(.),$wht20_11) and (every $note in (ancestor::ubl:Invoice/cbc:Note | ancestor::cn:CreditNote/cbc:Note) satisfies (not(starts-with(normalize-space($note),concat('#WITHHOLDINGTAXDESCRIPTION@WITHHOLDINGTAX-',normalize-space(substring-before(substring-after(.,'#WITHHOLDINGTAXTYPE@WITHHOLDINGTAX-'),'#')),'#')))))"},
{"id":"DT-CIUS-PT-020_11.5","texto":"The BT-22 when prefixed with '#WITHHOLDINGTAXTYPE@WITHHOLDINGTAX-000#' is mandatory an element with the prefix '#WITHHOLDINGTAXAMOUNT@WITHHOLDINGTAX-000#'.","categoria":"condicional","natureza":"RIR","gravidade":"erro","contexto":"//ubl:Invoice/cbc:Note | //cn:CreditNote/cbc:Note","elementos":["BT-22"],"expressao":"report (dispara quando verdadeiro): starts-with(normalize-space(.),$wht20_11) and (every $note in (ancestor::ubl:Invoice/cbc:Note | ancestor::cn:CreditNote/cbc:Note) satisfies (not(starts-with(normalize-space($note),concat('#WITHHOLDINGTAXAMOUNT@WITHHOLDINGTAX-',normalize-space(substring-before(substring-after(.,'#WITHHOLDINGTAXTYPE@WITHHOLDINGTAX-'),'#')),'#')))))"},
{"id":"DT-CIUS-PT-020_12.1","texto":"The BT-22 does not meet the defined format: it is mandatory to prefix the value with the following '#ENTITY@ATMPAYMENT-000#' and suffice with '#'. The sub-suffix \"-000\" must be used as a group of elements.","categoria":"formato","natureza":"RP","gravidade":"erro","contexto":"//ubl:Invoice/cbc:Note | //cn:CreditNote/cbc:Note","elementos":["BT-22"],"expressao":"report (dispara quando verdadeiro): starts-with(normalize-space(.),'#ENTITY@ATMPAYMENT-') and not(matches(.,'^(#(ENTITY@ATMPAYMENT)-([0-9]{3})#(.+)#)$'))"},
{"id":"DT-CIUS-PT-020_12.2","texto":"The BT-22 when prefixed with '#ENTITY@ATMPAYMENT-000#', have to meet the defined format: alphanumeric with size between 1 and 20.","categoria":"condicional","natureza":"RIR","gravidade":"erro","contexto":"//ubl:Invoice/cbc:Note | //cn:CreditNote/cbc:Note","elementos":["BT-22"],"expressao":"report (dispara quando verdadeiro): starts-with(normalize-space(.),'#ENTITY@ATMPAYMENT-') and not(matches(normalize-space(substring-before(substring-after(.,$atm20_12),'#')),'^(.{1,20})$'))"},
{"id":"DT-CIUS-PT-020_12.3","texto":"The BT-22 when prefixed with '#ENTITY@ATMPAYMENT-000#' must be unique.","categoria":"condicional","natureza":"RIR","gravidade":"erro","contexto":"//ubl:Invoice/cbc:Note | //cn:CreditNote/cbc:Note","elementos":["BT-22"],"expressao":"report (dispara quando verdadeiro): starts-with(normalize-space(.),$atm20_12) and $cnt20_12 > 1"},
{"id":"DT-CIUS-PT-020_12.4","texto":"The BT-22 when prefixed with '#ENTITY@ATMPAYMENT-000#' is mandatory an element with the prefix '#REFERENCE@ATMPAYMENT-000#'.","categoria":"condicional","natureza":"RIR","gravidade":"erro","contexto":"//ubl:Invoice/cbc:Note | //cn:CreditNote/cbc:Note","elementos":["BT-22"],"expressao":"report (dispara quando verdadeiro): starts-with(normalize-space(.),$atm20_12) and (every $note in (ancestor::ubl:Invoice/cbc:Note | ancestor::cn:CreditNote/cbc:Note) satisfies (not(starts-with(normalize-space($note),concat('#REFERENCE@ATMPAYMENT-',normalize-space(substring-before(substring-after(.,'#ENTITY@ATMPAYMENT-'),'#')),'#')))))"},
{"id":"DT-CIUS-PT-020_12.5","texto":"The BT-22 when prefixed with '#ENTITY@ATMPAYMENT-000#' is mandatory an element with the prefix '#AMOUNT@ATMPAYMENT-000#'.","categoria":"condicional","natureza":"RIR","gravidade":"erro","contexto":"//ubl:Invoice/cbc:Note | //cn:CreditNote/cbc:Note","elementos":["BT-22"],"expressao":"report (dispara quando verdadeiro): starts-with(normalize-space(.),$atm20_12) and (every $note in (ancestor::ubl:Invoice/cbc:Note | ancestor::cn:CreditNote/cbc:Note) satisfies (not(starts-with(normalize-space($note),concat('#AMOUNT@ATMPAYMENT-',normalize-space(substring-before(substring-after(.,'#ENTITY@ATMPAYMENT-'),'#')),'#')))))"},
{"id":"DT-CIUS-PT-020_13.1","texto":"The BT-22 does not meet the defined format: it is mandatory to prefix the value with the following '#REFERENCE@ATMPAYMENT-000#' and suffice with '#'. The sub-suffix \"-000\" must be used as a group of elements.","categoria":"formato","natureza":"RP","gravidade":"erro","contexto":"//ubl:Invoice/cbc:Note | //cn:CreditNote/cbc:Note","elementos":["BT-22"],"expressao":"report (dispara quando verdadeiro): starts-with(normalize-space(.),'#REFERENCE@ATMPAYMENT-') and not(matches(.,'^(#(REFERENCE@ATMPAYMENT)-([0-9]{3})#(.+)#)$'))"},
{"id":"DT-CIUS-PT-020_13.2","texto":"The BT-22 when prefixed with '#REFERENCE@ATMPAYMENT-000#', have to meet the defined format: alphanumeric with size between 1 and 20.","categoria":"condicional","natureza":"RIR","gravidade":"erro","contexto":"//ubl:Invoice/cbc:Note | //cn:CreditNote/cbc:Note","elementos":["BT-22"],"expressao":"report (dispara quando verdadeiro): starts-with(normalize-space(.),'#REFERENCE@ATMPAYMENT-') and not(matches(normalize-space(substring-before(substring-after(.,$atm20_13),'#')),'^(.{1,20})$'))"},
{"id":"DT-CIUS-PT-020_13.3","texto":"The BT-22 when prefixed with '#REFERENCE@ATMPAYMENT-000#' must be unique.","categoria":"condicional","natureza":"RIR","gravidade":"erro","contexto":"//ubl:Invoice/cbc:Note | //cn:CreditNote/cbc:Note","elementos":["BT-22"],"expressao":"report (dispara quando verdadeiro): starts-with(normalize-space(.),$atm20_13) and $cnt20_13 > 1"},
{"id":"DT-CIUS-PT-020_13.4","texto":"The BT-22 when prefixed with '#REFERENCE@ATMPAYMENT-000#' is mandatory an element with the prefix '#ENTITY@ATMPAYMENT-000#'.","categoria":"condicional","natureza":"RIR","gravidade":"erro","contexto":"//ubl:Invoice/cbc:Note | //cn:CreditNote/cbc:Note","elementos":["BT-22"],"expressao":"report (dispara quando verdadeiro): starts-with(normalize-space(.),$atm20_13) and (every $note in (ancestor::ubl:Invoice/cbc:Note | ancestor::cn:CreditNote/cbc:Note) satisfies (not(starts-with(normalize-space($note),concat('#ENTITY@ATMPAYMENT-',normalize-space(substring-before(substring-after(.,'#REFERENCE@ATMPAYMENT-'),'#')),'#')))))"},
{"id":"DT-CIUS-PT-020_13.5","texto":"The BT-22 when prefixed with '#REFERENCE@ATMPAYMENT-000#' is mandatory an element with the prefix '#AMOUNT@ATMPAYMENT-000#'.","categoria":"condicional","natureza":"RIR","gravidade":"erro","contexto":"//ubl:Invoice/cbc:Note | //cn:CreditNote/cbc:Note","elementos":["BT-22"],"expressao":"report (dispara quando verdadeiro): starts-with(normalize-space(.),$atm20_13) and (every $note in (ancestor::ubl:Invoice/cbc:Note | ancestor::cn:CreditNote/cbc:Note) satisfies (not(starts-with(normalize-space($note),concat('#AMOUNT@ATMPAYMENT-',normalize-space(substring-before(substring-after(.,'#REFERENCE@ATMPAYMENT-'),'#')),'#')))))"},
{"id":"DT-CIUS-PT-020_14.1","texto":"The BT-22 does not meet the defined format: it is mandatory to prefix the value with the following '#AMOUNT@ATMPAYMENT-000#' and suffice with '#'. The sub-suffix \"-000\" must be used as a group of elements.","categoria":"formato","natureza":"RP","gravidade":"erro","contexto":"//ubl:Invoice/cbc:Note | //cn:CreditNote/cbc:Note","elementos":["BT-22"],"expressao":"report (dispara quando verdadeiro): starts-with(normalize-space(.),'#AMOUNT@ATMPAYMENT-') and not(matches(.,'^(#(AMOUNT@ATMPAYMENT)-([0-9]{3})#(.+)#)$'))"},
{"id":"DT-CIUS-PT-020_14.2","texto":"The BT-22 when prefixed with '#AMOUNT@ATMPAYMENT-000#', have to meet the defined format: decimal value with 2 decimal places and 13 unit places.","categoria":"condicional","natureza":"RIR","gravidade":"erro","contexto":"//ubl:Invoice/cbc:Note | //cn:CreditNote/cbc:Note","elementos":["BT-22"],"expressao":"report (dispara quando verdadeiro): starts-with(normalize-space(.),'#AMOUNT@ATMPAYMENT-') and not(matches(normalize-space(substring-before(substring-after(.,$atm20_14),'#')),'^([0-9]{1,13}.[0-9]{2})$'))"},
{"id":"DT-CIUS-PT-020_14.3","texto":"The BT-22 when prefixed with '#AMOUNT@ATMPAYMENT-000#' must be unique.","categoria":"condicional","natureza":"RIR","gravidade":"erro","contexto":"//ubl:Invoice/cbc:Note | //cn:CreditNote/cbc:Note","elementos":["BT-22"],"expressao":"report (dispara quando verdadeiro): starts-with(normalize-space(.),$atm20_14) and $cnt20_14 > 1"},
{"id":"DT-CIUS-PT-020_14.4","texto":"The BT-22 when prefixed with '#AMOUNT@ATMPAYMENT-000#' is mandatory an element with the prefix '#ENTITY@ATMPAYMENT-000#'.","categoria":"condicional","natureza":"RIR","gravidade":"erro","contexto":"//ubl:Invoice/cbc:Note | //cn:CreditNote/cbc:Note","elementos":["BT-22"],"expressao":"report (dispara quando verdadeiro): starts-with(normalize-space(.),$atm20_14) and (every $note in (ancestor::ubl:Invoice/cbc:Note | ancestor::cn:CreditNote/cbc:Note) satisfies (not(starts-with(normalize-space($note),concat('#ENTITY@ATMPAYMENT-',normalize-space(substring-before(substring-after(.,'#AMOUNT@ATMPAYMENT-'),'#')),'#')))))"},
{"id":"DT-CIUS-PT-020_14.5","texto":"The BT-22 when prefixed with '#AMOUNT@ATMPAYMENT-000#' is mandatory an element with the prefix '#REFERENCE@ATMPAYMENT-000#'.","categoria":"condicional","natureza":"RIR","gravidade":"erro","contexto":"//ubl:Invoice/cbc:Note | //cn:CreditNote/cbc:Note","elementos":["BT-22"],"expressao":"report (dispara quando verdadeiro): starts-with(normalize-space(.),$atm20_14) and (every $note in (ancestor::ubl:Invoice/cbc:Note | ancestor::cn:CreditNote/cbc:Note) satisfies (not(starts-with(normalize-space($note),concat('#REFERENCE@ATMPAYMENT-',normalize-space(substring-before(substring-after(.,'#AMOUNT@ATMPAYMENT-'),'#')),'#')))))"},
{"id":"DT-CIUS-PT-020_15.1","texto":"The BT-22 does not meet the defined format: it is mandatory to prefix the value with the following '#DESCRIPTION@ATMPAYMENT-000#' and suffice with '#'. The sub-suffix \"-000\" must be used as a group of elements.","categoria":"formato","natureza":"RP","gravidade":"erro","contexto":"//ubl:Invoice/cbc:Note | //cn:CreditNote/cbc:Note","elementos":["BT-22"],"expressao":"report (dispara quando verdadeiro): starts-with(normalize-space(.),'#DESCRIPTION@ATMPAYMENT-') and not(matches(.,'^(#(DESCRIPTION@ATMPAYMENT)-([0-9]{3})#(.+)#)$'))"},
{"id":"DT-CIUS-PT-020_15.2","texto":"The BT-22 when prefixed with '#DESCRIPTION@ATMPAYMENT-000#', have to meet the defined format: alphanumeric with size between 1 and 150.","categoria":"condicional","natureza":"RIR","gravidade":"erro","contexto":"//ubl:Invoice/cbc:Note | //cn:CreditNote/cbc:Note","elementos":["BT-22"],"expressao":"report (dispara quando verdadeiro): starts-with(normalize-space(.),'#DESCRIPTION@ATMPAYMENT-') and not(matches(normalize-space(substring-before(substring-after(.,$atm20_15),'#')),'^(.{1,150})$'))"},
{"id":"DT-CIUS-PT-020_15.3","texto":"The BT-22 when prefixed with '#DESCRIPTION@ATMPAYMENT-000#' must be unique.","categoria":"condicional","natureza":"RIR","gravidade":"erro","contexto":"//ubl:Invoice/cbc:Note | //cn:CreditNote/cbc:Note","elementos":["BT-22"],"expressao":"report (dispara quando verdadeiro): starts-with(normalize-space(.),$atm20_15) and $cnt20_15 > 1"},
{"id":"DT-CIUS-PT-020_15.4","texto":"The BT-22 when prefixed with '#DESCRIPTION@ATMPAYMENT-000#' is mandatory an element with the prefix '#ENTITY@ATMPAYMENT-000#'.","categoria":"condicional","natureza":"RIR","gravidade":"erro","contexto":"//ubl:Invoice/cbc:Note | //cn:CreditNote/cbc:Note","elementos":["BT-22"],"expressao":"report (dispara quando verdadeiro): starts-with(normalize-space(.),$atm20_15) and (every $note in (ancestor::ubl:Invoice/cbc:Note | ancestor::cn:CreditNote/cbc:Note) satisfies (not(starts-with(normalize-space($note),concat('#ENTITY@ATMPAYMENT-',normalize-space(substring-before(substring-after(.,'#DESCRIPTION@ATMPAYMENT-'),'#')),'#')))))"},
{"id":"DT-CIUS-PT-020_15.5","texto":"The BT-22 when prefixed with '#DESCRIPTION@ATMPAYMENT-000#' is mandatory an element with the prefix '#REFERENCE@ATMPAYMENT-000#'.","categoria":"condicional","natureza":"RIR","gravidade":"erro","contexto":"//ubl:Invoice/cbc:Note | //cn:CreditNote/cbc:Note","elementos":["BT-22"],"expressao":"report (dispara quando verdadeiro): starts-with(normalize-space(.),$atm20_15) and (every $note in (ancestor::ubl:Invoice/cbc:Note | ancestor::cn:CreditNote/cbc:Note) satisfies (not(starts-with(normalize-space($note),concat('#REFERENCE@ATMPAYMENT-',normalize-space(substring-before(substring-after(.,'#DESCRIPTION@ATMPAYMENT-'),'#')),'#')))))"},
{"id":"DT-CIUS-PT-020_15.6","texto":"The BT-22 when prefixed with '#DESCRIPTION@ATMPAYMENT-000#' is mandatory an element with the prefix '#AMOUNT@ATMPAYMENT-000#'.","categoria":"condicional","natureza":"RIR","gravidade":"erro","contexto":"//ubl:Invoice/cbc:Note | //cn:CreditNote/cbc:Note","elementos":["BT-22"],"expressao":"report (dispara quando verdadeiro): starts-with(normalize-space(.),$atm20_15) and (every $note in (ancestor::ubl:Invoice/cbc:Note | ancestor::cn:CreditNote/cbc:Note) satisfies (not(starts-with(normalize-space($note),concat('#AMOUNT@ATMPAYMENT-',normalize-space(substring-before(substring-after(.,'#DESCRIPTION@ATMPAYMENT-'),'#')),'#')))))"},
{"id":"DT-CIUS-PT-021","texto":"The BT-23 does not meet the defined format: alphanumeric with size between 1 and 50.","categoria":"formato","natureza":"RP","gravidade":"erro","contexto":"//ubl:Invoice/cbc:ProfileID | //cn:CreditNote/cbc:ProfileID","elementos":["BT-23"],"expressao":"matches(.,'^(.{1,50})$')"},
{"id":"DT-CIUS-PT-022","texto":"The BT-24 only allows the following value: urn:cen.eu:en16931:2017#compliant#urn:feap.gov.pt:CIUS-PT: followed by the version identifier.","categoria":"valores","natureza":"RP","gravidade":"erro","contexto":"//ubl:Invoice/cbc:CustomizationID | //cn:CreditNote/cbc:CustomizationID","elementos":["BT-24"],"expressao":"matches(.,'^urn:cen.eu:en16931:2017#compliant#urn:feap.gov.pt:CIUS-PT:(.{1,10})$')"},
{"id":"DT-CIUS-PT-023","texto":"The BT-25 does not meet the defined format: alphanumeric with size between 1 and 50.","categoria":"formato","natureza":"RP","gravidade":"erro","contexto":"//ubl:Invoice/cac:BillingReference/cac:InvoiceDocumentReference/cbc:ID | //cn:CreditNote/cac:BillingReference/cac:InvoiceDocumentReference/cbc:ID","elementos":["BT-25"],"expressao":"matches(.,'^(.{1,50})$')"},
{"id":"DT-CIUS-PT-024","texto":"The BT-26 does not meet the defined format: YYYY-MM-DD.","categoria":"formato","natureza":"RP","gravidade":"erro","contexto":"//ubl:Invoice/cac:BillingReference/cac:InvoiceDocumentReference/cbc:IssueDate | //cn:CreditNote/cac:BillingReference/cac:InvoiceDocumentReference/cbc:IssueDate","elementos":["BT-26"],"expressao":"matches(.,'^((\\d{4})-(\\d{2})-(\\d{2}))$')"},
{"id":"DT-CIUS-PT-025","texto":"The BT-27 does not meet the defined format: alphanumeric with size between 1 and 200.","categoria":"formato","natureza":"RP","gravidade":"erro","contexto":"//ubl:Invoice/cac:AccountingSupplierParty/cac:Party/cac:PartyLegalEntity/cbc:RegistrationName | //cn:CreditNote/cac:AccountingSupplierParty/cac:Party/cac:PartyLegalEntity/cbc:RegistrationName","elementos":["BT-27"],"expressao":"matches(.,'^(.{1,200})$')"},
{"id":"DT-CIUS-PT-026","texto":"The BT-28 does not meet the defined format: alphanumeric with size between 1 and 200.","categoria":"formato","natureza":"RP","gravidade":"erro","contexto":"//ubl:Invoice/cac:AccountingSupplierParty/cac:Party/cac:PartyName/cbc:Name | //cn:CreditNote/cac:AccountingSupplierParty/cac:Party/cac:PartyName/cbc:Name","elementos":["BT-28"],"expressao":"matches(.,'^(.{1,200})$')"},
{"id":"DT-CIUS-PT-027.1","texto":"The BT-29 and BT-90 does not meet the defined format: alphanumeric with size between 1 and 50.","categoria":"formato","natureza":"RP","gravidade":"erro","contexto":"//ubl:Invoice/cac:AccountingSupplierParty/cac:Party/cac:PartyIdentification/cbc:ID | //cn:CreditNote/cac:AccountingSupplierParty/cac:Party/cac:PartyIdentification/cbc:ID","elementos":["BT-29","BT-90"],"expressao":"matches(.,'^(.{1,50})$')"},
{"id":"DT-CIUS-PT-027.2","texto":"The BT-29 and BT-90 identification scheme identifier must be coded using one of the ISO 6523 ICD list or SEPA.","categoria":"outra","natureza":"?","gravidade":"erro","contexto":"//ubl:Invoice/cac:AccountingSupplierParty/cac:Party/cac:PartyIdentification/cbc:ID | //cn:CreditNote/cac:AccountingSupplierParty/cac:Party/cac:PartyIdentification/cbc:ID","elementos":["BT-29","BT-90"],"expressao":"report (dispara quando verdadeiro): (exists(@schemeID) and (contains(normalize-space(@schemeID), ' ') or not(contains(' 0001 0002 0003 0004 0005 0006 0007 0008 0009 0010 0011 0012 0013 0014 0015 0016 0017 0018 0019 0020 0021 0022 0023 0024 0025 0026 0027 0028 0029 0030 0031 0032 0033 0034 0035 0036 0037 0038 0039 0040 0041 0042 0043 0044 0045 0046 0047 0048 0049 0050 0051 0052 0053 0054 0055 0056 0057 0058 0059 0060 0061 0062 0063 0064 0065 0066 0067 0068 0069 0070 0071 0072 0073 0074 0075 0076 0077 0078 0079 0080 0081 0082 0083 0084 0085 0086 0087 0088 0089 0090 0091 0092 0093 0094 0095 0096 0097 0098 0099 0100 0101 0102 0103 0104 0105 0106 0107 0108 0109 0110 0111 0112 0113 0114 0115 0116 0117 0118 0119 0120 0121 0122 0123 0124 0125 0126 0127 0128 0129 0130 0131 0132 0133 0134 0135 0136 0137 0138 0139 0140 0141 0142 0143 0144 0145 0146 0147 0148 0149 0150 0151 0152 0153 0154 0155 0156 0157 0158 0159 0160 0161 0162 0163 0164 0165 0166 0167 0168 0169 0170 0171 0172 0173 0174 0175 0176 0177 0178 0179 0180 0183 0184 0191 0192 SEPA ', concat(' ', normalize-space(@schemeID), ' ')))))"},
{"id":"DT-CIUS-PT-028.1","texto":"The BT-30 does not meet the defined format: alphanumeric with size between 1 and 200.","categoria":"formato","natureza":"RP","gravidade":"erro","contexto":"//ubl:Invoice/cac:AccountingSupplierParty/cac:Party/cac:PartyLegalEntity/cbc:CompanyID | //cn:CreditNote/cac:AccountingSupplierParty/cac:Party/cac:PartyLegalEntity/cbc:CompanyID","elementos":["BT-30"],"expressao":"matches(.,'^(.{1,200})$')"},
{"id":"DT-CIUS-PT-028.2","texto":"The BT-30 identification scheme identifier MUST be coded using one of the ISO 6523 ICD list.","categoria":"outra","natureza":"?","gravidade":"erro","contexto":"//ubl:Invoice/cac:AccountingSupplierParty/cac:Party/cac:PartyLegalEntity/cbc:CompanyID | //cn:CreditNote/cac:AccountingSupplierParty/cac:Party/cac:PartyLegalEntity/cbc:CompanyID","elementos":["BT-30"],"expressao":"report (dispara quando verdadeiro): (exists(@schemeID) and (contains(normalize-space(@schemeID), ' ') or not(contains(' 0001 0002 0003 0004 0005 0006 0007 0008 0009 0010 0011 0012 0013 0014 0015 0016 0017 0018 0019 0020 0021 0022 0023 0024 0025 0026 0027 0028 0029 0030 0031 0032 0033 0034 0035 0036 0037 0038 0039 0040 0041 0042 0043 0044 0045 0046 0047 0048 0049 0050 0051 0052 0053 0054 0055 0056 0057 0058 0059 0060 0061 0062 0063 0064 0065 0066 0067 0068 0069 0070 0071 0072 0073 0074 0075 0076 0077 0078 0079 0080 0081 0082 0083 0084 0085 0086 0087 0088 0089 0090 0091 0092 0093 0094 0095 0096 0097 0098 0099 0100 0101 0102 0103 0104 0105 0106 0107 0108 0109 0110 0111 0112 0113 0114 0115 0116 0117 0118 0119 0120 0121 0122 0123 0124 0125 0126 0127 0128 0129 0130 0131 0132 0133 0134 0135 0136 0137 0138 0139 0140 0141 0142 0143 0144 0145 0146 0147 0148 0149 0150 0151 0152 0153 0154 0155 0156 0157 0158 0159 0160 0161 0162 0163 0164 0165 0166 0167 0168 0169 0170 0171 0172 0173 0174 0175 0176 0177 0178 0179 0180 0183 0184 0191 0192 ', concat(' ', normalize-space(@schemeID), ' ')))))"},
{"id":"DT-CIUS-PT-029","texto":"The BT-31 does not meet the defined format: value preceded by the country code, according to ISO code list 3166-1.","categoria":"valores","natureza":"RP","gravidade":"erro","contexto":"//ubl:Invoice/cac:AccountingSupplierParty/cac:Party/cac:PartyTaxScheme/cbc:CompanyID | //cn:CreditNote/cac:AccountingSupplierParty/cac:Party/cac:PartyTaxScheme/cbc:CompanyID","elementos":["BT-31"],"expressao":"((not(contains(substring(normalize-space(.),0,3), ' ')) and contains(' AD AE AF AG AI AL AM AN AO AQ AR AS AT AU AW AX AZ BA BB BD BE BF BG BH BI BL BJ BM BN BO BR BS BT BV BW BY BZ CA CC CD CF CG CH CI CK CL CM CN CO CR CU CV CX CY CZ DE DJ DK DM DO DZ EC EE EG EH ER ES ET FI FJ FK FM FO FR GA GB GD GE GF GG GH GI GL GM GN GP GQ GR GS GT GU GW GY HK HM HN HR HT HU ID IE IL IM IN IO IQ IR IS IT JE JM JO JP KE KG KH KI KM KN KP KR KW KY KZ LA LB LC LI LK LR LS LT LU LV LY MA MC MD ME MF MG MH MK ML MM MN MO MP MQ MR MS MT MU MV MW MX MY MZ NA NC NE NF NG NI NL NO NP NR NU NZ OM PA PE PF PG PH PK PL PM PN PR PS PT PW PY QA RO RS RU RW SA SB SC SD SE SG SH SI SJ SK SL SM SN SO SR ST SV SY SZ TC TD TF TG TH TJ TK TL TM TN TO TR TT TV TW TZ UA UG UM US UY UZ VA VC VE VG VI VN VU WF WS YE YT ZA ZM ZW ', concat(' ', substring(normalize-space(.),0,3), ' '))))"},
{"id":"DT-CIUS-PT-030","texto":"The BT-32 does not meet the defined format: alphanumeric with size between 1 and 50.","categoria":"formato","natureza":"RP","gravidade":"erro","contexto":"//ubl:Invoice/cac:AccountingSupplierParty/cac:Party/cac:PartyTaxScheme/cbc:CompanyID | //cn:CreditNote/cac:AccountingSupplierParty/cac:Party/cac:PartyTaxScheme/cbc:CompanyID","elementos":["BT-32"],"expressao":"matches(.,'^(.{1,50})$')"},
{"id":"DT-CIUS-PT-031","texto":"The BT-33 does not meet the defined format: alphanumeric with size between 1 and 200.","categoria":"formato","natureza":"RP","gravidade":"erro","contexto":"//ubl:Invoice/cac:AccountingSupplierParty/cac:Party/cac:PartyLegalEntity/cbc:CompanyLegalForm | //cn:CreditNote/cac:AccountingSupplierParty/cac:Party/cac:PartyLegalEntity/cbc:CompanyLegalForm","elementos":["BT-33"],"expressao":"matches(.,'^(.{1,200})$')"},
{"id":"DT-CIUS-PT-032.1","texto":"The BT-34 does not meet the defined format: alphanumeric with size between 1 and 50.","categoria":"formato","natureza":"RP","gravidade":"erro","contexto":"//ubl:Invoice/cac:AccountingSupplierParty/cac:Party/cbc:EndpointID | //cn:CreditNote/cac:AccountingSupplierParty/cac:Party/cbc:EndpointID","elementos":["BT-34"],"expressao":"matches(.,'^(.{1,50})$')"},
{"id":"DT-CIUS-PT-032.2","texto":"The BT-34 identification scheme identifier does not meet the defined format: alphanumeric with size between 1 and 20.","categoria":"formato","natureza":"RP","gravidade":"erro","contexto":"//ubl:Invoice/cac:AccountingSupplierParty/cac:Party/cbc:EndpointID | //cn:CreditNote/cac:AccountingSupplierParty/cac:Party/cbc:EndpointID","elementos":["BT-34"],"expressao":"report (dispara quando verdadeiro): (exists(@schemeID) and not(matches(@schemeID,'^(.{1,20})$')))"},
{"id":"DT-CIUS-PT-033","texto":"The BT-35 does not meet the defined format: alphanumeric with size between 1 and 200.","categoria":"formato","natureza":"RP","gravidade":"erro","contexto":"//ubl:Invoice/cac:AccountingSupplierParty/cac:Party/cac:PostalAddress/cbc:StreetName | //cn:CreditNote/cac:AccountingSupplierParty/cac:Party/cac:PostalAddress/cbc:StreetName","elementos":["BT-35"],"expressao":"matches(.,'^(.{1,200})$')"},
{"id":"DT-CIUS-PT-034","texto":"The BT-36 does not meet the defined format: alphanumeric with size between 1 and 200.","categoria":"formato","natureza":"RP","gravidade":"erro","contexto":"//ubl:Invoice/cac:AccountingSupplierParty/cac:Party/cac:PostalAddress/cbc:AdditionalStreetName | //cn:CreditNote/cac:AccountingSupplierParty/cac:Party/cac:PostalAddress/cbc:AdditionalStreetName","elementos":["BT-36"],"expressao":"matches(.,'^(.{1,200})$')"},
{"id":"DT-CIUS-PT-035","texto":"The BT-162 does not meet the defined format: alphanumeric with size between 1 and 200.","categoria":"formato","natureza":"RP","gravidade":"erro","contexto":"//ubl:Invoice/cac:AccountingSupplierParty/cac:Party/cac:PostalAddress/cac:AddressLine/cbc:Line | //cn:CreditNote/cac:AccountingSupplierParty/cac:Party/cac:PostalAddress/cac:AddressLine/cbc:Line","elementos":["BT-162"],"expressao":"matches(.,'^(.{1,200})$')"},
{"id":"DT-CIUS-PT-036","texto":"The BT-37 does not meet the defined format: alphanumeric with size between 1 and 200.","categoria":"formato","natureza":"RP","gravidade":"erro","contexto":"//ubl:Invoice/cac:AccountingSupplierParty/cac:Party/cac:PostalAddress/cbc:CityName | //cn:CreditNote/cac:AccountingSupplierParty/cac:Party/cac:PostalAddress/cbc:CityName","elementos":["BT-37"],"expressao":"matches(.,'^(.{1,200})$')"},
{"id":"DT-CIUS-PT-037","texto":"The BT-38 does not meet the defined format: alphanumeric with size between 1 and 200.","categoria":"formato","natureza":"RP","gravidade":"erro","contexto":"//ubl:Invoice/cac:AccountingSupplierParty/cac:Party/cac:PostalAddress/cbc:PostalZone | //cn:CreditNote/cac:AccountingSupplierParty/cac:Party/cac:PostalAddress/cbc:PostalZone","elementos":["BT-38"],"expressao":"matches(.,'^(.{1,200})$')"},
{"id":"DT-CIUS-PT-038","texto":"The BT-39 does not meet the defined format: alphanumeric with size between 1 and 200.","categoria":"formato","natureza":"RP","gravidade":"erro","contexto":"//ubl:Invoice/cac:AccountingSupplierParty/cac:Party/cac:PostalAddress/cbc:CountrySubentity | //cn:CreditNote/cac:AccountingSupplierParty/cac:Party/cac:PostalAddress/cbc:CountrySubentity","elementos":["BT-39"],"expressao":"matches(.,'^(.{1,200})$')"},
{"id":"DT-CIUS-PT-141","texto":"The BT-40 must be coded using ISO code list 3166-1.","categoria":"valores","natureza":"RP","gravidade":"erro","contexto":"//ubl:Invoice/cac:AccountingSupplierParty/cac:Party/cac:PostalAddress/cac:Country/cbc:IdentificationCode | //cn:CreditNote/cac:AccountingSupplierParty/cac:Party/cac:PostalAddress/cac:Country/cbc:IdentificationCode","elementos":["BT-40"],"expressao":"(not(contains(normalize-space(.), ' ')) and contains(' AD AE AF AG AI AL AM AN AO AQ AR AS AT AU AW AX AZ BA BB BD BE BF BG BH BI BL BJ BM BN BO BR BS BT BV BW BY BZ CA CC CD CF CG CH CI CK CL CM CN CO CR CU CV CX CY CZ DE DJ DK DM DO DZ EC EE EG EH ER ES ET FI FJ FK FM FO FR GA GB GD GE GF GG GH GI GL GM GN GP GQ GR GS GT GU GW GY HK HM HN HR HT HU ID IE IL IM IN IO IQ IR IS IT JE JM JO JP KE KG KH KI KM KN KP KR KW KY KZ LA LB LC LI LK LR LS LT LU LV LY MA MC MD ME MF MG MH MK ML MM MN MO MP MQ MR MS MT MU MV MW MX MY MZ NA NC NE NF NG NI NL NO NP NR NU NZ OM PA PE PF PG PH PK PL PM PN PR PS PT PW PY QA RO RS RU RW SA SB SC SD SE SG SH SI SJ SK SL SM SN SO SR ST SV SY SZ TC TD TF TG TH TJ TK TL TM TN TO TR TT TV TW TZ UA UG UM US UY UZ VA VC VE VG VI VN VU WF WS YE YT ZA ZM ZW ', concat(' ', normalize-space(.), ' ')))"},
{"id":"DT-CIUS-PT-039","texto":"The BT-41 does not meet the defined format: alphanumeric with size between 1 and 200.","categoria":"formato","natureza":"RP","gravidade":"erro","contexto":"//ubl:Invoice/cac:AccountingSupplierParty/cac:Party/cac:Contact/cbc:Name | //cn:CreditNote/cac:AccountingSupplierParty/cac:Party/cac:Contact/cbc:Name","elementos":["BT-41"],"expressao":"matches(.,'^(.{1,200})$')"},
{"id":"DT-CIUS-PT-040","texto":"The BT-42 does not meet the defined format: alphanumeric with size between 1 and 200.","categoria":"formato","natureza":"RP","gravidade":"erro","contexto":"//ubl:Invoice/cac:AccountingSupplierParty/cac:Party/cac:Contact/cbc:Telephone | //cn:CreditNote/cac:AccountingSupplierParty/cac:Party/cac:Contact/cbc:Telephone","elementos":["BT-42"],"expressao":"matches(.,'^(.{1,200})$')"},
{"id":"DT-CIUS-PT-041","texto":"The BT-43 does not meet the defined format: alphanumeric with size between 1 and 200.","categoria":"formato","natureza":"RP","gravidade":"erro","contexto":"//ubl:Invoice/cac:AccountingSupplierParty/cac:Party/cac:Contact/cbc:ElectronicMail | //cn:CreditNote/cac:AccountingSupplierParty/cac:Party/cac:Contact/cbc:ElectronicMail","elementos":["BT-43"],"expressao":"matches(.,'^(.{1,200})$')"},
{"id":"DT-CIUS-PT-042","texto":"The BT-44 does not meet the defined format: alphanumeric with size between 1 and 200.","categoria":"formato","natureza":"RP","gravidade":"erro","contexto":"//ubl:Invoice/cac:AccountingCustomerParty/cac:Party/cac:PartyLegalEntity/cbc:RegistrationName | //cn:CreditNote/cac:AccountingCustomerParty/cac:Party/cac:PartyLegalEntity/cbc:RegistrationName","elementos":["BT-44"],"expressao":"matches(.,'^(.{1,200})$')"},
{"id":"DT-CIUS-PT-043","texto":"The BT-45 does not meet the defined format: alphanumeric with size between 1 and 200.","categoria":"formato","natureza":"RP","gravidade":"erro","contexto":"//ubl:Invoice/cac:AccountingCustomerParty/cac:Party/cac:PartyName/cbc:Name | //cn:CreditNote/cac:AccountingCustomerParty/cac:Party/cac:PartyName/cbc:Name","elementos":["BT-45"],"expressao":"matches(.,'^(.{1,200})$')"},
{"id":"DT-CIUS-PT-044.1","texto":"The BT-46 does not meet the defined format: alphanumeric with size between 1 and 50.","categoria":"formato","natureza":"RP","gravidade":"erro","contexto":"//ubl:Invoice/cac:AccountingCustomerParty/cac:Party/cac:PartyIdentification/cbc:ID | //cn:CreditNote/cac:AccountingCustomerParty/cac:Party/cac:PartyIdentification/cbc:ID","elementos":["BT-46"],"expressao":"matches(.,'^(.{1,50})$')"},
{"id":"DT-CIUS-PT-044.2","texto":"The BT-46 identification scheme identifier MUST be coded using one of the ISO 6523 ICD list.","categoria":"outra","natureza":"?","gravidade":"erro","contexto":"//ubl:Invoice/cac:AccountingCustomerParty/cac:Party/cac:PartyIdentification/cbc:ID | //cn:CreditNote/cac:AccountingCustomerParty/cac:Party/cac:PartyIdentification/cbc:ID","elementos":["BT-46"],"expressao":"report (dispara quando verdadeiro): (exists(@schemeID) and (contains(normalize-space(@schemeID), ' ') or not(contains(' 0001 0002 0003 0004 0005 0006 0007 0008 0009 0010 0011 0012 0013 0014 0015 0016 0017 0018 0019 0020 0021 0022 0023 0024 0025 0026 0027 0028 0029 0030 0031 0032 0033 0034 0035 0036 0037 0038 0039 0040 0041 0042 0043 0044 0045 0046 0047 0048 0049 0050 0051 0052 0053 0054 0055 0056 0057 0058 0059 0060 0061 0062 0063 0064 0065 0066 0067 0068 0069 0070 0071 0072 0073 0074 0075 0076 0077 0078 0079 0080 0081 0082 0083 0084 0085 0086 0087 0088 0089 0090 0091 0092 0093 0094 0095 0096 0097 0098 0099 0100 0101 0102 0103 0104 0105 0106 0107 0108 0109 0110 0111 0112 0113 0114 0115 0116 0117 0118 0119 0120 0121 0122 0123 0124 0125 0126 0127 0128 0129 0130 0131 0132 0133 0134 0135 0136 0137 0138 0139 0140 0141 0142 0143 0144 0145 0146 0147 0148 0149 0150 0151 0152 0153 0154 0155 0156 0157 0158 0159 0160 0161 0162 0163 0164 0165 0166 0167 0168 0169 0170 0171 0172 0173 0174 0175 0176 0177 0178 0179 0180 0183 0184 0191 0192 SEPA ', concat(' ', normalize-space(@schemeID), ' ')))))"},
{"id":"DT-CIUS-PT-045.1","texto":"The BT-47 does not meet the defined format: alphanumeric with size between 1 and 50.","categoria":"formato","natureza":"RP","gravidade":"erro","contexto":"//ubl:Invoice/cac:AccountingCustomerParty/cac:Party/cac:PartyLegalEntity/cbc:CompanyID | //cn:CreditNote/cac:AccountingCustomerParty/cac:Party/cac:PartyLegalEntity/cbc:CompanyID","elementos":["BT-47"],"expressao":"matches(.,'^(.{1,50})$')"},
{"id":"DT-CIUS-PT-045.2","texto":"The BT-47 identification scheme identifier MUST be coded using one of the ISO 6523 ICD list.","categoria":"outra","natureza":"?","gravidade":"erro","contexto":"//ubl:Invoice/cac:AccountingCustomerParty/cac:Party/cac:PartyLegalEntity/cbc:CompanyID | //cn:CreditNote/cac:AccountingCustomerParty/cac:Party/cac:PartyLegalEntity/cbc:CompanyID","elementos":["BT-47"],"expressao":"report (dispara quando verdadeiro): (exists(@schemeID) and (contains(normalize-space(@schemeID), ' ') or not(contains(' 0001 0002 0003 0004 0005 0006 0007 0008 0009 0010 0011 0012 0013 0014 0015 0016 0017 0018 0019 0020 0021 0022 0023 0024 0025 0026 0027 0028 0029 0030 0031 0032 0033 0034 0035 0036 0037 0038 0039 0040 0041 0042 0043 0044 0045 0046 0047 0048 0049 0050 0051 0052 0053 0054 0055 0056 0057 0058 0059 0060 0061 0062 0063 0064 0065 0066 0067 0068 0069 0070 0071 0072 0073 0074 0075 0076 0077 0078 0079 0080 0081 0082 0083 0084 0085 0086 0087 0088 0089 0090 0091 0092 0093 0094 0095 0096 0097 0098 0099 0100 0101 0102 0103 0104 0105 0106 0107 0108 0109 0110 0111 0112 0113 0114 0115 0116 0117 0118 0119 0120 0121 0122 0123 0124 0125 0126 0127 0128 0129 0130 0131 0132 0133 0134 0135 0136 0137 0138 0139 0140 0141 0142 0143 0144 0145 0146 0147 0148 0149 0150 0151 0152 0153 0154 0155 0156 0157 0158 0159 0160 0161 0162 0163 0164 0165 0166 0167 0168 0169 0170 0171 0172 0173 0174 0175 0176 0177 0178 0179 0180 0183 0184 0191 0192 ', concat(' ', normalize-space(@schemeID), ' ')))))"},
{"id":"DT-CIUS-PT-046.1","texto":"The BT-48 does not meet the defined format: value preceded by the country code, according to ISO code list 3166-1.","categoria":"valores","natureza":"RP","gravidade":"erro","contexto":"//ubl:Invoice/cac:AccountingCustomerParty/cac:Party/cac:PartyTaxScheme/cbc:CompanyID | //cn:CreditNote/cac:AccountingCustomerParty/cac:Party/cac:PartyTaxScheme/cbc:CompanyID","elementos":["BT-48"],"expressao":"((not(contains(substring(normalize-space(.),0,3), ' ')) and contains(' AD AE AF AG AI AL AM AN AO AQ AR AS AT AU AW AX AZ BA BB BD BE BF BG BH BI BL BJ BM BN BO BR BS BT BV BW BY BZ CA CC CD CF CG CH CI CK CL CM CN CO CR CU CV CX CY CZ DE DJ DK DM DO DZ EC EE EG EH ER ES ET FI FJ FK FM FO FR GA GB GD GE GF GG GH GI GL GM GN GP GQ GR GS GT GU GW GY HK HM HN HR HT HU ID IE IL IM IN IO IQ IR IS IT JE JM JO JP KE KG KH KI KM KN KP KR KW KY KZ LA LB LC LI LK LR LS LT LU LV LY MA MC MD ME MF MG MH MK ML MM MN MO MP MQ MR MS MT MU MV MW MX MY MZ NA NC NE NF NG NI NL NO NP NR NU NZ OM PA PE PF PG PH PK PL PM PN PR PS PT PW PY QA RO RS RU RW SA SB SC SD SE SG SH SI SJ SK SL SM SN SO SR ST SV SY SZ TC TD TF TG TH TJ TK TL TM TN TO TR TT TV TW TZ UA UG UM US UY UZ VA VC VE VG VI VN VU WF WS YE YT ZA ZM ZW ', concat(' ', substring(normalize-space(.),0,3), ' '))))"},
{"id":"DT-CIUS-PT-046.2","texto":"The BT-48 does not meet the defined format: alphanumeric with size between 1 and 50.","categoria":"formato","natureza":"RP","gravidade":"erro","contexto":"//ubl:Invoice/cac:AccountingCustomerParty/cac:Party/cac:PartyTaxScheme/cbc:CompanyID | //cn:CreditNote/cac:AccountingCustomerParty/cac:Party/cac:PartyTaxScheme/cbc:CompanyID","elementos":["BT-48"],"expressao":"matches(.,'^(.{1,50})$')"},
{"id":"DT-CIUS-PT-047.1","texto":"The BT-49 does not meet the defined format: alphanumeric with size between 1 and 50.","categoria":"formato","natureza":"RP","gravidade":"erro","contexto":"//ubl:Invoice/cac:AccountingCustomerParty/cac:Party/cbc:EndpointID | //cn:CreditNote/cac:AccountingCustomerParty/cac:Party/cbc:EndpointID","elementos":["BT-49"],"expressao":"matches(.,'^(.{1,50})$')"},
{"id":"DT-CIUS-PT-047.2","texto":"The BT-49 identification scheme identifier does not meet the defined format: alphanumeric with size between 1 and 20.","categoria":"formato","natureza":"RP","gravidade":"erro","contexto":"//ubl:Invoice/cac:AccountingCustomerParty/cac:Party/cbc:EndpointID | //cn:CreditNote/cac:AccountingCustomerParty/cac:Party/cbc:EndpointID","elementos":["BT-49"],"expressao":"report (dispara quando verdadeiro): (exists(@schemeID) and not(matches(@schemeID,'^(.{1,20})$')))"},
{"id":"DT-CIUS-PT-048","texto":"The BT-50 does not meet the defined format: alphanumeric with size between 1 and 200.","categoria":"formato","natureza":"RP","gravidade":"erro","contexto":"//ubl:Invoice/cac:AccountingCustomerParty/cac:Party/cac:PostalAddress/cbc:StreetName | //cn:CreditNote/cac:AccountingCustomerParty/cac:Party/cac:PostalAddress/cbc:StreetName","elementos":["BT-50"],"expressao":"matches(.,'^(.{1,200})$')"},
{"id":"DT-CIUS-PT-049","texto":"The BT-51 does not meet the defined format: alphanumeric with size between 1 and 200.","categoria":"formato","natureza":"RP","gravidade":"erro","contexto":"//ubl:Invoice/cac:AccountingCustomerParty/cac:Party/cac:PostalAddress/cbc:AdditionalStreetName | //cn:CreditNote/cac:AccountingCustomerParty/cac:Party/cac:PostalAddress/cbc:AdditionalStreetName","elementos":["BT-51"],"expressao":"matches(.,'^(.{1,200})$')"},
{"id":"DT-CIUS-PT-050","texto":"The BT-163 does not meet the defined format: alphanumeric with size between 1 and 200.","categoria":"formato","natureza":"RP","gravidade":"erro","contexto":"//ubl:Invoice/cac:AccountingCustomerParty/cac:Party/cac:PostalAddress/cac:AddressLine/cbc:Line | //cn:CreditNote/cac:AccountingCustomerParty/cac:Party/cac:PostalAddress/cac:AddressLine/cbc:Line","elementos":["BT-163"],"expressao":"matches(.,'^(.{1,200})$')"},
{"id":"DT-CIUS-PT-051","texto":"The BT-52 does not meet the defined format: alphanumeric with size between 1 and 200.","categoria":"formato","natureza":"RP","gravidade":"erro","contexto":"//ubl:Invoice/cac:AccountingCustomerParty/cac:Party/cac:PostalAddress/cbc:CityName | //cn:CreditNote/cac:AccountingCustomerParty/cac:Party/cac:PostalAddress/cbc:CityName","elementos":["BT-52"],"expressao":"matches(.,'^(.{1,200})$')"},
{"id":"DT-CIUS-PT-052","texto":"The BT-53 does not meet the defined format: alphanumeric with size between 1 and 200.","categoria":"formato","natureza":"RP","gravidade":"erro","contexto":"//ubl:Invoice/cac:AccountingCustomerParty/cac:Party/cac:PostalAddress/cbc:PostalZone | //cn:CreditNote/cac:AccountingCustomerParty/cac:Party/cac:PostalAddress/cbc:PostalZone","elementos":["BT-53"],"expressao":"matches(.,'^(.{1,200})$')"},
{"id":"DT-CIUS-PT-053","texto":"The BT-54 does not meet the defined format: alphanumeric with size between 1 and 200.","categoria":"formato","natureza":"RP","gravidade":"erro","contexto":"//ubl:Invoice/cac:AccountingCustomerParty/cac:Party/cac:PostalAddress/cbc:CountrySubentity | //cn:CreditNote/cac:AccountingCustomerParty/cac:Party/cac:PostalAddress/cbc:CountrySubentity","elementos":["BT-54"],"expressao":"matches(.,'^(.{1,200})$')"},
{"id":"DT-CIUS-PT-142","texto":"The BT-55 must be coded using ISO code list 3166-1.","categoria":"valores","natureza":"RP","gravidade":"erro","contexto":"//ubl:Invoice/cac:AccountingCustomerParty/cac:Party/cac:PostalAddress/cac:Country/cbc:IdentificationCode | //cn:CreditNote/cac:AccountingCustomerParty/cac:Party/cac:PostalAddress/cac:Country/cbc:IdentificationCode","elementos":["BT-55"],"expressao":"((not(contains(normalize-space(.), ' ')) and contains(' AD AE AF AG AI AL AM AN AO AQ AR AS AT AU AW AX AZ BA BB BD BE BF BG BH BI BL BJ BM BN BO BR BS BT BV BW BY BZ CA CC CD CF CG CH CI CK CL CM CN CO CR CU CV CX CY CZ DE DJ DK DM DO DZ EC EE EG EH ER ES ET FI FJ FK FM FO FR GA GB GD GE GF GG GH GI GL GM GN GP GQ GR GS GT GU GW GY HK HM HN HR HT HU ID IE IL IM IN IO IQ IR IS IT JE JM JO JP KE KG KH KI KM KN KP KR KW KY KZ LA LB LC LI LK LR LS LT LU LV LY MA MC MD ME MF MG MH MK ML MM MN MO MP MQ MR MS MT MU MV MW MX MY MZ NA NC NE NF NG NI NL NO NP NR NU NZ OM PA PE PF PG PH PK PL PM PN PR PS PT PW PY QA RO RS RU RW SA SB SC SD SE SG SH SI SJ SK SL SM SN SO SR ST SV SY SZ TC TD TF TG TH TJ TK TL TM TN TO TR TT TV TW TZ UA UG UM US UY UZ VA VC VE VG VI VN VU WF WS YE YT ZA ZM ZW ', concat(' ', normalize-space(.), ' '))))"},
{"id":"DT-CIUS-PT-054","texto":"The BT-56 does not meet the defined format: alphanumeric with size between 1 and 200.","categoria":"formato","natureza":"RP","gravidade":"erro","contexto":"//ubl:Invoice/cac:AccountingCustomerParty/cac:Party/cac:Contact/cbc:Name | //cn:CreditNote/cac:AccountingCustomerParty/cac:Party/cac:Contact/cbc:Name","elementos":["BT-56"],"expressao":"matches(.,'^(.{1,200})$')"},
{"id":"DT-CIUS-PT-055","texto":"The BT-57 does not meet the defined format: alphanumeric with size between 1 and 200.","categoria":"formato","natureza":"RP","gravidade":"erro","contexto":"//ubl:Invoice/cac:AccountingCustomerParty/cac:Party/cac:Contact/cbc:Telephone | //cn:CreditNote/cac:AccountingCustomerParty/cac:Party/cac:Contact/cbc:Telephone","elementos":["BT-57"],"expressao":"matches(.,'^(.{1,200})$')"},
{"id":"DT-CIUS-PT-056","texto":"The BT-58 does not meet the defined format: alphanumeric with size between 1 and 200.","categoria":"formato","natureza":"RP","gravidade":"erro","contexto":"//ubl:Invoice/cac:AccountingCustomerParty/cac:Party/cac:Contact/cbc:ElectronicMail | //cn:CreditNote/cac:AccountingCustomerParty/cac:Party/cac:Contact/cbc:ElectronicMail","elementos":["BT-58"],"expressao":"matches(.,'^(.{1,200})$')"},
{"id":"DT-CIUS-PT-057","texto":"The BT-59 does not meet the defined format: alphanumeric with size between 1 and 200.","categoria":"formato","natureza":"RP","gravidade":"erro","contexto":"//ubl:Invoice/cac:PayeeParty/cac:PartyName/cbc:Name | //cn:CreditNote/cac:PayeeParty/cac:PartyName/cbc:Name","elementos":["BT-59"],"expressao":"matches(.,'^(.{1,200})$')"},
{"id":"DT-CIUS-PT-058.1","texto":"The BT-60 and BT-90 does not meet the defined format: alphanumeric with size between 1 and 50.","categoria":"formato","natureza":"RP","gravidade":"erro","contexto":"//ubl:Invoice/cac:PayeeParty/cac:PartyIdentification/cbc:ID | //cn:CreditNote/cac:PayeeParty/cac:PartyIdentification/cbc:ID","elementos":["BT-60","BT-90"],"expressao":"matches(.,'^(.{1,50})$')"},
{"id":"DT-CIUS-PT-058.2","texto":"The BT-60 and BT-90 identification scheme identifier MUST be coded using one of the ISO 6523 ICD list or SEPA.","categoria":"outra","natureza":"?","gravidade":"erro","contexto":"//ubl:Invoice/cac:PayeeParty/cac:PartyIdentification/cbc:ID | //cn:CreditNote/cac:PayeeParty/cac:PartyIdentification/cbc:ID","elementos":["BT-60","BT-90"],"expressao":"report (dispara quando verdadeiro): (exists(@schemeID) and (contains(normalize-space(@schemeID), ' ') or not(contains(' 0001 0002 0003 0004 0005 0006 0007 0008 0009 0010 0011 0012 0013 0014 0015 0016 0017 0018 0019 0020 0021 0022 0023 0024 0025 0026 0027 0028 0029 0030 0031 0032 0033 0034 0035 0036 0037 0038 0039 0040 0041 0042 0043 0044 0045 0046 0047 0048 0049 0050 0051 0052 0053 0054 0055 0056 0057 0058 0059 0060 0061 0062 0063 0064 0065 0066 0067 0068 0069 0070 0071 0072 0073 0074 0075 0076 0077 0078 0079 0080 0081 0082 0083 0084 0085 0086 0087 0088 0089 0090 0091 0092 0093 0094 0095 0096 0097 0098 0099 0100 0101 0102 0103 0104 0105 0106 0107 0108 0109 0110 0111 0112 0113 0114 0115 0116 0117 0118 0119 0120 0121 0122 0123 0124 0125 0126 0127 0128 0129 0130 0131 0132 0133 0134 0135 0136 0137 0138 0139 0140 0141 0142 0143 0144 0145 0146 0147 0148 0149 0150 0151 0152 0153 0154 0155 0156 0157 0158 0159 0160 0161 0162 0163 0164 0165 0166 0167 0168 0169 0170 0171 0172 0173 0174 0175 0176 0177 0178 0179 0180 0183 0184 0191 0192 SEPA ', concat(' ', normalize-space(@schemeID), ' ')))))"},
{"id":"DT-CIUS-PT-059.1","texto":"The BT-61 does not meet the defined format: alphanumeric with size between 1 and 50.","categoria":"formato","natureza":"RP","gravidade":"erro","contexto":"//ubl:Invoice/cac:PayeeParty/cac:PartyLegalEntity/cbc:CompanyID | //cn:CreditNote/cac:PayeeParty/cac:PartyLegalEntity/cbc:CompanyID","elementos":["BT-61"],"expressao":"matches(.,'^(.{1,50})$')"},
{"id":"DT-CIUS-PT-059.2","texto":"The BT-61 identification scheme identifier MUST be coded using one of the ISO 6523 ICD list.","categoria":"outra","natureza":"?","gravidade":"erro","contexto":"//ubl:Invoice/cac:PayeeParty/cac:PartyLegalEntity/cbc:CompanyID | //cn:CreditNote/cac:PayeeParty/cac:PartyLegalEntity/cbc:CompanyID","elementos":["BT-61"],"expressao":"report (dispara quando verdadeiro): (exists(@schemeID) and (contains(normalize-space(@schemeID), ' ') or not(contains(' 0001 0002 0003 0004 0005 0006 0007 0008 0009 0010 0011 0012 0013 0014 0015 0016 0017 0018 0019 0020 0021 0022 0023 0024 0025 0026 0027 0028 0029 0030 0031 0032 0033 0034 0035 0036 0037 0038 0039 0040 0041 0042 0043 0044 0045 0046 0047 0048 0049 0050 0051 0052 0053 0054 0055 0056 0057 0058 0059 0060 0061 0062 0063 0064 0065 0066 0067 0068 0069 0070 0071 0072 0073 0074 0075 0076 0077 0078 0079 0080 0081 0082 0083 0084 0085 0086 0087 0088 0089 0090 0091 0092 0093 0094 0095 0096 0097 0098 0099 0100 0101 0102 0103 0104 0105 0106 0107 0108 0109 0110 0111 0112 0113 0114 0115 0116 0117 0118 0119 0120 0121 0122 0123 0124 0125 0126 0127 0128 0129 0130 0131 0132 0133 0134 0135 0136 0137 0138 0139 0140 0141 0142 0143 0144 0145 0146 0147 0148 0149 0150 0151 0152 0153 0154 0155 0156 0157 0158 0159 0160 0161 0162 0163 0164 0165 0166 0167 0168 0169 0170 0171 0172 0173 0174 0175 0176 0177 0178 0179 0180 0183 0184 0191 0192 ', concat(' ', normalize-space(@schemeID), ' ')))))"},
{"id":"DT-CIUS-PT-060","texto":"The BT-62 does not meet the defined format: alphanumeric with size between 1 and 200.","categoria":"formato","natureza":"RP","gravidade":"erro","contexto":"//ubl:Invoice/cac:TaxRepresentativeParty/cac:PartyName/cbc:Name | //cn:CreditNote/cac:TaxRepresentativeParty/cac:PartyName/cbc:Name","elementos":["BT-62"],"expressao":"matches(.,'^(.{1,200})$')"},
{"id":"DT-CIUS-PT-061.1","texto":"The BT-63 does not meet the defined format: value preceded by the country code, according to ISO code list 3166-1.","categoria":"valores","natureza":"RP","gravidade":"erro","contexto":"//ubl:Invoice/cac:TaxRepresentativeParty/cac:PartyTaxScheme/cbc:CompanyID | //cn:CreditNote/cac:TaxRepresentativeParty/cac:PartyTaxScheme/cbc:CompanyID","elementos":["BT-63"],"expressao":"((not(contains(substring(normalize-space(.),0,3), ' ')) and contains(' AD AE AF AG AI AL AM AN AO AQ AR AS AT AU AW AX AZ BA BB BD BE BF BG BH BI BL BJ BM BN BO BR BS BT BV BW BY BZ CA CC CD CF CG CH CI CK CL CM CN CO CR CU CV CX CY CZ DE DJ DK DM DO DZ EC EE EG EH ER ES ET FI FJ FK FM FO FR GA GB GD GE GF GG GH GI GL GM GN GP GQ GR GS GT GU GW GY HK HM HN HR HT HU ID IE IL IM IN IO IQ IR IS IT JE JM JO JP KE KG KH KI KM KN KP KR KW KY KZ LA LB LC LI LK LR LS LT LU LV LY MA MC MD ME MF MG MH MK ML MM MN MO MP MQ MR MS MT MU MV MW MX MY MZ NA NC NE NF NG NI NL NO NP NR NU NZ OM PA PE PF PG PH PK PL PM PN PR PS PT PW PY QA RO RS RU RW SA SB SC SD SE SG SH SI SJ SK SL SM SN SO SR ST SV SY SZ TC TD TF TG TH TJ TK TL TM TN TO TR TT TV TW TZ UA UG UM US UY UZ VA VC VE VG VI VN VU WF WS YE YT ZA ZM ZW ', concat(' ', substring(normalize-space(.),0,3), ' '))))"},
{"id":"DT-CIUS-PT-061.2","texto":"The BT-63 does not meet the defined format: alphanumeric with size between 1 and 50.","categoria":"formato","natureza":"RP","gravidade":"erro","contexto":"//ubl:Invoice/cac:TaxRepresentativeParty/cac:PartyTaxScheme/cbc:CompanyID | //cn:CreditNote/cac:TaxRepresentativeParty/cac:PartyTaxScheme/cbc:CompanyID","elementos":["BT-63"],"expressao":"matches(.,'^(.{1,50})$')"},
{"id":"DT-CIUS-PT-062","texto":"The BT-64 does not meet the defined format: alphanumeric with size between 1 and 200.","categoria":"formato","natureza":"RP","gravidade":"erro","contexto":"//ubl:Invoice/cac:TaxRepresentativeParty/cac:PostalAddress/cbc:StreetName | //cn:CreditNote/cac:TaxRepresentativeParty/cac:PostalAddress/cbc:StreetName","elementos":["BT-64"],"expressao":"matches(.,'^(.{1,200})$')"},
{"id":"DT-CIUS-PT-063","texto":"The BT-65 does not meet the defined format: alphanumeric with size between 1 and 200.","categoria":"formato","natureza":"RP","gravidade":"erro","contexto":"//ubl:Invoice/cac:TaxRepresentativeParty/cac:PostalAddress/cbc:AdditionalStreetName | //cn:CreditNote/cac:TaxRepresentativeParty/cac:PostalAddress/cbc:AdditionalStreetName","elementos":["BT-65"],"expressao":"matches(.,'^(.{1,200})$')"},
{"id":"DT-CIUS-PT-064","texto":"The BT-164 does not meet the defined format: alphanumeric with size between 1 and 200.","categoria":"formato","natureza":"RP","gravidade":"erro","contexto":"//ubl:Invoice/cac:TaxRepresentativeParty/cac:PostalAddress/cac:AddressLine/cbc:Line | //cn:CreditNote/cac:TaxRepresentativeParty/cac:PostalAddress/cac:AddressLine/cbc:Line","elementos":["BT-164"],"expressao":"matches(.,'^(.{1,200})$')"},
{"id":"DT-CIUS-PT-065","texto":"The BT-66 does not meet the defined format: alphanumeric with size between 1 and 200.","categoria":"formato","natureza":"RP","gravidade":"erro","contexto":"//ubl:Invoice/cac:TaxRepresentativeParty/cac:PostalAddress/cbc:CityName | //cn:CreditNote/cac:TaxRepresentativeParty/cac:PostalAddress/cbc:CityName","elementos":["BT-66"],"expressao":"matches(.,'^(.{1,200})$')"},
{"id":"DT-CIUS-PT-066","texto":"The BT-67 does not meet the defined format: alphanumeric with size between 1 and 200.","categoria":"formato","natureza":"RP","gravidade":"erro","contexto":"//ubl:Invoice/cac:TaxRepresentativeParty/cac:PostalAddress/cbc:PostalZone | //cn:CreditNote/cac:TaxRepresentativeParty/cac:PostalAddress/cbc:PostalZone","elementos":["BT-67"],"expressao":"matches(.,'^(.{1,200})$')"},
{"id":"DT-CIUS-PT-067","texto":"The BT-68 does not meet the defined format: alphanumeric with size between 1 and 200.","categoria":"formato","natureza":"RP","gravidade":"erro","contexto":"//ubl:Invoice/cac:TaxRepresentativeParty/cac:PostalAddress/cbc:CountrySubentity | //cn:CreditNote/cac:TaxRepresentativeParty/cac:PostalAddress/cbc:CountrySubentity","elementos":["BT-68"],"expressao":"matches(.,'^(.{1,200})$')"},
{"id":"DT-CIUS-PT-144","texto":"The BT-69 must be coded using ISO code list 3166-1.","categoria":"valores","natureza":"RP","gravidade":"erro","contexto":"//ubl:Invoice/cac:TaxRepresentativeParty/cac:PostalAddress/cac:Country/cbc:IdentificationCode | //cn:CreditNote/cac:TaxRepresentativeParty/cac:PostalAddress/cac:Country/cbc:IdentificationCode","elementos":["BT-69"],"expressao":"((not(contains(normalize-space(.), ' ')) and contains(' AD AE AF AG AI AL AM AN AO AQ AR AS AT AU AW AX AZ BA BB BD BE BF BG BH BI BL BJ BM BN BO BR BS BT BV BW BY BZ CA CC CD CF CG CH CI CK CL CM CN CO CR CU CV CX CY CZ DE DJ DK DM DO DZ EC EE EG EH ER ES ET FI FJ FK FM FO FR GA GB GD GE GF GG GH GI GL GM GN GP GQ GR GS GT GU GW GY HK HM HN HR HT HU ID IE IL IM IN IO IQ IR IS IT JE JM JO JP KE KG KH KI KM KN KP KR KW KY KZ LA LB LC LI LK LR LS LT LU LV LY MA MC MD ME MF MG MH MK ML MM MN MO MP MQ MR MS MT MU MV MW MX MY MZ NA NC NE NF NG NI NL NO NP NR NU NZ OM PA PE PF PG PH PK PL PM PN PR PS PT PW PY QA RO RS RU RW SA SB SC SD SE SG SH SI SJ SK SL SM SN SO SR ST SV SY SZ TC TD TF TG TH TJ TK TL TM TN TO TR TT TV TW TZ UA UG UM US UY UZ VA VC VE VG VI VN VU WF WS YE YT ZA ZM ZW ', concat(' ', normalize-space(.), ' '))))"},
{"id":"DT-CIUS-PT-068","texto":"The BT-70 does not meet the defined format: alphanumeric with size between 1 and 200.","categoria":"formato","natureza":"RP","gravidade":"erro","contexto":"//ubl:Invoice/cac:Delivery/cac:DeliveryParty/cac:PartyName/cbc:Name | //cn:CreditNote/cac:Delivery/cac:DeliveryParty/cac:PartyName/cbc:Name","elementos":["BT-70"],"expressao":"matches(.,'^(.{1,200})$')"},
{"id":"DT-CIUS-PT-069.1","texto":"The BT-71 does not meet the defined format: alphanumeric with size between 1 and 50.","categoria":"formato","natureza":"RP","gravidade":"erro","contexto":"//ubl:Invoice/cac:Delivery/cac:DeliveryLocation/cbc:ID | //cn:CreditNote/cac:Delivery/cac:DeliveryLocation/cbc:ID","elementos":["BT-71"],"expressao":"matches(.,'^(.{1,50})$')"},
{"id":"DT-CIUS-PT-069.2","texto":"The BT-71 identification scheme identifier MUST be coded using one of the ISO 6523 ICD list.","categoria":"outra","natureza":"?","gravidade":"erro","contexto":"//ubl:Invoice/cac:Delivery/cac:DeliveryLocation/cbc:ID | //cn:CreditNote/cac:Delivery/cac:DeliveryLocation/cbc:ID","elementos":["BT-71"],"expressao":"report (dispara quando verdadeiro): (exists(@schemeID) and (contains(normalize-space(@schemeID), ' ') or not(contains(' 0001 0002 0003 0004 0005 0006 0007 0008 0009 0010 0011 0012 0013 0014 0015 0016 0017 0018 0019 0020 0021 0022 0023 0024 0025 0026 0027 0028 0029 0030 0031 0032 0033 0034 0035 0036 0037 0038 0039 0040 0041 0042 0043 0044 0045 0046 0047 0048 0049 0050 0051 0052 0053 0054 0055 0056 0057 0058 0059 0060 0061 0062 0063 0064 0065 0066 0067 0068 0069 0070 0071 0072 0073 0074 0075 0076 0077 0078 0079 0080 0081 0082 0083 0084 0085 0086 0087 0088 0089 0090 0091 0092 0093 0094 0095 0096 0097 0098 0099 0100 0101 0102 0103 0104 0105 0106 0107 0108 0109 0110 0111 0112 0113 0114 0115 0116 0117 0118 0119 0120 0121 0122 0123 0124 0125 0126 0127 0128 0129 0130 0131 0132 0133 0134 0135 0136 0137 0138 0139 0140 0141 0142 0143 0144 0145 0146 0147 0148 0149 0150 0151 0152 0153 0154 0155 0156 0157 0158 0159 0160 0161 0162 0163 0164 0165 0166 0167 0168 0169 0170 0171 0172 0173 0174 0175 0176 0177 0178 0179 0180 0183 0184 0191 0192 ', concat(' ', normalize-space(@schemeID), ' ')))))"},
{"id":"DT-CIUS-PT-070","texto":"The BT-72 does not meet the defined format: YYYY-MM-DD.","categoria":"formato","natureza":"RP","gravidade":"erro","contexto":"//ubl:Invoice/cac:Delivery/cbc:ActualDeliveryDate | //cn:CreditNote/cac:Delivery/cbc:ActualDeliveryDate","elementos":["BT-72"],"expressao":"matches(.,'^((\\d{4})-(\\d{2})-(\\d{2}))$')"},
{"id":"DT-CIUS-PT-071","texto":"The BT-73 does not meet the defined format: YYYY-MM-DD.","categoria":"formato","natureza":"RP","gravidade":"erro","contexto":"//ubl:Invoice/cac:InvoicePeriod/cbc:StartDate | //cn:CreditNote/cac:InvoicePeriod/cbc:StartDate","elementos":["BT-73"],"expressao":"matches(.,'^((\\d{4})-(\\d{2})-(\\d{2}))$')"},
{"id":"DT-CIUS-PT-072","texto":"The BT-74 does not meet the defined format: YYYY-MM-DD.","categoria":"formato","natureza":"RP","gravidade":"erro","contexto":"//ubl:Invoice/cac:InvoicePeriod/cbc:EndDate | //cn:CreditNote/cac:InvoicePeriod/cbc:EndDate","elementos":["BT-74"],"expressao":"matches(.,'^((\\d{4})-(\\d{2})-(\\d{2}))$')"},
{"id":"DT-CIUS-PT-073","texto":"The BT-75 does not meet the defined format: alphanumeric with size between 1 and 200.","categoria":"formato","natureza":"RP","gravidade":"erro","contexto":"//ubl:Invoice/cac:Delivery/cac:DeliveryLocation/cac:Address/cbc:StreetName | //cn:CreditNote/cac:Delivery/cac:DeliveryLocation/cac:Address/cbc:StreetName","elementos":["BT-75"],"expressao":"matches(.,'^(.{1,200})$')"},
{"id":"DT-CIUS-PT-074","texto":"The BT-76 does not meet the defined format: alphanumeric with size between 1 and 200.","categoria":"formato","natureza":"RP","gravidade":"erro","contexto":"//ubl:Invoice/cac:Delivery/cac:DeliveryLocation/cac:Address/cbc:AdditionalStreetName | //cn:CreditNote/cac:Delivery/cac:DeliveryLocation/cac:Address/cbc:AdditionalStreetName","elementos":["BT-76"],"expressao":"matches(.,'^(.{1,200})$')"},
{"id":"DT-CIUS-PT-075","texto":"The BT-165 does not meet the defined format: alphanumeric with size between 1 and 200.","categoria":"formato","natureza":"RP","gravidade":"erro","contexto":"//ubl:Invoice/cac:Delivery/cac:DeliveryLocation/cac:Address/cac:AddressLine/cbc:Line | //cn:CreditNote/cac:Delivery/cac:DeliveryLocation/cac:Address/cac:AddressLine/cbc:Line","elementos":["BT-165"],"expressao":"matches(.,'^(.{1,200})$')"},
{"id":"DT-CIUS-PT-076","texto":"The BT-77 does not meet the defined format: alphanumeric with size between 1 and 200.","categoria":"formato","natureza":"RP","gravidade":"erro","contexto":"//ubl:Invoice/cac:Delivery/cac:DeliveryLocation/cac:Address/cbc:CityName | //cn:CreditNote/cac:Delivery/cac:DeliveryLocation/cac:Address/cbc:CityName","elementos":["BT-77"],"expressao":"matches(.,'^(.{1,200})$')"},
{"id":"DT-CIUS-PT-077","texto":"The BT-78 does not meet the defined format: alphanumeric with size between 1 and 200.","categoria":"formato","natureza":"RP","gravidade":"erro","contexto":"//ubl:Invoice/cac:Delivery/cac:DeliveryLocation/cac:Address/cbc:PostalZone | //cn:CreditNote/cac:Delivery/cac:DeliveryLocation/cac:Address/cbc:PostalZone","elementos":["BT-78"],"expressao":"matches(.,'^(.{1,200})$')"},
{"id":"DT-CIUS-PT-078","texto":"The BT-79 does not meet the defined format: alphanumeric with size between 1 and 200.","categoria":"formato","natureza":"RP","gravidade":"erro","contexto":"//ubl:Invoice/cac:Delivery/cac:DeliveryLocation/cac:Address/cbc:CountrySubentity | //cn:CreditNote/cac:Delivery/cac:DeliveryLocation/cac:Address/cbc:CountrySubentity","elementos":["BT-79"],"expressao":"matches(.,'^(.{1,200})$')"},
{"id":"DT-CIUS-PT-145","texto":"The BT-80 must be coded using ISO code list 3166-1.","categoria":"valores","natureza":"RP","gravidade":"erro","contexto":"//ubl:Invoice/cac:Delivery/cac:DeliveryLocation/cac:Address/cac:Country/cbc:IdentificationCode | //cn:CreditNote/cac:Delivery/cac:DeliveryLocation/cac:Address/cac:Country/cbc:IdentificationCode","elementos":["BT-80"],"expressao":"((not(contains(normalize-space(.), ' ')) and contains(' AD AE AF AG AI AL AM AN AO AQ AR AS AT AU AW AX AZ BA BB BD BE BF BG BH BI BL BJ BM BN BO BR BS BT BV BW BY BZ CA CC CD CF CG CH CI CK CL CM CN CO CR CU CV CX CY CZ DE DJ DK DM DO DZ EC EE EG EH ER ES ET FI FJ FK FM FO FR GA GB GD GE GF GG GH GI GL GM GN GP GQ GR GS GT GU GW GY HK HM HN HR HT HU ID IE IL IM IN IO IQ IR IS IT JE JM JO JP KE KG KH KI KM KN KP KR KW KY KZ LA LB LC LI LK LR LS LT LU LV LY MA MC MD ME MF MG MH MK ML MM MN MO MP MQ MR MS MT MU MV MW MX MY MZ NA NC NE NF NG NI NL NO NP NR NU NZ OM PA PE PF PG PH PK PL PM PN PR PS PT PW PY QA RO RS RU RW SA SB SC SD SE SG SH SI SJ SK SL SM SN SO SR ST SV SY SZ TC TD TF TG TH TJ TK TL TM TN TO TR TT TV TW TZ UA UG UM US UY UZ VA VC VE VG VI VN VU WF WS YE YT ZA ZM ZW ', concat(' ', normalize-space(.), ' '))))"},
{"id":"DT-CIUS-PT-079.1","texto":"The BT-81 does not meet the defined format: it is mandatory to prefix the value with the following '#ENTITY@ATMPAYMENT#' and suffice with '#'.","categoria":"formato","natureza":"RP","gravidade":"erro","contexto":"//ubl:Invoice/cac:PaymentMeans/cbc:PaymentMeansCode | //cn:CreditNote/cac:PaymentMeans/cbc:PaymentMeansCode","elementos":["BT-81"],"expressao":"report (dispara quando verdadeiro): starts-with(normalize-space(.),'#ENTITY@ATMPAYMENT#') and not(matches(.,'^(#(ENTITY@ATMPAYMENT)#(.{1,20})#)$'))"},
{"id":"DT-CIUS-PT-079.2","texto":"The BT-81 must be coded using UNCL4461 code list or the following values: CC, CD, CH, CI, CO, CS, DE, LC, MB, NU, OU, PR, TB, TR.","categoria":"valores","natureza":"RP","gravidade":"erro","contexto":"//ubl:Invoice/cac:PaymentMeans/cbc:PaymentMeansCode | //cn:CreditNote/cac:PaymentMeans/cbc:PaymentMeansCode","elementos":["BT-81"],"expressao":"report (dispara quando verdadeiro): not(starts-with(normalize-space(.),'#ENTITY@ATMPAYMENT#')) and (contains(normalize-space(.),' ') or not(contains( ' 30 48 49 57 58 59 CC CD CH CI CO CS DE LC MB NU OU PR TB TR ',concat(' ',normalize-space(.),' '))))"},
{"id":"DT-CIUS-PT-079.3","texto":"The BT-82 identification name does not meet the defined format: alphanumeric with size between 1 and 150.","categoria":"formato","natureza":"RP","gravidade":"erro","contexto":"//ubl:Invoice/cac:PaymentMeans/cbc:PaymentMeansCode | //cn:CreditNote/cac:PaymentMeans/cbc:PaymentMeansCode","elementos":["BT-82"],"expressao":"report (dispara quando verdadeiro): (exists(@name) and not(matches(@name,'^(.{1,150})$')))"},
{"id":"DT-CIUS-PT-079.4","texto":"The BT-82 does not meet the defined format: it is mandatory to prefix the value with the following '#DESCRIPTION@ATMPAYMENT#' and suffice with '#'.","categoria":"formato","natureza":"RP","gravidade":"erro","contexto":"//ubl:Invoice/cac:PaymentMeans/cbc:PaymentMeansCode | //cn:CreditNote/cac:PaymentMeans/cbc:PaymentMeansCode","elementos":["BT-82"],"expressao":"report (dispara quando verdadeiro): exists(@name) and starts-with(normalize-space(@name),'#DESCRIPTION@ATMPAYMENT#') and not(matches(@name,'^(#(DESCRIPTION@ATMPAYMENT)#(.{1,125})#)$'))"},
{"id":"DT-CIUS-PT-080","texto":"The BT-83 does not meet the defined format: it is mandatory to prefix the value with the following '#REFERENCE@ATMPAYMENT#' or '#REFERENCE@DUCPAYMENT#' and suffice with '#'.","categoria":"formato","natureza":"RP","gravidade":"erro","contexto":"//ubl:Invoice/cac:PaymentMeans/cbc:PaymentID | //cn:CreditNote/cac:PaymentMeans/cbc:PaymentID","elementos":["BT-83"],"expressao":"(matches(.,'^(#(REFERENCE@ATMPAYMENT)#(.{1,20})#)$') or matches(.,'^(#(REFERENCE@DUCPAYMENT)#(.{1,20})#)$'))"},
{"id":"DT-CIUS-PT-081","texto":"The BT-84 does not meet the defined format: alphanumeric with size between 1 and 50.","categoria":"formato","natureza":"RP","gravidade":"erro","contexto":"//ubl:Invoice/cac:PaymentMeans/cac:PayeeFinancialAccount/cbc:ID | //cn:CreditNote/cac:PaymentMeans/cac:PayeeFinancialAccount/cbc:ID","elementos":["BT-84"],"expressao":"matches(.,'^(.{1,50})$')"},
{"id":"DT-CIUS-PT-082","texto":"The BT-85 does not meet the defined format: alphanumeric with size between 1 and 200.","categoria":"formato","natureza":"RP","gravidade":"erro","contexto":"//ubl:Invoice/cac:PaymentMeans/cac:PayeeFinancialAccount/cbc:Name | //cn:CreditNote/cac:PaymentMeans/cac:PayeeFinancialAccount/cbc:Name","elementos":["BT-85"],"expressao":"matches(.,'^(.{1,200})$')"},
{"id":"DT-CIUS-PT-083","texto":"The BT-86 does not meet the defined format: alphanumeric with size between 1 and 50.","categoria":"formato","natureza":"RP","gravidade":"erro","contexto":"//ubl:Invoice/cac:PaymentMeans/cac:PayeeFinancialAccount/cac:FinancialInstitutionBranch/cbc:ID | //cn:CreditNote/cac:PaymentMeans/cac:PayeeFinancialAccount/cac:FinancialInstitutionBranch/cbc:ID","elementos":["BT-86"],"expressao":"matches(.,'^(.{1,50})$')"},
{"id":"DT-CIUS-PT-084.1","texto":"The BT-87 does not meet the defined format: alphanumeric with size between 1 and 200.","categoria":"formato","natureza":"RP","gravidade":"erro","contexto":"//ubl:Invoice/cac:PaymentMeans/cac:CardAccount/cbc:PrimaryAccountNumberID | //cn:CreditNote/cac:PaymentMeans/cac:CardAccount/cbc:PrimaryAccountNumberID","elementos":["BT-87"],"expressao":"matches(.,'^(.{1,200})$')"},
{"id":"DT-CIUS-PT-084.2","texto":"The Network identifier does not meet the defined format: alphanumeric with size between 1 and 200.","categoria":"formato","natureza":"RP","gravidade":"erro","contexto":"//ubl:Invoice/cac:PaymentMeans/cac:CardAccount/cbc:NetworkID | //cn:CreditNote/cac:PaymentMeans/cac:CardAccount/cbc:NetworkID","expressao":"matches(.,'^(.{1,200})$')"},
{"id":"DT-CIUS-PT-085","texto":"The BT-88 does not meet the defined format: alphanumeric with size between 1 and 200.","categoria":"formato","natureza":"RP","gravidade":"erro","contexto":"//ubl:Invoice/cac:PaymentMeans/cac:CardAccount/cbc:HolderName | //cn:CreditNote/cac:PaymentMeans/cac:CardAccount/cbc:HolderName","elementos":["BT-88"],"expressao":"matches(.,'^(.{1,200})$')"},
{"id":"DT-CIUS-PT-086","texto":"The BT-89 does not meet the defined format: alphanumeric with size between 1 and 50.","categoria":"formato","natureza":"RP","gravidade":"erro","contexto":"//ubl:Invoice/cac:PaymentMeans/cac:PaymentMandate/cbc:ID | //cn:CreditNote/cac:PaymentMeans/cac:PaymentMandate/cbc:ID","elementos":["BT-89"],"expressao":"matches(.,'^(.{1,50})$')"},
{"id":"DT-CIUS-PT-087","texto":"The BT-91 does not meet the defined format: alphanumeric with size between 1 and 50.","categoria":"formato","natureza":"RP","gravidade":"erro","contexto":"//ubl:Invoice/cac:PaymentMeans/cac:PaymentMandate/cac:PayerFinancialAccount/cbc:ID | //cn:CreditNote/cac:PaymentMeans/cac:PaymentMandate/cac:PayerFinancialAccount/cbc:ID","elementos":["BT-91"],"expressao":"matches(.,'^(.{1,50})$')"},
{"id":"DT-CIUS-PT-088.1","texto":"The BT-92 and BT-99 does not meet the defined format: decimal value with 2 decimal places and 13 unit places.","categoria":"formato","natureza":"RP","gravidade":"erro","contexto":"//ubl:Invoice/cac:AllowanceCharge/cbc:Amount | //cn:CreditNote/cac:AllowanceCharge/cbc:Amount","elementos":["BT-92","BT-99"],"expressao":"matches(.,'^(\\d{1,13}\\.\\d{2})$')"},
{"id":"DT-CIUS-PT-088.2","texto":"The BT-92 and BT-99 currencyID must be equal to BT-5.","categoria":"outra","natureza":"?","gravidade":"erro","contexto":"//ubl:Invoice/cac:AllowanceCharge/cbc:Amount | //cn:CreditNote/cac:AllowanceCharge/cbc:Amount","elementos":["BT-5","BT-92","BT-99"],"expressao":"normalize-space(@currencyID)= $bt05"},
{"id":"DT-CIUS-PT-089.1","texto":"The BT-93 and BT-100 does not meet the defined format: decimal value with 2 decimal places and 13 unit places.","categoria":"formato","natureza":"RP","gravidade":"erro","contexto":"//ubl:Invoice/cac:AllowanceCharge/cbc:BaseAmount | //cn:CreditNote/cac:AllowanceCharge/cbc:BaseAmount","elementos":["BT-93","BT-100"],"expressao":"matches(.,'^(\\d{1,13}\\.\\d{2})$')"},
{"id":"DT-CIUS-PT-089.2","texto":"The BT-93 and BT-100 currencyID must be equal to BT-5.","categoria":"outra","natureza":"?","gravidade":"erro","contexto":"//ubl:Invoice/cac:AllowanceCharge/cbc:BaseAmount | //cn:CreditNote/cac:AllowanceCharge/cbc:BaseAmount","elementos":["BT-5","BT-93","BT-100"],"expressao":"normalize-space(@currencyID)= $bt05"},
{"id":"DT-CIUS-PT-090.1","texto":"The BT-94 and BT-101 does not meet the defined format: decimal value with 2 decimal places and 3 unit places.","categoria":"formato","natureza":"RP","gravidade":"erro","contexto":"//ubl:Invoice/cac:AllowanceCharge/cbc:MultiplierFactorNumeric | //cn:CreditNote/cac:AllowanceCharge/cbc:MultiplierFactorNumeric","elementos":["BT-94","BT-101"],"expressao":"matches(.,'^(\\d{1,3}\\.\\d{2})$')"},
{"id":"DT-CIUS-PT-090.2","texto":"The BT-94 and BT-101 does not meet the defined format: value between 0.01 and 100.00.","categoria":"formato","natureza":"RP","gravidade":"erro","contexto":"//ubl:Invoice/cac:AllowanceCharge/cbc:MultiplierFactorNumeric | //cn:CreditNote/cac:AllowanceCharge/cbc:MultiplierFactorNumeric","elementos":["BT-94","BT-101"],"expressao":"report (dispara quando verdadeiro): matches(.,'^(\\d{1,3}\\.\\d{2})$') and (xs:decimal(.) < 0.00 or xs:decimal(.) > 100.00)"},
{"id":"DT-CIUS-PT-091","texto":"The BT-95 and BT-102 does not meet the defined format: only admits the following values: AA, S, E, RED, INT, NOR, ISE, OUT, NA, Z, AE, IC, G, O.","categoria":"valores","natureza":"RP","gravidade":"erro","contexto":"//ubl:Invoice/cac:AllowanceCharge/cac:TaxCategory/cbc:ID | //cn:CreditNote/cac:AllowanceCharge/cac:TaxCategory/cbc:ID","elementos":["BT-95","BT-102"],"expressao":"(not(contains(normalize-space(.),' ')) and contains(' AA S E RED INT NOR ISE OUT NA Z AE IC G O ',concat(' ',normalize-space(.),' ')))"},
{"id":"DT-CIUS-PT-092.1","texto":"The BT-96 and BT-103 does not meet the defined format: decimal value with 2 decimal places and 3 unit places.","categoria":"formato","natureza":"RP","gravidade":"erro","contexto":"//ubl:Invoice/cac:AllowanceCharge/cac:TaxCategory/cbc:Percent | //cn:CreditNote/cac:AllowanceCharge/cac:TaxCategory/cbc:Percent","elementos":["BT-96","BT-103"],"expressao":"matches(.,'^(\\d{1,3}\\.\\d{2})$')"},
{"id":"DT-CIUS-PT-092.2","texto":"The BT-96 and BT-103 does not meet the defined format: value between 0.01 and 100.00.","categoria":"formato","natureza":"RP","gravidade":"erro","contexto":"//ubl:Invoice/cac:AllowanceCharge/cac:TaxCategory/cbc:Percent | //cn:CreditNote/cac:AllowanceCharge/cac:TaxCategory/cbc:Percent","elementos":["BT-96","BT-103"],"expressao":"report (dispara quando verdadeiro): matches(.,'^(\\d{1,3}\\.\\d{2})$') and (xs:decimal(.) < 0.00 or xs:decimal(.) > 100.00)"},
{"id":"DT-CIUS-PT-156","texto":"The Invoice allowance (BG-20) and/or charge (BG-21) tax scheme should be coded using a restriction of UN/ECE 5153.","categoria":"outra","natureza":"?","gravidade":"erro","contexto":"//ubl:Invoice/cac:AllowanceCharge/cac:TaxCategory/cac:TaxScheme/cbc:ID | //cn:CreditNote/cac:AllowanceCharge/cac:TaxCategory/cac:TaxScheme/cbc:ID","elementos":["BG-20","BG-21"],"expressao":"(not(contains(normalize-space(.),' ')) and contains(' AAA AAB AAC AAD AAE AAF AAG AAH AAI AAJ AAK ADD BOL CAP CAR COC CST CUD CVD ENV EXC EXP FET FRE GCN GST ILL IMP IND LAC LCN LDP LOC LST MCA MCD OTH PDB PDC PRF SCN SSS STT SUP SUR SWT TAC TOT TOX TTA VAD VAT ',concat(' ',normalize-space(.),' ')))"},
{"id":"DT-CIUS-PT-093","texto":"The BT-97 and BT-104 does not meet the defined format: alphanumeric with size between 1 and 200.","categoria":"formato","natureza":"RP","gravidade":"erro","contexto":"//ubl:Invoice/cac:AllowanceCharge/cbc:AllowanceChargeReason | //cn:CreditNote/cac:AllowanceCharge/cbc:AllowanceChargeReason","elementos":["BT-97","BT-104"],"expressao":"matches(.,'^(.{1,200})$')"},
{"id":"DT-CIUS-PT-149","texto":"The BT-98 must belong to the UNCL 5189 code list.","categoria":"valores","natureza":"RP","gravidade":"erro","contexto":"//ubl:Invoice/cac:AllowanceCharge[cbc:ChargeIndicator = 'false']/cbc:AllowanceChargeReasonCode | //cn:CreditNote/cac:AllowanceCharge[cbc:ChargeIndicator = 'false']/cbc:AllowanceChargeReasonCode","elementos":["BT-98"],"expressao":"((not(contains(normalize-space(.), ' ')) and contains(' 41 42 60 62 63 64 65 66 67 68 70 71 88 95 100 102 103 104 105 ', concat(' ', normalize-space(.), ' '))))"},
{"id":"DT-CIUS-PT-150","texto":"The BT-105 must belong to the UNCL 7161 code list.","categoria":"valores","natureza":"RP","gravidade":"erro","contexto":"//ubl:Invoice/cac:AllowanceCharge[cbc:ChargeIndicator = 'true']/cbc:AllowanceChargeReasonCode | //cn:CreditNote/cac:AllowanceCharge[cbc:ChargeIndicator = 'true']/cbc:AllowanceChargeReasonCode","elementos":["BT-105"],"expressao":"((not(contains(normalize-space(.), ' ')) and contains(' AA AAA AAC AAD AAE AAF AAH AAI AAS AAT AAV AAY AAZ ABA ABB ABC ABD ABF ABK ABL ABN ABR ABS ABT ABU ACF ACG ACH ACI ACJ ACK ACL ACM ACS ADC ADE ADJ ADK ADL ADM ADN ADO ADP ADQ ADR ADT ADW ADY ADZ AEA AEB AEC AED AEF AEH AEI AEJ AEK AEL AEM AEN AEO AEP AES AET AEU AEV AEW AEX AEY AEZ AJ AU CA CAB CAD CAE CAF CAI CAJ CAK CAL CAM CAN CAO CAP CAQ CAR CAS CAT CAU CAV CAW CD CG CS CT DAB DAD DL EG EP ER FAA FAB FAC FC FH FI GAA HAA HD HH IAA IAB ID IF IR IS KO L1 LA LAA LAB LF MAE MI ML NAA OA PA PAA PC PL RAB RAC RAD RAF RE RF RH RV SA SAA SAD SAE SAI SG SH SM ST SU TAB TAC TT TV V1 V2 WH XAA YY ZZZ ', concat(' ', normalize-space(.), ' '))))"},
{"id":"DT-CIUS-PT-094.1","texto":"The BT-106 does not meet the defined format: decimal value with 2 decimal places and 13 unit places, than can be negative.","categoria":"formato","natureza":"RP","gravidade":"erro","contexto":"//ubl:Invoice/cac:LegalMonetaryTotal/cbc:LineExtensionAmount | //cn:CreditNote/cac:LegalMonetaryTotal/cbc:LineExtensionAmount","elementos":["BT-106"],"expressao":"matches(.,'^(-?\\d{1,13}\\.\\d{2})$')"},
{"id":"DT-CIUS-PT-094.2","texto":"The BT-106 currencyID must be equal to BT-5.","categoria":"outra","natureza":"?","gravidade":"erro","contexto":"//ubl:Invoice/cac:LegalMonetaryTotal/cbc:LineExtensionAmount | //cn:CreditNote/cac:LegalMonetaryTotal/cbc:LineExtensionAmount","elementos":["BT-5","BT-106"],"expressao":"normalize-space(@currencyID)= $bt05"},
{"id":"DT-CIUS-PT-095.1","texto":"The BT-107 does not meet the defined format: decimal value with 2 decimal places and 13 unit places.","categoria":"formato","natureza":"RP","gravidade":"erro","contexto":"//ubl:Invoice/cac:LegalMonetaryTotal/cbc:AllowanceTotalAmount | //cn:CreditNote/cac:LegalMonetaryTotal/cbc:AllowanceTotalAmount","elementos":["BT-107"],"expressao":"matches(.,'^(\\d{1,13}\\.\\d{2})$')"},
{"id":"DT-CIUS-PT-095.2","texto":"The BT-107 currencyID must be equal to BT-5.","categoria":"outra","natureza":"?","gravidade":"erro","contexto":"//ubl:Invoice/cac:LegalMonetaryTotal/cbc:AllowanceTotalAmount | //cn:CreditNote/cac:LegalMonetaryTotal/cbc:AllowanceTotalAmount","elementos":["BT-5","BT-107"],"expressao":"normalize-space(@currencyID)= $bt05"},
{"id":"DT-CIUS-PT-096.1","texto":"The BT-108 does not meet the defined format: decimal value with 2 decimal places and 13 unit places.","categoria":"formato","natureza":"RP","gravidade":"erro","contexto":"//ubl:Invoice/cac:LegalMonetaryTotal/cbc:ChargeTotalAmount | //cn:CreditNote/cac:LegalMonetaryTotal/cbc:ChargeTotalAmount","elementos":["BT-108"],"expressao":"matches(.,'^(\\d{1,13}\\.\\d{2})$')"},
{"id":"DT-CIUS-PT-096.2","texto":"The BT-108 currencyID must be equal to BT-5.","categoria":"outra","natureza":"?","gravidade":"erro","contexto":"//ubl:Invoice/cac:LegalMonetaryTotal/cbc:ChargeTotalAmount | //cn:CreditNote/cac:LegalMonetaryTotal/cbc:ChargeTotalAmount","elementos":["BT-5","BT-108"],"expressao":"normalize-space(@currencyID)= $bt05"},
{"id":"DT-CIUS-PT-097.1","texto":"The BT-109 does not meet the defined format: decimal value with 2 decimal places and 13 unit places.","categoria":"formato","natureza":"RP","gravidade":"erro","contexto":"//ubl:Invoice/cac:LegalMonetaryTotal/cbc:TaxExclusiveAmount | //cn:CreditNote/cac:LegalMonetaryTotal/cbc:TaxExclusiveAmount","elementos":["BT-109"],"expressao":"matches(.,'^(\\d{1,13}\\.\\d{2})$')"},
{"id":"DT-CIUS-PT-097.2","texto":"The BT-109 currencyID must be equal to BT-5.","categoria":"outra","natureza":"?","gravidade":"erro","contexto":"//ubl:Invoice/cac:LegalMonetaryTotal/cbc:TaxExclusiveAmount | //cn:CreditNote/cac:LegalMonetaryTotal/cbc:TaxExclusiveAmount","elementos":["BT-5","BT-109"],"expressao":"normalize-space(@currencyID)= $bt05"},
{"id":"DT-CIUS-PT-098.1","texto":"The BT-110 and BT-111 does not meet the defined format: decimal value with 2 decimal places and 13 unit places, than can be negative.","categoria":"formato","natureza":"RP","gravidade":"erro","contexto":"//ubl:Invoice/cac:TaxTotal/cbc:TaxAmount | //cn:CreditNote/cac:TaxTotal/cbc:TaxAmount","elementos":["BT-110","BT-111"],"expressao":"matches(.,'^(-?\\d{1,13}\\.\\d{2})$')"},
{"id":"DT-CIUS-PT-098.2","texto":"The BT-111 currencyID must be equal to BT-6.","categoria":"outra","natureza":"?","gravidade":"erro","contexto":"//ubl:Invoice/cac:TaxTotal/cbc:TaxAmount | //cn:CreditNote/cac:TaxTotal/cbc:TaxAmount","elementos":["BT-6","BT-111"],"expressao":"report (dispara quando verdadeiro): exists(//ubl:Invoice/cbc:TaxCurrencyCode | //cn:CreditNote/cbc:TaxCurrencyCode) and normalize-space(@currencyID) != $bt06"},
{"id":"DT-CIUS-PT-098.3","texto":"The BT-110 currencyID must be equal to BT-5.","categoria":"outra","natureza":"?","gravidade":"erro","contexto":"//ubl:Invoice/cac:TaxTotal/cbc:TaxAmount | //cn:CreditNote/cac:TaxTotal/cbc:TaxAmount","elementos":["BT-5","BT-110"],"expressao":"report (dispara quando verdadeiro): not(//ubl:Invoice/cbc:TaxCurrencyCode | //cn:CreditNote/cbc:TaxCurrencyCode) and normalize-space(@currencyID) != $bt05"},
{"id":"DT-CIUS-PT-099.1","texto":"The BT-112 does not meet the defined format: decimal value with 2 decimal places and 13 unit places.","categoria":"formato","natureza":"RP","gravidade":"erro","contexto":"//ubl:Invoice/cac:LegalMonetaryTotal/cbc:TaxInclusiveAmount | //cn:CreditNote/cac:LegalMonetaryTotal/cbc:TaxInclusiveAmount","elementos":["BT-112"],"expressao":"matches(.,'^(\\d{1,13}\\.\\d{2})$')"},
{"id":"DT-CIUS-PT-099.2","texto":"The BT-112 currencyID must be equal to BT-5.","categoria":"outra","natureza":"?","gravidade":"erro","contexto":"//ubl:Invoice/cac:LegalMonetaryTotal/cbc:TaxInclusiveAmount | //cn:CreditNote/cac:LegalMonetaryTotal/cbc:TaxInclusiveAmount","elementos":["BT-5","BT-112"],"expressao":"normalize-space(@currencyID)= $bt05"},
{"id":"DT-CIUS-PT-100.1","texto":"The BT-113 does not meet the defined format: decimal value with 2 decimal places and 13 unit places.","categoria":"formato","natureza":"RP","gravidade":"erro","contexto":"//ubl:Invoice/cac:LegalMonetaryTotal/cbc:PrepaidAmount | //cn:CreditNote/cac:LegalMonetaryTotal/cbc:PrepaidAmount","elementos":["BT-113"],"expressao":"matches(.,'^(\\d{1,13}\\.\\d{2})$')"},
{"id":"DT-CIUS-PT-100.2","texto":"The BT-113 currencyID must be equal to BT-5.","categoria":"outra","natureza":"?","gravidade":"erro","contexto":"//ubl:Invoice/cac:LegalMonetaryTotal/cbc:PrepaidAmount | //cn:CreditNote/cac:LegalMonetaryTotal/cbc:PrepaidAmount","elementos":["BT-5","BT-113"],"expressao":"normalize-space(@currencyID)= $bt05"},
{"id":"DT-CIUS-PT-101.1","texto":"The BT-114 does not meet the defined format: decimal value with 2 decimal places and 13 unit places, than can be negative.","categoria":"formato","natureza":"RP","gravidade":"erro","contexto":"//ubl:Invoice/cac:LegalMonetaryTotal/cbc:PayableRoundingAmount | //cn:CreditNote/cac:LegalMonetaryTotal/cbc:PayableRoundingAmount","elementos":["BT-114"],"expressao":"matches(.,'^(-?\\d{1,13}\\.\\d{2})$')"},
{"id":"DT-CIUS-PT-101.2","texto":"The BT-114 currencyID must be equal to BT-5.","categoria":"outra","natureza":"?","gravidade":"erro","contexto":"//ubl:Invoice/cac:LegalMonetaryTotal/cbc:PayableRoundingAmount | //cn:CreditNote/cac:LegalMonetaryTotal/cbc:PayableRoundingAmount","elementos":["BT-5","BT-114"],"expressao":"normalize-space(@currencyID)= $bt05"},
{"id":"DT-CIUS-PT-102.1","texto":"The BT-115 does not meet the defined format: decimal value with 2 decimal places and 13 unit places.","categoria":"formato","natureza":"RP","gravidade":"erro","contexto":"//ubl:Invoice/cac:LegalMonetaryTotal/cbc:PayableAmount  | //cn:CreditNote/cac:LegalMonetaryTotal/cbc:PayableAmount","elementos":["BT-115"],"expressao":"matches(.,'^(\\d{1,13}\\.\\d{2})$')"},
{"id":"DT-CIUS-PT-102.2","texto":"The BT-115 currencyID must be equal to BT-5.","categoria":"outra","natureza":"?","gravidade":"erro","contexto":"//ubl:Invoice/cac:LegalMonetaryTotal/cbc:PayableAmount  | //cn:CreditNote/cac:LegalMonetaryTotal/cbc:PayableAmount","elementos":["BT-5","BT-115"],"expressao":"normalize-space(@currencyID)= $bt05"},
{"id":"DT-CIUS-PT-103.1","texto":"The BT-116 does not meet the defined format: decimal value with 3 decimal places and 13 unit places, than can be negative.","categoria":"formato","natureza":"RP","gravidade":"erro","contexto":"//ubl:Invoice/cac:TaxTotal/cac:TaxSubtotal/cbc:TaxableAmount | //cn:CreditNote/cac:TaxTotal/cac:TaxSubtotal/cbc:TaxableAmount","elementos":["BT-116"],"expressao":"matches(.,'^(-?\\d{1,13}\\.\\d{2,3})$')"},
{"id":"DT-CIUS-PT-103.2","texto":"The BT-116 currencyID must be equal to BT-5.","categoria":"outra","natureza":"?","gravidade":"erro","contexto":"//ubl:Invoice/cac:TaxTotal/cac:TaxSubtotal/cbc:TaxableAmount | //cn:CreditNote/cac:TaxTotal/cac:TaxSubtotal/cbc:TaxableAmount","elementos":["BT-5","BT-116"],"expressao":"normalize-space(@currencyID)= $bt05"},
{"id":"DT-CIUS-PT-104.1","texto":"The BT-117 does not meet the defined format: decimal value with 2 decimal places and 13 unit places, than can be negative.","categoria":"formato","natureza":"RP","gravidade":"erro","contexto":"//ubl:Invoice/cac:TaxTotal/cac:TaxSubtotal/cbc:TaxAmount  | //cn:CreditNote/cac:TaxTotal/cac:TaxSubtotal/cbc:TaxAmount","elementos":["BT-117"],"expressao":"matches(.,'^(-?\\d{1,13}\\.\\d{2})$')"},
{"id":"DT-CIUS-PT-104.2","texto":"The BT-117 currencyID must be equal to BT-6.","categoria":"outra","natureza":"?","gravidade":"erro","contexto":"//ubl:Invoice/cac:TaxTotal/cac:TaxSubtotal/cbc:TaxAmount  | //cn:CreditNote/cac:TaxTotal/cac:TaxSubtotal/cbc:TaxAmount","elementos":["BT-6","BT-117"],"expressao":"report (dispara quando verdadeiro): exists(//ubl:Invoice/cbc:TaxCurrencyCode | //cn:CreditNote/cbc:TaxCurrencyCode) and normalize-space(@currencyID) != $bt06"},
{"id":"DT-CIUS-PT-104.3","texto":"The BT-117 currencyID must be equal to BT-5.","categoria":"outra","natureza":"?","gravidade":"erro","contexto":"//ubl:Invoice/cac:TaxTotal/cac:TaxSubtotal/cbc:TaxAmount  | //cn:CreditNote/cac:TaxTotal/cac:TaxSubtotal/cbc:TaxAmount","elementos":["BT-5","BT-117"],"expressao":"report (dispara quando verdadeiro): not(//ubl:Invoice/cbc:TaxCurrencyCode | //cn:CreditNote/cbc:TaxCurrencyCode) and normalize-space(@currencyID) != $bt05"},
{"id":"DT-CIUS-PT-105","texto":"The BT-118 does not meet the defined format: only admits the following values: AA, S, E, RED, INT, NOR, ISE, OUT, NA, Z, AE, IC, G, O.","categoria":"valores","natureza":"RP","gravidade":"erro","contexto":"//ubl:Invoice/cac:TaxTotal/cac:TaxSubtotal/cac:TaxCategory/cbc:ID | //cn:CreditNote/cac:TaxTotal/cac:TaxSubtotal/cac:TaxCategory/cbc:ID","elementos":["BT-118"],"expressao":"(not(contains(normalize-space(.),' ')) and contains(' AA S E RED INT NOR ISE OUT NA Z AE IC G O ',concat(' ',normalize-space(.),' ')))"},
{"id":"DT-CIUS-PT-106.1","texto":"The BT-119 does not meet the defined format: decimal value with 2 decimal places and 3 unit places.","categoria":"formato","natureza":"RP","gravidade":"erro","contexto":"//ubl:Invoice/cac:TaxTotal/cac:TaxSubtotal/cac:TaxCategory/cbc:Percent | //cn:CreditNote/cac:TaxTotal/cac:TaxSubtotal/cac:TaxCategory/cbc:Percent","elementos":["BT-119"],"expressao":"matches(.,'^(\\d{1,3}\\.\\d{2})$')"},
{"id":"DT-CIUS-PT-106.2","texto":"The BT-119 does not meet the defined format: value between 0.01 and 100.00.","categoria":"formato","natureza":"RP","gravidade":"erro","contexto":"//ubl:Invoice/cac:TaxTotal/cac:TaxSubtotal/cac:TaxCategory/cbc:Percent | //cn:CreditNote/cac:TaxTotal/cac:TaxSubtotal/cac:TaxCategory/cbc:Percent","elementos":["BT-119"],"expressao":"report (dispara quando verdadeiro): matches(.,'^(\\d{1,3}\\.\\d{2})$') and (xs:decimal(.) < 0.00 or xs:decimal(.) > 100.00)"},
{"id":"DT-CIUS-PT-107","texto":"The BT-120 does not meet the defined format: alphanumeric with size between 1 and 200.","categoria":"formato","natureza":"RP","gravidade":"erro","contexto":"//ubl:Invoice/cac:TaxTotal/cac:TaxSubtotal/cac:TaxCategory/cbc:TaxExemptionReason | //cn:CreditNote/cac:TaxTotal/cac:TaxSubtotal/cac:TaxCategory/cbc:TaxExemptionReason","elementos":["BT-120"],"expressao":"matches(.,'^(.{1,200})$')"},
{"id":"DT-CIUS-PT-108","texto":"The BT-121 does not meet the defined format: alphanumeric with size between 1 and 5.","categoria":"formato","natureza":"RP","gravidade":"erro","contexto":"//ubl:Invoice/cac:TaxTotal/cac:TaxSubtotal/cac:TaxCategory/cbc:TaxExemptionReasonCode | //cn:CreditNote/cac:TaxTotal/cac:TaxSubtotal/cac:TaxCategory/cbc:TaxExemptionReasonCode","elementos":["BT-121"],"expressao":"matches(.,'^(.{1,5})$')"},
{"id":"DT-CIUS-PT-154","texto":"The VATBReakdown (BG-23) tax scheme should be coded using a restriction of UN/ECE 5153.","categoria":"outra","natureza":"?","gravidade":"erro","contexto":"//ubl:Invoice/cac:TaxTotal/cac:TaxSubtotal/cac:TaxCategory/cac:TaxScheme/cbc:ID | //cn:CreditNote/cac:TaxTotal/cac:TaxSubtotal/cac:TaxCategory/cac:TaxScheme/cbc:ID","elementos":["BG-23"],"expressao":"(not(contains(normalize-space(.),' ')) and contains(' AAA AAB AAC AAD AAE AAF AAG AAH AAI AAJ AAK ADD BOL CAP CAR COC CST CUD CVD ENV EXC EXP FET FRE GCN GST ILL IMP IND LAC LCN LDP LOC LST MCA MCD OTH PDB PDC PRF SCN SSS STT SUP SUR SWT TAC TOT TOX TTA VAD VAT ',concat(' ',normalize-space(.),' ')))"},
{"id":"DT-CIUS-PT-109","texto":"The BT-123 does not meet the defined format: alphanumeric with size between 1 and 200.","categoria":"formato","natureza":"RP","gravidade":"erro","contexto":"//ubl:Invoice/cac:AdditionalDocumentReference/cbc:DocumentDescription | //cn:CreditNote/cac:AdditionalDocumentReference/cbc:DocumentDescription","elementos":["BT-123"],"expressao":"matches(.,'^(.{1,200})$')"},
{"id":"DT-CIUS-PT-110","texto":"The BT-124 does not meet the defined format: alphanumeric with size between 1 and 200.","categoria":"formato","natureza":"RP","gravidade":"erro","contexto":"//ubl:Invoice/cac:AdditionalDocumentReference/cac:Attachment/cac:ExternalReference/cbc:URI | //cn:CreditNote/cac:AdditionalDocumentReference/cac:Attachment/cac:ExternalReference/cbc:URI","elementos":["BT-124"],"expressao":"matches(.,'^(.{1,200})$')"},
{"id":"DT-CIUS-PT-111.1","texto":"The BT-125 does not meet the defined format: alphanumeric with size between 1 and 6826666.","categoria":"formato","natureza":"RP","gravidade":"erro","contexto":"//ubl:Invoice/cac:AdditionalDocumentReference/cac:Attachment/cbc:EmbeddedDocumentBinaryObject | //cn:CreditNote/cac:AdditionalDocumentReference/cac:Attachment/cbc:EmbeddedDocumentBinaryObject","elementos":["BT-125"],"expressao":"matches(.,'^(.{1,6826666})$')"},
{"id":"DT-CIUS-PT-111.2","texto":"The BT-125 does not meet the defined format: the maximum size per file is 5 Mb.","categoria":"formato","natureza":"RP","gravidade":"erro","contexto":"//ubl:Invoice/cac:AdditionalDocumentReference/cac:Attachment/cbc:EmbeddedDocumentBinaryObject | //cn:CreditNote/cac:AdditionalDocumentReference/cac:Attachment/cbc:EmbeddedDocumentBinaryObject","elementos":["BT-125"],"expressao":"((string-length(.)*0.75) div 1024) < 5000"},
{"id":"DT-CIUS-PT-112","texto":"The BT-125_1 does not meet the defined format: only admits the following values: text/plain, image/png, image/jpeg, application/pdf, application/msword, application/vnd.openxmlformats-officedocument.wordprocessingml.document, application/vnd.ms-excel, application/vnd.openxmlformats-officedocument.spreadsheetml.sheet, application/xml, text/xml, text/csv.","categoria":"valores","natureza":"RP","gravidade":"erro","contexto":"//ubl:Invoice/cac:AdditionalDocumentReference/cac:Attachment/cbc:EmbeddedDocumentBinaryObject | //cn:CreditNote/cac:AdditionalDocumentReference/cac:Attachment/cbc:EmbeddedDocumentBinaryObject","expressao":"(not(contains(normalize-space(@mimeCode),' ')) and contains(' text/plain image/png image/jpeg application/pdf application/msword application/vnd.openxmlformats-officedocument.wordprocessingml.document application/vnd.ms-excel application/vnd.openxmlformats-officedocument.spreadsheetml.sheet application/xml text/xml text/csv ',concat(' ',normalize-space(@mimeCode),' ')))"},
{"id":"DT-CIUS-PT-113","texto":"The BT-125_2 does not meet the defined format: alphanumeric with size between 1 and 50.","categoria":"formato","natureza":"RP","gravidade":"erro","contexto":"//ubl:Invoice/cac:AdditionalDocumentReference/cac:Attachment/cbc:EmbeddedDocumentBinaryObject | //cn:CreditNote/cac:AdditionalDocumentReference/cac:Attachment/cbc:EmbeddedDocumentBinaryObject","expressao":"matches(@filename,'^(.{1,50})$')"},
{"id":"DT-CIUS-PT-114.1","texto":"The BT-126 does not meet the defined format: alphanumeric with size between 1 and 50.","categoria":"formato","natureza":"RP","gravidade":"erro","contexto":"//ubl:Invoice/cac:InvoiceLine/cbc:ID | //cn:CreditNote/cac:CreditNoteLine/cbc:ID","elementos":["BT-126"],"expressao":"matches(.,'^(.{1,50})$')"},
{"id":"DT-CIUS-PT-114.2","texto":"The BT-126 value must be unique.","categoria":"cardinalidade","natureza":"RE","gravidade":"erro","contexto":"//ubl:Invoice/cac:InvoiceLine/cbc:ID | //cn:CreditNote/cac:CreditNoteLine/cbc:ID","elementos":["BT-126"],"expressao":"count(//ubl:Invoice/cac:InvoiceLine/cbc:ID | //cn:CreditNote/cac:CreditNoteLine/cbc:ID) = count(distinct-values(//ubl:Invoice/cac:InvoiceLine/cbc:ID | //cn:CreditNote/cac:CreditNoteLine/cbc:ID))"},
{"id":"DT-CIUS-PT-115","texto":"The BT-127 does not meet the defined format: alphanumeric with size between 1 and 500.","categoria":"formato","natureza":"RP","gravidade":"erro","contexto":"//ubl:Invoice/cac:InvoiceLine/cbc:Note | //cn:CreditNote/cac:CreditNoteLine/cbc:Note","elementos":["BT-127"],"expressao":"matches(.,'^(.{1,500})$')"},
{"id":"DT-CIUS-PT-116.1","texto":"The BT-128 does not meet the defined format: alphanumeric with size between 1 and 50.","categoria":"formato","natureza":"RP","gravidade":"erro","contexto":"//ubl:Invoice/cac:InvoiceLine/cac:DocumentReference/cbc:ID | //cn:CreditNote/cac:CreditNoteLine/cac:DocumentReference/cbc:ID","elementos":["BT-128"],"expressao":"matches(.,'^(.{1,50})$')"},
{"id":"DT-CIUS-PT-116.2","texto":"The BT-128 identification scheme identifier MUST be coded using a restriction of UNTDID 1153.","categoria":"outra","natureza":"?","gravidade":"erro","contexto":"//ubl:Invoice/cac:InvoiceLine/cac:DocumentReference/cbc:ID | //cn:CreditNote/cac:CreditNoteLine/cac:DocumentReference/cbc:ID","elementos":["BT-128"],"expressao":"report (dispara quando verdadeiro): (exists(@schemeID) and (contains(normalize-space(@schemeID), ' ') or not(contains(' AAA AAB AAC AAD AAE AAF AAG AAH AAI AAJ AAK AAL AAM AAN AAO AAP AAQ AAR AAS AAT AAU AAV AAW AAX AAY AAZ ABA ABB ABC ABD ABE ABF ABG ABH ABI ABJ ABK ABL ABM ABN ABO ABP ABQ ABR ABS ABT ABU ABV ABW ABX ABY ABZ AC ACA ACB ACC ACD ACE ACF ACG ACH ACI ACJ ACK ACL ACN ACO ACP ACQ ACR ACT ACU ACV ACW ACX ACY ACZ ADA ADB ADC ADD ADE ADF ADG ADI ADJ ADK ADL ADM ADN ADO ADP ADQ ADT ADU ADV ADW ADX ADY ADZ AE AEA AEB AEC AED AEE AEF AEG AEH AEI AEJ AEK AEL AEM AEN AEO AEP AEQ AER AES AET AEU AEV AEW AEX AEY AEZ AF AFA AFB AFC AFD AFE AFF AFG AFH AFI AFJ AFK AFL AFM AFN AFO AFP AFQ AFR AFS AFT AFU AFV AFW AFX AFY AFZ AGA AGB AGC AGD AGE AGF AGG AGH AGI AGJ AGK AGL AGM AGN AGO AGP AGQ AGR AGS AGT AGU AGV AGW AGX AGY AGZ AHA AHB AHC AHD AHE AHF AHG AHH AHI AHJ AHK AHL AHM AHN AHO AHP AHQ AHR AHS AHT AHU AHV AHX AHY AHZ AIA AIB AIC AID AIE AIF AIG AIH AII AIJ AIK AIL AIM AIN AIO AIP AIQ AIR AIS AIT AIU AIV AIW AIX AIY AIZ AJA AJB AJC AJD AJE AJF AJG AJH AJI AJJ AJK AJL AJM AJN AJO AJP AJQ AJR AJS AJT AJU AJV AJW AJX AJY AJZ AKA AKB AKC AKD AKE AKF AKG AKH AKI AKJ AKK AKL AKM AKN AKO AKP AKQ AKR AKS AKT AKU AKV AKW AKX AKY AKZ ALA ALB ALC ALD ALE ALF ALG ALH ALI ALJ ALK ALL ALM ALN ALO ALP ALQ ALR ALS ALT ALU ALV ALW ALX ALY ALZ AMA AMB AMC AMD AME AMF AMG AMH AMI AMJ AMK AML AMM AMN AMO AMP AMQ AMR AMS AMT AMU AMV AMW AMX AMY AMZ ANA ANB ANC AND ANE ANF ANG ANH ANI ANJ ANK ANL ANM ANN ANO ANP ANQ ANR ANS ANT ANU ANV ANW ANX ANY AOA AOD AOE AOF AOG AOH AOI AOJ AOK AOL AOM AON AOO AOP AOQ AOR AOS AOT AOU AOV AOW AOX AOY AOZ AP APA APB APC APD APE APF APG APH API APJ APK APL APM APN APO APP APQ APR APS APT APU APV APW APX APY APZ AQA AQB AQC AQD AQE AQF AQG AQH AQI AQJ AQK AQL AQM AQN AQO AQP AQQ AQR AQS AQT AQU AQV AQW AQX AQY AQZ ARA ARB ARC ARD ARE ARF ARG ARH ARI ARJ ARK ARL ARM ARN ARO ARP ARQ ARR ARS ART ARU ARV ARW ARX ARY ARZ ASA ASB ASC ASD ASE ASF ASG ASH ASI ASJ ASK ASL ASM ASN ASO ASP ASQ ASR ASS AST ASU ASV ASW ASX ASY ASZ ATA ATB ATC ATD ATE ATF ATG ATH ATI ATJ ATK ATL ATM ATN ATO ATP ATQ ATR ATS ATT ATU ATV ATW ATX ATY ATZ AU AUA AUB AUC AUD AUE AUF AUG AUH AUI AUJ AUK AUL AUM AUN AUO AUP AUQ AUR AUS AUT AUU AUV AUW AUX AUY AUZ AV AVA AVB AVC AVD AVE AVF AVG AVH AVI AVJ AVK AVL AVM AVN AVO AVP AVQ AVR AVS AVT AVU AVV AVW AVX AVY AVZ AWA AWB AWC AWD AWE AWF AWG AWH AWI AWJ AWK AWL AWM AWN AWO AWP AWQ AWR AWS AWT AWU AWV AWW AWX AWY AWZ AXA AXB AXC AXD AXE AXF AXG AXH AXI AXJ AXK AXL AXM AXN AXO AXP AXQ AXR BA BC BD BE BH BM BN BO BR BT BW CAS CAT CAU CAV CAW CAX CAY CAZ CBA CBB CD CEC CED CFE CFF CFO CG CH CK CKN CM CMR CN CNO COF CP CR CRN CS CST CT CU CV CW CZ DA DAN DB DI DL DM DQ DR EA EB ED EE EI EN EQ ER ERN ET EX FC FF FI FLW FN FO FS FT FV FX GA GC GD GDN GN HS HWB IA IB ICA ICE ICO II IL INB INN INO IP IS IT IV JB JE LA LAN LAR LB LC LI LO LRC LS MA MB MF MG MH MR MRN MS MSS MWB NA NF OH OI ON OP OR PB PC PD PE PF PI PK PL POR PP PQ PR PS PW PY RA RC RCN RE REN RF RR RT SA SB SD SE SEA SF SH SI SM SN SP SQ SRN SS STA SW SZ TB TCR TE TF TI TIN TL TN TP UAR UC UCN UN UO URI VA VC VGR VM VN VON VOR VP VR VS VT VV WE WM WN WR WS WY XA XC XP ZZZ ', concat(' ', normalize-space(@schemeID), ' ')))))"},
{"id":"DT-CIUS-PT-117.1","texto":"The BT-129 does not meet the defined format: decimal value with 3 decimal places and 13 unit places, than can be negative.","categoria":"formato","natureza":"RP","gravidade":"erro","contexto":"//ubl:Invoice/cac:InvoiceLine/cbc:InvoicedQuantity  | //cn:CreditNote/cac:CreditNoteLine/cbc:CreditedQuantity","elementos":["BT-129"],"expressao":"matches(.,'^(-?\\d{1,13}\\.\\d{2,3})$')"},
{"id":"DT-CIUS-PT-143","texto":"The BT-130 Unit code must be coded according to the UN/ECE Recommendation 20 with Rec 21 extension.","categoria":"outra","natureza":"?","gravidade":"erro","contexto":"//ubl:Invoice/cac:InvoiceLine/cbc:InvoicedQuantity  | //cn:CreditNote/cac:CreditNoteLine/cbc:CreditedQuantity","elementos":["BT-130"],"expressao":"((not(contains(normalize-space(@unitCode), ' ')) and contains(' 10 11 13 14 15 20 21 22 23 24 25 27 28 33 34 35 37 38 40 41 56 57 58 59 60 61 64 66 74 76 77 78 80 81 84 85 87 89 91 1I 2A 2B 2C 2G 2H 2I 2J 2K 2L 2M 2N 2P 2Q 2R 2U 2X 2Y 2Z 3B 3C 4C 4G 4H 4K 4L 4M 4N 4O 4P 4Q 4R 4T 4U 4W 4X 5A 5B 5E 5J A1 A10 A11 A12 A13 A14 A15 A16 A17 A18 A19 A2 A20 A21 A22 A23 A24 A25 A26 A27 A28 A29 A3 A30 A31 A32 A33 A34 A35 A36 A37 A38 A39 A4 A40 A41 A42 A43 A44 A45 A47 A48 A49 A5 A50 A51 A52 A53 A54 A55 A56 A57 A58 A59 A6 A60 A61 A62 A63 A64 A65 A66 A67 A68 A69 A7 A70 A71 A73 A74 A75 A76 A77 A78 A79 A8 A80 A81 A82 A83 A84 A85 A86 A87 A88 A89 A9 A90 A91 A93 A94 A95 A96 A97 A98 A99 AA AB ACR ACT AD AE AH AI AK AL AMH AMP ANN APZ AQ ARE AS ASM ASU ATM ATT AY AZ B1 B10 B11 B12 B13 B14 B15 B16 B17 B18 B19 B20 B21 B22 B23 B24 B25 B26 B27 B28 B29 B3 B30 B31 B32 B33 B34 B35 B36 B37 B38 B39 B4 B40 B41 B42 B43 B44 B45 B46 B47 B48 B49 B50 B51 B52 B53 B54 B55 B56 B57 B58 B59 B60 B61 B62 B63 B64 B65 B66 B67 B68 B69 B7 B70 B71 B72 B73 B74 B75 B76 B77 B78 B79 B8 B80 B81 B82 B83 B84 B85 B86 B87 B88 B89 B90 B91 B92 B93 B94 B95 B96 B97 B98 B99 BAR BB BFT BHP BIL BLD BLL BP BQL BTU BUA BUI C0 C10 C11 C12 C13 C14 C15 C16 C17 C18 C19 C20 C21 C22 C23 C24 C25 C26 C27 C28 C29 C3 C30 C31 C32 C33 C34 C35 C36 C37 C38 C39 C40 C41 C42 C43 C44 C45 C46 C47 C48 C49 C50 C51 C52 C53 C54 C55 C56 C57 C58 C59 C60 C61 C62 C63 C64 C65 C66 C67 C68 C69 C7 C70 C71 C72 C73 C74 C75 C76 C78 C79 C8 C80 C81 C82 C83 C84 C85 C86 C87 C88 C89 C9 C90 C91 C92 C93 C94 C95 C96 C97 C99 CCT CDL CEL CEN CG CGM CKG CLF CLT CMK CMQ CMT CNP CNT COU CTG CTM CTN CUR CWA CWI D03 D04 D1 D10 D11 D12 D13 D15 D16 D17 D18 D19 D2 D20 D21 D22 D23 D24 D25 D26 D27 D29 D30 D31 D32 D33 D34 D35 D36 D37 D38 D39 D41 D42 D43 D44 D45 D46 D47 D48 D49 D5 D50 D51 D52 D53 D54 D55 D56 D57 D58 D59 D6 D60 D61 D62 D63 D65 D68 D69 D70 D71 D72 D73 D74 D75 D76 D77 D78 D80 D81 D82 D83 D85 D86 D87 D88 D89 D9 D91 D93 D94 D95 DAA DAD DAY DB DD DEC DG DJ DLT DMA DMK DMO DMQ DMT DN DPC DPR DPT DRA DRI DRL DT DTN DU DWT DX DZN DZP E01 E07 E08 E09 E10 E11 E12 E14 E15 E16 E17 E18 E19 E20 E21 E22 E23 E25 E27 E28 E30 E31 E32 E33 E34 E35 E36 E37 E38 E39 E4 E40 E41 E42 E43 E44 E45 E46 E47 E48 E49 E50 E51 E52 E53 E54 E55 E56 E57 E58 E59 E60 E61 E62 E63 E64 E65 E66 E67 E68 E69 E70 E71 E72 E73 E74 E75 E76 E77 E78 E79 E80 E81 E82 E83 E84 E85 E86 E87 E88 E89 E90 E91 E92 E93 E94 E95 E96 E97 E98 E99 EA EB EQ F01 F02 F03 F04 F05 F06 F07 F08 F10 F11 F12 F13 F14 F15 F16 F17 F18 F19 F20 F21 F22 F23 F24 F25 F26 F27 F28 F29 F30 F31 F32 F33 F34 F35 F36 F37 F38 F39 F40 F41 F42 F43 F44 F45 F46 F47 F48 F49 F50 F51 F52 F53 F54 F55 F56 F57 F58 F59 F60 F61 F62 F63 F64 F65 F66 F67 F68 F69 F70 F71 F72 F73 F74 F75 F76 F77 F78 F79 F80 F81 F82 F83 F84 F85 F86 F87 F88 F89 F90 F91 F92 F93 F94 F95 F96 F97 F98 F99 FAH FAR FBM FC FF FH FIT FL FOT FP FR FS FTK FTQ G01 G04 G05 G06 G08 G09 G10 G11 G12 G13 G14 G15 G16 G17 G18 G19 G2 G20 G21 G23 G24 G25 G26 G27 G28 G29 G3 G30 G31 G32 G33 G34 G35 G36 G37 G38 G39 G40 G41 G42 G43 G44 G45 G46 G47 G48 G49 G50 G51 G52 G53 G54 G55 G56 G57 G58 G59 G60 G61 G62 G63 G64 G65 G66 G67 G68 G69 G70 G71 G72 G73 G74 G75 G76 G77 G78 G79 G80 G81 G82 G83 G84 G85 G86 G87 G88 G89 G90 G91 G92 G93 G94 G95 G96 G97 G98 G99 GB GBQ GDW GE GF GFI GGR GIA GIC GII GIP GJ GL GLD GLI GLL GM GO GP GQ GRM GRN GRO GRT GT GV GWH H03 H04 H05 H06 H07 H08 H09 H10 H11 H12 H13 H14 H15 H16 H18 H19 H20 H21 H22 H23 H24 H25 H26 H27 H28 H29 H30 H31 H32 H33 H34 H35 H36 H37 H38 H39 H40 H41 H42 H43 H44 H45 H46 H47 H48 H49 H50 H51 H52 H53 H54 H55 H56 H57 H58 H59 H60 H61 H62 H63 H64 H65 H66 H67 H68 H69 H70 H71 H72 H73 H74 H75 H76 H77 H78 H79 H80 H81 H82 H83 H84 H85 H87 H88 H89 H90 H91 H92 H93 H94 H95 H96 H98 H99 HA HAR HBA HBX HC HDW HEA HGM HH HIU HJ HKM HLT HM HMQ HMT HN HP HPA HTZ HUR IA IE INH INK INQ ISD IU IV J10 J12 J13 J14 J15 J16 J17 J18 J19 J2 J20 J21 J22 J23 J24 J25 J26 J27 J28 J29 J30 J31 J32 J33 J34 J35 J36 J38 J39 J40 J41 J42 J43 J44 J45 J46 J47 J48 J49 J50 J51 J52 J53 J54 J55 J56 J57 J58 J59 J60 J61 J62 J63 J64 J65 J66 J67 J68 J69 J70 J71 J72 J73 J74 J75 J76 J78 J79 J81 J82 J83 J84 J85 J87 J89 J90 J91 J92 J93 J94 J95 J96 J97 J98 J99 JE JK JM JNT JOU JPS JWL K1 K10 K11 K12 K13 K14 K15 K16 K17 K18 K19 K2 K20 K21 K22 K23 K24 K25 K26 K27 K28 K3 K30 K31 K32 K33 K34 K35 K36 K37 K38 K39 K40 K41 K42 K43 K45 K46 K47 K48 K49 K5 K50 K51 K52 K53 K54 K55 K58 K59 K6 K60 K61 K62 K63 K64 K65 K66 K67 K68 K69 K70 K71 K73 K74 K75 K76 K77 K78 K79 K80 K81 K82 K83 K84 K85 K86 K87 K88 K89 K90 K91 K92 K93 K94 K95 K96 K97 K98 K99 KA KAT KB KBA KCC KDW KEL KGM KGS KHY KHZ KI KIC KIP KJ KJO KL KLK KLX KMA KMH KMK KMQ KMT KNI KNS KNT KO KPA KPH KPO KPP KR KSD KSH KT KTN KUR KVA KVR KVT KW KWH KWO KWT KX L10 L11 L12 L13 L14 L15 L16 L17 L18 L19 L2 L20 L21 L23 L24 L25 L26 L27 L28 L29 L30 L31 L32 L33 L34 L35 L36 L37 L38 L39 L40 L41 L42 L43 L44 L45 L46 L47 L48 L49 L50 L51 L52 L53 L54 L55 L56 L57 L58 L59 L60 L63 L64 L65 L66 L67 L68 L69 L70 L71 L72 L73 L74 L75 L76 L77 L78 L79 L80 L81 L82 L83 L84 L85 L86 L87 L88 L89 L90 L91 L92 L93 L94 L95 L96 L98 L99 LA LAC LBR LBT LD LEF LF LH LK LM LN LO LP LPA LR LS LTN LTR LUB LUM LUX LY M1 M10 M11 M12 M13 M14 M15 M16 M17 M18 M19 M20 M21 M22 M23 M24 M25 M26 M27 M29 M30 M31 M32 M33 M34 M35 M36 M37 M38 M39 M4 M40 M41 M42 M43 M44 M45 M46 M47 M48 M49 M5 M50 M51 M52 M53 M55 M56 M57 M58 M59 M60 M61 M62 M63 M64 M65 M66 M67 M68 M69 M7 M70 M71 M72 M73 M74 M75 M76 M77 M78 M79 M80 M81 M82 M83 M84 M85 M86 M87 M88 M89 M9 M90 M91 M92 M93 M94 M95 M96 M97 M98 M99 MAH MAL MAM MAR MAW MBE MBF MBR MC MCU MD MGM MHZ MIK MIL MIN MIO MIU MLD MLT MMK MMQ MMT MND MON MPA MQH MQS MSK MTK MTQ MTR MTS MVA MWH N1 N10 N11 N12 N13 N14 N15 N16 N17 N18 N19 N20 N21 N22 N23 N24 N25 N26 N27 N28 N29 N3 N30 N31 N32 N33 N34 N35 N36 N37 N38 N39 N40 N41 N42 N43 N44 N45 N46 N47 N48 N49 N50 N51 N52 N53 N54 N55 N56 N57 N58 N59 N60 N61 N62 N63 N64 N65 N66 N67 N68 N69 N70 N71 N72 N73 N74 N75 N76 N77 N78 N79 N80 N81 N82 N83 N84 N85 N86 N87 N88 N89 N90 N91 N92 N93 N94 N95 N96 N97 N98 N99 NA NAR NCL NEW NF NIL NIU NL NMI NMP NPR NPT NQ NR NT NTT NU NX OA ODE OHM ON ONZ OT OZ OZA OZI P1 P10 P11 P12 P13 P14 P15 P16 P17 P18 P19 P2 P20 P21 P22 P23 P24 P25 P26 P27 P28 P29 P30 P31 P32 P33 P34 P35 P36 P37 P38 P39 P40 P41 P42 P43 P44 P45 P46 P47 P48 P49 P5 P50 P51 P52 P53 P54 P55 P56 P57 P58 P59 P60 P61 P62 P63 P64 P65 P66 P67 P68 P69 P70 P71 P72 P73 P74 P75 P76 P77 P78 P79 P80 P81 P82 P83 P84 P85 P86 P87 P88 P89 P90 P91 P92 P93 P94 P95 P96 P97 P98 P99 PAL PD PFL PGL PI PLA PO PQ PR PS PT PTD PTI PTL Q10 Q11 Q12 Q13 Q14 Q15 Q16 Q17 Q18 Q19 Q20 Q21 Q22 Q23 Q24 Q25 Q26 Q27 Q28 Q3 QA QAN QB QR QT QTD QTI QTL QTR R1 R9 RH RM ROM RP RPM RPS RT S3 S4 SAN SCO SCR SEC SET SG SHT SIE SMI SQ SQR SR STC STI STK STL STN STW SW SX SYR T0 T3 TAH TAN TI TIC TIP TKM TMS TNE TP TPR TQD TRL TST TTS U1 U2 UA UB UC VA VLT VP W2 WA WB WCD WE WEB WEE WG WHR WM WSD WTT WW X1 YDK YDQ YRD Z11 ZP ZZ X43 X44 X1A X1B X1D X1F X1G X1W X2C X3A X3H X4A X4B X4C X4D X4F X4G X4H X5H X5L X5M X6H X6P X7A X7B X8A X8B X8C XAA XAB XAC XAD XAE XAF XAG XAH XAI XAJ XAL XAM XAP XAT XAV XB4 XBA XBB XBC XBD XBE XBF XBG XBH XBI XBJ XBK XBL XBM XBN XBO XBP XBQ XBR XBS XBT XBU XBV XBW XBX XBY XBZ XCA XCB XCC XCD XCE XCF XCG XCH XCI XCJ XCK XCL XCM XCN XCO XCP XCQ XCR XCS XCT XCU XCV XCW XCX XCY XCZ XDA XDB XDC XDG XDH XDI XDJ XDK XDL XDM XDN XDP XDR XDS XDT XDU XDV XDW XDX XDY XEC XED XEE XEF XEG XEH XEI XEN XFB XFC XFD XFE XFI XFL XFO XFP XFR XFT XFW XFX XGB XGI XGL XGR XGU XGY XGZ XHA XHB XHC XHG XHN XHR XIA XIB XIC XID XIE XIF XIG XIH XIK XIL XIN XIZ XJB XJC XJG XJR XJT XJY XKG XKI XLE XLG XLT XLU XLV XLZ XMA XMB XMC XME XMR XMS XMT XMW XMX XNA XNE XNF XNG XNS XNT XNU XNV XOA XOB XOC XOD XOE XOF XOK XOT XOU XP2 XPA XPB XPC XPD XPE XPF XPG XPH XPI XPJ XPK XPL XPN XPO XPP XPR XPT XPU XPV XPX XPY XPZ XQA XQB XQC XQD XQF XQG XQH XQJ XQK XQL XQM XQN XQP XQQ XQR XQS XRD XRG XRJ XRK XRL XRO XRT XRZ XSA XSB XSC XSD XSE XSH XSI XSK XSL XSM XSO XSP XSS XST XSU XSV XSW XSY XSZ XT1 XTB XTC XTD XTE XTG XTI XTK XTL XTN XTO XTR XTS XTT XTU XTV XTW XTY XTZ XUC XUN XVA XVG XVI XVK XVL XVN XVO XVP XVQ XVR XVS XVY XWA XWB XWC XWD XWF XWG XWH XWJ XWK XWL XWM XWN XWP XWQ XWR XWS XWT XWU XWV XWW XWX XWY XWZ XXA XXB XXC XXD XXF XXG XXH XXJ XXK XYA XYB XYC XYD XYF XYG XYH XYJ XYK XYL XYM XYN XYP XYQ XYR XYS XYT XYV XYW XYX XYY XYZ XZA XZB XZC XZD XZF XZG XZH XZJ XZK XZL XZM XZN XZP XZQ XZR XZS XZT XZU XZV XZW XZX XZY XZZ ', concat(' ', normalize-space(@unitCode), ' '))))"},
{"id":"DT-CIUS-PT-118.1","texto":"The BT-131 does not meet the defined format: decimal value with 8 decimal places and 13 unit places, than can be negative.","categoria":"formato","natureza":"RP","gravidade":"erro","contexto":"//ubl:Invoice/cac:InvoiceLine/cbc:LineExtensionAmount  | //cn:CreditNote/cac:CreditNoteLine/cbc:LineExtensionAmount","elementos":["BT-131"],"expressao":"matches(.,'^(-?\\d{1,13}\\.\\d{2,8})$')"},
{"id":"DT-CIUS-PT-118.2","texto":"The BT-131 currencyID must be equal to BT-5.","categoria":"outra","natureza":"?","gravidade":"erro","contexto":"//ubl:Invoice/cac:InvoiceLine/cbc:LineExtensionAmount  | //cn:CreditNote/cac:CreditNoteLine/cbc:LineExtensionAmount","elementos":["BT-5","BT-131"],"expressao":"normalize-space(@currencyID)= $bt05"},
{"id":"DT-CIUS-PT-119","texto":"The BT-132 does not meet the defined format: alphanumeric with size between 1 and 20.","categoria":"formato","natureza":"RP","gravidade":"erro","contexto":"//ubl:Invoice/cac:InvoiceLine/cac:OrderLineReference/cbc:LineID | //cn:CreditNote/cac:CreditNoteLine/cac:OrderLineReference/cbc:LineID","elementos":["BT-132"],"expressao":"matches(.,'^(.{1,20})$')"},
{"id":"DT-CIUS-PT-120","texto":"The BT-133 does not meet the defined format: alphanumeric with size between 1 and 200.","categoria":"formato","natureza":"RP","gravidade":"erro","contexto":"//ubl:Invoice/cac:InvoiceLine/cbc:AccountingCost | //cn:CreditNote/cac:CreditNoteLine/cbc:AccountingCost","elementos":["BT-133"],"expressao":"matches(.,'^(.{1,200})$')"},
{"id":"DT-CIUS-PT-121","texto":"The BT-134 does not meet the defined format: YYYY-MM-DD.","categoria":"formato","natureza":"RP","gravidade":"erro","contexto":"//ubl:Invoice/cac:InvoiceLine/cac:InvoicePeriod/cbc:StartDate | //cn:CreditNote/cac:CreditNoteLine/cac:InvoicePeriod/cbc:StartDate","elementos":["BT-134"],"expressao":"matches(.,'^((\\d{4})-(\\d{2})-(\\d{2}))$')"},
{"id":"DT-CIUS-PT-122","texto":"The BT-135 does not meet the defined format: YYYY-MM-DD.","categoria":"formato","natureza":"RP","gravidade":"erro","contexto":"//ubl:Invoice/cac:InvoiceLine/cac:InvoicePeriod/cbc:EndDate | //cn:CreditNote/cac:CreditNoteLine/cac:InvoicePeriod/cbc:EndDate","elementos":["BT-135"],"expressao":"matches(.,'^((\\d{4})-(\\d{2})-(\\d{2}))$')"},
{"id":"DT-CIUS-PT-123.1","texto":"The BT-136 and BT-141 does not meet the defined format: decimal value with 2 decimal places and 13 unit places.","categoria":"formato","natureza":"RP","gravidade":"erro","contexto":"//ubl:Invoice/cac:InvoiceLine/cac:AllowanceCharge/cbc:Amount | //cn:CreditNote/cac:CreditNoteLine/cac:AllowanceCharge/cbc:Amount","elementos":["BT-136","BT-141"],"expressao":"matches(.,'^(\\d{1,13}\\.\\d{2})$')"},
{"id":"DT-CIUS-PT-123.2","texto":"The BT-136 and BT-141 currencyID must be equal to BT-5.","categoria":"outra","natureza":"?","gravidade":"erro","contexto":"//ubl:Invoice/cac:InvoiceLine/cac:AllowanceCharge/cbc:Amount | //cn:CreditNote/cac:CreditNoteLine/cac:AllowanceCharge/cbc:Amount","elementos":["BT-5","BT-136","BT-141"],"expressao":"normalize-space(@currencyID)= $bt05"},
{"id":"DT-CIUS-PT-124.1","texto":"The BT-137 and BT-142 does not meet the defined format: decimal value with 2 decimal places and 13 unit places.","categoria":"formato","natureza":"RP","gravidade":"erro","contexto":"//ubl:Invoice/cac:InvoiceLine/cac:AllowanceCharge/cbc:BaseAmount | //cn:CreditNote/cac:CreditNoteLine/cac:AllowanceCharge/cbc:BaseAmount","elementos":["BT-137","BT-142"],"expressao":"matches(.,'^(\\d{1,13}\\.\\d{2})$')"},
{"id":"DT-CIUS-PT-124.2","texto":"The BT-137 and BT-142 currencyID must be equal to BT-5.","categoria":"outra","natureza":"?","gravidade":"erro","contexto":"//ubl:Invoice/cac:InvoiceLine/cac:AllowanceCharge/cbc:BaseAmount | //cn:CreditNote/cac:CreditNoteLine/cac:AllowanceCharge/cbc:BaseAmount","elementos":["BT-5","BT-137","BT-142"],"expressao":"normalize-space(@currencyID)= $bt05"},
{"id":"DT-CIUS-PT-125.1","texto":"The BT-138 and BT-143 does not meet the defined format: decimal value with 2 decimal places and 3 unit places.","categoria":"formato","natureza":"RP","gravidade":"erro","contexto":"//ubl:Invoice/cac:InvoiceLine/cac:AllowanceCharge/cbc:MultiplierFactorNumeric | //cn:CreditNote/cac:CreditNoteLine/cac:AllowanceCharge/cbc:MultiplierFactorNumeric","elementos":["BT-138","BT-143"],"expressao":"matches(.,'^(\\d{1,3}\\.\\d{2})$')"},
{"id":"DT-CIUS-PT-125.2","texto":"The BT-138 and BT-143 does not meet the defined format: value between 0.01 and 100.00.","categoria":"formato","natureza":"RP","gravidade":"erro","contexto":"//ubl:Invoice/cac:InvoiceLine/cac:AllowanceCharge/cbc:MultiplierFactorNumeric | //cn:CreditNote/cac:CreditNoteLine/cac:AllowanceCharge/cbc:MultiplierFactorNumeric","elementos":["BT-138","BT-143"],"expressao":"report (dispara quando verdadeiro): matches(.,'^(\\d{1,3}\\.\\d{2})$') and (xs:decimal(.) < 0.00 or xs:decimal(.) > 100.00)"},
{"id":"DT-CIUS-PT-126","texto":"The BT-139 and BT-144 does not meet the defined format: alphanumeric with size between 1 and 200.","categoria":"formato","natureza":"RP","gravidade":"erro","contexto":"//ubl:Invoice/cac:InvoiceLine/cac:AllowanceCharge/cbc:AllowanceChargeReason | //cn:CreditNote/cac:CreditNoteLine/cac:AllowanceCharge/cbc:AllowanceChargeReason","elementos":["BT-139","BT-144"],"expressao":"matches(.,'^(.{1,200})$')"},
{"id":"DT-CIUS-PT-147","texto":"The BT-140 must belong to the UNCL 5189 code list.","categoria":"valores","natureza":"RP","gravidade":"erro","contexto":"//ubl:Invoice/cac:InvoiceLine/cac:AllowanceCharge[cbc:ChargeIndicator = 'false']/cbc:AllowanceChargeReasonCode | //cn:CreditNote/cac:CreditNoteLine/cac:AllowanceCharge[cbc:ChargeIndicator = 'false']/cbc:AllowanceChargeReasonCode","elementos":["BT-140"],"expressao":"((not(contains(normalize-space(.), ' ')) and contains(' 41 42 60 62 63 64 65 66 67 68 70 71 88 95 100 102 103 104 105 ', concat(' ', normalize-space(.), ' '))))"},
{"id":"DT-CIUS-PT-148","texto":"The BT-145 must belong to the UNCL 7161 code list.","categoria":"valores","natureza":"RP","gravidade":"erro","contexto":"//ubl:Invoice/cac:InvoiceLine/cac:AllowanceCharge[cbc:ChargeIndicator = 'true']/cbc:AllowanceChargeReasonCode | //cn:CreditNote/cac:CreditNoteLine/cac:AllowanceCharge[cbc:ChargeIndicator = 'true']/cbc:AllowanceChargeReasonCode","elementos":["BT-145"],"expressao":"((not(contains(normalize-space(.), ' ')) and contains(' AA AAA AAC AAD AAE AAF AAH AAI AAS AAT AAV AAY AAZ ABA ABB ABC ABD ABF ABK ABL ABN ABR ABS ABT ABU ACF ACG ACH ACI ACJ ACK ACL ACM ACS ADC ADE ADF ADJ ADK ADL ADM ADN ADO ADP ADQ ADR ADT ADW ADY ADZ AEA AEB AEC AED AEF AEH AEI AEJ AEK AEL AEM AEN AEO AEP AES AET AEU AEV AEW AEX AEY AEZ AJ AU CA CAB CAD CAE CAF CAI CAJ CAK CAL CAM CAN CAO CAP CAQ CAR CAS CAT CAU CAV CAW CD CG CS CT DAB DAD DL EG EP ER FAA FAB FAC FC FH FI GAA HAA HD HH IAA IAB ID IF IR IS KO L1 LA LAA LAB LF MAE MI ML NAA OA PA PAA PC PL RAB RAC RAD RAF RE RF RH RV SA SAA SAD SAE SAI SG SH SM ST SU TAB TAC TT TV V1 V2 WH XAA YY ZZZ ', concat(' ', normalize-space(.), ' '))))"},
{"id":"DT-CIUS-PT-127.1","texto":"The BT-146 does not meet the defined format: decimal value with 8 decimal places and 13 unit places.","categoria":"formato","natureza":"RP","gravidade":"erro","contexto":"//ubl:Invoice/cac:InvoiceLine/cac:Price/cbc:PriceAmount  | //cn:CreditNote/cac:CreditNoteLine/cac:Price/cbc:PriceAmount","elementos":["BT-146"],"expressao":"matches(.,'^(\\d{1,13}\\.\\d{2,8})$')"},
{"id":"DT-CIUS-PT-127.2","texto":"The BT-146 currencyID must be equal to BT-5.","categoria":"outra","natureza":"?","gravidade":"erro","contexto":"//ubl:Invoice/cac:InvoiceLine/cac:Price/cbc:PriceAmount  | //cn:CreditNote/cac:CreditNoteLine/cac:Price/cbc:PriceAmount","elementos":["BT-5","BT-146"],"expressao":"normalize-space(@currencyID)= $bt05"},
{"id":"DT-CIUS-PT-128.1","texto":"The BT-147 does not meet the defined format: decimal value with 8 decimal places and 13 unit places.","categoria":"formato","natureza":"RP","gravidade":"erro","contexto":"//ubl:Invoice/cac:InvoiceLine/cac:Price/cac:AllowanceCharge/cbc:Amount | //cn:CreditNote/cac:CreditNoteLine/cac:Price/cac:AllowanceCharge/cbc:Amount","elementos":["BT-147"],"expressao":"matches(.,'^(\\d{1,13}\\.\\d{2,8})$')"},
{"id":"DT-CIUS-PT-128.2","texto":"The BT-147 currencyID must be equal to BT-5.","categoria":"outra","natureza":"?","gravidade":"erro","contexto":"//ubl:Invoice/cac:InvoiceLine/cac:Price/cac:AllowanceCharge/cbc:Amount | //cn:CreditNote/cac:CreditNoteLine/cac:Price/cac:AllowanceCharge/cbc:Amount","elementos":["BT-5","BT-147"],"expressao":"normalize-space(@currencyID)= $bt05"},
{"id":"DT-CIUS-PT-129.1","texto":"The BT-148 does not meet the defined format: decimal value with 8 decimal places and 13 unit places.","categoria":"formato","natureza":"RP","gravidade":"erro","contexto":"//ubl:Invoice/cac:InvoiceLine/cac:Price/cac:AllowanceCharge/cbc:BaseAmount  | //cn:CreditNote/cac:CreditNoteLine/cac:Price/cac:AllowanceCharge/cbc:BaseAmount","elementos":["BT-148"],"expressao":"matches(.,'^(\\d{1,13}\\.\\d{2,8})$')"},
{"id":"DT-CIUS-PT-129.2","texto":"The BT-148 currencyID must be equal to BT-5.","categoria":"outra","natureza":"?","gravidade":"erro","contexto":"//ubl:Invoice/cac:InvoiceLine/cac:Price/cac:AllowanceCharge/cbc:BaseAmount  | //cn:CreditNote/cac:CreditNoteLine/cac:Price/cac:AllowanceCharge/cbc:BaseAmount","elementos":["BT-5","BT-148"],"expressao":"normalize-space(@currencyID)= $bt05"},
{"id":"DT-CIUS-PT-130.1","texto":"The BT-149 does not meet the defined format: decimal value with 3 decimal places and 13 unit places.","categoria":"formato","natureza":"RP","gravidade":"erro","contexto":"//ubl:Invoice/cac:InvoiceLine/cac:Price/cbc:BaseQuantity  | //cn:CreditNote/cac:CreditNoteLine/cac:Price/cbc:BaseQuantity","elementos":["BT-149"],"expressao":"matches(.,'^(\\d{1,13}\\.\\d{2,3})$')"},
{"id":"DT-CIUS-PT-130.2","texto":"The BT-149 Unit code must be coded according to the UN/ECE Recommendation 20 with Rec 21 extension.","categoria":"outra","natureza":"?","gravidade":"erro","contexto":"//ubl:Invoice/cac:InvoiceLine/cac:Price/cbc:BaseQuantity  | //cn:CreditNote/cac:CreditNoteLine/cac:Price/cbc:BaseQuantity","elementos":["BT-149"],"expressao":"report (dispara quando verdadeiro): (exists(@unitCode) and (contains(normalize-space(@unitCode), ' ') or not(contains(' 10 11 13 14 15 20 21 22 23 24 25 27 28 33 34 35 37 38 40 41 56 57 58 59 60 61 64 66 74 76 77 78 80 81 84 85 87 89 91 1I 2A 2B 2C 2G 2H 2I 2J 2K 2L 2M 2N 2P 2Q 2R 2U 2X 2Y 2Z 3B 3C 4C 4G 4H 4K 4L 4M 4N 4O 4P 4Q 4R 4T 4U 4W 4X 5A 5B 5E 5J A1 A10 A11 A12 A13 A14 A15 A16 A17 A18 A19 A2 A20 A21 A22 A23 A24 A25 A26 A27 A28 A29 A3 A30 A31 A32 A33 A34 A35 A36 A37 A38 A39 A4 A40 A41 A42 A43 A44 A45 A47 A48 A49 A5 A50 A51 A52 A53 A54 A55 A56 A57 A58 A59 A6 A60 A61 A62 A63 A64 A65 A66 A67 A68 A69 A7 A70 A71 A73 A74 A75 A76 A77 A78 A79 A8 A80 A81 A82 A83 A84 A85 A86 A87 A88 A89 A9 A90 A91 A93 A94 A95 A96 A97 A98 A99 AA AB ACR ACT AD AE AH AI AK AL AMH AMP ANN APZ AQ ARE AS ASM ASU ATM ATT AY AZ B1 B10 B11 B12 B13 B14 B15 B16 B17 B18 B19 B20 B21 B22 B23 B24 B25 B26 B27 B28 B29 B3 B30 B31 B32 B33 B34 B35 B36 B37 B38 B39 B4 B40 B41 B42 B43 B44 B45 B46 B47 B48 B49 B50 B51 B52 B53 B54 B55 B56 B57 B58 B59 B60 B61 B62 B63 B64 B65 B66 B67 B68 B69 B7 B70 B71 B72 B73 B74 B75 B76 B77 B78 B79 B8 B80 B81 B82 B83 B84 B85 B86 B87 B88 B89 B90 B91 B92 B93 B94 B95 B96 B97 B98 B99 BAR BB BFT BHP BIL BLD BLL BP BQL BTU BUA BUI C0 C10 C11 C12 C13 C14 C15 C16 C17 C18 C19 C20 C21 C22 C23 C24 C25 C26 C27 C28 C29 C3 C30 C31 C32 C33 C34 C35 C36 C37 C38 C39 C40 C41 C42 C43 C44 C45 C46 C47 C48 C49 C50 C51 C52 C53 C54 C55 C56 C57 C58 C59 C60 C61 C62 C63 C64 C65 C66 C67 C68 C69 C7 C70 C71 C72 C73 C74 C75 C76 C78 C79 C8 C80 C81 C82 C83 C84 C85 C86 C87 C88 C89 C9 C90 C91 C92 C93 C94 C95 C96 C97 C99 CCT CDL CEL CEN CG CGM CKG CLF CLT CMK CMQ CMT CNP CNT COU CTG CTM CTN CUR CWA CWI D03 D04 D1 D10 D11 D12 D13 D15 D16 D17 D18 D19 D2 D20 D21 D22 D23 D24 D25 D26 D27 D29 D30 D31 D32 D33 D34 D35 D36 D37 D38 D39 D41 D42 D43 D44 D45 D46 D47 D48 D49 D5 D50 D51 D52 D53 D54 D55 D56 D57 D58 D59 D6 D60 D61 D62 D63 D65 D68 D69 D70 D71 D72 D73 D74 D75 D76 D77 D78 D80 D81 D82 D83 D85 D86 D87 D88 D89 D9 D91 D93 D94 D95 DAA DAD DAY DB DD DEC DG DJ DLT DMA DMK DMO DMQ DMT DN DPC DPR DPT DRA DRI DRL DT DTN DU DWT DX DZN DZP E01 E07 E08 E09 E10 E11 E12 E14 E15 E16 E17 E18 E19 E20 E21 E22 E23 E25 E27 E28 E30 E31 E32 E33 E34 E35 E36 E37 E38 E39 E4 E40 E41 E42 E43 E44 E45 E46 E47 E48 E49 E50 E51 E52 E53 E54 E55 E56 E57 E58 E59 E60 E61 E62 E63 E64 E65 E66 E67 E68 E69 E70 E71 E72 E73 E74 E75 E76 E77 E78 E79 E80 E81 E82 E83 E84 E85 E86 E87 E88 E89 E90 E91 E92 E93 E94 E95 E96 E97 E98 E99 EA EB EQ F01 F02 F03 F04 F05 F06 F07 F08 F10 F11 F12 F13 F14 F15 F16 F17 F18 F19 F20 F21 F22 F23 F24 F25 F26 F27 F28 F29 F30 F31 F32 F33 F34 F35 F36 F37 F38 F39 F40 F41 F42 F43 F44 F45 F46 F47 F48 F49 F50 F51 F52 F53 F54 F55 F56 F57 F58 F59 F60 F61 F62 F63 F64 F65 F66 F67 F68 F69 F70 F71 F72 F73 F74 F75 F76 F77 F78 F79 F80 F81 F82 F83 F84 F85 F86 F87 F88 F89 F90 F91 F92 F93 F94 F95 F96 F97 F98 F99 FAH FAR FBM FC FF FH FIT FL FOT FP FR FS FTK FTQ G01 G04 G05 G06 G08 G09 G10 G11 G12 G13 G14 G15 G16 G17 G18 G19 G2 G20 G21 G23 G24 G25 G26 G27 G28 G29 G3 G30 G31 G32 G33 G34 G35 G36 G37 G38 G39 G40 G41 G42 G43 G44 G45 G46 G47 G48 G49 G50 G51 G52 G53 G54 G55 G56 G57 G58 G59 G60 G61 G62 G63 G64 G65 G66 G67 G68 G69 G70 G71 G72 G73 G74 G75 G76 G77 G78 G79 G80 G81 G82 G83 G84 G85 G86 G87 G88 G89 G90 G91 G92 G93 G94 G95 G96 G97 G98 G99 GB GBQ GDW GE GF GFI GGR GIA GIC GII GIP GJ GL GLD GLI GLL GM GO GP GQ GRM GRN GRO GRT GT GV GWH H03 H04 H05 H06 H07 H08 H09 H10 H11 H12 H13 H14 H15 H16 H18 H19 H20 H21 H22 H23 H24 H25 H26 H27 H28 H29 H30 H31 H32 H33 H34 H35 H36 H37 H38 H39 H40 H41 H42 H43 H44 H45 H46 H47 H48 H49 H50 H51 H52 H53 H54 H55 H56 H57 H58 H59 H60 H61 H62 H63 H64 H65 H66 H67 H68 H69 H70 H71 H72 H73 H74 H75 H76 H77 H78 H79 H80 H81 H82 H83 H84 H85 H87 H88 H89 H90 H91 H92 H93 H94 H95 H96 H98 H99 HA HAR HBA HBX HC HDW HEA HGM HH HIU HJ HKM HLT HM HMQ HMT HN HP HPA HTZ HUR IA IE INH INK INQ ISD IU IV J10 J12 J13 J14 J15 J16 J17 J18 J19 J2 J20 J21 J22 J23 J24 J25 J26 J27 J28 J29 J30 J31 J32 J33 J34 J35 J36 J38 J39 J40 J41 J42 J43 J44 J45 J46 J47 J48 J49 J50 J51 J52 J53 J54 J55 J56 J57 J58 J59 J60 J61 J62 J63 J64 J65 J66 J67 J68 J69 J70 J71 J72 J73 J74 J75 J76 J78 J79 J81 J82 J83 J84 J85 J87 J89 J90 J91 J92 J93 J94 J95 J96 J97 J98 J99 JE JK JM JNT JOU JPS JWL K1 K10 K11 K12 K13 K14 K15 K16 K17 K18 K19 K2 K20 K21 K22 K23 K24 K25 K26 K27 K28 K3 K30 K31 K32 K33 K34 K35 K36 K37 K38 K39 K40 K41 K42 K43 K45 K46 K47 K48 K49 K5 K50 K51 K52 K53 K54 K55 K58 K59 K6 K60 K61 K62 K63 K64 K65 K66 K67 K68 K69 K70 K71 K73 K74 K75 K76 K77 K78 K79 K80 K81 K82 K83 K84 K85 K86 K87 K88 K89 K90 K91 K92 K93 K94 K95 K96 K97 K98 K99 KA KAT KB KBA KCC KDW KEL KGM KGS KHY KHZ KI KIC KIP KJ KJO KL KLK KLX KMA KMH KMK KMQ KMT KNI KNS KNT KO KPA KPH KPO KPP KR KSD KSH KT KTN KUR KVA KVR KVT KW KWH KWO KWT KX L10 L11 L12 L13 L14 L15 L16 L17 L18 L19 L2 L20 L21 L23 L24 L25 L26 L27 L28 L29 L30 L31 L32 L33 L34 L35 L36 L37 L38 L39 L40 L41 L42 L43 L44 L45 L46 L47 L48 L49 L50 L51 L52 L53 L54 L55 L56 L57 L58 L59 L60 L63 L64 L65 L66 L67 L68 L69 L70 L71 L72 L73 L74 L75 L76 L77 L78 L79 L80 L81 L82 L83 L84 L85 L86 L87 L88 L89 L90 L91 L92 L93 L94 L95 L96 L98 L99 LA LAC LBR LBT LD LEF LF LH LK LM LN LO LP LPA LR LS LTN LTR LUB LUM LUX LY M1 M10 M11 M12 M13 M14 M15 M16 M17 M18 M19 M20 M21 M22 M23 M24 M25 M26 M27 M29 M30 M31 M32 M33 M34 M35 M36 M37 M38 M39 M4 M40 M41 M42 M43 M44 M45 M46 M47 M48 M49 M5 M50 M51 M52 M53 M55 M56 M57 M58 M59 M60 M61 M62 M63 M64 M65 M66 M67 M68 M69 M7 M70 M71 M72 M73 M74 M75 M76 M77 M78 M79 M80 M81 M82 M83 M84 M85 M86 M87 M88 M89 M9 M90 M91 M92 M93 M94 M95 M96 M97 M98 M99 MAH MAL MAM MAR MAW MBE MBF MBR MC MCU MD MGM MHZ MIK MIL MIN MIO MIU MLD MLT MMK MMQ MMT MND MON MPA MQH MQS MSK MTK MTQ MTR MTS MVA MWH N1 N10 N11 N12 N13 N14 N15 N16 N17 N18 N19 N20 N21 N22 N23 N24 N25 N26 N27 N28 N29 N3 N30 N31 N32 N33 N34 N35 N36 N37 N38 N39 N40 N41 N42 N43 N44 N45 N46 N47 N48 N49 N50 N51 N52 N53 N54 N55 N56 N57 N58 N59 N60 N61 N62 N63 N64 N65 N66 N67 N68 N69 N70 N71 N72 N73 N74 N75 N76 N77 N78 N79 N80 N81 N82 N83 N84 N85 N86 N87 N88 N89 N90 N91 N92 N93 N94 N95 N96 N97 N98 N99 NA NAR NCL NEW NF NIL NIU NL NMI NMP NPR NPT NQ NR NT NTT NU NX OA ODE OHM ON ONZ OT OZ OZA OZI P1 P10 P11 P12 P13 P14 P15 P16 P17 P18 P19 P2 P20 P21 P22 P23 P24 P25 P26 P27 P28 P29 P30 P31 P32 P33 P34 P35 P36 P37 P38 P39 P40 P41 P42 P43 P44 P45 P46 P47 P48 P49 P5 P50 P51 P52 P53 P54 P55 P56 P57 P58 P59 P60 P61 P62 P63 P64 P65 P66 P67 P68 P69 P70 P71 P72 P73 P74 P75 P76 P77 P78 P79 P80 P81 P82 P83 P84 P85 P86 P87 P88 P89 P90 P91 P92 P93 P94 P95 P96 P97 P98 P99 PAL PD PFL PGL PI PLA PO PQ PR PS PT PTD PTI PTL Q10 Q11 Q12 Q13 Q14 Q15 Q16 Q17 Q18 Q19 Q20 Q21 Q22 Q23 Q24 Q25 Q26 Q27 Q28 Q3 QA QAN QB QR QT QTD QTI QTL QTR R1 R9 RH RM ROM RP RPM RPS RT S3 S4 SAN SCO SCR SEC SET SG SHT SIE SMI SQ SQR SR STC STI STK STL STN STW SW SX SYR T0 T3 TAH TAN TI TIC TIP TKM TMS TNE TP TPR TQD TRL TST TTS U1 U2 UA UB UC VA VLT VP W2 WA WB WCD WE WEB WEE WG WHR WM WSD WTT WW X1 YDK YDQ YRD Z11 ZP ZZ X43 X44 X1A X1B X1D X1F X1G X1W X2C X3A X3H X4A X4B X4C X4D X4F X4G X4H X5H X5L X5M X6H X6P X7A X7B X8A X8B X8C XAA XAB XAC XAD XAE XAF XAG XAH XAI XAJ XAL XAM XAP XAT XAV XB4 XBA XBB XBC XBD XBE XBF XBG XBH XBI XBJ XBK XBL XBM XBN XBO XBP XBQ XBR XBS XBT XBU XBV XBW XBX XBY XBZ XCA XCB XCC XCD XCE XCF XCG XCH XCI XCJ XCK XCL XCM XCN XCO XCP XCQ XCR XCS XCT XCU XCV XCW XCX XCY XCZ XDA XDB XDC XDG XDH XDI XDJ XDK XDL XDM XDN XDP XDR XDS XDT XDU XDV XDW XDX XDY XEC XED XEE XEF XEG XEH XEI XEN XFB XFC XFD XFE XFI XFL XFO XFP XFR XFT XFW XFX XGB XGI XGL XGR XGU XGY XGZ XHA XHB XHC XHG XHN XHR XIA XIB XIC XID XIE XIF XIG XIH XIK XIL XIN XIZ XJB XJC XJG XJR XJT XJY XKG XKI XLE XLG XLT XLU XLV XLZ XMA XMB XMC XME XMR XMS XMT XMW XMX XNA XNE XNF XNG XNS XNT XNU XNV XOA XOB XOC XOD XOE XOF XOK XOT XOU XP2 XPA XPB XPC XPD XPE XPF XPG XPH XPI XPJ XPK XPL XPN XPO XPP XPR XPT XPU XPV XPX XPY XPZ XQA XQB XQC XQD XQF XQG XQH XQJ XQK XQL XQM XQN XQP XQQ XQR XQS XRD XRG XRJ XRK XRL XRO XRT XRZ XSA XSB XSC XSD XSE XSH XSI XSK XSL XSM XSO XSP XSS XST XSU XSV XSW XSY XSZ XT1 XTB XTC XTD XTE XTG XTI XTK XTL XTN XTO XTR XTS XTT XTU XTV XTW XTY XTZ XUC XUN XVA XVG XVI XVK XVL XVN XVO XVP XVQ XVR XVS XVY XWA XWB XWC XWD XWF XWG XWH XWJ XWK XWL XWM XWN XWP XWQ XWR XWS XWT XWU XWV XWW XWX XWY XWZ XXA XXB XXC XXD XXF XXG XXH XXJ XXK XYA XYB XYC XYD XYF XYG XYH XYJ XYK XYL XYM XYN XYP XYQ XYR XYS XYT XYV XYW XYX XYY XYZ XZA XZB XZC XZD XZF XZG XZH XZJ XZK XZL XZM XZN XZP XZQ XZR XZS XZT XZU XZV XZW XZX XZY XZZ ', concat(' ', normalize-space(@unitCode), ' ')))))"},
{"id":"DT-CIUS-PT-131","texto":"The BT-151 does not meet the defined format: only admits the following values: AA, S, E, RED, INT, NOR, ISE, OUT, NA, Z, AE, IC, G, O.","categoria":"valores","natureza":"RP","gravidade":"erro","contexto":"//ubl:Invoice/cac:InvoiceLine/cac:Item/cac:ClassifiedTaxCategory/cbc:ID | //cn:CreditNote/cac:CreditNoteLine/cac:Item/cac:ClassifiedTaxCategory/cbc:ID","elementos":["BT-151"],"expressao":"(not(contains(normalize-space(.),' ')) and contains(' AA S E RED INT NOR ISE OUT NA Z AE IC G O ',concat(' ',normalize-space(.),' ')))"},
{"id":"DT-CIUS-PT-132.1","texto":"The BT-152 does not meet the defined format: decimal value with 2 decimal places and 3 unit places.","categoria":"formato","natureza":"RP","gravidade":"erro","contexto":"//ubl:Invoice/cac:InvoiceLine/cac:Item/cac:ClassifiedTaxCategory/cbc:Percent | //cn:CreditNote/cac:CreditNoteLine/cac:Item/cac:ClassifiedTaxCategory/cbc:Percent","elementos":["BT-152"],"expressao":"matches(.,'^(\\d{1,3}\\.\\d{2})$')"},
{"id":"DT-CIUS-PT-132.2","texto":"The BT-152 does not meet the defined format: value between 0.01 and 100.00.","categoria":"formato","natureza":"RP","gravidade":"erro","contexto":"//ubl:Invoice/cac:InvoiceLine/cac:Item/cac:ClassifiedTaxCategory/cbc:Percent | //cn:CreditNote/cac:CreditNoteLine/cac:Item/cac:ClassifiedTaxCategory/cbc:Percent","elementos":["BT-152"],"expressao":"report (dispara quando verdadeiro): matches(.,'^(\\d{1,3}\\.\\d{2})$') and (xs:decimal(.) < 0.00 or xs:decimal(.) > 100.00)"},
{"id":"DT-CIUS-PT-155","texto":"The Invoice line (BG-25) tax scheme should be coded using a restriction of UN/ECE 5153.","categoria":"outra","natureza":"?","gravidade":"erro","contexto":"//ubl:Invoice/cac:InvoiceLine/cac:Item/cac:ClassifiedTaxCategory/cac:TaxScheme/cbc:ID | //cn:CreditNote/cac:CreditNoteLine/cac:Item/cac:ClassifiedTaxCategory/cac:TaxScheme/cbc:ID","elementos":["BG-25"],"expressao":"(not(contains(normalize-space(.),' ')) and contains(' AAA AAB AAC AAD AAE AAF AAG AAH AAI AAJ AAK ADD BOL CAP CAR COC CST CUD CVD ENV EXC EXP FET FRE GCN GST ILL IMP IND LAC LCN LDP LOC LST MCA MCD OTH PDB PDC PRF SCN SSS STT SUP SUR SWT TAC TOT TOX TTA VAD VAT ',concat(' ',normalize-space(.),' ')))"},
{"id":"DT-CIUS-PT-133","texto":"The BT-153 does not meet the defined format: alphanumeric with size between 1 and 200.","categoria":"formato","natureza":"RP","gravidade":"erro","contexto":"//ubl:Invoice/cac:InvoiceLine/cac:Item/cbc:Name | //cn:CreditNote/cac:CreditNoteLine/cac:Item/cbc:Name","elementos":["BT-153"],"expressao":"matches(.,'^(.{1,200})$')"},
{"id":"DT-CIUS-PT-134","texto":"The BT-154 does not meet the defined format: alphanumeric with size between 1 and 200.","categoria":"formato","natureza":"RP","gravidade":"erro","contexto":"//ubl:Invoice/cac:InvoiceLine/cac:Item/cbc:Description | //cn:CreditNote/cac:CreditNoteLine/cac:Item/cbc:Description","elementos":["BT-154"],"expressao":"matches(.,'^(.{1,200})$')"},
{"id":"DT-CIUS-PT-135","texto":"The BT-155 does not meet the defined format: alphanumeric with size between 1 and 50.","categoria":"formato","natureza":"RP","gravidade":"erro","contexto":"//ubl:Invoice/cac:InvoiceLine/cac:Item/cac:SellersItemIdentification/cbc:ID | //cn:CreditNote/cac:CreditNoteLine/cac:Item/cac:SellersItemIdentification/cbc:ID","elementos":["BT-155"],"expressao":"matches(.,'^(.{1,50})$')"},
{"id":"DT-CIUS-PT-136","texto":"The BT-156 does not meet the defined format: alphanumeric with size between 1 and 50.","categoria":"formato","natureza":"RP","gravidade":"erro","contexto":"//ubl:Invoice/cac:InvoiceLine/cac:Item/cac:BuyersItemIdentification/cbc:ID | //cn:CreditNote/cac:CreditNoteLine/cac:Item/cac:BuyersItemIdentification/cbc:ID","elementos":["BT-156"],"expressao":"matches(.,'^(.{1,50})$')"},
{"id":"DT-CIUS-PT-137.1","texto":"The BT-157 does not meet the defined format: alphanumeric with size between 1 and 50.","categoria":"formato","natureza":"RP","gravidade":"erro","contexto":"//ubl:Invoice/cac:InvoiceLine/cac:Item/cac:StandardItemIdentification/cbc:ID | //cn:CreditNote/cac:CreditNoteLine/cac:Item/cac:StandardItemIdentification/cbc:ID","elementos":["BT-157"],"expressao":"matches(.,'^(.{1,50})$')"},
{"id":"DT-CIUS-PT-137.2","texto":"The BT-157 identifier scheme identifier MUST belong to the ISO 6523 ICD code list.","categoria":"valores","natureza":"RP","gravidade":"erro","contexto":"//ubl:Invoice/cac:InvoiceLine/cac:Item/cac:StandardItemIdentification/cbc:ID | //cn:CreditNote/cac:CreditNoteLine/cac:Item/cac:StandardItemIdentification/cbc:ID","elementos":["BT-157"],"expressao":"((not(contains(normalize-space(@schemeID), ' ')) and contains(' 0001 0002 0003 0004 0005 0006 0007 0008 0009 0010 0011 0012 0013 0014 0015 0016 0017 0018 0019 0020 0021 0022 0023 0024 0025 0026 0027 0028 0029 0030 0031 0032 0033 0034 0035 0036 0037 0038 0039 0040 0041 0042 0043 0044 0045 0046 0047 0048 0049 0050 0051 0052 0053 0054 0055 0056 0057 0058 0059 0060 0061 0062 0063 0064 0065 0066 0067 0068 0069 0070 0071 0072 0073 0074 0075 0076 0077 0078 0079 0080 0081 0082 0083 0084 0085 0086 0087 0088 0089 0090 0091 0092 0093 0094 0095 0096 0097 0098 0099 0100 0101 0102 0103 0104 0105 0106 0107 0108 0109 0110 0111 0112 0113 0114 0115 0116 0117 0118 0119 0120 0121 0122 0123 0124 0125 0126 0127 0128 0129 0130 0131 0132 0133 0134 0135 0136 0137 0138 0139 0140 0141 0142 0143 0144 0145 0146 0147 0148 0149 0150 0151 0152 0153 0154 0155 0156 0157 0158 0159 0160 0161 0162 0163 0164 0165 0166 0167 0168 0169 0170 0171 0172 0173 0174 0175 0176 0177 0178 0179 0180 0183 0184 0191 0192 ', concat(' ', normalize-space(@schemeID), ' '))))"},
{"id":"DT-CIUS-PT-138.1","texto":"The BT-158 does not meet the defined format: alphanumeric with size between 1 and 50.","categoria":"formato","natureza":"RP","gravidade":"erro","contexto":"//ubl:Invoice/cac:InvoiceLine/cac:Item/cac:CommodityClassification/cbc:ItemClassificationCode | //cn:CreditNote/cac:CreditNoteLine/cac:Item/cac:CommodityClassification/cbc:ItemClassificationCode","elementos":["BT-158"],"expressao":"matches(.,'^(.{1,50})$')"},
{"id":"DT-CIUS-PT-138.2","texto":"The BT-158 identification list must be coded using one of the UNTDID 7143 list.","categoria":"outra","natureza":"?","gravidade":"erro","contexto":"//ubl:Invoice/cac:InvoiceLine/cac:Item/cac:CommodityClassification/cbc:ItemClassificationCode | //cn:CreditNote/cac:CreditNoteLine/cac:Item/cac:CommodityClassification/cbc:ItemClassificationCode","elementos":["BT-158"],"expressao":"((not(contains(normalize-space(@listID), ' ')) and contains(' AA AB AC AD AE AF AG AH AI AJ AK AL AM AN AO AP AQ AR AS AT AU AV AW AX AY AZ BA BB BC BD BE BF BG BH BI BJ BK BL BM BN BO BP BQ BR BS BT BU BV BW BX BY BZ CC CG CL CR CV DR DW EC EF EN FS GB GN GS HS IB IN IS IT IZ MA MF MN MP NB ON PD PL PO PV QS RC RN RU RY SA SG SK SN SRS SRT SRU SRV SRW SRX SRY SRZ SS SSA SSB SSC SSD SSE SSF SSG SSH SSI SSJ SSK SSL SSM SSN SSO SSP SSQ SSR SSS SST SSU SSV SSW SSX SSY SSZ ST STA STB STC STD STE STF STG STH STI STJ STK STL STM STN STO STP STQ STR STS STT STU STV STW STX STY STZ SUA SUB SUC SUD SUE SUF SUG SUH SUI SUJ SUK SUL SUM TG TSN TSO TSP UA UP VN VP VS VX ZZZ ', concat(' ', normalize-space(@listID), ' '))))"},
{"id":"DT-CIUS-PT-138.3","texto":"The BT-158 identification list version identifier does not meet the defined format: alphanumeric with size between 1 and 20.","categoria":"formato","natureza":"RP","gravidade":"erro","contexto":"//ubl:Invoice/cac:InvoiceLine/cac:Item/cac:CommodityClassification/cbc:ItemClassificationCode | //cn:CreditNote/cac:CreditNoteLine/cac:Item/cac:CommodityClassification/cbc:ItemClassificationCode","elementos":["BT-158"],"expressao":"report (dispara quando verdadeiro): (exists(@listVersionID) and not(matches(@listVersionID,'^(.{1,20})$')))"},
{"id":"DT-CIUS-PT-146","texto":"The BT-159 must be coded using ISO code list 3166-1.","categoria":"valores","natureza":"RP","gravidade":"erro","contexto":"//ubl:Invoice/cac:InvoiceLine/cac:Item/cac:OriginCountry/cbc:IdentificationCode | //cn:CreditNote/cac:CreditNoteLine/cac:Item/cac:OriginCountry/cbc:IdentificationCode","elementos":["BT-159"],"expressao":"((not(contains(normalize-space(.), ' ')) and contains(' AD AE AF AG AI AL AM AN AO AQ AR AS AT AU AW AX AZ BA BB BD BE BF BG BH BI BL BJ BM BN BO BR BS BT BV BW BY BZ CA CC CD CF CG CH CI CK CL CM CN CO CR CU CV CX CY CZ DE DJ DK DM DO DZ EC EE EG EH ER ES ET FI FJ FK FM FO FR GA GB GD GE GF GG GH GI GL GM GN GP GQ GR GS GT GU GW GY HK HM HN HR HT HU ID IE IL IM IN IO IQ IR IS IT JE JM JO JP KE KG KH KI KM KN KP KR KW KY KZ LA LB LC LI LK LR LS LT LU LV LY MA MC MD ME MF MG MH MK ML MM MN MO MP MQ MR MS MT MU MV MW MX MY MZ NA NC NE NF NG NI NL NO NP NR NU NZ OM PA PE PF PG PH PK PL PM PN PR PS PT PW PY QA RO RS RU RW SA SB SC SD SE SG SH SI SJ SK SL SM SN SO SR ST SV SY SZ TC TD TF TG TH TJ TK TL TM TN TO TR TT TV TW TZ UA UG UM US UY UZ VA VC VE VG VI VN VU WF WS YE YT ZA ZM ZW ', concat(' ', normalize-space(.), ' '))))"},
{"id":"DT-CIUS-PT-139","texto":"The BT-160 does not meet the defined format: alphanumeric with size between 1 and 200.","categoria":"formato","natureza":"RP","gravidade":"erro","contexto":"//ubl:Invoice/cac:InvoiceLine/cac:Item/cac:AdditionalItemProperty/cbc:Name | //cn:CreditNote/cac:CreditNoteLine/cac:Item/cac:AdditionalItemProperty/cbc:Name","elementos":["BT-160"],"expressao":"matches(.,'^(.{1,200})$')"},
{"id":"DT-CIUS-PT-139_1","texto":"The BT-160 does not meet the defined format: it is mandatory to fill out with '#ID@INVOICEDOCUMENTREFERENCE@BILLINGREFERENCE-000#'. The sub-suffix \"-000\" must be used as a group of elements.","categoria":"formato","natureza":"RP","gravidade":"erro","contexto":"//ubl:Invoice/cac:InvoiceLine/cac:Item/cac:AdditionalItemProperty/cbc:Name | //cn:CreditNote/cac:CreditNoteLine/cac:Item/cac:AdditionalItemProperty/cbc:Name","elementos":["BT-160"],"expressao":"report (dispara quando verdadeiro): starts-with(normalize-space(.),'#ID@INVOICEDOCUMENTREFERENCE@BILLINGREFERENCE-') and not(matches(.,'^(#(ID@INVOICEDOCUMENTREFERENCE@BILLINGREFERENCE)-([0-9]{3})#)$'))"},
{"id":"DT-CIUS-PT-139_2","texto":"The BT-160 when fill out with '#TAXEXEMPTIONREASONCODE@CLASSIFIEDTAXCATEGORY#', can only exist once.","categoria":"condicional","natureza":"RIR","gravidade":"erro","contexto":"//ubl:Invoice/cac:InvoiceLine/cac:Item/cac:AdditionalItemProperty/cbc:Name | //cn:CreditNote/cac:CreditNoteLine/cac:Item/cac:AdditionalItemProperty/cbc:Name","elementos":["BT-160"],"expressao":"report (dispara quando verdadeiro): starts-with(normalize-space(.),'#TAXEXEMPTIONREASONCODE@CLASSIFIEDTAXCATEGORY#') and $cnt139_2 > $cntLine"},
{"id":"DT-CIUS-PT-139_3","texto":"The BT-160 when fill out with '#TAXEXEMPTIONREASON@CLASSIFIEDTAXCATEGORY#', can only exist once.","categoria":"condicional","natureza":"RIR","gravidade":"erro","contexto":"//ubl:Invoice/cac:InvoiceLine/cac:Item/cac:AdditionalItemProperty/cbc:Name | //cn:CreditNote/cac:CreditNoteLine/cac:Item/cac:AdditionalItemProperty/cbc:Name","elementos":["BT-160"],"expressao":"report (dispara quando verdadeiro): starts-with(normalize-space(.),'#TAXEXEMPTIONREASON@CLASSIFIEDTAXCATEGORY#') and $cnt139_3 > $cntLine"},
{"id":"DT-CIUS-PT-139_5","texto":"The BT-160 when fill out with '#LINEID@COMMITMENTLINEREFERENCE#', can only exist once.","categoria":"condicional","natureza":"RIR","gravidade":"erro","contexto":"//ubl:Invoice/cac:InvoiceLine/cac:Item/cac:AdditionalItemProperty/cbc:Name | //cn:CreditNote/cac:CreditNoteLine/cac:Item/cac:AdditionalItemProperty/cbc:Name","elementos":["BT-160"],"expressao":"report (dispara quando verdadeiro): starts-with(normalize-space(.),'#LINEID@COMMITMENTLINEREFERENCE#') and $cnt139_5 > $cntLine"},
{"id":"DT-CIUS-PT-140","texto":"The BT-161 does not meet the defined format: alphanumeric with size between 1 and 200.","categoria":"formato","natureza":"RP","gravidade":"erro","contexto":"//ubl:Invoice/cac:InvoiceLine/cac:Item/cac:AdditionalItemProperty/cbc:Value | //cn:CreditNote/cac:CreditNoteLine/cac:Item/cac:AdditionalItemProperty/cbc:Value","elementos":["BT-161"],"expressao":"matches(.,'^(.{1,200})$')"}
]
```

### Fonte cius-pt-ubl-fatura: Modelo UBL 2.1 CIUS-PT anotado: Fatura (modelo sintático (XML anotado)) — complementar: só para confirmar cardinalidades e descrições

Papel: sintaxe UBL da fatura: cardinalidades e descrições em português de cada elemento

Grupos (85):
```json
[
{"id":"/Invoice","nome":"Invoice","cardinalidade":"1..1"},
{"id":"/Invoice/InvoicePeriod","nome":"InvoicePeriod","cardinalidade":"0..1","pai":"/Invoice"},
{"id":"/Invoice/OrderReference","nome":"OrderReference","cardinalidade":"0..1","pai":"/Invoice"},
{"id":"/Invoice/BillingReference","nome":"BillingReference","cardinalidade":"0..*","pai":"/Invoice"},
{"id":"/Invoice/BillingReference/InvoiceDocumentReference","nome":"InvoiceDocumentReference","cardinalidade":"1..1","pai":"/Invoice/BillingReference"},
{"id":"/Invoice/DespatchDocumentReference","nome":"DespatchDocumentReference","cardinalidade":"0..*","pai":"/Invoice"},
{"id":"/Invoice/ReceiptDocumentReference","nome":"ReceiptDocumentReference","cardinalidade":"0..1","pai":"/Invoice"},
{"id":"/Invoice/OriginatorDocumentReference","nome":"OriginatorDocumentReference","cardinalidade":"0..1","pai":"/Invoice"},
{"id":"/Invoice/ContractDocumentReference","nome":"ContractDocumentReference","cardinalidade":"0..1","pai":"/Invoice"},
{"id":"/Invoice/AdditionalDocumentReference","nome":"AdditionalDocumentReference","cardinalidade":"0..*","pai":"/Invoice"},
{"id":"/Invoice/AdditionalDocumentReference","nome":"AdditionalDocumentReference","cardinalidade":"0..*","pai":"/Invoice"},
{"id":"/Invoice/AdditionalDocumentReference/Attachment","nome":"Attachment","cardinalidade":"0..1","pai":"/Invoice/AdditionalDocumentReference"},
{"id":"/Invoice/AdditionalDocumentReference/Attachment/ExternalReference","nome":"ExternalReference","cardinalidade":"0..1","pai":"/Invoice/AdditionalDocumentReference/Attachment"},
{"id":"/Invoice/ProjectReference","nome":"ProjectReference","cardinalidade":"0..1","pai":"/Invoice"},
{"id":"/Invoice/AccountingSupplierParty","nome":"AccountingSupplierParty","cardinalidade":"1..1","pai":"/Invoice"},
{"id":"/Invoice/AccountingSupplierParty/Party","nome":"Party","cardinalidade":"1..1","pai":"/Invoice/AccountingSupplierParty"},
{"id":"/Invoice/AccountingSupplierParty/Party/PartyIdentification","nome":"PartyIdentification","cardinalidade":"0..*","pai":"/Invoice/AccountingSupplierParty/Party"},
{"id":"/Invoice/AccountingSupplierParty/Party/PartyName","nome":"PartyName","cardinalidade":"0..1","pai":"/Invoice/AccountingSupplierParty/Party"},
{"id":"/Invoice/AccountingSupplierParty/Party/PostalAddress","nome":"PostalAddress","cardinalidade":"1..1","pai":"/Invoice/AccountingSupplierParty/Party"},
{"id":"/Invoice/AccountingSupplierParty/Party/PostalAddress/AddressLine","nome":"AddressLine","cardinalidade":"0..1","pai":"/Invoice/AccountingSupplierParty/Party/PostalAddress"},
{"id":"/Invoice/AccountingSupplierParty/Party/PostalAddress/Country","nome":"Country","cardinalidade":"1..1","pai":"/Invoice/AccountingSupplierParty/Party/PostalAddress"},
{"id":"/Invoice/AccountingSupplierParty/Party/PartyTaxScheme","nome":"PartyTaxScheme","cardinalidade":"0..1","pai":"/Invoice/AccountingSupplierParty/Party"},
{"id":"/Invoice/AccountingSupplierParty/Party/PartyTaxScheme/TaxScheme","nome":"TaxScheme","cardinalidade":"1..1","pai":"/Invoice/AccountingSupplierParty/Party/PartyTaxScheme"},
{"id":"/Invoice/AccountingSupplierParty/Party/PartyLegalEntity","nome":"PartyLegalEntity","cardinalidade":"1..1","pai":"/Invoice/AccountingSupplierParty/Party"},
{"id":"/Invoice/AccountingSupplierParty/Party/Contact","nome":"Contact","cardinalidade":"0..1","pai":"/Invoice/AccountingSupplierParty/Party"},
{"id":"/Invoice/AccountingCustomerParty","nome":"AccountingCustomerParty","cardinalidade":"1..1","pai":"/Invoice"},
{"id":"/Invoice/AccountingCustomerParty/Party","nome":"Party","cardinalidade":"1..1","pai":"/Invoice/AccountingCustomerParty"},
{"id":"/Invoice/AccountingCustomerParty/Party/PartyIdentification","nome":"PartyIdentification","cardinalidade":"0..*","pai":"/Invoice/AccountingCustomerParty/Party"},
{"id":"/Invoice/AccountingCustomerParty/Party/PartyName","nome":"PartyName","cardinalidade":"0..1","pai":"/Invoice/AccountingCustomerParty/Party"},
{"id":"/Invoice/AccountingCustomerParty/Party/PostalAddress","nome":"PostalAddress","cardinalidade":"1..1","pai":"/Invoice/AccountingCustomerParty/Party"},
{"id":"/Invoice/AccountingCustomerParty/Party/PostalAddress/AddressLine","nome":"AddressLine","cardinalidade":"0..1","pai":"/Invoice/AccountingCustomerParty/Party/PostalAddress"},
{"id":"/Invoice/AccountingCustomerParty/Party/PostalAddress/Country","nome":"Country","cardinalidade":"1..1","pai":"/Invoice/AccountingCustomerParty/Party/PostalAddress"},
{"id":"/Invoice/AccountingCustomerParty/Party/PartyTaxScheme","nome":"PartyTaxScheme","cardinalidade":"0..1","pai":"/Invoice/AccountingCustomerParty/Party"},
{"id":"/Invoice/AccountingCustomerParty/Party/PartyTaxScheme/TaxScheme","nome":"TaxScheme","cardinalidade":"1..1","pai":"/Invoice/AccountingCustomerParty/Party/PartyTaxScheme"},
{"id":"/Invoice/AccountingCustomerParty/Party/PartyLegalEntity","nome":"PartyLegalEntity","cardinalidade":"1..1","pai":"/Invoice/AccountingCustomerParty/Party"},
{"id":"/Invoice/AccountingCustomerParty/Party/Contact","nome":"Contact","cardinalidade":"0..1","pai":"/Invoice/AccountingCustomerParty/Party"},
{"id":"/Invoice/PayeeParty","nome":"PayeeParty","cardinalidade":"0..1","pai":"/Invoice"},
{"id":"/Invoice/PayeeParty/PartyIdentification","nome":"PartyIdentification","cardinalidade":"0..1","pai":"/Invoice/PayeeParty"},
{"id":"/Invoice/PayeeParty/PartyName","nome":"PartyName","cardinalidade":"1..1","pai":"/Invoice/PayeeParty"},
{"id":"/Invoice/PayeeParty/PartyLegalEntity","nome":"PartyLegalEntity","cardinalidade":"1..1","pai":"/Invoice/PayeeParty"},
{"id":"/Invoice/TaxRepresentativeParty","nome":"TaxRepresentativeParty","cardinalidade":"0..1","pai":"/Invoice"},
{"id":"/Invoice/TaxRepresentativeParty/PartyName","nome":"PartyName","cardinalidade":"1..1","pai":"/Invoice/TaxRepresentativeParty"},
{"id":"/Invoice/TaxRepresentativeParty/PostalAddress","nome":"PostalAddress","cardinalidade":"1..1","pai":"/Invoice/TaxRepresentativeParty"},
{"id":"/Invoice/TaxRepresentativeParty/PostalAddress/AddressLine","nome":"AddressLine","cardinalidade":"0..1","pai":"/Invoice/TaxRepresentativeParty/PostalAddress"},
{"id":"/Invoice/TaxRepresentativeParty/PostalAddress/Country","nome":"Country","cardinalidade":"1..1","pai":"/Invoice/TaxRepresentativeParty/PostalAddress"},
{"id":"/Invoice/TaxRepresentativeParty/PartyTaxScheme","nome":"PartyTaxScheme","cardinalidade":"1..1","pai":"/Invoice/TaxRepresentativeParty"},
{"id":"/Invoice/TaxRepresentativeParty/PartyTaxScheme/TaxScheme","nome":"TaxScheme","cardinalidade":"1..1","pai":"/Invoice/TaxRepresentativeParty/PartyTaxScheme"},
{"id":"/Invoice/Delivery","nome":"Delivery","cardinalidade":"1..*","pai":"/Invoice"},
{"id":"/Invoice/Delivery/DeliveryLocation","nome":"DeliveryLocation","cardinalidade":"0..1","pai":"/Invoice/Delivery"},
{"id":"/Invoice/Delivery/DeliveryLocation/Address","nome":"Address","cardinalidade":"0..1","pai":"/Invoice/Delivery/DeliveryLocation"},
{"id":"/Invoice/Delivery/DeliveryLocation/Address/AddressLine","nome":"AddressLine","cardinalidade":"0..1","pai":"/Invoice/Delivery/DeliveryLocation/Address"},
{"id":"/Invoice/Delivery/DeliveryLocation/Address/Country","nome":"Country","cardinalidade":"1..1","pai":"/Invoice/Delivery/DeliveryLocation/Address"},
{"id":"/Invoice/Delivery/DeliveryParty","nome":"DeliveryParty","cardinalidade":"0..1","pai":"/Invoice/Delivery"},
{"id":"/Invoice/Delivery/DeliveryParty/PartyName","nome":"PartyName","cardinalidade":"0..*","pai":"/Invoice/Delivery/DeliveryParty"},
{"id":"/Invoice/PaymentMeans","nome":"PaymentMeans","cardinalidade":"0..1","pai":"/Invoice"},
{"id":"/Invoice/PaymentMeans/CardAccount","nome":"CardAccount","cardinalidade":"0..1","pai":"/Invoice/PaymentMeans"},
{"id":"/Invoice/PaymentMeans/PayeeFinancialAccount","nome":"PayeeFinancialAccount","cardinalidade":"0..*","pai":"/Invoice/PaymentMeans"},
{"id":"/Invoice/PaymentMeans/PayeeFinancialAccount/FinancialInstitutionBranch","nome":"FinancialInstitutionBranch","cardinalidade":"0..1","pai":"/Invoice/PaymentMeans/PayeeFinancialAccount"},
{"id":"/Invoice/PaymentMeans/PaymentMandate","nome":"PaymentMandate","cardinalidade":"0..1","pai":"/Invoice/PaymentMeans"},
{"id":"/Invoice/PaymentMeans/PaymentMandate/PayerFinancialAccount","nome":"PayerFinancialAccount","cardinalidade":"0..1","pai":"/Invoice/PaymentMeans/PaymentMandate"},
{"id":"/Invoice/PaymentTerms","nome":"PaymentTerms","cardinalidade":"0..1","pai":"/Invoice"},
{"id":"/Invoice/AllowanceCharge","nome":"AllowanceCharge","cardinalidade":"0..*","pai":"/Invoice"},
{"id":"/Invoice/AllowanceCharge/TaxCategory","nome":"TaxCategory","cardinalidade":"0..1","pai":"/Invoice/AllowanceCharge"},
{"id":"/Invoice/AllowanceCharge/TaxCategory/TaxScheme","nome":"TaxScheme","cardinalidade":"1..1","pai":"/Invoice/AllowanceCharge/TaxCategory"},
{"id":"/Invoice/TaxTotal","nome":"TaxTotal","cardinalidade":"0..1","pai":"/Invoice"},
{"id":"/Invoice/TaxTotal/TaxSubtotal","nome":"TaxSubtotal","cardinalidade":"1..*","pai":"/Invoice/TaxTotal"},
{"id":"/Invoice/TaxTotal/TaxSubtotal/TaxCategory","nome":"TaxCategory","cardinalidade":"1..1","pai":"/Invoice/TaxTotal/TaxSubtotal"},
{"id":"/Invoice/TaxTotal/TaxSubtotal/TaxCategory/TaxScheme","nome":"TaxScheme","cardinalidade":"1..1","pai":"/Invoice/TaxTotal/TaxSubtotal/TaxCategory"},
{"id":"/Invoice/LegalMonetaryTotal","nome":"LegalMonetaryTotal","cardinalidade":"1..1","pai":"/Invoice"},
{"id":"/Invoice/InvoiceLine","nome":"InvoiceLine","cardinalidade":"1..*","pai":"/Invoice"},
{"id":"/Invoice/InvoiceLine/InvoicePeriod","nome":"InvoicePeriod","cardinalidade":"0..1","pai":"/Invoice/InvoiceLine"},
{"id":"/Invoice/InvoiceLine/OrderLineReference","nome":"OrderLineReference","cardinalidade":"0..1","pai":"/Invoice/InvoiceLine"},
{"id":"/Invoice/InvoiceLine/DocumentReference","nome":"DocumentReference","cardinalidade":"0..1","pai":"/Invoice/InvoiceLine"},
{"id":"/Invoice/InvoiceLine/AllowanceCharge","nome":"AllowanceCharge","cardinalidade":"0..*","pai":"/Invoice/InvoiceLine"},
{"id":"/Invoice/InvoiceLine/Item","nome":"Item","cardinalidade":"1..1","pai":"/Invoice/InvoiceLine"},
{"id":"/Invoice/InvoiceLine/Item/BuyersItemIdentification","nome":"BuyersItemIdentification","cardinalidade":"0..1","pai":"/Invoice/InvoiceLine/Item"},
{"id":"/Invoice/InvoiceLine/Item/SellersItemIdentification","nome":"SellersItemIdentification","cardinalidade":"0..1","pai":"/Invoice/InvoiceLine/Item"},
{"id":"/Invoice/InvoiceLine/Item/StandardItemIdentification","nome":"StandardItemIdentification","cardinalidade":"0..1","pai":"/Invoice/InvoiceLine/Item"},
{"id":"/Invoice/InvoiceLine/Item/OriginCountry","nome":"OriginCountry","cardinalidade":"0..1","pai":"/Invoice/InvoiceLine/Item"},
{"id":"/Invoice/InvoiceLine/Item/CommodityClassification","nome":"CommodityClassification","cardinalidade":"0..*","pai":"/Invoice/InvoiceLine/Item"},
{"id":"/Invoice/InvoiceLine/Item/ClassifiedTaxCategory","nome":"ClassifiedTaxCategory","cardinalidade":"1..1","pai":"/Invoice/InvoiceLine/Item"},
{"id":"/Invoice/InvoiceLine/Item/ClassifiedTaxCategory/TaxScheme","nome":"TaxScheme","cardinalidade":"1..1","pai":"/Invoice/InvoiceLine/Item/ClassifiedTaxCategory"},
{"id":"/Invoice/InvoiceLine/Item/AdditionalItemProperty","nome":"AdditionalItemProperty","cardinalidade":"0..*","pai":"/Invoice/InvoiceLine/Item"},
{"id":"/Invoice/InvoiceLine/Price","nome":"Price","cardinalidade":"1..1","pai":"/Invoice/InvoiceLine"},
{"id":"/Invoice/InvoiceLine/Price/AllowanceCharge","nome":"AllowanceCharge","cardinalidade":"0..1","pai":"/Invoice/InvoiceLine/Price"}
]
```

Elementos (156):
```json
[
{"id":"/Invoice/CustomizationID","descricao":"ID Customização [Predefinição: urn:www:espap:pt:profiles:profile1:seguido do identificador da versão]","cardinalidade":"1..1"},
{"id":"/Invoice/ProfileID","descricao":"Perfil onde se enquadra a customização associada ao Template UBL 2.1","cardinalidade":"0..1"},
{"id":"/Invoice/ID","descricao":"Número do documento","cardinalidade":"1..1"},
{"id":"/Invoice/IssueDate","descricao":"Data de emissão do documento [AAAA-MM-DD]","cardinalidade":"1..1"},
{"id":"/Invoice/DueDate","descricao":"Data de vencimento do documento [AAAA-MM-DD]","cardinalidade":"0..1"},
{"id":"/Invoice/InvoiceTypeCode","descricao":"Código que identifica o tipo funcional da fatura eletrónica, segundo a lista de códigos UNCL1001 (http://www.unece.org/trade/untdid/d98a/uncl/uncl1001.htm) [FE: 380 / ND: 383]","cardinalidade":"1..1"},
{"id":"/Invoice/Note","descricao":"Notas textuais que permitem ao fornecedor enviar informação não estruturada relativa ao documento.","cardinalidade":"0..*"},
{"id":"/Invoice/TaxPointDate","descricao":"A data em que o IVA se torna aplicável para o Vendedor e para o Comprador na medida em que essa data pode ser determinada e difere da data de emissão da fatura, de acordo com a diretiva do IVA [AAAA-MM-DD]","cardinalidade":"0..1"},
{"id":"/Invoice/DocumentCurrencyCode","descricao":"Moeda, segundo a lista de códigos ISO4217 (https://www.iso.org/iso-4217-currency-codes.html) [Predefinição: EUR]","cardinalidade":"1..1"},
{"id":"/Invoice/TaxCurrencyCode","descricao":"A moeda usada para fins de contabilidade e relatórios de IVA, conforme aceite ou exigida no país do vendedor.","cardinalidade":"0..1"},
{"id":"/Invoice/AccountingCost","descricao":"Número do compromisso.","cardinalidade":"0..1"},
{"id":"/Invoice/BuyerReference","descricao":"Referência do Cliente","cardinalidade":"0..1"},
{"id":"/Invoice/InvoicePeriod/StartDate","descricao":"A data em que o período de faturação começa.[AAAA-MM-DD]","cardinalidade":"0..1"},
{"id":"/Invoice/InvoicePeriod/EndDate","descricao":"A data em que o período de faturação acaba.[AAAA-MM-DD]","cardinalidade":"0..1"},
{"id":"/Invoice/InvoicePeriod/DescriptionCode","descricao":"O código da data em que o IVA se torna aplicável pelo vendedor e pelo comprador.","cardinalidade":"0..1"},
{"id":"/Invoice/OrderReference/ID","descricao":"Número da nota de encomenda.","cardinalidade":"0..1"},
{"id":"/Invoice/OrderReference/SalesOrderID","descricao":"Número da ordem de venda, emitida pelo fornecedor.","cardinalidade":"0..1"},
{"id":"/Invoice/BillingReference/InvoiceDocumentReference/ID","descricao":"Número de referência do documento, emitido pelo fornecedor, anteriormente enviado.","cardinalidade":"1..1"},
{"id":"/Invoice/BillingReference/InvoiceDocumentReference/IssueDate","descricao":"Data de emissão do documento, anteriormente enviado.[AAAA-MM-DD]","cardinalidade":"0..1"},
{"id":"/Invoice/DespatchDocumentReference/ID","descricao":"Referência do aviso de envio.","cardinalidade":"1..1"},
{"id":"/Invoice/ReceiptDocumentReference/ID","descricao":"Número do aviso de recebimento referenciado.","cardinalidade":"1..1"},
{"id":"/Invoice/OriginatorDocumentReference/ID","descricao":"Número do acordo quadro.","cardinalidade":"1..1"},
{"id":"/Invoice/ContractDocumentReference/ID","descricao":"Número do contrato.","cardinalidade":"1..1"},
{"id":"/Invoice/AdditionalDocumentReference/ID","descricao":"Identificador do processo de registo de entrada do documento.Identificador do anexo referenciado de acordo com a norma UNCL1153 (https://docs.peppol.eu/poacc/billing/3.0/codelist/UNCL1153/) Scheme ID = AIM para colocar UUID","cardinalidade":"0..1"},
{"id":"/Invoice/AdditionalDocumentReference/ID","descricao":"Identificador do processo de registo de entrada do documento.Identificador do anexo referenciado de acordo com a norma UNCL1153 (https://docs.peppol.eu/poacc/billing/3.0/codelist/UNCL1153/)","cardinalidade":"0..1"},
{"id":"/Invoice/AdditionalDocumentReference/DocumentTypeCode","descricao":"Código que identifica o tipo funcional da fatura eletrónica, segundo a lista de códigos UNCL1001 (http://www.unece.org/trade/untdid/d98a/uncl/uncl1001.htm) [FE: 380]","cardinalidade":"0..1"},
{"id":"/Invoice/AdditionalDocumentReference/DocumentDescription","descricao":"Descrição do documento anexado [Predefinição: Facturas: INVOICE_REPRESENTATION | Anexos: ATTACHMENT]","cardinalidade":"0..1"},
{"id":"/Invoice/AdditionalDocumentReference/Attachment/EmbeddedDocumentBinaryObject","descricao":"Documento codificado em base 64","cardinalidade":"0..1"},
{"id":"/Invoice/AdditionalDocumentReference/Attachment/ExternalReference/URI","descricao":"Endereço para um documento, localizado externamente.","cardinalidade":"1..1"},
{"id":"/Invoice/ProjectReference/ID","descricao":"Número do Projeto","cardinalidade":"1..1"},
{"id":"/Invoice/AccountingSupplierParty/Party/EndpointID","descricao":"Código de identificação do Fornecedor, por exemplo GLN, URN etc","cardinalidade":"0..1"},
{"id":"/Invoice/AccountingSupplierParty/Party/PartyIdentification/ID","descricao":"Identificação do vendedor (ID Bancário)","cardinalidade":"1..1"},
{"id":"/Invoice/AccountingSupplierParty/Party/PartyName/Name","descricao":"Nome do fornecedor","cardinalidade":"1..1"},
{"id":"/Invoice/AccountingSupplierParty/Party/PostalAddress/StreetName","descricao":"Morada do fornecedor","cardinalidade":"1..1"},
{"id":"/Invoice/AccountingSupplierParty/Party/PostalAddress/AdditionalStreetName","descricao":"Morada do fornecedor (adicional)","cardinalidade":"0..1"},
{"id":"/Invoice/AccountingSupplierParty/Party/PostalAddress/CityName","descricao":"Cidade do fornecedor","cardinalidade":"1..1"},
{"id":"/Invoice/AccountingSupplierParty/Party/PostalAddress/PostalZone","descricao":"Código Postal do fornecedor","cardinalidade":"1..1"},
{"id":"/Invoice/AccountingSupplierParty/Party/PostalAddress/CountrySubentity","descricao":"Região/Província da morada do fornecedor","cardinalidade":"0..1"},
{"id":"/Invoice/AccountingSupplierParty/Party/PostalAddress/AddressLine/Line","descricao":"Linha de endereço adicional que pode ser usado para fornecer mais detalhes, complementando a linha principal.","cardinalidade":"1..1"},
{"id":"/Invoice/AccountingSupplierParty/Party/PostalAddress/Country/IdentificationCode","descricao":"País do fornecedor, segundo o código ISO 3166-1 alfa-2","cardinalidade":"1..1"},
{"id":"/Invoice/AccountingSupplierParty/Party/PartyTaxScheme/CompanyID","descricao":"Número de identificação fiscal do fornecedor, precedido do código do país, segundo o código ISO 3166-1 alfa-2","cardinalidade":"1..1"},
{"id":"/Invoice/AccountingSupplierParty/Party/PartyTaxScheme/TaxScheme/ID","descricao":"O valor do ID corresponde à lista de códigos UN/ECE 5153, da Comissão Económica das Nações Unidas para a Europa. [Predefinição: VAT]","cardinalidade":"1..1"},
{"id":"/Invoice/AccountingSupplierParty/Party/PartyLegalEntity/RegistrationName","descricao":"Identificação do fornecedor na IRN","cardinalidade":"1..1"},
{"id":"/Invoice/AccountingSupplierParty/Party/PartyLegalEntity/CompanyID","descricao":"Número de Identificação do fornecedor na conservatória","cardinalidade":"0..1"},
{"id":"/Invoice/AccountingSupplierParty/Party/PartyLegalEntity/CompanyLegalForm","descricao":"Capital Social do fornecedor","cardinalidade":"0..1"},
{"id":"/Invoice/AccountingSupplierParty/Party/Contact/Name","descricao":"Ponto de contato do fornecedor.","cardinalidade":"0..1"},
{"id":"/Invoice/AccountingSupplierParty/Party/Contact/Telephone","descricao":"Contacto telefónico do fornecedor.","cardinalidade":"0..1"},
{"id":"/Invoice/AccountingSupplierParty/Party/Contact/ElectronicMail","descricao":"Endereço de correio eletrónico do fornecedor.","cardinalidade":"0..1"},
{"id":"/Invoice/AccountingCustomerParty/Party/EndpointID","descricao":"Código de identificação do Cliente, por exemplo GLN, URN etc","cardinalidade":"0..1"},
{"id":"/Invoice/AccountingCustomerParty/Party/PartyIdentification/ID","descricao":"Identificação do cliente","cardinalidade":"1..1"},
{"id":"/Invoice/AccountingCustomerParty/Party/PartyName/Name","descricao":"Nome do cliente","cardinalidade":"1..1"},
{"id":"/Invoice/AccountingCustomerParty/Party/PostalAddress/StreetName","descricao":"Linha 1 da morada do cliente.","cardinalidade":"0..1"},
{"id":"/Invoice/AccountingCustomerParty/Party/PostalAddress/AdditionalStreetName","descricao":"Linha 2 da morada do cliente.","cardinalidade":"0..1"},
{"id":"/Invoice/AccountingCustomerParty/Party/PostalAddress/CityName","descricao":"Cidade do cliente","cardinalidade":"0..1"},
{"id":"/Invoice/AccountingCustomerParty/Party/PostalAddress/PostalZone","descricao":"Código Postal do cliente","cardinalidade":"0..1"},
{"id":"/Invoice/AccountingCustomerParty/Party/PostalAddress/CountrySubentity","descricao":"Região/Província da morada do cliente.","cardinalidade":"0..1"},
{"id":"/Invoice/AccountingCustomerParty/Party/PostalAddress/AddressLine/Line","descricao":"Linha de endereço adicional que pode ser usado para fornecer mais detalhes, complementando a linha principal.","cardinalidade":"1..1"},
{"id":"/Invoice/AccountingCustomerParty/Party/PostalAddress/Country/IdentificationCode","descricao":"País do cliente, segundo o código ISO 3166-1 alfa-2","cardinalidade":"1..1"},
{"id":"/Invoice/AccountingCustomerParty/Party/PartyTaxScheme/CompanyID","descricao":"Número de identificação fiscal do cliente, precedido do código do país, segundo o código ISO 3166-1 alfa-2","cardinalidade":"1..1"},
{"id":"/Invoice/AccountingCustomerParty/Party/PartyTaxScheme/TaxScheme/ID","descricao":"O valor do ID corresponde à lista de códigos UN/ECE 5153, da Comissão Económica das Nações Unidas para a Europa. [Predefinição: VAT]","cardinalidade":"1..1"},
{"id":"/Invoice/AccountingCustomerParty/Party/PartyLegalEntity/RegistrationName","descricao":"Nome do cliente.","cardinalidade":"1..1"},
{"id":"/Invoice/AccountingCustomerParty/Party/PartyLegalEntity/CompanyID","descricao":"Informação sobre o registo na conservatória do cliente.","cardinalidade":"0..1"},
{"id":"/Invoice/AccountingCustomerParty/Party/Contact/Name","descricao":"Ponto de contato do cliente.","cardinalidade":"0..1"},
{"id":"/Invoice/AccountingCustomerParty/Party/Contact/Telephone","descricao":"Contacto telefónico do cliente.","cardinalidade":"0..1"},
{"id":"/Invoice/AccountingCustomerParty/Party/Contact/ElectronicMail","descricao":"Email de contacto do cliente","cardinalidade":"0..1"},
{"id":"/Invoice/PayeeParty/PartyIdentification/ID","descricao":"Identificador do recebedor do pagamento.","cardinalidade":"1..1"},
{"id":"/Invoice/PayeeParty/PartyName/Name","descricao":"Nome da entidade que recebe o pagamento.","cardinalidade":"1..1"},
{"id":"/Invoice/PayeeParty/PartyLegalEntity/CompanyID","descricao":"Informação sobre o registo na conservatória do recebedor do pagamento","cardinalidade":"0..1"},
{"id":"/Invoice/TaxRepresentativeParty/PartyName/Name","descricao":"Nome do representante legal para os temas fiscais.","cardinalidade":"1..1"},
{"id":"/Invoice/TaxRepresentativeParty/PostalAddress/StreetName","descricao":"Linha 1 da morada do representante legal para os temas fiscais.","cardinalidade":"0..1"},
{"id":"/Invoice/TaxRepresentativeParty/PostalAddress/AdditionalStreetName","descricao":"Linha 2 da morada do representante legal para os temas fiscais.","cardinalidade":"0..1"},
{"id":"/Invoice/TaxRepresentativeParty/PostalAddress/CityName","descricao":"Cidade da morada do representante legal para os temas fiscais.","cardinalidade":"0..1"},
{"id":"/Invoice/TaxRepresentativeParty/PostalAddress/PostalZone","descricao":"Código postal da morada do representante legal para os temas fiscais.","cardinalidade":"0..1"},
{"id":"/Invoice/TaxRepresentativeParty/PostalAddress/CountrySubentity","descricao":"Região/Província da morada do representante legal para os temas fiscais.","cardinalidade":"0..1"},
{"id":"/Invoice/TaxRepresentativeParty/PostalAddress/AddressLine/Line","descricao":"Linha de endereço adicional que pode ser usado para fornecer mais detalhes, complementando a linha principal.","cardinalidade":"1..1"},
{"id":"/Invoice/TaxRepresentativeParty/PostalAddress/Country/IdentificationCode","descricao":"Código identificador do país da morada do representante legal para os temas fiscais.","cardinalidade":"1..1"},
{"id":"/Invoice/TaxRepresentativeParty/PartyTaxScheme/CompanyID","descricao":"Número de identificação fiscal do representante legal para os temas fiscais.","cardinalidade":"1..1"},
{"id":"/Invoice/TaxRepresentativeParty/PartyTaxScheme/TaxScheme/ID","descricao":"O valor do ID corresponde à lista de códigos UN/ECE 5153, da Comissão Económica das Nações Unidas para a Europa. [Predefinição:VAT]","cardinalidade":"1..1"},
{"id":"/Invoice/Delivery/ActualDeliveryDate","descricao":"Data de entrega","cardinalidade":"0..1"},
{"id":"/Invoice/Delivery/DeliveryLocation/ID","descricao":"Identificador do local em que os bens e serviços são entregues.","cardinalidade":"0..1"},
{"id":"/Invoice/Delivery/DeliveryLocation/Address/StreetName","descricao":"Linha 1 da morada do local de entrega.","cardinalidade":"1..1"},
{"id":"/Invoice/Delivery/DeliveryLocation/Address/AdditionalStreetName","descricao":"Linha 2 da morada do local de entrega.","cardinalidade":"0..1"},
{"id":"/Invoice/Delivery/DeliveryLocation/Address/CityName","descricao":"Cidade do local de entrega","cardinalidade":"1..1"},
{"id":"/Invoice/Delivery/DeliveryLocation/Address/PostalZone","descricao":"Código postal da morada do local de entrega","cardinalidade":"1..1"},
{"id":"/Invoice/Delivery/DeliveryLocation/Address/CountrySubentity","descricao":"Região/Província da morada do local de entrega.","cardinalidade":"0..1"},
{"id":"/Invoice/Delivery/DeliveryLocation/Address/AddressLine/Line","descricao":"Linha de endereço adicional que pode ser usado para fornecer mais detalhes, complementando a linha principal.","cardinalidade":"1..1"},
{"id":"/Invoice/Delivery/DeliveryLocation/Address/Country/IdentificationCode","descricao":"País do local de entrega, segundo o código ISO 3166-1 alfa-2","cardinalidade":"1..1"},
{"id":"/Invoice/Delivery/DeliveryParty/PartyName/Name","descricao":"Nome do local de entrega","cardinalidade":"1..1"},
{"id":"/Invoice/PaymentMeans/PaymentMeansCode","descricao":"Código identificador do método de pagamento,deve mencionar o método de pagamento, segundo o código UNCL4461.","cardinalidade":"1..1"},
{"id":"/Invoice/PaymentMeans/PaymentID","descricao":"Descrição da referência a pagamento do documento por ATM.","cardinalidade":"0..1"},
{"id":"/Invoice/PaymentMeans/CardAccount/PrimaryAccountNumberID","descricao":"Número da conta principal do cartão utilizado no pagamento, PAN.","cardinalidade":"1..1"},
{"id":"/Invoice/PaymentMeans/CardAccount/NetworkID","descricao":"Identificador da rede [ex: VISA, MASTER CARD, American Express...]","cardinalidade":"1..1"},
{"id":"/Invoice/PaymentMeans/CardAccount/HolderName","descricao":"Nome do titular do cartão de pagamento.","cardinalidade":"0..1"},
{"id":"/Invoice/PaymentMeans/PayeeFinancialAccount/ID","descricao":"Identificador do pagamento, código IBAN.","cardinalidade":"0..1"},
{"id":"/Invoice/PaymentMeans/PayeeFinancialAccount/Name","descricao":"Identificação da conta, para a qual o pagamento deve ser efectuado.","cardinalidade":"0..1"},
{"id":"/Invoice/PaymentMeans/PayeeFinancialAccount/FinancialInstitutionBranch/ID","descricao":"Código da instituição bancária. Será considerado o código SWIFT se o atributo schemeID for igual a BIC, segundo a lista de códigos ISO 9362.","cardinalidade":"1..1"},
{"id":"/Invoice/PaymentMeans/PaymentMandate/ID","descricao":"Identificador exclusivo atribuído pelo Beneficiário para referenciar o mandato de débito direto (Nº Mandato).","cardinalidade":"0..1"},
{"id":"/Invoice/PaymentMeans/PaymentMandate/PayerFinancialAccount/ID","descricao":"A conta a ser debitada pelo débito direto.","cardinalidade":"1..1"},
{"id":"/Invoice/PaymentTerms/Note","descricao":"Descritivo das condições de pagamento.","cardinalidade":"0..*"},
{"id":"/Invoice/AllowanceCharge/ChargeIndicator","descricao":"Indica se o valor é um encargo ou um desconto da linha do documento. Indicador de encargo (true). Indicador de desconto (false).","cardinalidade":"1..1"},
{"id":"/Invoice/AllowanceCharge/AllowanceChargeReasonCode","descricao":"Código do motivo, que possa levar a que o montante contemplado no desconto/encargo, esteja isento de imposto.","cardinalidade":"0..1"},
{"id":"/Invoice/AllowanceCharge/AllowanceChargeReason","descricao":"Representação textual do desconto/encargo","cardinalidade":"0..1"},
{"id":"/Invoice/AllowanceCharge/MultiplierFactorNumeric","descricao":"Fator multiplicador sobre o montante base do desconto/encargo","cardinalidade":"0..1"},
{"id":"/Invoice/AllowanceCharge/Amount","descricao":"Montante do desconto/encargo, sem impostos.A Moeda, segundo a lista de códigos ISO4217 (https://www.iso.org/iso-4217-currency-codes.html)","cardinalidade":"1..1"},
{"id":"/Invoice/AllowanceCharge/BaseAmount","descricao":"Montante base do desconto/encargo. A Moeda, segundo a lista de códigos ISO4217 (https://www.iso.org/iso-4217-currency-codes.html)","cardinalidade":"0..1"},
{"id":"/Invoice/AllowanceCharge/TaxCategory/ID","descricao":"Código de imposto aplicado ao desconto/encargo","cardinalidade":"1..1"},
{"id":"/Invoice/AllowanceCharge/TaxCategory/Percent","descricao":"Percentagem de imposto aplicada ao desconto/encargo","cardinalidade":"1..1"},
{"id":"/Invoice/AllowanceCharge/TaxCategory/TaxScheme/ID","descricao":"O valor do ID corresponde à lista de códigos UN/ECE 5153 [Predefinição:VAT]","cardinalidade":"1..1"},
{"id":"/Invoice/TaxTotal/TaxAmount","descricao":"Total de impostos.A Moeda, segundo a lista de códigos ISO4217 (https://www.iso.org/iso-4217-currency-codes.html)","cardinalidade":"1..1"},
{"id":"/Invoice/TaxTotal/TaxSubtotal/TaxableAmount","descricao":"Montante base de incidência para a taxa de imposto aplicada no respetivo subtotal.A Moeda, segundo a lista de códigos ISO4217 (https://www.iso.org/iso-4217-currency-codes.html)","cardinalidade":"1..1"},
{"id":"/Invoice/TaxTotal/TaxSubtotal/TaxAmount","descricao":"Montante calculado do imposto sobre o montante base de incidência respetivo..A Moeda, segundo a lista de códigos ISO4217 (https://www.iso.org/iso-4217-currency-codes.html)","cardinalidade":"1..1"},
{"id":"/Invoice/TaxTotal/TaxSubtotal/TaxCategory/ID","descricao":"Código de imposto respeitante à taxa aplicada no item da linha do documento, segundo a lista de códigos UN/ECE 5305 (http://www.unece.org/trade/untdid/d07a/tred/tred5305.htm) [Predefinição: S]","cardinalidade":"1..1"},
{"id":"/Invoice/TaxTotal/TaxSubtotal/TaxCategory/Percent","descricao":"Percentagem de imposto do subtotal","cardinalidade":"1..1"},
{"id":"/Invoice/TaxTotal/TaxSubtotal/TaxCategory/TaxExemptionReasonCode","descricao":"Código do motivo, que possa levar a que o montante contemplado no subtotal, respetivo, esteja isento de imposto.","cardinalidade":"0..1"},
{"id":"/Invoice/TaxTotal/TaxSubtotal/TaxCategory/TaxExemptionReason","descricao":"Descrição textual do motivo, que possa levar a que o montante contemplado no subtotal, respetivo, esteja isento de imposto.","cardinalidade":"0..1"},
{"id":"/Invoice/TaxTotal/TaxSubtotal/TaxCategory/TaxScheme/ID","descricao":"O valor do ID corresponde à lista de códigos UN/ECE 5153 [Predefinição: VAT]","cardinalidade":"1..1"},
{"id":"/Invoice/LegalMonetaryTotal/LineExtensionAmount","descricao":"Soma dos montantes das linhas do documento (s/imposto). A Moeda, segundo a lista de códigos ISO4217 (https://www.iso.org/iso-4217-currency-codes.html)","cardinalidade":"1..1"},
{"id":"/Invoice/LegalMonetaryTotal/TaxExclusiveAmount","descricao":"Total do documento (s/imposto).A Moeda, segundo a lista de códigos ISO4217 (https://www.iso.org/iso-4217-currency-codes.html)","cardinalidade":"1..1"},
{"id":"/Invoice/LegalMonetaryTotal/TaxInclusiveAmount","descricao":"Total do documento (c/imposto). A Moeda, segundo a lista de códigos ISO4217 (https://www.iso.org/iso-4217-currency-codes.html)","cardinalidade":"1..1"},
{"id":"/Invoice/LegalMonetaryTotal/AllowanceTotalAmount","descricao":"Total de descontos aplicados no documento. A Moeda, segundo a lista de códigos ISO4217 (https://www.iso.org/iso-4217-currency-codes.html)","cardinalidade":"0..1"},
{"id":"/Invoice/LegalMonetaryTotal/ChargeTotalAmount","descricao":"Total de encargos aplicados no documento. A Moeda, segundo a lista de códigos ISO4217 (https://www.iso.org/iso-4217-currency-codes.html)","cardinalidade":"0..1"},
{"id":"/Invoice/LegalMonetaryTotal/PrepaidAmount","descricao":"Valor pago à-priori. O documento pode conter a soma de todos os montantes pré-pagos, que devem ser deduzidos do pagamento. A Moeda, segundo a lista de códigos ISO4217 (https://www.iso.org/iso-4217-currency-codes.html)","cardinalidade":"0..1"},
{"id":"/Invoice/LegalMonetaryTotal/PayableRoundingAmount","descricao":"Montante de arredondamento aplicado ao total do documento c/imposto. A Moeda, segundo a lista de códigos ISO4217 (https://www.iso.org/iso-4217-currency-codes.html)","cardinalidade":"0..1"},
{"id":"/Invoice/LegalMonetaryTotal/PayableAmount","descricao":"Valor a pagar. A Moeda, segundo a lista de códigos ISO4217 (https://www.iso.org/iso-4217-currency-codes.html)","cardinalidade":"1..1"},
{"id":"/Invoice/InvoiceLine/ID","descricao":"Identificador único da linha do documento, atribuído pelo fornecedor","cardinalidade":"1..1"},
{"id":"/Invoice/InvoiceLine/Note","descricao":"Texto livre para descrever alguma observação em relação ao item respetivo à linha do documento.","cardinalidade":"0..1"},
{"id":"/Invoice/InvoiceLine/InvoicedQuantity","descricao":"Quantidade faturada. A propriedade unitCode deverá ser preenchida com o código UNECERec20 de unidade medida. (http://www.unece.org/cefact/recommendations/rec20/Rec20_Rev6e_2009.xls).","cardinalidade":"1..1"},
{"id":"/Invoice/InvoiceLine/LineExtensionAmount","descricao":"Montante da linha (s/imposto). O valor deve incluir os respetivos encargos ou descontos aplicados à linha, desprovidos de imposto e outras taxas (que não sejam de IVA). A Moeda, segundo a lista de códigos ISO4217 (https://www.iso.org/iso-4217-currency-codes.html) [EUR]","cardinalidade":"1..1"},
{"id":"/Invoice/InvoiceLine/AccountingCost","descricao":"Número do compromisso associado à linha do documento.","cardinalidade":"0..1"},
{"id":"/Invoice/InvoiceLine/InvoicePeriod/StartDate","descricao":"A data em que o período começa.[AAAA-MM-DD]","cardinalidade":"0..1"},
{"id":"/Invoice/InvoiceLine/InvoicePeriod/EndDate","descricao":"A data em que o período acaba.[AAAA-MM-DD]","cardinalidade":"0..1"},
{"id":"/Invoice/InvoiceLine/OrderLineReference/LineID","descricao":"Referência para o item da nota de encomenda do cliente.","cardinalidade":"1..1"},
{"id":"/Invoice/InvoiceLine/DocumentReference/ID","descricao":"Identificador para um objeto no qual a linha da fatura é baseada, fornecida pelo fornecedor.","cardinalidade":"1..1"},
{"id":"/Invoice/InvoiceLine/AllowanceCharge/ChargeIndicator","descricao":"Indica se o valor é um encargo ou um desconto da linha do documento. Indicador de encargo (true). Indicador de desconto (false).","cardinalidade":"1..1"},
{"id":"/Invoice/InvoiceLine/AllowanceCharge/AllowanceChargeReasonCode","descricao":"Código do motivo, que possa levar a que o montante contemplado no desconto/encargo, esteja isento de imposto.","cardinalidade":"0..1"},
{"id":"/Invoice/InvoiceLine/AllowanceCharge/AllowanceChargeReason","descricao":"Representação textual da acção da linha do documento.","cardinalidade":"0..1"},
{"id":"/Invoice/InvoiceLine/AllowanceCharge/MultiplierFactorNumeric","descricao":"Fator multiplicador sobre o montante base da acção da linha do documento.","cardinalidade":"0..1"},
{"id":"/Invoice/InvoiceLine/AllowanceCharge/Amount","descricao":"Montante do encargo/desconto da linha do documento.A Moeda, segundo a lista de códigos ISO4217 (https://www.iso.org/iso-4217-currency-codes.html) [EUR]","cardinalidade":"1..1"},
{"id":"/Invoice/InvoiceLine/AllowanceCharge/BaseAmount","descricao":"Montante base da acção da linha do documento.A Moeda, segundo a lista de códigos ISO4217 (https://www.iso.org/iso-4217-currency-codes.html) [EUR]","cardinalidade":"0..1"},
{"id":"/Invoice/InvoiceLine/Item/Description","descricao":"Descrição do item da linha do documento.","cardinalidade":"0..*"},
{"id":"/Invoice/InvoiceLine/Item/Name","descricao":"Nome do item da linha do documento.","cardinalidade":"1..1"},
{"id":"/Invoice/InvoiceLine/Item/BuyersItemIdentification/ID","descricao":"Código de material do cliente.","cardinalidade":"1..1"},
{"id":"/Invoice/InvoiceLine/Item/SellersItemIdentification/ID","descricao":"Código de material usado pelo fornecedor para identificar univocamente o item da linha do documento.","cardinalidade":"1..1"},
{"id":"/Invoice/InvoiceLine/Item/StandardItemIdentification/ID","descricao":"Identificador do item da linha do documento de acordo com um esquema padrão (GTIN). A propriedade schemeID deve mencionar a norma de códigos EAN .","cardinalidade":"1..1"},
{"id":"/Invoice/InvoiceLine/Item/OriginCountry/IdentificationCode","descricao":"País de origem do item, segundo o código ISO 3166-1 alfa-2","cardinalidade":"1..1"},
{"id":"/Invoice/InvoiceLine/Item/CommodityClassification/ItemClassificationCode","descricao":"Código da classificação da mercadoria do item da linha do documento empregue na Administração Pública.Se o atributo listID for CPV, será considerado como o código CPV associado ao item da linha do documento.","cardinalidade":"1..1"},
{"id":"/Invoice/InvoiceLine/Item/ClassifiedTaxCategory/ID","descricao":"Código de imposto respeitante à taxa aplicada no item da linha do documento, segundo a lista de códigos UN/ECE 5305,[Predefinição: S]","cardinalidade":"1..1"},
{"id":"/Invoice/InvoiceLine/Item/ClassifiedTaxCategory/Percent","descricao":"Percentagem de imposto respeitante à taxa aplicada no item da linha do documento","cardinalidade":"1..1"},
{"id":"/Invoice/InvoiceLine/Item/ClassifiedTaxCategory/TaxScheme/ID","descricao":"Tipo de imposto do item da linha do documento, segundo a lista de códigos UN/ECE 5153. [Predefinição: VAT]","cardinalidade":"1..1"},
{"id":"/Invoice/InvoiceLine/Item/AdditionalItemProperty/Name","descricao":"Tipo da propriedade adicional do item da linha do documento.","cardinalidade":"1..1"},
{"id":"/Invoice/InvoiceLine/Item/AdditionalItemProperty/Value","descricao":"Valor da propriedade do item da linha do documento.","cardinalidade":"1..1"},
{"id":"/Invoice/InvoiceLine/Price/PriceAmount","descricao":"Montante do item após aplicação do desconto.Estrutura que guarda a informação de preço do item por quantidade base. Este preço, no caso de preenchida a estrtura de desconto sobre o preço, já será o resultante da aplicabilidade do referido desconto. A Moeda, segundo a lista de códigos ISO4217 (https://www.iso.org/iso-4217-currency-codes.html) [EUR]","cardinalidade":"1..1"},
{"id":"/Invoice/InvoiceLine/Price/BaseQuantity","descricao":"Número de quantidades que fazem o montante do preço. Por exemplo, se a quantidade faturada for 1000 litros, o preço pode ser 15e por 10 litros. A propriedade unitCode deverá ser preenchida com o código UNECERec20 de unidade medida, ex: KGM (quilograma).","cardinalidade":"0..1"},
{"id":"/Invoice/InvoiceLine/Price/AllowanceCharge/ChargeIndicator","descricao":"Indica se o valor é um encargo (true) ou um desconto (false) do preço do item da linha do documento.","cardinalidade":"1..1"},
{"id":"/Invoice/InvoiceLine/Price/AllowanceCharge/Amount","descricao":"Montante do desconto ou encardo sobre o preço do item da linha do documento.A Moeda, segundo a lista de códigos ISO4217 (https://www.iso.org/iso-4217-currency-codes.html) [EUR]","cardinalidade":"1..1"},
{"id":"/Invoice/InvoiceLine/Price/AllowanceCharge/BaseAmount","descricao":"Montante base onde incidirá o desconto ou encargo.A Moeda, segundo a lista de códigos ISO4217 (https://www.iso.org/iso-4217-currency-codes.html) [EUR]","cardinalidade":"0..1"}
]
```

### Fonte cius-pt-ubl-mensagem-de-estado: Modelo UBL 2.1 CIUS-PT anotado: Mensagem de estado (modelo sintático (XML anotado)) — complementar: só para confirmar cardinalidades e descrições

Papel: sintaxe UBL da mensagem de estado (resposta do adquirente)

Grupos (20):
```json
[
{"id":"/DocumentStatus","nome":"DocumentStatus","cardinalidade":"1..1"},
{"id":"/DocumentStatus/SenderParty","nome":"SenderParty","cardinalidade":"1..1","pai":"/DocumentStatus"},
{"id":"/DocumentStatus/SenderParty/PartyName","nome":"PartyName","cardinalidade":"0..1","pai":"/DocumentStatus/SenderParty"},
{"id":"/DocumentStatus/SenderParty/PostalAddress","nome":"PostalAddress","cardinalidade":"1..1","pai":"/DocumentStatus/SenderParty"},
{"id":"/DocumentStatus/SenderParty/PostalAddress/Country","nome":"Country","cardinalidade":"1..1","pai":"/DocumentStatus/SenderParty/PostalAddress"},
{"id":"/DocumentStatus/SenderParty/PartyTaxScheme","nome":"PartyTaxScheme","cardinalidade":"1..1","pai":"/DocumentStatus/SenderParty"},
{"id":"/DocumentStatus/SenderParty/PartyTaxScheme/TaxScheme","nome":"TaxScheme","cardinalidade":"1..1","pai":"/DocumentStatus/SenderParty/PartyTaxScheme"},
{"id":"/DocumentStatus/SenderParty/PartyLegalEntity","nome":"PartyLegalEntity","cardinalidade":"1..1","pai":"/DocumentStatus/SenderParty"},
{"id":"/DocumentStatus/SenderParty/Contact","nome":"Contact","cardinalidade":"0..1","pai":"/DocumentStatus/SenderParty"},
{"id":"/DocumentStatus/ReceiverParty","nome":"ReceiverParty","cardinalidade":"1..1","pai":"/DocumentStatus"},
{"id":"/DocumentStatus/ReceiverParty/PartyName","nome":"PartyName","cardinalidade":"0..1","pai":"/DocumentStatus/ReceiverParty"},
{"id":"/DocumentStatus/ReceiverParty/PostalAddress","nome":"PostalAddress","cardinalidade":"1..1","pai":"/DocumentStatus/ReceiverParty"},
{"id":"/DocumentStatus/ReceiverParty/PostalAddress/Country","nome":"Country","cardinalidade":"1..1","pai":"/DocumentStatus/ReceiverParty/PostalAddress"},
{"id":"/DocumentStatus/ReceiverParty/PartyTaxScheme","nome":"PartyTaxScheme","cardinalidade":"1..1","pai":"/DocumentStatus/ReceiverParty"},
{"id":"/DocumentStatus/ReceiverParty/PartyTaxScheme/TaxScheme","nome":"TaxScheme","cardinalidade":"1..1","pai":"/DocumentStatus/ReceiverParty/PartyTaxScheme"},
{"id":"/DocumentStatus/ReceiverParty/PartyLegalEntity","nome":"PartyLegalEntity","cardinalidade":"1..1","pai":"/DocumentStatus/ReceiverParty"},
{"id":"/DocumentStatus/ReceiverParty/Contact","nome":"Contact","cardinalidade":"0..1","pai":"/DocumentStatus/ReceiverParty"},
{"id":"/DocumentStatus/DocumentResponse","nome":"DocumentResponse","cardinalidade":"0..1","pai":"/DocumentStatus"},
{"id":"/DocumentStatus/DocumentResponse/Response","nome":"Response","cardinalidade":"1..1","pai":"/DocumentStatus/DocumentResponse"},
{"id":"/DocumentStatus/DocumentResponse/DocumentReference","nome":"DocumentReference","cardinalidade":"1..1","pai":"/DocumentStatus/DocumentResponse"}
]
```

Elementos (26):
```json
[
{"id":"/DocumentStatus/CustomizationID","descricao":"ID Costumização [Predefinição: urn:feap.gov.pt:MSGSTS_CIUS-PT: seguido do identificador da versão]","cardinalidade":"1..1"},
{"id":"/DocumentStatus/ID","descricao":"Número de referência deste documento emitido pelo emissor desta mensagem","cardinalidade":"1..1"},
{"id":"/DocumentStatus/IssueDate","descricao":"Data de emissão da mensagem de estado [AAAA-MM-DD]","cardinalidade":"1..1"},
{"id":"/DocumentStatus/IssueTime","descricao":"Hora de emissão da mensagem de estado [HH:MM:SS]","cardinalidade":"0..1"},
{"id":"/DocumentStatus/Note","descricao":"Notas textuais que permitem ao emissor enviar informação não estruturada relativa ao documento","cardinalidade":"1..*"},
{"id":"/DocumentStatus/SenderParty/PartyName/Name","descricao":"Nome do emissor da mensagem de estado.","cardinalidade":"1..1"},
{"id":"/DocumentStatus/SenderParty/PostalAddress/Country/IdentificationCode","descricao":"Código identificador do país da morada do emissor da mensagem de estado de acordo com os códigos ISO 3166-1 alfa-2.","cardinalidade":"1..1"},
{"id":"/DocumentStatus/SenderParty/PartyTaxScheme/CompanyID","descricao":"Número de identificação fiscal do emissor da mensagem de estado precedido do código do país, segundo o código ISO 3166-1 alfa-2","cardinalidade":"1..1"},
{"id":"/DocumentStatus/SenderParty/PartyTaxScheme/TaxScheme/ID","descricao":"O valor do ID corresponde à lista de códigos UN/ECE 5153, da Comissão Económica das Nações Unidas para a Europa. [Predefinição: VAT]","cardinalidade":"1..1"},
{"id":"/DocumentStatus/SenderParty/PartyLegalEntity/RegistrationName","descricao":"Identificação do emissor da mensagem de estado na IRN","cardinalidade":"1..1"},
{"id":"/DocumentStatus/SenderParty/PartyLegalEntity/CompanyID","descricao":"Número de Identificação do emissor da mensagem de estado na conservatória","cardinalidade":"0..1"},
{"id":"/DocumentStatus/SenderParty/Contact/ElectronicMail","descricao":"Endereço de correio eletrónico do emissor da mensagem de estado.","cardinalidade":"1..1"},
{"id":"/DocumentStatus/ReceiverParty/PartyName/Name","descricao":"Nome do receptor da mensagem de estado.","cardinalidade":"1..1"},
{"id":"/DocumentStatus/ReceiverParty/PostalAddress/Country/IdentificationCode","descricao":"Código identificador do país da morada do receptor da mensagem de estado de acordo com os códigos ISO 3166-1 alfa-2","cardinalidade":"1..1"},
{"id":"/DocumentStatus/ReceiverParty/PartyTaxScheme/CompanyID","descricao":"Número de identificação fiscal do receptor da mensagem de estado precedido do código do país, segundo o código ISO 3166-1 alfa-2","cardinalidade":"1..1"},
{"id":"/DocumentStatus/ReceiverParty/PartyTaxScheme/TaxScheme/ID","descricao":"O valor do ID corresponde à lista de códigos UN/ECE 5153, da Comissão Económica das Nações Unidas para a Europa. [Predefinição: VAT]","cardinalidade":"1..1"},
{"id":"/DocumentStatus/ReceiverParty/PartyLegalEntity/RegistrationName","descricao":"Identificação do receptor da mensagem de estado na IRN","cardinalidade":"1..1"},
{"id":"/DocumentStatus/ReceiverParty/PartyLegalEntity/CompanyID","descricao":"Número de Identificação do receptor da mensagem de estado na conservatória","cardinalidade":"0..1"},
{"id":"/DocumentStatus/ReceiverParty/Contact/ElectronicMail","descricao":"Endereço de correio eletrónico do receptor da mensagem de estado.","cardinalidade":"1..1"},
{"id":"/DocumentStatus/DocumentResponse/Response/ResponseCode","descricao":"Código da resposta","cardinalidade":"1..1"},
{"id":"/DocumentStatus/DocumentResponse/Response/Description","descricao":"Nota textual, que permite discriminar o(s) erro(s), ou o(s) aviso(s) ou a(s) informação (ões).","cardinalidade":"0..*"},
{"id":"/DocumentStatus/DocumentResponse/DocumentReference/ID","descricao":"Número de referência do documento que deu origem a esta mensagem.","cardinalidade":"1..1"},
{"id":"/DocumentStatus/DocumentResponse/DocumentReference/UUID","descricao":"Número de referência universal do documento (UUID)","cardinalidade":"0..1"},
{"id":"/DocumentStatus/DocumentResponse/DocumentReference/IssueDate","descricao":"Data de emissão do documento.[AAAA-MM-DD]","cardinalidade":"1..1"},
{"id":"/DocumentStatus/DocumentResponse/DocumentReference/DocumentTypeCode","descricao":"Código que identifica o tipo funcional do documento, segundo a lista de códigos UNCL1001 (http://www.unece.org/trade/untdid/d98a/uncl/uncl1001.htm) [FE: 380 / ND: 383] / NC: 381","cardinalidade":"1..1"},
{"id":"/DocumentStatus/DocumentResponse/DocumentReference/DocumentStatusCode","descricao":"Código do estado do documento, na prespectiva do cliente referenciado no mesmo.","cardinalidade":"0..1"}
]
```

### Fonte cius-pt-ubl-nota-de-credito: Modelo UBL 2.1 CIUS-PT anotado: Nota de Credito (modelo sintático (XML anotado)) — complementar: só para confirmar cardinalidades e descrições

Papel: sintaxe UBL da nota de crédito

Grupos (84):
```json
[
{"id":"/CreditNote","nome":"CreditNote","cardinalidade":"1..1"},
{"id":"/CreditNote/InvoicePeriod","nome":"InvoicePeriod","cardinalidade":"0..1","pai":"/CreditNote"},
{"id":"/CreditNote/OrderReference","nome":"OrderReference","cardinalidade":"0..1","pai":"/CreditNote"},
{"id":"/CreditNote/BillingReference","nome":"BillingReference","cardinalidade":"0..*","pai":"/CreditNote"},
{"id":"/CreditNote/BillingReference/InvoiceDocumentReference","nome":"InvoiceDocumentReference","cardinalidade":"1..1","pai":"/CreditNote/BillingReference"},
{"id":"/CreditNote/DespatchDocumentReference","nome":"DespatchDocumentReference","cardinalidade":"0..*","pai":"/CreditNote"},
{"id":"/CreditNote/ReceiptDocumentReference","nome":"ReceiptDocumentReference","cardinalidade":"0..1","pai":"/CreditNote"},
{"id":"/CreditNote/ContractDocumentReference","nome":"ContractDocumentReference","cardinalidade":"0..1","pai":"/CreditNote"},
{"id":"/CreditNote/AdditionalDocumentReference","nome":"AdditionalDocumentReference","cardinalidade":"0..*","pai":"/CreditNote"},
{"id":"/CreditNote/AdditionalDocumentReference","nome":"AdditionalDocumentReference","cardinalidade":"0..*","pai":"/CreditNote"},
{"id":"/CreditNote/AdditionalDocumentReference/Attachment","nome":"Attachment","cardinalidade":"0..1","pai":"/CreditNote/AdditionalDocumentReference"},
{"id":"/CreditNote/AdditionalDocumentReference/Attachment/ExternalReference","nome":"ExternalReference","cardinalidade":"0..1","pai":"/CreditNote/AdditionalDocumentReference/Attachment"},
{"id":"/CreditNote/OriginatorDocumentReference","nome":"OriginatorDocumentReference","cardinalidade":"0..*","pai":"/CreditNote"},
{"id":"/CreditNote/AccountingSupplierParty","nome":"AccountingSupplierParty","cardinalidade":"1..1","pai":"/CreditNote"},
{"id":"/CreditNote/AccountingSupplierParty/Party","nome":"Party","cardinalidade":"1..1","pai":"/CreditNote/AccountingSupplierParty"},
{"id":"/CreditNote/AccountingSupplierParty/Party/PartyIdentification","nome":"PartyIdentification","cardinalidade":"0..*","pai":"/CreditNote/AccountingSupplierParty/Party"},
{"id":"/CreditNote/AccountingSupplierParty/Party/PartyName","nome":"PartyName","cardinalidade":"0..1","pai":"/CreditNote/AccountingSupplierParty/Party"},
{"id":"/CreditNote/AccountingSupplierParty/Party/PostalAddress","nome":"PostalAddress","cardinalidade":"1..1","pai":"/CreditNote/AccountingSupplierParty/Party"},
{"id":"/CreditNote/AccountingSupplierParty/Party/PostalAddress/AddressLine","nome":"AddressLine","cardinalidade":"0..1","pai":"/CreditNote/AccountingSupplierParty/Party/PostalAddress"},
{"id":"/CreditNote/AccountingSupplierParty/Party/PostalAddress/Country","nome":"Country","cardinalidade":"1..1","pai":"/CreditNote/AccountingSupplierParty/Party/PostalAddress"},
{"id":"/CreditNote/AccountingSupplierParty/Party/PartyTaxScheme","nome":"PartyTaxScheme","cardinalidade":"0..1","pai":"/CreditNote/AccountingSupplierParty/Party"},
{"id":"/CreditNote/AccountingSupplierParty/Party/PartyTaxScheme/TaxScheme","nome":"TaxScheme","cardinalidade":"1..1","pai":"/CreditNote/AccountingSupplierParty/Party/PartyTaxScheme"},
{"id":"/CreditNote/AccountingSupplierParty/Party/PartyLegalEntity","nome":"PartyLegalEntity","cardinalidade":"1..1","pai":"/CreditNote/AccountingSupplierParty/Party"},
{"id":"/CreditNote/AccountingSupplierParty/Party/Contact","nome":"Contact","cardinalidade":"0..1","pai":"/CreditNote/AccountingSupplierParty/Party"},
{"id":"/CreditNote/AccountingCustomerParty","nome":"AccountingCustomerParty","cardinalidade":"1..1","pai":"/CreditNote"},
{"id":"/CreditNote/AccountingCustomerParty/Party","nome":"Party","cardinalidade":"1..1","pai":"/CreditNote/AccountingCustomerParty"},
{"id":"/CreditNote/AccountingCustomerParty/Party/PartyIdentification","nome":"PartyIdentification","cardinalidade":"0..*","pai":"/CreditNote/AccountingCustomerParty/Party"},
{"id":"/CreditNote/AccountingCustomerParty/Party/PartyName","nome":"PartyName","cardinalidade":"0..1","pai":"/CreditNote/AccountingCustomerParty/Party"},
{"id":"/CreditNote/AccountingCustomerParty/Party/PostalAddress","nome":"PostalAddress","cardinalidade":"1..1","pai":"/CreditNote/AccountingCustomerParty/Party"},
{"id":"/CreditNote/AccountingCustomerParty/Party/PostalAddress/AddressLine","nome":"AddressLine","cardinalidade":"0..1","pai":"/CreditNote/AccountingCustomerParty/Party/PostalAddress"},
{"id":"/CreditNote/AccountingCustomerParty/Party/PostalAddress/Country","nome":"Country","cardinalidade":"1..1","pai":"/CreditNote/AccountingCustomerParty/Party/PostalAddress"},
{"id":"/CreditNote/AccountingCustomerParty/Party/PartyTaxScheme","nome":"PartyTaxScheme","cardinalidade":"0..1","pai":"/CreditNote/AccountingCustomerParty/Party"},
{"id":"/CreditNote/AccountingCustomerParty/Party/PartyTaxScheme/TaxScheme","nome":"TaxScheme","cardinalidade":"1..1","pai":"/CreditNote/AccountingCustomerParty/Party/PartyTaxScheme"},
{"id":"/CreditNote/AccountingCustomerParty/Party/PartyLegalEntity","nome":"PartyLegalEntity","cardinalidade":"1..1","pai":"/CreditNote/AccountingCustomerParty/Party"},
{"id":"/CreditNote/AccountingCustomerParty/Party/Contact","nome":"Contact","cardinalidade":"0..1","pai":"/CreditNote/AccountingCustomerParty/Party"},
{"id":"/CreditNote/PayeeParty","nome":"PayeeParty","cardinalidade":"0..1","pai":"/CreditNote"},
{"id":"/CreditNote/PayeeParty/PartyIdentification","nome":"PartyIdentification","cardinalidade":"0..1","pai":"/CreditNote/PayeeParty"},
{"id":"/CreditNote/PayeeParty/PartyName","nome":"PartyName","cardinalidade":"1..1","pai":"/CreditNote/PayeeParty"},
{"id":"/CreditNote/PayeeParty/PartyLegalEntity","nome":"PartyLegalEntity","cardinalidade":"1..1","pai":"/CreditNote/PayeeParty"},
{"id":"/CreditNote/TaxRepresentativeParty","nome":"TaxRepresentativeParty","cardinalidade":"0..1","pai":"/CreditNote"},
{"id":"/CreditNote/TaxRepresentativeParty/PartyName","nome":"PartyName","cardinalidade":"1..1","pai":"/CreditNote/TaxRepresentativeParty"},
{"id":"/CreditNote/TaxRepresentativeParty/PostalAddress","nome":"PostalAddress","cardinalidade":"1..1","pai":"/CreditNote/TaxRepresentativeParty"},
{"id":"/CreditNote/TaxRepresentativeParty/PostalAddress/AddressLine","nome":"AddressLine","cardinalidade":"0..1","pai":"/CreditNote/TaxRepresentativeParty/PostalAddress"},
{"id":"/CreditNote/TaxRepresentativeParty/PostalAddress/Country","nome":"Country","cardinalidade":"1..1","pai":"/CreditNote/TaxRepresentativeParty/PostalAddress"},
{"id":"/CreditNote/TaxRepresentativeParty/PartyTaxScheme","nome":"PartyTaxScheme","cardinalidade":"1..1","pai":"/CreditNote/TaxRepresentativeParty"},
{"id":"/CreditNote/TaxRepresentativeParty/PartyTaxScheme/TaxScheme","nome":"TaxScheme","cardinalidade":"1..1","pai":"/CreditNote/TaxRepresentativeParty/PartyTaxScheme"},
{"id":"/CreditNote/Delivery","nome":"Delivery","cardinalidade":"1..*","pai":"/CreditNote"},
{"id":"/CreditNote/Delivery/DeliveryLocation","nome":"DeliveryLocation","cardinalidade":"0..1","pai":"/CreditNote/Delivery"},
{"id":"/CreditNote/Delivery/DeliveryLocation/Address","nome":"Address","cardinalidade":"0..1","pai":"/CreditNote/Delivery/DeliveryLocation"},
{"id":"/CreditNote/Delivery/DeliveryLocation/Address/AddressLine","nome":"AddressLine","cardinalidade":"0..1","pai":"/CreditNote/Delivery/DeliveryLocation/Address"},
{"id":"/CreditNote/Delivery/DeliveryLocation/Address/Country","nome":"Country","cardinalidade":"1..1","pai":"/CreditNote/Delivery/DeliveryLocation/Address"},
{"id":"/CreditNote/Delivery/DeliveryParty","nome":"DeliveryParty","cardinalidade":"0..1","pai":"/CreditNote/Delivery"},
{"id":"/CreditNote/Delivery/DeliveryParty/PartyName","nome":"PartyName","cardinalidade":"0..*","pai":"/CreditNote/Delivery/DeliveryParty"},
{"id":"/CreditNote/PaymentMeans","nome":"PaymentMeans","cardinalidade":"0..1","pai":"/CreditNote"},
{"id":"/CreditNote/PaymentMeans/CardAccount","nome":"CardAccount","cardinalidade":"0..1","pai":"/CreditNote/PaymentMeans"},
{"id":"/CreditNote/PaymentMeans/PayeeFinancialAccount","nome":"PayeeFinancialAccount","cardinalidade":"0..*","pai":"/CreditNote/PaymentMeans"},
{"id":"/CreditNote/PaymentMeans/PayeeFinancialAccount/FinancialInstitutionBranch","nome":"FinancialInstitutionBranch","cardinalidade":"0..1","pai":"/CreditNote/PaymentMeans/PayeeFinancialAccount"},
{"id":"/CreditNote/PaymentMeans/PaymentMandate","nome":"PaymentMandate","cardinalidade":"0..1","pai":"/CreditNote/PaymentMeans"},
{"id":"/CreditNote/PaymentMeans/PaymentMandate/PayerFinancialAccount","nome":"PayerFinancialAccount","cardinalidade":"0..1","pai":"/CreditNote/PaymentMeans/PaymentMandate"},
{"id":"/CreditNote/PaymentTerms","nome":"PaymentTerms","cardinalidade":"0..1","pai":"/CreditNote"},
{"id":"/CreditNote/AllowanceCharge","nome":"AllowanceCharge","cardinalidade":"0..*","pai":"/CreditNote"},
{"id":"/CreditNote/AllowanceCharge/TaxCategory","nome":"TaxCategory","cardinalidade":"0..1","pai":"/CreditNote/AllowanceCharge"},
{"id":"/CreditNote/AllowanceCharge/TaxCategory/TaxScheme","nome":"TaxScheme","cardinalidade":"1..1","pai":"/CreditNote/AllowanceCharge/TaxCategory"},
{"id":"/CreditNote/TaxTotal","nome":"TaxTotal","cardinalidade":"0..1","pai":"/CreditNote"},
{"id":"/CreditNote/TaxTotal/TaxSubtotal","nome":"TaxSubtotal","cardinalidade":"1..*","pai":"/CreditNote/TaxTotal"},
{"id":"/CreditNote/TaxTotal/TaxSubtotal/TaxCategory","nome":"TaxCategory","cardinalidade":"1..1","pai":"/CreditNote/TaxTotal/TaxSubtotal"},
{"id":"/CreditNote/TaxTotal/TaxSubtotal/TaxCategory/TaxScheme","nome":"TaxScheme","cardinalidade":"1..1","pai":"/CreditNote/TaxTotal/TaxSubtotal/TaxCategory"},
{"id":"/CreditNote/LegalMonetaryTotal","nome":"LegalMonetaryTotal","cardinalidade":"1..1","pai":"/CreditNote"},
{"id":"/CreditNote/CreditNoteLine","nome":"CreditNoteLine","cardinalidade":"1..*","pai":"/CreditNote"},
{"id":"/CreditNote/CreditNoteLine/InvoicePeriod","nome":"InvoicePeriod","cardinalidade":"0..1","pai":"/CreditNote/CreditNoteLine"},
{"id":"/CreditNote/CreditNoteLine/OrderLineReference","nome":"OrderLineReference","cardinalidade":"0..1","pai":"/CreditNote/CreditNoteLine"},
{"id":"/CreditNote/CreditNoteLine/DocumentReference","nome":"DocumentReference","cardinalidade":"0..1","pai":"/CreditNote/CreditNoteLine"},
{"id":"/CreditNote/CreditNoteLine/AllowanceCharge","nome":"AllowanceCharge","cardinalidade":"0..*","pai":"/CreditNote/CreditNoteLine"},
{"id":"/CreditNote/CreditNoteLine/Item","nome":"Item","cardinalidade":"1..1","pai":"/CreditNote/CreditNoteLine"},
{"id":"/CreditNote/CreditNoteLine/Item/BuyersItemIdentification","nome":"BuyersItemIdentification","cardinalidade":"0..1","pai":"/CreditNote/CreditNoteLine/Item"},
{"id":"/CreditNote/CreditNoteLine/Item/SellersItemIdentification","nome":"SellersItemIdentification","cardinalidade":"0..1","pai":"/CreditNote/CreditNoteLine/Item"},
{"id":"/CreditNote/CreditNoteLine/Item/StandardItemIdentification","nome":"StandardItemIdentification","cardinalidade":"0..1","pai":"/CreditNote/CreditNoteLine/Item"},
{"id":"/CreditNote/CreditNoteLine/Item/OriginCountry","nome":"OriginCountry","cardinalidade":"0..1","pai":"/CreditNote/CreditNoteLine/Item"},
{"id":"/CreditNote/CreditNoteLine/Item/CommodityClassification","nome":"CommodityClassification","cardinalidade":"0..*","pai":"/CreditNote/CreditNoteLine/Item"},
{"id":"/CreditNote/CreditNoteLine/Item/ClassifiedTaxCategory","nome":"ClassifiedTaxCategory","cardinalidade":"1..1","pai":"/CreditNote/CreditNoteLine/Item"},
{"id":"/CreditNote/CreditNoteLine/Item/ClassifiedTaxCategory/TaxScheme","nome":"TaxScheme","cardinalidade":"1..1","pai":"/CreditNote/CreditNoteLine/Item/ClassifiedTaxCategory"},
{"id":"/CreditNote/CreditNoteLine/Item/AdditionalItemProperty","nome":"AdditionalItemProperty","cardinalidade":"0..*","pai":"/CreditNote/CreditNoteLine/Item"},
{"id":"/CreditNote/CreditNoteLine/Price","nome":"Price","cardinalidade":"1..1","pai":"/CreditNote/CreditNoteLine"},
{"id":"/CreditNote/CreditNoteLine/Price/AllowanceCharge","nome":"AllowanceCharge","cardinalidade":"0..1","pai":"/CreditNote/CreditNoteLine/Price"}
]
```

Elementos (154):
```json
[
{"id":"/CreditNote/CustomizationID","descricao":"ID Costumização [Predefinição: ESPAP: urn:www:espap:pt:profiles:profile1:seguido do identificador da versão]","cardinalidade":"1..1"},
{"id":"/CreditNote/ProfileID","descricao":"Perfil onde se enquadra a customização associada ao Template UBL 2.1","cardinalidade":"0..1"},
{"id":"/CreditNote/ID","descricao":"Número do documento","cardinalidade":"1..1"},
{"id":"/CreditNote/IssueDate","descricao":"Data de emissão do documento [AAAA-MM-DD]","cardinalidade":"1..1"},
{"id":"/CreditNote/TaxPointDate","descricao":"A data em que o IVA se torna aplicável para o Vendedor e para o Comprador na medida em que essa data pode ser determinada e difere da data de emissão da fatura, de acordo com a diretiva do IVA [AAAA-MM-DD]","cardinalidade":"0..1"},
{"id":"/CreditNote/CreditNoteTypeCode","descricao":"Código que identifica o tipo funcional da fatura eletrónica, segundo a lista de códigos UNCL1001 (http://www.unece.org/trade/untdid/d98a/uncl/uncl1001.htm) [NC: 381]","cardinalidade":"1..1"},
{"id":"/CreditNote/Note","descricao":"Notas textuais que permitem ao fornecedor enviar informação não estruturada relativa ao documento.","cardinalidade":"0..*"},
{"id":"/CreditNote/DocumentCurrencyCode","descricao":"Moeda, segundo a lista de códigos ISO4217 (https://www.iso.org/iso-4217-currency-codes.html) [Predefinição: EUR]","cardinalidade":"1..1"},
{"id":"/CreditNote/TaxCurrencyCode","descricao":"A moeda usada para fins de contabilidade e relatórios de IVA, conforme aceite ou exigida no país do vendedor.","cardinalidade":"0..1"},
{"id":"/CreditNote/AccountingCost","descricao":"Número do compromisso.","cardinalidade":"0..1"},
{"id":"/CreditNote/BuyerReference","descricao":"Referência do Cliente","cardinalidade":"0..1"},
{"id":"/CreditNote/InvoicePeriod/StartDate","descricao":"A data em que o período de faturação começa.[AAAA-MM-DD]","cardinalidade":"0..1"},
{"id":"/CreditNote/InvoicePeriod/EndDate","descricao":"A data em que o período de faturação acaba.[AAAA-MM-DD]","cardinalidade":"0..1"},
{"id":"/CreditNote/InvoicePeriod/DescriptionCode","descricao":"O código da data em que o IVA se torna aplicável pelo vendedor e pelo comprador.","cardinalidade":"0..1"},
{"id":"/CreditNote/OrderReference/ID","descricao":"Número da nota de encomenda.","cardinalidade":"0..1"},
{"id":"/CreditNote/OrderReference/SalesOrderID","descricao":"Número da ordem de venda, emitida pelo fornecedor.","cardinalidade":"0..1"},
{"id":"/CreditNote/BillingReference/InvoiceDocumentReference/ID","descricao":"Número de referência do documento, emitido pelo fornecedor, anteriormente enviado.","cardinalidade":"1..1"},
{"id":"/CreditNote/BillingReference/InvoiceDocumentReference/IssueDate","descricao":"Data de emissão do documento, anteriormente enviado.[AAAA-MM-DD]","cardinalidade":"0..1"},
{"id":"/CreditNote/DespatchDocumentReference/ID","descricao":"Referência do aviso de envio.","cardinalidade":"1..1"},
{"id":"/CreditNote/ReceiptDocumentReference/ID","descricao":"Número do aviso de recebimento referenciado.","cardinalidade":"1..1"},
{"id":"/CreditNote/ContractDocumentReference/ID","descricao":"Número do contrato.","cardinalidade":"1..1"},
{"id":"/CreditNote/AdditionalDocumentReference/ID","descricao":"Identificador do processo de registo de entrada do documento.Identificador do anexo referenciado de acordo com a norma UNCL1153 (https://docs.peppol.eu/poacc/billing/3.0/codelist/UNCL1153/) Scheme ID = AIM para colocar UUID","cardinalidade":"0..1"},
{"id":"/CreditNote/AdditionalDocumentReference/ID","descricao":"Identificador do processo de registo de entrada do documento.Identificador do anexo referenciado de acordo com a norma UNCL1153 (https://docs.peppol.eu/poacc/billing/3.0/codelist/UNCL1153/)","cardinalidade":"0..1"},
{"id":"/CreditNote/AdditionalDocumentReference/DocumentTypeCode","descricao":"Código que identifica o tipo funcional da fatura eletrónica, segundo a lista de códigos UNCL1001 (http://www.unece.org/trade/untdid/d98a/uncl/uncl1001.htm) [NC: 381]","cardinalidade":"0..1"},
{"id":"/CreditNote/AdditionalDocumentReference/DocumentDescription","descricao":"Descrição do documento anexado.[Predefinição: Facturas: CREDITNOTE_REPRESENTATION | Anexos: ATTACHMENT]","cardinalidade":"0..1"},
{"id":"/CreditNote/AdditionalDocumentReference/Attachment/EmbeddedDocumentBinaryObject","descricao":"Documento codificado em base 64","cardinalidade":"0..1"},
{"id":"/CreditNote/AdditionalDocumentReference/Attachment/ExternalReference/URI","descricao":"Endereço para um documento, localizado externamente.","cardinalidade":"1..1"},
{"id":"/CreditNote/OriginatorDocumentReference/ID","descricao":"Número do acordo quadro.","cardinalidade":"1..1"},
{"id":"/CreditNote/AccountingSupplierParty/Party/EndpointID","descricao":"Código de identificação do Fornecedor, por exemplo GLN, URN etc","cardinalidade":"0..1"},
{"id":"/CreditNote/AccountingSupplierParty/Party/PartyIdentification/ID","descricao":"Identificação do vendedor (ID Bancário)","cardinalidade":"1..1"},
{"id":"/CreditNote/AccountingSupplierParty/Party/PartyName/Name","descricao":"Nome do fornecedor","cardinalidade":"1..1"},
{"id":"/CreditNote/AccountingSupplierParty/Party/PostalAddress/StreetName","descricao":"Morada do fornecedor","cardinalidade":"1..1"},
{"id":"/CreditNote/AccountingSupplierParty/Party/PostalAddress/AdditionalStreetName","descricao":"Morada do fornecedor (adicional)","cardinalidade":"0..1"},
{"id":"/CreditNote/AccountingSupplierParty/Party/PostalAddress/CityName","descricao":"Cidade do fornecedor","cardinalidade":"1..1"},
{"id":"/CreditNote/AccountingSupplierParty/Party/PostalAddress/PostalZone","descricao":"Código Postal do fornecedor","cardinalidade":"1..1"},
{"id":"/CreditNote/AccountingSupplierParty/Party/PostalAddress/CountrySubentity","descricao":"Região/Província da morada do fornecedor","cardinalidade":"0..1"},
{"id":"/CreditNote/AccountingSupplierParty/Party/PostalAddress/AddressLine/Line","descricao":"Linha de endereço adicional que pode ser usado para fornecer mais detalhes, complementando a linha principal.","cardinalidade":"1..1"},
{"id":"/CreditNote/AccountingSupplierParty/Party/PostalAddress/Country/IdentificationCode","descricao":"País do fornecedor, segundo o código ISO 3166-1 alfa-2","cardinalidade":"1..1"},
{"id":"/CreditNote/AccountingSupplierParty/Party/PartyTaxScheme/CompanyID","descricao":"Número de identificação fiscal do fornecedor, precedido do código do país, segundo o código ISO 3166-1 alfa-2","cardinalidade":"1..1"},
{"id":"/CreditNote/AccountingSupplierParty/Party/PartyTaxScheme/TaxScheme/ID","descricao":"O valor do ID corresponde à lista de códigos UN/ECE 5153, da Comissão Económica das Nações Unidas para a Europa. [Predefinição: VAT]","cardinalidade":"1..1"},
{"id":"/CreditNote/AccountingSupplierParty/Party/PartyLegalEntity/RegistrationName","descricao":"Identificação do fornecedor na IRN","cardinalidade":"1..1"},
{"id":"/CreditNote/AccountingSupplierParty/Party/PartyLegalEntity/CompanyID","descricao":"Número de Identificação do fornecedor na conservatória","cardinalidade":"0..1"},
{"id":"/CreditNote/AccountingSupplierParty/Party/PartyLegalEntity/CompanyLegalForm","descricao":"Capital Social do fornecedor","cardinalidade":"0..1"},
{"id":"/CreditNote/AccountingSupplierParty/Party/Contact/Name","descricao":"Ponto de contato do fornecedor.","cardinalidade":"0..1"},
{"id":"/CreditNote/AccountingSupplierParty/Party/Contact/Telephone","descricao":"Contacto telefónico do fornecedor.","cardinalidade":"0..1"},
{"id":"/CreditNote/AccountingSupplierParty/Party/Contact/ElectronicMail","descricao":"Endereço de correio eletrónico do fornecedor.","cardinalidade":"0..1"},
{"id":"/CreditNote/AccountingCustomerParty/Party/EndpointID","descricao":"Código de identificação do Cliente, por exemplo GLN, URN etc","cardinalidade":"0..1"},
{"id":"/CreditNote/AccountingCustomerParty/Party/PartyIdentification/ID","descricao":"Identificação do cliente","cardinalidade":"1..1"},
{"id":"/CreditNote/AccountingCustomerParty/Party/PartyName/Name","descricao":"Nome do cliente","cardinalidade":"1..1"},
{"id":"/CreditNote/AccountingCustomerParty/Party/PostalAddress/StreetName","descricao":"Linha 1 da morada do cliente.","cardinalidade":"0..1"},
{"id":"/CreditNote/AccountingCustomerParty/Party/PostalAddress/AdditionalStreetName","descricao":"Linha 2 da morada do cliente.","cardinalidade":"0..1"},
{"id":"/CreditNote/AccountingCustomerParty/Party/PostalAddress/CityName","descricao":"Cidade do cliente","cardinalidade":"0..1"},
{"id":"/CreditNote/AccountingCustomerParty/Party/PostalAddress/PostalZone","descricao":"Código Postal do cliente","cardinalidade":"0..1"},
{"id":"/CreditNote/AccountingCustomerParty/Party/PostalAddress/CountrySubentity","descricao":"Região/Província da morada do cliente.","cardinalidade":"0..1"},
{"id":"/CreditNote/AccountingCustomerParty/Party/PostalAddress/AddressLine/Line","descricao":"Linha de endereço adicional que pode ser usado para fornecer mais detalhes, complementando a linha principal.","cardinalidade":"1..1"},
{"id":"/CreditNote/AccountingCustomerParty/Party/PostalAddress/Country/IdentificationCode","descricao":"País do cliente, segundo o código ISO 3166-1 alfa-2","cardinalidade":"1..1"},
{"id":"/CreditNote/AccountingCustomerParty/Party/PartyTaxScheme/CompanyID","descricao":"Número de identificação fiscal do cliente, precedido do código do país, segundo o código ISO 3166-1 alfa-2","cardinalidade":"0..1"},
{"id":"/CreditNote/AccountingCustomerParty/Party/PartyTaxScheme/TaxScheme/ID","descricao":"O valor do ID corresponde à lista de códigos UN/ECE 5153, da Comissão Económica das Nações Unidas para a Europa. [Predefinição: VAT]","cardinalidade":"1..1"},
{"id":"/CreditNote/AccountingCustomerParty/Party/PartyLegalEntity/RegistrationName","descricao":"Nome do cliente.","cardinalidade":"1..1"},
{"id":"/CreditNote/AccountingCustomerParty/Party/PartyLegalEntity/CompanyID","descricao":"Informação sobre o registo na conservatória do cliente.","cardinalidade":"0..1"},
{"id":"/CreditNote/AccountingCustomerParty/Party/Contact/Name","descricao":"Ponto de contato do cliente.","cardinalidade":"0..1"},
{"id":"/CreditNote/AccountingCustomerParty/Party/Contact/Telephone","descricao":"Contacto telefónico do cliente.","cardinalidade":"0..1"},
{"id":"/CreditNote/AccountingCustomerParty/Party/Contact/ElectronicMail","descricao":"Email de contacto do cliente","cardinalidade":"0..1"},
{"id":"/CreditNote/PayeeParty/PartyIdentification/ID","descricao":"Identificador do recebedor do pagamento.","cardinalidade":"1..1"},
{"id":"/CreditNote/PayeeParty/PartyName/Name","descricao":"Nome da entidade que recebe o pagamento.","cardinalidade":"1..1"},
{"id":"/CreditNote/PayeeParty/PartyLegalEntity/CompanyID","descricao":"Informação sobre o registo na conservatória do recebedor do pagamento","cardinalidade":"0..1"},
{"id":"/CreditNote/TaxRepresentativeParty/PartyName/Name","descricao":"Nome do representante legal para os temas fiscais.","cardinalidade":"1..1"},
{"id":"/CreditNote/TaxRepresentativeParty/PostalAddress/StreetName","descricao":"Linha 1 da morada do representante legal para os temas fiscais.","cardinalidade":"0..1"},
{"id":"/CreditNote/TaxRepresentativeParty/PostalAddress/AdditionalStreetName","descricao":"Linha 2 da morada do representante legal para os temas fiscais.","cardinalidade":"0..1"},
{"id":"/CreditNote/TaxRepresentativeParty/PostalAddress/CityName","descricao":"Cidade da morada do representante legal para os temas fiscais.","cardinalidade":"0..1"},
{"id":"/CreditNote/TaxRepresentativeParty/PostalAddress/PostalZone","descricao":"Código postal da morada do representante legal para os temas fiscais.","cardinalidade":"0..1"},
{"id":"/CreditNote/TaxRepresentativeParty/PostalAddress/CountrySubentity","descricao":"Região/Província da morada do representante legal para os temas fiscais.","cardinalidade":"0..1"},
{"id":"/CreditNote/TaxRepresentativeParty/PostalAddress/AddressLine/Line","descricao":"Linha de endereço adicional que pode ser usado para fornecer mais detalhes, complementando a linha principal.","cardinalidade":"1..1"},
{"id":"/CreditNote/TaxRepresentativeParty/PostalAddress/Country/IdentificationCode","descricao":"Código identificador do país da morada do representante legal para os temas fiscais.","cardinalidade":"1..1"},
{"id":"/CreditNote/TaxRepresentativeParty/PartyTaxScheme/CompanyID","descricao":"Número de identificação fiscal do representante legal para os temas fiscais.","cardinalidade":"1..1"},
{"id":"/CreditNote/TaxRepresentativeParty/PartyTaxScheme/TaxScheme/ID","descricao":"O valor do ID corresponde à lista de códigos UN/ECE 5153, da Comissão Económica das Nações Unidas para a Europa. [Predefinição:VAT]","cardinalidade":"1..1"},
{"id":"/CreditNote/Delivery/DeliveryLocation/ID","descricao":"Identificador do local em que os bens e serviços são entregues.","cardinalidade":"0..1"},
{"id":"/CreditNote/Delivery/DeliveryLocation/Address/StreetName","descricao":"Linha 1 da morada do local de entrega.","cardinalidade":"1..1"},
{"id":"/CreditNote/Delivery/DeliveryLocation/Address/AdditionalStreetName","descricao":"Linha 2 da morada do local de entrega.","cardinalidade":"0..1"},
{"id":"/CreditNote/Delivery/DeliveryLocation/Address/CityName","descricao":"Cidade do local de entrega","cardinalidade":"1..1"},
{"id":"/CreditNote/Delivery/DeliveryLocation/Address/PostalZone","descricao":"Código postal da morada do local de entrega","cardinalidade":"1..1"},
{"id":"/CreditNote/Delivery/DeliveryLocation/Address/CountrySubentity","descricao":"Região/Província da morada do local de entrega.","cardinalidade":"0..1"},
{"id":"/CreditNote/Delivery/DeliveryLocation/Address/AddressLine/Line","descricao":"Linha de endereço adicional que pode ser usado para fornecer mais detalhes, complementando a linha principal.","cardinalidade":"1..1"},
{"id":"/CreditNote/Delivery/DeliveryLocation/Address/Country/IdentificationCode","descricao":"País do local de entrega, segundo o código ISO 3166-1 alfa-2","cardinalidade":"1..1"},
{"id":"/CreditNote/Delivery/DeliveryParty/PartyName/Name","descricao":"Nome do local de entrega","cardinalidade":"1..1"},
{"id":"/CreditNote/PaymentMeans/PaymentMeansCode","descricao":"Código identificador do método de pagamento,deve mencionar o método de pagamento, segundo o código UNCL4461.","cardinalidade":"1..1"},
{"id":"/CreditNote/PaymentMeans/PaymentDueDate","descricao":"Data de vencimento do documento [AAAA-MM-DD]","cardinalidade":"0..1"},
{"id":"/CreditNote/PaymentMeans/PaymentID","descricao":"Descrição da referência a pagamento do documento por ATM.","cardinalidade":"0..1"},
{"id":"/CreditNote/PaymentMeans/CardAccount/PrimaryAccountNumberID","descricao":"Número da conta principal do cartão utilizado no pagamento, PAN.","cardinalidade":"1..1"},
{"id":"/CreditNote/PaymentMeans/CardAccount/NetworkID","descricao":"Identificador da rede [ex: VISA, MASTER CARD, American Express...]","cardinalidade":"1..1"},
{"id":"/CreditNote/PaymentMeans/CardAccount/HolderName","descricao":"Nome do titular do cartão de pagamento.","cardinalidade":"0..1"},
{"id":"/CreditNote/PaymentMeans/PayeeFinancialAccount/ID","descricao":"Identificador do pagamento, código IBAN.","cardinalidade":"0..1"},
{"id":"/CreditNote/PaymentMeans/PayeeFinancialAccount/Name","descricao":"Identificação da conta, para a qual o pagamento deve ser efectuado.","cardinalidade":"0..1"},
{"id":"/CreditNote/PaymentMeans/PayeeFinancialAccount/FinancialInstitutionBranch/ID","descricao":"Código da instituição bancária. Será considerado o código SWIFT se o atributo schemeID for igual a BIC, segundo a lista de códigos ISO 9362.","cardinalidade":"1..1"},
{"id":"/CreditNote/PaymentMeans/PaymentMandate/ID","descricao":"Identificador exclusivo atribuído pelo Beneficiário para referenciar o mandato de débito direto (Nº Mandato).","cardinalidade":"0..1"},
{"id":"/CreditNote/PaymentMeans/PaymentMandate/PayerFinancialAccount/ID","descricao":"A conta a ser debitada pelo débito direto.","cardinalidade":"1..1"},
{"id":"/CreditNote/PaymentTerms/Note","descricao":"Descritivo das condições de pagamento.","cardinalidade":"0..*"},
{"id":"/CreditNote/AllowanceCharge/ChargeIndicator","descricao":"Indica se o valor é um encargo ou um desconto da linha do documento. Indicador de encargo (true). Indicador de desconto (false).","cardinalidade":"1..1"},
{"id":"/CreditNote/AllowanceCharge/AllowanceChargeReasonCode","descricao":"Código do motivo, que possa levar a que o montante contemplado no desconto/encargo, esteja isento de imposto.","cardinalidade":"0..1"},
{"id":"/CreditNote/AllowanceCharge/AllowanceChargeReason","descricao":"Representação textual do desconto/encargo","cardinalidade":"0..1"},
{"id":"/CreditNote/AllowanceCharge/MultiplierFactorNumeric","descricao":"Fator multiplicador sobre o montante base do desconto/encargo","cardinalidade":"0..1"},
{"id":"/CreditNote/AllowanceCharge/Amount","descricao":"Montante do desconto/encargo, sem impostos.A Moeda, segundo a lista de códigos ISO4217 (https://www.iso.org/iso-4217-currency-codes.html)","cardinalidade":"1..1"},
{"id":"/CreditNote/AllowanceCharge/BaseAmount","descricao":"Montante base do desconto/encargo. A Moeda, segundo a lista de códigos ISO4217 (https://www.iso.org/iso-4217-currency-codes.html)","cardinalidade":"0..1"},
{"id":"/CreditNote/AllowanceCharge/TaxCategory/ID","descricao":"Código de imposto aplicado ao desconto/encargo","cardinalidade":"1..1"},
{"id":"/CreditNote/AllowanceCharge/TaxCategory/Percent","descricao":"Percentagem de imposto aplicada ao desconto/encargo","cardinalidade":"1..1"},
{"id":"/CreditNote/AllowanceCharge/TaxCategory/TaxScheme/ID","descricao":"O valor do ID corresponde à lista de códigos UN/ECE 5153 [Predefinição:VAT]","cardinalidade":"1..1"},
{"id":"/CreditNote/TaxTotal/TaxAmount","descricao":"Total de impostos.A Moeda, segundo a lista de códigos ISO4217 (https://www.iso.org/iso-4217-currency-codes.html)","cardinalidade":"1..1"},
{"id":"/CreditNote/TaxTotal/TaxSubtotal/TaxableAmount","descricao":"Montante base de incidência para a taxa de imposto aplicada no respetivo subtotal.A Moeda, segundo a lista de códigos ISO4217 (https://www.iso.org/iso-4217-currency-codes.html)","cardinalidade":"1..1"},
{"id":"/CreditNote/TaxTotal/TaxSubtotal/TaxAmount","descricao":"Montante calculado do imposto sobre o montante base de incidência respetivo..A Moeda, segundo a lista de códigos ISO4217 (https://www.iso.org/iso-4217-currency-codes.html)","cardinalidade":"1..1"},
{"id":"/CreditNote/TaxTotal/TaxSubtotal/TaxCategory/ID","descricao":"Código de imposto respeitante à taxa aplicada no item da linha do documento, segundo a lista de códigos UN/ECE 5305 (http://www.unece.org/trade/untdid/d07a/tred/tred5305.htm) [Predefinição: S]","cardinalidade":"1..1"},
{"id":"/CreditNote/TaxTotal/TaxSubtotal/TaxCategory/Percent","descricao":"Percentagem de imposto do subtotal","cardinalidade":"1..1"},
{"id":"/CreditNote/TaxTotal/TaxSubtotal/TaxCategory/TaxExemptionReasonCode","descricao":"Código do motivo, que possa levar a que o montante contemplado no subtotal, respetivo, esteja isento de imposto.","cardinalidade":"0..1"},
{"id":"/CreditNote/TaxTotal/TaxSubtotal/TaxCategory/TaxExemptionReason","descricao":"Descrição textual do motivo, que possa levar a que o montante contemplado no subtotal, respetivo, esteja isento de imposto.","cardinalidade":"0..1"},
{"id":"/CreditNote/TaxTotal/TaxSubtotal/TaxCategory/TaxScheme/ID","descricao":"O valor do ID corresponde à lista de códigos UN/ECE 5153 [Predefinição: VAT]","cardinalidade":"1..1"},
{"id":"/CreditNote/LegalMonetaryTotal/LineExtensionAmount","descricao":"Soma dos montantes das linhas do documento (s/imposto). A Moeda, segundo a lista de códigos ISO4217 (https://www.iso.org/iso-4217-currency-codes.html)","cardinalidade":"1..1"},
{"id":"/CreditNote/LegalMonetaryTotal/TaxExclusiveAmount","descricao":"Total do documento (s/imposto).A Moeda, segundo a lista de códigos ISO4217 (https://www.iso.org/iso-4217-currency-codes.html)","cardinalidade":"1..1"},
{"id":"/CreditNote/LegalMonetaryTotal/TaxInclusiveAmount","descricao":"Total do documento (c/imposto). A Moeda, segundo a lista de códigos ISO4217 (https://www.iso.org/iso-4217-currency-codes.html)","cardinalidade":"1..1"},
{"id":"/CreditNote/LegalMonetaryTotal/AllowanceTotalAmount","descricao":"Total de descontos aplicados no documento. A Moeda, segundo a lista de códigos ISO4217 (https://www.iso.org/iso-4217-currency-codes.html)","cardinalidade":"0..1"},
{"id":"/CreditNote/LegalMonetaryTotal/ChargeTotalAmount","descricao":"Total de encargos aplicados no documento. A Moeda, segundo a lista de códigos ISO4217 (https://www.iso.org/iso-4217-currency-codes.html)","cardinalidade":"0..1"},
{"id":"/CreditNote/LegalMonetaryTotal/PrepaidAmount","descricao":"Valor pago à-priori. O documento pode conter a soma de todos os montantes pré-pagos, que devem ser deduzidos do pagamento. A Moeda, segundo a lista de códigos ISO4217 (https://www.iso.org/iso-4217-currency-codes.html)","cardinalidade":"0..1"},
{"id":"/CreditNote/LegalMonetaryTotal/PayableRoundingAmount","descricao":"Montante de arredondamento aplicado ao total do documento c/imposto. A Moeda, segundo a lista de códigos ISO4217 (https://www.iso.org/iso-4217-currency-codes.html)","cardinalidade":"0..1"},
{"id":"/CreditNote/LegalMonetaryTotal/PayableAmount","descricao":"Valor a pagar. A Moeda, segundo a lista de códigos ISO4217 (https://www.iso.org/iso-4217-currency-codes.html)","cardinalidade":"1..1"},
{"id":"/CreditNote/CreditNoteLine/ID","descricao":"Identificador único da linha do documento, atribuído pelo fornecedor","cardinalidade":"1..1"},
{"id":"/CreditNote/CreditNoteLine/Note","descricao":"Texto livre para descrever alguma observação em relação ao item respetivo à linha do documento.","cardinalidade":"0..1"},
{"id":"/CreditNote/CreditNoteLine/CreditedQuantity","descricao":"Quantidade faturada. A propriedade unitCode deverá ser preenchida com o código UNECERec20 de unidade medida. (http://www.unece.org/cefact/recommendations/rec20/Rec20_Rev6e_2009.xls).","cardinalidade":"1..1"},
{"id":"/CreditNote/CreditNoteLine/LineExtensionAmount","descricao":"Montante da linha (s/imposto). O valor deve incluir os respetivos encargos ou descontos aplicados à linha, desprovidos de imposto e outras taxas (que não sejam de IVA). A Moeda, segundo a lista de códigos ISO4217 (https://www.iso.org/iso-4217-currency-codes.html) [EUR]","cardinalidade":"1..1"},
{"id":"/CreditNote/CreditNoteLine/AccountingCost","descricao":"Número do compromisso associado à linha do documento.","cardinalidade":"0..1"},
{"id":"/CreditNote/CreditNoteLine/InvoicePeriod/StartDate","descricao":"A data em que o período começa.[AAAA-MM-DD]","cardinalidade":"0..1"},
{"id":"/CreditNote/CreditNoteLine/InvoicePeriod/EndDate","descricao":"A data em que o período acaba.[AAAA-MM-DD]","cardinalidade":"0..1"},
{"id":"/CreditNote/CreditNoteLine/OrderLineReference/LineID","descricao":"Referência para o item da nota de encomenda do cliente.","cardinalidade":"1..1"},
{"id":"/CreditNote/CreditNoteLine/DocumentReference/ID","descricao":"Identificador para um objeto no qual a linha da fatura é baseada, fornecida pelo fornecedor.","cardinalidade":"1..1"},
{"id":"/CreditNote/CreditNoteLine/AllowanceCharge/ChargeIndicator","descricao":"Indica se o valor é um encargo ou um desconto da linha do documento. Indicador de encargo (true). Indicador de desconto (false).","cardinalidade":"1..1"},
{"id":"/CreditNote/CreditNoteLine/AllowanceCharge/AllowanceChargeReasonCode","descricao":"Código do motivo, que possa levar a que o montante contemplado no desconto/encargo, esteja isento de imposto.","cardinalidade":"0..1"},
{"id":"/CreditNote/CreditNoteLine/AllowanceCharge/AllowanceChargeReason","descricao":"Representação textual da acção da linha do documento.","cardinalidade":"0..1"},
{"id":"/CreditNote/CreditNoteLine/AllowanceCharge/MultiplierFactorNumeric","descricao":"Fator multiplicador sobre o montante base da acção da linha do documento.","cardinalidade":"0..1"},
{"id":"/CreditNote/CreditNoteLine/AllowanceCharge/Amount","descricao":"Montante do encargo/desconto da linha do documento.A Moeda, segundo a lista de códigos ISO4217 (https://www.iso.org/iso-4217-currency-codes.html) [EUR]","cardinalidade":"1..1"},
{"id":"/CreditNote/CreditNoteLine/AllowanceCharge/BaseAmount","descricao":"Montante base da acção da linha do documento.A Moeda, segundo a lista de códigos ISO4217 (https://www.iso.org/iso-4217-currency-codes.html) [EUR]","cardinalidade":"0..1"},
{"id":"/CreditNote/CreditNoteLine/Item/Description","descricao":"Descrição do item da linha do documento.","cardinalidade":"0..*"},
{"id":"/CreditNote/CreditNoteLine/Item/Name","descricao":"Nome do item da linha do documento.","cardinalidade":"1..1"},
{"id":"/CreditNote/CreditNoteLine/Item/BuyersItemIdentification/ID","descricao":"Código de material do cliente.","cardinalidade":"1..1"},
{"id":"/CreditNote/CreditNoteLine/Item/SellersItemIdentification/ID","descricao":"Código de material usado pelo fornecedor para identificar univocamente o item da linha do documento.","cardinalidade":"1..1"},
{"id":"/CreditNote/CreditNoteLine/Item/StandardItemIdentification/ID","descricao":"Identificador do item da linha do documento de acordo com um esquema padrão (GTIN). A propriedade schemeID deve mencionar a norma de códigos EAN .","cardinalidade":"1..1"},
{"id":"/CreditNote/CreditNoteLine/Item/OriginCountry/IdentificationCode","descricao":"País de origem do item, segundo o código ISO 3166-1 alfa-2","cardinalidade":"1..1"},
{"id":"/CreditNote/CreditNoteLine/Item/CommodityClassification/ItemClassificationCode","descricao":"Código da classificação da mercadoria do item da linha do documento empregue na Administração Pública.Se o atributo listID for CPV, será considerado como o código CPV associado ao item da linha do documento.","cardinalidade":"1..1"},
{"id":"/CreditNote/CreditNoteLine/Item/ClassifiedTaxCategory/ID","descricao":"Código de imposto respeitante à taxa aplicada no item da linha do documento, segundo a lista de códigos UN/ECE 5305,[Predefinição: S]","cardinalidade":"1..1"},
{"id":"/CreditNote/CreditNoteLine/Item/ClassifiedTaxCategory/Percent","descricao":"Percentagem de imposto respeitante à taxa aplicada no item da linha do documento","cardinalidade":"1..1"},
{"id":"/CreditNote/CreditNoteLine/Item/ClassifiedTaxCategory/TaxScheme/ID","descricao":"Tipo de imposto do item da linha do documento, segundo a lista de códigos UN/ECE 5153. [Predefinição: VAT]","cardinalidade":"1..1"},
{"id":"/CreditNote/CreditNoteLine/Item/AdditionalItemProperty/Name","descricao":"Tipo da propriedade adicional do item da linha do documento.","cardinalidade":"1..1"},
{"id":"/CreditNote/CreditNoteLine/Item/AdditionalItemProperty/Value","descricao":"Valor da propriedade do item da linha do documento.","cardinalidade":"1..1"},
{"id":"/CreditNote/CreditNoteLine/Price/PriceAmount","descricao":"Montante do item após aplicação do desconto.Estrutura que guarda a informação de preço do item por quantidade base. Este preço, no caso de preenchida a estrtura de desconto sobre o preço, já será o resultante da aplicabilidade do referido desconto. A Moeda, segundo a lista de códigos ISO4217 (https://www.iso.org/iso-4217-currency-codes.html) [EUR]","cardinalidade":"1..1"},
{"id":"/CreditNote/CreditNoteLine/Price/BaseQuantity","descricao":"Número de quantidades que fazem o montante do preço. Por exemplo, se a quantidade faturada for 1000 litros, o preço pode ser 15e por 10 litros. A propriedade unitCode deverá ser preenchida com o código UNECERec20 de unidade medida, ex: KGM (quilograma).","cardinalidade":"0..1"},
{"id":"/CreditNote/CreditNoteLine/Price/AllowanceCharge/ChargeIndicator","descricao":"Indica se o valor é um encargo (true) ou um desconto (false) do preço do item da linha do documento.","cardinalidade":"1..1"},
{"id":"/CreditNote/CreditNoteLine/Price/AllowanceCharge/Amount","descricao":"Montante do desconto ou encardo sobre o preço do item da linha do documento.A Moeda, segundo a lista de códigos ISO4217 (https://www.iso.org/iso-4217-currency-codes.html) [EUR]","cardinalidade":"1..1"},
{"id":"/CreditNote/CreditNoteLine/Price/AllowanceCharge/BaseAmount","descricao":"Montante base onde incidirá o desconto ou encargo.A Moeda, segundo a lista de códigos ISO4217 (https://www.iso.org/iso-4217-currency-codes.html) [EUR]","cardinalidade":"0..1"}
]
```

### Fonte fm-dart: Modelos Dart da aplicação FM (modelo de aplicação (classes))

Papel: entidades da aplicação FM: cliente, vendedor, empresa, artigo, entrega, linha de entrega, zona, configuração

Grupos (14):
```json
[
{"id":"Article","nome":"Article","descricao":"Classe Article","elementos":["Article.internalId","Article.registrationDate","Article.code","Article.articleCode","Article.barCode","Article.description","Article.reference","Article.artForm","Article.supplier","Article.unit","Article.saleIva","Article.ecoTaxa","Article.costPrice","Article.costDiscount","Article.salePrice","Article.ppPrice","Article.isCar","Article.observations","Article.discount2","Article.weight","Article.familyCode","Article.costPriceNoIva","Article.costPriceWithIva","Article.supplierCode","Article.familyDescription","Article.costPriceNoIva2","Article.costPriceWithIva2","Article.service","Article.carRegistration","Article.stockQuantity","Article.stockOutQuantity","Article.carQuantityTotal","Article.carQuantityNormal","Article.carQuantityOut"]},
{"id":"BaseEntity","nome":"BaseEntity","descricao":"Classe BaseEntity","elementos":["BaseEntity.fields"]},
{"id":"Client","nome":"Client","descricao":"Classe Client","elementos":["Client.internalId","Client.registrationDate","Client.code","Client.name","Client.address","Client.city","Client.zipCode","Client.zipCodeLoc","Client.nif","Client.phoneNumber","Client.zone","Client.chargeLocation","Client.email","Client.notes","Client.fixePhoneNumber","Client.sellerCode","Client.orderNumber","Client.dateOfBirth","Client.citizenCard","Client.citizenCardExpirationDate","Client.name2","Client.address2","Client.city2","Client.zipCode2","Client.zipCodeLoc2","Client.citizenCard2","Client.citizenCardExpirationDate2","Client.nif2","Client.fixePhoneNumber2","Client.receivingDay","Client.isNew"]},
{"id":"Company","nome":"Company","descricao":"Classe Company","elementos":["Company.prop","Company.value"]},
{"id":"Config","nome":"Config","descricao":"Classe Config","elementos":["Config.prop","Config.value"]},
{"id":"Delivery","nome":"Delivery","descricao":"Classe Delivery","elementos":["Delivery.internalId","Delivery.registrationDate","Delivery.clientBuyer","Delivery.clientDelivery","Delivery.articles","Delivery.deliveryNumber","Delivery.invoiceNumber","Delivery.deliveryGuideNumber","Delivery.contractNumber","Delivery.documentSaleNumber","Delivery.documentType","Delivery.status","Delivery.date"]},
{"id":"DeliveryConfirmation","nome":"DeliveryConfirmation","descricao":"Classe DeliveryConfirmation","elementos":["DeliveryConfirmation.internalId","DeliveryConfirmation.document","DeliveryConfirmation.contract","DeliveryConfirmation.delivery","DeliveryConfirmation.originalPrice","DeliveryConfirmation.signal","DeliveryConfirmation.installment"]},
{"id":"DeliveryItem","nome":"DeliveryItem","descricao":"Classe DeliveryItem","elementos":["DeliveryItem.internalId","DeliveryItem.article","DeliveryItem.seriesNumber","DeliveryItem.quantity","DeliveryItem.customPrice","DeliveryItem.customDiscount"]},
{"id":"Status","nome":"Status","descricao":"Enumerado Status: FATURADO, ENTREGUE, ENVIADO, PENDENTE, POR_FATURAR, ERRO"},
{"id":"FileInfo","nome":"FileInfo","descricao":"Classe FileInfo","elementos":["FileInfo.name","FileInfo.size","FileInfo.lastModified","FileInfo.nCli","FileInfo.nArt","FileInfo.nDlv","FileInfo.nItem","FileInfo.file"]},
{"id":"HeaderInfo","nome":"HeaderInfo","descricao":"Classe HeaderInfo","elementos":["HeaderInfo.nCli","HeaderInfo.nArt","HeaderInfo.nArtVeic","HeaderInfo.nZone"]},
{"id":"Seller","nome":"Seller","descricao":"Classe Seller","elementos":["Seller.internalId","Seller.registrationDate","Seller.code","Seller.name","Seller.address","Seller.city","Seller.zipCode","Seller.zipCodeLoc","Seller.nif","Seller.seriesNumber","Seller.seriesNumberStartingDate","Seller.commissionOfSaleOfProduct","Seller.commissionOfSaleOfInstallment","Seller.commissionOfCharge","Seller.phoneNumber","Seller.carRegistration","Seller.car","Seller.carModel","Seller.transportGuideNumber","Seller.transportGuideExtraNumber","Seller.familyCodeExtra","Seller.processReceiptsPermissions","Seller.senderNif"]},
{"id":"SellerProperty","nome":"SellerProperty","descricao":"Classe SellerProperty","elementos":["SellerProperty.propertyName","SellerProperty.propertyValue"]},
{"id":"Zone","nome":"Zone","descricao":"Classe Zone","elementos":["Zone.internalId","Zone.code","Zone.name"]}
]
```

Elementos (136):
```json
[
{"id":"Article.internalId","nome":"internalId","tipo":"texto","tipoOrigem":"String","cardinalidade":"1..1","grupo":"Article"},
{"id":"Article.registrationDate","nome":"registrationDate","tipo":"data","tipoOrigem":"DateTime","cardinalidade":"1..1","grupo":"Article"},
{"id":"Article.code","nome":"code","tipo":"texto","tipoOrigem":"String","cardinalidade":"1..1","grupo":"Article"},
{"id":"Article.articleCode","nome":"articleCode","tipo":"texto","tipoOrigem":"String","cardinalidade":"1..1","grupo":"Article"},
{"id":"Article.barCode","nome":"barCode","tipo":"texto","tipoOrigem":"String","cardinalidade":"1..1","grupo":"Article"},
{"id":"Article.description","nome":"description","tipo":"texto","tipoOrigem":"String","cardinalidade":"1..1","grupo":"Article"},
{"id":"Article.reference","nome":"reference","tipo":"texto","tipoOrigem":"String","cardinalidade":"1..1","grupo":"Article"},
{"id":"Article.artForm","nome":"artForm","tipo":"texto","tipoOrigem":"String","cardinalidade":"1..1","grupo":"Article"},
{"id":"Article.supplier","nome":"supplier","tipo":"texto","tipoOrigem":"String","cardinalidade":"1..1","grupo":"Article"},
{"id":"Article.unit","nome":"unit","tipo":"texto","tipoOrigem":"String","cardinalidade":"1..1","grupo":"Article"},
{"id":"Article.saleIva","nome":"saleIva","descricao":"23%","tipo":"decimal","tipoOrigem":"double","cardinalidade":"1..1","grupo":"Article"},
{"id":"Article.ecoTaxa","nome":"ecoTaxa","tipo":"decimal","tipoOrigem":"double","cardinalidade":"1..1","grupo":"Article"},
{"id":"Article.costPrice","nome":"costPrice","tipo":"decimal","tipoOrigem":"double","cardinalidade":"1..1","grupo":"Article"},
{"id":"Article.costDiscount","nome":"costDiscount","tipo":"decimal","tipoOrigem":"double","cardinalidade":"1..1","grupo":"Article"},
{"id":"Article.salePrice","nome":"salePrice","tipo":"decimal","tipoOrigem":"double","cardinalidade":"1..1","grupo":"Article"},
{"id":"Article.ppPrice","nome":"ppPrice","tipo":"decimal","tipoOrigem":"double","cardinalidade":"1..1","grupo":"Article"},
{"id":"Article.isCar","nome":"isCar","tipo":"booleano","tipoOrigem":"bool","grupo":"Article"},
{"id":"Article.observations","nome":"observations","tipo":"texto","tipoOrigem":"String","cardinalidade":"1..1","grupo":"Article"},
{"id":"Article.discount2","nome":"discount2","tipo":"decimal","tipoOrigem":"double","grupo":"Article"},
{"id":"Article.weight","nome":"weight","tipo":"decimal","tipoOrigem":"double","grupo":"Article"},
{"id":"Article.familyCode","nome":"familyCode","tipo":"texto","tipoOrigem":"String","grupo":"Article"},
{"id":"Article.costPriceNoIva","nome":"costPriceNoIva","tipo":"decimal","tipoOrigem":"double","grupo":"Article"},
{"id":"Article.costPriceWithIva","nome":"costPriceWithIva","tipo":"decimal","tipoOrigem":"double","grupo":"Article"},
{"id":"Article.supplierCode","nome":"supplierCode","tipo":"texto","tipoOrigem":"String","grupo":"Article"},
{"id":"Article.familyDescription","nome":"familyDescription","tipo":"texto","tipoOrigem":"String","grupo":"Article"},
{"id":"Article.costPriceNoIva2","nome":"costPriceNoIva2","tipo":"decimal","tipoOrigem":"double","grupo":"Article"},
{"id":"Article.costPriceWithIva2","nome":"costPriceWithIva2","tipo":"decimal","tipoOrigem":"double","grupo":"Article"},
{"id":"Article.service","nome":"service","tipo":"texto","tipoOrigem":"String","grupo":"Article"},
{"id":"Article.carRegistration","nome":"carRegistration","tipo":"texto","tipoOrigem":"String","grupo":"Article"},
{"id":"Article.stockQuantity","nome":"stockQuantity","tipo":"inteiro","tipoOrigem":"int","cardinalidade":"1..1","grupo":"Article"},
{"id":"Article.stockOutQuantity","nome":"stockOutQuantity","tipo":"inteiro","tipoOrigem":"int","grupo":"Article"},
{"id":"Article.carQuantityTotal","nome":"carQuantityTotal","tipo":"inteiro","tipoOrigem":"int","cardinalidade":"1..1","grupo":"Article"},
{"id":"Article.carQuantityNormal","nome":"carQuantityNormal","tipo":"inteiro","tipoOrigem":"int","grupo":"Article"},
{"id":"Article.carQuantityOut","nome":"carQuantityOut","tipo":"inteiro","tipoOrigem":"int","grupo":"Article"},
{"id":"BaseEntity.fields","nome":"fields","tipoOrigem":"Map<String, dynamic> get","grupo":"BaseEntity"},
{"id":"Client.internalId","nome":"internalId","tipo":"texto","tipoOrigem":"String","cardinalidade":"1..1","grupo":"Client"},
{"id":"Client.registrationDate","nome":"registrationDate","tipo":"data","tipoOrigem":"DateTime","cardinalidade":"1..1","grupo":"Client"},
{"id":"Client.code","nome":"code","tipo":"texto","tipoOrigem":"String","cardinalidade":"1..1","grupo":"Client"},
{"id":"Client.name","nome":"name","tipo":"texto","tipoOrigem":"String","cardinalidade":"1..1","grupo":"Client"},
{"id":"Client.address","nome":"address","tipo":"texto","tipoOrigem":"String","cardinalidade":"1..1","grupo":"Client"},
{"id":"Client.city","nome":"city","tipo":"texto","tipoOrigem":"String","cardinalidade":"1..1","grupo":"Client"},
{"id":"Client.zipCode","nome":"zipCode","tipo":"texto","tipoOrigem":"String","cardinalidade":"1..1","grupo":"Client"},
{"id":"Client.zipCodeLoc","nome":"zipCodeLoc","tipo":"texto","tipoOrigem":"String","cardinalidade":"1..1","grupo":"Client"},
{"id":"Client.nif","nome":"nif","tipo":"texto","tipoOrigem":"String","cardinalidade":"1..1","grupo":"Client"},
{"id":"Client.phoneNumber","nome":"phoneNumber","tipo":"texto","tipoOrigem":"String","cardinalidade":"1..1","grupo":"Client"},
{"id":"Client.zone","nome":"zone","tipo":"texto","tipoOrigem":"String","cardinalidade":"1..1","grupo":"Client"},
{"id":"Client.chargeLocation","nome":"chargeLocation","tipo":"texto","tipoOrigem":"String","cardinalidade":"1..1","grupo":"Client"},
{"id":"Client.email","nome":"email","tipo":"texto","tipoOrigem":"String","cardinalidade":"1..1","grupo":"Client"},
{"id":"Client.notes","nome":"notes","tipo":"texto","tipoOrigem":"String","grupo":"Client"},
{"id":"Client.fixePhoneNumber","nome":"fixePhoneNumber","tipo":"texto","tipoOrigem":"String","grupo":"Client"},
{"id":"Client.sellerCode","nome":"sellerCode","tipo":"texto","tipoOrigem":"String","grupo":"Client"},
{"id":"Client.orderNumber","nome":"orderNumber","tipo":"texto","tipoOrigem":"String","grupo":"Client"},
{"id":"Client.dateOfBirth","nome":"dateOfBirth","tipo":"data","tipoOrigem":"DateTime","grupo":"Client"},
{"id":"Client.citizenCard","nome":"citizenCard","tipo":"texto","tipoOrigem":"String","grupo":"Client"},
{"id":"Client.citizenCardExpirationDate","nome":"citizenCardExpirationDate","tipo":"data","tipoOrigem":"DateTime","grupo":"Client"},
{"id":"Client.name2","nome":"name2","tipo":"texto","tipoOrigem":"String","grupo":"Client"},
{"id":"Client.address2","nome":"address2","tipo":"texto","tipoOrigem":"String","grupo":"Client"},
{"id":"Client.city2","nome":"city2","tipo":"texto","tipoOrigem":"String","grupo":"Client"},
{"id":"Client.zipCode2","nome":"zipCode2","tipo":"texto","tipoOrigem":"String","grupo":"Client"},
{"id":"Client.zipCodeLoc2","nome":"zipCodeLoc2","tipo":"texto","tipoOrigem":"String","grupo":"Client"},
{"id":"Client.citizenCard2","nome":"citizenCard2","tipo":"texto","tipoOrigem":"String","grupo":"Client"},
{"id":"Client.citizenCardExpirationDate2","nome":"citizenCardExpirationDate2","tipo":"data","tipoOrigem":"DateTime","grupo":"Client"},
{"id":"Client.nif2","nome":"nif2","tipo":"texto","tipoOrigem":"String","grupo":"Client"},
{"id":"Client.fixePhoneNumber2","nome":"fixePhoneNumber2","tipo":"texto","tipoOrigem":"String","grupo":"Client"},
{"id":"Client.receivingDay","nome":"receivingDay","tipo":"texto","tipoOrigem":"String","grupo":"Client"},
{"id":"Client.isNew","nome":"isNew","tipo":"booleano","tipoOrigem":"bool","grupo":"Client"},
{"id":"Company.prop","nome":"prop","tipo":"texto","tipoOrigem":"String","cardinalidade":"1..1","grupo":"Company"},
{"id":"Company.value","nome":"value","tipo":"texto","tipoOrigem":"String","cardinalidade":"1..1","grupo":"Company"},
{"id":"Config.prop","nome":"prop","tipo":"texto","tipoOrigem":"String","cardinalidade":"1..1","grupo":"Config"},
{"id":"Config.value","nome":"value","tipo":"texto","tipoOrigem":"String","cardinalidade":"1..1","grupo":"Config"},
{"id":"Delivery.internalId","nome":"internalId","tipo":"texto","tipoOrigem":"String","cardinalidade":"1..1","grupo":"Delivery"},
{"id":"Delivery.registrationDate","nome":"registrationDate","tipo":"data","tipoOrigem":"DateTime","cardinalidade":"1..1","grupo":"Delivery"},
{"id":"Delivery.clientBuyer","nome":"clientBuyer","tipoOrigem":"Client","cardinalidade":"1..1","grupo":"Delivery","notas":"referência à classe Client"},
{"id":"Delivery.clientDelivery","nome":"clientDelivery","tipoOrigem":"Client","cardinalidade":"1..1","grupo":"Delivery","notas":"referência à classe Client"},
{"id":"Delivery.articles","nome":"articles","tipoOrigem":"List<DeliveryItem>","cardinalidade":"0..*","grupo":"Delivery","notas":"referência à classe DeliveryItem (lista)"},
{"id":"Delivery.deliveryNumber","nome":"deliveryNumber","tipo":"texto","tipoOrigem":"String","cardinalidade":"1..1","grupo":"Delivery"},
{"id":"Delivery.invoiceNumber","nome":"invoiceNumber","tipo":"texto","tipoOrigem":"String","cardinalidade":"1..1","grupo":"Delivery"},
{"id":"Delivery.deliveryGuideNumber","nome":"deliveryGuideNumber","tipo":"texto","tipoOrigem":"String","cardinalidade":"1..1","grupo":"Delivery"},
{"id":"Delivery.contractNumber","nome":"contractNumber","tipo":"texto","tipoOrigem":"String","cardinalidade":"1..1","grupo":"Delivery"},
{"id":"Delivery.documentSaleNumber","nome":"documentSaleNumber","tipo":"texto","tipoOrigem":"String","cardinalidade":"1..1","grupo":"Delivery"},
{"id":"Delivery.documentType","nome":"documentType","descricao":"New field added here","tipo":"texto","tipoOrigem":"String","cardinalidade":"1..1","grupo":"Delivery"},
{"id":"Delivery.status","nome":"status","descricao":"New field added here","tipo":"texto","tipoOrigem":"String","cardinalidade":"1..1","grupo":"Delivery"},
{"id":"Delivery.date","nome":"date","tipo":"data","tipoOrigem":"DateTime","cardinalidade":"1..1","grupo":"Delivery"},
{"id":"DeliveryConfirmation.internalId","nome":"internalId","tipo":"texto","tipoOrigem":"String","cardinalidade":"1..1","grupo":"DeliveryConfirmation"},
{"id":"DeliveryConfirmation.document","nome":"document","tipo":"booleano","tipoOrigem":"bool","cardinalidade":"1..1","grupo":"DeliveryConfirmation"},
{"id":"DeliveryConfirmation.contract","nome":"contract","tipo":"booleano","tipoOrigem":"bool","cardinalidade":"1..1","grupo":"DeliveryConfirmation"},
{"id":"DeliveryConfirmation.delivery","nome":"delivery","tipo":"booleano","tipoOrigem":"bool","cardinalidade":"1..1","grupo":"DeliveryConfirmation"},
{"id":"DeliveryConfirmation.originalPrice","nome":"originalPrice","tipo":"decimal","tipoOrigem":"double","cardinalidade":"1..1","grupo":"DeliveryConfirmation"},
{"id":"DeliveryConfirmation.signal","nome":"signal","tipo":"decimal","tipoOrigem":"double","cardinalidade":"1..1","grupo":"DeliveryConfirmation"},
{"id":"DeliveryConfirmation.installment","nome":"installment","tipo":"decimal","tipoOrigem":"double","cardinalidade":"1..1","grupo":"DeliveryConfirmation"},
{"id":"DeliveryItem.internalId","nome":"internalId","tipo":"texto","tipoOrigem":"String","cardinalidade":"1..1","grupo":"DeliveryItem"},
{"id":"DeliveryItem.article","nome":"article","descricao":"The article being delivered","tipoOrigem":"Article","cardinalidade":"1..1","grupo":"DeliveryItem","notas":"referência à classe Article"},
{"id":"DeliveryItem.seriesNumber","nome":"seriesNumber","tipo":"texto","tipoOrigem":"String","cardinalidade":"1..1","grupo":"DeliveryItem"},
{"id":"DeliveryItem.quantity","nome":"quantity","descricao":"The quantity of this article in the delivery","tipo":"inteiro","tipoOrigem":"int","cardinalidade":"1..1","grupo":"DeliveryItem"},
{"id":"DeliveryItem.customPrice","nome":"customPrice","tipo":"decimal","tipoOrigem":"double","cardinalidade":"1..1","grupo":"DeliveryItem"},
{"id":"DeliveryItem.customDiscount","nome":"customDiscount","tipo":"decimal","tipoOrigem":"double","cardinalidade":"1..1","grupo":"DeliveryItem"},
{"id":"FileInfo.name","nome":"name","tipo":"texto","tipoOrigem":"String","cardinalidade":"1..1","grupo":"FileInfo"},
{"id":"FileInfo.size","nome":"size","tipo":"decimal","tipoOrigem":"double","cardinalidade":"1..1","grupo":"FileInfo"},
{"id":"FileInfo.lastModified","nome":"lastModified","tipo":"texto","tipoOrigem":"String","cardinalidade":"1..1","grupo":"FileInfo"},
{"id":"FileInfo.nCli","nome":"nCli","tipo":"inteiro","tipoOrigem":"int","cardinalidade":"1..1","grupo":"FileInfo"},
{"id":"FileInfo.nArt","nome":"nArt","tipo":"inteiro","tipoOrigem":"int","cardinalidade":"1..1","grupo":"FileInfo"},
{"id":"FileInfo.nDlv","nome":"nDlv","tipo":"inteiro","tipoOrigem":"int","cardinalidade":"1..1","grupo":"FileInfo"},
{"id":"FileInfo.nItem","nome":"nItem","tipo":"inteiro","tipoOrigem":"int","cardinalidade":"1..1","grupo":"FileInfo"},
{"id":"FileInfo.file","nome":"file","tipoOrigem":"File","cardinalidade":"1..1","grupo":"FileInfo"},
{"id":"HeaderInfo.nCli","nome":"nCli","tipo":"texto","tipoOrigem":"String","cardinalidade":"1..1","grupo":"HeaderInfo"},
{"id":"HeaderInfo.nArt","nome":"nArt","tipo":"texto","tipoOrigem":"String","grupo":"HeaderInfo"},
{"id":"HeaderInfo.nArtVeic","nome":"nArtVeic","tipo":"texto","tipoOrigem":"String","grupo":"HeaderInfo"},
{"id":"HeaderInfo.nZone","nome":"nZone","tipo":"texto","tipoOrigem":"String","grupo":"HeaderInfo"},
{"id":"Seller.internalId","nome":"internalId","tipo":"texto","tipoOrigem":"String","cardinalidade":"1..1","grupo":"Seller"},
{"id":"Seller.registrationDate","nome":"registrationDate","tipo":"data","tipoOrigem":"DateTime","cardinalidade":"1..1","grupo":"Seller"},
{"id":"Seller.code","nome":"code","tipo":"texto","tipoOrigem":"String","cardinalidade":"1..1","grupo":"Seller"},
{"id":"Seller.name","nome":"name","tipo":"texto","tipoOrigem":"String","cardinalidade":"1..1","grupo":"Seller"},
{"id":"Seller.address","nome":"address","tipo":"texto","tipoOrigem":"String","cardinalidade":"1..1","grupo":"Seller"},
{"id":"Seller.city","nome":"city","tipo":"texto","tipoOrigem":"String","cardinalidade":"1..1","grupo":"Seller"},
{"id":"Seller.zipCode","nome":"zipCode","tipo":"texto","tipoOrigem":"String","cardinalidade":"1..1","grupo":"Seller"},
{"id":"Seller.zipCodeLoc","nome":"zipCodeLoc","tipo":"texto","tipoOrigem":"String","cardinalidade":"1..1","grupo":"Seller"},
{"id":"Seller.nif","nome":"nif","tipo":"texto","tipoOrigem":"String","cardinalidade":"1..1","grupo":"Seller"},
{"id":"Seller.seriesNumber","nome":"seriesNumber","tipo":"texto","tipoOrigem":"String","cardinalidade":"1..1","grupo":"Seller"},
{"id":"Seller.seriesNumberStartingDate","nome":"seriesNumberStartingDate","tipo":"data","tipoOrigem":"DateTime","cardinalidade":"1..1","grupo":"Seller"},
{"id":"Seller.commissionOfSaleOfProduct","nome":"commissionOfSaleOfProduct","tipo":"decimal","tipoOrigem":"double","cardinalidade":"1..1","grupo":"Seller"},
{"id":"Seller.commissionOfSaleOfInstallment","nome":"commissionOfSaleOfInstallment","tipo":"decimal","tipoOrigem":"double","cardinalidade":"1..1","grupo":"Seller"},
{"id":"Seller.commissionOfCharge","nome":"commissionOfCharge","tipo":"decimal","tipoOrigem":"double","cardinalidade":"1..1","grupo":"Seller"},
{"id":"Seller.phoneNumber","nome":"phoneNumber","tipo":"texto","tipoOrigem":"String","cardinalidade":"1..1","grupo":"Seller"},
{"id":"Seller.carRegistration","nome":"carRegistration","tipo":"texto","tipoOrigem":"String","cardinalidade":"1..1","grupo":"Seller"},
{"id":"Seller.car","nome":"car","tipo":"texto","tipoOrigem":"String","cardinalidade":"1..1","grupo":"Seller"},
{"id":"Seller.carModel","nome":"carModel","tipo":"texto","tipoOrigem":"String","cardinalidade":"1..1","grupo":"Seller"},
{"id":"Seller.transportGuideNumber","nome":"transportGuideNumber","tipo":"inteiro","tipoOrigem":"int","cardinalidade":"1..1","grupo":"Seller"},
{"id":"Seller.transportGuideExtraNumber","nome":"transportGuideExtraNumber","tipo":"inteiro","tipoOrigem":"int","cardinalidade":"1..1","grupo":"Seller"},
{"id":"Seller.familyCodeExtra","nome":"familyCodeExtra","tipo":"texto","tipoOrigem":"String","cardinalidade":"1..1","grupo":"Seller"},
{"id":"Seller.processReceiptsPermissions","nome":"processReceiptsPermissions","tipo":"booleano","tipoOrigem":"bool","cardinalidade":"1..1","grupo":"Seller"},
{"id":"Seller.senderNif","nome":"senderNif","tipo":"texto","tipoOrigem":"String","cardinalidade":"1..1","grupo":"Seller"},
{"id":"SellerProperty.propertyName","nome":"propertyName","tipo":"texto","tipoOrigem":"String","grupo":"SellerProperty"},
{"id":"SellerProperty.propertyValue","nome":"propertyValue","tipo":"texto","tipoOrigem":"String","grupo":"SellerProperty"},
{"id":"Zone.internalId","nome":"internalId","tipo":"texto","tipoOrigem":"String","cardinalidade":"1..1","grupo":"Zone"},
{"id":"Zone.code","nome":"code","tipo":"texto","tipoOrigem":"String","cardinalidade":"1..1","grupo":"Zone"},
{"id":"Zone.name","nome":"name","tipo":"texto","tipoOrigem":"String","cardinalidade":"1..1","grupo":"Zone"}
]
```

Regras (1):
```json
[
{"id":"Status-valores","texto":"Os valores de Status são FATURADO, ENTREGUE, ENVIADO, PENDENTE, POR_FATURAR, ERRO.","categoria":"valores","natureza":"RP","contexto":"Status"}
]
```

### Fonte fm-registos: Desenho dos registos de exportação FM (formato de ficheiro (registos de largura fixa))

Papel: desenho dos registos de exportação FM (VDM, CLI, YCL, STK, AUX, PRV): campos, comprimentos e tipos

Grupos (6):
```json
[
{"id":"VDM","nome":"Vendedores e Numerações","nomeOrigem":"VDM","descricao":"Registo VDM: Vendedores e Numerações","elementos":["VDM.Codigo Vendedor","VDM.Nome Vendedor","VDM.Morada Vendedor","VDM.Localidade Vendedor","VDM.Codigo Postal vendedor","VDM.Telfone Vendedor","VDM.Telemovel Vendedor","VDM.NIF Vendedor","VDM.Nº Ultimo Cliente","VDM.Serie Numerações","VDM.Data Inicio Serie","VDM.Comissao Venda Pronto","VDM.Comissao Venda Prestacao","VDM.Comissao Cobranca","VDM.Matricula","VDM.Veiculo","VDM.Modelo","VDM.Nº Ult. Encomenda","VDM.Nº ult. Fatura","VDM.Nº Ult. Fatura Recibo","VDM.Nº Ult. Nota Credito","VDM.Nº Ult. Alteração enc.","VDM.Nº Ult Recebimento","VDM.Prefixo ATCUD","VDM.Data ULt Enomenda","VDM.Data Ult. Fatura","VDM.Data Ult. Fatura Recibo","VDM.Data Ult. Nota Credito","VDM.Data Ult Alteração  Encomenda","VDM.Data Ult . Recebimento","VDM.Numero Guia Transporte","VDM.Numero Guia Transporte Extra","VDM.Codigo Familia Extra","VDM.Trata Recebimentos","VDM.Num Ult. Recibo","VDM.Data Ult Recibo","VDM.Numero Digitos Serie","VDM.Prefixo ATCUD Fatura","VDM.Prefixo ATCUD Fatura/ Recibo","VDM.Prefixo ATCUD Nota Credito","VDM.Prefixo ATCUD Encomenda","VDM.Prefixo ATCUD Recibo","VDM.Contribuinte do Emissor","VDM.Num Ult Entrada em CC","VDM.Data Ult. Entrada CC"]},
{"id":"CLI","nome":"Clientes","nomeOrigem":"CLI","descricao":"Registo CLI: Clientes","elementos":["CLI.Codigo Cliente","CLI.Nome Cliente","CLI.Morada Cliente","CLI.Localidade Cliente","CLI.Codigo Postal cliente","CLI.Zona","CLI.Telefone Cliente","CLI.Telemovel Cliente","CLI.Data Abertura Ficha","CLI.Contribuinte Cliente","CLI.Codigo Vendedor","CLI.Numero Ordem","CLI.Email Cliente","CLI.Data Nascimento Cliente","CLI.Local Cobrança","CLI.Nome 2 Titular","CLI.Morada 2 Titular","CLI.Localidade 2 Titular","CLI.Cod Postal 2 Titular","CLI.Nº CC 2 Titular","CLI.Nº CC Cliente","CLI.Data Validade CC","CLI.Data Validade CC 2 Titular","CLI.Telefone 2 Titular","CLI.Contribuinte 2 Titular","CLI.Dia Recebimento"]},
{"id":"YCL","nome":"Clientes","nomeOrigem":"YCL","descricao":"Registo YCL: Clientes","elementos":["YCL.Codigo Cliente","YCL.Saldo","YCL.Valor Total Vendas","YCL.Valor Saldo Inicial","YCL.Valor Pago Saldo Inicial","YCL.Data Saldo Inicial"]},
{"id":"STK","nome":"Stocks","nomeOrigem":"STK","descricao":"Registo STK: Stocks","elementos":["STK.Codigo Artigo","STK.Codigo Axiliar","STK.Codigp EAN","STK.Descricao","STK.Referencia","STK.Unidade Medida","STK.Data Criação ficha","STK.Preço Venda com Iva","STK.% Desconto1","STK.% Desconto2","STK.Taxa de Iva","STK.Quantidade em stock","STK.Quantidade em stock Out","STK.Peso","STK.Preço Venda 1 sem Iva","STK.Codigo Familia","STK.Preço Custo sem Iva","STK.Preço Custo com Iva","STK.Codigo Fornecedor","STK.Nome Fornecedor","STK.Descricção Familia","STK.Preço Venda 2 com IVA","STK.Preço Venda 2 sem IVA","STK.Serviço","STK.Exporta OBS"]},
{"id":"AUX","nome":"Auxiliar","nomeOrigem":"AUX","descricao":"Registo AUX: Auxiliar","elementos":["AUX.ID","AUX.Texto"]},
{"id":"PRV","nome":"Produtos no veiculo","nomeOrigem":"PRV","descricao":"Registo PRV: Produtos no veiculo","elementos":["PRV.Matricula","PRV.Codigo Artigo","PRV.Quantidade Total","PRV.Quantidade Normal","PRV.Quantidade Fora"]}
]
```

Elementos (109):
```json
[
{"id":"VDM.Codigo Vendedor","descricao":"Codigo Vendedor","tipo":"inteiro","tipoOrigem":"N","grupo":"VDM","notas":"comprimento 10; ficheiro VDM; OK"},
{"id":"VDM.Nome Vendedor","descricao":"Nome Vendedor","tipo":"texto","tipoOrigem":"C","grupo":"VDM","notas":"comprimento 35; ficheiro VDM; OK"},
{"id":"VDM.Morada Vendedor","descricao":"Morada Vendedor","tipo":"texto","tipoOrigem":"C","grupo":"VDM","notas":"comprimento 35; ficheiro VDM; OK"},
{"id":"VDM.Localidade Vendedor","descricao":"Localidade Vendedor","tipo":"texto","tipoOrigem":"C","grupo":"VDM","notas":"comprimento 35; ficheiro VDM; OK"},
{"id":"VDM.Codigo Postal vendedor","descricao":"Codigo Postal vendedor","tipo":"texto","tipoOrigem":"C","grupo":"VDM","notas":"comprimento 35; ficheiro VDM; OK"},
{"id":"VDM.Telfone Vendedor","descricao":"Telfone Vendedor","tipo":"texto","tipoOrigem":"C","grupo":"VDM","notas":"comprimento 15; ficheiro VDM; OK"},
{"id":"VDM.Telemovel Vendedor","descricao":"Telemovel Vendedor","tipo":"texto","tipoOrigem":"C","grupo":"VDM","notas":"comprimento 15; ficheiro VDM; OK"},
{"id":"VDM.NIF Vendedor","descricao":"NIF Vendedor","tipo":"texto","tipoOrigem":"C","grupo":"VDM","notas":"comprimento 15; ficheiro VDM; OK"},
{"id":"VDM.Nº Ultimo Cliente","descricao":"Nº Ultimo Cliente","tipo":"inteiro","tipoOrigem":"N(10)","grupo":"VDM","notas":"comprimento 10; ficheiro VDM; OK"},
{"id":"VDM.Serie Numerações","descricao":"Serie Numerações","tipo":"texto","tipoOrigem":"C","grupo":"VDM","notas":"comprimento 3; ficheiro VDM"},
{"id":"VDM.Data Inicio Serie","descricao":"Data Inicio Serie","tipo":"data","tipoOrigem":"D","grupo":"VDM","notas":"comprimento 10; ficheiro VDM"},
{"id":"VDM.Comissao Venda Pronto","descricao":"Comissao Venda Pronto","tipo":"decimal","tipoOrigem":"N(2.2)","grupo":"VDM","notas":"comprimento 6; ficheiro VDM"},
{"id":"VDM.Comissao Venda Prestacao","descricao":"Comissao Venda Prestacao","tipo":"decimal","tipoOrigem":"N(2.2)","grupo":"VDM","notas":"comprimento 6; ficheiro VDM"},
{"id":"VDM.Comissao Cobranca","descricao":"Comissao Cobranca","tipo":"decimal","tipoOrigem":"N(2.2)","grupo":"VDM","notas":"comprimento 6; ficheiro VDM"},
{"id":"VDM.Matricula","descricao":"Matricula","tipo":"texto","tipoOrigem":"C","grupo":"VDM","notas":"comprimento 15; ficheiro VDM; OK"},
{"id":"VDM.Veiculo","descricao":"Veiculo","tipo":"texto","tipoOrigem":"C","grupo":"VDM","notas":"comprimento 25; ficheiro VDM; OK"},
{"id":"VDM.Modelo","descricao":"Modelo","tipo":"texto","tipoOrigem":"C","grupo":"VDM","notas":"comprimento 20; ficheiro VDM; OK"},
{"id":"VDM.Nº Ult. Encomenda","descricao":"Nº Ult. Encomenda","tipo":"inteiro","tipoOrigem":"N(10)","grupo":"VDM","notas":"comprimento 10; ficheiro NRD; OK"},
{"id":"VDM.Nº ult. Fatura","descricao":"Nº ult. Fatura","tipo":"inteiro","tipoOrigem":"N(10)","grupo":"VDM","notas":"comprimento 10; ficheiro NRD; OK"},
{"id":"VDM.Nº Ult. Fatura Recibo","descricao":"Nº Ult. Fatura Recibo","tipo":"inteiro","tipoOrigem":"N(10)","grupo":"VDM","notas":"comprimento 10; ficheiro NRD; OK"},
{"id":"VDM.Nº Ult. Nota Credito","descricao":"Nº Ult. Nota Credito","tipo":"inteiro","tipoOrigem":"N(10)","grupo":"VDM","notas":"comprimento 10; ficheiro NRD; OK"},
{"id":"VDM.Nº Ult. Alteração enc.","descricao":"Nº Ult. Alteração enc.","tipo":"inteiro","tipoOrigem":"N(10)","grupo":"VDM","notas":"comprimento 10; ficheiro NRD"},
{"id":"VDM.Nº Ult Recebimento","descricao":"Nº Ult Recebimento","tipo":"inteiro","tipoOrigem":"N(10)","grupo":"VDM","notas":"comprimento 10; ficheiro NRD; OK"},
{"id":"VDM.Prefixo ATCUD","descricao":"Prefixo ATCUD","tipo":"texto","tipoOrigem":"C","grupo":"VDM","notas":"comprimento 15; ficheiro NRD"},
{"id":"VDM.Data ULt Enomenda","descricao":"Data ULt Enomenda","tipo":"data","tipoOrigem":"D","grupo":"VDM","notas":"comprimento 10; ficheiro NRD"},
{"id":"VDM.Data Ult. Fatura","descricao":"Data Ult. Fatura","tipo":"data","tipoOrigem":"D","grupo":"VDM","notas":"comprimento 10; ficheiro NRD"},
{"id":"VDM.Data Ult. Fatura Recibo","descricao":"Data Ult. Fatura Recibo","tipo":"data","tipoOrigem":"D","grupo":"VDM","notas":"comprimento 10; ficheiro NRD"},
{"id":"VDM.Data Ult. Nota Credito","descricao":"Data Ult. Nota Credito","tipo":"data","tipoOrigem":"D","grupo":"VDM","notas":"comprimento 10; ficheiro NRD"},
{"id":"VDM.Data Ult Alteração  Encomenda","descricao":"Data Ult Alteração  Encomenda","tipo":"data","tipoOrigem":"D","grupo":"VDM","notas":"comprimento 10; ficheiro NRD"},
{"id":"VDM.Data Ult . Recebimento","descricao":"Data Ult . Recebimento","tipo":"data","tipoOrigem":"D","grupo":"VDM","notas":"comprimento 10; ficheiro NRD"},
{"id":"VDM.Numero Guia Transporte","descricao":"Numero Guia Transporte","tipo":"inteiro","tipoOrigem":"N(10)","grupo":"VDM","notas":"comprimento 10; ficheiro VDM"},
{"id":"VDM.Numero Guia Transporte Extra","descricao":"Numero Guia Transporte Extra","tipo":"inteiro","tipoOrigem":"N(10)","grupo":"VDM","notas":"comprimento 10; ficheiro VDM"},
{"id":"VDM.Codigo Familia Extra","descricao":"Codigo Familia Extra","tipo":"texto","tipoOrigem":"C","grupo":"VDM","notas":"comprimento 7; ficheiro VDM"},
{"id":"VDM.Trata Recebimentos","descricao":"Trata Recebimentos","tipo":"booleano","tipoOrigem":"L","grupo":"VDM","notas":"comprimento 1; ficheiro VDM"},
{"id":"VDM.Num Ult. Recibo","descricao":"Num Ult. Recibo","tipo":"inteiro","tipoOrigem":"N(10)","grupo":"VDM","notas":"comprimento 10; ficheiro NRD"},
{"id":"VDM.Data Ult Recibo","descricao":"Data Ult Recibo","tipo":"inteiro","tipoOrigem":"N(10)","grupo":"VDM","notas":"comprimento 10; ficheiro NRD"},
{"id":"VDM.Numero Digitos Serie","descricao":"Numero Digitos Serie","tipo":"texto","tipoOrigem":"C","grupo":"VDM","notas":"comprimento 4; ficheiro NRD"},
{"id":"VDM.Prefixo ATCUD Fatura","descricao":"Prefixo ATCUD Fatura","tipo":"texto","tipoOrigem":"C","grupo":"VDM","notas":"comprimento 10; ficheiro NRD"},
{"id":"VDM.Prefixo ATCUD Fatura/ Recibo","descricao":"Prefixo ATCUD Fatura/ Recibo","tipo":"texto","tipoOrigem":"C","grupo":"VDM","notas":"comprimento 10; ficheiro NRD"},
{"id":"VDM.Prefixo ATCUD Nota Credito","descricao":"Prefixo ATCUD Nota Credito","tipo":"texto","tipoOrigem":"C","grupo":"VDM","notas":"comprimento 10; ficheiro NRD"},
{"id":"VDM.Prefixo ATCUD Encomenda","descricao":"Prefixo ATCUD Encomenda","tipo":"texto","tipoOrigem":"C","grupo":"VDM","notas":"comprimento 10; ficheiro NRD"},
{"id":"VDM.Prefixo ATCUD Recibo","descricao":"Prefixo ATCUD Recibo","tipo":"texto","tipoOrigem":"C","grupo":"VDM","notas":"comprimento 10; ficheiro NRD"},
{"id":"VDM.Contribuinte do Emissor","descricao":"Contribuinte do Emissor","tipo":"texto","tipoOrigem":"C","grupo":"VDM","notas":"comprimento 15; ficheiro VDM"},
{"id":"VDM.Num Ult Entrada em CC","descricao":"Num Ult Entrada em CC","tipo":"inteiro","tipoOrigem":"N(10)","grupo":"VDM","notas":"comprimento 10; ficheiro NRD"},
{"id":"VDM.Data Ult. Entrada CC","descricao":"Data Ult. Entrada CC","tipo":"inteiro","tipoOrigem":"N(10)","grupo":"VDM","notas":"comprimento 10; ficheiro NRD"},
{"id":"CLI.Codigo Cliente","descricao":"Codigo Cliente","tipo":"inteiro","tipoOrigem":"N","grupo":"CLI","nomesAlternativos":["code"],"notas":"comprimento 10; ficheiro CLI; IMUTAVEL (Automatico)"},
{"id":"CLI.Nome Cliente","descricao":"Nome Cliente","tipo":"texto","tipoOrigem":"C","grupo":"CLI","nomesAlternativos":["name"],"notas":"comprimento 35; ficheiro CLI; OK"},
{"id":"CLI.Morada Cliente","descricao":"Morada Cliente","tipo":"texto","tipoOrigem":"C","grupo":"CLI","nomesAlternativos":["address"],"notas":"comprimento 35; ficheiro CLI; OK"},
{"id":"CLI.Localidade Cliente","descricao":"Localidade Cliente","tipo":"texto","tipoOrigem":"C","grupo":"CLI","nomesAlternativos":["city"],"notas":"comprimento 35; ficheiro CLI; OK"},
{"id":"CLI.Codigo Postal cliente","descricao":"Codigo Postal cliente","tipo":"texto","tipoOrigem":"C","grupo":"CLI","nomesAlternativos":["zipCode","zipCodeLoc"],"notas":"comprimento 35; ficheiro CLI; Passa para 10 pq dividido em 2 campos"},
{"id":"CLI.Zona","descricao":"Zona","tipo":"texto","tipoOrigem":"C","grupo":"CLI","nomesAlternativos":["zone"],"notas":"comprimento 10; ficheiro CLI; Nao tem texto mas sim  -> Referencia para Zona"},
{"id":"CLI.Telefone Cliente","descricao":"Telefone Cliente","tipo":"texto","tipoOrigem":"C","grupo":"CLI","nomesAlternativos":["fixePhoneNumber"],"notas":"comprimento 15; ficheiro CLI"},
{"id":"CLI.Telemovel Cliente","descricao":"Telemovel Cliente","tipo":"texto","tipoOrigem":"C","grupo":"CLI","nomesAlternativos":["phoneNumber"],"notas":"comprimento 15; ficheiro CLI; Ok"},
{"id":"CLI.Data Abertura Ficha","descricao":"Data Abertura Ficha","tipo":"data","tipoOrigem":"D","grupo":"CLI","nomesAlternativos":["registrationDate"],"notas":"comprimento 10; ficheiro CLI; Parametro DATE"},
{"id":"CLI.Contribuinte Cliente","descricao":"Contribuinte Cliente","tipo":"texto","tipoOrigem":"C","grupo":"CLI","nomesAlternativos":["nif"],"notas":"comprimento 15; ficheiro CLI; Ok"},
{"id":"CLI.Codigo Vendedor","descricao":"Codigo Vendedor","tipo":"inteiro","tipoOrigem":"N(10)","grupo":"CLI","nomesAlternativos":["sellerCode"],"notas":"comprimento 10; ficheiro CLI"},
{"id":"CLI.Numero Ordem","descricao":"Numero Ordem","tipo":"inteiro","tipoOrigem":"N(6)","grupo":"CLI","nomesAlternativos":["orderNumber"],"notas":"comprimento 6; ficheiro CLI"},
{"id":"CLI.Email Cliente","descricao":"Email Cliente","tipo":"texto","tipoOrigem":"C","grupo":"CLI","nomesAlternativos":["email"],"notas":"comprimento 60; ficheiro CLI; 60? Usei 35"},
{"id":"CLI.Data Nascimento Cliente","descricao":"Data Nascimento Cliente","tipo":"data","tipoOrigem":"D","grupo":"CLI","nomesAlternativos":["dateOfBirth"],"notas":"comprimento 10; ficheiro CLI"},
{"id":"CLI.Local Cobrança","descricao":"Local Cobrança","tipo":"texto","tipoOrigem":"C","grupo":"CLI","nomesAlternativos":["chargeLocation"],"notas":"comprimento 10; ficheiro CLI; Usei 5"},
{"id":"CLI.Nome 2 Titular","descricao":"Nome 2 Titular","tipo":"texto","tipoOrigem":"C","grupo":"CLI","nomesAlternativos":["name2"],"notas":"comprimento 35; ficheiro CLI"},
{"id":"CLI.Morada 2 Titular","descricao":"Morada 2 Titular","tipo":"texto","tipoOrigem":"C","grupo":"CLI","nomesAlternativos":["address2"],"notas":"comprimento 35; ficheiro CLI"},
{"id":"CLI.Localidade 2 Titular","descricao":"Localidade 2 Titular","tipo":"texto","tipoOrigem":"C","grupo":"CLI","nomesAlternativos":["city2"],"notas":"comprimento 35; ficheiro CLI"},
{"id":"CLI.Cod Postal 2 Titular","descricao":"Cod Postal 2 Titular","tipo":"texto","tipoOrigem":"C","grupo":"CLI","nomesAlternativos":["zipCode2"],"notas":"comprimento 35; ficheiro CLI"},
{"id":"CLI.Nº CC 2 Titular","descricao":"Nº CC 2 Titular","tipo":"texto","tipoOrigem":"C","grupo":"CLI","nomesAlternativos":["citizenCard2"],"notas":"comprimento 15; ficheiro CLI"},
{"id":"CLI.Nº CC Cliente","descricao":"Nº CC Cliente","tipo":"texto","tipoOrigem":"C","grupo":"CLI","nomesAlternativos":["citizenCard"],"notas":"comprimento 15; ficheiro CLI"},
{"id":"CLI.Data Validade CC","descricao":"Data Validade CC","tipo":"data","tipoOrigem":"D","grupo":"CLI","nomesAlternativos":["citizenCardExpirationDate"],"notas":"comprimento 10; ficheiro CLI"},
{"id":"CLI.Data Validade CC 2 Titular","descricao":"Data Validade CC 2 Titular","tipo":"data","tipoOrigem":"D","grupo":"CLI","nomesAlternativos":["citizenCardExpirationDate2"],"notas":"comprimento 10; ficheiro CLI"},
{"id":"CLI.Telefone 2 Titular","descricao":"Telefone 2 Titular","tipo":"texto","tipoOrigem":"C","grupo":"CLI","nomesAlternativos":["fixePhoneNumber2"],"notas":"comprimento 15; ficheiro CLI"},
{"id":"CLI.Contribuinte 2 Titular","descricao":"Contribuinte 2 Titular","tipo":"texto","tipoOrigem":"C","grupo":"CLI","nomesAlternativos":["nif2"],"notas":"comprimento 15; ficheiro CLI"},
{"id":"CLI.Dia Recebimento","descricao":"Dia Recebimento","tipo":"inteiro","tipoOrigem":"N(2)","grupo":"CLI","notas":"comprimento 2; ficheiro CLI"},
{"id":"YCL.Codigo Cliente","descricao":"Codigo Cliente","tipo":"inteiro","tipoOrigem":"N(10)","grupo":"YCL","notas":"comprimento 10; ficheiro CLI"},
{"id":"YCL.Saldo","descricao":"Saldo","tipo":"decimal","tipoOrigem":"N(8.2)","grupo":"YCL","notas":"comprimento 13; ficheiro CLI"},
{"id":"YCL.Valor Total Vendas","descricao":"Valor Total Vendas","tipo":"decimal","tipoOrigem":"N(8.2)","grupo":"YCL","notas":"comprimento 13; ficheiro CLI"},
{"id":"YCL.Valor Saldo Inicial","descricao":"Valor Saldo Inicial","tipo":"decimal","tipoOrigem":"N(8.2)","grupo":"YCL","notas":"comprimento 13; ficheiro CLI"},
{"id":"YCL.Valor Pago Saldo Inicial","descricao":"Valor Pago Saldo Inicial","tipo":"decimal","tipoOrigem":"N(8.2)","grupo":"YCL","notas":"comprimento 13; ficheiro CLI"},
{"id":"YCL.Data Saldo Inicial","descricao":"Data Saldo Inicial","tipo":"data","tipoOrigem":"D","grupo":"YCL","notas":"comprimento 10; ficheiro CLI"},
{"id":"STK.Codigo Artigo","descricao":"Codigo Artigo","tipo":"texto","tipoOrigem":"C","grupo":"STK","notas":"comprimento 6; ficheiro STK"},
{"id":"STK.Codigo Axiliar","descricao":"Codigo Axiliar","tipo":"texto","tipoOrigem":"C","grupo":"STK","notas":"comprimento 13; ficheiro STK"},
{"id":"STK.Codigp EAN","descricao":"Codigp EAN","tipo":"texto","tipoOrigem":"C","grupo":"STK","notas":"comprimento 15; ficheiro STK"},
{"id":"STK.Descricao","descricao":"Descricao","tipo":"texto","tipoOrigem":"C","grupo":"STK","notas":"comprimento 50; ficheiro STK"},
{"id":"STK.Referencia","descricao":"Referencia","tipo":"texto","tipoOrigem":"C","grupo":"STK","notas":"comprimento 20; ficheiro STK"},
{"id":"STK.Unidade Medida","descricao":"Unidade Medida","tipo":"texto","tipoOrigem":"C","grupo":"STK","notas":"comprimento 6; ficheiro STK"},
{"id":"STK.Data Criação ficha","descricao":"Data Criação ficha","tipo":"data","tipoOrigem":"D","grupo":"STK","notas":"comprimento 10; ficheiro STK"},
{"id":"STK.Preço Venda com Iva","descricao":"Preço Venda com Iva","tipo":"decimal","tipoOrigem":"N(8.3)","grupo":"STK","notas":"comprimento 13; ficheiro STK"},
{"id":"STK.% Desconto1","descricao":"% Desconto1","tipo":"decimal","tipoOrigem":"N(2.2)","grupo":"STK","notas":"comprimento 6; ficheiro STK"},
{"id":"STK.% Desconto2","descricao":"% Desconto2","tipo":"decimal","tipoOrigem":"N(2.2)","grupo":"STK","notas":"comprimento 6; ficheiro STK"},
{"id":"STK.Taxa de Iva","descricao":"Taxa de Iva","tipo":"decimal","tipoOrigem":"N(2.2)","grupo":"STK","notas":"comprimento 5; ficheiro STK"},
{"id":"STK.Quantidade em stock","descricao":"Quantidade em stock","tipo":"decimal","tipoOrigem":"N(6.3)","grupo":"STK","notas":"comprimento 10; ficheiro STK"},
{"id":"STK.Quantidade em stock Out","descricao":"Quantidade em stock Out","tipo":"decimal","tipoOrigem":"N(6.3)","grupo":"STK","notas":"comprimento 10; ficheiro STK"},
{"id":"STK.Peso","descricao":"Peso","tipo":"decimal","tipoOrigem":"N(3.3)","grupo":"STK","notas":"comprimento 10; ficheiro STK"},
{"id":"STK.Preço Venda 1 sem Iva","descricao":"Preço Venda 1 sem Iva","tipo":"decimal","tipoOrigem":"N(10.3)","grupo":"STK","notas":"comprimento 13; ficheiro STK"},
{"id":"STK.Codigo Familia","descricao":"Codigo Familia","tipo":"texto","tipoOrigem":"C","grupo":"STK","notas":"comprimento 7; ficheiro STK"},
{"id":"STK.Preço Custo sem Iva","descricao":"Preço Custo sem Iva","tipo":"decimal","tipoOrigem":"N(10.3)","grupo":"STK","notas":"comprimento 13; ficheiro STK"},
{"id":"STK.Preço Custo com Iva","descricao":"Preço Custo com Iva","tipo":"decimal","tipoOrigem":"N(10.3)","grupo":"STK","notas":"comprimento 13; ficheiro STK"},
{"id":"STK.Codigo Fornecedor","descricao":"Codigo Fornecedor","tipo":"inteiro","tipoOrigem":"N(10)","grupo":"STK","notas":"comprimento 10; ficheiro STK"},
{"id":"STK.Nome Fornecedor","descricao":"Nome Fornecedor","tipo":"texto","tipoOrigem":"C","grupo":"STK","notas":"comprimento 35; ficheiro STK"},
{"id":"STK.Descricção Familia","descricao":"Descricção Familia","tipo":"texto","tipoOrigem":"C","grupo":"STK","notas":"comprimento 35; ficheiro STK"},
{"id":"STK.Preço Venda 2 com IVA","descricao":"Preço Venda 2 com IVA","tipo":"decimal","tipoOrigem":"N(10.3)","grupo":"STK","notas":"comprimento 13; ficheiro STK"},
{"id":"STK.Preço Venda 2 sem IVA","descricao":"Preço Venda 2 sem IVA","tipo":"decimal","tipoOrigem":"N(10.3)","grupo":"STK","notas":"comprimento 13; ficheiro STK"},
{"id":"STK.Serviço","descricao":"Serviço","tipo":"booleano","tipoOrigem":"L","grupo":"STK","notas":"comprimento 1; ficheiro STK"},
{"id":"STK.Exporta OBS","descricao":"Exporta OBS","tipo":"booleano","tipoOrigem":"L","grupo":"STK","notas":"comprimento 1; ficheiro STK"},
{"id":"AUX.ID","descricao":"ID","tipo":"inteiro","tipoOrigem":"N(3)","grupo":"AUX","notas":"comprimento 3; ficheiro AUX"},
{"id":"AUX.Texto","descricao":"Texto","tipo":"texto","tipoOrigem":"C","grupo":"AUX","notas":"comprimento 40; ficheiro AUX"},
{"id":"PRV.Matricula","descricao":"Matricula","tipo":"texto","tipoOrigem":"C","grupo":"PRV","notas":"comprimento 15"},
{"id":"PRV.Codigo Artigo","descricao":"Codigo Artigo","tipo":"texto","tipoOrigem":"C","grupo":"PRV","notas":"comprimento 7"},
{"id":"PRV.Quantidade Total","descricao":"Quantidade Total","tipo":"decimal","tipoOrigem":"N(7.2)","grupo":"PRV","notas":"comprimento 10"},
{"id":"PRV.Quantidade Normal","descricao":"Quantidade Normal","tipo":"decimal","tipoOrigem":"N(7.2)","grupo":"PRV","notas":"comprimento 10"},
{"id":"PRV.Quantidade Fora","descricao":"Quantidade Fora","tipo":"decimal","tipoOrigem":"N(7.2)","grupo":"PRV","notas":"comprimento 10"}
]
```

Regras (50):
```json
[
{"id":"VDM-2-COMPRIMENTO","texto":"Nome Vendedor tem no máximo 35 caracteres.","categoria":"formato","natureza":"RP","contexto":"VDM","elementos":["VDM.Nome Vendedor"],"expressao":"LENGTH [0, 35]"},
{"id":"VDM-3-COMPRIMENTO","texto":"Morada Vendedor tem no máximo 35 caracteres.","categoria":"formato","natureza":"RP","contexto":"VDM","elementos":["VDM.Morada Vendedor"],"expressao":"LENGTH [0, 35]"},
{"id":"VDM-4-COMPRIMENTO","texto":"Localidade Vendedor tem no máximo 35 caracteres.","categoria":"formato","natureza":"RP","contexto":"VDM","elementos":["VDM.Localidade Vendedor"],"expressao":"LENGTH [0, 35]"},
{"id":"VDM-5-COMPRIMENTO","texto":"Codigo Postal vendedor tem no máximo 35 caracteres.","categoria":"formato","natureza":"RP","contexto":"VDM","elementos":["VDM.Codigo Postal vendedor"],"expressao":"LENGTH [0, 35]"},
{"id":"VDM-6-COMPRIMENTO","texto":"Telfone Vendedor tem no máximo 15 caracteres.","categoria":"formato","natureza":"RP","contexto":"VDM","elementos":["VDM.Telfone Vendedor"],"expressao":"LENGTH [0, 15]"},
{"id":"VDM-7-COMPRIMENTO","texto":"Telemovel Vendedor tem no máximo 15 caracteres.","categoria":"formato","natureza":"RP","contexto":"VDM","elementos":["VDM.Telemovel Vendedor"],"expressao":"LENGTH [0, 15]"},
{"id":"VDM-8-COMPRIMENTO","texto":"NIF Vendedor tem no máximo 15 caracteres.","categoria":"formato","natureza":"RP","contexto":"VDM","elementos":["VDM.NIF Vendedor"],"expressao":"LENGTH [0, 15]"},
{"id":"VDM-10-COMPRIMENTO","texto":"Serie Numerações tem no máximo 3 caracteres.","categoria":"formato","natureza":"RP","contexto":"VDM","elementos":["VDM.Serie Numerações"],"expressao":"LENGTH [0, 3]"},
{"id":"VDM-15-COMPRIMENTO","texto":"Matricula tem no máximo 15 caracteres.","categoria":"formato","natureza":"RP","contexto":"VDM","elementos":["VDM.Matricula"],"expressao":"LENGTH [0, 15]"},
{"id":"VDM-16-COMPRIMENTO","texto":"Veiculo tem no máximo 25 caracteres.","categoria":"formato","natureza":"RP","contexto":"VDM","elementos":["VDM.Veiculo"],"expressao":"LENGTH [0, 25]"},
{"id":"VDM-17-COMPRIMENTO","texto":"Modelo tem no máximo 20 caracteres.","categoria":"formato","natureza":"RP","contexto":"VDM","elementos":["VDM.Modelo"],"expressao":"LENGTH [0, 20]"},
{"id":"VDM-24-COMPRIMENTO","texto":"Prefixo ATCUD tem no máximo 15 caracteres.","categoria":"formato","natureza":"RP","contexto":"VDM","elementos":["VDM.Prefixo ATCUD"],"expressao":"LENGTH [0, 15]"},
{"id":"VDM-33-COMPRIMENTO","texto":"Codigo Familia Extra tem no máximo 7 caracteres.","categoria":"formato","natureza":"RP","contexto":"VDM","elementos":["VDM.Codigo Familia Extra"],"expressao":"LENGTH [0, 7]"},
{"id":"VDM-37-COMPRIMENTO","texto":"Numero Digitos Serie tem no máximo 4 caracteres.","categoria":"formato","natureza":"RP","contexto":"VDM","elementos":["VDM.Numero Digitos Serie"],"expressao":"LENGTH [0, 4]"},
{"id":"VDM-38-COMPRIMENTO","texto":"Prefixo ATCUD Fatura tem no máximo 10 caracteres.","categoria":"formato","natureza":"RP","contexto":"VDM","elementos":["VDM.Prefixo ATCUD Fatura"],"expressao":"LENGTH [0, 10]"},
{"id":"VDM-39-COMPRIMENTO","texto":"Prefixo ATCUD Fatura/ Recibo tem no máximo 10 caracteres.","categoria":"formato","natureza":"RP","contexto":"VDM","elementos":["VDM.Prefixo ATCUD Fatura/ Recibo"],"expressao":"LENGTH [0, 10]"},
{"id":"VDM-40-COMPRIMENTO","texto":"Prefixo ATCUD Nota Credito tem no máximo 10 caracteres.","categoria":"formato","natureza":"RP","contexto":"VDM","elementos":["VDM.Prefixo ATCUD Nota Credito"],"expressao":"LENGTH [0, 10]"},
{"id":"VDM-41-COMPRIMENTO","texto":"Prefixo ATCUD Encomenda tem no máximo 10 caracteres.","categoria":"formato","natureza":"RP","contexto":"VDM","elementos":["VDM.Prefixo ATCUD Encomenda"],"expressao":"LENGTH [0, 10]"},
{"id":"VDM-42-COMPRIMENTO","texto":"Prefixo ATCUD Recibo tem no máximo 10 caracteres.","categoria":"formato","natureza":"RP","contexto":"VDM","elementos":["VDM.Prefixo ATCUD Recibo"],"expressao":"LENGTH [0, 10]"},
{"id":"VDM-43-COMPRIMENTO","texto":"Contribuinte do Emissor tem no máximo 15 caracteres.","categoria":"formato","natureza":"RP","contexto":"VDM","elementos":["VDM.Contribuinte do Emissor"],"expressao":"LENGTH [0, 15]"},
{"id":"CLI-2-COMPRIMENTO","texto":"Nome Cliente tem no máximo 35 caracteres.","categoria":"formato","natureza":"RP","contexto":"CLI","elementos":["CLI.Nome Cliente"],"expressao":"LENGTH [0, 35]"},
{"id":"CLI-3-COMPRIMENTO","texto":"Morada Cliente tem no máximo 35 caracteres.","categoria":"formato","natureza":"RP","contexto":"CLI","elementos":["CLI.Morada Cliente"],"expressao":"LENGTH [0, 35]"},
{"id":"CLI-4-COMPRIMENTO","texto":"Localidade Cliente tem no máximo 35 caracteres.","categoria":"formato","natureza":"RP","contexto":"CLI","elementos":["CLI.Localidade Cliente"],"expressao":"LENGTH [0, 35]"},
{"id":"CLI-5-COMPRIMENTO","texto":"Codigo Postal cliente tem no máximo 35 caracteres.","categoria":"formato","natureza":"RP","contexto":"CLI","elementos":["CLI.Codigo Postal cliente"],"expressao":"LENGTH [0, 35]"},
{"id":"CLI-6-COMPRIMENTO","texto":"Zona tem no máximo 10 caracteres.","categoria":"formato","natureza":"RP","contexto":"CLI","elementos":["CLI.Zona"],"expressao":"LENGTH [0, 10]"},
{"id":"CLI-7-COMPRIMENTO","texto":"Telefone Cliente tem no máximo 15 caracteres.","categoria":"formato","natureza":"RP","contexto":"CLI","elementos":["CLI.Telefone Cliente"],"expressao":"LENGTH [0, 15]"},
{"id":"CLI-8-COMPRIMENTO","texto":"Telemovel Cliente tem no máximo 15 caracteres.","categoria":"formato","natureza":"RP","contexto":"CLI","elementos":["CLI.Telemovel Cliente"],"expressao":"LENGTH [0, 15]"},
{"id":"CLI-10-COMPRIMENTO","texto":"Contribuinte Cliente tem no máximo 15 caracteres.","categoria":"formato","natureza":"RP","contexto":"CLI","elementos":["CLI.Contribuinte Cliente"],"expressao":"LENGTH [0, 15]"},
{"id":"CLI-13-COMPRIMENTO","texto":"Email Cliente tem no máximo 60 caracteres.","categoria":"formato","natureza":"RP","contexto":"CLI","elementos":["CLI.Email Cliente"],"expressao":"LENGTH [0, 60]"},
{"id":"CLI-15-COMPRIMENTO","texto":"Local Cobrança tem no máximo 10 caracteres.","categoria":"formato","natureza":"RP","contexto":"CLI","elementos":["CLI.Local Cobrança"],"expressao":"LENGTH [0, 10]"},
{"id":"CLI-16-COMPRIMENTO","texto":"Nome 2 Titular tem no máximo 35 caracteres.","categoria":"formato","natureza":"RP","contexto":"CLI","elementos":["CLI.Nome 2 Titular"],"expressao":"LENGTH [0, 35]"},
{"id":"CLI-17-COMPRIMENTO","texto":"Morada 2 Titular tem no máximo 35 caracteres.","categoria":"formato","natureza":"RP","contexto":"CLI","elementos":["CLI.Morada 2 Titular"],"expressao":"LENGTH [0, 35]"},
{"id":"CLI-18-COMPRIMENTO","texto":"Localidade 2 Titular tem no máximo 35 caracteres.","categoria":"formato","natureza":"RP","contexto":"CLI","elementos":["CLI.Localidade 2 Titular"],"expressao":"LENGTH [0, 35]"},
{"id":"CLI-19-COMPRIMENTO","texto":"Cod Postal 2 Titular tem no máximo 35 caracteres.","categoria":"formato","natureza":"RP","contexto":"CLI","elementos":["CLI.Cod Postal 2 Titular"],"expressao":"LENGTH [0, 35]"},
{"id":"CLI-20-COMPRIMENTO","texto":"Nº CC 2 Titular tem no máximo 15 caracteres.","categoria":"formato","natureza":"RP","contexto":"CLI","elementos":["CLI.Nº CC 2 Titular"],"expressao":"LENGTH [0, 15]"},
{"id":"CLI-21-COMPRIMENTO","texto":"Nº CC Cliente tem no máximo 15 caracteres.","categoria":"formato","natureza":"RP","contexto":"CLI","elementos":["CLI.Nº CC Cliente"],"expressao":"LENGTH [0, 15]"},
{"id":"CLI-24-COMPRIMENTO","texto":"Telefone 2 Titular tem no máximo 15 caracteres.","categoria":"formato","natureza":"RP","contexto":"CLI","elementos":["CLI.Telefone 2 Titular"],"expressao":"LENGTH [0, 15]"},
{"id":"CLI-25-COMPRIMENTO","texto":"Contribuinte 2 Titular tem no máximo 15 caracteres.","categoria":"formato","natureza":"RP","contexto":"CLI","elementos":["CLI.Contribuinte 2 Titular"],"expressao":"LENGTH [0, 15]"},
{"id":"STK-1-COMPRIMENTO","texto":"Codigo Artigo tem no máximo 6 caracteres.","categoria":"formato","natureza":"RP","contexto":"STK","elementos":["STK.Codigo Artigo"],"expressao":"LENGTH [0, 6]"},
{"id":"STK-2-COMPRIMENTO","texto":"Codigo Axiliar tem no máximo 13 caracteres.","categoria":"formato","natureza":"RP","contexto":"STK","elementos":["STK.Codigo Axiliar"],"expressao":"LENGTH [0, 13]"},
{"id":"STK-3-COMPRIMENTO","texto":"Codigp EAN tem no máximo 15 caracteres.","categoria":"formato","natureza":"RP","contexto":"STK","elementos":["STK.Codigp EAN"],"expressao":"LENGTH [0, 15]"},
{"id":"STK-4-COMPRIMENTO","texto":"Descricao tem no máximo 50 caracteres.","categoria":"formato","natureza":"RP","contexto":"STK","elementos":["STK.Descricao"],"expressao":"LENGTH [0, 50]"},
{"id":"STK-5-COMPRIMENTO","texto":"Referencia tem no máximo 20 caracteres.","categoria":"formato","natureza":"RP","contexto":"STK","elementos":["STK.Referencia"],"expressao":"LENGTH [0, 20]"},
{"id":"STK-6-COMPRIMENTO","texto":"Unidade Medida tem no máximo 6 caracteres.","categoria":"formato","natureza":"RP","contexto":"STK","elementos":["STK.Unidade Medida"],"expressao":"LENGTH [0, 6]"},
{"id":"STK-16-COMPRIMENTO","texto":"Codigo Familia tem no máximo 7 caracteres.","categoria":"formato","natureza":"RP","contexto":"STK","elementos":["STK.Codigo Familia"],"expressao":"LENGTH [0, 7]"},
{"id":"STK-20-COMPRIMENTO","texto":"Nome Fornecedor tem no máximo 35 caracteres.","categoria":"formato","natureza":"RP","contexto":"STK","elementos":["STK.Nome Fornecedor"],"expressao":"LENGTH [0, 35]"},
{"id":"STK-21-COMPRIMENTO","texto":"Descricção Familia tem no máximo 35 caracteres.","categoria":"formato","natureza":"RP","contexto":"STK","elementos":["STK.Descricção Familia"],"expressao":"LENGTH [0, 35]"},
{"id":"AUX-2-COMPRIMENTO","texto":"Texto tem no máximo 40 caracteres.","categoria":"formato","natureza":"RP","contexto":"AUX","elementos":["AUX.Texto"],"expressao":"LENGTH [0, 40]"},
{"id":"PRV-1-COMPRIMENTO","texto":"Matricula tem no máximo 15 caracteres.","categoria":"formato","natureza":"RP","contexto":"PRV","elementos":["PRV.Matricula"],"expressao":"LENGTH [0, 15]"},
{"id":"PRV-2-COMPRIMENTO","texto":"Codigo Artigo tem no máximo 7 caracteres.","categoria":"formato","natureza":"RP","contexto":"PRV","elementos":["PRV.Codigo Artigo"],"expressao":"LENGTH [0, 7]"}
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
