# Pedido de alterações → operações

## Objetivo

Traduzir um pedido de alterações, escrito em linguagem natural pela pessoa que revê as declarações, numa lista de operações do vocabulário fechado, que o código aplica de forma determinística às declarações do domínio. O pedido pode corrigir o que existe ou acrescentar informação nova (de uma tabela, de um documento ou de outra fonte, dada em "Informação adicional"). Não alteres nada que o pedido não diga; se o pedido for ambíguo, escolhe a interpretação mínima e explica-a em `notas`.

Camada em revisão: B (Projeções (RE)).

## Orientação da camada

Camada em revisão: B · Projeções (RE). Declarar as utilizações de cada HLM (projeções) com as propriedades obrigatórias e permitidas: as regras estruturais.

Princípios da camada:
- A obrigatoriedade de uma propriedade numa utilização exprime-se na projeção, não numa regra.
- Uma projeção por utilização real (fatura eletrónica CIUS-PT, nota de crédito, exportação FM); não se inventam utilizações.
- Caminhos a partir do HLM; X.* para tudo abaixo de X; um caminho não pode ser obrigatório e permitido ao mesmo tempo.
- Regras de presença condicionais ('se existir X, então Y é obrigatório') não são projeções: são RIR (com uma função de presença).

Procedimento da camada:
1. Para cada HLM, uma projeção por utilização real do domínio (as utilizações estão nos dados).
2. Cada regra de presença ou de cardinalidade da fonte torna a propriedade obrigatória (OBRIGATORIA) numa ou mais projeções; o que não é obrigatório mas pode estar presente é permitido; o resto fica excluído (não se declara).
3. Caminhos a partir do HLM; X.* quando tudo abaixo de X tem o mesmo tratamento.
4. Uma regra de presença condicional ("se…, então… é obrigatório") não é uma projeção: é uma RIR com uma função de presença (ver funções).
5. Mapeamento de cada regra tratada: destino Projecao:<Nome>/<caminho>, ou descartada com o motivo.

## Exemplos de pedidos e das operações correspondentes

- "Coloca a morada de entrega num USM próprio": `extrair_usm` (ou `compor` do USM Morada com o papel MoradaEntrega, se já existir).
- "Esta propriedade pertence àquele USM": `mover_propriedade`.
- "Estes dois USM são o mesmo": `fundir_modelos`.
- "As linhas são obrigatórias, pelo menos uma": `alterar_composicao` (cardinalidade 1..*).
- "Muda o nome de X para Y": `renomear_modelo` ou `renomear_propriedade`.
- "Este campo da fonte não interessa": `mapear` com decisão `descartado` e o motivo.
- "A regra X só se aplica a faturas simplificadas": `substituir_regra` (acrescenta o termo à condição; uma RP passa a RIR).
- "Num laboratório, a humidade tem de estar entre 30 e 60 %": `adicionar_regra` com uma RIR (condição sobre o ambiente e o tipo de dispositivo, restrição RANGE sobre o valor).
- "Acrescenta as regras desta tabela" (com a tabela em Informação adicional): uma `adicionar_regra` por linha, e `mapear` quando a tabela vem de uma fonte do inventário.

## Vocabulário de operações

- `criar_modelo` (nivel, nome, descricao, propriedades?, composicao?, declaracoes?): Cria um USM ou SM (nas declarações indicadas, ou nas que o vierem a compor).
- `remover_modelo` (nivel, nome): Remove o modelo e as composições que o referem.
- `renomear_modelo` (nivel, de, para): Muda o nome e atualiza as composições que o referem (o papel por omissão muda com ele).
- `alterar_modelo` (nivel, nome, descricao?, notas?): Muda a descrição ou as notas.
- `fundir_modelos` (nivel, de: [nomes], para): Junta vários modelos num só: as propriedades unem-se (pelo nome) e as composições passam a apontar para o modelo resultante.
- `extrair_usm` (de: {nivel, modelo}, propriedades: [nomes], novo: {nome, descricao}, papel?, cardinalidade?): Cria um USM com as propriedades indicadas, retira-as do modelo de origem e compõe o novo USM nele.
- `criar_hlm` (nome, descricao, composicao, declaracao?): Cria um HLM e a sua declaração.
- `remover_hlm` (nome): Remove a declaração do HLM.
- `adicionar_propriedade` (nivel, modelo, propriedade): Acrescenta uma propriedade ao modelo.
- `remover_propriedade` (nivel, modelo, nome): Remove a propriedade (e as regras que vivem nela).
- `mover_propriedade` (de: {nivel, modelo}, para: {nivel, modelo}, nome): Move a propriedade, com as regras que vivem nela, para outro modelo.
- `renomear_propriedade` (nivel, modelo, de, para): Muda o nome; o nome antigo passa a nome alternativo.
- `alterar_propriedade` (nivel, modelo, nome, tipo?, descricao?, nomesAlternativos?): Muda o tipo, a descrição ou os nomes alternativos.
- `compor` (pai: {nivel, nome}, filho: {nivel, nome}, cardinalidade, papel?): Acrescenta uma composição; o filho é copiado para as declarações do pai que ainda não o têm.
- `remover_composicao` (pai, filho, papel?): Remove uma composição.
- `alterar_composicao` (pai, filho, papel?, cardinalidade?, novoPapel?): Muda a cardinalidade ou o papel.
- `adicionar_regra` (onde: {nivel, modelo, propriedade?}, regra): Acrescenta uma regra (RP, RIR ou RIC) no nó indicado.
- `substituir_regra` (id, regra): Substitui a regra com esse id (onde quer que viva).
- `remover_regra` (id): Remove a regra.
- `mover_regra` (id, para: {nivel, modelo, propriedade?}): Move a regra para outro nó (os caminhos têm de ser revistos: a verificação aponta-os).
- `definir_projecao` (projecao): Cria ou substitui uma projeção (na declaração do seu HLM).
- `remover_projecao` (nome): Remove a projeção.
- `definir_perfil` (perfil): Cria ou substitui um perfil (na declaração do HLM da sua projeção).
- `remover_perfil` (nome): Remove o perfil.
- `definir_funcao` (funcao, declaracoes?): Cria ou substitui uma função (em todas as declarações que a têm, ou nas indicadas).
- `remover_funcao` (nome): Remove a função.
- `definir_contexto` (contexto, declaracoes?): Cria ou substitui um contexto externo.
- `remover_contexto` (nome): Remove o contexto externo.
- `mapear` (fonte, origem, decisao, destino?, motivo?): Regista ou corrige uma entrada do mapeamento.

Operações mais usadas nesta camada: definir_projecao, remover_projecao, mapear. Qualquer operação do vocabulário pode ser usada.

### Forma exata dos campos (exemplos)

`nivel` é sempre `"HLM"`, `"SM"` ou `"USM"`. Os campos `pai`, `filho`, `de`, `para` e `onde` são objetos:

```json
{"op": "renomear_propriedade", "nivel": "USM", "modelo": "Morada", "de": "cp", "para": "codigoPostal"}
{"op": "mover_propriedade", "de": {"nivel": "SM", "modelo": "Cliente"}, "para": {"nivel": "USM", "modelo": "Contacto"}, "nome": "telefone"}
{"op": "compor", "pai": {"nivel": "SM", "nome": "Cliente"}, "filho": {"nivel": "USM", "nome": "Morada"}, "cardinalidade": "0..1", "papel": "MoradaEntrega"}
{"op": "alterar_composicao", "pai": {"nivel": "HLM", "nome": "Fatura"}, "filho": {"nivel": "SM", "nome": "Linhas"}, "cardinalidade": "1..1", "novoPapel": "LinhasDocumento"}
{"op": "extrair_usm", "de": {"nivel": "SM", "modelo": "Cliente"}, "propriedades": ["rua", "localidade"], "novo": {"nome": "Morada", "descricao": "…"}, "cardinalidade": "1..1"}
{"op": "adicionar_regra", "onde": {"nivel": "USM", "modelo": "Morada", "propriedade": "pais"}, "regra": {"id": "RP-PAIS", "natureza": "plausibilidade", "restricao": {"propriedade": "pais", "operador": "IN", "valor": ["PT"], "mensagem": "…"}}}
{"op": "mapear", "fonte": "fm-dart", "origem": "Client.zip", "decisao": "mapeado", "destino": "HLM:Fatura/Cliente.Morada.codigoPostal"}
```

### O que o código faz sozinho e o que tens de fazer tu

- Renomear um modelo, uma propriedade ou um papel, e extrair um USM, reescreve os caminhos das projeções, dos perfis, das regras e dos destinos do mapeamento.
- Mover uma propriedade (`mover_propriedade`) muda o sítio dela na árvore: os caminhos antigos deixam de existir. Acrescenta tu as operações `mapear` (e `substituir_regra`, se houver regras com esses caminhos) para os novos caminhos.
- Uma operação sobre um modelo partilhado aplica-se a todas as declarações que o contêm.

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


## Declarações atuais do domínio

```json
[
 {
  "$schema": "../../../specs/declaracao/ecv.schema.json",
  "declaracao": {
   "nome": "documento_faturacao",
   "versao": "0.1.0",
   "descricao": "Documento de faturação CIUS-PT (fatura 380, nota de crédito 381, nota de débito 383, adiantamento 386, autofaturação 389): estrutura semântica EN 16931 e regras do schematron CIUS-PT 2.1.1.",
   "dominios": [
    "faturação"
   ],
   "hlm": "DocumentoFaturacao"
  },
  "funcoes": [
   {
    "nome": "algumPresente",
    "descricao": "Verdadeira quando pelo menos um dos dois valores indicados está presente.",
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
    "contextosExternos": [],
    "retorno": "booleano"
   },
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
    "contextosExternos": [],
    "retorno": "booleano"
   },
   {
    "nome": "existe",
    "descricao": "Verdadeira quando o valor indicado está presente.",
    "parametros": [
     {
      "nome": "valor",
      "tipo": "valor",
      "papel": "alvo"
     }
    ],
    "contextosExternos": [],
    "retorno": "booleano"
   },
   {
    "nome": "colecaoNaoVazia",
    "descricao": "Verdadeira quando a coleção tem pelo menos um valor presente.",
    "parametros": [
     {
      "nome": "valores",
      "tipo": "lista<valor>",
      "papel": "alvo",
      "colecao": true
     }
    ],
    "contextosExternos": [],
    "retorno": "booleano"
   },
   {
    "nome": "mutuamenteExclusivos",
    "descricao": "Verdadeira quando os dois valores indicados não estão presentes ao mesmo tempo.",
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
    "contextosExternos": [],
    "retorno": "booleano"
   },
   {
    "nome": "naoAnteriorA",
    "descricao": "Verdadeira quando alguma das datas está ausente ou quando a data não é anterior à data de referência.",
    "parametros": [
     {
      "nome": "data",
      "tipo": "data",
      "papel": "alvo"
     },
     {
      "nome": "referencia",
      "tipo": "data",
      "papel": "alvo"
     }
    ],
    "contextosExternos": [],
    "retorno": "booleano"
   },
   {
    "nome": "somaIgualATolerancia",
    "descricao": "Verdadeira quando o total está ausente ou quando a soma dos valores da coleção difere do total, no máximo, pela tolerância.",
    "parametros": [
     {
      "nome": "valores",
      "tipo": "lista<decimal>",
      "papel": "alvo",
      "colecao": true
     },
     {
      "nome": "total",
      "tipo": "decimal",
      "papel": "alvo"
     },
     {
      "nome": "tolerancia",
      "tipo": "decimal",
      "papel": "parametro"
     }
    ],
    "contextosExternos": [],
    "retorno": "booleano"
   },
   {
    "nome": "somaParcelasIgualA",
    "descricao": "Verdadeira quando o total está ausente ou quando a soma das duas parcelas (as ausentes contam como zero) difere do total, no máximo, pela tolerância.",
    "parametros": [
     {
      "nome": "parcelaA",
      "tipo": "decimal",
      "papel": "alvo"
     },
     {
      "nome": "parcelaB",
      "tipo": "decimal",
      "papel": "alvo"
     },
     {
      "nome": "total",
      "tipo": "decimal",
      "papel": "alvo"
     },
     {
      "nome": "tolerancia",
      "tipo": "decimal",
      "papel": "parametro"
     }
    ],
    "contextosExternos": [],
    "retorno": "booleano"
   },
   {
    "nome": "saldoIgualA",
    "descricao": "Verdadeira quando base menos subtrair mais somar (os ausentes contam como zero) difere do total, no máximo, pela tolerância.",
    "parametros": [
     {
      "nome": "base",
      "tipo": "decimal",
      "papel": "alvo"
     },
     {
      "nome": "subtrair",
      "tipo": "decimal",
      "papel": "alvo"
     },
     {
      "nome": "somar",
      "tipo": "decimal",
      "papel": "alvo"
     },
     {
      "nome": "total",
      "tipo": "decimal",
      "papel": "alvo"
     },
     {
      "nome": "tolerancia",
      "tipo": "decimal",
      "papel": "parametro"
     }
    ],
    "contextosExternos": [],
    "retorno": "booleano"
   },
   {
    "nome": "produtoPercentualIgualA",
    "descricao": "Verdadeira quando falta a base ou a percentagem, ou quando base × percentagem / 100 difere do resultado, no máximo, pela tolerância.",
    "parametros": [
     {
      "nome": "base",
      "tipo": "decimal",
      "papel": "alvo"
     },
     {
      "nome": "percentagem",
      "tipo": "decimal",
      "papel": "alvo"
     },
     {
      "nome": "resultado",
      "tipo": "decimal",
      "papel": "alvo"
     },
     {
      "nome": "tolerancia",
      "tipo": "decimal",
      "papel": "parametro"
     }
    ],
    "contextosExternos": [],
    "retorno": "booleano"
   },
   {
    "nome": "montanteLinhaCoerente",
    "descricao": "Verdadeira quando quantidade × preço / quantidade base (1 se ausente ou zero), menos os descontos e mais os encargos da linha, difere do montante da linha, no máximo, pela tolerância.",
    "parametros": [
     {
      "nome": "quantidade",
      "tipo": "decimal",
      "papel": "alvo"
     },
     {
      "nome": "preco",
      "tipo": "decimal",
      "papel": "alvo"
     },
     {
      "nome": "quantidadeBase",
      "tipo": "decimal",
      "papel": "alvo"
     },
     {
      "nome": "descontos",
      "tipo": "lista<decimal>",
      "papel": "alvo",
      "colecao": true
     },
     {
      "nome": "encargos",
      "tipo": "lista<decimal>",
      "papel": "alvo",
      "colecao": true
     },
     {
      "nome": "montante",
      "tipo": "decimal",
      "papel": "alvo"
     },
     {
      "nome": "tolerancia",
      "tipo": "decimal",
      "papel": "parametro"
     }
    ],
    "contextosExternos": [],
    "retorno": "booleano"
   },
   {
    "nome": "baseTributavelCoerente",
    "descricao": "Verdadeira quando, para cada categoria e taxa de IVA da decomposição, a base tributável é igual à soma dos montantes das linhas mais os encargos e menos os descontos dessa categoria e taxa (com a tolerância).",
    "parametros": [
     {
      "nome": "decomposicoes",
      "tipo": "modelo",
      "papel": "alvo",
      "colecao": true
     },
     {
      "nome": "linhas",
      "tipo": "modelo",
      "papel": "alvo",
      "colecao": true
     },
     {
      "nome": "descontos",
      "tipo": "modelo",
      "papel": "alvo",
      "colecao": true
     },
     {
      "nome": "encargos",
      "tipo": "modelo",
      "papel": "alvo",
      "colecao": true
     },
     {
      "nome": "tolerancia",
      "tipo": "decimal",
      "papel": "parametro"
     }
    ],
    "contextosExternos": [],
    "retorno": "booleano"
   },
   {
    "nome": "categoriasIvaDecompostas",
    "descricao": "Verdadeira quando cada código de categoria de IVA usado nas linhas, nos descontos e nos encargos aparece na decomposição do IVA.",
    "parametros": [
     {
      "nome": "codigosLinhas",
      "tipo": "lista<texto>",
      "papel": "alvo",
      "colecao": true
     },
     {
      "nome": "codigosDescontos",
      "tipo": "lista<texto>",
      "papel": "alvo",
      "colecao": true
     },
     {
      "nome": "codigosEncargos",
      "tipo": "lista<texto>",
      "papel": "alvo",
      "colecao": true
     },
     {
      "nome": "codigosDecomposicao",
      "tipo": "lista<texto>",
      "papel": "alvo",
      "colecao": true
     }
    ],
    "contextosExternos": [],
    "retorno": "booleano"
   },
   {
    "nome": "valoresTextoUnicos",
    "descricao": "Verdadeira quando nenhum valor de texto da coleção se repete.",
    "parametros": [
     {
      "nome": "valores",
      "tipo": "lista<texto>",
      "papel": "alvo",
      "colecao": true
     }
    ],
    "contextosExternos": [],
    "retorno": "booleano"
   },
   {
    "nome": "localEntregaIdentificado",
    "descricao": "Verdadeira quando está presente pelo menos um destes: o nome do local, o identificador do local, a data de entrega ou a morada.",
    "parametros": [
     {
      "nome": "nome",
      "tipo": "texto",
      "papel": "alvo"
     },
     {
      "nome": "identificador",
      "tipo": "texto",
      "papel": "alvo"
     },
     {
      "nome": "data",
      "tipo": "data",
      "papel": "alvo"
     },
     {
      "nome": "rua",
      "tipo": "texto",
      "papel": "alvo"
     }
    ],
    "contextosExternos": [],
    "retorno": "booleano"
   }
  ],
  "usm": [
   {
    "nome": "SujeitoPassivo",
    "descricao": "Pessoa singular ou coletiva identificada para efeitos fiscais, com o identificador de IVA precedido do código do país.",
    "propriedades": [
     {
      "nome": "nome",
      "tipo": "texto",
      "descricao": "Nome formal completo ou denominação social registada",
      "nomesAlternativos": [
       "RegistrationName",
       "Seller name",
       "Buyer name",
       "Payee name"
      ],
      "regras": [
       {
        "id": "RP-SP-NOME",
        "natureza": "plausibilidade",
        "restricao": {
         "propriedade": "nome",
         "operador": "LENGTH",
         "valor": [
          1,
          200
         ],
         "mensagem": "O nome tem de ter entre 1 e 200 caracteres."
        },
        "descricao": "SujeitoPassivo.nome tem entre 1 e 200 caracteres"
       }
      ]
     },
     {
      "nome": "nomeComercial",
      "tipo": "texto",
      "descricao": "Nome comercial pelo qual a parte é conhecida",
      "nomesAlternativos": [
       "PartyName",
       "trading name"
      ],
      "regras": [
       {
        "id": "RP-SP-NOMECOM",
        "natureza": "plausibilidade",
        "restricao": {
         "propriedade": "nomeComercial",
         "operador": "LENGTH",
         "valor": [
          1,
          200
         ],
         "mensagem": "O nome comercial tem de ter entre 1 e 200 caracteres."
        },
        "descricao": "SujeitoPassivo.nomeComercial tem entre 1 e 200 caracteres"
       }
      ]
     },
     {
      "nome": "identificador",
      "tipo": "texto",
      "descricao": "Identificador da parte segundo um esquema de identificação (ex.: GLN, identificação bancária)",
      "nomesAlternativos": [
       "PartyIdentification"
      ],
      "regras": [
       {
        "id": "RP-SP-IDENT",
        "natureza": "plausibilidade",
        "restricao": {
         "propriedade": "identificador",
         "operador": "LENGTH",
         "valor": [
          1,
          50
         ],
         "mensagem": "O identificador da parte tem de ter entre 1 e 50 caracteres."
        },
        "descricao": "SujeitoPassivo.identificador tem entre 1 e 50 caracteres"
       }
      ]
     },
     {
      "nome": "identificadorRegisto",
      "tipo": "texto",
      "descricao": "Identificador do registo comercial (conservatória) da parte",
      "nomesAlternativos": [
       "legal registration identifier"
      ],
      "regras": [
       {
        "id": "RP-SP-REGISTO",
        "natureza": "plausibilidade",
        "restricao": {
         "propriedade": "identificadorRegisto",
         "operador": "LENGTH",
         "valor": [
          1,
          200
         ],
         "mensagem": "O identificador de registo tem de ter entre 1 e 200 caracteres."
        },
        "descricao": "SujeitoPassivo.identificadorRegisto tem entre 1 e 200 caracteres"
       }
      ]
     },
     {
      "nome": "identificadorIva",
      "tipo": "texto",
      "descricao": "Número de identificação fiscal para efeitos de IVA, precedido do código ISO 3166-1 alfa-2 do país",
      "nomesAlternativos": [
       "VAT identifier",
       "PartyTaxScheme"
      ],
      "regras": [
       {
        "id": "RP-SP-IVA",
        "natureza": "plausibilidade",
        "restricao": {
         "propriedade": "identificadorIva",
         "operador": "PATTERN",
         "valor": "^[A-Z]{2}.{1,48}$",
         "mensagem": "O identificador de IVA tem de começar pelo código do país (duas letras) e ter no máximo 50 caracteres."
        },
        "descricao": "SujeitoPassivo.identificadorIva segue o padrão ^[A-Z]{2}.{1,48}$"
       }
      ]
     }
    ]
   },
   {
    "nome": "Morada",
    "descricao": "Morada postal: arruamento, código postal, localidade, freguesia e país.",
    "propriedades": [
     {
      "nome": "rua",
      "tipo": "texto",
      "descricao": "Arruamento e número de porta"
     },
     {
      "nome": "codigoPostal",
      "tipo": "texto",
      "descricao": "Código postal da morada",
      "nomesAlternativos": [
       "zipCode",
       "postalCode",
       "CP"
      ],
      "regras": [
       {
        "id": "RP-CP",
        "natureza": "plausibilidade",
        "descricao": "Morada.codigoPostal segue o padrão ^([1-9][0-9]{3}-[0-9]{3}|[0-5][0-9]{4}|[A-Z]{1,2}[0-9][0-9A-Z]? [0-9][A-Z]{2})$",
        "restricao": {
         "propriedade": "codigoPostal",
         "operador": "PATTERN",
         "valor": "^([1-9][0-9]{3}-[0-9]{3}|[0-5][0-9]{4}|[A-Z]{1,2}[0-9][0-9A-Z]? [0-9][A-Z]{2})$",
         "mensagem": "O código postal não tem nenhum dos formatos possíveis (português, espanhol ou britânico)."
        },
        "notas": "Plausibilidade: os formatos possíveis {PT, ES, GB}. Qual se aplica decide-se por inferência (RIR-CP-PT/ES/GB)."
       }
      ]
     },
     {
      "nome": "localidade",
      "tipo": "texto",
      "descricao": "Localidade da morada (em maiúsculas, sem acentos)"
     },
     {
      "nome": "freguesia",
      "tipo": "texto",
      "descricao": "Freguesia da morada (só para moradas em Lisboa)",
      "regras": [
       {
        "id": "RP-FREGUESIA",
        "natureza": "plausibilidade",
        "descricao": "Morada.freguesia ∈ {AJUDA, ALCANTARA, ALVALADE, AREEIRO, ARROIOS, AVENIDAS_NOVAS, BEATO, BELEM, BENFICA, CAMPO_DE_OURIQUE, CAMPOLIDE, CARNIDE, ESTRELA, LUMIAR, MARVILA, MISERICORDIA, OLIVAIS, PARQUE_DAS_NACOES, PENHA_DE_FRANCA, SANTA_CLARA, SANTA_MARIA_MAIOR, SANTO_ANTONIO, SAO_DOMINGOS_DE_BENFICA, SAO_VICENTE}",
        "restricao": {
         "propriedade": "freguesia",
         "operador": "IN",
         "valor": [
          "AJUDA",
          "ALCANTARA",
          "ALVALADE",
          "AREEIRO",
          "ARROIOS",
          "AVENIDAS_NOVAS",
          "BEATO",
          "BELEM",
          "BENFICA",
          "CAMPO_DE_OURIQUE",
          "CAMPOLIDE",
          "CARNIDE",
          "ESTRELA",
          "LUMIAR",
          "MARVILA",
          "MISERICORDIA",
          "OLIVAIS",
          "PARQUE_DAS_NACOES",
          "PENHA_DE_FRANCA",
          "SANTA_CLARA",
          "SANTA_MARIA_MAIOR",
          "SANTO_ANTONIO",
          "SAO_DOMINGOS_DE_BENFICA",
          "SAO_VICENTE"
         ],
         "mensagem": "A freguesia não pertence às freguesias de Lisboa conhecidas."
        }
       }
      ]
     },
     {
      "nome": "pais",
      "tipo": "texto",
      "descricao": "País da morada (código ISO de duas letras)",
      "nomesAlternativos": [
       "country",
       "countryCode"
      ],
      "regras": [
       {
        "id": "RP-PAIS",
        "natureza": "plausibilidade",
        "descricao": "Morada.pais ∈ {PT, ES, GB}",
        "restricao": {
         "propriedade": "pais",
         "operador": "IN",
         "valor": [
          "PT",
          "ES",
          "GB"
         ],
         "mensagem": "O país tem de ser PT, ES ou GB."
        }
       }
      ]
     }
    ],
    "regras": [
     {
      "id": "RIR-CP-PT",
      "natureza": "inferencia_restritiva",
      "descricao": "Se Morada.pais = PT → Morada.codigoPostal segue o padrão ^[1-9][0-9]{3}-[0-9]{3}$",
      "condicao": [
       {
        "propriedade": "pais",
        "operador": "EQUALS",
        "valor": "PT"
       }
      ],
      "restricao": {
       "propriedade": "codigoPostal",
       "operador": "PATTERN",
       "valor": "^[1-9][0-9]{3}-[0-9]{3}$",
       "mensagem": "O código postal português tem de ter o formato 0000-000, sem começar por zero."
      }
     },
     {
      "id": "RIR-CP-ES",
      "natureza": "inferencia_restritiva",
      "descricao": "Se Morada.pais = ES → Morada.codigoPostal segue o padrão ^[0-5][0-9]{4}$",
      "condicao": [
       {
        "propriedade": "pais",
        "operador": "EQUALS",
        "valor": "ES"
       }
      ],
      "restricao": {
       "propriedade": "codigoPostal",
       "operador": "PATTERN",
       "valor": "^[0-5][0-9]{4}$",
       "mensagem": "O código postal espanhol tem de ter cinco algarismos, a começar por 0 a 5."
      }
     },
     {
      "id": "RIR-CP-GB",
      "natureza": "inferencia_restritiva",
      "descricao": "Se Morada.pais = GB → Morada.codigoPostal segue o padrão ^[A-Z]{1,2}[0-9][0-9A-Z]? [0-9][A-Z]{2}$",
      "condicao": [
       {
        "propriedade": "pais",
        "operador": "EQUALS",
        "valor": "GB"
       }
      ],
      "restricao": {
       "propriedade": "codigoPostal",
       "operador": "PATTERN",
       "valor": "^[A-Z]{1,2}[0-9][0-9A-Z]? [0-9][A-Z]{2}$",
       "mensagem": "O código postal britânico tem de ter a forma de um postcode (ex.: SW1A 1AA)."
      }
     },
     {
      "id": "RIR-CP-LX-AJUDA",
      "natureza": "inferencia_restritiva",
      "descricao": "Se Morada.pais = PT e Morada.localidade = LISBOA e Morada.freguesia = AJUDA → Morada.codigoPostal segue o padrão ^(1300|1349)-[0-9]{3}$",
      "condicao": [
       {
        "propriedade": "pais",
        "operador": "EQUALS",
        "valor": "PT"
       },
       {
        "propriedade": "localidade",
        "operador": "EQUALS",
        "valor": "LISBOA"
       },
       {
        "propriedade": "freguesia",
        "operador": "EQUALS",
        "valor": "AJUDA"
       }
      ],
      "restricao": {
       "propriedade": "codigoPostal",
       "operador": "PATTERN",
       "valor": "^(1300|1349)-[0-9]{3}$",
       "mensagem": "O código postal de uma morada da freguesia Ajuda (Lisboa) começa por 1300 ou 1349."
      },
      "notas": "Mapeamento conhecido (códigos postais por freguesia de Lisboa) convertido em RIR: uma regra por freguesia. A vista de decisão sobre Morada.codigoPostal reconstrói a tabela."
     },
     {
      "id": "RIR-CP-LX-ALCANTARA",
      "natureza": "inferencia_restritiva",
      "descricao": "Se Morada.pais = PT e Morada.localidade = LISBOA e Morada.freguesia = ALCANTARA → Morada.codigoPostal segue o padrão ^(1300|1350)-[0-9]{3}$",
      "condicao": [
       {
        "propriedade": "pais",
        "operador": "EQUALS",
        "valor": "PT"
       },
       {
        "propriedade": "localidade",
        "operador": "EQUALS",
        "valor": "LISBOA"
       },
       {
        "propriedade": "freguesia",
        "operador": "EQUALS",
        "valor": "ALCANTARA"
       }
      ],
      "restricao": {
       "propriedade": "codigoPostal",
       "operador": "PATTERN",
       "valor": "^(1300|1350)-[0-9]{3}$",
       "mensagem": "O código postal de uma morada da freguesia Alcantara (Lisboa) começa por 1300 ou 1350."
      }
     },
     {
      "id": "RIR-CP-LX-ALVALADE",
      "natureza": "inferencia_restritiva",
      "descricao": "Se Morada.pais = PT e Morada.localidade = LISBOA e Morada.freguesia = ALVALADE → Morada.codigoPostal segue o padrão ^(1700|1749)-[0-9]{3}$",
      "condicao": [
       {
        "propriedade": "pais",
        "operador": "EQUALS",
        "valor": "PT"
       },
       {
        "propriedade": "localidade",
        "operador": "EQUALS",
        "valor": "LISBOA"
       },
       {
        "propriedade": "freguesia",
        "operador": "EQUALS",
        "valor": "ALVALADE"
       }
      ],
      "restricao": {
       "propriedade": "codigoPostal",
       "operador": "PATTERN",
       "valor": "^(1700|1749)-[0-9]{3}$",
       "mensagem": "O código postal de uma morada da freguesia Alvalade (Lisboa) começa por 1700 ou 1749."
      }
     },
     {
      "id": "RIR-CP-LX-AREEIRO",
      "natureza": "inferencia_restritiva",
      "descricao": "Se Morada.pais = PT e Morada.localidade = LISBOA e Morada.freguesia = AREEIRO → Morada.codigoPostal segue o padrão ^(1000|1049)-[0-9]{3}$",
      "condicao": [
       {
        "propriedade": "pais",
        "operador": "EQUALS",
        "valor": "PT"
       },
       {
        "propriedade": "localidade",
        "operador": "EQUALS",
        "valor": "LISBOA"
       },
       {
        "propriedade": "freguesia",
        "operador": "EQUALS",
        "valor": "AREEIRO"
       }
      ],
      "restricao": {
       "propriedade": "codigoPostal",
       "operador": "PATTERN",
       "valor": "^(1000|1049)-[0-9]{3}$",
       "mensagem": "O código postal de uma morada da freguesia Areeiro (Lisboa) começa por 1000 ou 1049."
      }
     },
     {
      "id": "RIR-CP-LX-ARROIOS",
      "natureza": "inferencia_restritiva",
      "descricao": "Se Morada.pais = PT e Morada.localidade = LISBOA e Morada.freguesia = ARROIOS → Morada.codigoPostal segue o padrão ^(1150|1169)-[0-9]{3}$",
      "condicao": [
       {
        "propriedade": "pais",
        "operador": "EQUALS",
        "valor": "PT"
       },
       {
        "propriedade": "localidade",
        "operador": "EQUALS",
        "valor": "LISBOA"
       },
       {
        "propriedade": "freguesia",
        "operador": "EQUALS",
        "valor": "ARROIOS"
       }
      ],
      "restricao": {
       "propriedade": "codigoPostal",
       "operador": "PATTERN",
       "valor": "^(1150|1169)-[0-9]{3}$",
       "mensagem": "O código postal de uma morada da freguesia Arroios (Lisboa) começa por 1150 ou 1169."
      }
     },
     {
      "id": "RIR-CP-LX-AVENIDAS-NOVAS",
      "natureza": "inferencia_restritiva",
      "descricao": "Se Morada.pais = PT e Morada.localidade = LISBOA e Morada.freguesia = AVENIDAS_NOVAS → Morada.codigoPostal segue o padrão ^(1050|1069)-[0-9]{3}$",
      "condicao": [
       {
        "propriedade": "pais",
        "operador": "EQUALS",
        "valor": "PT"
       },
       {
        "propriedade": "localidade",
        "operador": "EQUALS",
        "valor": "LISBOA"
       },
       {
        "propriedade": "freguesia",
        "operador": "EQUALS",
        "valor": "AVENIDAS_NOVAS"
       }
      ],
      "restricao": {
       "propriedade": "codigoPostal",
       "operador": "PATTERN",
       "valor": "^(1050|1069)-[0-9]{3}$",
       "mensagem": "O código postal de uma morada da freguesia Avenidas Novas (Lisboa) começa por 1050 ou 1069."
      }
     },
     {
      "id": "RIR-CP-LX-BEATO",
      "natureza": "inferencia_restritiva",
      "descricao": "Se Morada.pais = PT e Morada.localidade = LISBOA e Morada.freguesia = BEATO → Morada.codigoPostal segue o padrão ^(1900|1949)-[0-9]{3}$",
      "condicao": [
       {
        "propriedade": "pais",
        "operador": "EQUALS",
        "valor": "PT"
       },
       {
        "propriedade": "localidade",
        "operador": "EQUALS",
        "valor": "LISBOA"
       },
       {
        "propriedade": "freguesia",
        "operador": "EQUALS",
        "valor": "BEATO"
       }
      ],
      "restricao": {
       "propriedade": "codigoPostal",
       "operador": "PATTERN",
       "valor": "^(1900|1949)-[0-9]{3}$",
       "mensagem": "O código postal de uma morada da freguesia Beato (Lisboa) começa por 1900 ou 1949."
      }
     },
     {
      "id": "RIR-CP-LX-BELEM",
      "natureza": "inferencia_restritiva",
      "descricao": "Se Morada.pais = PT e Morada.localidade = LISBOA e Morada.freguesia = BELEM → Morada.codigoPostal segue o padrão ^(1400|1449)-[0-9]{3}$",
      "condicao": [
       {
        "propriedade": "pais",
        "operador": "EQUALS",
        "valor": "PT"
       },
       {
        "propriedade": "localidade",
        "operador": "EQUALS",
        "valor": "LISBOA"
       },
       {
        "propriedade": "freguesia",
        "operador": "EQUALS",
        "valor": "BELEM"
       }
      ],
      "restricao": {
       "propriedade": "codigoPostal",
       "operador": "PATTERN",
       "valor": "^(1400|1449)-[0-9]{3}$",
       "mensagem": "O código postal de uma morada da freguesia Belem (Lisboa) começa por 1400 ou 1449."
      }
     },
     {
      "id": "RIR-CP-LX-BENFICA",
      "natureza": "inferencia_restritiva",
      "descricao": "Se Morada.pais = PT e Morada.localidade = LISBOA e Morada.freguesia = BENFICA → Morada.codigoPostal segue o padrão ^(1500|1549)-[0-9]{3}$",
      "condicao": [
       {
        "propriedade": "pais",
        "operador": "EQUALS",
        "valor": "PT"
       },
       {
        "propriedade": "localidade",
        "operador": "EQUALS",
        "valor": "LISBOA"
       },
       {
        "propriedade": "freguesia",
        "operador": "EQUALS",
        "valor": "BENFICA"
       }
      ],
      "restricao": {
       "propriedade": "codigoPostal",
       "operador": "PATTERN",
       "valor": "^(1500|1549)-[0-9]{3}$",
       "mensagem": "O código postal de uma morada da freguesia Benfica (Lisboa) começa por 1500 ou 1549."
      }
     },
     {
      "id": "RIR-CP-LX-CAMPO-DE-OURIQUE",
      "natureza": "inferencia_restritiva",
      "descricao": "Se Morada.pais = PT e Morada.localidade = LISBOA e Morada.freguesia = CAMPO_DE_OURIQUE → Morada.codigoPostal segue o padrão ^(1250|1350)-[0-9]{3}$",
      "condicao": [
       {
        "propriedade": "pais",
        "operador": "EQUALS",
        "valor": "PT"
       },
       {
        "propriedade": "localidade",
        "operador": "EQUALS",
        "valor": "LISBOA"
       },
       {
        "propriedade": "freguesia",
        "operador": "EQUALS",
        "valor": "CAMPO_DE_OURIQUE"
       }
      ],
      "restricao": {
       "propriedade": "codigoPostal",
       "operador": "PATTERN",
       "valor": "^(1250|1350)-[0-9]{3}$",
       "mensagem": "O código postal de uma morada da freguesia Campo de Ourique (Lisboa) começa por 1250 ou 1350."
      }
     },
     {
      "id": "RIR-CP-LX-CAMPOLIDE",
      "natureza": "inferencia_restritiva",
      "descricao": "Se Morada.pais = PT e Morada.localidade = LISBOA e Morada.freguesia = CAMPOLIDE → Morada.codigoPostal segue o padrão ^(1070|1099)-[0-9]{3}$",
      "condicao": [
       {
        "propriedade": "pais",
        "operador": "EQUALS",
        "valor": "PT"
       },
       {
        "propriedade": "localidade",
        "operador": "EQUALS",
        "valor": "LISBOA"
       },
       {
        "propriedade": "freguesia",
        "operador": "EQUALS",
        "valor": "CAMPOLIDE"
       }
      ],
      "restricao": {
       "propriedade": "codigoPostal",
       "operador": "PATTERN",
       "valor": "^(1070|1099)-[0-9]{3}$",
       "mensagem": "O código postal de uma morada da freguesia Campolide (Lisboa) começa por 1070 ou 1099."
      }
     },
     {
      "id": "RIR-CP-LX-CARNIDE",
      "natureza": "inferencia_restritiva",
      "descricao": "Se Morada.pais = PT e Morada.localidade = LISBOA e Morada.freguesia = CARNIDE → Morada.codigoPostal segue o padrão ^(1600|1649)-[0-9]{3}$",
      "condicao": [
       {
        "propriedade": "pais",
        "operador": "EQUALS",
        "valor": "PT"
       },
       {
        "propriedade": "localidade",
        "operador": "EQUALS",
        "valor": "LISBOA"
       },
       {
        "propriedade": "freguesia",
        "operador": "EQUALS",
        "valor": "CARNIDE"
       }
      ],
      "restricao": {
       "propriedade": "codigoPostal",
       "operador": "PATTERN",
       "valor": "^(1600|1649)-[0-9]{3}$",
       "mensagem": "O código postal de uma morada da freguesia Carnide (Lisboa) começa por 1600 ou 1649."
      }
     },
     {
      "id": "RIR-CP-LX-ESTRELA",
      "natureza": "inferencia_restritiva",
      "descricao": "Se Morada.pais = PT e Morada.localidade = LISBOA e Morada.freguesia = ESTRELA → Morada.codigoPostal segue o padrão ^(1200|1249)-[0-9]{3}$",
      "condicao": [
       {
        "propriedade": "pais",
        "operador": "EQUALS",
        "valor": "PT"
       },
       {
        "propriedade": "localidade",
        "operador": "EQUALS",
        "valor": "LISBOA"
       },
       {
        "propriedade": "freguesia",
        "operador": "EQUALS",
        "valor": "ESTRELA"
       }
      ],
      "restricao": {
       "propriedade": "codigoPostal",
       "operador": "PATTERN",
       "valor": "^(1200|1249)-[0-9]{3}$",
       "mensagem": "O código postal de uma morada da freguesia Estrela (Lisboa) começa por 1200 ou 1249."
      }
     },
     {
      "id": "RIR-CP-LX-LUMIAR",
      "natureza": "inferencia_restritiva",
      "descricao": "Se Morada.pais = PT e Morada.localidade = LISBOA e Morada.freguesia = LUMIAR → Morada.codigoPostal segue o padrão ^(1600|1750)-[0-9]{3}$",
      "condicao": [
       {
        "propriedade": "pais",
        "operador": "EQUALS",
        "valor": "PT"
       },
       {
        "propriedade": "localidade",
        "operador": "EQUALS",
        "valor": "LISBOA"
       },
       {
        "propriedade": "freguesia",
        "operador": "EQUALS",
        "valor": "LUMIAR"
       }
      ],
      "restricao": {
       "propriedade": "codigoPostal",
       "operador": "PATTERN",
       "valor": "^(1600|1750)-[0-9]{3}$",
       "mensagem": "O código postal de uma morada da freguesia Lumiar (Lisboa) começa por 1600 ou 1750."
      }
     },
     {
      "id": "RIR-CP-LX-MARVILA",
      "natureza": "inferencia_restritiva",
      "descricao": "Se Morada.pais = PT e Morada.localidade = LISBOA e Morada.freguesia = MARVILA → Morada.codigoPostal segue o padrão ^(1800|1949)-[0-9]{3}$",
      "condicao": [
       {
        "propriedade": "pais",
        "operador": "EQUALS",
        "valor": "PT"
       },
       {
        "propriedade": "localidade",
        "operador": "EQUALS",
        "valor": "LISBOA"
       },
       {
        "propriedade": "freguesia",
        "operador": "EQUALS",
        "valor": "MARVILA"
       }
      ],
      "restricao": {
       "propriedade": "codigoPostal",
       "operador": "PATTERN",
       "valor": "^(1800|1949)-[0-9]{3}$",
       "mensagem": "O código postal de uma morada da freguesia Marvila (Lisboa) começa por 1800 ou 1949."
      }
     },
     {
      "id": "RIR-CP-LX-MISERICORDIA",
      "natureza": "inferencia_restritiva",
      "descricao": "Se Morada.pais = PT e Morada.localidade = LISBOA e Morada.freguesia = MISERICORDIA → Morada.codigoPostal segue o padrão ^(1200|1249)-[0-9]{3}$",
      "condicao": [
       {
        "propriedade": "pais",
        "operador": "EQUALS",
        "valor": "PT"
       },
       {
        "propriedade": "localidade",
        "operador": "EQUALS",
        "valor": "LISBOA"
       },
       {
        "propriedade": "freguesia",
        "operador": "EQUALS",
        "valor": "MISERICORDIA"
       }
      ],
      "restricao": {
       "propriedade": "codigoPostal",
       "operador": "PATTERN",
       "valor": "^(1200|1249)-[0-9]{3}$",
       "mensagem": "O código postal de uma morada da freguesia Misericordia (Lisboa) começa por 1200 ou 1249."
      }
     },
     {
      "id": "RIR-CP-LX-OLIVAIS",
      "natureza": "inferencia_restritiva",
      "descricao": "Se Morada.pais = PT e Morada.localidade = LISBOA e Morada.freguesia = OLIVAIS → Morada.codigoPostal segue o padrão ^(1800|1885)-[0-9]{3}$",
      "condicao": [
       {
        "propriedade": "pais",
        "operador": "EQUALS",
        "valor": "PT"
       },
       {
        "propriedade": "localidade",
        "operador": "EQUALS",
        "valor": "LISBOA"
       },
       {
        "propriedade": "freguesia",
        "operador": "EQUALS",
        "valor": "OLIVAIS"
       }
      ],
      "restricao": {
       "propriedade": "codigoPostal",
       "operador": "PATTERN",
       "valor": "^(1800|1885)-[0-9]{3}$",
       "mensagem": "O código postal de uma morada da freguesia Olivais (Lisboa) começa por 1800 ou 1885."
      }
     },
     {
      "id": "RIR-CP-LX-PARQUE-DAS-NACOES",
      "natureza": "inferencia_restritiva",
      "descricao": "Se Morada.pais = PT e Morada.localidade = LISBOA e Morada.freguesia = PARQUE_DAS_NACOES → Morada.codigoPostal segue o padrão ^(1990|1998)-[0-9]{3}$",
      "condicao": [
       {
        "propriedade": "pais",
        "operador": "EQUALS",
        "valor": "PT"
       },
       {
        "propriedade": "localidade",
        "operador": "EQUALS",
        "valor": "LISBOA"
       },
       {
        "propriedade": "freguesia",
        "operador": "EQUALS",
        "valor": "PARQUE_DAS_NACOES"
       }
      ],
      "restricao": {
       "propriedade": "codigoPostal",
       "operador": "PATTERN",
       "valor": "^(1990|1998)-[0-9]{3}$",
       "mensagem": "O código postal de uma morada da freguesia Parque das Nacoes (Lisboa) começa por 1990 ou 1998."
      }
     },
     {
      "id": "RIR-CP-LX-PENHA-DE-FRANCA",
      "natureza": "inferencia_restritiva",
      "descricao": "Se Morada.pais = PT e Morada.localidade = LISBOA e Morada.freguesia = PENHA_DE_FRANCA → Morada.codigoPostal segue o padrão ^(1170|1199)-[0-9]{3}$",
      "condicao": [
       {
        "propriedade": "pais",
        "operador": "EQUALS",
        "valor": "PT"
       },
       {
        "propriedade": "localidade",
        "operador": "EQUALS",
        "valor": "LISBOA"
       },
       {
        "propriedade": "freguesia",
        "operador": "EQUALS",
        "valor": "PENHA_DE_FRANCA"
       }
      ],
      "restricao": {
       "propriedade": "codigoPostal",
       "operador": "PATTERN",
       "valor": "^(1170|1199)-[0-9]{3}$",
       "mensagem": "O código postal de uma morada da freguesia Penha de Franca (Lisboa) começa por 1170 ou 1199."
      }
     },
     {
      "id": "RIR-CP-LX-SANTA-CLARA",
      "natureza": "inferencia_restritiva",
      "descricao": "Se Morada.pais = PT e Morada.localidade = LISBOA e Morada.freguesia = SANTA_CLARA → Morada.codigoPostal segue o padrão ^(1750|1769)-[0-9]{3}$",
      "condicao": [
       {
        "propriedade": "pais",
        "operador": "EQUALS",
        "valor": "PT"
       },
       {
        "propriedade": "localidade",
        "operador": "EQUALS",
        "valor": "LISBOA"
       },
       {
        "propriedade": "freguesia",
        "operador": "EQUALS",
        "valor": "SANTA_CLARA"
       }
      ],
      "restricao": {
       "propriedade": "codigoPostal",
       "operador": "PATTERN",
       "valor": "^(1750|1769)-[0-9]{3}$",
       "mensagem": "O código postal de uma morada da freguesia Santa Clara (Lisboa) começa por 1750 ou 1769."
      }
     },
     {
      "id": "RIR-CP-LX-SANTA-MARIA-MAIOR",
      "natureza": "inferencia_restritiva",
      "descricao": "Se Morada.pais = PT e Morada.localidade = LISBOA e Morada.freguesia = SANTA_MARIA_MAIOR → Morada.codigoPostal segue o padrão ^(1100|1149)-[0-9]{3}$",
      "condicao": [
       {
        "propriedade": "pais",
        "operador": "EQUALS",
        "valor": "PT"
       },
       {
        "propriedade": "localidade",
        "operador": "EQUALS",
        "valor": "LISBOA"
       },
       {
        "propriedade": "freguesia",
        "operador": "EQUALS",
        "valor": "SANTA_MARIA_MAIOR"
       }
      ],
      "restricao": {
       "propriedade": "codigoPostal",
       "operador": "PATTERN",
       "valor": "^(1100|1149)-[0-9]{3}$",
       "mensagem": "O código postal de uma morada da freguesia Santa Maria Maior (Lisboa) começa por 1100 ou 1149."
      }
     },
     {
      "id": "RIR-CP-LX-SANTO-ANTONIO",
      "natureza": "inferencia_restritiva",
      "descricao": "Se Morada.pais = PT e Morada.localidade = LISBOA e Morada.freguesia = SANTO_ANTONIO → Morada.codigoPostal segue o padrão ^(1250|1269)-[0-9]{3}$",
      "condicao": [
       {
        "propriedade": "pais",
        "operador": "EQUALS",
        "valor": "PT"
       },
       {
        "propriedade": "localidade",
        "operador": "EQUALS",
        "valor": "LISBOA"
       },
       {
        "propriedade": "freguesia",
        "operador": "EQUALS",
        "valor": "SANTO_ANTONIO"
       }
      ],
      "restricao": {
       "propriedade": "codigoPostal",
       "operador": "PATTERN",
       "valor": "^(1250|1269)-[0-9]{3}$",
       "mensagem": "O código postal de uma morada da freguesia Santo Antonio (Lisboa) começa por 1250 ou 1269."
      }
     },
     {
      "id": "RIR-CP-LX-SAO-DOMINGOS-DE-BENFICA",
      "natureza": "inferencia_restritiva",
      "descricao": "Se Morada.pais = PT e Morada.localidade = LISBOA e Morada.freguesia = SAO_DOMINGOS_DE_BENFICA → Morada.codigoPostal segue o padrão ^(1500|1600)-[0-9]{3}$",
      "condicao": [
       {
        "propriedade": "pais",
        "operador": "EQUALS",
        "valor": "PT"
       },
       {
        "propriedade": "localidade",
        "operador": "EQUALS",
        "valor": "LISBOA"
       },
       {
        "propriedade": "freguesia",
        "operador": "EQUALS",
        "valor": "SAO_DOMINGOS_DE_BENFICA"
       }
      ],
      "restricao": {
       "propriedade": "codigoPostal",
       "operador": "PATTERN",
       "valor": "^(1500|1600)-[0-9]{3}$",
       "mensagem": "O código postal de uma morada da freguesia Sao Domingos de Benfica (Lisboa) começa por 1500 ou 1600."
      }
     },
     {
      "id": "RIR-CP-LX-SAO-VICENTE",
      "natureza": "inferencia_restritiva",
      "descricao": "Se Morada.pais = PT e Morada.localidade = LISBOA e Morada.freguesia = SAO_VICENTE → Morada.codigoPostal segue o padrão ^(1100|1170)-[0-9]{3}$",
      "condicao": [
       {
        "propriedade": "pais",
        "operador": "EQUALS",
        "valor": "PT"
       },
       {
        "propriedade": "localidade",
        "operador": "EQUALS",
        "valor": "LISBOA"
       },
       {
        "propriedade": "freguesia",
        "operador": "EQUALS",
        "valor": "SAO_VICENTE"
       }
      ],
      "restricao": {
       "propriedade": "codigoPostal",
       "operador": "PATTERN",
       "valor": "^(1100|1170)-[0-9]{3}$",
       "mensagem": "O código postal de uma morada da freguesia Sao Vicente (Lisboa) começa por 1100 ou 1170."
      }
     }
    ]
   },
   {
    "nome": "ComplementoMorada",
    "descricao": "Linhas complementares de uma morada postal: linha adicional, terceira linha e região ou província.",
    "notas": "Criado para não alterar o USM Morada reutilizado, que não tem estas linhas.",
    "propriedades": [
     {
      "nome": "linha2",
      "tipo": "texto",
      "descricao": "Segunda linha da morada",
      "nomesAlternativos": [
       "AdditionalStreetName"
      ],
      "regras": [
       {
        "id": "RP-CMOR-LINHA2",
        "natureza": "plausibilidade",
        "restricao": {
         "propriedade": "linha2",
         "operador": "LENGTH",
         "valor": [
          1,
          200
         ],
         "mensagem": "A segunda linha da morada tem de ter entre 1 e 200 caracteres."
        },
        "descricao": "ComplementoMorada.linha2 tem entre 1 e 200 caracteres"
       }
      ]
     },
     {
      "nome": "linha3",
      "tipo": "texto",
      "descricao": "Linha de endereço adicional, que complementa a linha principal",
      "nomesAlternativos": [
       "AddressLine"
      ],
      "regras": [
       {
        "id": "RP-CMOR-LINHA3",
        "natureza": "plausibilidade",
        "restricao": {
         "propriedade": "linha3",
         "operador": "LENGTH",
         "valor": [
          1,
          200
         ],
         "mensagem": "A linha adicional da morada tem de ter entre 1 e 200 caracteres."
        },
        "descricao": "ComplementoMorada.linha3 tem entre 1 e 200 caracteres"
       }
      ]
     },
     {
      "nome": "regiao",
      "tipo": "texto",
      "descricao": "Região ou província da morada",
      "nomesAlternativos": [
       "CountrySubentity"
      ],
      "regras": [
       {
        "id": "RP-CMOR-REGIAO",
        "natureza": "plausibilidade",
        "restricao": {
         "propriedade": "regiao",
         "operador": "LENGTH",
         "valor": [
          1,
          200
         ],
         "mensagem": "A região da morada tem de ter entre 1 e 200 caracteres."
        },
        "descricao": "ComplementoMorada.regiao tem entre 1 e 200 caracteres"
       }
      ]
     }
    ]
   },
   {
    "nome": "Contacto",
    "descricao": "Contacto eletrónico de uma entidade.",
    "propriedades": [
     {
      "nome": "email",
      "tipo": "texto",
      "descricao": "Endereço de correio eletrónico",
      "nomesAlternativos": [
       "eMail",
       "correioEletronico"
      ],
      "regras": [
       {
        "id": "RP-EMAIL",
        "natureza": "plausibilidade",
        "descricao": "Contacto.email segue o padrão ^[a-z0-9._-]+@[a-z0-9-]+(\\.[a-z0-9-]+)+$",
        "restricao": {
         "propriedade": "email",
         "operador": "PATTERN",
         "valor": "^[a-z0-9._-]+@[a-z0-9-]+(\\.[a-z0-9-]+)+$",
         "mensagem": "O email tem de ter uma parte local e um domínio com pelo menos um ponto, sem espaços nem maiúsculas."
        }
       }
      ]
     }
    ]
   },
   {
    "nome": "ContactoTelefonico",
    "descricao": "Contactos telefónicos de uma pessoa ou entidade: telefone e telemóvel.",
    "propriedades": [
     {
      "nome": "telefone",
      "tipo": "texto",
      "descricao": "Número de telefone (rede fixa ou geral)",
      "nomesAlternativos": [
       "Telephone",
       "fixePhoneNumber"
      ],
      "regras": [
       {
        "id": "RP-TELEFONE",
        "natureza": "plausibilidade",
        "restricao": {
         "propriedade": "telefone",
         "operador": "LENGTH",
         "valor": [
          1,
          200
         ],
         "mensagem": "O telefone tem de ter entre 1 e 200 caracteres."
        },
        "descricao": "ContactoTelefonico.telefone tem entre 1 e 200 caracteres"
       }
      ]
     },
     {
      "nome": "telemovel",
      "tipo": "texto",
      "descricao": "Número de telemóvel",
      "nomesAlternativos": [
       "phoneNumber",
       "mobile"
      ]
     }
    ]
   },
   {
    "nome": "ReferenciaDocumento",
    "descricao": "Referência a outro documento: o número atribuído pelo emissor e a data de emissão.",
    "propriedades": [
     {
      "nome": "numero",
      "tipo": "texto",
      "descricao": "Número de referência do documento referido",
      "nomesAlternativos": [
       "Preceding Invoice reference",
       "DocumentReference"
      ],
      "regras": [
       {
        "id": "RP-REFDOC-NUMERO",
        "natureza": "plausibilidade",
        "restricao": {
         "propriedade": "numero",
         "operador": "LENGTH",
         "valor": [
          1,
          50
         ],
         "mensagem": "O número do documento referido tem de ter entre 1 e 50 caracteres."
        },
        "descricao": "ReferenciaDocumento.numero tem entre 1 e 50 caracteres"
       }
      ]
     },
     {
      "nome": "dataEmissao",
      "tipo": "data",
      "descricao": "Data de emissão do documento referido"
     }
    ]
   },
   {
    "nome": "Periodo",
    "descricao": "Intervalo temporal definido por uma data de início e uma data de fim.",
    "propriedades": [
     {
      "nome": "dataInicio",
      "tipo": "data",
      "descricao": "Data em que o período começa",
      "nomesAlternativos": [
       "StartDate"
      ]
     },
     {
      "nome": "dataFim",
      "tipo": "data",
      "descricao": "Data em que o período acaba",
      "nomesAlternativos": [
       "EndDate"
      ]
     }
    ],
    "regras": [
     {
      "id": "RP-PERIODO-ORDEM",
      "natureza": "plausibilidade",
      "restricao": {
       "operador": "FUNCTION",
       "chamada": {
        "funcao": "naoAnteriorA",
        "argumentos": [
         {
          "caminho": "dataFim"
         },
         {
          "caminho": "dataInicio"
         }
        ]
       },
       "mensagem": "A data de fim do período não pode ser anterior à data de início."
      },
      "descricao": "naoAnteriorA(Periodo.dataFim, Periodo.dataInicio)"
     },
     {
      "id": "RP-PERIODO-DATA",
      "natureza": "plausibilidade",
      "restricao": {
       "operador": "FUNCTION",
       "chamada": {
        "funcao": "algumPresente",
        "argumentos": [
         {
          "caminho": "dataInicio"
         },
         {
          "caminho": "dataFim"
         }
        ]
       },
       "mensagem": "Um período tem de indicar a data de início, a data de fim ou ambas."
      },
      "descricao": "algumPresente(Periodo.dataInicio, Periodo.dataFim)"
     }
    ]
   },
   {
    "nome": "ContaBancaria",
    "descricao": "Conta bancária para transferência: IBAN, nome da conta e código da instituição (BIC/SWIFT).",
    "propriedades": [
     {
      "nome": "iban",
      "tipo": "texto",
      "descricao": "Identificador da conta (código IBAN)",
      "nomesAlternativos": [
       "Payment account identifier",
       "IBAN"
      ],
      "regras": [
       {
        "id": "RP-CONTA-IBAN",
        "natureza": "plausibilidade",
        "restricao": {
         "propriedade": "iban",
         "operador": "LENGTH",
         "valor": [
          1,
          50
         ],
         "mensagem": "O IBAN tem de ter entre 1 e 50 caracteres."
        },
        "descricao": "ContaBancaria.iban tem entre 1 e 50 caracteres"
       }
      ]
     },
     {
      "nome": "nomeConta",
      "tipo": "texto",
      "descricao": "Nome da conta para a qual o pagamento deve ser feito",
      "nomesAlternativos": [
       "Payment account name"
      ],
      "regras": [
       {
        "id": "RP-CONTA-NOME",
        "natureza": "plausibilidade",
        "restricao": {
         "propriedade": "nomeConta",
         "operador": "LENGTH",
         "valor": [
          1,
          200
         ],
         "mensagem": "O nome da conta tem de ter entre 1 e 200 caracteres."
        },
        "descricao": "ContaBancaria.nomeConta tem entre 1 e 200 caracteres"
       }
      ]
     },
     {
      "nome": "bic",
      "tipo": "texto",
      "descricao": "Código da instituição bancária (BIC/SWIFT)",
      "nomesAlternativos": [
       "Payment service provider identifier",
       "SWIFT"
      ],
      "regras": [
       {
        "id": "RP-CONTA-BIC",
        "natureza": "plausibilidade",
        "restricao": {
         "propriedade": "bic",
         "operador": "LENGTH",
         "valor": [
          1,
          50
         ],
         "mensagem": "O código da instituição bancária tem de ter entre 1 e 50 caracteres."
        },
        "descricao": "ContaBancaria.bic tem entre 1 e 50 caracteres"
       }
      ]
     }
    ]
   },
   {
    "nome": "CartaoPagamento",
    "descricao": "Cartão usado no pagamento: número principal da conta (PAN) e titular.",
    "propriedades": [
     {
      "nome": "numeroConta",
      "tipo": "texto",
      "descricao": "Número principal da conta do cartão (PAN)",
      "nomesAlternativos": [
       "Payment card primary account number",
       "PAN"
      ],
      "regras": [
       {
        "id": "RP-CARTAO-PAN",
        "natureza": "plausibilidade",
        "restricao": {
         "propriedade": "numeroConta",
         "operador": "LENGTH",
         "valor": [
          1,
          200
         ],
         "mensagem": "O número do cartão tem de ter entre 1 e 200 caracteres."
        },
        "descricao": "CartaoPagamento.numeroConta tem entre 1 e 200 caracteres"
       }
      ]
     },
     {
      "nome": "titular",
      "tipo": "texto",
      "descricao": "Nome do titular do cartão",
      "nomesAlternativos": [
       "HolderName"
      ],
      "regras": [
       {
        "id": "RP-CARTAO-TITULAR",
        "natureza": "plausibilidade",
        "restricao": {
         "propriedade": "titular",
         "operador": "LENGTH",
         "valor": [
          1,
          200
         ],
         "mensagem": "O nome do titular do cartão tem de ter entre 1 e 200 caracteres."
        },
        "descricao": "CartaoPagamento.titular tem entre 1 e 200 caracteres"
       }
      ]
     }
    ]
   },
   {
    "nome": "DebitoDireto",
    "descricao": "Mandato de débito direto: referência do mandato, identificador do credor e conta a debitar.",
    "propriedades": [
     {
      "nome": "referenciaMandato",
      "tipo": "texto",
      "descricao": "Identificador único do mandato de débito direto atribuído pelo beneficiário",
      "nomesAlternativos": [
       "Mandate reference identifier"
      ],
      "regras": [
       {
        "id": "RP-DD-MANDATO",
        "natureza": "plausibilidade",
        "restricao": {
         "propriedade": "referenciaMandato",
         "operador": "LENGTH",
         "valor": [
          1,
          50
         ],
         "mensagem": "A referência do mandato tem de ter entre 1 e 50 caracteres."
        },
        "descricao": "DebitoDireto.referenciaMandato tem entre 1 e 50 caracteres"
       }
      ]
     },
     {
      "nome": "identificadorCredor",
      "tipo": "texto",
      "descricao": "Identificador do credor atribuído pelo banco",
      "nomesAlternativos": [
       "Bank assigned creditor identifier"
      ]
     },
     {
      "nome": "contaDebitada",
      "tipo": "texto",
      "descricao": "Conta a debitar pelo débito direto",
      "nomesAlternativos": [
       "Debited account identifier"
      ],
      "regras": [
       {
        "id": "RP-DD-CONTA",
        "natureza": "plausibilidade",
        "restricao": {
         "propriedade": "contaDebitada",
         "operador": "LENGTH",
         "valor": [
          1,
          50
         ],
         "mensagem": "A conta a debitar tem de ter entre 1 e 50 caracteres."
        },
        "descricao": "DebitoDireto.contaDebitada tem entre 1 e 50 caracteres"
       }
      ]
     }
    ]
   },
   {
    "nome": "DescontoEncargo",
    "descricao": "Desconto ou encargo sobre um montante: valor, base, percentagem e motivo (o papel da composição diz se é desconto ou encargo).",
    "propriedades": [
     {
      "nome": "montante",
      "tipo": "decimal",
      "descricao": "Montante do desconto ou do encargo, sem impostos",
      "nomesAlternativos": [
       "Amount",
       "allowance amount",
       "charge amount"
      ],
      "regras": [
       {
        "id": "RP-DE-MONTANTE",
        "natureza": "plausibilidade",
        "restricao": {
         "propriedade": "montante",
         "operador": "GTE",
         "valor": 0,
         "mensagem": "O montante do desconto ou do encargo não pode ser negativo."
        },
        "descricao": "DescontoEncargo.montante ≥ 0"
       }
      ]
     },
     {
      "nome": "montanteBase",
      "tipo": "decimal",
      "descricao": "Montante base sobre o qual incide a percentagem",
      "nomesAlternativos": [
       "BaseAmount"
      ],
      "regras": [
       {
        "id": "RP-DE-BASE",
        "natureza": "plausibilidade",
        "restricao": {
         "propriedade": "montanteBase",
         "operador": "GTE",
         "valor": 0,
         "mensagem": "O montante base não pode ser negativo."
        },
        "descricao": "DescontoEncargo.montanteBase ≥ 0"
       }
      ]
     },
     {
      "nome": "percentagem",
      "tipo": "decimal",
      "descricao": "Percentagem aplicada ao montante base",
      "nomesAlternativos": [
       "MultiplierFactorNumeric"
      ],
      "regras": [
       {
        "id": "RP-DE-PERC",
        "natureza": "plausibilidade",
        "restricao": {
         "propriedade": "percentagem",
         "operador": "RANGE",
         "valor": [
          0,
          100
         ],
         "mensagem": "A percentagem tem de estar entre 0 e 100."
        },
        "descricao": "DescontoEncargo.percentagem entre 0 e 100"
       }
      ]
     },
     {
      "nome": "motivo",
      "tipo": "texto",
      "descricao": "Descrição em texto do motivo do desconto ou do encargo",
      "nomesAlternativos": [
       "AllowanceChargeReason"
      ],
      "regras": [
       {
        "id": "RP-DE-MOTIVO",
        "natureza": "plausibilidade",
        "restricao": {
         "propriedade": "motivo",
         "operador": "LENGTH",
         "valor": [
          1,
          200
         ],
         "mensagem": "O motivo tem de ter entre 1 e 200 caracteres."
        },
        "descricao": "DescontoEncargo.motivo tem entre 1 e 200 caracteres"
       }
      ]
     },
     {
      "nome": "codigoMotivo",
      "tipo": "texto",
      "descricao": "Código do motivo (UNCL 5189 para descontos, UNCL 7161 para encargos)",
      "nomesAlternativos": [
       "AllowanceChargeReasonCode"
      ],
      "regras": [
       {
        "id": "RP-DE-CODMOTIVO",
        "natureza": "plausibilidade",
        "restricao": {
         "propriedade": "codigoMotivo",
         "operador": "PATTERN",
         "valor": "^[A-Z0-9]{1,3}$",
         "mensagem": "O código do motivo tem de ser um código UNCL 5189 ou UNCL 7161 (1 a 3 letras ou algarismos)."
        },
        "descricao": "DescontoEncargo.codigoMotivo segue o padrão ^[A-Z0-9]{1,3}$"
       }
      ]
     }
    ],
    "regras": [
     {
      "id": "RP-DE-JUSTIFICADO",
      "natureza": "plausibilidade",
      "restricao": {
       "operador": "FUNCTION",
       "chamada": {
        "funcao": "algumPresente",
        "argumentos": [
         {
          "caminho": "motivo"
         },
         {
          "caminho": "codigoMotivo"
         }
        ]
       },
       "mensagem": "Um desconto ou encargo tem de indicar o motivo, o código do motivo ou ambos."
      },
      "descricao": "algumPresente(DescontoEncargo.motivo, DescontoEncargo.codigoMotivo)"
     },
     {
      "id": "RP-DE-CALCULO",
      "natureza": "plausibilidade",
      "restricao": {
       "operador": "FUNCTION",
       "chamada": {
        "funcao": "produtoPercentualIgualA",
        "argumentos": [
         {
          "caminho": "montanteBase"
         },
         {
          "caminho": "percentagem"
         },
         {
          "caminho": "montante"
         },
         {
          "literal": 1.0
         }
        ]
       },
       "mensagem": "O montante tem de ser igual ao montante base vezes a percentagem, com uma tolerância de 1,00 €."
      },
      "descricao": "produtoPercentualIgualA(DescontoEncargo.montanteBase, DescontoEncargo.percentagem, DescontoEncargo.montante, 1)"
     }
    ]
   },
   {
    "nome": "CategoriaIva",
    "descricao": "Categoria de IVA aplicada: código da categoria, taxa e motivo de isenção.",
    "propriedades": [
     {
      "nome": "codigoCategoria",
      "tipo": "texto",
      "descricao": "Código da categoria de IVA (UN/ECE 5305 com os códigos portugueses NOR, INT, RED, ISE, OUT)",
      "nomesAlternativos": [
       "VAT category code",
       "ClassifiedTaxCategory",
       "TaxCategory"
      ],
      "regras": [
       {
        "id": "RP-IVA-CATEGORIA",
        "natureza": "plausibilidade",
        "restricao": {
         "propriedade": "codigoCategoria",
         "operador": "IN",
         "valor": [
          "AA",
          "S",
          "E",
          "RED",
          "INT",
          "NOR",
          "ISE",
          "OUT",
          "NA",
          "Z",
          "AE",
          "IC",
          "G",
          "O"
         ],
         "mensagem": "O código da categoria de IVA tem de ser um destes: AA, S, E, RED, INT, NOR, ISE, OUT, NA, Z, AE, IC, G, O."
        },
        "descricao": "CategoriaIva.codigoCategoria ∈ {AA, S, E, RED, INT, NOR, ISE, OUT, NA, Z, AE, IC, G, O}"
       }
      ]
     },
     {
      "nome": "taxa",
      "tipo": "decimal",
      "descricao": "Taxa de IVA, em percentagem",
      "nomesAlternativos": [
       "VAT rate",
       "Percent"
      ],
      "regras": [
       {
        "id": "RP-IVA-TAXA",
        "natureza": "plausibilidade",
        "restricao": {
         "propriedade": "taxa",
         "operador": "RANGE",
         "valor": [
          0,
          100
         ],
         "mensagem": "A taxa de IVA tem de estar entre 0 e 100."
        },
        "descricao": "CategoriaIva.taxa entre 0 e 100"
       }
      ]
     },
     {
      "nome": "motivoIsencao",
      "tipo": "texto",
      "descricao": "Descrição em texto do motivo de isenção de IVA",
      "nomesAlternativos": [
       "VAT exemption reason text",
       "TaxExemptionReason"
      ],
      "regras": [
       {
        "id": "RP-IVA-MOTIVO",
        "natureza": "plausibilidade",
        "restricao": {
         "propriedade": "motivoIsencao",
         "operador": "LENGTH",
         "valor": [
          1,
          200
         ],
         "mensagem": "O motivo de isenção tem de ter entre 1 e 200 caracteres."
        },
        "descricao": "CategoriaIva.motivoIsencao tem entre 1 e 200 caracteres"
       }
      ]
     },
     {
      "nome": "codigoMotivoIsencao",
      "tipo": "texto",
      "descricao": "Código do motivo de isenção de IVA",
      "nomesAlternativos": [
       "VAT exemption reason code",
       "TaxExemptionReasonCode"
      ],
      "regras": [
       {
        "id": "RP-IVA-CODMOTIVO",
        "natureza": "plausibilidade",
        "restricao": {
         "propriedade": "codigoMotivoIsencao",
         "operador": "LENGTH",
         "valor": [
          1,
          5
         ],
         "mensagem": "O código do motivo de isenção tem de ter entre 1 e 5 caracteres."
        },
        "descricao": "CategoriaIva.codigoMotivoIsencao tem entre 1 e 5 caracteres"
       }
      ]
     }
    ],
    "regras": [
     {
      "id": "RIR-IVA-TAXA-ISENTA",
      "natureza": "inferencia_restritiva",
      "condicao": [
       {
        "propriedade": "codigoCategoria",
        "operador": "IN",
        "valor": [
         "E",
         "ISE"
        ]
       }
      ],
      "restricao": {
       "propriedade": "taxa",
       "operador": "EQUALS",
       "valor": 0,
       "mensagem": "Numa categoria isenta de IVA (E, ISE), a taxa tem de ser 0."
      },
      "descricao": "Se CategoriaIva.codigoCategoria ∈ {E, ISE} → CategoriaIva.taxa = 0"
     },
     {
      "id": "RIR-IVA-TAXA-POSITIVA",
      "natureza": "inferencia_restritiva",
      "condicao": [
       {
        "propriedade": "codigoCategoria",
        "operador": "IN",
        "valor": [
         "S",
         "NOR",
         "AA",
         "RED",
         "INT"
        ]
       }
      ],
      "restricao": {
       "propriedade": "taxa",
       "operador": "GT",
       "valor": 0,
       "mensagem": "Numa categoria de taxa normal, intermédia ou reduzida, a taxa de IVA tem de ser maior do que zero."
      },
      "descricao": "Se CategoriaIva.codigoCategoria ∈ {S, NOR, AA, RED, INT} → CategoriaIva.taxa > 0"
     }
    ]
   },
   {
    "nome": "Preco",
    "descricao": "Preço de um bem ou serviço: preço líquido, desconto, preço bruto e quantidade base do preço.",
    "propriedades": [
     {
      "nome": "precoLiquido",
      "tipo": "decimal",
      "descricao": "Preço do item depois do desconto, por quantidade base",
      "nomesAlternativos": [
       "Item net price",
       "PriceAmount"
      ],
      "regras": [
       {
        "id": "RP-PRECO-LIQ",
        "natureza": "plausibilidade",
        "restricao": {
         "propriedade": "precoLiquido",
         "operador": "GTE",
         "valor": 0,
         "mensagem": "O preço líquido não pode ser negativo."
        },
        "descricao": "Preco.precoLiquido ≥ 0"
       }
      ]
     },
     {
      "nome": "descontoPreco",
      "tipo": "decimal",
      "descricao": "Desconto sobre o preço do item",
      "nomesAlternativos": [
       "Item price discount"
      ],
      "regras": [
       {
        "id": "RP-PRECO-DESC",
        "natureza": "plausibilidade",
        "restricao": {
         "propriedade": "descontoPreco",
         "operador": "GTE",
         "valor": 0,
         "mensagem": "O desconto sobre o preço não pode ser negativo."
        },
        "descricao": "Preco.descontoPreco ≥ 0"
       }
      ]
     },
     {
      "nome": "precoBruto",
      "tipo": "decimal",
      "descricao": "Preço do item antes do desconto",
      "nomesAlternativos": [
       "Item gross price"
      ],
      "regras": [
       {
        "id": "RP-PRECO-BRUTO",
        "natureza": "plausibilidade",
        "restricao": {
         "propriedade": "precoBruto",
         "operador": "GTE",
         "valor": 0,
         "mensagem": "O preço bruto não pode ser negativo."
        },
        "descricao": "Preco.precoBruto ≥ 0"
       }
      ]
     },
     {
      "nome": "quantidadeBase",
      "tipo": "decimal",
      "descricao": "Número de unidades a que o preço se refere (ex.: 15 € por 10 litros)",
      "nomesAlternativos": [
       "Item price base quantity",
       "BaseQuantity"
      ],
      "regras": [
       {
        "id": "RP-PRECO-QBASE",
        "natureza": "plausibilidade",
        "restricao": {
         "propriedade": "quantidadeBase",
         "operador": "GT",
         "valor": 0,
         "mensagem": "A quantidade base do preço tem de ser maior do que zero."
        },
        "descricao": "Preco.quantidadeBase > 0"
       }
      ]
     },
     {
      "nome": "unidadeQuantidadeBase",
      "tipo": "texto",
      "descricao": "Unidade de medida da quantidade base (UN/ECE Rec. 20 e 21)",
      "regras": [
       {
        "id": "RP-PRECO-UNIDADE",
        "natureza": "plausibilidade",
        "restricao": {
         "propriedade": "unidadeQuantidadeBase",
         "operador": "PATTERN",
         "valor": "^[A-Z0-9]{1,3}$",
         "mensagem": "A unidade da quantidade base tem de ser um código UN/ECE Rec. 20 (1 a 3 letras ou algarismos)."
        },
        "descricao": "Preco.unidadeQuantidadeBase segue o padrão ^[A-Z0-9]{1,3}$"
       }
      ]
     }
    ],
    "regras": [
     {
      "id": "RP-PRECO-CALCULO",
      "natureza": "plausibilidade",
      "restricao": {
       "operador": "FUNCTION",
       "chamada": {
        "funcao": "somaParcelasIgualA",
        "argumentos": [
         {
          "caminho": "precoLiquido"
         },
         {
          "caminho": "descontoPreco"
         },
         {
          "caminho": "precoBruto"
         },
         {
          "literal": 1.0
         }
        ]
       },
       "mensagem": "O preço líquido tem de ser igual ao preço bruto menos o desconto, com uma tolerância de 1,00 €."
      },
      "descricao": "somaParcelasIgualA(Preco.precoLiquido, Preco.descontoPreco, Preco.precoBruto, 1)"
     }
    ]
   },
   {
    "nome": "Artigo",
    "descricao": "Bem ou serviço transacionado: designação, descrição, códigos de identificação e país de origem.",
    "propriedades": [
     {
      "nome": "nome",
      "tipo": "texto",
      "descricao": "Designação do bem ou serviço",
      "nomesAlternativos": [
       "Item name",
       "description"
      ],
      "regras": [
       {
        "id": "RP-ART-NOME",
        "natureza": "plausibilidade",
        "restricao": {
         "propriedade": "nome",
         "operador": "LENGTH",
         "valor": [
          1,
          200
         ],
         "mensagem": "A designação do artigo tem de ter entre 1 e 200 caracteres."
        },
        "descricao": "Artigo.nome tem entre 1 e 200 caracteres"
       }
      ]
     },
     {
      "nome": "descricao",
      "tipo": "texto",
      "descricao": "Descrição detalhada do bem ou serviço",
      "nomesAlternativos": [
       "Item description"
      ],
      "regras": [
       {
        "id": "RP-ART-DESC",
        "natureza": "plausibilidade",
        "restricao": {
         "propriedade": "descricao",
         "operador": "LENGTH",
         "valor": [
          1,
          200
         ],
         "mensagem": "A descrição do artigo tem de ter entre 1 e 200 caracteres."
        },
        "descricao": "Artigo.descricao tem entre 1 e 200 caracteres"
       }
      ]
     },
     {
      "nome": "codigo",
      "tipo": "texto",
      "descricao": "Código do artigo atribuído pelo vendedor",
      "nomesAlternativos": [
       "Item Seller s identifier",
       "code"
      ],
      "regras": [
       {
        "id": "RP-ART-CODIGO",
        "natureza": "plausibilidade",
        "restricao": {
         "propriedade": "codigo",
         "operador": "LENGTH",
         "valor": [
          1,
          50
         ],
         "mensagem": "O código do artigo tem de ter entre 1 e 50 caracteres."
        },
        "descricao": "Artigo.codigo tem entre 1 e 50 caracteres"
       }
      ]
     },
     {
      "nome": "codigoComprador",
      "tipo": "texto",
      "descricao": "Código do artigo atribuído pelo comprador",
      "nomesAlternativos": [
       "Item Buyer s identifier"
      ],
      "regras": [
       {
        "id": "RP-ART-CODCOMP",
        "natureza": "plausibilidade",
        "restricao": {
         "propriedade": "codigoComprador",
         "operador": "LENGTH",
         "valor": [
          1,
          50
         ],
         "mensagem": "O código do artigo do comprador tem de ter entre 1 e 50 caracteres."
        },
        "descricao": "Artigo.codigoComprador tem entre 1 e 50 caracteres"
       }
      ]
     },
     {
      "nome": "codigoBarras",
      "tipo": "texto",
      "descricao": "Identificador normalizado do artigo (EAN/GTIN)",
      "nomesAlternativos": [
       "Item standard identifier",
       "barCode",
       "EAN"
      ],
      "regras": [
       {
        "id": "RP-ART-CODBARRAS",
        "natureza": "plausibilidade",
        "restricao": {
         "propriedade": "codigoBarras",
         "operador": "LENGTH",
         "valor": [
          1,
          50
         ],
         "mensagem": "O código EAN tem de ter entre 1 e 50 caracteres."
        },
        "descricao": "Artigo.codigoBarras tem entre 1 e 50 caracteres"
       }
      ]
     },
     {
      "nome": "classificacao",
      "tipo": "texto",
      "descricao": "Código de classificação da mercadoria (ex.: CPV)",
      "nomesAlternativos": [
       "Item classification identifier",
       "CPV"
      ],
      "regras": [
       {
        "id": "RP-ART-CLASSIF",
        "natureza": "plausibilidade",
        "restricao": {
         "propriedade": "classificacao",
         "operador": "LENGTH",
         "valor": [
          1,
          50
         ],
         "mensagem": "O código de classificação tem de ter entre 1 e 50 caracteres."
        },
        "descricao": "Artigo.classificacao tem entre 1 e 50 caracteres"
       }
      ]
     },
     {
      "nome": "paisOrigem",
      "tipo": "texto",
      "descricao": "País de origem do artigo (código ISO 3166-1 alfa-2)",
      "nomesAlternativos": [
       "Item country of origin"
      ],
      "regras": [
       {
        "id": "RP-ART-PAIS",
        "natureza": "plausibilidade",
        "restricao": {
         "propriedade": "paisOrigem",
         "operador": "PATTERN",
         "valor": "^[A-Z]{2}$",
         "mensagem": "O país de origem tem de ser um código ISO 3166-1 de duas letras."
        },
        "descricao": "Artigo.paisOrigem segue o padrão ^[A-Z]{2}$"
       }
      ]
     }
    ]
   },
   {
    "nome": "AtributoArtigo",
    "descricao": "Propriedade adicional de um artigo, como um par nome e valor.",
    "propriedades": [
     {
      "nome": "nome",
      "tipo": "texto",
      "descricao": "Nome ou tipo da propriedade adicional",
      "nomesAlternativos": [
       "AdditionalItemProperty Name"
      ],
      "regras": [
       {
        "id": "RP-ATRIB-NOME",
        "natureza": "plausibilidade",
        "restricao": {
         "propriedade": "nome",
         "operador": "LENGTH",
         "valor": [
          1,
          200
         ],
         "mensagem": "O nome da propriedade adicional tem de ter entre 1 e 200 caracteres."
        },
        "descricao": "AtributoArtigo.nome tem entre 1 e 200 caracteres"
       }
      ]
     },
     {
      "nome": "valor",
      "tipo": "texto",
      "descricao": "Valor da propriedade adicional",
      "nomesAlternativos": [
       "Item attribute value"
      ],
      "regras": [
       {
        "id": "RP-ATRIB-VALOR",
        "natureza": "plausibilidade",
        "restricao": {
         "propriedade": "valor",
         "operador": "LENGTH",
         "valor": [
          1,
          200
         ],
         "mensagem": "O valor da propriedade adicional tem de ter entre 1 e 200 caracteres."
        },
        "descricao": "AtributoArtigo.valor tem entre 1 e 200 caracteres"
       }
      ]
     }
    ]
   }
  ],
  "sm": [
   {
    "nome": "Metainformacao",
    "descricao": "Metainformação do próprio modelo: origem, versão da fonte, entidade de origem, utilização e domínio.",
    "propriedades": [
     {
      "nome": "origemModelo",
      "tipo": "texto",
      "descricao": "Fonte do modelo de dados (norma, sistema ou repositório)"
     },
     {
      "nome": "versaoOrigem",
      "tipo": "texto",
      "descricao": "Versão da fonte usada"
     },
     {
      "nome": "referenciaOrigem",
      "tipo": "texto",
      "descricao": "Identificador da entidade na fonte (ex.: BG-0 Invoice, Device)"
     },
     {
      "nome": "utilizacao",
      "tipo": "texto",
      "descricao": "Finalidade ou contexto de utilização do modelo"
     },
     {
      "nome": "dominio",
      "tipo": "texto",
      "descricao": "Domínio a que o modelo pertence"
     },
     {
      "nome": "observacoes",
      "tipo": "texto",
      "descricao": "Outra metainformação relevante sobre o modelo"
     }
    ]
   },
   {
    "nome": "CabecalhoDocumento",
    "descricao": "Identificação do documento de faturação: número, data, tipo, moedas, datas de IVA e de vencimento, e especificação.",
    "propriedades": [
     {
      "nome": "numero",
      "tipo": "texto",
      "descricao": "Número de referência do documento, atribuído pelo fornecedor",
      "nomesAlternativos": [
       "Invoice number"
      ],
      "regras": [
       {
        "id": "RP-DOC-NUMERO",
        "natureza": "plausibilidade",
        "restricao": {
         "propriedade": "numero",
         "operador": "LENGTH",
         "valor": [
          1,
          50
         ],
         "mensagem": "O número do documento tem de ter entre 1 e 50 caracteres."
        },
        "descricao": "CabecalhoDocumento.numero tem entre 1 e 50 caracteres"
       }
      ]
     },
     {
      "nome": "dataEmissao",
      "tipo": "data",
      "descricao": "Data de emissão do documento",
      "nomesAlternativos": [
       "Invoice issue date",
       "IssueDate"
      ]
     },
     {
      "nome": "tipoDocumento",
      "tipo": "texto",
      "descricao": "Código do tipo funcional do documento (UNCL 1001 ou código AT)",
      "nomesAlternativos": [
       "Invoice type code",
       "InvoiceTypeCode",
       "CreditNoteTypeCode"
      ],
      "regras": [
       {
        "id": "RP-DOC-TIPO",
        "natureza": "plausibilidade",
        "restricao": {
         "propriedade": "tipoDocumento",
         "operador": "IN",
         "valor": [
          "380",
          "381",
          "383",
          "386",
          "389",
          "FT",
          "FS",
          "FR",
          "ND",
          "NC",
          "RP",
          "RE",
          "CS",
          "LD",
          "RA"
         ],
         "mensagem": "O tipo de documento tem de ser um destes: 380, 381, 383, 386, 389, FT, FS, FR, ND, NC, RP, RE, CS, LD, RA."
        },
        "descricao": "CabecalhoDocumento.tipoDocumento ∈ {380, 381, 383, 386, 389, FT, FS, FR, ND, NC, RP, RE, CS, LD, RA}"
       }
      ]
     },
     {
      "nome": "moeda",
      "tipo": "texto",
      "descricao": "Moeda em que estão os montantes do documento (ISO 4217 alfa-3)",
      "nomesAlternativos": [
       "Invoice currency code",
       "DocumentCurrencyCode"
      ],
      "regras": [
       {
        "id": "RP-DOC-MOEDA",
        "natureza": "plausibilidade",
        "restricao": {
         "propriedade": "moeda",
         "operador": "PATTERN",
         "valor": "^[A-Z]{3}$",
         "mensagem": "A moeda do documento tem de ser um código ISO 4217 de três letras."
        },
        "descricao": "CabecalhoDocumento.moeda segue o padrão ^[A-Z]{3}$"
       }
      ]
     },
     {
      "nome": "moedaIva",
      "tipo": "texto",
      "descricao": "Moeda usada para a contabilidade e as declarações de IVA no país do vendedor",
      "nomesAlternativos": [
       "TaxCurrencyCode"
      ],
      "regras": [
       {
        "id": "RP-DOC-MOEDAIVA",
        "natureza": "plausibilidade",
        "restricao": {
         "propriedade": "moedaIva",
         "operador": "PATTERN",
         "valor": "^[A-Z]{3}$",
         "mensagem": "A moeda contabilística do IVA tem de ser um código ISO 4217 de três letras."
        },
        "descricao": "CabecalhoDocumento.moedaIva segue o padrão ^[A-Z]{3}$"
       }
      ]
     },
     {
      "nome": "dataIva",
      "tipo": "data",
      "descricao": "Data em que o IVA se torna exigível, quando difere da data de emissão",
      "nomesAlternativos": [
       "Value added tax point date",
       "TaxPointDate"
      ]
     },
     {
      "nome": "codigoDataIva",
      "tipo": "texto",
      "descricao": "Código da data em que o IVA se torna exigível",
      "nomesAlternativos": [
       "Value added tax point date code",
       "DescriptionCode"
      ],
      "regras": [
       {
        "id": "RP-DOC-CODDATAIVA",
        "natureza": "plausibilidade",
        "restricao": {
         "propriedade": "codigoDataIva",
         "operador": "IN",
         "valor": [
          "3",
          "35",
          "432"
         ],
         "mensagem": "O código da data de IVA tem de ser 3, 35 ou 432."
        },
        "descricao": "CabecalhoDocumento.codigoDataIva ∈ {3, 35, 432}"
       }
      ]
     },
     {
      "nome": "dataVencimento",
      "tipo": "data",
      "descricao": "Data de vencimento do pagamento",
      "nomesAlternativos": [
       "Payment due date",
       "DueDate",
       "PaymentDueDate"
      ]
     },
     {
      "nome": "referenciaCliente",
      "tipo": "texto",
      "descricao": "Referência atribuída pelo cliente",
      "nomesAlternativos": [
       "BuyerReference"
      ],
      "regras": [
       {
        "id": "RP-DOC-REFCLIENTE",
        "natureza": "plausibilidade",
        "restricao": {
         "propriedade": "referenciaCliente",
         "operador": "LENGTH",
         "valor": [
          1,
          50
         ],
         "mensagem": "A referência do cliente tem de ter entre 1 e 50 caracteres."
        },
        "descricao": "CabecalhoDocumento.referenciaCliente tem entre 1 e 50 caracteres"
       }
      ]
     },
     {
      "nome": "numeroCompromisso",
      "tipo": "texto",
      "descricao": "Número do compromisso orçamental do adquirente público",
      "nomesAlternativos": [
       "AccountingCost"
      ],
      "regras": [
       {
        "id": "RP-DOC-COMPROMISSO",
        "natureza": "plausibilidade",
        "restricao": {
         "propriedade": "numeroCompromisso",
         "operador": "LENGTH",
         "valor": [
          1,
          50
         ],
         "mensagem": "O número do compromisso tem de ter entre 1 e 50 caracteres."
        },
        "descricao": "CabecalhoDocumento.numeroCompromisso tem entre 1 e 50 caracteres"
       }
      ]
     },
     {
      "nome": "condicoesPagamento",
      "tipo": "texto",
      "descricao": "Descrição das condições de pagamento",
      "nomesAlternativos": [
       "Payment terms"
      ],
      "regras": [
       {
        "id": "RP-DOC-CONDPAG",
        "natureza": "plausibilidade",
        "restricao": {
         "propriedade": "condicoesPagamento",
         "operador": "LENGTH",
         "valor": [
          1,
          200
         ],
         "mensagem": "As condições de pagamento têm de ter entre 1 e 200 caracteres."
        },
        "descricao": "CabecalhoDocumento.condicoesPagamento tem entre 1 e 200 caracteres"
       }
      ]
     },
     {
      "nome": "tipoProcesso",
      "tipo": "texto",
      "descricao": "Tipo de processo de negócio em que o documento se insere",
      "nomesAlternativos": [
       "ProfileID",
       "Business process type"
      ],
      "regras": [
       {
        "id": "RP-DOC-PROCESSO",
        "natureza": "plausibilidade",
        "restricao": {
         "propriedade": "tipoProcesso",
         "operador": "LENGTH",
         "valor": [
          1,
          50
         ],
         "mensagem": "O tipo de processo tem de ter entre 1 e 50 caracteres."
        },
        "descricao": "CabecalhoDocumento.tipoProcesso tem entre 1 e 50 caracteres"
       }
      ]
     },
     {
      "nome": "identificadorEspecificacao",
      "tipo": "texto",
      "descricao": "Identificador da customização CIUS-PT seguida, que permite ao recetor validar o documento",
      "nomesAlternativos": [
       "Specification identifier",
       "CustomizationID"
      ],
      "regras": [
       {
        "id": "RP-DOC-ESPEC",
        "natureza": "plausibilidade",
        "restricao": {
         "propriedade": "identificadorEspecificacao",
         "operador": "PATTERN",
         "valor": "^urn:cen\\.eu:en16931:2017#compliant#urn:feap\\.gov\\.pt:CIUS-PT:.{1,10}$",
         "mensagem": "O identificador da especificação tem de ser urn:cen.eu:en16931:2017#compliant#urn:feap.gov.pt:CIUS-PT: seguido da versão."
        },
        "descricao": "CabecalhoDocumento.identificadorEspecificacao segue o padrão ^urn:cen\\.eu:en16931:2017#compliant#urn:feap\\.gov\\.pt:CIUS-PT:.{1,10}$"
       }
      ]
     }
    ],
    "regras": [
     {
      "id": "RP-DOC-DATAIVA",
      "natureza": "plausibilidade",
      "restricao": {
       "operador": "FUNCTION",
       "chamada": {
        "funcao": "mutuamenteExclusivos",
        "argumentos": [
         {
          "caminho": "dataIva"
         },
         {
          "caminho": "codigoDataIva"
         }
        ]
       },
       "mensagem": "A data de IVA e o código da data de IVA não podem vir os dois no mesmo documento."
      },
      "descricao": "mutuamenteExclusivos(CabecalhoDocumento.dataIva, CabecalhoDocumento.codigoDataIva)"
     }
    ]
   },
   {
    "nome": "ReferenciasDocumento",
    "descricao": "Referências a outros documentos e processos do adquirente: projeto, contrato, encomenda, avisos e acordo-quadro.",
    "propriedades": [
     {
      "nome": "projeto",
      "tipo": "texto",
      "descricao": "Número do projeto",
      "nomesAlternativos": [
       "Project reference"
      ],
      "regras": [
       {
        "id": "RP-REF-PROJETO",
        "natureza": "plausibilidade",
        "restricao": {
         "propriedade": "projeto",
         "operador": "LENGTH",
         "valor": [
          1,
          50
         ],
         "mensagem": "A referência do projeto tem de ter entre 1 e 50 caracteres."
        },
        "descricao": "ReferenciasDocumento.projeto tem entre 1 e 50 caracteres"
       }
      ]
     },
     {
      "nome": "contrato",
      "tipo": "texto",
      "descricao": "Número do contrato",
      "nomesAlternativos": [
       "Contract reference"
      ],
      "regras": [
       {
        "id": "RP-REF-CONTRATO",
        "natureza": "plausibilidade",
        "restricao": {
         "propriedade": "contrato",
         "operador": "LENGTH",
         "valor": [
          1,
          20
         ],
         "mensagem": "A referência do contrato tem de ter entre 1 e 20 caracteres."
        },
        "descricao": "ReferenciasDocumento.contrato tem entre 1 e 20 caracteres"
       }
      ]
     },
     {
      "nome": "encomenda",
      "tipo": "texto",
      "descricao": "Número da nota de encomenda do adquirente",
      "nomesAlternativos": [
       "Purchase order reference"
      ],
      "regras": [
       {
        "id": "RP-REF-ENCOMENDA",
        "natureza": "plausibilidade",
        "restricao": {
         "propriedade": "encomenda",
         "operador": "LENGTH",
         "valor": [
          1,
          20
         ],
         "mensagem": "A referência da encomenda tem de ter entre 1 e 20 caracteres."
        },
        "descricao": "ReferenciasDocumento.encomenda tem entre 1 e 20 caracteres"
       }
      ]
     },
     {
      "nome": "ordemVenda",
      "tipo": "texto",
      "descricao": "Número da ordem de venda emitida pelo fornecedor",
      "nomesAlternativos": [
       "Sales order reference"
      ],
      "regras": [
       {
        "id": "RP-REF-ORDEMVENDA",
        "natureza": "plausibilidade",
        "restricao": {
         "propriedade": "ordemVenda",
         "operador": "LENGTH",
         "valor": [
          1,
          20
         ],
         "mensagem": "A referência da ordem de venda tem de ter entre 1 e 20 caracteres."
        },
        "descricao": "ReferenciasDocumento.ordemVenda tem entre 1 e 20 caracteres"
       }
      ]
     },
     {
      "nome": "avisoRececao",
      "tipo": "texto",
      "descricao": "Número do aviso de receção",
      "nomesAlternativos": [
       "Receiving advice reference"
      ],
      "regras": [
       {
        "id": "RP-REF-RECECAO",
        "natureza": "plausibilidade",
        "restricao": {
         "propriedade": "avisoRececao",
         "operador": "LENGTH",
         "valor": [
          1,
          20
         ],
         "mensagem": "A referência do aviso de receção tem de ter entre 1 e 20 caracteres."
        },
        "descricao": "ReferenciasDocumento.avisoRececao tem entre 1 e 20 caracteres"
       }
      ]
     },
     {
      "nome": "avisoEnvio",
      "tipo": "texto",
      "descricao": "Referência do aviso de expedição",
      "nomesAlternativos": [
       "Despatch advice reference"
      ],
      "regras": [
       {
        "id": "RP-REF-ENVIO",
        "natureza": "plausibilidade",
        "restricao": {
         "propriedade": "avisoEnvio",
         "operador": "LENGTH",
         "valor": [
          1,
          20
         ],
         "mensagem": "A referência do aviso de expedição tem de ter entre 1 e 20 caracteres."
        },
        "descricao": "ReferenciasDocumento.avisoEnvio tem entre 1 e 20 caracteres"
       }
      ]
     },
     {
      "nome": "acordoQuadro",
      "tipo": "texto",
      "descricao": "Número do acordo-quadro ou do lote do concurso",
      "nomesAlternativos": [
       "Tender or lot reference"
      ],
      "regras": [
       {
        "id": "RP-REF-ACORDO",
        "natureza": "plausibilidade",
        "restricao": {
         "propriedade": "acordoQuadro",
         "operador": "LENGTH",
         "valor": [
          1,
          20
         ],
         "mensagem": "A referência do acordo-quadro tem de ter entre 1 e 20 caracteres."
        },
        "descricao": "ReferenciasDocumento.acordoQuadro tem entre 1 e 20 caracteres"
       }
      ]
     },
     {
      "nome": "processoRegisto",
      "tipo": "texto",
      "descricao": "Identificador do processo de registo de entrada do documento no adquirente",
      "nomesAlternativos": [
       "Invoiced object identifier"
      ],
      "regras": [
       {
        "id": "RP-REF-PROCESSO",
        "natureza": "plausibilidade",
        "restricao": {
         "propriedade": "processoRegisto",
         "operador": "LENGTH",
         "valor": [
          1,
          50
         ],
         "mensagem": "O identificador do processo de registo tem de ter entre 1 e 50 caracteres."
        },
        "descricao": "ReferenciasDocumento.processoRegisto tem entre 1 e 50 caracteres"
       }
      ]
     }
    ]
   },
   {
    "nome": "NotaDocumento",
    "descricao": "Nota em texto livre sobre o documento, com o assunto, se houver.",
    "propriedades": [
     {
      "nome": "assunto",
      "tipo": "texto",
      "descricao": "Assunto da nota"
     },
     {
      "nome": "texto",
      "tipo": "texto",
      "descricao": "Texto da nota, com informação não estruturada sobre o documento",
      "nomesAlternativos": [
       "Note"
      ],
      "regras": [
       {
        "id": "RP-NOTA-TEXTO",
        "natureza": "plausibilidade",
        "restricao": {
         "propriedade": "texto",
         "operador": "LENGTH",
         "valor": [
          1,
          500
         ],
         "mensagem": "A nota tem de ter entre 1 e 500 caracteres."
        },
        "descricao": "NotaDocumento.texto tem entre 1 e 500 caracteres"
       }
      ]
     }
    ]
   },
   {
    "nome": "DocumentosAnteriores",
    "descricao": "Coleção das referências a documentos anteriores (faturas retificadas ou corrigidas).",
    "composicao": [
     {
      "usm": "ReferenciaDocumento",
      "cardinalidade": "0..*"
     }
    ]
   },
   {
    "nome": "Fornecedor",
    "descricao": "Quem fornece e fatura: identificação fiscal, morada, contactos e dados legais.",
    "composicao": [
     {
      "usm": "SujeitoPassivo",
      "cardinalidade": "1..1"
     },
     {
      "usm": "Morada",
      "cardinalidade": "1..1"
     },
     {
      "usm": "ComplementoMorada",
      "cardinalidade": "0..1"
     },
     {
      "usm": "ContactoTelefonico",
      "cardinalidade": "0..1"
     },
     {
      "usm": "Contacto",
      "cardinalidade": "0..1"
     }
    ],
    "propriedades": [
     {
      "nome": "registoFiscal",
      "tipo": "texto",
      "descricao": "Identificação do local do fornecedor para fins fiscais ou referência ao seu estatuto fiscal",
      "nomesAlternativos": [
       "Seller tax registration identifier"
      ],
      "regras": [
       {
        "id": "RP-FORN-REGFISCAL",
        "natureza": "plausibilidade",
        "restricao": {
         "propriedade": "registoFiscal",
         "operador": "LENGTH",
         "valor": [
          1,
          50
         ],
         "mensagem": "O registo fiscal do fornecedor tem de ter entre 1 e 50 caracteres."
        },
        "descricao": "Fornecedor.registoFiscal tem entre 1 e 50 caracteres"
       }
      ]
     },
     {
      "nome": "capitalSocial",
      "tipo": "texto",
      "descricao": "Informação sobre o capital social e a forma jurídica do fornecedor",
      "nomesAlternativos": [
       "CompanyLegalForm"
      ],
      "regras": [
       {
        "id": "RP-FORN-CAPITAL",
        "natureza": "plausibilidade",
        "restricao": {
         "propriedade": "capitalSocial",
         "operador": "LENGTH",
         "valor": [
          1,
          200
         ],
         "mensagem": "A informação de capital social tem de ter entre 1 e 200 caracteres."
        },
        "descricao": "Fornecedor.capitalSocial tem entre 1 e 200 caracteres"
       }
      ]
     },
     {
      "nome": "enderecoEletronico",
      "tipo": "texto",
      "descricao": "Endereço eletrónico de receção de documentos do fornecedor",
      "nomesAlternativos": [
       "Seller electronic address",
       "EndpointID"
      ],
      "regras": [
       {
        "id": "RP-FORN-ENDELET",
        "natureza": "plausibilidade",
        "restricao": {
         "propriedade": "enderecoEletronico",
         "operador": "LENGTH",
         "valor": [
          1,
          50
         ],
         "mensagem": "O endereço eletrónico do fornecedor tem de ter entre 1 e 50 caracteres."
        },
        "descricao": "Fornecedor.enderecoEletronico tem entre 1 e 50 caracteres"
       }
      ]
     },
     {
      "nome": "pontoContacto",
      "tipo": "texto",
      "descricao": "Pessoa ou serviço de contacto do fornecedor",
      "nomesAlternativos": [
       "Seller contact point"
      ],
      "regras": [
       {
        "id": "RP-FORN-CONTACTO",
        "natureza": "plausibilidade",
        "restricao": {
         "propriedade": "pontoContacto",
         "operador": "LENGTH",
         "valor": [
          1,
          200
         ],
         "mensagem": "O ponto de contacto do fornecedor tem de ter entre 1 e 200 caracteres."
        },
        "descricao": "Fornecedor.pontoContacto tem entre 1 e 200 caracteres"
       }
      ]
     }
    ]
   },
   {
    "nome": "Adquirente",
    "descricao": "Quem adquire e recebe o documento: identificação fiscal, morada e contactos.",
    "composicao": [
     {
      "usm": "SujeitoPassivo",
      "cardinalidade": "1..1"
     },
     {
      "usm": "Morada",
      "cardinalidade": "1..1"
     },
     {
      "usm": "ComplementoMorada",
      "cardinalidade": "0..1"
     },
     {
      "usm": "ContactoTelefonico",
      "cardinalidade": "0..1"
     },
     {
      "usm": "Contacto",
      "cardinalidade": "0..1"
     }
    ],
    "propriedades": [
     {
      "nome": "enderecoEletronico",
      "tipo": "texto",
      "descricao": "Endereço eletrónico de receção de documentos do adquirente",
      "nomesAlternativos": [
       "Buyer electronic address",
       "EndpointID"
      ],
      "regras": [
       {
        "id": "RP-ADQ-ENDELET",
        "natureza": "plausibilidade",
        "restricao": {
         "propriedade": "enderecoEletronico",
         "operador": "LENGTH",
         "valor": [
          1,
          50
         ],
         "mensagem": "O endereço eletrónico do adquirente tem de ter entre 1 e 50 caracteres."
        },
        "descricao": "Adquirente.enderecoEletronico tem entre 1 e 50 caracteres"
       }
      ]
     },
     {
      "nome": "pontoContacto",
      "tipo": "texto",
      "descricao": "Pessoa ou serviço de contacto do adquirente",
      "nomesAlternativos": [
       "Buyer contact point"
      ],
      "regras": [
       {
        "id": "RP-ADQ-CONTACTO",
        "natureza": "plausibilidade",
        "restricao": {
         "propriedade": "pontoContacto",
         "operador": "LENGTH",
         "valor": [
          1,
          200
         ],
         "mensagem": "O ponto de contacto do adquirente tem de ter entre 1 e 200 caracteres."
        },
        "descricao": "Adquirente.pontoContacto tem entre 1 e 200 caracteres"
       }
      ]
     }
    ]
   },
   {
    "nome": "RecebedorPagamento",
    "descricao": "Entidade que recebe o pagamento, quando é diferente do fornecedor.",
    "composicao": [
     {
      "usm": "SujeitoPassivo",
      "cardinalidade": "1..1"
     }
    ]
   },
   {
    "nome": "RepresentanteFiscal",
    "descricao": "Representante do fornecedor para efeitos fiscais: identificação e morada.",
    "composicao": [
     {
      "usm": "SujeitoPassivo",
      "cardinalidade": "1..1"
     },
     {
      "usm": "Morada",
      "cardinalidade": "1..1"
     },
     {
      "usm": "ComplementoMorada",
      "cardinalidade": "0..1"
     }
    ]
   },
   {
    "nome": "LocalEntrega",
    "descricao": "Local e data em que os bens ou serviços são entregues.",
    "composicao": [
     {
      "usm": "Morada",
      "cardinalidade": "0..1"
     },
     {
      "usm": "ComplementoMorada",
      "cardinalidade": "0..1"
     }
    ],
    "propriedades": [
     {
      "nome": "nomeLocal",
      "tipo": "texto",
      "descricao": "Nome da parte ou do local de entrega",
      "nomesAlternativos": [
       "Deliver to party name"
      ],
      "regras": [
       {
        "id": "RP-LENT-NOME",
        "natureza": "plausibilidade",
        "restricao": {
         "propriedade": "nomeLocal",
         "operador": "LENGTH",
         "valor": [
          1,
          200
         ],
         "mensagem": "O nome do local de entrega tem de ter entre 1 e 200 caracteres."
        },
        "descricao": "LocalEntrega.nomeLocal tem entre 1 e 200 caracteres"
       }
      ]
     },
     {
      "nome": "identificadorLocal",
      "tipo": "texto",
      "descricao": "Identificador do local onde os bens ou serviços são entregues",
      "nomesAlternativos": [
       "Deliver to location identifier"
      ],
      "regras": [
       {
        "id": "RP-LENT-IDLOCAL",
        "natureza": "plausibilidade",
        "restricao": {
         "propriedade": "identificadorLocal",
         "operador": "LENGTH",
         "valor": [
          1,
          50
         ],
         "mensagem": "O identificador do local de entrega tem de ter entre 1 e 50 caracteres."
        },
        "descricao": "LocalEntrega.identificadorLocal tem entre 1 e 50 caracteres"
       }
      ]
     },
     {
      "nome": "dataEntrega",
      "tipo": "data",
      "descricao": "Data efetiva da entrega",
      "nomesAlternativos": [
       "Actual delivery date"
      ]
     }
    ],
    "regras": [
     {
      "id": "RP-LENT-IDENT",
      "natureza": "plausibilidade",
      "restricao": {
       "operador": "FUNCTION",
       "chamada": {
        "funcao": "localEntregaIdentificado",
        "argumentos": [
         {
          "caminho": "nomeLocal"
         },
         {
          "caminho": "identificadorLocal"
         },
         {
          "caminho": "dataEntrega"
         },
         {
          "caminho": "Morada.rua"
         }
        ]
       },
       "mensagem": "A informação de entrega tem de indicar a data, o identificador do local, a morada ou o nome do local."
      },
      "descricao": "localEntregaIdentificado(LocalEntrega.nomeLocal, LocalEntrega.identificadorLocal, LocalEntrega.dataEntrega, LocalEntrega.Morada.rua)"
     }
    ]
   },
   {
    "nome": "PeriodoFaturacao",
    "descricao": "Período a que a faturação diz respeito.",
    "composicao": [
     {
      "usm": "Periodo",
      "cardinalidade": "1..1"
     }
    ]
   },
   {
    "nome": "Pagamento",
    "descricao": "Instruções de pagamento: meio de pagamento, referência e dados de transferência, cartão ou débito direto.",
    "composicao": [
     {
      "usm": "ContaBancaria",
      "cardinalidade": "0..*"
     },
     {
      "usm": "CartaoPagamento",
      "cardinalidade": "0..1"
     },
     {
      "usm": "DebitoDireto",
      "cardinalidade": "0..1"
     }
    ],
    "propriedades": [
     {
      "nome": "meioPagamento",
      "tipo": "texto",
      "descricao": "Código do meio de pagamento (UNCL 4461 ou código nacional)",
      "nomesAlternativos": [
       "Payment means type code",
       "PaymentMeansCode"
      ],
      "regras": [
       {
        "id": "RP-PAG-MEIO",
        "natureza": "plausibilidade",
        "restricao": {
         "propriedade": "meioPagamento",
         "operador": "IN",
         "valor": [
          "30",
          "48",
          "49",
          "57",
          "58",
          "59",
          "CC",
          "CD",
          "CH",
          "CI",
          "CO",
          "CS",
          "DE",
          "LC",
          "MB",
          "NU",
          "OU",
          "PR",
          "TB",
          "TR"
         ],
         "mensagem": "O meio de pagamento tem de ser um código UNCL 4461 admitido (30, 48, 49, 57, 58, 59) ou um destes: CC, CD, CH, CI, CO, CS, DE, LC, MB, NU, OU, PR, TB, TR."
        },
        "descricao": "Pagamento.meioPagamento ∈ {30, 48, 49, 57, 58, 59, CC, CD, CH, CI, CO, CS, DE, LC, MB, NU, OU, PR, TB, TR}"
       }
      ]
     },
     {
      "nome": "detalhePagamento",
      "tipo": "texto",
      "descricao": "Descrição do pagamento (ex.: pagamento por ATM)",
      "regras": [
       {
        "id": "RP-PAG-DETALHE",
        "natureza": "plausibilidade",
        "restricao": {
         "propriedade": "detalhePagamento",
         "operador": "LENGTH",
         "valor": [
          1,
          150
         ],
         "mensagem": "A descrição do pagamento tem de ter entre 1 e 150 caracteres."
        },
        "descricao": "Pagamento.detalhePagamento tem entre 1 e 150 caracteres"
       }
      ]
     },
     {
      "nome": "referenciaPagamento",
      "tipo": "texto",
      "descricao": "Referência de pagamento por ATM ou DUC",
      "nomesAlternativos": [
       "PaymentID"
      ],
      "regras": [
       {
        "id": "RP-PAG-REF",
        "natureza": "plausibilidade",
        "restricao": {
         "propriedade": "referenciaPagamento",
         "operador": "PATTERN",
         "valor": "^#REFERENCE@(ATM|DUC)PAYMENT#.{1,20}#$",
         "mensagem": "A referência de pagamento tem de ter a forma #REFERENCE@ATMPAYMENT#…# ou #REFERENCE@DUCPAYMENT#…#, com 1 a 20 caracteres."
        },
        "descricao": "Pagamento.referenciaPagamento segue o padrão ^#REFERENCE@(ATM|DUC)PAYMENT#.{1,20}#$"
       }
      ]
     }
    ],
    "regras": [
     {
      "id": "RIR-PAG-IBAN",
      "natureza": "inferencia_restritiva",
      "condicao": [
       {
        "propriedade": "meioPagamento",
        "operador": "IN",
        "valor": [
         "30",
         "58"
        ]
       }
      ],
      "restricao": {
       "operador": "FUNCTION",
       "chamada": {
        "funcao": "colecaoNaoVazia",
        "argumentos": [
         {
          "caminho": "ContaBancaria.iban"
         }
        ]
       },
       "mensagem": "No pagamento por transferência bancária (30 ou 58), é obrigatório indicar o IBAN da conta."
      },
      "descricao": "Se Pagamento.meioPagamento ∈ {30, 58} → colecaoNaoVazia(Pagamento.ContaBancaria.iban)"
     }
    ]
   },
   {
    "nome": "DescontoEncargoDocumento",
    "descricao": "Desconto ou encargo ao nível do documento, com a categoria de IVA que lhe é aplicada.",
    "composicao": [
     {
      "usm": "DescontoEncargo",
      "cardinalidade": "1..1"
     },
     {
      "usm": "CategoriaIva",
      "cardinalidade": "1..1"
     }
    ]
   },
   {
    "nome": "Totais",
    "descricao": "Totais monetários do documento: soma das linhas, descontos, encargos, IVA, total e valor a pagar.",
    "propriedades": [
     {
      "nome": "somaLinhas",
      "tipo": "decimal",
      "descricao": "Soma dos montantes líquidos das linhas, sem imposto",
      "nomesAlternativos": [
       "Sum of Invoice line net amount",
       "LineExtensionAmount"
      ]
     },
     {
      "nome": "totalDescontos",
      "tipo": "decimal",
      "descricao": "Soma dos descontos ao nível do documento",
      "nomesAlternativos": [
       "AllowanceTotalAmount"
      ],
      "regras": [
       {
        "id": "RP-TOT-DESC-POS",
        "natureza": "plausibilidade",
        "restricao": {
         "propriedade": "totalDescontos",
         "operador": "GTE",
         "valor": 0,
         "mensagem": "O total dos descontos não pode ser negativo."
        },
        "descricao": "Totais.totalDescontos ≥ 0"
       }
      ]
     },
     {
      "nome": "totalEncargos",
      "tipo": "decimal",
      "descricao": "Soma dos encargos ao nível do documento",
      "nomesAlternativos": [
       "ChargeTotalAmount"
      ],
      "regras": [
       {
        "id": "RP-TOT-ENC-POS",
        "natureza": "plausibilidade",
        "restricao": {
         "propriedade": "totalEncargos",
         "operador": "GTE",
         "valor": 0,
         "mensagem": "O total dos encargos não pode ser negativo."
        },
        "descricao": "Totais.totalEncargos ≥ 0"
       }
      ]
     },
     {
      "nome": "totalSemIva",
      "tipo": "decimal",
      "descricao": "Total do documento sem IVA",
      "nomesAlternativos": [
       "Invoice total amount without VAT",
       "TaxExclusiveAmount"
      ],
      "regras": [
       {
        "id": "RP-TOT-SEMIVA-POS",
        "natureza": "plausibilidade",
        "restricao": {
         "propriedade": "totalSemIva",
         "operador": "GTE",
         "valor": 0,
         "mensagem": "O total sem IVA não pode ser negativo."
        },
        "descricao": "Totais.totalSemIva ≥ 0"
       }
      ]
     },
     {
      "nome": "totalIva",
      "tipo": "decimal",
      "descricao": "Total do IVA do documento",
      "nomesAlternativos": [
       "Total VAT amount",
       "TaxAmount"
      ]
     },
     {
      "nome": "totalIvaMoedaContabilistica",
      "tipo": "decimal",
      "descricao": "Total do IVA na moeda aceite ou exigida no país do fornecedor"
     },
     {
      "nome": "totalComIva",
      "tipo": "decimal",
      "descricao": "Total do documento com IVA",
      "nomesAlternativos": [
       "Invoice total amount with VAT",
       "TaxInclusiveAmount"
      ],
      "regras": [
       {
        "id": "RP-TOT-COMIVA-POS",
        "natureza": "plausibilidade",
        "restricao": {
         "propriedade": "totalComIva",
         "operador": "GTE",
         "valor": 0,
         "mensagem": "O total com IVA não pode ser negativo."
        },
        "descricao": "Totais.totalComIva ≥ 0"
       }
      ]
     },
     {
      "nome": "valorPago",
      "tipo": "decimal",
      "descricao": "Soma dos montantes já pagos, a deduzir do valor a pagar",
      "nomesAlternativos": [
       "Paid amount",
       "PrepaidAmount"
      ],
      "regras": [
       {
        "id": "RP-TOT-PAGO-POS",
        "natureza": "plausibilidade",
        "restricao": {
         "propriedade": "valorPago",
         "operador": "GTE",
         "valor": 0,
         "mensagem": "O valor já pago não pode ser negativo."
        },
        "descricao": "Totais.valorPago ≥ 0"
       }
      ]
     },
     {
      "nome": "arredondamento",
      "tipo": "decimal",
      "descricao": "Montante de arredondamento aplicado ao total com IVA",
      "nomesAlternativos": [
       "Rounding amount",
       "PayableRoundingAmount"
      ]
     },
     {
      "nome": "valorPagar",
      "tipo": "decimal",
      "descricao": "Valor a pagar",
      "nomesAlternativos": [
       "Amount due for payment",
       "PayableAmount"
      ],
      "regras": [
       {
        "id": "RP-TOT-PAGAR-POS",
        "natureza": "plausibilidade",
        "restricao": {
         "propriedade": "valorPagar",
         "operador": "GTE",
         "valor": 0,
         "mensagem": "O valor a pagar não pode ser negativo."
        },
        "descricao": "Totais.valorPagar ≥ 0"
       }
      ]
     }
    ],
    "regras": [
     {
      "id": "RP-TOT-COMIVA",
      "natureza": "plausibilidade",
      "restricao": {
       "operador": "FUNCTION",
       "chamada": {
        "funcao": "somaParcelasIgualA",
        "argumentos": [
         {
          "caminho": "totalSemIva"
         },
         {
          "caminho": "totalIva"
         },
         {
          "caminho": "totalComIva"
         },
         {
          "literal": 1.0
         }
        ]
       },
       "mensagem": "O total com IVA tem de ser igual ao total sem IVA mais o total do IVA, com uma tolerância de 1,00 €."
      },
      "descricao": "somaParcelasIgualA(Totais.totalSemIva, Totais.totalIva, Totais.totalComIva, 1)"
     },
     {
      "id": "RP-TOT-SEMIVA",
      "natureza": "plausibilidade",
      "restricao": {
       "operador": "FUNCTION",
       "chamada": {
        "funcao": "saldoIgualA",
        "argumentos": [
         {
          "caminho": "somaLinhas"
         },
         {
          "caminho": "totalDescontos"
         },
         {
          "caminho": "totalEncargos"
         },
         {
          "caminho": "totalSemIva"
         },
         {
          "literal": 1.0
         }
        ]
       },
       "mensagem": "O total sem IVA tem de ser igual à soma das linhas, menos os descontos e mais os encargos, com uma tolerância de 1,00 €."
      },
      "descricao": "saldoIgualA(Totais.somaLinhas, Totais.totalDescontos, Totais.totalEncargos, Totais.totalSemIva, 1)"
     },
     {
      "id": "RP-TOT-PAGAR",
      "natureza": "plausibilidade",
      "restricao": {
       "operador": "FUNCTION",
       "chamada": {
        "funcao": "saldoIgualA",
        "argumentos": [
         {
          "caminho": "totalComIva"
         },
         {
          "caminho": "valorPago"
         },
         {
          "caminho": "arredondamento"
         },
         {
          "caminho": "valorPagar"
         },
         {
          "literal": 1.0
         }
        ]
       },
       "mensagem": "O valor a pagar tem de ser igual ao total com IVA, menos o valor já pago e mais o arredondamento, com uma tolerância de 1,00 €."
      },
      "descricao": "saldoIgualA(Totais.totalComIva, Totais.valorPago, Totais.arredondamento, Totais.valorPagar, 1)"
     }
    ]
   },
   {
    "nome": "DecomposicaoIva",
    "descricao": "Subtotal de IVA por categoria e taxa: base tributável, imposto e categoria.",
    "composicao": [
     {
      "usm": "CategoriaIva",
      "cardinalidade": "1..1"
     }
    ],
    "propriedades": [
     {
      "nome": "baseTributavel",
      "tipo": "decimal",
      "descricao": "Base de incidência da taxa de IVA neste subtotal",
      "nomesAlternativos": [
       "VAT category taxable amount",
       "TaxableAmount"
      ]
     },
     {
      "nome": "montanteImposto",
      "tipo": "decimal",
      "descricao": "Imposto calculado sobre a base de incidência",
      "nomesAlternativos": [
       "VAT category tax amount",
       "TaxAmount"
      ]
     }
    ],
    "regras": [
     {
      "id": "RP-DECOMP-IMPOSTO",
      "natureza": "plausibilidade",
      "restricao": {
       "operador": "FUNCTION",
       "chamada": {
        "funcao": "produtoPercentualIgualA",
        "argumentos": [
         {
          "caminho": "baseTributavel"
         },
         {
          "caminho": "CategoriaIva.taxa"
         },
         {
          "caminho": "montanteImposto"
         },
         {
          "literal": 1.0
         }
        ]
       },
       "mensagem": "O imposto do subtotal tem de ser igual à base tributável vezes a taxa, com uma tolerância de 1,00 €."
      },
      "descricao": "produtoPercentualIgualA(DecomposicaoIva.baseTributavel, DecomposicaoIva.CategoriaIva.taxa, DecomposicaoIva.montanteImposto, 1)"
     },
     {
      "id": "RIR-DECOMP-ISENTO",
      "natureza": "inferencia_restritiva",
      "condicao": [
       {
        "propriedade": "CategoriaIva.codigoCategoria",
        "operador": "IN",
        "valor": [
         "E",
         "ISE"
        ]
       }
      ],
      "restricao": {
       "propriedade": "montanteImposto",
       "operador": "EQUALS",
       "valor": 0,
       "mensagem": "Num subtotal isento de IVA, o imposto tem de ser 0."
      },
      "descricao": "Se DecomposicaoIva.CategoriaIva.codigoCategoria ∈ {E, ISE} → DecomposicaoIva.montanteImposto = 0"
     },
     {
      "id": "RIR-DECOMP-ISENCAO",
      "natureza": "inferencia_restritiva",
      "condicao": [
       {
        "propriedade": "CategoriaIva.codigoCategoria",
        "operador": "IN",
        "valor": [
         "E",
         "ISE"
        ]
       }
      ],
      "restricao": {
       "operador": "FUNCTION",
       "chamada": {
        "funcao": "algumPresente",
        "argumentos": [
         {
          "caminho": "CategoriaIva.motivoIsencao"
         },
         {
          "caminho": "CategoriaIva.codigoMotivoIsencao"
         }
        ]
       },
       "mensagem": "Um subtotal isento de IVA tem de indicar o motivo de isenção ou o seu código."
      },
      "descricao": "Se DecomposicaoIva.CategoriaIva.codigoCategoria ∈ {E, ISE} → algumPresente(DecomposicaoIva.CategoriaIva.motivoIsencao, DecomposicaoIva.CategoriaIva.codigoMotivoIsencao)"
     },
     {
      "id": "RIR-DECOMP-SEM-ISENCAO",
      "natureza": "inferencia_restritiva",
      "condicao": [
       {
        "propriedade": "CategoriaIva.codigoCategoria",
        "operador": "IN",
        "valor": [
         "S",
         "NOR",
         "AA",
         "RED",
         "INT"
        ]
       }
      ],
      "restricao": {
       "operador": "FUNCTION",
       "chamada": {
        "funcao": "nenhumPresente",
        "argumentos": [
         {
          "caminho": "CategoriaIva.motivoIsencao"
         },
         {
          "caminho": "CategoriaIva.codigoMotivoIsencao"
         }
        ]
       },
       "mensagem": "Um subtotal de taxa normal, intermédia ou reduzida não pode ter motivo de isenção."
      },
      "descricao": "Se DecomposicaoIva.CategoriaIva.codigoCategoria ∈ {S, NOR, AA, RED, INT} → nenhumPresente(DecomposicaoIva.CategoriaIva.motivoIsencao, DecomposicaoIva.CategoriaIva.codigoMotivoIsencao)"
     }
    ]
   },
   {
    "nome": "DocumentoSuporte",
    "descricao": "Documento de suporte anexado ou referenciado: referência, descrição, localização externa ou ficheiro embebido.",
    "propriedades": [
     {
      "nome": "referencia",
      "tipo": "texto",
      "descricao": "Identificador do documento de suporte",
      "nomesAlternativos": [
       "Supporting document reference"
      ],
      "regras": [
       {
        "id": "RP-SUP-REF",
        "natureza": "plausibilidade",
        "restricao": {
         "propriedade": "referencia",
         "operador": "LENGTH",
         "valor": [
          1,
          50
         ],
         "mensagem": "A referência do documento de suporte tem de ter entre 1 e 50 caracteres."
        },
        "descricao": "DocumentoSuporte.referencia tem entre 1 e 50 caracteres"
       }
      ]
     },
     {
      "nome": "descricao",
      "tipo": "texto",
      "descricao": "Descrição do documento de suporte",
      "nomesAlternativos": [
       "DocumentDescription"
      ],
      "regras": [
       {
        "id": "RP-SUP-DESC",
        "natureza": "plausibilidade",
        "restricao": {
         "propriedade": "descricao",
         "operador": "LENGTH",
         "valor": [
          1,
          200
         ],
         "mensagem": "A descrição do documento de suporte tem de ter entre 1 e 200 caracteres."
        },
        "descricao": "DocumentoSuporte.descricao tem entre 1 e 200 caracteres"
       }
      ]
     },
     {
      "nome": "localizacaoExterna",
      "tipo": "texto",
      "descricao": "Endereço (URI) de um documento guardado externamente",
      "nomesAlternativos": [
       "External document location",
       "URI"
      ],
      "regras": [
       {
        "id": "RP-SUP-URI",
        "natureza": "plausibilidade",
        "restricao": {
         "propriedade": "localizacaoExterna",
         "operador": "LENGTH",
         "valor": [
          1,
          200
         ],
         "mensagem": "A localização externa tem de ter entre 1 e 200 caracteres."
        },
        "descricao": "DocumentoSuporte.localizacaoExterna tem entre 1 e 200 caracteres"
       }
      ]
     },
     {
      "nome": "anexo",
      "tipo": "texto",
      "descricao": "Conteúdo do documento anexado, codificado em base 64",
      "nomesAlternativos": [
       "Attached document",
       "EmbeddedDocumentBinaryObject"
      ],
      "regras": [
       {
        "id": "RP-SUP-ANEXO",
        "natureza": "plausibilidade",
        "restricao": {
         "propriedade": "anexo",
         "operador": "LENGTH",
         "valor": [
          1,
          6826666
         ],
         "mensagem": "O anexo não pode exceder 5 MB (6 826 666 caracteres em base 64)."
        },
        "descricao": "DocumentoSuporte.anexo tem entre 1 e 6826666 caracteres"
       }
      ]
     },
     {
      "nome": "tipoMime",
      "tipo": "texto",
      "descricao": "Tipo MIME do documento anexado",
      "nomesAlternativos": [
       "mimeCode"
      ],
      "regras": [
       {
        "id": "RP-SUP-MIME",
        "natureza": "plausibilidade",
        "restricao": {
         "propriedade": "tipoMime",
         "operador": "IN",
         "valor": [
          "text/plain",
          "image/png",
          "image/jpeg",
          "application/pdf",
          "application/msword",
          "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
          "application/vnd.ms-excel",
          "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
          "application/xml",
          "text/xml",
          "text/csv"
         ],
         "mensagem": "O tipo do anexo tem de ser texto, PNG, JPEG, PDF, Word, Excel, XML ou CSV."
        },
        "descricao": "DocumentoSuporte.tipoMime ∈ {text/plain, image/png, image/jpeg, application/pdf, application/msword, application/vnd.openxmlformats-officedocument.wordprocessingml.document, application/vnd.ms-excel, application/vnd.openxmlformats-officedocument.spreadsheetml.sheet, application/xml, text/xml, text/csv}"
       }
      ]
     },
     {
      "nome": "nomeFicheiro",
      "tipo": "texto",
      "descricao": "Nome do ficheiro anexado",
      "nomesAlternativos": [
       "filename"
      ],
      "regras": [
       {
        "id": "RP-SUP-FICHEIRO",
        "natureza": "plausibilidade",
        "restricao": {
         "propriedade": "nomeFicheiro",
         "operador": "LENGTH",
         "valor": [
          1,
          50
         ],
         "mensagem": "O nome do ficheiro anexado tem de ter entre 1 e 50 caracteres."
        },
        "descricao": "DocumentoSuporte.nomeFicheiro tem entre 1 e 50 caracteres"
       }
      ]
     }
    ],
    "regras": [
     {
      "id": "RP-SUP-CONTEUDO",
      "natureza": "plausibilidade",
      "restricao": {
       "operador": "FUNCTION",
       "chamada": {
        "funcao": "algumPresente",
        "argumentos": [
         {
          "caminho": "localizacaoExterna"
         },
         {
          "caminho": "anexo"
         }
        ]
       },
       "mensagem": "Um documento de suporte tem de indicar a localização externa, o anexo ou ambos."
      },
      "descricao": "algumPresente(DocumentoSuporte.localizacaoExterna, DocumentoSuporte.anexo)"
     },
     {
      "id": "RIR-SUP-MIME",
      "natureza": "inferencia_restritiva",
      "condicao": [
       {
        "operador": "FUNCTION",
        "chamada": {
         "funcao": "existe",
         "argumentos": [
          {
           "caminho": "anexo"
          }
         ]
        }
       }
      ],
      "restricao": {
       "operador": "FUNCTION",
       "chamada": {
        "funcao": "existe",
        "argumentos": [
         {
          "caminho": "tipoMime"
         }
        ]
       },
       "mensagem": "Um documento anexado tem de indicar o tipo MIME."
      },
      "descricao": "Se existe(DocumentoSuporte.anexo) → existe(DocumentoSuporte.tipoMime)"
     },
     {
      "id": "RIR-SUP-FICHEIRO",
      "natureza": "inferencia_restritiva",
      "condicao": [
       {
        "operador": "FUNCTION",
        "chamada": {
         "funcao": "existe",
         "argumentos": [
          {
           "caminho": "anexo"
          }
         ]
        }
       }
      ],
      "restricao": {
       "operador": "FUNCTION",
       "chamada": {
        "funcao": "existe",
        "argumentos": [
         {
          "caminho": "nomeFicheiro"
         }
        ]
       },
       "mensagem": "Um documento anexado tem de indicar o nome do ficheiro."
      },
      "descricao": "Se existe(DocumentoSuporte.anexo) → existe(DocumentoSuporte.nomeFicheiro)"
     }
    ]
   },
   {
    "nome": "LinhaDocumento",
    "descricao": "Linha do documento: bem ou serviço faturado, com quantidade, preço, descontos, encargos, IVA e montante líquido.",
    "composicao": [
     {
      "usm": "Artigo",
      "cardinalidade": "1..1"
     },
     {
      "usm": "Preco",
      "cardinalidade": "1..1"
     },
     {
      "usm": "CategoriaIva",
      "cardinalidade": "1..1"
     },
     {
      "usm": "Periodo",
      "cardinalidade": "0..1"
     },
     {
      "usm": "DescontoEncargo",
      "papel": "Desconto",
      "cardinalidade": "0..*"
     },
     {
      "usm": "DescontoEncargo",
      "papel": "Encargo",
      "cardinalidade": "0..*"
     },
     {
      "usm": "AtributoArtigo",
      "cardinalidade": "0..*"
     }
    ],
    "propriedades": [
     {
      "nome": "identificador",
      "tipo": "texto",
      "descricao": "Identificador único da linha no documento, atribuído pelo fornecedor",
      "nomesAlternativos": [
       "Invoice line identifier"
      ],
      "regras": [
       {
        "id": "RP-LIN-ID",
        "natureza": "plausibilidade",
        "restricao": {
         "propriedade": "identificador",
         "operador": "LENGTH",
         "valor": [
          1,
          50
         ],
         "mensagem": "O identificador da linha tem de ter entre 1 e 50 caracteres."
        },
        "descricao": "LinhaDocumento.identificador tem entre 1 e 50 caracteres"
       }
      ]
     },
     {
      "nome": "nota",
      "tipo": "texto",
      "descricao": "Observação em texto livre sobre a linha",
      "nomesAlternativos": [
       "Invoice line note"
      ],
      "regras": [
       {
        "id": "RP-LIN-NOTA",
        "natureza": "plausibilidade",
        "restricao": {
         "propriedade": "nota",
         "operador": "LENGTH",
         "valor": [
          1,
          500
         ],
         "mensagem": "A nota da linha tem de ter entre 1 e 500 caracteres."
        },
        "descricao": "LinhaDocumento.nota tem entre 1 e 500 caracteres"
       }
      ]
     },
     {
      "nome": "identificadorObjeto",
      "tipo": "texto",
      "descricao": "Identificador do objeto em que a linha se baseia, dado pelo fornecedor",
      "nomesAlternativos": [
       "Invoice line object identifier"
      ],
      "regras": [
       {
        "id": "RP-LIN-OBJETO",
        "natureza": "plausibilidade",
        "restricao": {
         "propriedade": "identificadorObjeto",
         "operador": "LENGTH",
         "valor": [
          1,
          50
         ],
         "mensagem": "O identificador do objeto da linha tem de ter entre 1 e 50 caracteres."
        },
        "descricao": "LinhaDocumento.identificadorObjeto tem entre 1 e 50 caracteres"
       }
      ]
     },
     {
      "nome": "quantidade",
      "tipo": "decimal",
      "descricao": "Quantidade faturada do bem ou serviço",
      "nomesAlternativos": [
       "Invoiced quantity",
       "InvoicedQuantity",
       "CreditedQuantity"
      ]
     },
     {
      "nome": "unidadeMedida",
      "tipo": "texto",
      "descricao": "Unidade de medida da quantidade faturada (UN/ECE Rec. 20 e 21)",
      "nomesAlternativos": [
       "Invoiced quantity unit of measure code",
       "unitCode"
      ],
      "regras": [
       {
        "id": "RP-LIN-UNIDADE",
        "natureza": "plausibilidade",
        "restricao": {
         "propriedade": "unidadeMedida",
         "operador": "PATTERN",
         "valor": "^[A-Z0-9]{1,3}$",
         "mensagem": "A unidade de medida tem de ser um código UN/ECE Rec. 20 (1 a 3 letras ou algarismos)."
        },
        "descricao": "LinhaDocumento.unidadeMedida segue o padrão ^[A-Z0-9]{1,3}$"
       }
      ]
     },
     {
      "nome": "montanteLiquido",
      "tipo": "decimal",
      "descricao": "Montante da linha sem IVA, já com os descontos e encargos da linha",
      "nomesAlternativos": [
       "Invoice line net amount",
       "LineExtensionAmount"
      ]
     },
     {
      "nome": "referenciaLinhaEncomenda",
      "tipo": "texto",
      "descricao": "Referência da linha da nota de encomenda do cliente",
      "nomesAlternativos": [
       "Referenced purchase order line reference"
      ],
      "regras": [
       {
        "id": "RP-LIN-REFENC",
        "natureza": "plausibilidade",
        "restricao": {
         "propriedade": "referenciaLinhaEncomenda",
         "operador": "LENGTH",
         "valor": [
          1,
          20
         ],
         "mensagem": "A referência da linha de encomenda tem de ter entre 1 e 20 caracteres."
        },
        "descricao": "LinhaDocumento.referenciaLinhaEncomenda tem entre 1 e 20 caracteres"
       }
      ]
     },
     {
      "nome": "numeroCompromisso",
      "tipo": "texto",
      "descricao": "Número do compromisso associado à linha",
      "nomesAlternativos": [
       "AccountingCost"
      ],
      "regras": [
       {
        "id": "RP-LIN-COMPROMISSO",
        "natureza": "plausibilidade",
        "restricao": {
         "propriedade": "numeroCompromisso",
         "operador": "LENGTH",
         "valor": [
          1,
          200
         ],
         "mensagem": "O número do compromisso da linha tem de ter entre 1 e 200 caracteres."
        },
        "descricao": "LinhaDocumento.numeroCompromisso tem entre 1 e 200 caracteres"
       }
      ]
     }
    ],
    "regras": [
     {
      "id": "RP-LIN-MONTANTE",
      "natureza": "plausibilidade",
      "restricao": {
       "operador": "FUNCTION",
       "chamada": {
        "funcao": "montanteLinhaCoerente",
        "argumentos": [
         {
          "caminho": "quantidade"
         },
         {
          "caminho": "Preco.precoLiquido"
         },
         {
          "caminho": "Preco.quantidadeBase"
         },
         {
          "caminho": "Desconto.montante"
         },
         {
          "caminho": "Encargo.montante"
         },
         {
          "caminho": "montanteLiquido"
         },
         {
          "literal": 1.0
         }
        ]
       },
       "mensagem": "O montante da linha tem de ser igual a quantidade × preço / quantidade base, menos os descontos e mais os encargos da linha, com uma tolerância de 1,00 €."
      },
      "descricao": "montanteLinhaCoerente(LinhaDocumento.quantidade, LinhaDocumento.Preco.precoLiquido, LinhaDocumento.Preco.quantidadeBase, LinhaDocumento.Desconto.montante, LinhaDocumento.Encargo.montante, LinhaDocumento.montanteLiquido, 1)"
     },
     {
      "id": "RIR-LIN-ISENCAO",
      "natureza": "inferencia_restritiva",
      "condicao": [
       {
        "propriedade": "CategoriaIva.codigoCategoria",
        "operador": "IN",
        "valor": [
         "E",
         "ISE"
        ]
       }
      ],
      "restricao": {
       "operador": "FUNCTION",
       "chamada": {
        "funcao": "algumPresente",
        "argumentos": [
         {
          "caminho": "CategoriaIva.motivoIsencao"
         },
         {
          "caminho": "CategoriaIva.codigoMotivoIsencao"
         }
        ]
       },
       "mensagem": "Uma linha isenta de IVA tem de indicar o motivo de isenção ou o seu código."
      },
      "descricao": "Se LinhaDocumento.CategoriaIva.codigoCategoria ∈ {E, ISE} → algumPresente(LinhaDocumento.CategoriaIva.motivoIsencao, LinhaDocumento.CategoriaIva.codigoMotivoIsencao)"
     },
     {
      "id": "RIR-LIN-SEM-ISENCAO",
      "natureza": "inferencia_restritiva",
      "condicao": [
       {
        "propriedade": "CategoriaIva.codigoCategoria",
        "operador": "IN",
        "valor": [
         "S",
         "NOR",
         "AA",
         "RED",
         "INT"
        ]
       }
      ],
      "restricao": {
       "operador": "FUNCTION",
       "chamada": {
        "funcao": "nenhumPresente",
        "argumentos": [
         {
          "caminho": "CategoriaIva.motivoIsencao"
         },
         {
          "caminho": "CategoriaIva.codigoMotivoIsencao"
         }
        ]
       },
       "mensagem": "Uma linha de taxa normal, intermédia ou reduzida não pode ter motivo de isenção."
      },
      "descricao": "Se LinhaDocumento.CategoriaIva.codigoCategoria ∈ {S, NOR, AA, RED, INT} → nenhumPresente(LinhaDocumento.CategoriaIva.motivoIsencao, LinhaDocumento.CategoriaIva.codigoMotivoIsencao)"
     }
    ]
   }
  ],
  "hlm": [
   {
    "nome": "DocumentoFaturacao",
    "descricao": "Documento de faturação eletrónica CIUS-PT (fatura, nota de crédito, nota de débito, adiantamento, autofaturação): partes, referências, linhas, descontos, encargos, IVA e totais.",
    "notas": "O nome Fatura já está ocupado por outro HLM, com outra estrutura; este é o BG-0 do modelo semântico EN 16931 / CIUS-PT.",
    "composicao": [
     {
      "sm": "CabecalhoDocumento",
      "cardinalidade": "1..1"
     },
     {
      "sm": "ReferenciasDocumento",
      "cardinalidade": "0..1"
     },
     {
      "sm": "NotaDocumento",
      "cardinalidade": "0..*"
     },
     {
      "sm": "DocumentosAnteriores",
      "cardinalidade": "0..1"
     },
     {
      "sm": "Fornecedor",
      "cardinalidade": "1..1"
     },
     {
      "sm": "Adquirente",
      "cardinalidade": "1..1"
     },
     {
      "sm": "RecebedorPagamento",
      "cardinalidade": "0..1"
     },
     {
      "sm": "RepresentanteFiscal",
      "cardinalidade": "0..1"
     },
     {
      "sm": "LocalEntrega",
      "cardinalidade": "0..*"
     },
     {
      "sm": "PeriodoFaturacao",
      "cardinalidade": "0..1"
     },
     {
      "sm": "Pagamento",
      "cardinalidade": "0..1"
     },
     {
      "sm": "DescontoEncargoDocumento",
      "papel": "Desconto",
      "cardinalidade": "0..*"
     },
     {
      "sm": "DescontoEncargoDocumento",
      "papel": "Encargo",
      "cardinalidade": "0..*"
     },
     {
      "sm": "Totais",
      "cardinalidade": "1..1"
     },
     {
      "sm": "DecomposicaoIva",
      "cardinalidade": "1..*"
     },
     {
      "sm": "DocumentoSuporte",
      "cardinalidade": "0..*"
     },
     {
      "sm": "LinhaDocumento",
      "cardinalidade": "1..*"
     },
     {
      "sm": "Metainformacao",
      "papel": "Metainformacao",
      "cardinalidade": "0..1"
     }
    ],
    "regras": [
     {
      "id": "RP-SOMA-LINHAS",
      "natureza": "plausibilidade",
      "restricao": {
       "operador": "FUNCTION",
       "chamada": {
        "funcao": "somaIgualATolerancia",
        "argumentos": [
         {
          "caminho": "LinhaDocumento.montanteLiquido"
         },
         {
          "caminho": "Totais.somaLinhas"
         },
         {
          "literal": 1.0
         }
        ]
       },
       "mensagem": "A soma dos montantes das linhas tem de ser igual à soma dos montantes líquidos de todas as linhas, com uma tolerância de 1,00 €."
      },
      "descricao": "somaIgualATolerancia(LinhaDocumento.montanteLiquido, Totais.somaLinhas, 1)"
     },
     {
      "id": "RP-SOMA-DESCONTOS",
      "natureza": "plausibilidade",
      "restricao": {
       "operador": "FUNCTION",
       "chamada": {
        "funcao": "somaIgualATolerancia",
        "argumentos": [
         {
          "caminho": "Desconto.DescontoEncargo.montante"
         },
         {
          "caminho": "Totais.totalDescontos"
         },
         {
          "literal": 1.0
         }
        ]
       },
       "mensagem": "O total dos descontos tem de ser igual à soma dos descontos ao nível do documento, com uma tolerância de 1,00 €."
      },
      "descricao": "somaIgualATolerancia(Desconto.DescontoEncargo.montante, Totais.totalDescontos, 1)"
     },
     {
      "id": "RP-SOMA-ENCARGOS",
      "natureza": "plausibilidade",
      "restricao": {
       "operador": "FUNCTION",
       "chamada": {
        "funcao": "somaIgualATolerancia",
        "argumentos": [
         {
          "caminho": "Encargo.DescontoEncargo.montante"
         },
         {
          "caminho": "Totais.totalEncargos"
         },
         {
          "literal": 1.0
         }
        ]
       },
       "mensagem": "O total dos encargos tem de ser igual à soma dos encargos ao nível do documento, com uma tolerância de 1,00 €."
      },
      "descricao": "somaIgualATolerancia(Encargo.DescontoEncargo.montante, Totais.totalEncargos, 1)"
     },
     {
      "id": "RP-SOMA-IVA",
      "natureza": "plausibilidade",
      "restricao": {
       "operador": "FUNCTION",
       "chamada": {
        "funcao": "somaIgualATolerancia",
        "argumentos": [
         {
          "caminho": "DecomposicaoIva.montanteImposto"
         },
         {
          "caminho": "Totais.totalIva"
         },
         {
          "literal": 1.0
         }
        ]
       },
       "mensagem": "O total do IVA tem de ser igual à soma dos impostos da decomposição do IVA, com uma tolerância de 1,00 €."
      },
      "descricao": "somaIgualATolerancia(DecomposicaoIva.montanteImposto, Totais.totalIva, 1)"
     },
     {
      "id": "RP-IVA-BASE",
      "natureza": "plausibilidade",
      "restricao": {
       "operador": "FUNCTION",
       "chamada": {
        "funcao": "baseTributavelCoerente",
        "argumentos": [
         {
          "caminho": "DecomposicaoIva"
         },
         {
          "caminho": "LinhaDocumento"
         },
         {
          "caminho": "Desconto"
         },
         {
          "caminho": "Encargo"
         },
         {
          "literal": 1.0
         }
        ]
       },
       "mensagem": "A base tributável de cada subtotal de IVA tem de ser igual à soma das linhas, mais os encargos e menos os descontos da mesma categoria e taxa, com uma tolerância de 1,00 €."
      },
      "descricao": "baseTributavelCoerente(DecomposicaoIva, LinhaDocumento, Desconto, Encargo, 1)"
     },
     {
      "id": "RP-IVA-DECOMP",
      "natureza": "plausibilidade",
      "restricao": {
       "operador": "FUNCTION",
       "chamada": {
        "funcao": "categoriasIvaDecompostas",
        "argumentos": [
         {
          "caminho": "LinhaDocumento.CategoriaIva.codigoCategoria"
         },
         {
          "caminho": "Desconto.CategoriaIva.codigoCategoria"
         },
         {
          "caminho": "Encargo.CategoriaIva.codigoCategoria"
         },
         {
          "caminho": "DecomposicaoIva.CategoriaIva.codigoCategoria"
         }
        ]
       },
       "mensagem": "Cada categoria de IVA usada nas linhas, nos descontos ou nos encargos tem de aparecer na decomposição do IVA."
      },
      "descricao": "categoriasIvaDecompostas(LinhaDocumento.CategoriaIva.codigoCategoria, Desconto.CategoriaIva.codigoCategoria, Encargo.CategoriaIva.codigoCategoria, DecomposicaoIva.CategoriaIva.codigoCategoria)"
     },
     {
      "id": "RP-LIN-UNICAS",
      "natureza": "plausibilidade",
      "restricao": {
       "operador": "FUNCTION",
       "chamada": {
        "funcao": "valoresTextoUnicos",
        "argumentos": [
         {
          "caminho": "LinhaDocumento.identificador"
         }
        ]
       },
       "mensagem": "Os identificadores das linhas não se podem repetir no documento."
      },
      "descricao": "valoresTextoUnicos(LinhaDocumento.identificador)"
     },
     {
      "id": "RP-LENT-MORADA",
      "natureza": "plausibilidade",
      "restricao": {
       "operador": "FUNCTION",
       "chamada": {
        "funcao": "colecaoNaoVazia",
        "argumentos": [
         {
          "caminho": "LocalEntrega.Morada.rua"
         }
        ]
       },
       "mensagem": "O documento tem de indicar pelo menos uma morada de entrega."
      },
      "descricao": "colecaoNaoVazia(LocalEntrega.Morada.rua)"
     },
     {
      "id": "RIR-PAGAMENTO-PRAZO",
      "natureza": "inferencia_restritiva",
      "condicao": [
       {
        "propriedade": "Totais.valorPagar",
        "operador": "GT",
        "valor": 0
       }
      ],
      "restricao": {
       "operador": "FUNCTION",
       "chamada": {
        "funcao": "algumPresente",
        "argumentos": [
         {
          "caminho": "CabecalhoDocumento.dataVencimento"
         },
         {
          "caminho": "CabecalhoDocumento.condicoesPagamento"
         }
        ]
       },
       "mensagem": "Com valor a pagar positivo, é obrigatório indicar a data de vencimento ou as condições de pagamento."
      },
      "descricao": "Se Totais.valorPagar > 0 → algumPresente(CabecalhoDocumento.dataVencimento, CabecalhoDocumento.condicoesPagamento)"
     },
     {
      "id": "RIR-REFANT-ND",
      "natureza": "inferencia_restritiva",
      "condicao": [
       {
        "propriedade": "CabecalhoDocumento.tipoDocumento",
        "operador": "IN",
        "valor": [
         "383",
         "ND"
        ]
       }
      ],
      "restricao": {
       "operador": "FUNCTION",
       "chamada": {
        "funcao": "colecaoNaoVazia",
        "argumentos": [
         {
          "caminho": "DocumentosAnteriores.ReferenciaDocumento.numero"
         }
        ]
       },
       "mensagem": "Uma nota de débito tem de referenciar o documento anterior a que respeita."
      },
      "descricao": "Se CabecalhoDocumento.tipoDocumento ∈ {383, ND} → colecaoNaoVazia(DocumentosAnteriores.ReferenciaDocumento.numero)"
     },
     {
      "id": "RIR-REFANT-NC",
      "natureza": "inferencia_restritiva",
      "condicao": [
       {
        "propriedade": "CabecalhoDocumento.tipoDocumento",
        "operador": "IN",
        "valor": [
         "381",
         "NC"
        ]
       }
      ],
      "restricao": {
       "operador": "FUNCTION",
       "chamada": {
        "funcao": "colecaoNaoVazia",
        "argumentos": [
         {
          "caminho": "DocumentosAnteriores.ReferenciaDocumento.numero"
         }
        ]
       },
       "mensagem": "Uma nota de crédito tem de referenciar a fatura original."
      },
      "descricao": "Se CabecalhoDocumento.tipoDocumento ∈ {381, NC} → colecaoNaoVazia(DocumentosAnteriores.ReferenciaDocumento.numero)"
     },
     {
      "id": "RIR-TOT-DESCONTOS",
      "natureza": "inferencia_restritiva",
      "condicao": [
       {
        "operador": "FUNCTION",
        "chamada": {
         "funcao": "colecaoNaoVazia",
         "argumentos": [
          {
           "caminho": "Desconto.DescontoEncargo.montante"
          }
         ]
        }
       }
      ],
      "restricao": {
       "operador": "FUNCTION",
       "chamada": {
        "funcao": "existe",
        "argumentos": [
         {
          "caminho": "Totais.totalDescontos"
         }
        ]
       },
       "mensagem": "Se houver descontos ao nível do documento, o total dos descontos é obrigatório."
      },
      "descricao": "Se colecaoNaoVazia(Desconto.DescontoEncargo.montante) → existe(Totais.totalDescontos)"
     },
     {
      "id": "RIR-TOT-ENCARGOS",
      "natureza": "inferencia_restritiva",
      "condicao": [
       {
        "operador": "FUNCTION",
        "chamada": {
         "funcao": "colecaoNaoVazia",
         "argumentos": [
          {
           "caminho": "Encargo.DescontoEncargo.montante"
          }
         ]
        }
       }
      ],
      "restricao": {
       "operador": "FUNCTION",
       "chamada": {
        "funcao": "existe",
        "argumentos": [
         {
          "caminho": "Totais.totalEncargos"
         }
        ]
       },
       "mensagem": "Se houver encargos ao nível do documento, o total dos encargos é obrigatório."
      },
      "descricao": "Se colecaoNaoVazia(Encargo.DescontoEncargo.montante) → existe(Totais.totalEncargos)"
     }
    ]
   }
  ],
  "projecoes": [
   {
    "nome": "FaturaCiusPt",
    "hlm": "DocumentoFaturacao",
    "descricao": "Fatura eletrónica CIUS-PT para entidades públicas (380) e documentos com a mesma estrutura: nota de débito (383), fatura de adiantamento (386) e autofaturação (389).",
    "obrigatorias": [
     "CabecalhoDocumento.numero",
     "CabecalhoDocumento.dataEmissao",
     "CabecalhoDocumento.tipoDocumento",
     "CabecalhoDocumento.moeda",
     "CabecalhoDocumento.identificadorEspecificacao",
     "Fornecedor.SujeitoPassivo.nome",
     "Fornecedor.SujeitoPassivo.identificadorIva",
     "Fornecedor.Morada.rua",
     "Fornecedor.Morada.localidade",
     "Fornecedor.Morada.codigoPostal",
     "Fornecedor.Morada.pais",
     "Adquirente.SujeitoPassivo.nome",
     "Adquirente.SujeitoPassivo.identificadorIva",
     "Adquirente.Morada.pais",
     "DocumentosAnteriores.ReferenciaDocumento.numero",
     "RecebedorPagamento.SujeitoPassivo.nome",
     "RepresentanteFiscal.SujeitoPassivo.nome",
     "RepresentanteFiscal.SujeitoPassivo.identificadorIva",
     "RepresentanteFiscal.Morada.pais",
     "LocalEntrega.Morada.rua",
     "LocalEntrega.Morada.localidade",
     "LocalEntrega.Morada.codigoPostal",
     "LocalEntrega.Morada.pais",
     "Pagamento.meioPagamento",
     "Pagamento.ContaBancaria.iban",
     "Pagamento.CartaoPagamento.numeroConta",
     "Desconto.DescontoEncargo.montante",
     "Desconto.CategoriaIva.codigoCategoria",
     "Desconto.CategoriaIva.taxa",
     "Encargo.DescontoEncargo.montante",
     "Encargo.CategoriaIva.codigoCategoria",
     "Encargo.CategoriaIva.taxa",
     "Totais.somaLinhas",
     "Totais.totalSemIva",
     "Totais.totalIva",
     "Totais.totalComIva",
     "Totais.valorPagar",
     "DecomposicaoIva.baseTributavel",
     "DecomposicaoIva.montanteImposto",
     "DecomposicaoIva.CategoriaIva.codigoCategoria",
     "DecomposicaoIva.CategoriaIva.taxa",
     "DocumentoSuporte.referencia",
     "NotaDocumento.texto",
     "LinhaDocumento.identificador",
     "LinhaDocumento.quantidade",
     "LinhaDocumento.unidadeMedida",
     "LinhaDocumento.montanteLiquido",
     "LinhaDocumento.Artigo.nome",
     "LinhaDocumento.Preco.precoLiquido",
     "LinhaDocumento.CategoriaIva.codigoCategoria",
     "LinhaDocumento.CategoriaIva.taxa",
     "LinhaDocumento.Desconto.montante",
     "LinhaDocumento.Encargo.montante",
     "LinhaDocumento.AtributoArtigo.nome",
     "LinhaDocumento.AtributoArtigo.valor"
    ],
    "permitidas": [
     "CabecalhoDocumento.moedaIva",
     "CabecalhoDocumento.dataIva",
     "CabecalhoDocumento.codigoDataIva",
     "CabecalhoDocumento.dataVencimento",
     "CabecalhoDocumento.referenciaCliente",
     "CabecalhoDocumento.numeroCompromisso",
     "CabecalhoDocumento.condicoesPagamento",
     "CabecalhoDocumento.tipoProcesso",
     "ReferenciasDocumento.*",
     "NotaDocumento.assunto",
     "DocumentosAnteriores.ReferenciaDocumento.dataEmissao",
     "Fornecedor.SujeitoPassivo.nomeComercial",
     "Fornecedor.SujeitoPassivo.identificador",
     "Fornecedor.SujeitoPassivo.identificadorRegisto",
     "Fornecedor.Morada.freguesia",
     "Fornecedor.ComplementoMorada.*",
     "Fornecedor.ContactoTelefonico.telefone",
     "Fornecedor.Contacto.email",
     "Fornecedor.registoFiscal",
     "Fornecedor.capitalSocial",
     "Fornecedor.enderecoEletronico",
     "Fornecedor.pontoContacto",
     "Adquirente.SujeitoPassivo.nomeComercial",
     "Adquirente.SujeitoPassivo.identificador",
     "Adquirente.SujeitoPassivo.identificadorRegisto",
     "Adquirente.Morada.rua",
     "Adquirente.Morada.localidade",
     "Adquirente.Morada.codigoPostal",
     "Adquirente.Morada.freguesia",
     "Adquirente.ComplementoMorada.*",
     "Adquirente.ContactoTelefonico.telefone",
     "Adquirente.Contacto.email",
     "Adquirente.enderecoEletronico",
     "Adquirente.pontoContacto",
     "RecebedorPagamento.SujeitoPassivo.identificador",
     "RecebedorPagamento.SujeitoPassivo.identificadorRegisto",
     "RepresentanteFiscal.Morada.rua",
     "RepresentanteFiscal.Morada.localidade",
     "RepresentanteFiscal.Morada.codigoPostal",
     "RepresentanteFiscal.Morada.freguesia",
     "RepresentanteFiscal.ComplementoMorada.*",
     "LocalEntrega.nomeLocal",
     "LocalEntrega.identificadorLocal",
     "LocalEntrega.dataEntrega",
     "LocalEntrega.Morada.freguesia",
     "LocalEntrega.ComplementoMorada.*",
     "PeriodoFaturacao.*",
     "Pagamento.detalhePagamento",
     "Pagamento.referenciaPagamento",
     "Pagamento.ContaBancaria.nomeConta",
     "Pagamento.ContaBancaria.bic",
     "Pagamento.CartaoPagamento.titular",
     "Pagamento.DebitoDireto.*",
     "Desconto.DescontoEncargo.montanteBase",
     "Desconto.DescontoEncargo.percentagem",
     "Desconto.DescontoEncargo.motivo",
     "Desconto.DescontoEncargo.codigoMotivo",
     "Encargo.DescontoEncargo.montanteBase",
     "Encargo.DescontoEncargo.percentagem",
     "Encargo.DescontoEncargo.motivo",
     "Encargo.DescontoEncargo.codigoMotivo",
     "Totais.totalDescontos",
     "Totais.totalEncargos",
     "Totais.totalIvaMoedaContabilistica",
     "Totais.valorPago",
     "Totais.arredondamento",
     "DecomposicaoIva.CategoriaIva.motivoIsencao",
     "DecomposicaoIva.CategoriaIva.codigoMotivoIsencao",
     "DocumentoSuporte.descricao",
     "DocumentoSuporte.localizacaoExterna",
     "DocumentoSuporte.anexo",
     "DocumentoSuporte.tipoMime",
     "DocumentoSuporte.nomeFicheiro",
     "LinhaDocumento.nota",
     "LinhaDocumento.identificadorObjeto",
     "LinhaDocumento.referenciaLinhaEncomenda",
     "LinhaDocumento.numeroCompromisso",
     "LinhaDocumento.Periodo.*",
     "LinhaDocumento.Desconto.montanteBase",
     "LinhaDocumento.Desconto.percentagem",
     "LinhaDocumento.Desconto.motivo",
     "LinhaDocumento.Desconto.codigoMotivo",
     "LinhaDocumento.Encargo.montanteBase",
     "LinhaDocumento.Encargo.percentagem",
     "LinhaDocumento.Encargo.motivo",
     "LinhaDocumento.Encargo.codigoMotivo",
     "LinhaDocumento.Preco.descontoPreco",
     "LinhaDocumento.Preco.precoBruto",
     "LinhaDocumento.Preco.quantidadeBase",
     "LinhaDocumento.Preco.unidadeQuantidadeBase",
     "LinhaDocumento.CategoriaIva.motivoIsencao",
     "LinhaDocumento.CategoriaIva.codigoMotivoIsencao",
     "LinhaDocumento.Artigo.descricao",
     "LinhaDocumento.Artigo.codigo",
     "LinhaDocumento.Artigo.codigoComprador",
     "LinhaDocumento.Artigo.codigoBarras",
     "LinhaDocumento.Artigo.classificacao",
     "LinhaDocumento.Artigo.paisOrigem",
     "Metainformacao.*"
    ]
   },
   {
    "nome": "NotaCreditoCiusPt",
    "hlm": "DocumentoFaturacao",
    "descricao": "Nota de crédito CIUS-PT (381), incluindo a nota de crédito de rappel; o modelo UBL da nota de crédito não tem a data efetiva de entrega.",
    "obrigatorias": [
     "CabecalhoDocumento.numero",
     "CabecalhoDocumento.dataEmissao",
     "CabecalhoDocumento.tipoDocumento",
     "CabecalhoDocumento.moeda",
     "CabecalhoDocumento.identificadorEspecificacao",
     "Fornecedor.SujeitoPassivo.nome",
     "Fornecedor.SujeitoPassivo.identificadorIva",
     "Fornecedor.Morada.rua",
     "Fornecedor.Morada.localidade",
     "Fornecedor.Morada.codigoPostal",
     "Fornecedor.Morada.pais",
     "Adquirente.SujeitoPassivo.nome",
     "Adquirente.SujeitoPassivo.identificadorIva",
     "Adquirente.Morada.pais",
     "DocumentosAnteriores.ReferenciaDocumento.numero",
     "RecebedorPagamento.SujeitoPassivo.nome",
     "RepresentanteFiscal.SujeitoPassivo.nome",
     "RepresentanteFiscal.SujeitoPassivo.identificadorIva",
     "RepresentanteFiscal.Morada.pais",
     "LocalEntrega.Morada.rua",
     "LocalEntrega.Morada.localidade",
     "LocalEntrega.Morada.codigoPostal",
     "LocalEntrega.Morada.pais",
     "Pagamento.meioPagamento",
     "Pagamento.ContaBancaria.iban",
     "Pagamento.CartaoPagamento.numeroConta",
     "Desconto.DescontoEncargo.montante",
     "Desconto.CategoriaIva.codigoCategoria",
     "Desconto.CategoriaIva.taxa",
     "Encargo.DescontoEncargo.montante",
     "Encargo.CategoriaIva.codigoCategoria",
     "Encargo.CategoriaIva.taxa",
     "Totais.somaLinhas",
     "Totais.totalSemIva",
     "Totais.totalIva",
     "Totais.totalComIva",
     "Totais.valorPagar",
     "DecomposicaoIva.baseTributavel",
     "DecomposicaoIva.montanteImposto",
     "DecomposicaoIva.CategoriaIva.codigoCategoria",
     "DecomposicaoIva.CategoriaIva.taxa",
     "DocumentoSuporte.referencia",
     "NotaDocumento.texto",
     "LinhaDocumento.identificador",
     "LinhaDocumento.quantidade",
     "LinhaDocumento.unidadeMedida",
     "LinhaDocumento.montanteLiquido",
     "LinhaDocumento.Artigo.nome",
     "LinhaDocumento.Preco.precoLiquido",
     "LinhaDocumento.CategoriaIva.codigoCategoria",
     "LinhaDocumento.CategoriaIva.taxa",
     "LinhaDocumento.Desconto.montante",
     "LinhaDocumento.Encargo.montante",
     "LinhaDocumento.AtributoArtigo.nome",
     "LinhaDocumento.AtributoArtigo.valor"
    ],
    "permitidas": [
     "CabecalhoDocumento.moedaIva",
     "CabecalhoDocumento.dataIva",
     "CabecalhoDocumento.codigoDataIva",
     "CabecalhoDocumento.dataVencimento",
     "CabecalhoDocumento.referenciaCliente",
     "CabecalhoDocumento.numeroCompromisso",
     "CabecalhoDocumento.condicoesPagamento",
     "CabecalhoDocumento.tipoProcesso",
     "ReferenciasDocumento.*",
     "NotaDocumento.assunto",
     "DocumentosAnteriores.ReferenciaDocumento.dataEmissao",
     "Fornecedor.SujeitoPassivo.nomeComercial",
     "Fornecedor.SujeitoPassivo.identificador",
     "Fornecedor.SujeitoPassivo.identificadorRegisto",
     "Fornecedor.Morada.freguesia",
     "Fornecedor.ComplementoMorada.*",
     "Fornecedor.ContactoTelefonico.telefone",
     "Fornecedor.Contacto.email",
     "Fornecedor.registoFiscal",
     "Fornecedor.capitalSocial",
     "Fornecedor.enderecoEletronico",
     "Fornecedor.pontoContacto",
     "Adquirente.SujeitoPassivo.nomeComercial",
     "Adquirente.SujeitoPassivo.identificador",
     "Adquirente.SujeitoPassivo.identificadorRegisto",
     "Adquirente.Morada.rua",
     "Adquirente.Morada.localidade",
     "Adquirente.Morada.codigoPostal",
     "Adquirente.Morada.freguesia",
     "Adquirente.ComplementoMorada.*",
     "Adquirente.ContactoTelefonico.telefone",
     "Adquirente.Contacto.email",
     "Adquirente.enderecoEletronico",
     "Adquirente.pontoContacto",
     "RecebedorPagamento.SujeitoPassivo.identificador",
     "RecebedorPagamento.SujeitoPassivo.identificadorRegisto",
     "RepresentanteFiscal.Morada.rua",
     "RepresentanteFiscal.Morada.localidade",
     "RepresentanteFiscal.Morada.codigoPostal",
     "RepresentanteFiscal.Morada.freguesia",
     "RepresentanteFiscal.ComplementoMorada.*",
     "LocalEntrega.nomeLocal",
     "LocalEntrega.identificadorLocal",
     "LocalEntrega.Morada.freguesia",
     "LocalEntrega.ComplementoMorada.*",
     "PeriodoFaturacao.*",
     "Pagamento.detalhePagamento",
     "Pagamento.referenciaPagamento",
     "Pagamento.ContaBancaria.nomeConta",
     "Pagamento.ContaBancaria.bic",
     "Pagamento.CartaoPagamento.titular",
     "Pagamento.DebitoDireto.*",
     "Desconto.DescontoEncargo.montanteBase",
     "Desconto.DescontoEncargo.percentagem",
     "Desconto.DescontoEncargo.motivo",
     "Desconto.DescontoEncargo.codigoMotivo",
     "Encargo.DescontoEncargo.montanteBase",
     "Encargo.DescontoEncargo.percentagem",
     "Encargo.DescontoEncargo.motivo",
     "Encargo.DescontoEncargo.codigoMotivo",
     "Totais.totalDescontos",
     "Totais.totalEncargos",
     "Totais.totalIvaMoedaContabilistica",
     "Totais.valorPago",
     "Totais.arredondamento",
     "DecomposicaoIva.CategoriaIva.motivoIsencao",
     "DecomposicaoIva.CategoriaIva.codigoMotivoIsencao",
     "DocumentoSuporte.descricao",
     "DocumentoSuporte.localizacaoExterna",
     "DocumentoSuporte.anexo",
     "DocumentoSuporte.tipoMime",
     "DocumentoSuporte.nomeFicheiro",
     "LinhaDocumento.nota",
     "LinhaDocumento.identificadorObjeto",
     "LinhaDocumento.referenciaLinhaEncomenda",
     "LinhaDocumento.numeroCompromisso",
     "LinhaDocumento.Periodo.*",
     "LinhaDocumento.Desconto.montanteBase",
     "LinhaDocumento.Desconto.percentagem",
     "LinhaDocumento.Desconto.motivo",
     "LinhaDocumento.Desconto.codigoMotivo",
     "LinhaDocumento.Encargo.montanteBase",
     "LinhaDocumento.Encargo.percentagem",
     "LinhaDocumento.Encargo.motivo",
     "LinhaDocumento.Encargo.codigoMotivo",
     "LinhaDocumento.Preco.descontoPreco",
     "LinhaDocumento.Preco.precoBruto",
     "LinhaDocumento.Preco.quantidadeBase",
     "LinhaDocumento.Preco.unidadeQuantidadeBase",
     "LinhaDocumento.CategoriaIva.motivoIsencao",
     "LinhaDocumento.CategoriaIva.codigoMotivoIsencao",
     "LinhaDocumento.Artigo.descricao",
     "LinhaDocumento.Artigo.codigo",
     "LinhaDocumento.Artigo.codigoComprador",
     "LinhaDocumento.Artigo.codigoBarras",
     "LinhaDocumento.Artigo.classificacao",
     "LinhaDocumento.Artigo.paisOrigem",
     "Metainformacao.*"
    ]
   }
  ],
  "perfis": [
   {
    "nome": "EmissaoFaturaCiusPt",
    "projecao": "FaturaCiusPt",
    "descricao": "Emissão de fatura eletrónica (380) em Portugal, em euros, por um fornecedor com NIF português.",
    "fixa": [
     {
      "propriedade": "CabecalhoDocumento.tipoDocumento",
      "valor": "380"
     },
     {
      "propriedade": "CabecalhoDocumento.moeda",
      "valor": "EUR"
     },
     {
      "propriedade": "Fornecedor.Morada.pais",
      "valor": "PT"
     }
    ]
   },
   {
    "nome": "EmissaoFaturaIsenta",
    "projecao": "FaturaCiusPt",
    "descricao": "Fatura isenta de IVA (380, em euros, em Portugal): o motivo de isenção é exigido linha a linha e no subtotal (RIR-LIN-ISENCAO, RIR-DECOMP-ISENCAO).",
    "fixa": [
     {
      "propriedade": "CabecalhoDocumento.tipoDocumento",
      "valor": "380"
     },
     {
      "propriedade": "CabecalhoDocumento.moeda",
      "valor": "EUR"
     },
     {
      "propriedade": "Fornecedor.Morada.pais",
      "valor": "PT"
     }
    ]
   },
   {
    "nome": "EmissaoNotaDebito",
    "projecao": "FaturaCiusPt",
    "descricao": "Emissão de nota de débito (383) em euros, que referencia o documento anterior.",
    "fixa": [
     {
      "propriedade": "CabecalhoDocumento.tipoDocumento",
      "valor": "383"
     },
     {
      "propriedade": "CabecalhoDocumento.moeda",
      "valor": "EUR"
     },
     {
      "propriedade": "Fornecedor.Morada.pais",
      "valor": "PT"
     }
    ]
   },
   {
    "nome": "EmissaoFaturaAdiantamento",
    "projecao": "FaturaCiusPt",
    "descricao": "Emissão de fatura de adiantamento (386) em euros.",
    "fixa": [
     {
      "propriedade": "CabecalhoDocumento.tipoDocumento",
      "valor": "386"
     },
     {
      "propriedade": "CabecalhoDocumento.moeda",
      "valor": "EUR"
     },
     {
      "propriedade": "Fornecedor.Morada.pais",
      "valor": "PT"
     }
    ]
   },
   {
    "nome": "EmissaoAutofaturacao",
    "projecao": "FaturaCiusPt",
    "descricao": "Emissão de autofaturação (389) em euros.",
    "fixa": [
     {
      "propriedade": "CabecalhoDocumento.tipoDocumento",
      "valor": "389"
     },
     {
      "propriedade": "CabecalhoDocumento.moeda",
      "valor": "EUR"
     },
     {
      "propriedade": "Fornecedor.Morada.pais",
      "valor": "PT"
     }
    ]
   },
   {
    "nome": "EmissaoNotaCredito",
    "projecao": "NotaCreditoCiusPt",
    "descricao": "Nota de crédito (381) em euros, que referencia a fatura original.",
    "fixa": [
     {
      "propriedade": "CabecalhoDocumento.tipoDocumento",
      "valor": "381"
     },
     {
      "propriedade": "CabecalhoDocumento.moeda",
      "valor": "EUR"
     },
     {
      "propriedade": "Fornecedor.Morada.pais",
      "valor": "PT"
     }
    ]
   }
  ]
 },
 {
  "$schema": "../../../specs/declaracao/ecv.schema.json",
  "declaracao": {
   "nome": "entrega",
   "versao": "0.1.0",
   "descricao": "Entrega ou encomenda da aplicação de vendas FM: documento, clientes comprador e destinatário, linhas de artigos e confirmação.",
   "dominios": [
    "faturação"
   ],
   "hlm": "Entrega"
  },
  "funcoes": [
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
    "contextosExternos": [],
    "retorno": "booleano"
   }
  ],
  "usm": [
   {
    "nome": "Entidade",
    "descricao": "Pessoa singular ou coletiva identificada pelo NIF.",
    "propriedades": [
     {
      "nome": "nif",
      "tipo": "texto",
      "descricao": "Número de identificação fiscal",
      "nomesAlternativos": [
       "taxId",
       "VATNumber"
      ],
      "regras": [
       {
        "id": "RP-NIF",
        "natureza": "plausibilidade",
        "descricao": "Entidade.nif segue o padrão ^[0-9]{9}$",
        "restricao": {
         "propriedade": "nif",
         "operador": "PATTERN",
         "valor": "^[0-9]{9}$",
         "mensagem": "O NIF tem de ter nove algarismos."
        }
       },
       {
        "id": "RP-NIF-DC",
        "natureza": "plausibilidade",
        "descricao": "digitoControloValido(Entidade.nif)",
        "restricao": {
         "operador": "FUNCTION",
         "chamada": {
          "funcao": "digitoControloValido",
          "argumentos": [
           {
            "caminho": "nif"
           }
          ]
         },
         "mensagem": "O dígito de controlo do NIF não está correto."
        }
       }
      ]
     },
     {
      "nome": "nome",
      "tipo": "texto",
      "descricao": "Nome ou denominação social",
      "nomesAlternativos": [
       "name",
       "denominacao"
      ]
     }
    ]
   },
   {
    "nome": "Morada",
    "descricao": "Morada postal: arruamento, código postal, localidade, freguesia e país.",
    "propriedades": [
     {
      "nome": "rua",
      "tipo": "texto",
      "descricao": "Arruamento e número de porta"
     },
     {
      "nome": "codigoPostal",
      "tipo": "texto",
      "descricao": "Código postal da morada",
      "nomesAlternativos": [
       "zipCode",
       "postalCode",
       "CP"
      ],
      "regras": [
       {
        "id": "RP-CP",
        "natureza": "plausibilidade",
        "descricao": "Morada.codigoPostal segue o padrão ^([1-9][0-9]{3}-[0-9]{3}|[0-5][0-9]{4}|[A-Z]{1,2}[0-9][0-9A-Z]? [0-9][A-Z]{2})$",
        "restricao": {
         "propriedade": "codigoPostal",
         "operador": "PATTERN",
         "valor": "^([1-9][0-9]{3}-[0-9]{3}|[0-5][0-9]{4}|[A-Z]{1,2}[0-9][0-9A-Z]? [0-9][A-Z]{2})$",
         "mensagem": "O código postal não tem nenhum dos formatos possíveis (português, espanhol ou britânico)."
        },
        "notas": "Plausibilidade: os formatos possíveis {PT, ES, GB}. Qual se aplica decide-se por inferência (RIR-CP-PT/ES/GB)."
       }
      ]
     },
     {
      "nome": "localidade",
      "tipo": "texto",
      "descricao": "Localidade da morada (em maiúsculas, sem acentos)"
     },
     {
      "nome": "freguesia",
      "tipo": "texto",
      "descricao": "Freguesia da morada (só para moradas em Lisboa)",
      "regras": [
       {
        "id": "RP-FREGUESIA",
        "natureza": "plausibilidade",
        "descricao": "Morada.freguesia ∈ {AJUDA, ALCANTARA, ALVALADE, AREEIRO, ARROIOS, AVENIDAS_NOVAS, BEATO, BELEM, BENFICA, CAMPO_DE_OURIQUE, CAMPOLIDE, CARNIDE, ESTRELA, LUMIAR, MARVILA, MISERICORDIA, OLIVAIS, PARQUE_DAS_NACOES, PENHA_DE_FRANCA, SANTA_CLARA, SANTA_MARIA_MAIOR, SANTO_ANTONIO, SAO_DOMINGOS_DE_BENFICA, SAO_VICENTE}",
        "restricao": {
         "propriedade": "freguesia",
         "operador": "IN",
         "valor": [
          "AJUDA",
          "ALCANTARA",
          "ALVALADE",
          "AREEIRO",
          "ARROIOS",
          "AVENIDAS_NOVAS",
          "BEATO",
          "BELEM",
          "BENFICA",
          "CAMPO_DE_OURIQUE",
          "CAMPOLIDE",
          "CARNIDE",
          "ESTRELA",
          "LUMIAR",
          "MARVILA",
          "MISERICORDIA",
          "OLIVAIS",
          "PARQUE_DAS_NACOES",
          "PENHA_DE_FRANCA",
          "SANTA_CLARA",
          "SANTA_MARIA_MAIOR",
          "SANTO_ANTONIO",
          "SAO_DOMINGOS_DE_BENFICA",
          "SAO_VICENTE"
         ],
         "mensagem": "A freguesia não pertence às freguesias de Lisboa conhecidas."
        }
       }
      ]
     },
     {
      "nome": "pais",
      "tipo": "texto",
      "descricao": "País da morada (código ISO de duas letras)",
      "nomesAlternativos": [
       "country",
       "countryCode"
      ],
      "regras": [
       {
        "id": "RP-PAIS",
        "natureza": "plausibilidade",
        "descricao": "Morada.pais ∈ {PT, ES, GB}",
        "restricao": {
         "propriedade": "pais",
         "operador": "IN",
         "valor": [
          "PT",
          "ES",
          "GB"
         ],
         "mensagem": "O país tem de ser PT, ES ou GB."
        }
       }
      ]
     }
    ],
    "regras": [
     {
      "id": "RIR-CP-PT",
      "natureza": "inferencia_restritiva",
      "descricao": "Se Morada.pais = PT → Morada.codigoPostal segue o padrão ^[1-9][0-9]{3}-[0-9]{3}$",
      "condicao": [
       {
        "propriedade": "pais",
        "operador": "EQUALS",
        "valor": "PT"
       }
      ],
      "restricao": {
       "propriedade": "codigoPostal",
       "operador": "PATTERN",
       "valor": "^[1-9][0-9]{3}-[0-9]{3}$",
       "mensagem": "O código postal português tem de ter o formato 0000-000, sem começar por zero."
      }
     },
     {
      "id": "RIR-CP-ES",
      "natureza": "inferencia_restritiva",
      "descricao": "Se Morada.pais = ES → Morada.codigoPostal segue o padrão ^[0-5][0-9]{4}$",
      "condicao": [
       {
        "propriedade": "pais",
        "operador": "EQUALS",
        "valor": "ES"
       }
      ],
      "restricao": {
       "propriedade": "codigoPostal",
       "operador": "PATTERN",
       "valor": "^[0-5][0-9]{4}$",
       "mensagem": "O código postal espanhol tem de ter cinco algarismos, a começar por 0 a 5."
      }
     },
     {
      "id": "RIR-CP-GB",
      "natureza": "inferencia_restritiva",
      "descricao": "Se Morada.pais = GB → Morada.codigoPostal segue o padrão ^[A-Z]{1,2}[0-9][0-9A-Z]? [0-9][A-Z]{2}$",
      "condicao": [
       {
        "propriedade": "pais",
        "operador": "EQUALS",
        "valor": "GB"
       }
      ],
      "restricao": {
       "propriedade": "codigoPostal",
       "operador": "PATTERN",
       "valor": "^[A-Z]{1,2}[0-9][0-9A-Z]? [0-9][A-Z]{2}$",
       "mensagem": "O código postal britânico tem de ter a forma de um postcode (ex.: SW1A 1AA)."
      }
     },
     {
      "id": "RIR-CP-LX-AJUDA",
      "natureza": "inferencia_restritiva",
      "descricao": "Se Morada.pais = PT e Morada.localidade = LISBOA e Morada.freguesia = AJUDA → Morada.codigoPostal segue o padrão ^(1300|1349)-[0-9]{3}$",
      "condicao": [
       {
        "propriedade": "pais",
        "operador": "EQUALS",
        "valor": "PT"
       },
       {
        "propriedade": "localidade",
        "operador": "EQUALS",
        "valor": "LISBOA"
       },
       {
        "propriedade": "freguesia",
        "operador": "EQUALS",
        "valor": "AJUDA"
       }
      ],
      "restricao": {
       "propriedade": "codigoPostal",
       "operador": "PATTERN",
       "valor": "^(1300|1349)-[0-9]{3}$",
       "mensagem": "O código postal de uma morada da freguesia Ajuda (Lisboa) começa por 1300 ou 1349."
      },
      "notas": "Mapeamento conhecido (códigos postais por freguesia de Lisboa) convertido em RIR: uma regra por freguesia. A vista de decisão sobre Morada.codigoPostal reconstrói a tabela."
     },
     {
      "id": "RIR-CP-LX-ALCANTARA",
      "natureza": "inferencia_restritiva",
      "descricao": "Se Morada.pais = PT e Morada.localidade = LISBOA e Morada.freguesia = ALCANTARA → Morada.codigoPostal segue o padrão ^(1300|1350)-[0-9]{3}$",
      "condicao": [
       {
        "propriedade": "pais",
        "operador": "EQUALS",
        "valor": "PT"
       },
       {
        "propriedade": "localidade",
        "operador": "EQUALS",
        "valor": "LISBOA"
       },
       {
        "propriedade": "freguesia",
        "operador": "EQUALS",
        "valor": "ALCANTARA"
       }
      ],
      "restricao": {
       "propriedade": "codigoPostal",
       "operador": "PATTERN",
       "valor": "^(1300|1350)-[0-9]{3}$",
       "mensagem": "O código postal de uma morada da freguesia Alcantara (Lisboa) começa por 1300 ou 1350."
      }
     },
     {
      "id": "RIR-CP-LX-ALVALADE",
      "natureza": "inferencia_restritiva",
      "descricao": "Se Morada.pais = PT e Morada.localidade = LISBOA e Morada.freguesia = ALVALADE → Morada.codigoPostal segue o padrão ^(1700|1749)-[0-9]{3}$",
      "condicao": [
       {
        "propriedade": "pais",
        "operador": "EQUALS",
        "valor": "PT"
       },
       {
        "propriedade": "localidade",
        "operador": "EQUALS",
        "valor": "LISBOA"
       },
       {
        "propriedade": "freguesia",
        "operador": "EQUALS",
        "valor": "ALVALADE"
       }
      ],
      "restricao": {
       "propriedade": "codigoPostal",
       "operador": "PATTERN",
       "valor": "^(1700|1749)-[0-9]{3}$",
       "mensagem": "O código postal de uma morada da freguesia Alvalade (Lisboa) começa por 1700 ou 1749."
      }
     },
     {
      "id": "RIR-CP-LX-AREEIRO",
      "natureza": "inferencia_restritiva",
      "descricao": "Se Morada.pais = PT e Morada.localidade = LISBOA e Morada.freguesia = AREEIRO → Morada.codigoPostal segue o padrão ^(1000|1049)-[0-9]{3}$",
      "condicao": [
       {
        "propriedade": "pais",
        "operador": "EQUALS",
        "valor": "PT"
       },
       {
        "propriedade": "localidade",
        "operador": "EQUALS",
        "valor": "LISBOA"
       },
       {
        "propriedade": "freguesia",
        "operador": "EQUALS",
        "valor": "AREEIRO"
       }
      ],
      "restricao": {
       "propriedade": "codigoPostal",
       "operador": "PATTERN",
       "valor": "^(1000|1049)-[0-9]{3}$",
       "mensagem": "O código postal de uma morada da freguesia Areeiro (Lisboa) começa por 1000 ou 1049."
      }
     },
     {
      "id": "RIR-CP-LX-ARROIOS",
      "natureza": "inferencia_restritiva",
      "descricao": "Se Morada.pais = PT e Morada.localidade = LISBOA e Morada.freguesia = ARROIOS → Morada.codigoPostal segue o padrão ^(1150|1169)-[0-9]{3}$",
      "condicao": [
       {
        "propriedade": "pais",
        "operador": "EQUALS",
        "valor": "PT"
       },
       {
        "propriedade": "localidade",
        "operador": "EQUALS",
        "valor": "LISBOA"
       },
       {
        "propriedade": "freguesia",
        "operador": "EQUALS",
        "valor": "ARROIOS"
       }
      ],
      "restricao": {
       "propriedade": "codigoPostal",
       "operador": "PATTERN",
       "valor": "^(1150|1169)-[0-9]{3}$",
       "mensagem": "O código postal de uma morada da freguesia Arroios (Lisboa) começa por 1150 ou 1169."
      }
     },
     {
      "id": "RIR-CP-LX-AVENIDAS-NOVAS",
      "natureza": "inferencia_restritiva",
      "descricao": "Se Morada.pais = PT e Morada.localidade = LISBOA e Morada.freguesia = AVENIDAS_NOVAS → Morada.codigoPostal segue o padrão ^(1050|1069)-[0-9]{3}$",
      "condicao": [
       {
        "propriedade": "pais",
        "operador": "EQUALS",
        "valor": "PT"
       },
       {
        "propriedade": "localidade",
        "operador": "EQUALS",
        "valor": "LISBOA"
       },
       {
        "propriedade": "freguesia",
        "operador": "EQUALS",
        "valor": "AVENIDAS_NOVAS"
       }
      ],
      "restricao": {
       "propriedade": "codigoPostal",
       "operador": "PATTERN",
       "valor": "^(1050|1069)-[0-9]{3}$",
       "mensagem": "O código postal de uma morada da freguesia Avenidas Novas (Lisboa) começa por 1050 ou 1069."
      }
     },
     {
      "id": "RIR-CP-LX-BEATO",
      "natureza": "inferencia_restritiva",
      "descricao": "Se Morada.pais = PT e Morada.localidade = LISBOA e Morada.freguesia = BEATO → Morada.codigoPostal segue o padrão ^(1900|1949)-[0-9]{3}$",
      "condicao": [
       {
        "propriedade": "pais",
        "operador": "EQUALS",
        "valor": "PT"
       },
       {
        "propriedade": "localidade",
        "operador": "EQUALS",
        "valor": "LISBOA"
       },
       {
        "propriedade": "freguesia",
        "operador": "EQUALS",
        "valor": "BEATO"
       }
      ],
      "restricao": {
       "propriedade": "codigoPostal",
       "operador": "PATTERN",
       "valor": "^(1900|1949)-[0-9]{3}$",
       "mensagem": "O código postal de uma morada da freguesia Beato (Lisboa) começa por 1900 ou 1949."
      }
     },
     {
      "id": "RIR-CP-LX-BELEM",
      "natureza": "inferencia_restritiva",
      "descricao": "Se Morada.pais = PT e Morada.localidade = LISBOA e Morada.freguesia = BELEM → Morada.codigoPostal segue o padrão ^(1400|1449)-[0-9]{3}$",
      "condicao": [
       {
        "propriedade": "pais",
        "operador": "EQUALS",
        "valor": "PT"
       },
       {
        "propriedade": "localidade",
        "operador": "EQUALS",
        "valor": "LISBOA"
       },
       {
        "propriedade": "freguesia",
        "operador": "EQUALS",
        "valor": "BELEM"
       }
      ],
      "restricao": {
       "propriedade": "codigoPostal",
       "operador": "PATTERN",
       "valor": "^(1400|1449)-[0-9]{3}$",
       "mensagem": "O código postal de uma morada da freguesia Belem (Lisboa) começa por 1400 ou 1449."
      }
     },
     {
      "id": "RIR-CP-LX-BENFICA",
      "natureza": "inferencia_restritiva",
      "descricao": "Se Morada.pais = PT e Morada.localidade = LISBOA e Morada.freguesia = BENFICA → Morada.codigoPostal segue o padrão ^(1500|1549)-[0-9]{3}$",
      "condicao": [
       {
        "propriedade": "pais",
        "operador": "EQUALS",
        "valor": "PT"
       },
       {
        "propriedade": "localidade",
        "operador": "EQUALS",
        "valor": "LISBOA"
       },
       {
        "propriedade": "freguesia",
        "operador": "EQUALS",
        "valor": "BENFICA"
       }
      ],
      "restricao": {
       "propriedade": "codigoPostal",
       "operador": "PATTERN",
       "valor": "^(1500|1549)-[0-9]{3}$",
       "mensagem": "O código postal de uma morada da freguesia Benfica (Lisboa) começa por 1500 ou 1549."
      }
     },
     {
      "id": "RIR-CP-LX-CAMPO-DE-OURIQUE",
      "natureza": "inferencia_restritiva",
      "descricao": "Se Morada.pais = PT e Morada.localidade = LISBOA e Morada.freguesia = CAMPO_DE_OURIQUE → Morada.codigoPostal segue o padrão ^(1250|1350)-[0-9]{3}$",
      "condicao": [
       {
        "propriedade": "pais",
        "operador": "EQUALS",
        "valor": "PT"
       },
       {
        "propriedade": "localidade",
        "operador": "EQUALS",
        "valor": "LISBOA"
       },
       {
        "propriedade": "freguesia",
        "operador": "EQUALS",
        "valor": "CAMPO_DE_OURIQUE"
       }
      ],
      "restricao": {
       "propriedade": "codigoPostal",
       "operador": "PATTERN",
       "valor": "^(1250|1350)-[0-9]{3}$",
       "mensagem": "O código postal de uma morada da freguesia Campo de Ourique (Lisboa) começa por 1250 ou 1350."
      }
     },
     {
      "id": "RIR-CP-LX-CAMPOLIDE",
      "natureza": "inferencia_restritiva",
      "descricao": "Se Morada.pais = PT e Morada.localidade = LISBOA e Morada.freguesia = CAMPOLIDE → Morada.codigoPostal segue o padrão ^(1070|1099)-[0-9]{3}$",
      "condicao": [
       {
        "propriedade": "pais",
        "operador": "EQUALS",
        "valor": "PT"
       },
       {
        "propriedade": "localidade",
        "operador": "EQUALS",
        "valor": "LISBOA"
       },
       {
        "propriedade": "freguesia",
        "operador": "EQUALS",
        "valor": "CAMPOLIDE"
       }
      ],
      "restricao": {
       "propriedade": "codigoPostal",
       "operador": "PATTERN",
       "valor": "^(1070|1099)-[0-9]{3}$",
       "mensagem": "O código postal de uma morada da freguesia Campolide (Lisboa) começa por 1070 ou 1099."
      }
     },
     {
      "id": "RIR-CP-LX-CARNIDE",
      "natureza": "inferencia_restritiva",
      "descricao": "Se Morada.pais = PT e Morada.localidade = LISBOA e Morada.freguesia = CARNIDE → Morada.codigoPostal segue o padrão ^(1600|1649)-[0-9]{3}$",
      "condicao": [
       {
        "propriedade": "pais",
        "operador": "EQUALS",
        "valor": "PT"
       },
       {
        "propriedade": "localidade",
        "operador": "EQUALS",
        "valor": "LISBOA"
       },
       {
        "propriedade": "freguesia",
        "operador": "EQUALS",
        "valor": "CARNIDE"
       }
      ],
      "restricao": {
       "propriedade": "codigoPostal",
       "operador": "PATTERN",
       "valor": "^(1600|1649)-[0-9]{3}$",
       "mensagem": "O código postal de uma morada da freguesia Carnide (Lisboa) começa por 1600 ou 1649."
      }
     },
     {
      "id": "RIR-CP-LX-ESTRELA",
      "natureza": "inferencia_restritiva",
      "descricao": "Se Morada.pais = PT e Morada.localidade = LISBOA e Morada.freguesia = ESTRELA → Morada.codigoPostal segue o padrão ^(1200|1249)-[0-9]{3}$",
      "condicao": [
       {
        "propriedade": "pais",
        "operador": "EQUALS",
        "valor": "PT"
       },
       {
        "propriedade": "localidade",
        "operador": "EQUALS",
        "valor": "LISBOA"
       },
       {
        "propriedade": "freguesia",
        "operador": "EQUALS",
        "valor": "ESTRELA"
       }
      ],
      "restricao": {
       "propriedade": "codigoPostal",
       "operador": "PATTERN",
       "valor": "^(1200|1249)-[0-9]{3}$",
       "mensagem": "O código postal de uma morada da freguesia Estrela (Lisboa) começa por 1200 ou 1249."
      }
     },
     {
      "id": "RIR-CP-LX-LUMIAR",
      "natureza": "inferencia_restritiva",
      "descricao": "Se Morada.pais = PT e Morada.localidade = LISBOA e Morada.freguesia = LUMIAR → Morada.codigoPostal segue o padrão ^(1600|1750)-[0-9]{3}$",
      "condicao": [
       {
        "propriedade": "pais",
        "operador": "EQUALS",
        "valor": "PT"
       },
       {
        "propriedade": "localidade",
        "operador": "EQUALS",
        "valor": "LISBOA"
       },
       {
        "propriedade": "freguesia",
        "operador": "EQUALS",
        "valor": "LUMIAR"
       }
      ],
      "restricao": {
       "propriedade": "codigoPostal",
       "operador": "PATTERN",
       "valor": "^(1600|1750)-[0-9]{3}$",
       "mensagem": "O código postal de uma morada da freguesia Lumiar (Lisboa) começa por 1600 ou 1750."
      }
     },
     {
      "id": "RIR-CP-LX-MARVILA",
      "natureza": "inferencia_restritiva",
      "descricao": "Se Morada.pais = PT e Morada.localidade = LISBOA e Morada.freguesia = MARVILA → Morada.codigoPostal segue o padrão ^(1800|1949)-[0-9]{3}$",
      "condicao": [
       {
        "propriedade": "pais",
        "operador": "EQUALS",
        "valor": "PT"
       },
       {
        "propriedade": "localidade",
        "operador": "EQUALS",
        "valor": "LISBOA"
       },
       {
        "propriedade": "freguesia",
        "operador": "EQUALS",
        "valor": "MARVILA"
       }
      ],
      "restricao": {
       "propriedade": "codigoPostal",
       "operador": "PATTERN",
       "valor": "^(1800|1949)-[0-9]{3}$",
       "mensagem": "O código postal de uma morada da freguesia Marvila (Lisboa) começa por 1800 ou 1949."
      }
     },
     {
      "id": "RIR-CP-LX-MISERICORDIA",
      "natureza": "inferencia_restritiva",
      "descricao": "Se Morada.pais = PT e Morada.localidade = LISBOA e Morada.freguesia = MISERICORDIA → Morada.codigoPostal segue o padrão ^(1200|1249)-[0-9]{3}$",
      "condicao": [
       {
        "propriedade": "pais",
        "operador": "EQUALS",
        "valor": "PT"
       },
       {
        "propriedade": "localidade",
        "operador": "EQUALS",
        "valor": "LISBOA"
       },
       {
        "propriedade": "freguesia",
        "operador": "EQUALS",
        "valor": "MISERICORDIA"
       }
      ],
      "restricao": {
       "propriedade": "codigoPostal",
       "operador": "PATTERN",
       "valor": "^(1200|1249)-[0-9]{3}$",
       "mensagem": "O código postal de uma morada da freguesia Misericordia (Lisboa) começa por 1200 ou 1249."
      }
     },
     {
      "id": "RIR-CP-LX-OLIVAIS",
      "natureza": "inferencia_restritiva",
      "descricao": "Se Morada.pais = PT e Morada.localidade = LISBOA e Morada.freguesia = OLIVAIS → Morada.codigoPostal segue o padrão ^(1800|1885)-[0-9]{3}$",
      "condicao": [
       {
        "propriedade": "pais",
        "operador": "EQUALS",
        "valor": "PT"
       },
       {
        "propriedade": "localidade",
        "operador": "EQUALS",
        "valor": "LISBOA"
       },
       {
        "propriedade": "freguesia",
        "operador": "EQUALS",
        "valor": "OLIVAIS"
       }
      ],
      "restricao": {
       "propriedade": "codigoPostal",
       "operador": "PATTERN",
       "valor": "^(1800|1885)-[0-9]{3}$",
       "mensagem": "O código postal de uma morada da freguesia Olivais (Lisboa) começa por 1800 ou 1885."
      }
     },
     {
      "id": "RIR-CP-LX-PARQUE-DAS-NACOES",
      "natureza": "inferencia_restritiva",
      "descricao": "Se Morada.pais = PT e Morada.localidade = LISBOA e Morada.freguesia = PARQUE_DAS_NACOES → Morada.codigoPostal segue o padrão ^(1990|1998)-[0-9]{3}$",
      "condicao": [
       {
        "propriedade": "pais",
        "operador": "EQUALS",
        "valor": "PT"
       },
       {
        "propriedade": "localidade",
        "operador": "EQUALS",
        "valor": "LISBOA"
       },
       {
        "propriedade": "freguesia",
        "operador": "EQUALS",
        "valor": "PARQUE_DAS_NACOES"
       }
      ],
      "restricao": {
       "propriedade": "codigoPostal",
       "operador": "PATTERN",
       "valor": "^(1990|1998)-[0-9]{3}$",
       "mensagem": "O código postal de uma morada da freguesia Parque das Nacoes (Lisboa) começa por 1990 ou 1998."
      }
     },
     {
      "id": "RIR-CP-LX-PENHA-DE-FRANCA",
      "natureza": "inferencia_restritiva",
      "descricao": "Se Morada.pais = PT e Morada.localidade = LISBOA e Morada.freguesia = PENHA_DE_FRANCA → Morada.codigoPostal segue o padrão ^(1170|1199)-[0-9]{3}$",
      "condicao": [
       {
        "propriedade": "pais",
        "operador": "EQUALS",
        "valor": "PT"
       },
       {
        "propriedade": "localidade",
        "operador": "EQUALS",
        "valor": "LISBOA"
       },
       {
        "propriedade": "freguesia",
        "operador": "EQUALS",
        "valor": "PENHA_DE_FRANCA"
       }
      ],
      "restricao": {
       "propriedade": "codigoPostal",
       "operador": "PATTERN",
       "valor": "^(1170|1199)-[0-9]{3}$",
       "mensagem": "O código postal de uma morada da freguesia Penha de Franca (Lisboa) começa por 1170 ou 1199."
      }
     },
     {
      "id": "RIR-CP-LX-SANTA-CLARA",
      "natureza": "inferencia_restritiva",
      "descricao": "Se Morada.pais = PT e Morada.localidade = LISBOA e Morada.freguesia = SANTA_CLARA → Morada.codigoPostal segue o padrão ^(1750|1769)-[0-9]{3}$",
      "condicao": [
       {
        "propriedade": "pais",
        "operador": "EQUALS",
        "valor": "PT"
       },
       {
        "propriedade": "localidade",
        "operador": "EQUALS",
        "valor": "LISBOA"
       },
       {
        "propriedade": "freguesia",
        "operador": "EQUALS",
        "valor": "SANTA_CLARA"
       }
      ],
      "restricao": {
       "propriedade": "codigoPostal",
       "operador": "PATTERN",
       "valor": "^(1750|1769)-[0-9]{3}$",
       "mensagem": "O código postal de uma morada da freguesia Santa Clara (Lisboa) começa por 1750 ou 1769."
      }
     },
     {
      "id": "RIR-CP-LX-SANTA-MARIA-MAIOR",
      "natureza": "inferencia_restritiva",
      "descricao": "Se Morada.pais = PT e Morada.localidade = LISBOA e Morada.freguesia = SANTA_MARIA_MAIOR → Morada.codigoPostal segue o padrão ^(1100|1149)-[0-9]{3}$",
      "condicao": [
       {
        "propriedade": "pais",
        "operador": "EQUALS",
        "valor": "PT"
       },
       {
        "propriedade": "localidade",
        "operador": "EQUALS",
        "valor": "LISBOA"
       },
       {
        "propriedade": "freguesia",
        "operador": "EQUALS",
        "valor": "SANTA_MARIA_MAIOR"
       }
      ],
      "restricao": {
       "propriedade": "codigoPostal",
       "operador": "PATTERN",
       "valor": "^(1100|1149)-[0-9]{3}$",
       "mensagem": "O código postal de uma morada da freguesia Santa Maria Maior (Lisboa) começa por 1100 ou 1149."
      }
     },
     {
      "id": "RIR-CP-LX-SANTO-ANTONIO",
      "natureza": "inferencia_restritiva",
      "descricao": "Se Morada.pais = PT e Morada.localidade = LISBOA e Morada.freguesia = SANTO_ANTONIO → Morada.codigoPostal segue o padrão ^(1250|1269)-[0-9]{3}$",
      "condicao": [
       {
        "propriedade": "pais",
        "operador": "EQUALS",
        "valor": "PT"
       },
       {
        "propriedade": "localidade",
        "operador": "EQUALS",
        "valor": "LISBOA"
       },
       {
        "propriedade": "freguesia",
        "operador": "EQUALS",
        "valor": "SANTO_ANTONIO"
       }
      ],
      "restricao": {
       "propriedade": "codigoPostal",
       "operador": "PATTERN",
       "valor": "^(1250|1269)-[0-9]{3}$",
       "mensagem": "O código postal de uma morada da freguesia Santo Antonio (Lisboa) começa por 1250 ou 1269."
      }
     },
     {
      "id": "RIR-CP-LX-SAO-DOMINGOS-DE-BENFICA",
      "natureza": "inferencia_restritiva",
      "descricao": "Se Morada.pais = PT e Morada.localidade = LISBOA e Morada.freguesia = SAO_DOMINGOS_DE_BENFICA → Morada.codigoPostal segue o padrão ^(1500|1600)-[0-9]{3}$",
      "condicao": [
       {
        "propriedade": "pais",
        "operador": "EQUALS",
        "valor": "PT"
       },
       {
        "propriedade": "localidade",
        "operador": "EQUALS",
        "valor": "LISBOA"
       },
       {
        "propriedade": "freguesia",
        "operador": "EQUALS",
        "valor": "SAO_DOMINGOS_DE_BENFICA"
       }
      ],
      "restricao": {
       "propriedade": "codigoPostal",
       "operador": "PATTERN",
       "valor": "^(1500|1600)-[0-9]{3}$",
       "mensagem": "O código postal de uma morada da freguesia Sao Domingos de Benfica (Lisboa) começa por 1500 ou 1600."
      }
     },
     {
      "id": "RIR-CP-LX-SAO-VICENTE",
      "natureza": "inferencia_restritiva",
      "descricao": "Se Morada.pais = PT e Morada.localidade = LISBOA e Morada.freguesia = SAO_VICENTE → Morada.codigoPostal segue o padrão ^(1100|1170)-[0-9]{3}$",
      "condicao": [
       {
        "propriedade": "pais",
        "operador": "EQUALS",
        "valor": "PT"
       },
       {
        "propriedade": "localidade",
        "operador": "EQUALS",
        "valor": "LISBOA"
       },
       {
        "propriedade": "freguesia",
        "operador": "EQUALS",
        "valor": "SAO_VICENTE"
       }
      ],
      "restricao": {
       "propriedade": "codigoPostal",
       "operador": "PATTERN",
       "valor": "^(1100|1170)-[0-9]{3}$",
       "mensagem": "O código postal de uma morada da freguesia Sao Vicente (Lisboa) começa por 1100 ou 1170."
      }
     }
    ]
   },
   {
    "nome": "Contacto",
    "descricao": "Contacto eletrónico de uma entidade.",
    "propriedades": [
     {
      "nome": "email",
      "tipo": "texto",
      "descricao": "Endereço de correio eletrónico",
      "nomesAlternativos": [
       "eMail",
       "correioEletronico"
      ],
      "regras": [
       {
        "id": "RP-EMAIL",
        "natureza": "plausibilidade",
        "descricao": "Contacto.email segue o padrão ^[a-z0-9._-]+@[a-z0-9-]+(\\.[a-z0-9-]+)+$",
        "restricao": {
         "propriedade": "email",
         "operador": "PATTERN",
         "valor": "^[a-z0-9._-]+@[a-z0-9-]+(\\.[a-z0-9-]+)+$",
         "mensagem": "O email tem de ter uma parte local e um domínio com pelo menos um ponto, sem espaços nem maiúsculas."
        }
       }
      ]
     }
    ]
   },
   {
    "nome": "ContactoTelefonico",
    "descricao": "Contactos telefónicos de uma pessoa ou entidade: telefone e telemóvel.",
    "propriedades": [
     {
      "nome": "telefone",
      "tipo": "texto",
      "descricao": "Número de telefone (rede fixa ou geral)",
      "nomesAlternativos": [
       "Telephone",
       "fixePhoneNumber"
      ],
      "regras": [
       {
        "id": "RP-TELEFONE",
        "natureza": "plausibilidade",
        "restricao": {
         "propriedade": "telefone",
         "operador": "LENGTH",
         "valor": [
          1,
          200
         ],
         "mensagem": "O telefone tem de ter entre 1 e 200 caracteres."
        },
        "descricao": "ContactoTelefonico.telefone tem entre 1 e 200 caracteres"
       }
      ]
     },
     {
      "nome": "telemovel",
      "tipo": "texto",
      "descricao": "Número de telemóvel",
      "nomesAlternativos": [
       "phoneNumber",
       "mobile"
      ]
     }
    ]
   },
   {
    "nome": "DocumentoIdentificacao",
    "descricao": "Documento de identificação pessoal (ex.: cartão de cidadão): número e data de validade.",
    "propriedades": [
     {
      "nome": "numero",
      "tipo": "texto",
      "descricao": "Número do documento de identificação",
      "nomesAlternativos": [
       "citizenCard"
      ]
     },
     {
      "nome": "dataValidade",
      "tipo": "data",
      "descricao": "Data de validade do documento de identificação",
      "nomesAlternativos": [
       "citizenCardExpirationDate"
      ]
     }
    ]
   },
   {
    "nome": "Artigo",
    "descricao": "Bem ou serviço transacionado: designação, descrição, códigos de identificação e país de origem.",
    "propriedades": [
     {
      "nome": "nome",
      "tipo": "texto",
      "descricao": "Designação do bem ou serviço",
      "nomesAlternativos": [
       "Item name",
       "description"
      ],
      "regras": [
       {
        "id": "RP-ART-NOME",
        "natureza": "plausibilidade",
        "restricao": {
         "propriedade": "nome",
         "operador": "LENGTH",
         "valor": [
          1,
          200
         ],
         "mensagem": "A designação do artigo tem de ter entre 1 e 200 caracteres."
        },
        "descricao": "Artigo.nome tem entre 1 e 200 caracteres"
       }
      ]
     },
     {
      "nome": "descricao",
      "tipo": "texto",
      "descricao": "Descrição detalhada do bem ou serviço",
      "nomesAlternativos": [
       "Item description"
      ],
      "regras": [
       {
        "id": "RP-ART-DESC",
        "natureza": "plausibilidade",
        "restricao": {
         "propriedade": "descricao",
         "operador": "LENGTH",
         "valor": [
          1,
          200
         ],
         "mensagem": "A descrição do artigo tem de ter entre 1 e 200 caracteres."
        },
        "descricao": "Artigo.descricao tem entre 1 e 200 caracteres"
       }
      ]
     },
     {
      "nome": "codigo",
      "tipo": "texto",
      "descricao": "Código do artigo atribuído pelo vendedor",
      "nomesAlternativos": [
       "Item Seller s identifier",
       "code"
      ],
      "regras": [
       {
        "id": "RP-ART-CODIGO",
        "natureza": "plausibilidade",
        "restricao": {
         "propriedade": "codigo",
         "operador": "LENGTH",
         "valor": [
          1,
          50
         ],
         "mensagem": "O código do artigo tem de ter entre 1 e 50 caracteres."
        },
        "descricao": "Artigo.codigo tem entre 1 e 50 caracteres"
       }
      ]
     },
     {
      "nome": "codigoComprador",
      "tipo": "texto",
      "descricao": "Código do artigo atribuído pelo comprador",
      "nomesAlternativos": [
       "Item Buyer s identifier"
      ],
      "regras": [
       {
        "id": "RP-ART-CODCOMP",
        "natureza": "plausibilidade",
        "restricao": {
         "propriedade": "codigoComprador",
         "operador": "LENGTH",
         "valor": [
          1,
          50
         ],
         "mensagem": "O código do artigo do comprador tem de ter entre 1 e 50 caracteres."
        },
        "descricao": "Artigo.codigoComprador tem entre 1 e 50 caracteres"
       }
      ]
     },
     {
      "nome": "codigoBarras",
      "tipo": "texto",
      "descricao": "Identificador normalizado do artigo (EAN/GTIN)",
      "nomesAlternativos": [
       "Item standard identifier",
       "barCode",
       "EAN"
      ],
      "regras": [
       {
        "id": "RP-ART-CODBARRAS",
        "natureza": "plausibilidade",
        "restricao": {
         "propriedade": "codigoBarras",
         "operador": "LENGTH",
         "valor": [
          1,
          50
         ],
         "mensagem": "O código EAN tem de ter entre 1 e 50 caracteres."
        },
        "descricao": "Artigo.codigoBarras tem entre 1 e 50 caracteres"
       }
      ]
     },
     {
      "nome": "classificacao",
      "tipo": "texto",
      "descricao": "Código de classificação da mercadoria (ex.: CPV)",
      "nomesAlternativos": [
       "Item classification identifier",
       "CPV"
      ],
      "regras": [
       {
        "id": "RP-ART-CLASSIF",
        "natureza": "plausibilidade",
        "restricao": {
         "propriedade": "classificacao",
         "operador": "LENGTH",
         "valor": [
          1,
          50
         ],
         "mensagem": "O código de classificação tem de ter entre 1 e 50 caracteres."
        },
        "descricao": "Artigo.classificacao tem entre 1 e 50 caracteres"
       }
      ]
     },
     {
      "nome": "paisOrigem",
      "tipo": "texto",
      "descricao": "País de origem do artigo (código ISO 3166-1 alfa-2)",
      "nomesAlternativos": [
       "Item country of origin"
      ],
      "regras": [
       {
        "id": "RP-ART-PAIS",
        "natureza": "plausibilidade",
        "restricao": {
         "propriedade": "paisOrigem",
         "operador": "PATTERN",
         "valor": "^[A-Z]{2}$",
         "mensagem": "O país de origem tem de ser um código ISO 3166-1 de duas letras."
        },
        "descricao": "Artigo.paisOrigem segue o padrão ^[A-Z]{2}$"
       }
      ]
     }
    ]
   }
  ],
  "sm": [
   {
    "nome": "Metainformacao",
    "descricao": "Metainformação do próprio modelo: origem, versão da fonte, entidade de origem, utilização e domínio.",
    "propriedades": [
     {
      "nome": "origemModelo",
      "tipo": "texto",
      "descricao": "Fonte do modelo de dados (norma, sistema ou repositório)"
     },
     {
      "nome": "versaoOrigem",
      "tipo": "texto",
      "descricao": "Versão da fonte usada"
     },
     {
      "nome": "referenciaOrigem",
      "tipo": "texto",
      "descricao": "Identificador da entidade na fonte (ex.: BG-0 Invoice, Device)"
     },
     {
      "nome": "utilizacao",
      "tipo": "texto",
      "descricao": "Finalidade ou contexto de utilização do modelo"
     },
     {
      "nome": "dominio",
      "tipo": "texto",
      "descricao": "Domínio a que o modelo pertence"
     },
     {
      "nome": "observacoes",
      "tipo": "texto",
      "descricao": "Outra metainformação relevante sobre o modelo"
     }
    ]
   },
   {
    "nome": "ClienteVenda",
    "descricao": "Cliente da aplicação de vendas FM: identificação, morada, contactos, documento de identificação, segundo titular e dados comerciais (zona, vendedor, cobrança).",
    "notas": "O SM Cliente existente não serve tal e qual (só tem Entidade, Morada e consentimento); este é o cliente operacional do FM, com segundo titular.",
    "composicao": [
     {
      "usm": "Entidade",
      "cardinalidade": "1..1"
     },
     {
      "usm": "Morada",
      "cardinalidade": "1..1"
     },
     {
      "usm": "Contacto",
      "cardinalidade": "0..1"
     },
     {
      "usm": "ContactoTelefonico",
      "cardinalidade": "0..1"
     },
     {
      "usm": "DocumentoIdentificacao",
      "papel": "CartaoCidadao",
      "cardinalidade": "0..1"
     },
     {
      "usm": "Entidade",
      "papel": "SegundoTitular",
      "cardinalidade": "0..1"
     },
     {
      "usm": "Morada",
      "papel": "MoradaSegundoTitular",
      "cardinalidade": "0..1"
     },
     {
      "usm": "ContactoTelefonico",
      "papel": "ContactoSegundoTitular",
      "cardinalidade": "0..1"
     },
     {
      "usm": "DocumentoIdentificacao",
      "papel": "CartaoCidadaoSegundoTitular",
      "cardinalidade": "0..1"
     }
    ],
    "propriedades": [
     {
      "nome": "codigo",
      "tipo": "texto",
      "descricao": "Código do cliente na aplicação (atribuído automaticamente e imutável)",
      "nomesAlternativos": [
       "code",
       "Codigo Cliente"
      ]
     },
     {
      "nome": "designacaoPostal",
      "tipo": "texto",
      "descricao": "Designação postal (localidade) que acompanha o código postal do cliente",
      "nomesAlternativos": [
       "zipCodeLoc"
      ]
     },
     {
      "nome": "designacaoPostalSegundoTitular",
      "tipo": "texto",
      "descricao": "Designação postal que acompanha o código postal do segundo titular",
      "nomesAlternativos": [
       "zipCodeLoc2"
      ]
     },
     {
      "nome": "zona",
      "tipo": "texto",
      "descricao": "Código da zona comercial do cliente (referência a uma Zona)",
      "nomesAlternativos": [
       "zone",
       "Zona"
      ],
      "regras": [
       {
        "id": "RP-CLI-ZONA",
        "natureza": "plausibilidade",
        "restricao": {
         "propriedade": "zona",
         "operador": "LENGTH",
         "valor": [
          0,
          10
         ],
         "mensagem": "A zona do cliente tem no máximo 10 caracteres."
        },
        "descricao": "ClienteVenda.zona tem entre 0 e 10 caracteres"
       }
      ]
     },
     {
      "nome": "localCobranca",
      "tipo": "texto",
      "descricao": "Local onde é feita a cobrança ao cliente",
      "nomesAlternativos": [
       "chargeLocation",
       "Local Cobrança"
      ],
      "regras": [
       {
        "id": "RP-CLI-COBRANCA",
        "natureza": "plausibilidade",
        "restricao": {
         "propriedade": "localCobranca",
         "operador": "LENGTH",
         "valor": [
          0,
          10
         ],
         "mensagem": "O local de cobrança tem no máximo 10 caracteres."
        },
        "descricao": "ClienteVenda.localCobranca tem entre 0 e 10 caracteres"
       }
      ]
     },
     {
      "nome": "observacoes",
      "tipo": "texto",
      "descricao": "Observações livres sobre o cliente",
      "nomesAlternativos": [
       "notes"
      ]
     },
     {
      "nome": "codigoVendedor",
      "tipo": "texto",
      "descricao": "Código do vendedor responsável pelo cliente",
      "nomesAlternativos": [
       "sellerCode",
       "Codigo Vendedor"
      ]
     },
     {
      "nome": "numeroOrdem",
      "tipo": "texto",
      "descricao": "Número de ordem do cliente no percurso do vendedor",
      "nomesAlternativos": [
       "orderNumber",
       "Numero Ordem"
      ]
     },
     {
      "nome": "dataNascimento",
      "tipo": "data",
      "descricao": "Data de nascimento do cliente",
      "nomesAlternativos": [
       "dateOfBirth"
      ]
     },
     {
      "nome": "diaRecebimento",
      "tipo": "texto",
      "descricao": "Dia do mês para recebimento das prestações",
      "nomesAlternativos": [
       "receivingDay",
       "Dia Recebimento"
      ]
     },
     {
      "nome": "novo",
      "tipo": "booleano",
      "descricao": "Indica se o cliente foi criado no dispositivo e ainda não foi sincronizado",
      "nomesAlternativos": [
       "isNew"
      ]
     },
     {
      "nome": "dataRegisto",
      "tipo": "data",
      "descricao": "Data de abertura da ficha do cliente",
      "nomesAlternativos": [
       "registrationDate",
       "Data Abertura Ficha"
      ]
     }
    ],
    "regras": [
     {
      "id": "RP-CLI-NOME",
      "natureza": "plausibilidade",
      "restricao": {
       "propriedade": "Entidade.nome",
       "operador": "LENGTH",
       "valor": [
        0,
        35
       ],
       "mensagem": "O nome do cliente tem no máximo 35 caracteres."
      },
      "descricao": "ClienteVenda.Entidade.nome tem entre 0 e 35 caracteres"
     },
     {
      "id": "RP-CLI-NIF",
      "natureza": "plausibilidade",
      "restricao": {
       "propriedade": "Entidade.nif",
       "operador": "LENGTH",
       "valor": [
        0,
        15
       ],
       "mensagem": "O contribuinte do cliente tem no máximo 15 caracteres."
      },
      "descricao": "ClienteVenda.Entidade.nif tem entre 0 e 15 caracteres"
     },
     {
      "id": "RP-CLI-RUA",
      "natureza": "plausibilidade",
      "restricao": {
       "propriedade": "Morada.rua",
       "operador": "LENGTH",
       "valor": [
        0,
        35
       ],
       "mensagem": "A morada do cliente tem no máximo 35 caracteres."
      },
      "descricao": "ClienteVenda.Morada.rua tem entre 0 e 35 caracteres"
     },
     {
      "id": "RP-CLI-LOCALIDADE",
      "natureza": "plausibilidade",
      "restricao": {
       "propriedade": "Morada.localidade",
       "operador": "LENGTH",
       "valor": [
        0,
        35
       ],
       "mensagem": "A localidade do cliente tem no máximo 35 caracteres."
      },
      "descricao": "ClienteVenda.Morada.localidade tem entre 0 e 35 caracteres"
     },
     {
      "id": "RP-CLI-CP",
      "natureza": "plausibilidade",
      "restricao": {
       "propriedade": "Morada.codigoPostal",
       "operador": "LENGTH",
       "valor": [
        0,
        35
       ],
       "mensagem": "O código postal do cliente tem no máximo 35 caracteres."
      },
      "descricao": "ClienteVenda.Morada.codigoPostal tem entre 0 e 35 caracteres"
     },
     {
      "id": "RP-CLI-EMAIL",
      "natureza": "plausibilidade",
      "restricao": {
       "propriedade": "Contacto.email",
       "operador": "LENGTH",
       "valor": [
        0,
        60
       ],
       "mensagem": "O email do cliente tem no máximo 60 caracteres."
      },
      "descricao": "ClienteVenda.Contacto.email tem entre 0 e 60 caracteres"
     },
     {
      "id": "RP-CLI-TELEFONE",
      "natureza": "plausibilidade",
      "restricao": {
       "propriedade": "ContactoTelefonico.telefone",
       "operador": "LENGTH",
       "valor": [
        0,
        15
       ],
       "mensagem": "O telefone do cliente tem no máximo 15 caracteres."
      },
      "descricao": "ClienteVenda.ContactoTelefonico.telefone tem entre 0 e 15 caracteres"
     },
     {
      "id": "RP-CLI-TELEMOVEL",
      "natureza": "plausibilidade",
      "restricao": {
       "propriedade": "ContactoTelefonico.telemovel",
       "operador": "LENGTH",
       "valor": [
        0,
        15
       ],
       "mensagem": "O telemóvel do cliente tem no máximo 15 caracteres."
      },
      "descricao": "ClienteVenda.ContactoTelefonico.telemovel tem entre 0 e 15 caracteres"
     },
     {
      "id": "RP-CLI-CC",
      "natureza": "plausibilidade",
      "restricao": {
       "propriedade": "CartaoCidadao.numero",
       "operador": "LENGTH",
       "valor": [
        0,
        15
       ],
       "mensagem": "O número do cartão de cidadão do cliente tem no máximo 15 caracteres."
      },
      "descricao": "ClienteVenda.CartaoCidadao.numero tem entre 0 e 15 caracteres"
     },
     {
      "id": "RP-CLI-NOME2",
      "natureza": "plausibilidade",
      "restricao": {
       "propriedade": "SegundoTitular.nome",
       "operador": "LENGTH",
       "valor": [
        0,
        35
       ],
       "mensagem": "O nome do segundo titular tem no máximo 35 caracteres."
      },
      "descricao": "ClienteVenda.SegundoTitular.nome tem entre 0 e 35 caracteres"
     },
     {
      "id": "RP-CLI-NIF2",
      "natureza": "plausibilidade",
      "restricao": {
       "propriedade": "SegundoTitular.nif",
       "operador": "LENGTH",
       "valor": [
        0,
        15
       ],
       "mensagem": "O contribuinte do segundo titular tem no máximo 15 caracteres."
      },
      "descricao": "ClienteVenda.SegundoTitular.nif tem entre 0 e 15 caracteres"
     },
     {
      "id": "RP-CLI-RUA2",
      "natureza": "plausibilidade",
      "restricao": {
       "propriedade": "MoradaSegundoTitular.rua",
       "operador": "LENGTH",
       "valor": [
        0,
        35
       ],
       "mensagem": "A morada do segundo titular tem no máximo 35 caracteres."
      },
      "descricao": "ClienteVenda.MoradaSegundoTitular.rua tem entre 0 e 35 caracteres"
     },
     {
      "id": "RP-CLI-LOCALIDADE2",
      "natureza": "plausibilidade",
      "restricao": {
       "propriedade": "MoradaSegundoTitular.localidade",
       "operador": "LENGTH",
       "valor": [
        0,
        35
       ],
       "mensagem": "A localidade do segundo titular tem no máximo 35 caracteres."
      },
      "descricao": "ClienteVenda.MoradaSegundoTitular.localidade tem entre 0 e 35 caracteres"
     },
     {
      "id": "RP-CLI-CP2",
      "natureza": "plausibilidade",
      "restricao": {
       "propriedade": "MoradaSegundoTitular.codigoPostal",
       "operador": "LENGTH",
       "valor": [
        0,
        35
       ],
       "mensagem": "O código postal do segundo titular tem no máximo 35 caracteres."
      },
      "descricao": "ClienteVenda.MoradaSegundoTitular.codigoPostal tem entre 0 e 35 caracteres"
     },
     {
      "id": "RP-CLI-TELEFONE2",
      "natureza": "plausibilidade",
      "restricao": {
       "propriedade": "ContactoSegundoTitular.telefone",
       "operador": "LENGTH",
       "valor": [
        0,
        15
       ],
       "mensagem": "O telefone do segundo titular tem no máximo 15 caracteres."
      },
      "descricao": "ClienteVenda.ContactoSegundoTitular.telefone tem entre 0 e 15 caracteres"
     },
     {
      "id": "RP-CLI-CC2",
      "natureza": "plausibilidade",
      "restricao": {
       "propriedade": "CartaoCidadaoSegundoTitular.numero",
       "operador": "LENGTH",
       "valor": [
        0,
        15
       ],
       "mensagem": "O número do cartão de cidadão do segundo titular tem no máximo 15 caracteres."
      },
      "descricao": "ClienteVenda.CartaoCidadaoSegundoTitular.numero tem entre 0 e 15 caracteres"
     }
    ]
   },
   {
    "nome": "DadosEntrega",
    "descricao": "Identificação da entrega: números do documento, da fatura, da guia e do contrato, tipo, estado e datas.",
    "propriedades": [
     {
      "nome": "numeroEntrega",
      "tipo": "texto",
      "descricao": "Número da entrega",
      "nomesAlternativos": [
       "deliveryNumber"
      ]
     },
     {
      "nome": "numeroFatura",
      "tipo": "texto",
      "descricao": "Número da fatura associada à entrega",
      "nomesAlternativos": [
       "invoiceNumber"
      ]
     },
     {
      "nome": "numeroGuiaTransporte",
      "tipo": "texto",
      "descricao": "Número da guia de transporte da entrega",
      "nomesAlternativos": [
       "deliveryGuideNumber"
      ]
     },
     {
      "nome": "numeroContrato",
      "tipo": "texto",
      "descricao": "Número do contrato associado à entrega",
      "nomesAlternativos": [
       "contractNumber"
      ]
     },
     {
      "nome": "numeroDocumentoVenda",
      "tipo": "texto",
      "descricao": "Número do documento de venda",
      "nomesAlternativos": [
       "documentSaleNumber"
      ]
     },
     {
      "nome": "tipoDocumento",
      "tipo": "texto",
      "descricao": "Tipo do documento emitido para a entrega",
      "nomesAlternativos": [
       "documentType"
      ]
     },
     {
      "nome": "estado",
      "tipo": "texto",
      "descricao": "Estado da entrega no circuito de faturação",
      "nomesAlternativos": [
       "status"
      ],
      "regras": [
       {
        "id": "RP-ENTFM-ESTADO",
        "natureza": "plausibilidade",
        "restricao": {
         "propriedade": "estado",
         "operador": "IN",
         "valor": [
          "FATURADO",
          "ENTREGUE",
          "ENVIADO",
          "PENDENTE",
          "POR_FATURAR",
          "ERRO"
         ],
         "mensagem": "O estado da entrega tem de ser FATURADO, ENTREGUE, ENVIADO, PENDENTE, POR_FATURAR ou ERRO."
        },
        "descricao": "DadosEntrega.estado ∈ {FATURADO, ENTREGUE, ENVIADO, PENDENTE, POR_FATURAR, ERRO}"
       }
      ]
     },
     {
      "nome": "data",
      "tipo": "data",
      "descricao": "Data da entrega",
      "nomesAlternativos": [
       "date"
      ]
     },
     {
      "nome": "dataRegisto",
      "tipo": "data",
      "descricao": "Data de registo da entrega na aplicação",
      "nomesAlternativos": [
       "registrationDate"
      ]
     }
    ]
   },
   {
    "nome": "LinhaEntrega",
    "descricao": "Linha de uma entrega: artigo entregue, número de série, quantidade, e preço e desconto acordados.",
    "composicao": [
     {
      "usm": "Artigo",
      "cardinalidade": "1..1"
     }
    ],
    "propriedades": [
     {
      "nome": "numeroSerie",
      "tipo": "texto",
      "descricao": "Número de série do artigo entregue",
      "nomesAlternativos": [
       "seriesNumber"
      ]
     },
     {
      "nome": "quantidade",
      "tipo": "inteiro",
      "descricao": "Quantidade do artigo nesta entrega",
      "nomesAlternativos": [
       "quantity"
      ]
     },
     {
      "nome": "precoPersonalizado",
      "tipo": "decimal",
      "descricao": "Preço acordado para o artigo nesta entrega",
      "nomesAlternativos": [
       "customPrice"
      ]
     },
     {
      "nome": "descontoPersonalizado",
      "tipo": "decimal",
      "descricao": "Desconto acordado para o artigo nesta entrega",
      "nomesAlternativos": [
       "customDiscount"
      ]
     }
    ]
   },
   {
    "nome": "ConfirmacaoEntrega",
    "descricao": "Confirmação da entrega: documentos confirmados, preço original, sinal e prestação acordados.",
    "propriedades": [
     {
      "nome": "documentoConfirmado",
      "tipo": "booleano",
      "descricao": "Indica se o documento de venda foi confirmado",
      "nomesAlternativos": [
       "document"
      ]
     },
     {
      "nome": "contratoConfirmado",
      "tipo": "booleano",
      "descricao": "Indica se o contrato foi confirmado",
      "nomesAlternativos": [
       "contract"
      ]
     },
     {
      "nome": "entregaConfirmada",
      "tipo": "booleano",
      "descricao": "Indica se a entrega foi confirmada",
      "nomesAlternativos": [
       "delivery"
      ]
     },
     {
      "nome": "precoOriginal",
      "tipo": "decimal",
      "descricao": "Preço original da venda",
      "nomesAlternativos": [
       "originalPrice"
      ]
     },
     {
      "nome": "sinal",
      "tipo": "decimal",
      "descricao": "Valor pago como sinal",
      "nomesAlternativos": [
       "signal"
      ]
     },
     {
      "nome": "prestacao",
      "tipo": "decimal",
      "descricao": "Valor de cada prestação",
      "nomesAlternativos": [
       "installment"
      ]
     }
    ]
   }
  ],
  "hlm": [
   {
    "nome": "Entrega",
    "descricao": "Entrega ou encomenda da aplicação FM: dados do documento, cliente comprador, cliente de entrega, linhas de artigos e confirmação.",
    "composicao": [
     {
      "sm": "DadosEntrega",
      "cardinalidade": "1..1"
     },
     {
      "sm": "ClienteVenda",
      "papel": "Comprador",
      "cardinalidade": "1..1"
     },
     {
      "sm": "ClienteVenda",
      "papel": "Destinatario",
      "cardinalidade": "1..1"
     },
     {
      "sm": "LinhaEntrega",
      "cardinalidade": "0..*"
     },
     {
      "sm": "ConfirmacaoEntrega",
      "cardinalidade": "0..1"
     },
     {
      "sm": "Metainformacao",
      "papel": "Metainformacao",
      "cardinalidade": "0..1"
     }
    ]
   }
  ],
  "projecoes": [
   {
    "nome": "EntregaFm",
    "hlm": "Entrega",
    "descricao": "Registo de uma entrega ou encomenda na aplicação FM (documento de venda, guia de transporte).",
    "obrigatorias": [
     "DadosEntrega.numeroEntrega",
     "DadosEntrega.tipoDocumento",
     "DadosEntrega.estado",
     "DadosEntrega.data",
     "LinhaEntrega.Artigo.codigo",
     "LinhaEntrega.quantidade"
    ],
    "permitidas": [
     "DadosEntrega.numeroFatura",
     "DadosEntrega.numeroGuiaTransporte",
     "DadosEntrega.numeroContrato",
     "DadosEntrega.numeroDocumentoVenda",
     "DadosEntrega.dataRegisto",
     "Comprador.*",
     "Destinatario.*",
     "LinhaEntrega.Artigo.nome",
     "LinhaEntrega.Artigo.descricao",
     "LinhaEntrega.Artigo.codigoBarras",
     "LinhaEntrega.numeroSerie",
     "LinhaEntrega.precoPersonalizado",
     "LinhaEntrega.descontoPersonalizado",
     "ConfirmacaoEntrega.*",
     "Metainformacao.*"
    ]
   }
  ],
  "perfis": [
   {
    "nome": "EntregaPortugal",
    "projecao": "EntregaFm",
    "descricao": "Entrega a clientes com morada em Portugal.",
    "fixa": [
     {
      "propriedade": "Comprador.Morada.pais",
      "valor": "PT"
     },
     {
      "propriedade": "Destinatario.Morada.pais",
      "valor": "PT"
     }
    ]
   }
  ]
 },
 {
  "$schema": "../../../specs/declaracao/ecv.schema.json",
  "declaracao": {
   "nome": "exportacao_fm",
   "versao": "0.1.0",
   "descricao": "Exportação dos registos da aplicação FM (VDM, CLI, YCL, STK, AUX, PRV): vendedor e numerações, clientes, saldos, stocks, produtos no veículo, zonas e configuração.",
   "dominios": [
    "faturação"
   ],
   "hlm": "ExportacaoFm"
  },
  "funcoes": [
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
    "contextosExternos": [],
    "retorno": "booleano"
   }
  ],
  "usm": [
   {
    "nome": "Entidade",
    "descricao": "Pessoa singular ou coletiva identificada pelo NIF.",
    "propriedades": [
     {
      "nome": "nif",
      "tipo": "texto",
      "descricao": "Número de identificação fiscal",
      "nomesAlternativos": [
       "taxId",
       "VATNumber"
      ],
      "regras": [
       {
        "id": "RP-NIF",
        "natureza": "plausibilidade",
        "descricao": "Entidade.nif segue o padrão ^[0-9]{9}$",
        "restricao": {
         "propriedade": "nif",
         "operador": "PATTERN",
         "valor": "^[0-9]{9}$",
         "mensagem": "O NIF tem de ter nove algarismos."
        }
       },
       {
        "id": "RP-NIF-DC",
        "natureza": "plausibilidade",
        "descricao": "digitoControloValido(Entidade.nif)",
        "restricao": {
         "operador": "FUNCTION",
         "chamada": {
          "funcao": "digitoControloValido",
          "argumentos": [
           {
            "caminho": "nif"
           }
          ]
         },
         "mensagem": "O dígito de controlo do NIF não está correto."
        }
       }
      ]
     },
     {
      "nome": "nome",
      "tipo": "texto",
      "descricao": "Nome ou denominação social",
      "nomesAlternativos": [
       "name",
       "denominacao"
      ]
     }
    ]
   },
   {
    "nome": "Morada",
    "descricao": "Morada postal: arruamento, código postal, localidade, freguesia e país.",
    "propriedades": [
     {
      "nome": "rua",
      "tipo": "texto",
      "descricao": "Arruamento e número de porta"
     },
     {
      "nome": "codigoPostal",
      "tipo": "texto",
      "descricao": "Código postal da morada",
      "nomesAlternativos": [
       "zipCode",
       "postalCode",
       "CP"
      ],
      "regras": [
       {
        "id": "RP-CP",
        "natureza": "plausibilidade",
        "descricao": "Morada.codigoPostal segue o padrão ^([1-9][0-9]{3}-[0-9]{3}|[0-5][0-9]{4}|[A-Z]{1,2}[0-9][0-9A-Z]? [0-9][A-Z]{2})$",
        "restricao": {
         "propriedade": "codigoPostal",
         "operador": "PATTERN",
         "valor": "^([1-9][0-9]{3}-[0-9]{3}|[0-5][0-9]{4}|[A-Z]{1,2}[0-9][0-9A-Z]? [0-9][A-Z]{2})$",
         "mensagem": "O código postal não tem nenhum dos formatos possíveis (português, espanhol ou britânico)."
        },
        "notas": "Plausibilidade: os formatos possíveis {PT, ES, GB}. Qual se aplica decide-se por inferência (RIR-CP-PT/ES/GB)."
       }
      ]
     },
     {
      "nome": "localidade",
      "tipo": "texto",
      "descricao": "Localidade da morada (em maiúsculas, sem acentos)"
     },
     {
      "nome": "freguesia",
      "tipo": "texto",
      "descricao": "Freguesia da morada (só para moradas em Lisboa)",
      "regras": [
       {
        "id": "RP-FREGUESIA",
        "natureza": "plausibilidade",
        "descricao": "Morada.freguesia ∈ {AJUDA, ALCANTARA, ALVALADE, AREEIRO, ARROIOS, AVENIDAS_NOVAS, BEATO, BELEM, BENFICA, CAMPO_DE_OURIQUE, CAMPOLIDE, CARNIDE, ESTRELA, LUMIAR, MARVILA, MISERICORDIA, OLIVAIS, PARQUE_DAS_NACOES, PENHA_DE_FRANCA, SANTA_CLARA, SANTA_MARIA_MAIOR, SANTO_ANTONIO, SAO_DOMINGOS_DE_BENFICA, SAO_VICENTE}",
        "restricao": {
         "propriedade": "freguesia",
         "operador": "IN",
         "valor": [
          "AJUDA",
          "ALCANTARA",
          "ALVALADE",
          "AREEIRO",
          "ARROIOS",
          "AVENIDAS_NOVAS",
          "BEATO",
          "BELEM",
          "BENFICA",
          "CAMPO_DE_OURIQUE",
          "CAMPOLIDE",
          "CARNIDE",
          "ESTRELA",
          "LUMIAR",
          "MARVILA",
          "MISERICORDIA",
          "OLIVAIS",
          "PARQUE_DAS_NACOES",
          "PENHA_DE_FRANCA",
          "SANTA_CLARA",
          "SANTA_MARIA_MAIOR",
          "SANTO_ANTONIO",
          "SAO_DOMINGOS_DE_BENFICA",
          "SAO_VICENTE"
         ],
         "mensagem": "A freguesia não pertence às freguesias de Lisboa conhecidas."
        }
       }
      ]
     },
     {
      "nome": "pais",
      "tipo": "texto",
      "descricao": "País da morada (código ISO de duas letras)",
      "nomesAlternativos": [
       "country",
       "countryCode"
      ],
      "regras": [
       {
        "id": "RP-PAIS",
        "natureza": "plausibilidade",
        "descricao": "Morada.pais ∈ {PT, ES, GB}",
        "restricao": {
         "propriedade": "pais",
         "operador": "IN",
         "valor": [
          "PT",
          "ES",
          "GB"
         ],
         "mensagem": "O país tem de ser PT, ES ou GB."
        }
       }
      ]
     }
    ],
    "regras": [
     {
      "id": "RIR-CP-PT",
      "natureza": "inferencia_restritiva",
      "descricao": "Se Morada.pais = PT → Morada.codigoPostal segue o padrão ^[1-9][0-9]{3}-[0-9]{3}$",
      "condicao": [
       {
        "propriedade": "pais",
        "operador": "EQUALS",
        "valor": "PT"
       }
      ],
      "restricao": {
       "propriedade": "codigoPostal",
       "operador": "PATTERN",
       "valor": "^[1-9][0-9]{3}-[0-9]{3}$",
       "mensagem": "O código postal português tem de ter o formato 0000-000, sem começar por zero."
      }
     },
     {
      "id": "RIR-CP-ES",
      "natureza": "inferencia_restritiva",
      "descricao": "Se Morada.pais = ES → Morada.codigoPostal segue o padrão ^[0-5][0-9]{4}$",
      "condicao": [
       {
        "propriedade": "pais",
        "operador": "EQUALS",
        "valor": "ES"
       }
      ],
      "restricao": {
       "propriedade": "codigoPostal",
       "operador": "PATTERN",
       "valor": "^[0-5][0-9]{4}$",
       "mensagem": "O código postal espanhol tem de ter cinco algarismos, a começar por 0 a 5."
      }
     },
     {
      "id": "RIR-CP-GB",
      "natureza": "inferencia_restritiva",
      "descricao": "Se Morada.pais = GB → Morada.codigoPostal segue o padrão ^[A-Z]{1,2}[0-9][0-9A-Z]? [0-9][A-Z]{2}$",
      "condicao": [
       {
        "propriedade": "pais",
        "operador": "EQUALS",
        "valor": "GB"
       }
      ],
      "restricao": {
       "propriedade": "codigoPostal",
       "operador": "PATTERN",
       "valor": "^[A-Z]{1,2}[0-9][0-9A-Z]? [0-9][A-Z]{2}$",
       "mensagem": "O código postal britânico tem de ter a forma de um postcode (ex.: SW1A 1AA)."
      }
     },
     {
      "id": "RIR-CP-LX-AJUDA",
      "natureza": "inferencia_restritiva",
      "descricao": "Se Morada.pais = PT e Morada.localidade = LISBOA e Morada.freguesia = AJUDA → Morada.codigoPostal segue o padrão ^(1300|1349)-[0-9]{3}$",
      "condicao": [
       {
        "propriedade": "pais",
        "operador": "EQUALS",
        "valor": "PT"
       },
       {
        "propriedade": "localidade",
        "operador": "EQUALS",
        "valor": "LISBOA"
       },
       {
        "propriedade": "freguesia",
        "operador": "EQUALS",
        "valor": "AJUDA"
       }
      ],
      "restricao": {
       "propriedade": "codigoPostal",
       "operador": "PATTERN",
       "valor": "^(1300|1349)-[0-9]{3}$",
       "mensagem": "O código postal de uma morada da freguesia Ajuda (Lisboa) começa por 1300 ou 1349."
      },
      "notas": "Mapeamento conhecido (códigos postais por freguesia de Lisboa) convertido em RIR: uma regra por freguesia. A vista de decisão sobre Morada.codigoPostal reconstrói a tabela."
     },
     {
      "id": "RIR-CP-LX-ALCANTARA",
      "natureza": "inferencia_restritiva",
      "descricao": "Se Morada.pais = PT e Morada.localidade = LISBOA e Morada.freguesia = ALCANTARA → Morada.codigoPostal segue o padrão ^(1300|1350)-[0-9]{3}$",
      "condicao": [
       {
        "propriedade": "pais",
        "operador": "EQUALS",
        "valor": "PT"
       },
       {
        "propriedade": "localidade",
        "operador": "EQUALS",
        "valor": "LISBOA"
       },
       {
        "propriedade": "freguesia",
        "operador": "EQUALS",
        "valor": "ALCANTARA"
       }
      ],
      "restricao": {
       "propriedade": "codigoPostal",
       "operador": "PATTERN",
       "valor": "^(1300|1350)-[0-9]{3}$",
       "mensagem": "O código postal de uma morada da freguesia Alcantara (Lisboa) começa por 1300 ou 1350."
      }
     },
     {
      "id": "RIR-CP-LX-ALVALADE",
      "natureza": "inferencia_restritiva",
      "descricao": "Se Morada.pais = PT e Morada.localidade = LISBOA e Morada.freguesia = ALVALADE → Morada.codigoPostal segue o padrão ^(1700|1749)-[0-9]{3}$",
      "condicao": [
       {
        "propriedade": "pais",
        "operador": "EQUALS",
        "valor": "PT"
       },
       {
        "propriedade": "localidade",
        "operador": "EQUALS",
        "valor": "LISBOA"
       },
       {
        "propriedade": "freguesia",
        "operador": "EQUALS",
        "valor": "ALVALADE"
       }
      ],
      "restricao": {
       "propriedade": "codigoPostal",
       "operador": "PATTERN",
       "valor": "^(1700|1749)-[0-9]{3}$",
       "mensagem": "O código postal de uma morada da freguesia Alvalade (Lisboa) começa por 1700 ou 1749."
      }
     },
     {
      "id": "RIR-CP-LX-AREEIRO",
      "natureza": "inferencia_restritiva",
      "descricao": "Se Morada.pais = PT e Morada.localidade = LISBOA e Morada.freguesia = AREEIRO → Morada.codigoPostal segue o padrão ^(1000|1049)-[0-9]{3}$",
      "condicao": [
       {
        "propriedade": "pais",
        "operador": "EQUALS",
        "valor": "PT"
       },
       {
        "propriedade": "localidade",
        "operador": "EQUALS",
        "valor": "LISBOA"
       },
       {
        "propriedade": "freguesia",
        "operador": "EQUALS",
        "valor": "AREEIRO"
       }
      ],
      "restricao": {
       "propriedade": "codigoPostal",
       "operador": "PATTERN",
       "valor": "^(1000|1049)-[0-9]{3}$",
       "mensagem": "O código postal de uma morada da freguesia Areeiro (Lisboa) começa por 1000 ou 1049."
      }
     },
     {
      "id": "RIR-CP-LX-ARROIOS",
      "natureza": "inferencia_restritiva",
      "descricao": "Se Morada.pais = PT e Morada.localidade = LISBOA e Morada.freguesia = ARROIOS → Morada.codigoPostal segue o padrão ^(1150|1169)-[0-9]{3}$",
      "condicao": [
       {
        "propriedade": "pais",
        "operador": "EQUALS",
        "valor": "PT"
       },
       {
        "propriedade": "localidade",
        "operador": "EQUALS",
        "valor": "LISBOA"
       },
       {
        "propriedade": "freguesia",
        "operador": "EQUALS",
        "valor": "ARROIOS"
       }
      ],
      "restricao": {
       "propriedade": "codigoPostal",
       "operador": "PATTERN",
       "valor": "^(1150|1169)-[0-9]{3}$",
       "mensagem": "O código postal de uma morada da freguesia Arroios (Lisboa) começa por 1150 ou 1169."
      }
     },
     {
      "id": "RIR-CP-LX-AVENIDAS-NOVAS",
      "natureza": "inferencia_restritiva",
      "descricao": "Se Morada.pais = PT e Morada.localidade = LISBOA e Morada.freguesia = AVENIDAS_NOVAS → Morada.codigoPostal segue o padrão ^(1050|1069)-[0-9]{3}$",
      "condicao": [
       {
        "propriedade": "pais",
        "operador": "EQUALS",
        "valor": "PT"
       },
       {
        "propriedade": "localidade",
        "operador": "EQUALS",
        "valor": "LISBOA"
       },
       {
        "propriedade": "freguesia",
        "operador": "EQUALS",
        "valor": "AVENIDAS_NOVAS"
       }
      ],
      "restricao": {
       "propriedade": "codigoPostal",
       "operador": "PATTERN",
       "valor": "^(1050|1069)-[0-9]{3}$",
       "mensagem": "O código postal de uma morada da freguesia Avenidas Novas (Lisboa) começa por 1050 ou 1069."
      }
     },
     {
      "id": "RIR-CP-LX-BEATO",
      "natureza": "inferencia_restritiva",
      "descricao": "Se Morada.pais = PT e Morada.localidade = LISBOA e Morada.freguesia = BEATO → Morada.codigoPostal segue o padrão ^(1900|1949)-[0-9]{3}$",
      "condicao": [
       {
        "propriedade": "pais",
        "operador": "EQUALS",
        "valor": "PT"
       },
       {
        "propriedade": "localidade",
        "operador": "EQUALS",
        "valor": "LISBOA"
       },
       {
        "propriedade": "freguesia",
        "operador": "EQUALS",
        "valor": "BEATO"
       }
      ],
      "restricao": {
       "propriedade": "codigoPostal",
       "operador": "PATTERN",
       "valor": "^(1900|1949)-[0-9]{3}$",
       "mensagem": "O código postal de uma morada da freguesia Beato (Lisboa) começa por 1900 ou 1949."
      }
     },
     {
      "id": "RIR-CP-LX-BELEM",
      "natureza": "inferencia_restritiva",
      "descricao": "Se Morada.pais = PT e Morada.localidade = LISBOA e Morada.freguesia = BELEM → Morada.codigoPostal segue o padrão ^(1400|1449)-[0-9]{3}$",
      "condicao": [
       {
        "propriedade": "pais",
        "operador": "EQUALS",
        "valor": "PT"
       },
       {
        "propriedade": "localidade",
        "operador": "EQUALS",
        "valor": "LISBOA"
       },
       {
        "propriedade": "freguesia",
        "operador": "EQUALS",
        "valor": "BELEM"
       }
      ],
      "restricao": {
       "propriedade": "codigoPostal",
       "operador": "PATTERN",
       "valor": "^(1400|1449)-[0-9]{3}$",
       "mensagem": "O código postal de uma morada da freguesia Belem (Lisboa) começa por 1400 ou 1449."
      }
     },
     {
      "id": "RIR-CP-LX-BENFICA",
      "natureza": "inferencia_restritiva",
      "descricao": "Se Morada.pais = PT e Morada.localidade = LISBOA e Morada.freguesia = BENFICA → Morada.codigoPostal segue o padrão ^(1500|1549)-[0-9]{3}$",
      "condicao": [
       {
        "propriedade": "pais",
        "operador": "EQUALS",
        "valor": "PT"
       },
       {
        "propriedade": "localidade",
        "operador": "EQUALS",
        "valor": "LISBOA"
       },
       {
        "propriedade": "freguesia",
        "operador": "EQUALS",
        "valor": "BENFICA"
       }
      ],
      "restricao": {
       "propriedade": "codigoPostal",
       "operador": "PATTERN",
       "valor": "^(1500|1549)-[0-9]{3}$",
       "mensagem": "O código postal de uma morada da freguesia Benfica (Lisboa) começa por 1500 ou 1549."
      }
     },
     {
      "id": "RIR-CP-LX-CAMPO-DE-OURIQUE",
      "natureza": "inferencia_restritiva",
      "descricao": "Se Morada.pais = PT e Morada.localidade = LISBOA e Morada.freguesia = CAMPO_DE_OURIQUE → Morada.codigoPostal segue o padrão ^(1250|1350)-[0-9]{3}$",
      "condicao": [
       {
        "propriedade": "pais",
        "operador": "EQUALS",
        "valor": "PT"
       },
       {
        "propriedade": "localidade",
        "operador": "EQUALS",
        "valor": "LISBOA"
       },
       {
        "propriedade": "freguesia",
        "operador": "EQUALS",
        "valor": "CAMPO_DE_OURIQUE"
       }
      ],
      "restricao": {
       "propriedade": "codigoPostal",
       "operador": "PATTERN",
       "valor": "^(1250|1350)-[0-9]{3}$",
       "mensagem": "O código postal de uma morada da freguesia Campo de Ourique (Lisboa) começa por 1250 ou 1350."
      }
     },
     {
      "id": "RIR-CP-LX-CAMPOLIDE",
      "natureza": "inferencia_restritiva",
      "descricao": "Se Morada.pais = PT e Morada.localidade = LISBOA e Morada.freguesia = CAMPOLIDE → Morada.codigoPostal segue o padrão ^(1070|1099)-[0-9]{3}$",
      "condicao": [
       {
        "propriedade": "pais",
        "operador": "EQUALS",
        "valor": "PT"
       },
       {
        "propriedade": "localidade",
        "operador": "EQUALS",
        "valor": "LISBOA"
       },
       {
        "propriedade": "freguesia",
        "operador": "EQUALS",
        "valor": "CAMPOLIDE"
       }
      ],
      "restricao": {
       "propriedade": "codigoPostal",
       "operador": "PATTERN",
       "valor": "^(1070|1099)-[0-9]{3}$",
       "mensagem": "O código postal de uma morada da freguesia Campolide (Lisboa) começa por 1070 ou 1099."
      }
     },
     {
      "id": "RIR-CP-LX-CARNIDE",
      "natureza": "inferencia_restritiva",
      "descricao": "Se Morada.pais = PT e Morada.localidade = LISBOA e Morada.freguesia = CARNIDE → Morada.codigoPostal segue o padrão ^(1600|1649)-[0-9]{3}$",
      "condicao": [
       {
        "propriedade": "pais",
        "operador": "EQUALS",
        "valor": "PT"
       },
       {
        "propriedade": "localidade",
        "operador": "EQUALS",
        "valor": "LISBOA"
       },
       {
        "propriedade": "freguesia",
        "operador": "EQUALS",
        "valor": "CARNIDE"
       }
      ],
      "restricao": {
       "propriedade": "codigoPostal",
       "operador": "PATTERN",
       "valor": "^(1600|1649)-[0-9]{3}$",
       "mensagem": "O código postal de uma morada da freguesia Carnide (Lisboa) começa por 1600 ou 1649."
      }
     },
     {
      "id": "RIR-CP-LX-ESTRELA",
      "natureza": "inferencia_restritiva",
      "descricao": "Se Morada.pais = PT e Morada.localidade = LISBOA e Morada.freguesia = ESTRELA → Morada.codigoPostal segue o padrão ^(1200|1249)-[0-9]{3}$",
      "condicao": [
       {
        "propriedade": "pais",
        "operador": "EQUALS",
        "valor": "PT"
       },
       {
        "propriedade": "localidade",
        "operador": "EQUALS",
        "valor": "LISBOA"
       },
       {
        "propriedade": "freguesia",
        "operador": "EQUALS",
        "valor": "ESTRELA"
       }
      ],
      "restricao": {
       "propriedade": "codigoPostal",
       "operador": "PATTERN",
       "valor": "^(1200|1249)-[0-9]{3}$",
       "mensagem": "O código postal de uma morada da freguesia Estrela (Lisboa) começa por 1200 ou 1249."
      }
     },
     {
      "id": "RIR-CP-LX-LUMIAR",
      "natureza": "inferencia_restritiva",
      "descricao": "Se Morada.pais = PT e Morada.localidade = LISBOA e Morada.freguesia = LUMIAR → Morada.codigoPostal segue o padrão ^(1600|1750)-[0-9]{3}$",
      "condicao": [
       {
        "propriedade": "pais",
        "operador": "EQUALS",
        "valor": "PT"
       },
       {
        "propriedade": "localidade",
        "operador": "EQUALS",
        "valor": "LISBOA"
       },
       {
        "propriedade": "freguesia",
        "operador": "EQUALS",
        "valor": "LUMIAR"
       }
      ],
      "restricao": {
       "propriedade": "codigoPostal",
       "operador": "PATTERN",
       "valor": "^(1600|1750)-[0-9]{3}$",
       "mensagem": "O código postal de uma morada da freguesia Lumiar (Lisboa) começa por 1600 ou 1750."
      }
     },
     {
      "id": "RIR-CP-LX-MARVILA",
      "natureza": "inferencia_restritiva",
      "descricao": "Se Morada.pais = PT e Morada.localidade = LISBOA e Morada.freguesia = MARVILA → Morada.codigoPostal segue o padrão ^(1800|1949)-[0-9]{3}$",
      "condicao": [
       {
        "propriedade": "pais",
        "operador": "EQUALS",
        "valor": "PT"
       },
       {
        "propriedade": "localidade",
        "operador": "EQUALS",
        "valor": "LISBOA"
       },
       {
        "propriedade": "freguesia",
        "operador": "EQUALS",
        "valor": "MARVILA"
       }
      ],
      "restricao": {
       "propriedade": "codigoPostal",
       "operador": "PATTERN",
       "valor": "^(1800|1949)-[0-9]{3}$",
       "mensagem": "O código postal de uma morada da freguesia Marvila (Lisboa) começa por 1800 ou 1949."
      }
     },
     {
      "id": "RIR-CP-LX-MISERICORDIA",
      "natureza": "inferencia_restritiva",
      "descricao": "Se Morada.pais = PT e Morada.localidade = LISBOA e Morada.freguesia = MISERICORDIA → Morada.codigoPostal segue o padrão ^(1200|1249)-[0-9]{3}$",
      "condicao": [
       {
        "propriedade": "pais",
        "operador": "EQUALS",
        "valor": "PT"
       },
       {
        "propriedade": "localidade",
        "operador": "EQUALS",
        "valor": "LISBOA"
       },
       {
        "propriedade": "freguesia",
        "operador": "EQUALS",
        "valor": "MISERICORDIA"
       }
      ],
      "restricao": {
       "propriedade": "codigoPostal",
       "operador": "PATTERN",
       "valor": "^(1200|1249)-[0-9]{3}$",
       "mensagem": "O código postal de uma morada da freguesia Misericordia (Lisboa) começa por 1200 ou 1249."
      }
     },
     {
      "id": "RIR-CP-LX-OLIVAIS",
      "natureza": "inferencia_restritiva",
      "descricao": "Se Morada.pais = PT e Morada.localidade = LISBOA e Morada.freguesia = OLIVAIS → Morada.codigoPostal segue o padrão ^(1800|1885)-[0-9]{3}$",
      "condicao": [
       {
        "propriedade": "pais",
        "operador": "EQUALS",
        "valor": "PT"
       },
       {
        "propriedade": "localidade",
        "operador": "EQUALS",
        "valor": "LISBOA"
       },
       {
        "propriedade": "freguesia",
        "operador": "EQUALS",
        "valor": "OLIVAIS"
       }
      ],
      "restricao": {
       "propriedade": "codigoPostal",
       "operador": "PATTERN",
       "valor": "^(1800|1885)-[0-9]{3}$",
       "mensagem": "O código postal de uma morada da freguesia Olivais (Lisboa) começa por 1800 ou 1885."
      }
     },
     {
      "id": "RIR-CP-LX-PARQUE-DAS-NACOES",
      "natureza": "inferencia_restritiva",
      "descricao": "Se Morada.pais = PT e Morada.localidade = LISBOA e Morada.freguesia = PARQUE_DAS_NACOES → Morada.codigoPostal segue o padrão ^(1990|1998)-[0-9]{3}$",
      "condicao": [
       {
        "propriedade": "pais",
        "operador": "EQUALS",
        "valor": "PT"
       },
       {
        "propriedade": "localidade",
        "operador": "EQUALS",
        "valor": "LISBOA"
       },
       {
        "propriedade": "freguesia",
        "operador": "EQUALS",
        "valor": "PARQUE_DAS_NACOES"
       }
      ],
      "restricao": {
       "propriedade": "codigoPostal",
       "operador": "PATTERN",
       "valor": "^(1990|1998)-[0-9]{3}$",
       "mensagem": "O código postal de uma morada da freguesia Parque das Nacoes (Lisboa) começa por 1990 ou 1998."
      }
     },
     {
      "id": "RIR-CP-LX-PENHA-DE-FRANCA",
      "natureza": "inferencia_restritiva",
      "descricao": "Se Morada.pais = PT e Morada.localidade = LISBOA e Morada.freguesia = PENHA_DE_FRANCA → Morada.codigoPostal segue o padrão ^(1170|1199)-[0-9]{3}$",
      "condicao": [
       {
        "propriedade": "pais",
        "operador": "EQUALS",
        "valor": "PT"
       },
       {
        "propriedade": "localidade",
        "operador": "EQUALS",
        "valor": "LISBOA"
       },
       {
        "propriedade": "freguesia",
        "operador": "EQUALS",
        "valor": "PENHA_DE_FRANCA"
       }
      ],
      "restricao": {
       "propriedade": "codigoPostal",
       "operador": "PATTERN",
       "valor": "^(1170|1199)-[0-9]{3}$",
       "mensagem": "O código postal de uma morada da freguesia Penha de Franca (Lisboa) começa por 1170 ou 1199."
      }
     },
     {
      "id": "RIR-CP-LX-SANTA-CLARA",
      "natureza": "inferencia_restritiva",
      "descricao": "Se Morada.pais = PT e Morada.localidade = LISBOA e Morada.freguesia = SANTA_CLARA → Morada.codigoPostal segue o padrão ^(1750|1769)-[0-9]{3}$",
      "condicao": [
       {
        "propriedade": "pais",
        "operador": "EQUALS",
        "valor": "PT"
       },
       {
        "propriedade": "localidade",
        "operador": "EQUALS",
        "valor": "LISBOA"
       },
       {
        "propriedade": "freguesia",
        "operador": "EQUALS",
        "valor": "SANTA_CLARA"
       }
      ],
      "restricao": {
       "propriedade": "codigoPostal",
       "operador": "PATTERN",
       "valor": "^(1750|1769)-[0-9]{3}$",
       "mensagem": "O código postal de uma morada da freguesia Santa Clara (Lisboa) começa por 1750 ou 1769."
      }
     },
     {
      "id": "RIR-CP-LX-SANTA-MARIA-MAIOR",
      "natureza": "inferencia_restritiva",
      "descricao": "Se Morada.pais = PT e Morada.localidade = LISBOA e Morada.freguesia = SANTA_MARIA_MAIOR → Morada.codigoPostal segue o padrão ^(1100|1149)-[0-9]{3}$",
      "condicao": [
       {
        "propriedade": "pais",
        "operador": "EQUALS",
        "valor": "PT"
       },
       {
        "propriedade": "localidade",
        "operador": "EQUALS",
        "valor": "LISBOA"
       },
       {
        "propriedade": "freguesia",
        "operador": "EQUALS",
        "valor": "SANTA_MARIA_MAIOR"
       }
      ],
      "restricao": {
       "propriedade": "codigoPostal",
       "operador": "PATTERN",
       "valor": "^(1100|1149)-[0-9]{3}$",
       "mensagem": "O código postal de uma morada da freguesia Santa Maria Maior (Lisboa) começa por 1100 ou 1149."
      }
     },
     {
      "id": "RIR-CP-LX-SANTO-ANTONIO",
      "natureza": "inferencia_restritiva",
      "descricao": "Se Morada.pais = PT e Morada.localidade = LISBOA e Morada.freguesia = SANTO_ANTONIO → Morada.codigoPostal segue o padrão ^(1250|1269)-[0-9]{3}$",
      "condicao": [
       {
        "propriedade": "pais",
        "operador": "EQUALS",
        "valor": "PT"
       },
       {
        "propriedade": "localidade",
        "operador": "EQUALS",
        "valor": "LISBOA"
       },
       {
        "propriedade": "freguesia",
        "operador": "EQUALS",
        "valor": "SANTO_ANTONIO"
       }
      ],
      "restricao": {
       "propriedade": "codigoPostal",
       "operador": "PATTERN",
       "valor": "^(1250|1269)-[0-9]{3}$",
       "mensagem": "O código postal de uma morada da freguesia Santo Antonio (Lisboa) começa por 1250 ou 1269."
      }
     },
     {
      "id": "RIR-CP-LX-SAO-DOMINGOS-DE-BENFICA",
      "natureza": "inferencia_restritiva",
      "descricao": "Se Morada.pais = PT e Morada.localidade = LISBOA e Morada.freguesia = SAO_DOMINGOS_DE_BENFICA → Morada.codigoPostal segue o padrão ^(1500|1600)-[0-9]{3}$",
      "condicao": [
       {
        "propriedade": "pais",
        "operador": "EQUALS",
        "valor": "PT"
       },
       {
        "propriedade": "localidade",
        "operador": "EQUALS",
        "valor": "LISBOA"
       },
       {
        "propriedade": "freguesia",
        "operador": "EQUALS",
        "valor": "SAO_DOMINGOS_DE_BENFICA"
       }
      ],
      "restricao": {
       "propriedade": "codigoPostal",
       "operador": "PATTERN",
       "valor": "^(1500|1600)-[0-9]{3}$",
       "mensagem": "O código postal de uma morada da freguesia Sao Domingos de Benfica (Lisboa) começa por 1500 ou 1600."
      }
     },
     {
      "id": "RIR-CP-LX-SAO-VICENTE",
      "natureza": "inferencia_restritiva",
      "descricao": "Se Morada.pais = PT e Morada.localidade = LISBOA e Morada.freguesia = SAO_VICENTE → Morada.codigoPostal segue o padrão ^(1100|1170)-[0-9]{3}$",
      "condicao": [
       {
        "propriedade": "pais",
        "operador": "EQUALS",
        "valor": "PT"
       },
       {
        "propriedade": "localidade",
        "operador": "EQUALS",
        "valor": "LISBOA"
       },
       {
        "propriedade": "freguesia",
        "operador": "EQUALS",
        "valor": "SAO_VICENTE"
       }
      ],
      "restricao": {
       "propriedade": "codigoPostal",
       "operador": "PATTERN",
       "valor": "^(1100|1170)-[0-9]{3}$",
       "mensagem": "O código postal de uma morada da freguesia Sao Vicente (Lisboa) começa por 1100 ou 1170."
      }
     }
    ]
   },
   {
    "nome": "Contacto",
    "descricao": "Contacto eletrónico de uma entidade.",
    "propriedades": [
     {
      "nome": "email",
      "tipo": "texto",
      "descricao": "Endereço de correio eletrónico",
      "nomesAlternativos": [
       "eMail",
       "correioEletronico"
      ],
      "regras": [
       {
        "id": "RP-EMAIL",
        "natureza": "plausibilidade",
        "descricao": "Contacto.email segue o padrão ^[a-z0-9._-]+@[a-z0-9-]+(\\.[a-z0-9-]+)+$",
        "restricao": {
         "propriedade": "email",
         "operador": "PATTERN",
         "valor": "^[a-z0-9._-]+@[a-z0-9-]+(\\.[a-z0-9-]+)+$",
         "mensagem": "O email tem de ter uma parte local e um domínio com pelo menos um ponto, sem espaços nem maiúsculas."
        }
       }
      ]
     }
    ]
   },
   {
    "nome": "ContactoTelefonico",
    "descricao": "Contactos telefónicos de uma pessoa ou entidade: telefone e telemóvel.",
    "propriedades": [
     {
      "nome": "telefone",
      "tipo": "texto",
      "descricao": "Número de telefone (rede fixa ou geral)",
      "nomesAlternativos": [
       "Telephone",
       "fixePhoneNumber"
      ],
      "regras": [
       {
        "id": "RP-TELEFONE",
        "natureza": "plausibilidade",
        "restricao": {
         "propriedade": "telefone",
         "operador": "LENGTH",
         "valor": [
          1,
          200
         ],
         "mensagem": "O telefone tem de ter entre 1 e 200 caracteres."
        },
        "descricao": "ContactoTelefonico.telefone tem entre 1 e 200 caracteres"
       }
      ]
     },
     {
      "nome": "telemovel",
      "tipo": "texto",
      "descricao": "Número de telemóvel",
      "nomesAlternativos": [
       "phoneNumber",
       "mobile"
      ]
     }
    ]
   },
   {
    "nome": "DocumentoIdentificacao",
    "descricao": "Documento de identificação pessoal (ex.: cartão de cidadão): número e data de validade.",
    "propriedades": [
     {
      "nome": "numero",
      "tipo": "texto",
      "descricao": "Número do documento de identificação",
      "nomesAlternativos": [
       "citizenCard"
      ]
     },
     {
      "nome": "dataValidade",
      "tipo": "data",
      "descricao": "Data de validade do documento de identificação",
      "nomesAlternativos": [
       "citizenCardExpirationDate"
      ]
     }
    ]
   },
   {
    "nome": "Artigo",
    "descricao": "Bem ou serviço transacionado: designação, descrição, códigos de identificação e país de origem.",
    "propriedades": [
     {
      "nome": "nome",
      "tipo": "texto",
      "descricao": "Designação do bem ou serviço",
      "nomesAlternativos": [
       "Item name",
       "description"
      ],
      "regras": [
       {
        "id": "RP-ART-NOME",
        "natureza": "plausibilidade",
        "restricao": {
         "propriedade": "nome",
         "operador": "LENGTH",
         "valor": [
          1,
          200
         ],
         "mensagem": "A designação do artigo tem de ter entre 1 e 200 caracteres."
        },
        "descricao": "Artigo.nome tem entre 1 e 200 caracteres"
       }
      ]
     },
     {
      "nome": "descricao",
      "tipo": "texto",
      "descricao": "Descrição detalhada do bem ou serviço",
      "nomesAlternativos": [
       "Item description"
      ],
      "regras": [
       {
        "id": "RP-ART-DESC",
        "natureza": "plausibilidade",
        "restricao": {
         "propriedade": "descricao",
         "operador": "LENGTH",
         "valor": [
          1,
          200
         ],
         "mensagem": "A descrição do artigo tem de ter entre 1 e 200 caracteres."
        },
        "descricao": "Artigo.descricao tem entre 1 e 200 caracteres"
       }
      ]
     },
     {
      "nome": "codigo",
      "tipo": "texto",
      "descricao": "Código do artigo atribuído pelo vendedor",
      "nomesAlternativos": [
       "Item Seller s identifier",
       "code"
      ],
      "regras": [
       {
        "id": "RP-ART-CODIGO",
        "natureza": "plausibilidade",
        "restricao": {
         "propriedade": "codigo",
         "operador": "LENGTH",
         "valor": [
          1,
          50
         ],
         "mensagem": "O código do artigo tem de ter entre 1 e 50 caracteres."
        },
        "descricao": "Artigo.codigo tem entre 1 e 50 caracteres"
       }
      ]
     },
     {
      "nome": "codigoComprador",
      "tipo": "texto",
      "descricao": "Código do artigo atribuído pelo comprador",
      "nomesAlternativos": [
       "Item Buyer s identifier"
      ],
      "regras": [
       {
        "id": "RP-ART-CODCOMP",
        "natureza": "plausibilidade",
        "restricao": {
         "propriedade": "codigoComprador",
         "operador": "LENGTH",
         "valor": [
          1,
          50
         ],
         "mensagem": "O código do artigo do comprador tem de ter entre 1 e 50 caracteres."
        },
        "descricao": "Artigo.codigoComprador tem entre 1 e 50 caracteres"
       }
      ]
     },
     {
      "nome": "codigoBarras",
      "tipo": "texto",
      "descricao": "Identificador normalizado do artigo (EAN/GTIN)",
      "nomesAlternativos": [
       "Item standard identifier",
       "barCode",
       "EAN"
      ],
      "regras": [
       {
        "id": "RP-ART-CODBARRAS",
        "natureza": "plausibilidade",
        "restricao": {
         "propriedade": "codigoBarras",
         "operador": "LENGTH",
         "valor": [
          1,
          50
         ],
         "mensagem": "O código EAN tem de ter entre 1 e 50 caracteres."
        },
        "descricao": "Artigo.codigoBarras tem entre 1 e 50 caracteres"
       }
      ]
     },
     {
      "nome": "classificacao",
      "tipo": "texto",
      "descricao": "Código de classificação da mercadoria (ex.: CPV)",
      "nomesAlternativos": [
       "Item classification identifier",
       "CPV"
      ],
      "regras": [
       {
        "id": "RP-ART-CLASSIF",
        "natureza": "plausibilidade",
        "restricao": {
         "propriedade": "classificacao",
         "operador": "LENGTH",
         "valor": [
          1,
          50
         ],
         "mensagem": "O código de classificação tem de ter entre 1 e 50 caracteres."
        },
        "descricao": "Artigo.classificacao tem entre 1 e 50 caracteres"
       }
      ]
     },
     {
      "nome": "paisOrigem",
      "tipo": "texto",
      "descricao": "País de origem do artigo (código ISO 3166-1 alfa-2)",
      "nomesAlternativos": [
       "Item country of origin"
      ],
      "regras": [
       {
        "id": "RP-ART-PAIS",
        "natureza": "plausibilidade",
        "restricao": {
         "propriedade": "paisOrigem",
         "operador": "PATTERN",
         "valor": "^[A-Z]{2}$",
         "mensagem": "O país de origem tem de ser um código ISO 3166-1 de duas letras."
        },
        "descricao": "Artigo.paisOrigem segue o padrão ^[A-Z]{2}$"
       }
      ]
     }
    ]
   },
   {
    "nome": "Veiculo",
    "descricao": "Veículo identificado pela matrícula, com a marca e o modelo.",
    "propriedades": [
     {
      "nome": "matricula",
      "tipo": "texto",
      "descricao": "Matrícula do veículo",
      "nomesAlternativos": [
       "carRegistration",
       "Matricula"
      ],
      "regras": [
       {
        "id": "RP-VEIC-MATRICULA",
        "natureza": "plausibilidade",
        "restricao": {
         "propriedade": "matricula",
         "operador": "LENGTH",
         "valor": [
          0,
          15
         ],
         "mensagem": "A matrícula tem no máximo 15 caracteres."
        },
        "descricao": "Veiculo.matricula tem entre 0 e 15 caracteres"
       }
      ]
     },
     {
      "nome": "marca",
      "tipo": "texto",
      "descricao": "Marca ou designação do veículo",
      "nomesAlternativos": [
       "car",
       "Veiculo"
      ],
      "regras": [
       {
        "id": "RP-VEIC-MARCA",
        "natureza": "plausibilidade",
        "restricao": {
         "propriedade": "marca",
         "operador": "LENGTH",
         "valor": [
          0,
          25
         ],
         "mensagem": "A designação do veículo tem no máximo 25 caracteres."
        },
        "descricao": "Veiculo.marca tem entre 0 e 25 caracteres"
       }
      ]
     },
     {
      "nome": "modelo",
      "tipo": "texto",
      "descricao": "Modelo do veículo",
      "nomesAlternativos": [
       "carModel",
       "Modelo"
      ],
      "regras": [
       {
        "id": "RP-VEIC-MODELO",
        "natureza": "plausibilidade",
        "restricao": {
         "propriedade": "modelo",
         "operador": "LENGTH",
         "valor": [
          0,
          20
         ],
         "mensagem": "O modelo do veículo tem no máximo 20 caracteres."
        },
        "descricao": "Veiculo.modelo tem entre 0 e 20 caracteres"
       }
      ]
     }
    ]
   },
   {
    "nome": "NumeracaoDocumento",
    "descricao": "Estado da numeração de um tipo de documento numa série: último número, data do último documento e prefixo ATCUD.",
    "propriedades": [
     {
      "nome": "tipoDocumento",
      "tipo": "texto",
      "descricao": "Tipo de documento numerado na série",
      "regras": [
       {
        "id": "RP-NUM-TIPO",
        "natureza": "plausibilidade",
        "restricao": {
         "propriedade": "tipoDocumento",
         "operador": "IN",
         "valor": [
          "ENCOMENDA",
          "FATURA",
          "FATURA_RECIBO",
          "NOTA_CREDITO",
          "ALTERACAO_ENCOMENDA",
          "RECEBIMENTO",
          "RECIBO",
          "ENTRADA_CC"
         ],
         "mensagem": "O tipo de documento numerado tem de ser ENCOMENDA, FATURA, FATURA_RECIBO, NOTA_CREDITO, ALTERACAO_ENCOMENDA, RECEBIMENTO, RECIBO ou ENTRADA_CC."
        },
        "descricao": "NumeracaoDocumento.tipoDocumento ∈ {ENCOMENDA, FATURA, FATURA_RECIBO, NOTA_CREDITO, ALTERACAO_ENCOMENDA, RECEBIMENTO, RECIBO, ENTRADA_CC}"
       }
      ]
     },
     {
      "nome": "ultimoNumero",
      "tipo": "inteiro",
      "descricao": "Número do último documento emitido deste tipo"
     },
     {
      "nome": "dataUltimo",
      "tipo": "data",
      "descricao": "Data do último documento emitido deste tipo"
     },
     {
      "nome": "prefixoAtcud",
      "tipo": "texto",
      "descricao": "Prefixo ATCUD (código de validação da série) para este tipo de documento",
      "regras": [
       {
        "id": "RP-NUM-ATCUD",
        "natureza": "plausibilidade",
        "restricao": {
         "propriedade": "prefixoAtcud",
         "operador": "LENGTH",
         "valor": [
          0,
          10
         ],
         "mensagem": "O prefixo ATCUD do tipo de documento tem no máximo 10 caracteres."
        },
        "descricao": "NumeracaoDocumento.prefixoAtcud tem entre 0 e 10 caracteres"
       }
      ]
     }
    ]
   },
   {
    "nome": "ParametroConfiguracao",
    "descricao": "Parâmetro de configuração expresso como um par nome e valor.",
    "propriedades": [
     {
      "nome": "nome",
      "tipo": "texto",
      "descricao": "Nome do parâmetro",
      "nomesAlternativos": [
       "prop",
       "propertyName"
      ]
     },
     {
      "nome": "valor",
      "tipo": "texto",
      "descricao": "Valor do parâmetro",
      "nomesAlternativos": [
       "value",
       "propertyValue"
      ]
     }
    ]
   }
  ],
  "sm": [
   {
    "nome": "Metainformacao",
    "descricao": "Metainformação do próprio modelo: origem, versão da fonte, entidade de origem, utilização e domínio.",
    "propriedades": [
     {
      "nome": "origemModelo",
      "tipo": "texto",
      "descricao": "Fonte do modelo de dados (norma, sistema ou repositório)"
     },
     {
      "nome": "versaoOrigem",
      "tipo": "texto",
      "descricao": "Versão da fonte usada"
     },
     {
      "nome": "referenciaOrigem",
      "tipo": "texto",
      "descricao": "Identificador da entidade na fonte (ex.: BG-0 Invoice, Device)"
     },
     {
      "nome": "utilizacao",
      "tipo": "texto",
      "descricao": "Finalidade ou contexto de utilização do modelo"
     },
     {
      "nome": "dominio",
      "tipo": "texto",
      "descricao": "Domínio a que o modelo pertence"
     },
     {
      "nome": "observacoes",
      "tipo": "texto",
      "descricao": "Outra metainformação relevante sobre o modelo"
     }
    ]
   },
   {
    "nome": "ClienteVenda",
    "descricao": "Cliente da aplicação de vendas FM: identificação, morada, contactos, documento de identificação, segundo titular e dados comerciais (zona, vendedor, cobrança).",
    "notas": "O SM Cliente existente não serve tal e qual (só tem Entidade, Morada e consentimento); este é o cliente operacional do FM, com segundo titular.",
    "composicao": [
     {
      "usm": "Entidade",
      "cardinalidade": "1..1"
     },
     {
      "usm": "Morada",
      "cardinalidade": "1..1"
     },
     {
      "usm": "Contacto",
      "cardinalidade": "0..1"
     },
     {
      "usm": "ContactoTelefonico",
      "cardinalidade": "0..1"
     },
     {
      "usm": "DocumentoIdentificacao",
      "papel": "CartaoCidadao",
      "cardinalidade": "0..1"
     },
     {
      "usm": "Entidade",
      "papel": "SegundoTitular",
      "cardinalidade": "0..1"
     },
     {
      "usm": "Morada",
      "papel": "MoradaSegundoTitular",
      "cardinalidade": "0..1"
     },
     {
      "usm": "ContactoTelefonico",
      "papel": "ContactoSegundoTitular",
      "cardinalidade": "0..1"
     },
     {
      "usm": "DocumentoIdentificacao",
      "papel": "CartaoCidadaoSegundoTitular",
      "cardinalidade": "0..1"
     }
    ],
    "propriedades": [
     {
      "nome": "codigo",
      "tipo": "texto",
      "descricao": "Código do cliente na aplicação (atribuído automaticamente e imutável)",
      "nomesAlternativos": [
       "code",
       "Codigo Cliente"
      ]
     },
     {
      "nome": "designacaoPostal",
      "tipo": "texto",
      "descricao": "Designação postal (localidade) que acompanha o código postal do cliente",
      "nomesAlternativos": [
       "zipCodeLoc"
      ]
     },
     {
      "nome": "designacaoPostalSegundoTitular",
      "tipo": "texto",
      "descricao": "Designação postal que acompanha o código postal do segundo titular",
      "nomesAlternativos": [
       "zipCodeLoc2"
      ]
     },
     {
      "nome": "zona",
      "tipo": "texto",
      "descricao": "Código da zona comercial do cliente (referência a uma Zona)",
      "nomesAlternativos": [
       "zone",
       "Zona"
      ],
      "regras": [
       {
        "id": "RP-CLI-ZONA",
        "natureza": "plausibilidade",
        "restricao": {
         "propriedade": "zona",
         "operador": "LENGTH",
         "valor": [
          0,
          10
         ],
         "mensagem": "A zona do cliente tem no máximo 10 caracteres."
        },
        "descricao": "ClienteVenda.zona tem entre 0 e 10 caracteres"
       }
      ]
     },
     {
      "nome": "localCobranca",
      "tipo": "texto",
      "descricao": "Local onde é feita a cobrança ao cliente",
      "nomesAlternativos": [
       "chargeLocation",
       "Local Cobrança"
      ],
      "regras": [
       {
        "id": "RP-CLI-COBRANCA",
        "natureza": "plausibilidade",
        "restricao": {
         "propriedade": "localCobranca",
         "operador": "LENGTH",
         "valor": [
          0,
          10
         ],
         "mensagem": "O local de cobrança tem no máximo 10 caracteres."
        },
        "descricao": "ClienteVenda.localCobranca tem entre 0 e 10 caracteres"
       }
      ]
     },
     {
      "nome": "observacoes",
      "tipo": "texto",
      "descricao": "Observações livres sobre o cliente",
      "nomesAlternativos": [
       "notes"
      ]
     },
     {
      "nome": "codigoVendedor",
      "tipo": "texto",
      "descricao": "Código do vendedor responsável pelo cliente",
      "nomesAlternativos": [
       "sellerCode",
       "Codigo Vendedor"
      ]
     },
     {
      "nome": "numeroOrdem",
      "tipo": "texto",
      "descricao": "Número de ordem do cliente no percurso do vendedor",
      "nomesAlternativos": [
       "orderNumber",
       "Numero Ordem"
      ]
     },
     {
      "nome": "dataNascimento",
      "tipo": "data",
      "descricao": "Data de nascimento do cliente",
      "nomesAlternativos": [
       "dateOfBirth"
      ]
     },
     {
      "nome": "diaRecebimento",
      "tipo": "texto",
      "descricao": "Dia do mês para recebimento das prestações",
      "nomesAlternativos": [
       "receivingDay",
       "Dia Recebimento"
      ]
     },
     {
      "nome": "novo",
      "tipo": "booleano",
      "descricao": "Indica se o cliente foi criado no dispositivo e ainda não foi sincronizado",
      "nomesAlternativos": [
       "isNew"
      ]
     },
     {
      "nome": "dataRegisto",
      "tipo": "data",
      "descricao": "Data de abertura da ficha do cliente",
      "nomesAlternativos": [
       "registrationDate",
       "Data Abertura Ficha"
      ]
     }
    ],
    "regras": [
     {
      "id": "RP-CLI-NOME",
      "natureza": "plausibilidade",
      "restricao": {
       "propriedade": "Entidade.nome",
       "operador": "LENGTH",
       "valor": [
        0,
        35
       ],
       "mensagem": "O nome do cliente tem no máximo 35 caracteres."
      },
      "descricao": "ClienteVenda.Entidade.nome tem entre 0 e 35 caracteres"
     },
     {
      "id": "RP-CLI-NIF",
      "natureza": "plausibilidade",
      "restricao": {
       "propriedade": "Entidade.nif",
       "operador": "LENGTH",
       "valor": [
        0,
        15
       ],
       "mensagem": "O contribuinte do cliente tem no máximo 15 caracteres."
      },
      "descricao": "ClienteVenda.Entidade.nif tem entre 0 e 15 caracteres"
     },
     {
      "id": "RP-CLI-RUA",
      "natureza": "plausibilidade",
      "restricao": {
       "propriedade": "Morada.rua",
       "operador": "LENGTH",
       "valor": [
        0,
        35
       ],
       "mensagem": "A morada do cliente tem no máximo 35 caracteres."
      },
      "descricao": "ClienteVenda.Morada.rua tem entre 0 e 35 caracteres"
     },
     {
      "id": "RP-CLI-LOCALIDADE",
      "natureza": "plausibilidade",
      "restricao": {
       "propriedade": "Morada.localidade",
       "operador": "LENGTH",
       "valor": [
        0,
        35
       ],
       "mensagem": "A localidade do cliente tem no máximo 35 caracteres."
      },
      "descricao": "ClienteVenda.Morada.localidade tem entre 0 e 35 caracteres"
     },
     {
      "id": "RP-CLI-CP",
      "natureza": "plausibilidade",
      "restricao": {
       "propriedade": "Morada.codigoPostal",
       "operador": "LENGTH",
       "valor": [
        0,
        35
       ],
       "mensagem": "O código postal do cliente tem no máximo 35 caracteres."
      },
      "descricao": "ClienteVenda.Morada.codigoPostal tem entre 0 e 35 caracteres"
     },
     {
      "id": "RP-CLI-EMAIL",
      "natureza": "plausibilidade",
      "restricao": {
       "propriedade": "Contacto.email",
       "operador": "LENGTH",
       "valor": [
        0,
        60
       ],
       "mensagem": "O email do cliente tem no máximo 60 caracteres."
      },
      "descricao": "ClienteVenda.Contacto.email tem entre 0 e 60 caracteres"
     },
     {
      "id": "RP-CLI-TELEFONE",
      "natureza": "plausibilidade",
      "restricao": {
       "propriedade": "ContactoTelefonico.telefone",
       "operador": "LENGTH",
       "valor": [
        0,
        15
       ],
       "mensagem": "O telefone do cliente tem no máximo 15 caracteres."
      },
      "descricao": "ClienteVenda.ContactoTelefonico.telefone tem entre 0 e 15 caracteres"
     },
     {
      "id": "RP-CLI-TELEMOVEL",
      "natureza": "plausibilidade",
      "restricao": {
       "propriedade": "ContactoTelefonico.telemovel",
       "operador": "LENGTH",
       "valor": [
        0,
        15
       ],
       "mensagem": "O telemóvel do cliente tem no máximo 15 caracteres."
      },
      "descricao": "ClienteVenda.ContactoTelefonico.telemovel tem entre 0 e 15 caracteres"
     },
     {
      "id": "RP-CLI-CC",
      "natureza": "plausibilidade",
      "restricao": {
       "propriedade": "CartaoCidadao.numero",
       "operador": "LENGTH",
       "valor": [
        0,
        15
       ],
       "mensagem": "O número do cartão de cidadão do cliente tem no máximo 15 caracteres."
      },
      "descricao": "ClienteVenda.CartaoCidadao.numero tem entre 0 e 15 caracteres"
     },
     {
      "id": "RP-CLI-NOME2",
      "natureza": "plausibilidade",
      "restricao": {
       "propriedade": "SegundoTitular.nome",
       "operador": "LENGTH",
       "valor": [
        0,
        35
       ],
       "mensagem": "O nome do segundo titular tem no máximo 35 caracteres."
      },
      "descricao": "ClienteVenda.SegundoTitular.nome tem entre 0 e 35 caracteres"
     },
     {
      "id": "RP-CLI-NIF2",
      "natureza": "plausibilidade",
      "restricao": {
       "propriedade": "SegundoTitular.nif",
       "operador": "LENGTH",
       "valor": [
        0,
        15
       ],
       "mensagem": "O contribuinte do segundo titular tem no máximo 15 caracteres."
      },
      "descricao": "ClienteVenda.SegundoTitular.nif tem entre 0 e 15 caracteres"
     },
     {
      "id": "RP-CLI-RUA2",
      "natureza": "plausibilidade",
      "restricao": {
       "propriedade": "MoradaSegundoTitular.rua",
       "operador": "LENGTH",
       "valor": [
        0,
        35
       ],
       "mensagem": "A morada do segundo titular tem no máximo 35 caracteres."
      },
      "descricao": "ClienteVenda.MoradaSegundoTitular.rua tem entre 0 e 35 caracteres"
     },
     {
      "id": "RP-CLI-LOCALIDADE2",
      "natureza": "plausibilidade",
      "restricao": {
       "propriedade": "MoradaSegundoTitular.localidade",
       "operador": "LENGTH",
       "valor": [
        0,
        35
       ],
       "mensagem": "A localidade do segundo titular tem no máximo 35 caracteres."
      },
      "descricao": "ClienteVenda.MoradaSegundoTitular.localidade tem entre 0 e 35 caracteres"
     },
     {
      "id": "RP-CLI-CP2",
      "natureza": "plausibilidade",
      "restricao": {
       "propriedade": "MoradaSegundoTitular.codigoPostal",
       "operador": "LENGTH",
       "valor": [
        0,
        35
       ],
       "mensagem": "O código postal do segundo titular tem no máximo 35 caracteres."
      },
      "descricao": "ClienteVenda.MoradaSegundoTitular.codigoPostal tem entre 0 e 35 caracteres"
     },
     {
      "id": "RP-CLI-TELEFONE2",
      "natureza": "plausibilidade",
      "restricao": {
       "propriedade": "ContactoSegundoTitular.telefone",
       "operador": "LENGTH",
       "valor": [
        0,
        15
       ],
       "mensagem": "O telefone do segundo titular tem no máximo 15 caracteres."
      },
      "descricao": "ClienteVenda.ContactoSegundoTitular.telefone tem entre 0 e 15 caracteres"
     },
     {
      "id": "RP-CLI-CC2",
      "natureza": "plausibilidade",
      "restricao": {
       "propriedade": "CartaoCidadaoSegundoTitular.numero",
       "operador": "LENGTH",
       "valor": [
        0,
        15
       ],
       "mensagem": "O número do cartão de cidadão do segundo titular tem no máximo 15 caracteres."
      },
      "descricao": "ClienteVenda.CartaoCidadaoSegundoTitular.numero tem entre 0 e 15 caracteres"
     }
    ]
   },
   {
    "nome": "Vendedor",
    "descricao": "Vendedor da aplicação FM: identificação, morada, contactos, veículo, comissões, série de numeração e numerações por tipo de documento.",
    "composicao": [
     {
      "usm": "Entidade",
      "cardinalidade": "1..1"
     },
     {
      "usm": "Morada",
      "cardinalidade": "1..1"
     },
     {
      "usm": "ContactoTelefonico",
      "cardinalidade": "0..1"
     },
     {
      "usm": "Veiculo",
      "cardinalidade": "0..1"
     },
     {
      "usm": "NumeracaoDocumento",
      "cardinalidade": "0..*"
     }
    ],
    "propriedades": [
     {
      "nome": "codigo",
      "tipo": "texto",
      "descricao": "Código do vendedor",
      "nomesAlternativos": [
       "code",
       "Codigo Vendedor"
      ]
     },
     {
      "nome": "dataRegisto",
      "tipo": "data",
      "descricao": "Data de registo do vendedor na aplicação",
      "nomesAlternativos": [
       "registrationDate"
      ]
     },
     {
      "nome": "designacaoPostal",
      "tipo": "texto",
      "descricao": "Designação postal que acompanha o código postal do vendedor",
      "nomesAlternativos": [
       "zipCodeLoc"
      ]
     },
     {
      "nome": "numeroUltimoCliente",
      "tipo": "inteiro",
      "descricao": "Número do último cliente criado pelo vendedor",
      "nomesAlternativos": [
       "Nº Ultimo Cliente"
      ]
     },
     {
      "nome": "serie",
      "tipo": "texto",
      "descricao": "Série de numeração dos documentos do vendedor",
      "nomesAlternativos": [
       "seriesNumber",
       "Serie Numerações"
      ],
      "regras": [
       {
        "id": "RP-VEND-SERIE",
        "natureza": "plausibilidade",
        "restricao": {
         "propriedade": "serie",
         "operador": "LENGTH",
         "valor": [
          0,
          3
         ],
         "mensagem": "A série de numeração tem no máximo 3 caracteres."
        },
        "descricao": "Vendedor.serie tem entre 0 e 3 caracteres"
       }
      ]
     },
     {
      "nome": "dataInicioSerie",
      "tipo": "data",
      "descricao": "Data de início da série de numeração",
      "nomesAlternativos": [
       "seriesNumberStartingDate",
       "Data Inicio Serie"
      ]
     },
     {
      "nome": "numeroDigitosSerie",
      "tipo": "texto",
      "descricao": "Número de dígitos da numeração na série",
      "nomesAlternativos": [
       "Numero Digitos Serie"
      ],
      "regras": [
       {
        "id": "RP-VEND-DIGITOS",
        "natureza": "plausibilidade",
        "restricao": {
         "propriedade": "numeroDigitosSerie",
         "operador": "LENGTH",
         "valor": [
          0,
          4
         ],
         "mensagem": "O número de dígitos da série tem no máximo 4 caracteres."
        },
        "descricao": "Vendedor.numeroDigitosSerie tem entre 0 e 4 caracteres"
       }
      ]
     },
     {
      "nome": "prefixoAtcud",
      "tipo": "texto",
      "descricao": "Prefixo ATCUD geral da série do vendedor",
      "nomesAlternativos": [
       "Prefixo ATCUD"
      ],
      "regras": [
       {
        "id": "RP-VEND-ATCUD",
        "natureza": "plausibilidade",
        "restricao": {
         "propriedade": "prefixoAtcud",
         "operador": "LENGTH",
         "valor": [
          0,
          15
         ],
         "mensagem": "O prefixo ATCUD tem no máximo 15 caracteres."
        },
        "descricao": "Vendedor.prefixoAtcud tem entre 0 e 15 caracteres"
       }
      ]
     },
     {
      "nome": "comissaoVendaPronto",
      "tipo": "decimal",
      "descricao": "Comissão do vendedor nas vendas a pronto (%)",
      "nomesAlternativos": [
       "commissionOfSaleOfProduct",
       "Comissao Venda Pronto"
      ]
     },
     {
      "nome": "comissaoVendaPrestacao",
      "tipo": "decimal",
      "descricao": "Comissão do vendedor nas vendas a prestações (%)",
      "nomesAlternativos": [
       "commissionOfSaleOfInstallment",
       "Comissao Venda Prestacao"
      ]
     },
     {
      "nome": "comissaoCobranca",
      "tipo": "decimal",
      "descricao": "Comissão do vendedor sobre as cobranças (%)",
      "nomesAlternativos": [
       "commissionOfCharge",
       "Comissao Cobranca"
      ]
     },
     {
      "nome": "numeroGuiaTransporte",
      "tipo": "inteiro",
      "descricao": "Número da última guia de transporte",
      "nomesAlternativos": [
       "transportGuideNumber"
      ]
     },
     {
      "nome": "numeroGuiaTransporteExtra",
      "tipo": "inteiro",
      "descricao": "Número da última guia de transporte extra",
      "nomesAlternativos": [
       "transportGuideExtraNumber"
      ]
     },
     {
      "nome": "codigoFamiliaExtra",
      "tipo": "texto",
      "descricao": "Código da família de artigos extra",
      "nomesAlternativos": [
       "familyCodeExtra"
      ],
      "regras": [
       {
        "id": "RP-VEND-FAMEXTRA",
        "natureza": "plausibilidade",
        "restricao": {
         "propriedade": "codigoFamiliaExtra",
         "operador": "LENGTH",
         "valor": [
          0,
          7
         ],
         "mensagem": "O código da família extra tem no máximo 7 caracteres."
        },
        "descricao": "Vendedor.codigoFamiliaExtra tem entre 0 e 7 caracteres"
       }
      ]
     },
     {
      "nome": "trataRecebimentos",
      "tipo": "booleano",
      "descricao": "Indica se o vendedor pode processar recebimentos",
      "nomesAlternativos": [
       "processReceiptsPermissions",
       "Trata Recebimentos"
      ]
     },
     {
      "nome": "nifEmissor",
      "tipo": "texto",
      "descricao": "Contribuinte da entidade emissora dos documentos",
      "nomesAlternativos": [
       "senderNif",
       "Contribuinte do Emissor"
      ],
      "regras": [
       {
        "id": "RP-VEND-NIFEMISSOR",
        "natureza": "plausibilidade",
        "restricao": {
         "propriedade": "nifEmissor",
         "operador": "LENGTH",
         "valor": [
          0,
          15
         ],
         "mensagem": "O contribuinte do emissor tem no máximo 15 caracteres."
        },
        "descricao": "Vendedor.nifEmissor tem entre 0 e 15 caracteres"
       }
      ]
     }
    ],
    "regras": [
     {
      "id": "RP-VEND-NOME",
      "natureza": "plausibilidade",
      "restricao": {
       "propriedade": "Entidade.nome",
       "operador": "LENGTH",
       "valor": [
        0,
        35
       ],
       "mensagem": "O nome do vendedor tem no máximo 35 caracteres."
      },
      "descricao": "Vendedor.Entidade.nome tem entre 0 e 35 caracteres"
     },
     {
      "id": "RP-VEND-NIF",
      "natureza": "plausibilidade",
      "restricao": {
       "propriedade": "Entidade.nif",
       "operador": "LENGTH",
       "valor": [
        0,
        15
       ],
       "mensagem": "O NIF do vendedor tem no máximo 15 caracteres."
      },
      "descricao": "Vendedor.Entidade.nif tem entre 0 e 15 caracteres"
     },
     {
      "id": "RP-VEND-RUA",
      "natureza": "plausibilidade",
      "restricao": {
       "propriedade": "Morada.rua",
       "operador": "LENGTH",
       "valor": [
        0,
        35
       ],
       "mensagem": "A morada do vendedor tem no máximo 35 caracteres."
      },
      "descricao": "Vendedor.Morada.rua tem entre 0 e 35 caracteres"
     },
     {
      "id": "RP-VEND-LOCALIDADE",
      "natureza": "plausibilidade",
      "restricao": {
       "propriedade": "Morada.localidade",
       "operador": "LENGTH",
       "valor": [
        0,
        35
       ],
       "mensagem": "A localidade do vendedor tem no máximo 35 caracteres."
      },
      "descricao": "Vendedor.Morada.localidade tem entre 0 e 35 caracteres"
     },
     {
      "id": "RP-VEND-CP",
      "natureza": "plausibilidade",
      "restricao": {
       "propriedade": "Morada.codigoPostal",
       "operador": "LENGTH",
       "valor": [
        0,
        35
       ],
       "mensagem": "O código postal do vendedor tem no máximo 35 caracteres."
      },
      "descricao": "Vendedor.Morada.codigoPostal tem entre 0 e 35 caracteres"
     },
     {
      "id": "RP-VEND-TELEFONE",
      "natureza": "plausibilidade",
      "restricao": {
       "propriedade": "ContactoTelefonico.telefone",
       "operador": "LENGTH",
       "valor": [
        0,
        15
       ],
       "mensagem": "O telefone do vendedor tem no máximo 15 caracteres."
      },
      "descricao": "Vendedor.ContactoTelefonico.telefone tem entre 0 e 15 caracteres"
     },
     {
      "id": "RP-VEND-TELEMOVEL",
      "natureza": "plausibilidade",
      "restricao": {
       "propriedade": "ContactoTelefonico.telemovel",
       "operador": "LENGTH",
       "valor": [
        0,
        15
       ],
       "mensagem": "O telemóvel do vendedor tem no máximo 15 caracteres."
      },
      "descricao": "Vendedor.ContactoTelefonico.telemovel tem entre 0 e 15 caracteres"
     }
    ]
   },
   {
    "nome": "CabecalhoExportacao",
    "descricao": "Informação do ficheiro de exportação: nome, tamanho, data de modificação e contagens de registos.",
    "propriedades": [
     {
      "nome": "nomeFicheiro",
      "tipo": "texto",
      "descricao": "Nome do ficheiro de exportação",
      "nomesAlternativos": [
       "name"
      ]
     },
     {
      "nome": "tamanhoFicheiro",
      "tipo": "decimal",
      "descricao": "Tamanho do ficheiro",
      "nomesAlternativos": [
       "size"
      ]
     },
     {
      "nome": "dataModificacao",
      "tipo": "texto",
      "descricao": "Data e hora da última modificação do ficheiro, tal como registada",
      "nomesAlternativos": [
       "lastModified"
      ]
     },
     {
      "nome": "numeroClientes",
      "tipo": "inteiro",
      "descricao": "Número de registos de clientes",
      "nomesAlternativos": [
       "nCli"
      ]
     },
     {
      "nome": "numeroArtigos",
      "tipo": "inteiro",
      "descricao": "Número de registos de artigos",
      "nomesAlternativos": [
       "nArt"
      ]
     },
     {
      "nome": "numeroEntregas",
      "tipo": "inteiro",
      "descricao": "Número de entregas",
      "nomesAlternativos": [
       "nDlv"
      ]
     },
     {
      "nome": "numeroLinhasEntrega",
      "tipo": "inteiro",
      "descricao": "Número de linhas de entrega",
      "nomesAlternativos": [
       "nItem"
      ]
     },
     {
      "nome": "numeroArtigosVeiculo",
      "tipo": "inteiro",
      "descricao": "Número de registos de produtos no veículo",
      "nomesAlternativos": [
       "nArtVeic"
      ]
     },
     {
      "nome": "numeroZonas",
      "tipo": "inteiro",
      "descricao": "Número de registos de zonas",
      "nomesAlternativos": [
       "nZone"
      ]
     }
    ]
   },
   {
    "nome": "SaldoCliente",
    "descricao": "Conta corrente de um cliente: saldo, total de vendas e saldo inicial.",
    "propriedades": [
     {
      "nome": "codigoCliente",
      "tipo": "texto",
      "descricao": "Código do cliente a que o saldo respeita",
      "nomesAlternativos": [
       "Codigo Cliente"
      ]
     },
     {
      "nome": "saldo",
      "tipo": "decimal",
      "descricao": "Saldo atual do cliente",
      "nomesAlternativos": [
       "Saldo"
      ]
     },
     {
      "nome": "totalVendas",
      "tipo": "decimal",
      "descricao": "Valor total das vendas ao cliente",
      "nomesAlternativos": [
       "Valor Total Vendas"
      ]
     },
     {
      "nome": "saldoInicial",
      "tipo": "decimal",
      "descricao": "Valor do saldo inicial",
      "nomesAlternativos": [
       "Valor Saldo Inicial"
      ]
     },
     {
      "nome": "pagoSaldoInicial",
      "tipo": "decimal",
      "descricao": "Valor já pago do saldo inicial",
      "nomesAlternativos": [
       "Valor Pago Saldo Inicial"
      ]
     },
     {
      "nome": "dataSaldoInicial",
      "tipo": "data",
      "descricao": "Data do saldo inicial",
      "nomesAlternativos": [
       "Data Saldo Inicial"
      ]
     }
    ]
   },
   {
    "nome": "ArtigoStock",
    "descricao": "Ficha de artigo em stock: artigo, preços de venda e de custo, IVA, descontos, quantidades, família e fornecedor.",
    "composicao": [
     {
      "usm": "Artigo",
      "cardinalidade": "1..1"
     }
    ],
    "propriedades": [
     {
      "nome": "codigoAuxiliar",
      "tipo": "texto",
      "descricao": "Código auxiliar do artigo",
      "nomesAlternativos": [
       "articleCode",
       "Codigo Axiliar"
      ],
      "regras": [
       {
        "id": "RP-STK-AUXILIAR",
        "natureza": "plausibilidade",
        "restricao": {
         "propriedade": "codigoAuxiliar",
         "operador": "LENGTH",
         "valor": [
          0,
          13
         ],
         "mensagem": "O código auxiliar tem no máximo 13 caracteres."
        },
        "descricao": "ArtigoStock.codigoAuxiliar tem entre 0 e 13 caracteres"
       }
      ]
     },
     {
      "nome": "referencia",
      "tipo": "texto",
      "descricao": "Referência do artigo",
      "nomesAlternativos": [
       "reference",
       "Referencia"
      ],
      "regras": [
       {
        "id": "RP-STK-REFERENCIA",
        "natureza": "plausibilidade",
        "restricao": {
         "propriedade": "referencia",
         "operador": "LENGTH",
         "valor": [
          0,
          20
         ],
         "mensagem": "A referência do artigo tem no máximo 20 caracteres."
        },
        "descricao": "ArtigoStock.referencia tem entre 0 e 20 caracteres"
       }
      ]
     },
     {
      "nome": "unidadeMedida",
      "tipo": "texto",
      "descricao": "Unidade de medida do artigo",
      "nomesAlternativos": [
       "unit",
       "Unidade Medida"
      ],
      "regras": [
       {
        "id": "RP-STK-UNIDADE",
        "natureza": "plausibilidade",
        "restricao": {
         "propriedade": "unidadeMedida",
         "operador": "LENGTH",
         "valor": [
          0,
          6
         ],
         "mensagem": "A unidade de medida tem no máximo 6 caracteres."
        },
        "descricao": "ArtigoStock.unidadeMedida tem entre 0 e 6 caracteres"
       }
      ]
     },
     {
      "nome": "dataRegisto",
      "tipo": "data",
      "descricao": "Data de criação da ficha do artigo",
      "nomesAlternativos": [
       "registrationDate",
       "Data Criação ficha"
      ]
     },
     {
      "nome": "formaArtigo",
      "tipo": "texto",
      "descricao": "Forma de apresentação do artigo",
      "nomesAlternativos": [
       "artForm"
      ]
     },
     {
      "nome": "precoVendaComIva",
      "tipo": "decimal",
      "descricao": "Preço de venda 1 com IVA",
      "nomesAlternativos": [
       "salePrice",
       "Preço Venda com Iva"
      ]
     },
     {
      "nome": "precoVendaSemIva",
      "tipo": "decimal",
      "descricao": "Preço de venda 1 sem IVA",
      "nomesAlternativos": [
       "Preço Venda 1 sem Iva"
      ]
     },
     {
      "nome": "precoVenda2ComIva",
      "tipo": "decimal",
      "descricao": "Preço de venda 2 com IVA",
      "nomesAlternativos": [
       "Preço Venda 2 com IVA"
      ]
     },
     {
      "nome": "precoVenda2SemIva",
      "tipo": "decimal",
      "descricao": "Preço de venda 2 sem IVA",
      "nomesAlternativos": [
       "Preço Venda 2 sem IVA"
      ]
     },
     {
      "nome": "precoPublico",
      "tipo": "decimal",
      "descricao": "Preço de venda ao público",
      "nomesAlternativos": [
       "ppPrice"
      ]
     },
     {
      "nome": "desconto1",
      "tipo": "decimal",
      "descricao": "Percentagem do primeiro desconto",
      "nomesAlternativos": [
       "% Desconto1"
      ]
     },
     {
      "nome": "desconto2",
      "tipo": "decimal",
      "descricao": "Percentagem do segundo desconto",
      "nomesAlternativos": [
       "discount2",
       "% Desconto2"
      ]
     },
     {
      "nome": "taxaIva",
      "tipo": "decimal",
      "descricao": "Taxa de IVA de venda (%)",
      "nomesAlternativos": [
       "saleIva",
       "Taxa de Iva"
      ]
     },
     {
      "nome": "ecoTaxa",
      "tipo": "decimal",
      "descricao": "Valor da ecotaxa do artigo",
      "nomesAlternativos": [
       "ecoTaxa"
      ]
     },
     {
      "nome": "precoCusto",
      "tipo": "decimal",
      "descricao": "Preço de custo",
      "nomesAlternativos": [
       "costPrice"
      ]
     },
     {
      "nome": "descontoCusto",
      "tipo": "decimal",
      "descricao": "Desconto sobre o preço de custo",
      "nomesAlternativos": [
       "costDiscount"
      ]
     },
     {
      "nome": "precoCustoSemIva",
      "tipo": "decimal",
      "descricao": "Preço de custo sem IVA",
      "nomesAlternativos": [
       "costPriceNoIva",
       "Preço Custo sem Iva"
      ]
     },
     {
      "nome": "precoCustoComIva",
      "tipo": "decimal",
      "descricao": "Preço de custo com IVA",
      "nomesAlternativos": [
       "costPriceWithIva",
       "Preço Custo com Iva"
      ]
     },
     {
      "nome": "precoCusto2SemIva",
      "tipo": "decimal",
      "descricao": "Segundo preço de custo sem IVA",
      "nomesAlternativos": [
       "costPriceNoIva2"
      ]
     },
     {
      "nome": "precoCusto2ComIva",
      "tipo": "decimal",
      "descricao": "Segundo preço de custo com IVA",
      "nomesAlternativos": [
       "costPriceWithIva2"
      ]
     },
     {
      "nome": "quantidadeStock",
      "tipo": "decimal",
      "descricao": "Quantidade em stock",
      "nomesAlternativos": [
       "stockQuantity",
       "Quantidade em stock"
      ]
     },
     {
      "nome": "quantidadeStockFora",
      "tipo": "decimal",
      "descricao": "Quantidade em stock fora do armazém",
      "nomesAlternativos": [
       "stockOutQuantity",
       "Quantidade em stock Out"
      ]
     },
     {
      "nome": "peso",
      "tipo": "decimal",
      "descricao": "Peso do artigo",
      "nomesAlternativos": [
       "weight",
       "Peso"
      ]
     },
     {
      "nome": "codigoFamilia",
      "tipo": "texto",
      "descricao": "Código da família do artigo",
      "nomesAlternativos": [
       "familyCode",
       "Codigo Familia"
      ],
      "regras": [
       {
        "id": "RP-STK-FAMILIA",
        "natureza": "plausibilidade",
        "restricao": {
         "propriedade": "codigoFamilia",
         "operador": "LENGTH",
         "valor": [
          0,
          7
         ],
         "mensagem": "O código da família tem no máximo 7 caracteres."
        },
        "descricao": "ArtigoStock.codigoFamilia tem entre 0 e 7 caracteres"
       }
      ]
     },
     {
      "nome": "descricaoFamilia",
      "tipo": "texto",
      "descricao": "Descrição da família do artigo",
      "nomesAlternativos": [
       "familyDescription",
       "Descricção Familia"
      ],
      "regras": [
       {
        "id": "RP-STK-DESCFAMILIA",
        "natureza": "plausibilidade",
        "restricao": {
         "propriedade": "descricaoFamilia",
         "operador": "LENGTH",
         "valor": [
          0,
          35
         ],
         "mensagem": "A descrição da família tem no máximo 35 caracteres."
        },
        "descricao": "ArtigoStock.descricaoFamilia tem entre 0 e 35 caracteres"
       }
      ]
     },
     {
      "nome": "codigoFornecedor",
      "tipo": "texto",
      "descricao": "Código do fornecedor do artigo",
      "nomesAlternativos": [
       "supplierCode",
       "Codigo Fornecedor"
      ]
     },
     {
      "nome": "nomeFornecedor",
      "tipo": "texto",
      "descricao": "Nome do fornecedor do artigo",
      "nomesAlternativos": [
       "supplier",
       "Nome Fornecedor"
      ],
      "regras": [
       {
        "id": "RP-STK-FORNECEDOR",
        "natureza": "plausibilidade",
        "restricao": {
         "propriedade": "nomeFornecedor",
         "operador": "LENGTH",
         "valor": [
          0,
          35
         ],
         "mensagem": "O nome do fornecedor tem no máximo 35 caracteres."
        },
        "descricao": "ArtigoStock.nomeFornecedor tem entre 0 e 35 caracteres"
       }
      ]
     },
     {
      "nome": "servico",
      "tipo": "booleano",
      "descricao": "Indica se o artigo é um serviço",
      "nomesAlternativos": [
       "service",
       "Serviço"
      ]
     },
     {
      "nome": "exportaObservacoes",
      "tipo": "booleano",
      "descricao": "Indica se as observações do artigo são exportadas",
      "nomesAlternativos": [
       "Exporta OBS"
      ]
     },
     {
      "nome": "observacoes",
      "tipo": "texto",
      "descricao": "Observações sobre o artigo",
      "nomesAlternativos": [
       "observations"
      ]
     },
     {
      "nome": "emVeiculo",
      "tipo": "booleano",
      "descricao": "Indica se o artigo é transportado no veículo do vendedor",
      "nomesAlternativos": [
       "isCar"
      ]
     },
     {
      "nome": "matriculaVeiculo",
      "tipo": "texto",
      "descricao": "Matrícula do veículo onde o artigo está",
      "nomesAlternativos": [
       "carRegistration"
      ]
     }
    ],
    "regras": [
     {
      "id": "RP-STK-CODIGO",
      "natureza": "plausibilidade",
      "restricao": {
       "propriedade": "Artigo.codigo",
       "operador": "LENGTH",
       "valor": [
        0,
        6
       ],
       "mensagem": "O código do artigo no registo de stock tem no máximo 6 caracteres."
      },
      "descricao": "ArtigoStock.Artigo.codigo tem entre 0 e 6 caracteres"
     },
     {
      "id": "RP-STK-EAN",
      "natureza": "plausibilidade",
      "restricao": {
       "propriedade": "Artigo.codigoBarras",
       "operador": "LENGTH",
       "valor": [
        0,
        15
       ],
       "mensagem": "O código EAN no registo de stock tem no máximo 15 caracteres."
      },
      "descricao": "ArtigoStock.Artigo.codigoBarras tem entre 0 e 15 caracteres"
     },
     {
      "id": "RP-STK-DESCRICAO",
      "natureza": "plausibilidade",
      "restricao": {
       "propriedade": "Artigo.nome",
       "operador": "LENGTH",
       "valor": [
        0,
        50
       ],
       "mensagem": "A descrição do artigo no registo de stock tem no máximo 50 caracteres."
      },
      "descricao": "ArtigoStock.Artigo.nome tem entre 0 e 50 caracteres"
     }
    ]
   },
   {
    "nome": "ProdutoVeiculo",
    "descricao": "Quantidades de um artigo transportadas no veículo de um vendedor.",
    "propriedades": [
     {
      "nome": "matricula",
      "tipo": "texto",
      "descricao": "Matrícula do veículo",
      "nomesAlternativos": [
       "Matricula"
      ],
      "regras": [
       {
        "id": "RP-PRV-MATRICULA",
        "natureza": "plausibilidade",
        "restricao": {
         "propriedade": "matricula",
         "operador": "LENGTH",
         "valor": [
          0,
          15
         ],
         "mensagem": "A matrícula tem no máximo 15 caracteres."
        },
        "descricao": "ProdutoVeiculo.matricula tem entre 0 e 15 caracteres"
       }
      ]
     },
     {
      "nome": "codigoArtigo",
      "tipo": "texto",
      "descricao": "Código do artigo no veículo",
      "nomesAlternativos": [
       "Codigo Artigo"
      ],
      "regras": [
       {
        "id": "RP-PRV-ARTIGO",
        "natureza": "plausibilidade",
        "restricao": {
         "propriedade": "codigoArtigo",
         "operador": "LENGTH",
         "valor": [
          0,
          7
         ],
         "mensagem": "O código do artigo no veículo tem no máximo 7 caracteres."
        },
        "descricao": "ProdutoVeiculo.codigoArtigo tem entre 0 e 7 caracteres"
       }
      ]
     },
     {
      "nome": "quantidadeTotal",
      "tipo": "decimal",
      "descricao": "Quantidade total do artigo no veículo",
      "nomesAlternativos": [
       "carQuantityTotal",
       "Quantidade Total"
      ]
     },
     {
      "nome": "quantidadeNormal",
      "tipo": "decimal",
      "descricao": "Quantidade normal do artigo no veículo",
      "nomesAlternativos": [
       "carQuantityNormal",
       "Quantidade Normal"
      ]
     },
     {
      "nome": "quantidadeFora",
      "tipo": "decimal",
      "descricao": "Quantidade do artigo fora do veículo",
      "nomesAlternativos": [
       "carQuantityOut",
       "Quantidade Fora"
      ]
     }
    ]
   },
   {
    "nome": "Zona",
    "descricao": "Zona comercial a que os clientes são atribuídos.",
    "propriedades": [
     {
      "nome": "codigo",
      "tipo": "texto",
      "descricao": "Código da zona",
      "nomesAlternativos": [
       "code"
      ]
     },
     {
      "nome": "nome",
      "tipo": "texto",
      "descricao": "Nome da zona",
      "nomesAlternativos": [
       "name"
      ]
     }
    ]
   },
   {
    "nome": "Auxiliar",
    "descricao": "Registo auxiliar de texto da exportação, identificado por um número.",
    "propriedades": [
     {
      "nome": "identificador",
      "tipo": "inteiro",
      "descricao": "Identificador do texto auxiliar",
      "nomesAlternativos": [
       "ID"
      ]
     },
     {
      "nome": "texto",
      "tipo": "texto",
      "descricao": "Texto auxiliar",
      "nomesAlternativos": [
       "Texto"
      ],
      "regras": [
       {
        "id": "RP-AUX-TEXTO",
        "natureza": "plausibilidade",
        "restricao": {
         "propriedade": "texto",
         "operador": "LENGTH",
         "valor": [
          0,
          40
         ],
         "mensagem": "O texto auxiliar tem no máximo 40 caracteres."
        },
        "descricao": "Auxiliar.texto tem entre 0 e 40 caracteres"
       }
      ]
     }
    ]
   },
   {
    "nome": "Configuracao",
    "descricao": "Parâmetros de configuração da empresa, da aplicação e do vendedor.",
    "composicao": [
     {
      "usm": "ParametroConfiguracao",
      "papel": "ParametroEmpresa",
      "cardinalidade": "0..*"
     },
     {
      "usm": "ParametroConfiguracao",
      "papel": "ParametroAplicacao",
      "cardinalidade": "0..*"
     },
     {
      "usm": "ParametroConfiguracao",
      "papel": "ParametroVendedor",
      "cardinalidade": "0..*"
     }
    ]
   }
  ],
  "hlm": [
   {
    "nome": "ExportacaoFm",
    "descricao": "Exportação dos registos da aplicação FM de um vendedor: vendedor e numerações, clientes, saldos, stocks, produtos no veículo, zonas, textos auxiliares e configuração.",
    "composicao": [
     {
      "sm": "CabecalhoExportacao",
      "cardinalidade": "0..1"
     },
     {
      "sm": "Vendedor",
      "cardinalidade": "1..1"
     },
     {
      "sm": "ClienteVenda",
      "cardinalidade": "0..*"
     },
     {
      "sm": "SaldoCliente",
      "cardinalidade": "0..*"
     },
     {
      "sm": "ArtigoStock",
      "cardinalidade": "0..*"
     },
     {
      "sm": "ProdutoVeiculo",
      "cardinalidade": "0..*"
     },
     {
      "sm": "Zona",
      "cardinalidade": "0..*"
     },
     {
      "sm": "Auxiliar",
      "cardinalidade": "0..*"
     },
     {
      "sm": "Configuracao",
      "cardinalidade": "0..1"
     },
     {
      "sm": "Metainformacao",
      "papel": "Metainformacao",
      "cardinalidade": "0..1"
     }
    ]
   }
  ],
  "projecoes": [
   {
    "nome": "ExportacaoDiariaFm",
    "hlm": "ExportacaoFm",
    "descricao": "Exportação diária dos registos de um vendedor (VDM, CLI, YCL, STK, AUX, PRV).",
    "obrigatorias": [
     "Vendedor.codigo",
     "Vendedor.Entidade.nome",
     "Vendedor.Entidade.nif",
     "Vendedor.serie",
     "Vendedor.dataInicioSerie",
     "Vendedor.prefixoAtcud"
    ],
    "permitidas": [
     "CabecalhoExportacao.*",
     "Vendedor.Morada.*",
     "Vendedor.ContactoTelefonico.*",
     "Vendedor.Veiculo.*",
     "Vendedor.NumeracaoDocumento.*",
     "Vendedor.dataRegisto",
     "Vendedor.designacaoPostal",
     "Vendedor.numeroUltimoCliente",
     "Vendedor.numeroDigitosSerie",
     "Vendedor.comissaoVendaPronto",
     "Vendedor.comissaoVendaPrestacao",
     "Vendedor.comissaoCobranca",
     "Vendedor.numeroGuiaTransporte",
     "Vendedor.numeroGuiaTransporteExtra",
     "Vendedor.codigoFamiliaExtra",
     "Vendedor.trataRecebimentos",
     "Vendedor.nifEmissor",
     "ClienteVenda.*",
     "SaldoCliente.*",
     "ArtigoStock.*",
     "ProdutoVeiculo.*",
     "Zona.*",
     "Auxiliar.*",
     "Configuracao.*",
     "Metainformacao.*"
    ]
   }
  ],
  "perfis": [
   {
    "nome": "ExportacaoDiariaVendedor",
    "projecao": "ExportacaoDiariaFm",
    "descricao": "Exportação diária de um vendedor em Portugal, com a série e o prefixo ATCUD conhecidos (os valores concretos vêm da instância).",
    "fixa": [
     {
      "propriedade": "Vendedor.Morada.pais",
      "valor": "PT"
     }
    ]
   }
  ]
 },
 {
  "$schema": "../../../specs/declaracao/ecv.schema.json",
  "declaracao": {
   "nome": "mensagem_estado",
   "versao": "0.1.0",
   "descricao": "Mensagem de estado CIUS-PT: resposta do adquirente sobre um documento de faturação recebido.",
   "dominios": [
    "faturação"
   ],
   "hlm": "MensagemEstado"
  },
  "usm": [
   {
    "nome": "SujeitoPassivo",
    "descricao": "Pessoa singular ou coletiva identificada para efeitos fiscais, com o identificador de IVA precedido do código do país.",
    "propriedades": [
     {
      "nome": "nome",
      "tipo": "texto",
      "descricao": "Nome formal completo ou denominação social registada",
      "nomesAlternativos": [
       "RegistrationName",
       "Seller name",
       "Buyer name",
       "Payee name"
      ],
      "regras": [
       {
        "id": "RP-SP-NOME",
        "natureza": "plausibilidade",
        "restricao": {
         "propriedade": "nome",
         "operador": "LENGTH",
         "valor": [
          1,
          200
         ],
         "mensagem": "O nome tem de ter entre 1 e 200 caracteres."
        },
        "descricao": "SujeitoPassivo.nome tem entre 1 e 200 caracteres"
       }
      ]
     },
     {
      "nome": "nomeComercial",
      "tipo": "texto",
      "descricao": "Nome comercial pelo qual a parte é conhecida",
      "nomesAlternativos": [
       "PartyName",
       "trading name"
      ],
      "regras": [
       {
        "id": "RP-SP-NOMECOM",
        "natureza": "plausibilidade",
        "restricao": {
         "propriedade": "nomeComercial",
         "operador": "LENGTH",
         "valor": [
          1,
          200
         ],
         "mensagem": "O nome comercial tem de ter entre 1 e 200 caracteres."
        },
        "descricao": "SujeitoPassivo.nomeComercial tem entre 1 e 200 caracteres"
       }
      ]
     },
     {
      "nome": "identificador",
      "tipo": "texto",
      "descricao": "Identificador da parte segundo um esquema de identificação (ex.: GLN, identificação bancária)",
      "nomesAlternativos": [
       "PartyIdentification"
      ],
      "regras": [
       {
        "id": "RP-SP-IDENT",
        "natureza": "plausibilidade",
        "restricao": {
         "propriedade": "identificador",
         "operador": "LENGTH",
         "valor": [
          1,
          50
         ],
         "mensagem": "O identificador da parte tem de ter entre 1 e 50 caracteres."
        },
        "descricao": "SujeitoPassivo.identificador tem entre 1 e 50 caracteres"
       }
      ]
     },
     {
      "nome": "identificadorRegisto",
      "tipo": "texto",
      "descricao": "Identificador do registo comercial (conservatória) da parte",
      "nomesAlternativos": [
       "legal registration identifier"
      ],
      "regras": [
       {
        "id": "RP-SP-REGISTO",
        "natureza": "plausibilidade",
        "restricao": {
         "propriedade": "identificadorRegisto",
         "operador": "LENGTH",
         "valor": [
          1,
          200
         ],
         "mensagem": "O identificador de registo tem de ter entre 1 e 200 caracteres."
        },
        "descricao": "SujeitoPassivo.identificadorRegisto tem entre 1 e 200 caracteres"
       }
      ]
     },
     {
      "nome": "identificadorIva",
      "tipo": "texto",
      "descricao": "Número de identificação fiscal para efeitos de IVA, precedido do código ISO 3166-1 alfa-2 do país",
      "nomesAlternativos": [
       "VAT identifier",
       "PartyTaxScheme"
      ],
      "regras": [
       {
        "id": "RP-SP-IVA",
        "natureza": "plausibilidade",
        "restricao": {
         "propriedade": "identificadorIva",
         "operador": "PATTERN",
         "valor": "^[A-Z]{2}.{1,48}$",
         "mensagem": "O identificador de IVA tem de começar pelo código do país (duas letras) e ter no máximo 50 caracteres."
        },
        "descricao": "SujeitoPassivo.identificadorIva segue o padrão ^[A-Z]{2}.{1,48}$"
       }
      ]
     }
    ]
   },
   {
    "nome": "Morada",
    "descricao": "Morada postal: arruamento, código postal, localidade, freguesia e país.",
    "propriedades": [
     {
      "nome": "rua",
      "tipo": "texto",
      "descricao": "Arruamento e número de porta"
     },
     {
      "nome": "codigoPostal",
      "tipo": "texto",
      "descricao": "Código postal da morada",
      "nomesAlternativos": [
       "zipCode",
       "postalCode",
       "CP"
      ],
      "regras": [
       {
        "id": "RP-CP",
        "natureza": "plausibilidade",
        "descricao": "Morada.codigoPostal segue o padrão ^([1-9][0-9]{3}-[0-9]{3}|[0-5][0-9]{4}|[A-Z]{1,2}[0-9][0-9A-Z]? [0-9][A-Z]{2})$",
        "restricao": {
         "propriedade": "codigoPostal",
         "operador": "PATTERN",
         "valor": "^([1-9][0-9]{3}-[0-9]{3}|[0-5][0-9]{4}|[A-Z]{1,2}[0-9][0-9A-Z]? [0-9][A-Z]{2})$",
         "mensagem": "O código postal não tem nenhum dos formatos possíveis (português, espanhol ou britânico)."
        },
        "notas": "Plausibilidade: os formatos possíveis {PT, ES, GB}. Qual se aplica decide-se por inferência (RIR-CP-PT/ES/GB)."
       }
      ]
     },
     {
      "nome": "localidade",
      "tipo": "texto",
      "descricao": "Localidade da morada (em maiúsculas, sem acentos)"
     },
     {
      "nome": "freguesia",
      "tipo": "texto",
      "descricao": "Freguesia da morada (só para moradas em Lisboa)",
      "regras": [
       {
        "id": "RP-FREGUESIA",
        "natureza": "plausibilidade",
        "descricao": "Morada.freguesia ∈ {AJUDA, ALCANTARA, ALVALADE, AREEIRO, ARROIOS, AVENIDAS_NOVAS, BEATO, BELEM, BENFICA, CAMPO_DE_OURIQUE, CAMPOLIDE, CARNIDE, ESTRELA, LUMIAR, MARVILA, MISERICORDIA, OLIVAIS, PARQUE_DAS_NACOES, PENHA_DE_FRANCA, SANTA_CLARA, SANTA_MARIA_MAIOR, SANTO_ANTONIO, SAO_DOMINGOS_DE_BENFICA, SAO_VICENTE}",
        "restricao": {
         "propriedade": "freguesia",
         "operador": "IN",
         "valor": [
          "AJUDA",
          "ALCANTARA",
          "ALVALADE",
          "AREEIRO",
          "ARROIOS",
          "AVENIDAS_NOVAS",
          "BEATO",
          "BELEM",
          "BENFICA",
          "CAMPO_DE_OURIQUE",
          "CAMPOLIDE",
          "CARNIDE",
          "ESTRELA",
          "LUMIAR",
          "MARVILA",
          "MISERICORDIA",
          "OLIVAIS",
          "PARQUE_DAS_NACOES",
          "PENHA_DE_FRANCA",
          "SANTA_CLARA",
          "SANTA_MARIA_MAIOR",
          "SANTO_ANTONIO",
          "SAO_DOMINGOS_DE_BENFICA",
          "SAO_VICENTE"
         ],
         "mensagem": "A freguesia não pertence às freguesias de Lisboa conhecidas."
        }
       }
      ]
     },
     {
      "nome": "pais",
      "tipo": "texto",
      "descricao": "País da morada (código ISO de duas letras)",
      "nomesAlternativos": [
       "country",
       "countryCode"
      ],
      "regras": [
       {
        "id": "RP-PAIS",
        "natureza": "plausibilidade",
        "descricao": "Morada.pais ∈ {PT, ES, GB}",
        "restricao": {
         "propriedade": "pais",
         "operador": "IN",
         "valor": [
          "PT",
          "ES",
          "GB"
         ],
         "mensagem": "O país tem de ser PT, ES ou GB."
        }
       }
      ]
     }
    ],
    "regras": [
     {
      "id": "RIR-CP-PT",
      "natureza": "inferencia_restritiva",
      "descricao": "Se Morada.pais = PT → Morada.codigoPostal segue o padrão ^[1-9][0-9]{3}-[0-9]{3}$",
      "condicao": [
       {
        "propriedade": "pais",
        "operador": "EQUALS",
        "valor": "PT"
       }
      ],
      "restricao": {
       "propriedade": "codigoPostal",
       "operador": "PATTERN",
       "valor": "^[1-9][0-9]{3}-[0-9]{3}$",
       "mensagem": "O código postal português tem de ter o formato 0000-000, sem começar por zero."
      }
     },
     {
      "id": "RIR-CP-ES",
      "natureza": "inferencia_restritiva",
      "descricao": "Se Morada.pais = ES → Morada.codigoPostal segue o padrão ^[0-5][0-9]{4}$",
      "condicao": [
       {
        "propriedade": "pais",
        "operador": "EQUALS",
        "valor": "ES"
       }
      ],
      "restricao": {
       "propriedade": "codigoPostal",
       "operador": "PATTERN",
       "valor": "^[0-5][0-9]{4}$",
       "mensagem": "O código postal espanhol tem de ter cinco algarismos, a começar por 0 a 5."
      }
     },
     {
      "id": "RIR-CP-GB",
      "natureza": "inferencia_restritiva",
      "descricao": "Se Morada.pais = GB → Morada.codigoPostal segue o padrão ^[A-Z]{1,2}[0-9][0-9A-Z]? [0-9][A-Z]{2}$",
      "condicao": [
       {
        "propriedade": "pais",
        "operador": "EQUALS",
        "valor": "GB"
       }
      ],
      "restricao": {
       "propriedade": "codigoPostal",
       "operador": "PATTERN",
       "valor": "^[A-Z]{1,2}[0-9][0-9A-Z]? [0-9][A-Z]{2}$",
       "mensagem": "O código postal britânico tem de ter a forma de um postcode (ex.: SW1A 1AA)."
      }
     },
     {
      "id": "RIR-CP-LX-AJUDA",
      "natureza": "inferencia_restritiva",
      "descricao": "Se Morada.pais = PT e Morada.localidade = LISBOA e Morada.freguesia = AJUDA → Morada.codigoPostal segue o padrão ^(1300|1349)-[0-9]{3}$",
      "condicao": [
       {
        "propriedade": "pais",
        "operador": "EQUALS",
        "valor": "PT"
       },
       {
        "propriedade": "localidade",
        "operador": "EQUALS",
        "valor": "LISBOA"
       },
       {
        "propriedade": "freguesia",
        "operador": "EQUALS",
        "valor": "AJUDA"
       }
      ],
      "restricao": {
       "propriedade": "codigoPostal",
       "operador": "PATTERN",
       "valor": "^(1300|1349)-[0-9]{3}$",
       "mensagem": "O código postal de uma morada da freguesia Ajuda (Lisboa) começa por 1300 ou 1349."
      },
      "notas": "Mapeamento conhecido (códigos postais por freguesia de Lisboa) convertido em RIR: uma regra por freguesia. A vista de decisão sobre Morada.codigoPostal reconstrói a tabela."
     },
     {
      "id": "RIR-CP-LX-ALCANTARA",
      "natureza": "inferencia_restritiva",
      "descricao": "Se Morada.pais = PT e Morada.localidade = LISBOA e Morada.freguesia = ALCANTARA → Morada.codigoPostal segue o padrão ^(1300|1350)-[0-9]{3}$",
      "condicao": [
       {
        "propriedade": "pais",
        "operador": "EQUALS",
        "valor": "PT"
       },
       {
        "propriedade": "localidade",
        "operador": "EQUALS",
        "valor": "LISBOA"
       },
       {
        "propriedade": "freguesia",
        "operador": "EQUALS",
        "valor": "ALCANTARA"
       }
      ],
      "restricao": {
       "propriedade": "codigoPostal",
       "operador": "PATTERN",
       "valor": "^(1300|1350)-[0-9]{3}$",
       "mensagem": "O código postal de uma morada da freguesia Alcantara (Lisboa) começa por 1300 ou 1350."
      }
     },
     {
      "id": "RIR-CP-LX-ALVALADE",
      "natureza": "inferencia_restritiva",
      "descricao": "Se Morada.pais = PT e Morada.localidade = LISBOA e Morada.freguesia = ALVALADE → Morada.codigoPostal segue o padrão ^(1700|1749)-[0-9]{3}$",
      "condicao": [
       {
        "propriedade": "pais",
        "operador": "EQUALS",
        "valor": "PT"
       },
       {
        "propriedade": "localidade",
        "operador": "EQUALS",
        "valor": "LISBOA"
       },
       {
        "propriedade": "freguesia",
        "operador": "EQUALS",
        "valor": "ALVALADE"
       }
      ],
      "restricao": {
       "propriedade": "codigoPostal",
       "operador": "PATTERN",
       "valor": "^(1700|1749)-[0-9]{3}$",
       "mensagem": "O código postal de uma morada da freguesia Alvalade (Lisboa) começa por 1700 ou 1749."
      }
     },
     {
      "id": "RIR-CP-LX-AREEIRO",
      "natureza": "inferencia_restritiva",
      "descricao": "Se Morada.pais = PT e Morada.localidade = LISBOA e Morada.freguesia = AREEIRO → Morada.codigoPostal segue o padrão ^(1000|1049)-[0-9]{3}$",
      "condicao": [
       {
        "propriedade": "pais",
        "operador": "EQUALS",
        "valor": "PT"
       },
       {
        "propriedade": "localidade",
        "operador": "EQUALS",
        "valor": "LISBOA"
       },
       {
        "propriedade": "freguesia",
        "operador": "EQUALS",
        "valor": "AREEIRO"
       }
      ],
      "restricao": {
       "propriedade": "codigoPostal",
       "operador": "PATTERN",
       "valor": "^(1000|1049)-[0-9]{3}$",
       "mensagem": "O código postal de uma morada da freguesia Areeiro (Lisboa) começa por 1000 ou 1049."
      }
     },
     {
      "id": "RIR-CP-LX-ARROIOS",
      "natureza": "inferencia_restritiva",
      "descricao": "Se Morada.pais = PT e Morada.localidade = LISBOA e Morada.freguesia = ARROIOS → Morada.codigoPostal segue o padrão ^(1150|1169)-[0-9]{3}$",
      "condicao": [
       {
        "propriedade": "pais",
        "operador": "EQUALS",
        "valor": "PT"
       },
       {
        "propriedade": "localidade",
        "operador": "EQUALS",
        "valor": "LISBOA"
       },
       {
        "propriedade": "freguesia",
        "operador": "EQUALS",
        "valor": "ARROIOS"
       }
      ],
      "restricao": {
       "propriedade": "codigoPostal",
       "operador": "PATTERN",
       "valor": "^(1150|1169)-[0-9]{3}$",
       "mensagem": "O código postal de uma morada da freguesia Arroios (Lisboa) começa por 1150 ou 1169."
      }
     },
     {
      "id": "RIR-CP-LX-AVENIDAS-NOVAS",
      "natureza": "inferencia_restritiva",
      "descricao": "Se Morada.pais = PT e Morada.localidade = LISBOA e Morada.freguesia = AVENIDAS_NOVAS → Morada.codigoPostal segue o padrão ^(1050|1069)-[0-9]{3}$",
      "condicao": [
       {
        "propriedade": "pais",
        "operador": "EQUALS",
        "valor": "PT"
       },
       {
        "propriedade": "localidade",
        "operador": "EQUALS",
        "valor": "LISBOA"
       },
       {
        "propriedade": "freguesia",
        "operador": "EQUALS",
        "valor": "AVENIDAS_NOVAS"
       }
      ],
      "restricao": {
       "propriedade": "codigoPostal",
       "operador": "PATTERN",
       "valor": "^(1050|1069)-[0-9]{3}$",
       "mensagem": "O código postal de uma morada da freguesia Avenidas Novas (Lisboa) começa por 1050 ou 1069."
      }
     },
     {
      "id": "RIR-CP-LX-BEATO",
      "natureza": "inferencia_restritiva",
      "descricao": "Se Morada.pais = PT e Morada.localidade = LISBOA e Morada.freguesia = BEATO → Morada.codigoPostal segue o padrão ^(1900|1949)-[0-9]{3}$",
      "condicao": [
       {
        "propriedade": "pais",
        "operador": "EQUALS",
        "valor": "PT"
       },
       {
        "propriedade": "localidade",
        "operador": "EQUALS",
        "valor": "LISBOA"
       },
       {
        "propriedade": "freguesia",
        "operador": "EQUALS",
        "valor": "BEATO"
       }
      ],
      "restricao": {
       "propriedade": "codigoPostal",
       "operador": "PATTERN",
       "valor": "^(1900|1949)-[0-9]{3}$",
       "mensagem": "O código postal de uma morada da freguesia Beato (Lisboa) começa por 1900 ou 1949."
      }
     },
     {
      "id": "RIR-CP-LX-BELEM",
      "natureza": "inferencia_restritiva",
      "descricao": "Se Morada.pais = PT e Morada.localidade = LISBOA e Morada.freguesia = BELEM → Morada.codigoPostal segue o padrão ^(1400|1449)-[0-9]{3}$",
      "condicao": [
       {
        "propriedade": "pais",
        "operador": "EQUALS",
        "valor": "PT"
       },
       {
        "propriedade": "localidade",
        "operador": "EQUALS",
        "valor": "LISBOA"
       },
       {
        "propriedade": "freguesia",
        "operador": "EQUALS",
        "valor": "BELEM"
       }
      ],
      "restricao": {
       "propriedade": "codigoPostal",
       "operador": "PATTERN",
       "valor": "^(1400|1449)-[0-9]{3}$",
       "mensagem": "O código postal de uma morada da freguesia Belem (Lisboa) começa por 1400 ou 1449."
      }
     },
     {
      "id": "RIR-CP-LX-BENFICA",
      "natureza": "inferencia_restritiva",
      "descricao": "Se Morada.pais = PT e Morada.localidade = LISBOA e Morada.freguesia = BENFICA → Morada.codigoPostal segue o padrão ^(1500|1549)-[0-9]{3}$",
      "condicao": [
       {
        "propriedade": "pais",
        "operador": "EQUALS",
        "valor": "PT"
       },
       {
        "propriedade": "localidade",
        "operador": "EQUALS",
        "valor": "LISBOA"
       },
       {
        "propriedade": "freguesia",
        "operador": "EQUALS",
        "valor": "BENFICA"
       }
      ],
      "restricao": {
       "propriedade": "codigoPostal",
       "operador": "PATTERN",
       "valor": "^(1500|1549)-[0-9]{3}$",
       "mensagem": "O código postal de uma morada da freguesia Benfica (Lisboa) começa por 1500 ou 1549."
      }
     },
     {
      "id": "RIR-CP-LX-CAMPO-DE-OURIQUE",
      "natureza": "inferencia_restritiva",
      "descricao": "Se Morada.pais = PT e Morada.localidade = LISBOA e Morada.freguesia = CAMPO_DE_OURIQUE → Morada.codigoPostal segue o padrão ^(1250|1350)-[0-9]{3}$",
      "condicao": [
       {
        "propriedade": "pais",
        "operador": "EQUALS",
        "valor": "PT"
       },
       {
        "propriedade": "localidade",
        "operador": "EQUALS",
        "valor": "LISBOA"
       },
       {
        "propriedade": "freguesia",
        "operador": "EQUALS",
        "valor": "CAMPO_DE_OURIQUE"
       }
      ],
      "restricao": {
       "propriedade": "codigoPostal",
       "operador": "PATTERN",
       "valor": "^(1250|1350)-[0-9]{3}$",
       "mensagem": "O código postal de uma morada da freguesia Campo de Ourique (Lisboa) começa por 1250 ou 1350."
      }
     },
     {
      "id": "RIR-CP-LX-CAMPOLIDE",
      "natureza": "inferencia_restritiva",
      "descricao": "Se Morada.pais = PT e Morada.localidade = LISBOA e Morada.freguesia = CAMPOLIDE → Morada.codigoPostal segue o padrão ^(1070|1099)-[0-9]{3}$",
      "condicao": [
       {
        "propriedade": "pais",
        "operador": "EQUALS",
        "valor": "PT"
       },
       {
        "propriedade": "localidade",
        "operador": "EQUALS",
        "valor": "LISBOA"
       },
       {
        "propriedade": "freguesia",
        "operador": "EQUALS",
        "valor": "CAMPOLIDE"
       }
      ],
      "restricao": {
       "propriedade": "codigoPostal",
       "operador": "PATTERN",
       "valor": "^(1070|1099)-[0-9]{3}$",
       "mensagem": "O código postal de uma morada da freguesia Campolide (Lisboa) começa por 1070 ou 1099."
      }
     },
     {
      "id": "RIR-CP-LX-CARNIDE",
      "natureza": "inferencia_restritiva",
      "descricao": "Se Morada.pais = PT e Morada.localidade = LISBOA e Morada.freguesia = CARNIDE → Morada.codigoPostal segue o padrão ^(1600|1649)-[0-9]{3}$",
      "condicao": [
       {
        "propriedade": "pais",
        "operador": "EQUALS",
        "valor": "PT"
       },
       {
        "propriedade": "localidade",
        "operador": "EQUALS",
        "valor": "LISBOA"
       },
       {
        "propriedade": "freguesia",
        "operador": "EQUALS",
        "valor": "CARNIDE"
       }
      ],
      "restricao": {
       "propriedade": "codigoPostal",
       "operador": "PATTERN",
       "valor": "^(1600|1649)-[0-9]{3}$",
       "mensagem": "O código postal de uma morada da freguesia Carnide (Lisboa) começa por 1600 ou 1649."
      }
     },
     {
      "id": "RIR-CP-LX-ESTRELA",
      "natureza": "inferencia_restritiva",
      "descricao": "Se Morada.pais = PT e Morada.localidade = LISBOA e Morada.freguesia = ESTRELA → Morada.codigoPostal segue o padrão ^(1200|1249)-[0-9]{3}$",
      "condicao": [
       {
        "propriedade": "pais",
        "operador": "EQUALS",
        "valor": "PT"
       },
       {
        "propriedade": "localidade",
        "operador": "EQUALS",
        "valor": "LISBOA"
       },
       {
        "propriedade": "freguesia",
        "operador": "EQUALS",
        "valor": "ESTRELA"
       }
      ],
      "restricao": {
       "propriedade": "codigoPostal",
       "operador": "PATTERN",
       "valor": "^(1200|1249)-[0-9]{3}$",
       "mensagem": "O código postal de uma morada da freguesia Estrela (Lisboa) começa por 1200 ou 1249."
      }
     },
     {
      "id": "RIR-CP-LX-LUMIAR",
      "natureza": "inferencia_restritiva",
      "descricao": "Se Morada.pais = PT e Morada.localidade = LISBOA e Morada.freguesia = LUMIAR → Morada.codigoPostal segue o padrão ^(1600|1750)-[0-9]{3}$",
      "condicao": [
       {
        "propriedade": "pais",
        "operador": "EQUALS",
        "valor": "PT"
       },
       {
        "propriedade": "localidade",
        "operador": "EQUALS",
        "valor": "LISBOA"
       },
       {
        "propriedade": "freguesia",
        "operador": "EQUALS",
        "valor": "LUMIAR"
       }
      ],
      "restricao": {
       "propriedade": "codigoPostal",
       "operador": "PATTERN",
       "valor": "^(1600|1750)-[0-9]{3}$",
       "mensagem": "O código postal de uma morada da freguesia Lumiar (Lisboa) começa por 1600 ou 1750."
      }
     },
     {
      "id": "RIR-CP-LX-MARVILA",
      "natureza": "inferencia_restritiva",
      "descricao": "Se Morada.pais = PT e Morada.localidade = LISBOA e Morada.freguesia = MARVILA → Morada.codigoPostal segue o padrão ^(1800|1949)-[0-9]{3}$",
      "condicao": [
       {
        "propriedade": "pais",
        "operador": "EQUALS",
        "valor": "PT"
       },
       {
        "propriedade": "localidade",
        "operador": "EQUALS",
        "valor": "LISBOA"
       },
       {
        "propriedade": "freguesia",
        "operador": "EQUALS",
        "valor": "MARVILA"
       }
      ],
      "restricao": {
       "propriedade": "codigoPostal",
       "operador": "PATTERN",
       "valor": "^(1800|1949)-[0-9]{3}$",
       "mensagem": "O código postal de uma morada da freguesia Marvila (Lisboa) começa por 1800 ou 1949."
      }
     },
     {
      "id": "RIR-CP-LX-MISERICORDIA",
      "natureza": "inferencia_restritiva",
      "descricao": "Se Morada.pais = PT e Morada.localidade = LISBOA e Morada.freguesia = MISERICORDIA → Morada.codigoPostal segue o padrão ^(1200|1249)-[0-9]{3}$",
      "condicao": [
       {
        "propriedade": "pais",
        "operador": "EQUALS",
        "valor": "PT"
       },
       {
        "propriedade": "localidade",
        "operador": "EQUALS",
        "valor": "LISBOA"
       },
       {
        "propriedade": "freguesia",
        "operador": "EQUALS",
        "valor": "MISERICORDIA"
       }
      ],
      "restricao": {
       "propriedade": "codigoPostal",
       "operador": "PATTERN",
       "valor": "^(1200|1249)-[0-9]{3}$",
       "mensagem": "O código postal de uma morada da freguesia Misericordia (Lisboa) começa por 1200 ou 1249."
      }
     },
     {
      "id": "RIR-CP-LX-OLIVAIS",
      "natureza": "inferencia_restritiva",
      "descricao": "Se Morada.pais = PT e Morada.localidade = LISBOA e Morada.freguesia = OLIVAIS → Morada.codigoPostal segue o padrão ^(1800|1885)-[0-9]{3}$",
      "condicao": [
       {
        "propriedade": "pais",
        "operador": "EQUALS",
        "valor": "PT"
       },
       {
        "propriedade": "localidade",
        "operador": "EQUALS",
        "valor": "LISBOA"
       },
       {
        "propriedade": "freguesia",
        "operador": "EQUALS",
        "valor": "OLIVAIS"
       }
      ],
      "restricao": {
       "propriedade": "codigoPostal",
       "operador": "PATTERN",
       "valor": "^(1800|1885)-[0-9]{3}$",
       "mensagem": "O código postal de uma morada da freguesia Olivais (Lisboa) começa por 1800 ou 1885."
      }
     },
     {
      "id": "RIR-CP-LX-PARQUE-DAS-NACOES",
      "natureza": "inferencia_restritiva",
      "descricao": "Se Morada.pais = PT e Morada.localidade = LISBOA e Morada.freguesia = PARQUE_DAS_NACOES → Morada.codigoPostal segue o padrão ^(1990|1998)-[0-9]{3}$",
      "condicao": [
       {
        "propriedade": "pais",
        "operador": "EQUALS",
        "valor": "PT"
       },
       {
        "propriedade": "localidade",
        "operador": "EQUALS",
        "valor": "LISBOA"
       },
       {
        "propriedade": "freguesia",
        "operador": "EQUALS",
        "valor": "PARQUE_DAS_NACOES"
       }
      ],
      "restricao": {
       "propriedade": "codigoPostal",
       "operador": "PATTERN",
       "valor": "^(1990|1998)-[0-9]{3}$",
       "mensagem": "O código postal de uma morada da freguesia Parque das Nacoes (Lisboa) começa por 1990 ou 1998."
      }
     },
     {
      "id": "RIR-CP-LX-PENHA-DE-FRANCA",
      "natureza": "inferencia_restritiva",
      "descricao": "Se Morada.pais = PT e Morada.localidade = LISBOA e Morada.freguesia = PENHA_DE_FRANCA → Morada.codigoPostal segue o padrão ^(1170|1199)-[0-9]{3}$",
      "condicao": [
       {
        "propriedade": "pais",
        "operador": "EQUALS",
        "valor": "PT"
       },
       {
        "propriedade": "localidade",
        "operador": "EQUALS",
        "valor": "LISBOA"
       },
       {
        "propriedade": "freguesia",
        "operador": "EQUALS",
        "valor": "PENHA_DE_FRANCA"
       }
      ],
      "restricao": {
       "propriedade": "codigoPostal",
       "operador": "PATTERN",
       "valor": "^(1170|1199)-[0-9]{3}$",
       "mensagem": "O código postal de uma morada da freguesia Penha de Franca (Lisboa) começa por 1170 ou 1199."
      }
     },
     {
      "id": "RIR-CP-LX-SANTA-CLARA",
      "natureza": "inferencia_restritiva",
      "descricao": "Se Morada.pais = PT e Morada.localidade = LISBOA e Morada.freguesia = SANTA_CLARA → Morada.codigoPostal segue o padrão ^(1750|1769)-[0-9]{3}$",
      "condicao": [
       {
        "propriedade": "pais",
        "operador": "EQUALS",
        "valor": "PT"
       },
       {
        "propriedade": "localidade",
        "operador": "EQUALS",
        "valor": "LISBOA"
       },
       {
        "propriedade": "freguesia",
        "operador": "EQUALS",
        "valor": "SANTA_CLARA"
       }
      ],
      "restricao": {
       "propriedade": "codigoPostal",
       "operador": "PATTERN",
       "valor": "^(1750|1769)-[0-9]{3}$",
       "mensagem": "O código postal de uma morada da freguesia Santa Clara (Lisboa) começa por 1750 ou 1769."
      }
     },
     {
      "id": "RIR-CP-LX-SANTA-MARIA-MAIOR",
      "natureza": "inferencia_restritiva",
      "descricao": "Se Morada.pais = PT e Morada.localidade = LISBOA e Morada.freguesia = SANTA_MARIA_MAIOR → Morada.codigoPostal segue o padrão ^(1100|1149)-[0-9]{3}$",
      "condicao": [
       {
        "propriedade": "pais",
        "operador": "EQUALS",
        "valor": "PT"
       },
       {
        "propriedade": "localidade",
        "operador": "EQUALS",
        "valor": "LISBOA"
       },
       {
        "propriedade": "freguesia",
        "operador": "EQUALS",
        "valor": "SANTA_MARIA_MAIOR"
       }
      ],
      "restricao": {
       "propriedade": "codigoPostal",
       "operador": "PATTERN",
       "valor": "^(1100|1149)-[0-9]{3}$",
       "mensagem": "O código postal de uma morada da freguesia Santa Maria Maior (Lisboa) começa por 1100 ou 1149."
      }
     },
     {
      "id": "RIR-CP-LX-SANTO-ANTONIO",
      "natureza": "inferencia_restritiva",
      "descricao": "Se Morada.pais = PT e Morada.localidade = LISBOA e Morada.freguesia = SANTO_ANTONIO → Morada.codigoPostal segue o padrão ^(1250|1269)-[0-9]{3}$",
      "condicao": [
       {
        "propriedade": "pais",
        "operador": "EQUALS",
        "valor": "PT"
       },
       {
        "propriedade": "localidade",
        "operador": "EQUALS",
        "valor": "LISBOA"
       },
       {
        "propriedade": "freguesia",
        "operador": "EQUALS",
        "valor": "SANTO_ANTONIO"
       }
      ],
      "restricao": {
       "propriedade": "codigoPostal",
       "operador": "PATTERN",
       "valor": "^(1250|1269)-[0-9]{3}$",
       "mensagem": "O código postal de uma morada da freguesia Santo Antonio (Lisboa) começa por 1250 ou 1269."
      }
     },
     {
      "id": "RIR-CP-LX-SAO-DOMINGOS-DE-BENFICA",
      "natureza": "inferencia_restritiva",
      "descricao": "Se Morada.pais = PT e Morada.localidade = LISBOA e Morada.freguesia = SAO_DOMINGOS_DE_BENFICA → Morada.codigoPostal segue o padrão ^(1500|1600)-[0-9]{3}$",
      "condicao": [
       {
        "propriedade": "pais",
        "operador": "EQUALS",
        "valor": "PT"
       },
       {
        "propriedade": "localidade",
        "operador": "EQUALS",
        "valor": "LISBOA"
       },
       {
        "propriedade": "freguesia",
        "operador": "EQUALS",
        "valor": "SAO_DOMINGOS_DE_BENFICA"
       }
      ],
      "restricao": {
       "propriedade": "codigoPostal",
       "operador": "PATTERN",
       "valor": "^(1500|1600)-[0-9]{3}$",
       "mensagem": "O código postal de uma morada da freguesia Sao Domingos de Benfica (Lisboa) começa por 1500 ou 1600."
      }
     },
     {
      "id": "RIR-CP-LX-SAO-VICENTE",
      "natureza": "inferencia_restritiva",
      "descricao": "Se Morada.pais = PT e Morada.localidade = LISBOA e Morada.freguesia = SAO_VICENTE → Morada.codigoPostal segue o padrão ^(1100|1170)-[0-9]{3}$",
      "condicao": [
       {
        "propriedade": "pais",
        "operador": "EQUALS",
        "valor": "PT"
       },
       {
        "propriedade": "localidade",
        "operador": "EQUALS",
        "valor": "LISBOA"
       },
       {
        "propriedade": "freguesia",
        "operador": "EQUALS",
        "valor": "SAO_VICENTE"
       }
      ],
      "restricao": {
       "propriedade": "codigoPostal",
       "operador": "PATTERN",
       "valor": "^(1100|1170)-[0-9]{3}$",
       "mensagem": "O código postal de uma morada da freguesia Sao Vicente (Lisboa) começa por 1100 ou 1170."
      }
     }
    ]
   },
   {
    "nome": "Contacto",
    "descricao": "Contacto eletrónico de uma entidade.",
    "propriedades": [
     {
      "nome": "email",
      "tipo": "texto",
      "descricao": "Endereço de correio eletrónico",
      "nomesAlternativos": [
       "eMail",
       "correioEletronico"
      ],
      "regras": [
       {
        "id": "RP-EMAIL",
        "natureza": "plausibilidade",
        "descricao": "Contacto.email segue o padrão ^[a-z0-9._-]+@[a-z0-9-]+(\\.[a-z0-9-]+)+$",
        "restricao": {
         "propriedade": "email",
         "operador": "PATTERN",
         "valor": "^[a-z0-9._-]+@[a-z0-9-]+(\\.[a-z0-9-]+)+$",
         "mensagem": "O email tem de ter uma parte local e um domínio com pelo menos um ponto, sem espaços nem maiúsculas."
        }
       }
      ]
     }
    ]
   },
   {
    "nome": "ReferenciaDocumento",
    "descricao": "Referência a outro documento: o número atribuído pelo emissor e a data de emissão.",
    "propriedades": [
     {
      "nome": "numero",
      "tipo": "texto",
      "descricao": "Número de referência do documento referido",
      "nomesAlternativos": [
       "Preceding Invoice reference",
       "DocumentReference"
      ],
      "regras": [
       {
        "id": "RP-REFDOC-NUMERO",
        "natureza": "plausibilidade",
        "restricao": {
         "propriedade": "numero",
         "operador": "LENGTH",
         "valor": [
          1,
          50
         ],
         "mensagem": "O número do documento referido tem de ter entre 1 e 50 caracteres."
        },
        "descricao": "ReferenciaDocumento.numero tem entre 1 e 50 caracteres"
       }
      ]
     },
     {
      "nome": "dataEmissao",
      "tipo": "data",
      "descricao": "Data de emissão do documento referido"
     }
    ]
   }
  ],
  "sm": [
   {
    "nome": "Metainformacao",
    "descricao": "Metainformação do próprio modelo: origem, versão da fonte, entidade de origem, utilização e domínio.",
    "propriedades": [
     {
      "nome": "origemModelo",
      "tipo": "texto",
      "descricao": "Fonte do modelo de dados (norma, sistema ou repositório)"
     },
     {
      "nome": "versaoOrigem",
      "tipo": "texto",
      "descricao": "Versão da fonte usada"
     },
     {
      "nome": "referenciaOrigem",
      "tipo": "texto",
      "descricao": "Identificador da entidade na fonte (ex.: BG-0 Invoice, Device)"
     },
     {
      "nome": "utilizacao",
      "tipo": "texto",
      "descricao": "Finalidade ou contexto de utilização do modelo"
     },
     {
      "nome": "dominio",
      "tipo": "texto",
      "descricao": "Domínio a que o modelo pertence"
     },
     {
      "nome": "observacoes",
      "tipo": "texto",
      "descricao": "Outra metainformação relevante sobre o modelo"
     }
    ]
   },
   {
    "nome": "CabecalhoMensagem",
    "descricao": "Identificação da mensagem de estado: especificação, número, data e hora de emissão, e notas.",
    "propriedades": [
     {
      "nome": "identificadorEspecificacao",
      "tipo": "texto",
      "descricao": "Identificador da customização da mensagem de estado CIUS-PT (urn:feap.gov.pt:MSGSTS_CIUS-PT: seguido da versão)",
      "nomesAlternativos": [
       "CustomizationID"
      ]
     },
     {
      "nome": "numero",
      "tipo": "texto",
      "descricao": "Número de referência da mensagem, atribuído pelo emissor",
      "nomesAlternativos": [
       "ID"
      ]
     },
     {
      "nome": "dataEmissao",
      "tipo": "data",
      "descricao": "Data de emissão da mensagem de estado",
      "nomesAlternativos": [
       "IssueDate"
      ]
     },
     {
      "nome": "horaEmissao",
      "tipo": "texto",
      "descricao": "Hora de emissão da mensagem de estado (HH:MM:SS)",
      "nomesAlternativos": [
       "IssueTime"
      ],
      "regras": [
       {
        "id": "RP-MSG-HORA",
        "natureza": "plausibilidade",
        "restricao": {
         "propriedade": "horaEmissao",
         "operador": "PATTERN",
         "valor": "^[0-2][0-9]:[0-5][0-9]:[0-5][0-9]$",
         "mensagem": "A hora de emissão tem de ter o formato HH:MM:SS."
        },
        "descricao": "CabecalhoMensagem.horaEmissao segue o padrão ^[0-2][0-9]:[0-5][0-9]:[0-5][0-9]$"
       }
      ]
     },
     {
      "nome": "nota",
      "tipo": "texto",
      "descricao": "Informação não estruturada sobre a mensagem",
      "nomesAlternativos": [
       "Note"
      ]
     }
    ]
   },
   {
    "nome": "ParteMensagem",
    "descricao": "Parte que emite ou recebe a mensagem de estado: identificação fiscal, país e correio eletrónico.",
    "composicao": [
     {
      "usm": "SujeitoPassivo",
      "cardinalidade": "1..1"
     },
     {
      "usm": "Morada",
      "cardinalidade": "1..1"
     },
     {
      "usm": "Contacto",
      "cardinalidade": "0..1"
     }
    ]
   },
   {
    "nome": "RespostaDocumento",
    "descricao": "Resposta sobre um documento recebido: código e descrição da resposta, e o documento a que se refere.",
    "composicao": [
     {
      "usm": "ReferenciaDocumento",
      "cardinalidade": "1..1"
     }
    ],
    "propriedades": [
     {
      "nome": "codigoResposta",
      "tipo": "texto",
      "descricao": "Código da resposta",
      "nomesAlternativos": [
       "ResponseCode"
      ]
     },
     {
      "nome": "descricaoResposta",
      "tipo": "texto",
      "descricao": "Descrição dos erros, avisos ou informações da resposta",
      "nomesAlternativos": [
       "Description"
      ]
     },
     {
      "nome": "uuidDocumento",
      "tipo": "texto",
      "descricao": "Número de referência universal (UUID) do documento referido",
      "nomesAlternativos": [
       "UUID"
      ]
     },
     {
      "nome": "tipoDocumento",
      "tipo": "texto",
      "descricao": "Tipo funcional do documento referido (UNCL 1001)",
      "nomesAlternativos": [
       "DocumentTypeCode"
      ],
      "regras": [
       {
        "id": "RP-RESP-TIPODOC",
        "natureza": "plausibilidade",
        "restricao": {
         "propriedade": "tipoDocumento",
         "operador": "IN",
         "valor": [
          "380",
          "381",
          "383"
         ],
         "mensagem": "O tipo do documento referido tem de ser 380 (fatura), 381 (nota de crédito) ou 383 (nota de débito)."
        },
        "descricao": "RespostaDocumento.tipoDocumento ∈ {380, 381, 383}"
       }
      ]
     },
     {
      "nome": "estadoDocumento",
      "tipo": "texto",
      "descricao": "Estado do documento do ponto de vista do cliente nele referido",
      "nomesAlternativos": [
       "DocumentStatusCode"
      ]
     }
    ]
   }
  ],
  "hlm": [
   {
    "nome": "MensagemEstado",
    "descricao": "Mensagem de estado CIUS-PT: resposta de uma parte (normalmente o adquirente) sobre um documento de faturação recebido.",
    "composicao": [
     {
      "sm": "CabecalhoMensagem",
      "cardinalidade": "1..1"
     },
     {
      "sm": "ParteMensagem",
      "papel": "Emissor",
      "cardinalidade": "1..1"
     },
     {
      "sm": "ParteMensagem",
      "papel": "Recetor",
      "cardinalidade": "1..1"
     },
     {
      "sm": "RespostaDocumento",
      "cardinalidade": "0..1"
     },
     {
      "sm": "Metainformacao",
      "papel": "Metainformacao",
      "cardinalidade": "0..1"
     }
    ]
   }
  ],
  "projecoes": [
   {
    "nome": "MensagemEstadoCiusPt",
    "hlm": "MensagemEstado",
    "descricao": "Mensagem de estado com que o adquirente responde a um documento recebido.",
    "obrigatorias": [
     "CabecalhoMensagem.identificadorEspecificacao",
     "CabecalhoMensagem.numero",
     "CabecalhoMensagem.dataEmissao",
     "CabecalhoMensagem.nota",
     "Emissor.SujeitoPassivo.nome",
     "Emissor.SujeitoPassivo.identificadorIva",
     "Emissor.Morada.pais",
     "Emissor.Contacto.email",
     "Recetor.SujeitoPassivo.nome",
     "Recetor.SujeitoPassivo.identificadorIva",
     "Recetor.Morada.pais",
     "Recetor.Contacto.email",
     "RespostaDocumento.codigoResposta",
     "RespostaDocumento.tipoDocumento",
     "RespostaDocumento.ReferenciaDocumento.numero",
     "RespostaDocumento.ReferenciaDocumento.dataEmissao"
    ],
    "permitidas": [
     "CabecalhoMensagem.horaEmissao",
     "Emissor.SujeitoPassivo.nomeComercial",
     "Emissor.SujeitoPassivo.identificadorRegisto",
     "Emissor.Morada.localidade",
     "Emissor.Morada.codigoPostal",
     "Emissor.Morada.freguesia",
     "Recetor.SujeitoPassivo.nomeComercial",
     "Recetor.SujeitoPassivo.identificadorRegisto",
     "Recetor.Morada.localidade",
     "Recetor.Morada.codigoPostal",
     "Recetor.Morada.freguesia",
     "RespostaDocumento.descricaoResposta",
     "RespostaDocumento.uuidDocumento",
     "RespostaDocumento.estadoDocumento",
     "Metainformacao.*"
    ]
   }
  ],
  "perfis": [
   {
    "nome": "RespostaAdquirente",
    "projecao": "MensagemEstadoCiusPt",
    "descricao": "Resposta do adquirente a um documento emitido por um fornecedor português.",
    "fixa": [
     {
      "propriedade": "Recetor.Morada.pais",
      "valor": "PT"
     }
    ]
   }
  ]
 }
]
```

## Mapeamento atual

```json
[
 {
  "fonte": "cius-pt-guia",
  "origem": "BT-1",
  "decisao": "mapeado",
  "destino": "HLM:DocumentoFaturacao/CabecalhoDocumento.numero",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-guia",
  "origem": "BT-2",
  "decisao": "mapeado",
  "destino": "HLM:DocumentoFaturacao/CabecalhoDocumento.dataEmissao",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-guia",
  "origem": "BT-3",
  "decisao": "mapeado",
  "destino": "HLM:DocumentoFaturacao/CabecalhoDocumento.tipoDocumento",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-guia",
  "origem": "BT-5",
  "decisao": "mapeado",
  "destino": "HLM:DocumentoFaturacao/CabecalhoDocumento.moeda",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-guia",
  "origem": "BT-6",
  "decisao": "mapeado",
  "destino": "HLM:DocumentoFaturacao/CabecalhoDocumento.moedaIva",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-guia",
  "origem": "BT-7",
  "decisao": "mapeado",
  "destino": "HLM:DocumentoFaturacao/CabecalhoDocumento.dataIva",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-guia",
  "origem": "BT-8",
  "decisao": "mapeado",
  "destino": "HLM:DocumentoFaturacao/CabecalhoDocumento.codigoDataIva",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-guia",
  "origem": "BT-9",
  "decisao": "mapeado",
  "destino": "HLM:DocumentoFaturacao/CabecalhoDocumento.dataVencimento",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-guia",
  "origem": "BT-10",
  "decisao": "mapeado",
  "destino": "HLM:DocumentoFaturacao/CabecalhoDocumento.referenciaCliente",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-guia",
  "origem": "BT-11",
  "decisao": "mapeado",
  "destino": "HLM:DocumentoFaturacao/ReferenciasDocumento.projeto",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-guia",
  "origem": "BT-12",
  "decisao": "mapeado",
  "destino": "HLM:DocumentoFaturacao/ReferenciasDocumento.contrato",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-guia",
  "origem": "BT-13",
  "decisao": "mapeado",
  "destino": "HLM:DocumentoFaturacao/ReferenciasDocumento.encomenda",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-guia",
  "origem": "BT-14",
  "decisao": "mapeado",
  "destino": "HLM:DocumentoFaturacao/ReferenciasDocumento.ordemVenda",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-guia",
  "origem": "BT-15",
  "decisao": "mapeado",
  "destino": "HLM:DocumentoFaturacao/ReferenciasDocumento.avisoRececao",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-guia",
  "origem": "BT-16",
  "decisao": "mapeado",
  "destino": "HLM:DocumentoFaturacao/ReferenciasDocumento.avisoEnvio",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-guia",
  "origem": "BT-17",
  "decisao": "mapeado",
  "destino": "HLM:DocumentoFaturacao/ReferenciasDocumento.acordoQuadro",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-guia",
  "origem": "BT-18",
  "decisao": "mapeado",
  "destino": "HLM:DocumentoFaturacao/ReferenciasDocumento.processoRegisto",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-guia",
  "origem": "BT-19",
  "decisao": "mapeado",
  "destino": "HLM:DocumentoFaturacao/CabecalhoDocumento.numeroCompromisso",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-guia",
  "origem": "BT-20",
  "decisao": "mapeado",
  "destino": "HLM:DocumentoFaturacao/CabecalhoDocumento.condicoesPagamento",
  "nota": "0..* na fonte; o UBL-SR-05 limita a uma ocorrência",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-guia",
  "origem": "BT-21",
  "decisao": "mapeado",
  "destino": "HLM:DocumentoFaturacao/NotaDocumento.assunto",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-guia",
  "origem": "BT-22",
  "decisao": "mapeado",
  "destino": "HLM:DocumentoFaturacao/NotaDocumento.texto",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-guia",
  "origem": "BT-23",
  "decisao": "mapeado",
  "destino": "HLM:DocumentoFaturacao/CabecalhoDocumento.tipoProcesso",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-guia",
  "origem": "BT-24",
  "decisao": "mapeado",
  "destino": "HLM:DocumentoFaturacao/CabecalhoDocumento.identificadorEspecificacao",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-guia",
  "origem": "BT-25",
  "decisao": "mapeado",
  "destino": "HLM:DocumentoFaturacao/DocumentosAnteriores.ReferenciaDocumento.numero",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-guia",
  "origem": "BT-26",
  "decisao": "mapeado",
  "destino": "HLM:DocumentoFaturacao/DocumentosAnteriores.ReferenciaDocumento.dataEmissao",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-guia",
  "origem": "BT-27",
  "decisao": "mapeado",
  "destino": "HLM:DocumentoFaturacao/Fornecedor.SujeitoPassivo.nome",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-guia",
  "origem": "BT-28",
  "decisao": "mapeado",
  "destino": "HLM:DocumentoFaturacao/Fornecedor.SujeitoPassivo.nomeComercial",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-guia",
  "origem": "BT-29",
  "decisao": "mapeado",
  "destino": "HLM:DocumentoFaturacao/Fornecedor.SujeitoPassivo.identificador",
  "nota": "0..* na fonte; simplificado a um valor",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-guia",
  "origem": "BT-30",
  "decisao": "mapeado",
  "destino": "HLM:DocumentoFaturacao/Fornecedor.SujeitoPassivo.identificadorRegisto",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-guia",
  "origem": "BT-31",
  "decisao": "mapeado",
  "destino": "HLM:DocumentoFaturacao/Fornecedor.SujeitoPassivo.identificadorIva",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-guia",
  "origem": "BT-32",
  "decisao": "mapeado",
  "destino": "HLM:DocumentoFaturacao/Fornecedor.registoFiscal",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-guia",
  "origem": "BT-33",
  "decisao": "mapeado",
  "destino": "HLM:DocumentoFaturacao/Fornecedor.capitalSocial",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-guia",
  "origem": "BT-34",
  "decisao": "mapeado",
  "destino": "HLM:DocumentoFaturacao/Fornecedor.enderecoEletronico",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-guia",
  "origem": "BT-35",
  "decisao": "mapeado",
  "destino": "HLM:DocumentoFaturacao/Fornecedor.Morada.rua",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-guia",
  "origem": "BT-36",
  "decisao": "mapeado",
  "destino": "HLM:DocumentoFaturacao/Fornecedor.ComplementoMorada.linha2",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-guia",
  "origem": "BT-162",
  "decisao": "mapeado",
  "destino": "HLM:DocumentoFaturacao/Fornecedor.ComplementoMorada.linha3",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-guia",
  "origem": "BT-37",
  "decisao": "mapeado",
  "destino": "HLM:DocumentoFaturacao/Fornecedor.Morada.localidade",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-guia",
  "origem": "BT-38",
  "decisao": "mapeado",
  "destino": "HLM:DocumentoFaturacao/Fornecedor.Morada.codigoPostal",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-guia",
  "origem": "BT-39",
  "decisao": "mapeado",
  "destino": "HLM:DocumentoFaturacao/Fornecedor.ComplementoMorada.regiao",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-guia",
  "origem": "BT-40",
  "decisao": "mapeado",
  "destino": "HLM:DocumentoFaturacao/Fornecedor.Morada.pais",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-guia",
  "origem": "BT-41",
  "decisao": "mapeado",
  "destino": "HLM:DocumentoFaturacao/Fornecedor.pontoContacto",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-guia",
  "origem": "BT-42",
  "decisao": "mapeado",
  "destino": "HLM:DocumentoFaturacao/Fornecedor.ContactoTelefonico.telefone",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-guia",
  "origem": "BT-43",
  "decisao": "mapeado",
  "destino": "HLM:DocumentoFaturacao/Fornecedor.Contacto.email",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-guia",
  "origem": "BT-44",
  "decisao": "mapeado",
  "destino": "HLM:DocumentoFaturacao/Adquirente.SujeitoPassivo.nome",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-guia",
  "origem": "BT-45",
  "decisao": "mapeado",
  "destino": "HLM:DocumentoFaturacao/Adquirente.SujeitoPassivo.nomeComercial",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-guia",
  "origem": "BT-46",
  "decisao": "mapeado",
  "destino": "HLM:DocumentoFaturacao/Adquirente.SujeitoPassivo.identificador",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-guia",
  "origem": "BT-47",
  "decisao": "mapeado",
  "destino": "HLM:DocumentoFaturacao/Adquirente.SujeitoPassivo.identificadorRegisto",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-guia",
  "origem": "BT-48",
  "decisao": "mapeado",
  "destino": "HLM:DocumentoFaturacao/Adquirente.SujeitoPassivo.identificadorIva",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-guia",
  "origem": "BT-49",
  "decisao": "mapeado",
  "destino": "HLM:DocumentoFaturacao/Adquirente.enderecoEletronico",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-guia",
  "origem": "BT-50",
  "decisao": "mapeado",
  "destino": "HLM:DocumentoFaturacao/Adquirente.Morada.rua",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-guia",
  "origem": "BT-51",
  "decisao": "mapeado",
  "destino": "HLM:DocumentoFaturacao/Adquirente.ComplementoMorada.linha2",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-guia",
  "origem": "BT-163",
  "decisao": "mapeado",
  "destino": "HLM:DocumentoFaturacao/Adquirente.ComplementoMorada.linha3",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-guia",
  "origem": "BT-52",
  "decisao": "mapeado",
  "destino": "HLM:DocumentoFaturacao/Adquirente.Morada.localidade",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-guia",
  "origem": "BT-53",
  "decisao": "mapeado",
  "destino": "HLM:DocumentoFaturacao/Adquirente.Morada.codigoPostal",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-guia",
  "origem": "BT-54",
  "decisao": "mapeado",
  "destino": "HLM:DocumentoFaturacao/Adquirente.ComplementoMorada.regiao",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-guia",
  "origem": "BT-55",
  "decisao": "mapeado",
  "destino": "HLM:DocumentoFaturacao/Adquirente.Morada.pais",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-guia",
  "origem": "BT-56",
  "decisao": "mapeado",
  "destino": "HLM:DocumentoFaturacao/Adquirente.pontoContacto",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-guia",
  "origem": "BT-57",
  "decisao": "mapeado",
  "destino": "HLM:DocumentoFaturacao/Adquirente.ContactoTelefonico.telefone",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-guia",
  "origem": "BT-58",
  "decisao": "mapeado",
  "destino": "HLM:DocumentoFaturacao/Adquirente.Contacto.email",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-guia",
  "origem": "BT-59",
  "decisao": "mapeado",
  "destino": "HLM:DocumentoFaturacao/RecebedorPagamento.SujeitoPassivo.nome",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-guia",
  "origem": "BT-60",
  "decisao": "mapeado",
  "destino": "HLM:DocumentoFaturacao/RecebedorPagamento.SujeitoPassivo.identificador",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-guia",
  "origem": "BT-61",
  "decisao": "mapeado",
  "destino": "HLM:DocumentoFaturacao/RecebedorPagamento.SujeitoPassivo.identificadorRegisto",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-guia",
  "origem": "BT-62",
  "decisao": "mapeado",
  "destino": "HLM:DocumentoFaturacao/RepresentanteFiscal.SujeitoPassivo.nome",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-guia",
  "origem": "BT-63",
  "decisao": "mapeado",
  "destino": "HLM:DocumentoFaturacao/RepresentanteFiscal.SujeitoPassivo.identificadorIva",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-guia",
  "origem": "BT-64",
  "decisao": "mapeado",
  "destino": "HLM:DocumentoFaturacao/RepresentanteFiscal.Morada.rua",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-guia",
  "origem": "BT-65",
  "decisao": "mapeado",
  "destino": "HLM:DocumentoFaturacao/RepresentanteFiscal.ComplementoMorada.linha2",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-guia",
  "origem": "BT-164",
  "decisao": "mapeado",
  "destino": "HLM:DocumentoFaturacao/RepresentanteFiscal.ComplementoMorada.linha3",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-guia",
  "origem": "BT-66",
  "decisao": "mapeado",
  "destino": "HLM:DocumentoFaturacao/RepresentanteFiscal.Morada.localidade",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-guia",
  "origem": "BT-67",
  "decisao": "mapeado",
  "destino": "HLM:DocumentoFaturacao/RepresentanteFiscal.Morada.codigoPostal",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-guia",
  "origem": "BT-68",
  "decisao": "mapeado",
  "destino": "HLM:DocumentoFaturacao/RepresentanteFiscal.ComplementoMorada.regiao",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-guia",
  "origem": "BT-69",
  "decisao": "mapeado",
  "destino": "HLM:DocumentoFaturacao/RepresentanteFiscal.Morada.pais",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-guia",
  "origem": "BT-70",
  "decisao": "mapeado",
  "destino": "HLM:DocumentoFaturacao/LocalEntrega.nomeLocal",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-guia",
  "origem": "BT-71",
  "decisao": "mapeado",
  "destino": "HLM:DocumentoFaturacao/LocalEntrega.identificadorLocal",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-guia",
  "origem": "BT-72",
  "decisao": "mapeado",
  "destino": "HLM:DocumentoFaturacao/LocalEntrega.dataEntrega",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-guia",
  "origem": "BT-73",
  "decisao": "mapeado",
  "destino": "HLM:DocumentoFaturacao/PeriodoFaturacao.Periodo.dataInicio",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-guia",
  "origem": "BT-74",
  "decisao": "mapeado",
  "destino": "HLM:DocumentoFaturacao/PeriodoFaturacao.Periodo.dataFim",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-guia",
  "origem": "BT-75",
  "decisao": "mapeado",
  "destino": "HLM:DocumentoFaturacao/LocalEntrega.Morada.rua",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-guia",
  "origem": "BT-76",
  "decisao": "mapeado",
  "destino": "HLM:DocumentoFaturacao/LocalEntrega.ComplementoMorada.linha2",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-guia",
  "origem": "BT-165",
  "decisao": "mapeado",
  "destino": "HLM:DocumentoFaturacao/LocalEntrega.ComplementoMorada.linha3",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-guia",
  "origem": "BT-77",
  "decisao": "mapeado",
  "destino": "HLM:DocumentoFaturacao/LocalEntrega.Morada.localidade",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-guia",
  "origem": "BT-78",
  "decisao": "mapeado",
  "destino": "HLM:DocumentoFaturacao/LocalEntrega.Morada.codigoPostal",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-guia",
  "origem": "BT-79",
  "decisao": "mapeado",
  "destino": "HLM:DocumentoFaturacao/LocalEntrega.ComplementoMorada.regiao",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-guia",
  "origem": "BT-80",
  "decisao": "mapeado",
  "destino": "HLM:DocumentoFaturacao/LocalEntrega.Morada.pais",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-guia",
  "origem": "BT-81",
  "decisao": "mapeado",
  "destino": "HLM:DocumentoFaturacao/Pagamento.meioPagamento",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-guia",
  "origem": "BT-82",
  "decisao": "mapeado",
  "destino": "HLM:DocumentoFaturacao/Pagamento.detalhePagamento",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-guia",
  "origem": "BT-83",
  "decisao": "mapeado",
  "destino": "HLM:DocumentoFaturacao/Pagamento.referenciaPagamento",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-guia",
  "origem": "BT-84",
  "decisao": "mapeado",
  "destino": "HLM:DocumentoFaturacao/Pagamento.ContaBancaria.iban",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-guia",
  "origem": "BT-85",
  "decisao": "mapeado",
  "destino": "HLM:DocumentoFaturacao/Pagamento.ContaBancaria.nomeConta",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-guia",
  "origem": "BT-86",
  "decisao": "mapeado",
  "destino": "HLM:DocumentoFaturacao/Pagamento.ContaBancaria.bic",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-guia",
  "origem": "BT-87",
  "decisao": "mapeado",
  "destino": "HLM:DocumentoFaturacao/Pagamento.CartaoPagamento.numeroConta",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-guia",
  "origem": "BT-88",
  "decisao": "mapeado",
  "destino": "HLM:DocumentoFaturacao/Pagamento.CartaoPagamento.titular",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-guia",
  "origem": "BT-89",
  "decisao": "mapeado",
  "destino": "HLM:DocumentoFaturacao/Pagamento.DebitoDireto.referenciaMandato",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-guia",
  "origem": "BT-90",
  "decisao": "mapeado",
  "destino": "HLM:DocumentoFaturacao/Pagamento.DebitoDireto.identificadorCredor",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-guia",
  "origem": "BT-91",
  "decisao": "mapeado",
  "destino": "HLM:DocumentoFaturacao/Pagamento.DebitoDireto.contaDebitada",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-guia",
  "origem": "BT-92",
  "decisao": "mapeado",
  "destino": "HLM:DocumentoFaturacao/Desconto.DescontoEncargo.montante",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-guia",
  "origem": "BT-93",
  "decisao": "mapeado",
  "destino": "HLM:DocumentoFaturacao/Desconto.DescontoEncargo.montanteBase",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-guia",
  "origem": "BT-94",
  "decisao": "mapeado",
  "destino": "HLM:DocumentoFaturacao/Desconto.DescontoEncargo.percentagem",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-guia",
  "origem": "BT-95",
  "decisao": "mapeado",
  "destino": "HLM:DocumentoFaturacao/Desconto.CategoriaIva.codigoCategoria",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-guia",
  "origem": "BT-96",
  "decisao": "mapeado",
  "destino": "HLM:DocumentoFaturacao/Desconto.CategoriaIva.taxa",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-guia",
  "origem": "BT-97",
  "decisao": "mapeado",
  "destino": "HLM:DocumentoFaturacao/Desconto.DescontoEncargo.motivo",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-guia",
  "origem": "BT-98",
  "decisao": "mapeado",
  "destino": "HLM:DocumentoFaturacao/Desconto.DescontoEncargo.codigoMotivo",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-guia",
  "origem": "BT-99",
  "decisao": "mapeado",
  "destino": "HLM:DocumentoFaturacao/Encargo.DescontoEncargo.montante",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-guia",
  "origem": "BT-100",
  "decisao": "mapeado",
  "destino": "HLM:DocumentoFaturacao/Encargo.DescontoEncargo.montanteBase",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-guia",
  "origem": "BT-101",
  "decisao": "mapeado",
  "destino": "HLM:DocumentoFaturacao/Encargo.DescontoEncargo.percentagem",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-guia",
  "origem": "BT-102",
  "decisao": "mapeado",
  "destino": "HLM:DocumentoFaturacao/Encargo.CategoriaIva.codigoCategoria",
  "nota": "o guia admite só AA, S, E nos encargos; a RP aplica a lista completa de CategoriaIva",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-guia",
  "origem": "BT-103",
  "decisao": "mapeado",
  "destino": "HLM:DocumentoFaturacao/Encargo.CategoriaIva.taxa",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-guia",
  "origem": "BT-104",
  "decisao": "mapeado",
  "destino": "HLM:DocumentoFaturacao/Encargo.DescontoEncargo.motivo",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-guia",
  "origem": "BT-105",
  "decisao": "mapeado",
  "destino": "HLM:DocumentoFaturacao/Encargo.DescontoEncargo.codigoMotivo",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-guia",
  "origem": "BT-106",
  "decisao": "mapeado",
  "destino": "HLM:DocumentoFaturacao/Totais.somaLinhas",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-guia",
  "origem": "BT-107",
  "decisao": "mapeado",
  "destino": "HLM:DocumentoFaturacao/Totais.totalDescontos",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-guia",
  "origem": "BT-108",
  "decisao": "mapeado",
  "destino": "HLM:DocumentoFaturacao/Totais.totalEncargos",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-guia",
  "origem": "BT-109",
  "decisao": "mapeado",
  "destino": "HLM:DocumentoFaturacao/Totais.totalSemIva",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-guia",
  "origem": "BT-110",
  "decisao": "mapeado",
  "destino": "HLM:DocumentoFaturacao/Totais.totalIva",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-guia",
  "origem": "BT-111",
  "decisao": "mapeado",
  "destino": "HLM:DocumentoFaturacao/Totais.totalIvaMoedaContabilistica",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-guia",
  "origem": "BT-112",
  "decisao": "mapeado",
  "destino": "HLM:DocumentoFaturacao/Totais.totalComIva",
  "nota": "o nome alternativo 'VAT' da fonte foi ignorado por ser ambíguo",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-guia",
  "origem": "BT-113",
  "decisao": "mapeado",
  "destino": "HLM:DocumentoFaturacao/Totais.valorPago",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-guia",
  "origem": "BT-114",
  "decisao": "mapeado",
  "destino": "HLM:DocumentoFaturacao/Totais.arredondamento",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-guia",
  "origem": "BT-115",
  "decisao": "mapeado",
  "destino": "HLM:DocumentoFaturacao/Totais.valorPagar",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-guia",
  "origem": "BT-116",
  "decisao": "mapeado",
  "destino": "HLM:DocumentoFaturacao/DecomposicaoIva.baseTributavel",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-guia",
  "origem": "BT-117",
  "decisao": "mapeado",
  "destino": "HLM:DocumentoFaturacao/DecomposicaoIva.montanteImposto",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-guia",
  "origem": "BT-118",
  "decisao": "mapeado",
  "destino": "HLM:DocumentoFaturacao/DecomposicaoIva.CategoriaIva.codigoCategoria",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-guia",
  "origem": "BT-119",
  "decisao": "mapeado",
  "destino": "HLM:DocumentoFaturacao/DecomposicaoIva.CategoriaIva.taxa",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-guia",
  "origem": "BT-120",
  "decisao": "mapeado",
  "destino": "HLM:DocumentoFaturacao/DecomposicaoIva.CategoriaIva.motivoIsencao",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-guia",
  "origem": "BT-121",
  "decisao": "mapeado",
  "destino": "HLM:DocumentoFaturacao/DecomposicaoIva.CategoriaIva.codigoMotivoIsencao",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-guia",
  "origem": "BT-122",
  "decisao": "mapeado",
  "destino": "HLM:DocumentoFaturacao/DocumentoSuporte.referencia",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-guia",
  "origem": "BT-123",
  "decisao": "mapeado",
  "destino": "HLM:DocumentoFaturacao/DocumentoSuporte.descricao",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-guia",
  "origem": "BT-124",
  "decisao": "mapeado",
  "destino": "HLM:DocumentoFaturacao/DocumentoSuporte.localizacaoExterna",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-guia",
  "origem": "BT-125",
  "decisao": "mapeado",
  "destino": "HLM:DocumentoFaturacao/DocumentoSuporte.anexo",
  "nota": "o tipo MIME e o nome do ficheiro passam a DocumentoSuporte.tipoMime e .nomeFicheiro",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-guia",
  "origem": "BT-126",
  "decisao": "mapeado",
  "destino": "HLM:DocumentoFaturacao/LinhaDocumento.identificador",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-guia",
  "origem": "BT-127",
  "decisao": "mapeado",
  "destino": "HLM:DocumentoFaturacao/LinhaDocumento.nota",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-guia",
  "origem": "BT-128",
  "decisao": "mapeado",
  "destino": "HLM:DocumentoFaturacao/LinhaDocumento.identificadorObjeto",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-guia",
  "origem": "BT-129",
  "decisao": "mapeado",
  "destino": "HLM:DocumentoFaturacao/LinhaDocumento.quantidade",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-guia",
  "origem": "BT-130",
  "decisao": "mapeado",
  "destino": "HLM:DocumentoFaturacao/LinhaDocumento.unidadeMedida",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-guia",
  "origem": "BT-131",
  "decisao": "mapeado",
  "destino": "HLM:DocumentoFaturacao/LinhaDocumento.montanteLiquido",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-guia",
  "origem": "BT-132",
  "decisao": "mapeado",
  "destino": "HLM:DocumentoFaturacao/LinhaDocumento.referenciaLinhaEncomenda",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-guia",
  "origem": "BT-133",
  "decisao": "mapeado",
  "destino": "HLM:DocumentoFaturacao/LinhaDocumento.numeroCompromisso",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-guia",
  "origem": "BT-134",
  "decisao": "mapeado",
  "destino": "HLM:DocumentoFaturacao/LinhaDocumento.Periodo.dataInicio",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-guia",
  "origem": "BT-135",
  "decisao": "mapeado",
  "destino": "HLM:DocumentoFaturacao/LinhaDocumento.Periodo.dataFim",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-guia",
  "origem": "BT-136",
  "decisao": "mapeado",
  "destino": "HLM:DocumentoFaturacao/LinhaDocumento.Desconto.montante",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-guia",
  "origem": "BT-137",
  "decisao": "mapeado",
  "destino": "HLM:DocumentoFaturacao/LinhaDocumento.Desconto.montanteBase",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-guia",
  "origem": "BT-138",
  "decisao": "mapeado",
  "destino": "HLM:DocumentoFaturacao/LinhaDocumento.Desconto.percentagem",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-guia",
  "origem": "BT-139",
  "decisao": "mapeado",
  "destino": "HLM:DocumentoFaturacao/LinhaDocumento.Desconto.motivo",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-guia",
  "origem": "BT-140",
  "decisao": "mapeado",
  "destino": "HLM:DocumentoFaturacao/LinhaDocumento.Desconto.codigoMotivo",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-guia",
  "origem": "BT-141",
  "decisao": "mapeado",
  "destino": "HLM:DocumentoFaturacao/LinhaDocumento.Encargo.montante",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-guia",
  "origem": "BT-142",
  "decisao": "mapeado",
  "destino": "HLM:DocumentoFaturacao/LinhaDocumento.Encargo.montanteBase",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-guia",
  "origem": "BT-143",
  "decisao": "mapeado",
  "destino": "HLM:DocumentoFaturacao/LinhaDocumento.Encargo.percentagem",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-guia",
  "origem": "BT-144",
  "decisao": "mapeado",
  "destino": "HLM:DocumentoFaturacao/LinhaDocumento.Encargo.motivo",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-guia",
  "origem": "BT-145",
  "decisao": "mapeado",
  "destino": "HLM:DocumentoFaturacao/LinhaDocumento.Encargo.codigoMotivo",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-guia",
  "origem": "BT-146",
  "decisao": "mapeado",
  "destino": "HLM:DocumentoFaturacao/LinhaDocumento.Preco.precoLiquido",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-guia",
  "origem": "BT-147",
  "decisao": "mapeado",
  "destino": "HLM:DocumentoFaturacao/LinhaDocumento.Preco.descontoPreco",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-guia",
  "origem": "BT-148",
  "decisao": "mapeado",
  "destino": "HLM:DocumentoFaturacao/LinhaDocumento.Preco.precoBruto",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-guia",
  "origem": "BT-149",
  "decisao": "mapeado",
  "destino": "HLM:DocumentoFaturacao/LinhaDocumento.Preco.quantidadeBase",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-guia",
  "origem": "BT-150",
  "decisao": "mapeado",
  "destino": "HLM:DocumentoFaturacao/LinhaDocumento.Preco.unidadeQuantidadeBase",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-guia",
  "origem": "BT-151",
  "decisao": "mapeado",
  "destino": "HLM:DocumentoFaturacao/LinhaDocumento.CategoriaIva.codigoCategoria",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-guia",
  "origem": "BT-152",
  "decisao": "mapeado",
  "destino": "HLM:DocumentoFaturacao/LinhaDocumento.CategoriaIva.taxa",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-guia",
  "origem": "BT-153",
  "decisao": "mapeado",
  "destino": "HLM:DocumentoFaturacao/LinhaDocumento.Artigo.nome",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-guia",
  "origem": "BT-154",
  "decisao": "mapeado",
  "destino": "HLM:DocumentoFaturacao/LinhaDocumento.Artigo.descricao",
  "nota": "0..* na fonte; simplificado a um valor",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-guia",
  "origem": "BT-155",
  "decisao": "mapeado",
  "destino": "HLM:DocumentoFaturacao/LinhaDocumento.Artigo.codigo",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-guia",
  "origem": "BT-156",
  "decisao": "mapeado",
  "destino": "HLM:DocumentoFaturacao/LinhaDocumento.Artigo.codigoComprador",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-guia",
  "origem": "BT-157",
  "decisao": "mapeado",
  "destino": "HLM:DocumentoFaturacao/LinhaDocumento.Artigo.codigoBarras",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-guia",
  "origem": "BT-158",
  "decisao": "mapeado",
  "destino": "HLM:DocumentoFaturacao/LinhaDocumento.Artigo.classificacao",
  "nota": "0..* na fonte; simplificado a um valor",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-guia",
  "origem": "BT-159",
  "decisao": "mapeado",
  "destino": "HLM:DocumentoFaturacao/LinhaDocumento.Artigo.paisOrigem",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-guia",
  "origem": "BT-160",
  "decisao": "mapeado",
  "destino": "HLM:DocumentoFaturacao/LinhaDocumento.AtributoArtigo.nome",
  "nota": "quando codifica o motivo de isenção da linha (#TAXEXEMPTIONREASON…#), passa a LinhaDocumento.CategoriaIva.motivoIsencao/codigoMotivoIsencao",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-guia",
  "origem": "BT-161",
  "decisao": "mapeado",
  "destino": "HLM:DocumentoFaturacao/LinhaDocumento.AtributoArtigo.valor",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-schematron",
  "origem": "BR-01, BR-02, BR-03, BR-04, BR-05, BR-06, BR-07, BR-08, BR-09, BR-10, BR-11, BR-12, BR-13, BR-14, BR-15, BR-CIUS-PT-01, BR-CIUS-PT-03, BR-CIUS-PT-05, BR-CIUS-PT-06, BR-CIUS-PT-07, BR-CIUS-PT-10, BR-CIUS-PT-11",
  "decisao": "mapeado",
  "destino": "Projecao:FaturaCiusPt/obrigatorias",
  "nota": "presença obrigatória; igual em NotaCreditoCiusPt",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-schematron",
  "origem": "BR-21, BR-22, BR-23, BR-24, BR-25, BR-26, BR-CO-04, BR-31, BR-32, BR-36, BR-37, BR-41, BR-43, BR-45, BR-46, BR-47, BR-48, BR-49, BR-50, BR-52, BR-54, BR-55, UBL-SR-07, BR-56, BR-57, BR-CIUS-PT-21, BR-CIUS-PT-22, BR-CIUS-PT-23, BR-CIUS-PT-60, BR-17, BR-18, BR-19, BR-20",
  "decisao": "mapeado",
  "destino": "Projecao:FaturaCiusPt/obrigatorias",
  "nota": "'cada X tem Y': caminho obrigatório dentro de uma composição opcional ou repetível (vale em cada ocorrência presente)",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-schematron",
  "origem": "BR-16, BR-CO-18",
  "decisao": "mapeado",
  "destino": "HLM:DocumentoFaturacao/LinhaDocumento",
  "nota": "cardinalidade 1..* de LinhaDocumento e de DecomposicaoIva",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-schematron",
  "origem": "BR-CO-26, BR-AA-02, BR-AA-03, BR-AA-04, BR-S-02, BR-S-03, BR-S-04, BR-E-02, BR-E-03, BR-E-04",
  "decisao": "mapeado",
  "destino": "Projecao:FaturaCiusPt/Fornecedor.SujeitoPassivo.identificadorIva",
  "nota": "o CIUS-PT torna sempre obrigatório o identificador de IVA do fornecedor (BR-CIUS-PT-01), por isso estas regras ficam sempre cumpridas",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-schematron",
  "origem": "BR-CO-25",
  "decisao": "mapeado",
  "destino": "Regra:RIR-PAGAMENTO-PRAZO",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-schematron",
  "origem": "BR-AA-01, BR-S-01, BR-E-01, DT-CIUS-PT-176",
  "decisao": "mapeado",
  "destino": "Regra:RP-IVA-DECOMP",
  "nota": "DT-176 (um subtotal por motivo de isenção) fica a cargo da implementação da função",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-schematron",
  "origem": "DT-CIUS-PT-165",
  "decisao": "mapeado",
  "destino": "Regra:RP-TOT-COMIVA",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-schematron",
  "origem": "DT-CIUS-PT-163",
  "decisao": "mapeado",
  "destino": "Regra:RP-TOT-SEMIVA",
  "nota": "usa a soma das linhas (BT-106), que RP-SOMA-LINHAS liga a Σ BT-131",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-schematron",
  "origem": "DT-CIUS-PT-166",
  "decisao": "mapeado",
  "destino": "Regra:RP-TOT-PAGAR",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-schematron",
  "origem": "DT-CIUS-PT-160",
  "decisao": "mapeado",
  "destino": "Regra:RP-SOMA-LINHAS",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-schematron",
  "origem": "DT-CIUS-PT-161",
  "decisao": "mapeado",
  "destino": "Regra:RP-SOMA-DESCONTOS",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-schematron",
  "origem": "DT-CIUS-PT-162",
  "decisao": "mapeado",
  "destino": "Regra:RP-SOMA-ENCARGOS",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-schematron",
  "origem": "DT-CIUS-PT-164",
  "decisao": "mapeado",
  "destino": "Regra:RP-SOMA-IVA",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-schematron",
  "origem": "DT-CIUS-PT-171, DT-CIUS-PT-173, DT-CIUS-PT-175",
  "decisao": "mapeado",
  "destino": "Regra:RP-IVA-BASE",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-schematron",
  "origem": "DT-CIUS-PT-167, DT-CIUS-PT-172, DT-CIUS-PT-174",
  "decisao": "mapeado",
  "destino": "Regra:RP-DECOMP-IMPOSTO",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-schematron",
  "origem": "DT-CIUS-PT-157",
  "decisao": "mapeado",
  "destino": "Regra:RP-LIN-MONTANTE",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-schematron",
  "origem": "DT-CIUS-PT-158, DT-CIUS-PT-159, DT-CIUS-PT-168, DT-CIUS-PT-169",
  "decisao": "mapeado",
  "destino": "Regra:RP-DE-CALCULO",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-schematron",
  "origem": "DT-CIUS-PT-170",
  "decisao": "mapeado",
  "destino": "Regra:RP-PRECO-CALCULO",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-schematron",
  "origem": "BR-27, DT-CIUS-PT-127.1",
  "decisao": "mapeado",
  "destino": "Regra:RP-PRECO-LIQ",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-schematron",
  "origem": "BR-28, DT-CIUS-PT-129.1",
  "decisao": "mapeado",
  "destino": "Regra:RP-PRECO-BRUTO",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-schematron",
  "origem": "DT-CIUS-PT-128.1",
  "decisao": "mapeado",
  "destino": "Regra:RP-PRECO-DESC",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-schematron",
  "origem": "DT-CIUS-PT-177, DT-CIUS-PT-130.1",
  "decisao": "mapeado",
  "destino": "Regra:RP-PRECO-QBASE",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-schematron",
  "origem": "DT-CIUS-PT-130.2",
  "decisao": "mapeado",
  "destino": "Regra:RP-PRECO-UNIDADE",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-schematron",
  "origem": "BR-E-05, BR-E-06, BR-E-07, BR-CIUS-PT-16",
  "decisao": "mapeado",
  "destino": "Regra:RIR-IVA-TAXA-ISENTA",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-schematron",
  "origem": "BR-AA-05, BR-AA-06, BR-AA-07, BR-S-05, BR-S-06, BR-S-07, BR-CIUS-PT-12, BR-CIUS-PT-14",
  "decisao": "mapeado",
  "destino": "Regra:RIR-IVA-TAXA-POSITIVA",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-schematron",
  "origem": "BR-E-09",
  "decisao": "mapeado",
  "destino": "Regra:RIR-DECOMP-ISENTO",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-schematron",
  "origem": "BR-E-10",
  "decisao": "mapeado",
  "destino": "Regra:RIR-DECOMP-ISENCAO",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-schematron",
  "origem": "BR-S-10, BR-AA-10",
  "decisao": "mapeado",
  "destino": "Regra:RIR-DECOMP-SEM-ISENCAO",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-schematron",
  "origem": "BR-CIUS-PT-17, BR-CIUS-PT-18",
  "decisao": "mapeado",
  "destino": "Regra:RIR-LIN-ISENCAO",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-schematron",
  "origem": "BR-CIUS-PT-13, BR-CIUS-PT-15",
  "decisao": "mapeado",
  "destino": "Regra:RIR-LIN-SEM-ISENCAO",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-schematron",
  "origem": "BR-CO-03",
  "decisao": "mapeado",
  "destino": "Regra:RP-DOC-DATAIVA",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-schematron",
  "origem": "BR-29, BR-30",
  "decisao": "mapeado",
  "destino": "Regra:RP-PERIODO-ORDEM",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-schematron",
  "origem": "BR-CO-19, BR-CO-20",
  "decisao": "mapeado",
  "destino": "Regra:RP-PERIODO-DATA",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-schematron",
  "origem": "BR-33, BR-38, BR-42, BR-44, BR-CO-21, BR-CO-22, BR-CO-23, BR-CO-24",
  "decisao": "mapeado",
  "destino": "Regra:RP-DE-JUSTIFICADO",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-schematron",
  "origem": "BR-CIUS-PT-30",
  "decisao": "mapeado",
  "destino": "Regra:RP-SUP-CONTEUDO",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-schematron",
  "origem": "UBL-DT-06",
  "decisao": "mapeado",
  "destino": "Regra:RIR-SUP-MIME",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-schematron",
  "origem": "UBL-DT-07",
  "decisao": "mapeado",
  "destino": "Regra:RIR-SUP-FICHEIRO",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-schematron",
  "origem": "BR-CIUS-PT-64",
  "decisao": "mapeado",
  "destino": "Regra:RP-LENT-IDENT",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-schematron",
  "origem": "BR-CIUS-PT-66",
  "decisao": "mapeado",
  "destino": "Regra:RP-LENT-MORADA",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-schematron",
  "origem": "BR-CIUS-PT-25",
  "decisao": "mapeado",
  "destino": "Regra:RIR-REFANT-NC",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-schematron",
  "origem": "BR-CIUS-PT-65",
  "decisao": "mapeado",
  "destino": "Regra:RIR-REFANT-ND",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-schematron",
  "origem": "BR-CIUS-PT-62",
  "decisao": "mapeado",
  "destino": "Regra:RIR-TOT-DESCONTOS",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-schematron",
  "origem": "BR-CIUS-PT-63",
  "decisao": "mapeado",
  "destino": "Regra:RIR-TOT-ENCARGOS",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-schematron",
  "origem": "BR-61",
  "decisao": "mapeado",
  "destino": "Regra:RIR-PAG-IBAN",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-schematron",
  "origem": "DT-CIUS-PT-114.2",
  "decisao": "mapeado",
  "destino": "Regra:RP-LIN-UNICAS",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-schematron",
  "origem": "DT-CIUS-PT-001",
  "decisao": "mapeado",
  "destino": "Regra:RP-DOC-NUMERO",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-schematron",
  "origem": "DT-CIUS-PT-003_i, DT-CIUS-PT-003_cn",
  "decisao": "mapeado",
  "destino": "Regra:RP-DOC-TIPO",
  "nota": "reunião das duas listas; para a NC os valores 381/NC são fixados no perfil",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-schematron",
  "origem": "DT-CIUS-PT-151",
  "decisao": "mapeado",
  "destino": "Regra:RP-DOC-MOEDA",
  "nota": "lista ISO 4217 aproximada por padrão de 3 letras",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-schematron",
  "origem": "DT-CIUS-PT-152",
  "decisao": "mapeado",
  "destino": "Regra:RP-DOC-MOEDAIVA",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-schematron",
  "origem": "DT-CIUS-PT-007",
  "decisao": "mapeado",
  "destino": "Regra:RP-DOC-CODDATAIVA",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-schematron",
  "origem": "DT-CIUS-PT-009",
  "decisao": "mapeado",
  "destino": "Regra:RP-DOC-REFCLIENTE",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-schematron",
  "origem": "DT-CIUS-PT-010",
  "decisao": "mapeado",
  "destino": "Regra:RP-REF-PROJETO",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-schematron",
  "origem": "DT-CIUS-PT-011",
  "decisao": "mapeado",
  "destino": "Regra:RP-REF-CONTRATO",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-schematron",
  "origem": "DT-CIUS-PT-012",
  "decisao": "mapeado",
  "destino": "Regra:RP-REF-ENCOMENDA",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-schematron",
  "origem": "DT-CIUS-PT-013",
  "decisao": "mapeado",
  "destino": "Regra:RP-REF-ORDEMVENDA",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-schematron",
  "origem": "DT-CIUS-PT-014",
  "decisao": "mapeado",
  "destino": "Regra:RP-REF-RECECAO",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-schematron",
  "origem": "DT-CIUS-PT-015",
  "decisao": "mapeado",
  "destino": "Regra:RP-REF-ENVIO",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-schematron",
  "origem": "DT-CIUS-PT-016",
  "decisao": "mapeado",
  "destino": "Regra:RP-REF-ACORDO",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-schematron",
  "origem": "DT-CIUS-PT-017.1",
  "decisao": "mapeado",
  "destino": "Regra:RP-REF-PROCESSO",
  "nota": "também dá RP-SUP-REF (BT-122)",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-schematron",
  "origem": "DT-CIUS-PT-018",
  "decisao": "mapeado",
  "destino": "Regra:RP-DOC-COMPROMISSO",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-schematron",
  "origem": "DT-CIUS-PT-019",
  "decisao": "mapeado",
  "destino": "Regra:RP-DOC-CONDPAG",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-schematron",
  "origem": "DT-CIUS-PT-020",
  "decisao": "mapeado",
  "destino": "Regra:RP-NOTA-TEXTO",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-schematron",
  "origem": "DT-CIUS-PT-021",
  "decisao": "mapeado",
  "destino": "Regra:RP-DOC-PROCESSO",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-schematron",
  "origem": "DT-CIUS-PT-022",
  "decisao": "mapeado",
  "destino": "Regra:RP-DOC-ESPEC",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-schematron",
  "origem": "DT-CIUS-PT-023",
  "decisao": "mapeado",
  "destino": "Regra:RP-REFDOC-NUMERO",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-schematron",
  "origem": "DT-CIUS-PT-025, DT-CIUS-PT-042, DT-CIUS-PT-057, DT-CIUS-PT-060",
  "decisao": "mapeado",
  "destino": "Regra:RP-SP-NOME",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-schematron",
  "origem": "DT-CIUS-PT-026, DT-CIUS-PT-043",
  "decisao": "mapeado",
  "destino": "Regra:RP-SP-NOMECOM",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-schematron",
  "origem": "DT-CIUS-PT-027.1, DT-CIUS-PT-044.1, DT-CIUS-PT-058.1",
  "decisao": "mapeado",
  "destino": "Regra:RP-SP-IDENT",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-schematron",
  "origem": "DT-CIUS-PT-028.1, DT-CIUS-PT-045.1, DT-CIUS-PT-059.1",
  "decisao": "mapeado",
  "destino": "Regra:RP-SP-REGISTO",
  "nota": "BT-47/BT-61 admitem 50; ficou o máximo comum de 200",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-schematron",
  "origem": "DT-CIUS-PT-029, DT-CIUS-PT-046.1, DT-CIUS-PT-046.2, DT-CIUS-PT-061.1, DT-CIUS-PT-061.2",
  "decisao": "mapeado",
  "destino": "Regra:RP-SP-IVA",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-schematron",
  "origem": "DT-CIUS-PT-030",
  "decisao": "mapeado",
  "destino": "Regra:RP-FORN-REGFISCAL",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-schematron",
  "origem": "DT-CIUS-PT-031",
  "decisao": "mapeado",
  "destino": "Regra:RP-FORN-CAPITAL",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-schematron",
  "origem": "DT-CIUS-PT-032.1",
  "decisao": "mapeado",
  "destino": "Regra:RP-FORN-ENDELET",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-schematron",
  "origem": "DT-CIUS-PT-039",
  "decisao": "mapeado",
  "destino": "Regra:RP-FORN-CONTACTO",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-schematron",
  "origem": "DT-CIUS-PT-047.1",
  "decisao": "mapeado",
  "destino": "Regra:RP-ADQ-ENDELET",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-schematron",
  "origem": "DT-CIUS-PT-054",
  "decisao": "mapeado",
  "destino": "Regra:RP-ADQ-CONTACTO",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-schematron",
  "origem": "DT-CIUS-PT-034, DT-CIUS-PT-049, DT-CIUS-PT-063, DT-CIUS-PT-074",
  "decisao": "mapeado",
  "destino": "Regra:RP-CMOR-LINHA2",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-schematron",
  "origem": "DT-CIUS-PT-035, DT-CIUS-PT-050, DT-CIUS-PT-064, DT-CIUS-PT-075",
  "decisao": "mapeado",
  "destino": "Regra:RP-CMOR-LINHA3",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-schematron",
  "origem": "DT-CIUS-PT-038, DT-CIUS-PT-053, DT-CIUS-PT-067, DT-CIUS-PT-078",
  "decisao": "mapeado",
  "destino": "Regra:RP-CMOR-REGIAO",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-schematron",
  "origem": "DT-CIUS-PT-040, DT-CIUS-PT-055",
  "decisao": "mapeado",
  "destino": "Regra:RP-TELEFONE",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-schematron",
  "origem": "DT-CIUS-PT-068",
  "decisao": "mapeado",
  "destino": "Regra:RP-LENT-NOME",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-schematron",
  "origem": "DT-CIUS-PT-069.1",
  "decisao": "mapeado",
  "destino": "Regra:RP-LENT-IDLOCAL",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-schematron",
  "origem": "DT-CIUS-PT-079.2",
  "decisao": "mapeado",
  "destino": "Regra:RP-PAG-MEIO",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-schematron",
  "origem": "DT-CIUS-PT-079.3",
  "decisao": "mapeado",
  "destino": "Regra:RP-PAG-DETALHE",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-schematron",
  "origem": "DT-CIUS-PT-080",
  "decisao": "mapeado",
  "destino": "Regra:RP-PAG-REF",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-schematron",
  "origem": "DT-CIUS-PT-081",
  "decisao": "mapeado",
  "destino": "Regra:RP-CONTA-IBAN",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-schematron",
  "origem": "DT-CIUS-PT-082",
  "decisao": "mapeado",
  "destino": "Regra:RP-CONTA-NOME",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-schematron",
  "origem": "DT-CIUS-PT-083",
  "decisao": "mapeado",
  "destino": "Regra:RP-CONTA-BIC",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-schematron",
  "origem": "DT-CIUS-PT-084.1",
  "decisao": "mapeado",
  "destino": "Regra:RP-CARTAO-PAN",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-schematron",
  "origem": "DT-CIUS-PT-085",
  "decisao": "mapeado",
  "destino": "Regra:RP-CARTAO-TITULAR",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-schematron",
  "origem": "DT-CIUS-PT-086",
  "decisao": "mapeado",
  "destino": "Regra:RP-DD-MANDATO",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-schematron",
  "origem": "DT-CIUS-PT-087",
  "decisao": "mapeado",
  "destino": "Regra:RP-DD-CONTA",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-schematron",
  "origem": "DT-CIUS-PT-088.1, DT-CIUS-PT-123.1",
  "decisao": "mapeado",
  "destino": "Regra:RP-DE-MONTANTE",
  "nota": "o padrão sem sinal significa montante não negativo; as casas decimais ficam para a serialização",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-schematron",
  "origem": "DT-CIUS-PT-089.1, DT-CIUS-PT-124.1",
  "decisao": "mapeado",
  "destino": "Regra:RP-DE-BASE",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-schematron",
  "origem": "DT-CIUS-PT-090.1, DT-CIUS-PT-090.2, DT-CIUS-PT-125.1, DT-CIUS-PT-125.2",
  "decisao": "mapeado",
  "destino": "Regra:RP-DE-PERC",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-schematron",
  "origem": "DT-CIUS-PT-093, DT-CIUS-PT-126",
  "decisao": "mapeado",
  "destino": "Regra:RP-DE-MOTIVO",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-schematron",
  "origem": "DT-CIUS-PT-147, DT-CIUS-PT-148, DT-CIUS-PT-149, DT-CIUS-PT-150",
  "decisao": "mapeado",
  "destino": "Regra:RP-DE-CODMOTIVO",
  "nota": "as listas UNCL 5189/7161 ficaram aproximadas por um padrão: o USM não distingue desconto de encargo (isso é o papel)",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-schematron",
  "origem": "DT-CIUS-PT-091, DT-CIUS-PT-105, DT-CIUS-PT-131",
  "decisao": "mapeado",
  "destino": "Regra:RP-IVA-CATEGORIA",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-schematron",
  "origem": "DT-CIUS-PT-092.1, DT-CIUS-PT-092.2, DT-CIUS-PT-106.1, DT-CIUS-PT-106.2, DT-CIUS-PT-132.1, DT-CIUS-PT-132.2",
  "decisao": "mapeado",
  "destino": "Regra:RP-IVA-TAXA",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-schematron",
  "origem": "DT-CIUS-PT-107",
  "decisao": "mapeado",
  "destino": "Regra:RP-IVA-MOTIVO",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-schematron",
  "origem": "DT-CIUS-PT-108",
  "decisao": "mapeado",
  "destino": "Regra:RP-IVA-CODMOTIVO",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-schematron",
  "origem": "DT-CIUS-PT-095.1",
  "decisao": "mapeado",
  "destino": "Regra:RP-TOT-DESC-POS",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-schematron",
  "origem": "DT-CIUS-PT-096.1",
  "decisao": "mapeado",
  "destino": "Regra:RP-TOT-ENC-POS",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-schematron",
  "origem": "DT-CIUS-PT-097.1",
  "decisao": "mapeado",
  "destino": "Regra:RP-TOT-SEMIVA-POS",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-schematron",
  "origem": "DT-CIUS-PT-099.1",
  "decisao": "mapeado",
  "destino": "Regra:RP-TOT-COMIVA-POS",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-schematron",
  "origem": "DT-CIUS-PT-100.1",
  "decisao": "mapeado",
  "destino": "Regra:RP-TOT-PAGO-POS",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-schematron",
  "origem": "DT-CIUS-PT-102.1",
  "decisao": "mapeado",
  "destino": "Regra:RP-TOT-PAGAR-POS",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-schematron",
  "origem": "DT-CIUS-PT-109",
  "decisao": "mapeado",
  "destino": "Regra:RP-SUP-DESC",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-schematron",
  "origem": "DT-CIUS-PT-110",
  "decisao": "mapeado",
  "destino": "Regra:RP-SUP-URI",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-schematron",
  "origem": "DT-CIUS-PT-111.1, DT-CIUS-PT-111.2",
  "decisao": "mapeado",
  "destino": "Regra:RP-SUP-ANEXO",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-schematron",
  "origem": "DT-CIUS-PT-112",
  "decisao": "mapeado",
  "destino": "Regra:RP-SUP-MIME",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-schematron",
  "origem": "DT-CIUS-PT-113",
  "decisao": "mapeado",
  "destino": "Regra:RP-SUP-FICHEIRO",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-schematron",
  "origem": "DT-CIUS-PT-114.1",
  "decisao": "mapeado",
  "destino": "Regra:RP-LIN-ID",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-schematron",
  "origem": "DT-CIUS-PT-115",
  "decisao": "mapeado",
  "destino": "Regra:RP-LIN-NOTA",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-schematron",
  "origem": "DT-CIUS-PT-116.1",
  "decisao": "mapeado",
  "destino": "Regra:RP-LIN-OBJETO",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-schematron",
  "origem": "DT-CIUS-PT-143",
  "decisao": "mapeado",
  "destino": "Regra:RP-LIN-UNIDADE",
  "nota": "lista UN/ECE Rec. 20 aproximada por padrão",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-schematron",
  "origem": "DT-CIUS-PT-119",
  "decisao": "mapeado",
  "destino": "Regra:RP-LIN-REFENC",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-schematron",
  "origem": "DT-CIUS-PT-120",
  "decisao": "mapeado",
  "destino": "Regra:RP-LIN-COMPROMISSO",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-schematron",
  "origem": "DT-CIUS-PT-133",
  "decisao": "mapeado",
  "destino": "Regra:RP-ART-NOME",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-schematron",
  "origem": "DT-CIUS-PT-134",
  "decisao": "mapeado",
  "destino": "Regra:RP-ART-DESC",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-schematron",
  "origem": "DT-CIUS-PT-135",
  "decisao": "mapeado",
  "destino": "Regra:RP-ART-CODIGO",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-schematron",
  "origem": "DT-CIUS-PT-136",
  "decisao": "mapeado",
  "destino": "Regra:RP-ART-CODCOMP",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-schematron",
  "origem": "DT-CIUS-PT-137.1",
  "decisao": "mapeado",
  "destino": "Regra:RP-ART-CODBARRAS",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-schematron",
  "origem": "DT-CIUS-PT-138.1",
  "decisao": "mapeado",
  "destino": "Regra:RP-ART-CLASSIF",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-schematron",
  "origem": "DT-CIUS-PT-146",
  "decisao": "mapeado",
  "destino": "Regra:RP-ART-PAIS",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-schematron",
  "origem": "DT-CIUS-PT-139",
  "decisao": "mapeado",
  "destino": "Regra:RP-ATRIB-NOME",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-schematron",
  "origem": "DT-CIUS-PT-140",
  "decisao": "mapeado",
  "destino": "Regra:RP-ATRIB-VALOR",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-schematron",
  "origem": "DT-CIUS-PT-002, DT-CIUS-PT-006, DT-CIUS-PT-008, DT-CIUS-PT-024, DT-CIUS-PT-070, DT-CIUS-PT-071, DT-CIUS-PT-072, DT-CIUS-PT-121, DT-CIUS-PT-122",
  "decisao": "descartado",
  "motivo": "o formato AAAA-MM-DD já é garantido pelo tipo base data",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-schematron",
  "origem": "DT-CIUS-PT-094.1, DT-CIUS-PT-098.1, DT-CIUS-PT-101.1, DT-CIUS-PT-103.1, DT-CIUS-PT-104.1, DT-CIUS-PT-117.1, DT-CIUS-PT-118.1",
  "decisao": "descartado",
  "motivo": "o número de casas decimais e de dígitos é da representação na serialização, não do valor; admitem valores negativos",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-schematron",
  "origem": "DT-CIUS-PT-088.2, 089.2, 094.2, 095.2, 096.2, 097.2, 098.2, 098.3, 099.2, 100.2, 101.2, 102.2, 103.2, 104.2, 104.3, 118.2, 123.2, 124.2, 127.2, 128.2, 129.2",
  "decisao": "descartado",
  "motivo": "atributo currencyID da sintaxe UBL; no modelo semântico todos os montantes estão na moeda do documento (CabecalhoDocumento.moeda) ou na moeda do IVA",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-schematron",
  "origem": "DT-CIUS-PT-017.2, 027.2, 028.2, 032.2, 044.2, 045.2, 047.2, 058.2, 059.2, 069.2, 116.2, 137.2, 138.2, 138.3, 153, 154, 155, 156, 084.2; BR-62, BR-63, BR-64, BR-65; BR-CIUS-PT-02, 04, 08, 09, 19, 20",
  "decisao": "descartado",
  "motivo": "atributos de esquema e de regime fiscal da sintaxe UBL (schemeID, listID, TaxScheme = VAT, NetworkID, DocumentTypeCode 130), que não estão no modelo semântico",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-schematron",
  "origem": "DT-CIUS-PT-033, 036, 037, 048, 051, 052, 062, 065, 066, 073, 076, 077, 141, 142, 144, 145, 041, 056",
  "decisao": "descartado",
  "motivo": "comprimentos e código de país de Morada e de Contacto, que são USM reutilizados: as regras deles (RP-PAIS, RP-CP, RP-EMAIL…) já se aplicam e não se acrescentam regras a um modelo partilhado",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-schematron",
  "origem": "DT-CIUS-PT-020_2.1 a DT-CIUS-PT-020_15.6 (todas as DT-CIUS-PT-020_*), DT-CIUS-PT-079.1, DT-CIUS-PT-079.4",
  "decisao": "descartado",
  "motivo": "informação estruturada codificada em notas e atributos com prefixos #…# (câmbio, retenção na fonte, pagamento ATM, programa certificado AT); é uma convenção sintática e não está no modelo semântico do guia",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-schematron",
  "origem": "DT-CIUS-PT-139_1, DT-CIUS-PT-139_2, DT-CIUS-PT-139_3, DT-CIUS-PT-139_5",
  "decisao": "descartado",
  "motivo": "convenções #…# do BT-160; o motivo de isenção por linha está modelado em LinhaDocumento.CategoriaIva",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-schematron",
  "origem": "BR-CIUS-PT-24, 26, 27, 28, 29, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 59, 61",
  "decisao": "descartado",
  "motivo": "proíbem elementos UBL vazios ('shall be filled'); no modelo semântico uma propriedade ausente simplesmente não existe",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-schematron",
  "origem": "BR-CO-07, BR-CO-08",
  "decisao": "descartado",
  "motivo": "expressão true(): não verificável",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-schematron",
  "origem": "BR-CIUS-PT-58",
  "decisao": "descartado",
  "motivo": "o modelo só tem desconto sobre o preço; um encargo sobre o preço não tem lugar onde ser declarado",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-schematron",
  "origem": "UBL-CR-001 a UBL-CR-647 (todas as UBL-CR-*)",
  "decisao": "descartado",
  "motivo": "excluem elementos UBL não usados; a exclusão já resulta da projeção (o que não se declara fica excluído)",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-schematron",
  "origem": "UBL-DT-08 a UBL-DT-26",
  "decisao": "descartado",
  "motivo": "atributos da sintaxe UBL que não devem aparecer; não fazem parte do modelo semântico",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-schematron",
  "origem": "UBL-SR-01 a UBL-SR-40 (exceto UBL-SR-07)",
  "decisao": "descartado",
  "motivo": "'no máximo uma ocorrência': já garantido por propriedades simples e composições 0..1; UBL-SR-19/20/21 são avisos sobre o recebedor diferente do fornecedor",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-ubl-fatura",
  "origem": "/Invoice/* (todos os elementos com BT correspondente no guia)",
  "decisao": "fundido",
  "destino": "HLM:DocumentoFaturacao",
  "nota": "fonte complementar: usada para confirmar cardinalidades e descrições; cada elemento é o BT do guia com o mesmo significado",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-ubl-fatura",
  "origem": "/Invoice/*/TaxScheme/ID, /Invoice/PaymentMeans/CardAccount/NetworkID, /Invoice/AdditionalDocumentReference/DocumentTypeCode",
  "decisao": "descartado",
  "motivo": "constantes ou qualificadores da sintaxe UBL",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-ubl-fatura",
  "origem": "/Invoice/AllowanceCharge/ChargeIndicator, /Invoice/InvoiceLine/AllowanceCharge/ChargeIndicator, /Invoice/InvoiceLine/Price/AllowanceCharge/ChargeIndicator",
  "decisao": "descartado",
  "motivo": "a distinção entre desconto e encargo é dada pelo papel da composição (Desconto, Encargo)",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-ubl-nota-de-credito",
  "origem": "/CreditNote/* (todos os elementos com BT correspondente no guia)",
  "decisao": "fundido",
  "destino": "HLM:DocumentoFaturacao",
  "nota": "fonte complementar; CreditedQuantity = BT-129, PaymentMeans/PaymentDueDate = BT-9",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-ubl-nota-de-credito",
  "origem": "/CreditNote/*/TaxScheme/ID, /CreditNote/PaymentMeans/CardAccount/NetworkID, /CreditNote/AdditionalDocumentReference/DocumentTypeCode, /CreditNote/*/AllowanceCharge/ChargeIndicator",
  "decisao": "descartado",
  "motivo": "constantes ou qualificadores da sintaxe UBL; o desconto ou encargo é dado pelo papel",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-ubl-mensagem-de-estado",
  "origem": "/DocumentStatus/CustomizationID",
  "decisao": "mapeado",
  "destino": "HLM:MensagemEstado/CabecalhoMensagem.identificadorEspecificacao",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-ubl-mensagem-de-estado",
  "origem": "/DocumentStatus/ID",
  "decisao": "mapeado",
  "destino": "HLM:MensagemEstado/CabecalhoMensagem.numero",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-ubl-mensagem-de-estado",
  "origem": "/DocumentStatus/IssueDate",
  "decisao": "mapeado",
  "destino": "HLM:MensagemEstado/CabecalhoMensagem.dataEmissao",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-ubl-mensagem-de-estado",
  "origem": "/DocumentStatus/IssueTime",
  "decisao": "mapeado",
  "destino": "HLM:MensagemEstado/CabecalhoMensagem.horaEmissao",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-ubl-mensagem-de-estado",
  "origem": "/DocumentStatus/Note",
  "decisao": "mapeado",
  "destino": "HLM:MensagemEstado/CabecalhoMensagem.nota",
  "nota": "1..* na fonte; simplificado a um texto",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-ubl-mensagem-de-estado",
  "origem": "/DocumentStatus/SenderParty/PartyName/Name",
  "decisao": "mapeado",
  "destino": "HLM:MensagemEstado/Emissor.SujeitoPassivo.nomeComercial",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-ubl-mensagem-de-estado",
  "origem": "/DocumentStatus/SenderParty/PostalAddress/Country/IdentificationCode",
  "decisao": "mapeado",
  "destino": "HLM:MensagemEstado/Emissor.Morada.pais",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-ubl-mensagem-de-estado",
  "origem": "/DocumentStatus/SenderParty/PartyTaxScheme/CompanyID",
  "decisao": "mapeado",
  "destino": "HLM:MensagemEstado/Emissor.SujeitoPassivo.identificadorIva",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-ubl-mensagem-de-estado",
  "origem": "/DocumentStatus/SenderParty/PartyLegalEntity/RegistrationName",
  "decisao": "mapeado",
  "destino": "HLM:MensagemEstado/Emissor.SujeitoPassivo.nome",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-ubl-mensagem-de-estado",
  "origem": "/DocumentStatus/SenderParty/PartyLegalEntity/CompanyID",
  "decisao": "mapeado",
  "destino": "HLM:MensagemEstado/Emissor.SujeitoPassivo.identificadorRegisto",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-ubl-mensagem-de-estado",
  "origem": "/DocumentStatus/SenderParty/Contact/ElectronicMail",
  "decisao": "mapeado",
  "destino": "HLM:MensagemEstado/Emissor.Contacto.email",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-ubl-mensagem-de-estado",
  "origem": "/DocumentStatus/ReceiverParty/PartyName/Name",
  "decisao": "mapeado",
  "destino": "HLM:MensagemEstado/Recetor.SujeitoPassivo.nomeComercial",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-ubl-mensagem-de-estado",
  "origem": "/DocumentStatus/ReceiverParty/PostalAddress/Country/IdentificationCode",
  "decisao": "mapeado",
  "destino": "HLM:MensagemEstado/Recetor.Morada.pais",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-ubl-mensagem-de-estado",
  "origem": "/DocumentStatus/ReceiverParty/PartyTaxScheme/CompanyID",
  "decisao": "mapeado",
  "destino": "HLM:MensagemEstado/Recetor.SujeitoPassivo.identificadorIva",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-ubl-mensagem-de-estado",
  "origem": "/DocumentStatus/ReceiverParty/PartyLegalEntity/RegistrationName",
  "decisao": "mapeado",
  "destino": "HLM:MensagemEstado/Recetor.SujeitoPassivo.nome",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-ubl-mensagem-de-estado",
  "origem": "/DocumentStatus/ReceiverParty/PartyLegalEntity/CompanyID",
  "decisao": "mapeado",
  "destino": "HLM:MensagemEstado/Recetor.SujeitoPassivo.identificadorRegisto",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-ubl-mensagem-de-estado",
  "origem": "/DocumentStatus/ReceiverParty/Contact/ElectronicMail",
  "decisao": "mapeado",
  "destino": "HLM:MensagemEstado/Recetor.Contacto.email",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-ubl-mensagem-de-estado",
  "origem": "/DocumentStatus/SenderParty/PartyTaxScheme/TaxScheme/ID, /DocumentStatus/ReceiverParty/PartyTaxScheme/TaxScheme/ID",
  "decisao": "descartado",
  "motivo": "constante VAT da sintaxe UBL",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-ubl-mensagem-de-estado",
  "origem": "/DocumentStatus/DocumentResponse/Response/ResponseCode",
  "decisao": "mapeado",
  "destino": "HLM:MensagemEstado/RespostaDocumento.codigoResposta",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-ubl-mensagem-de-estado",
  "origem": "/DocumentStatus/DocumentResponse/Response/Description",
  "decisao": "mapeado",
  "destino": "HLM:MensagemEstado/RespostaDocumento.descricaoResposta",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-ubl-mensagem-de-estado",
  "origem": "/DocumentStatus/DocumentResponse/DocumentReference/ID",
  "decisao": "mapeado",
  "destino": "HLM:MensagemEstado/RespostaDocumento.ReferenciaDocumento.numero",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-ubl-mensagem-de-estado",
  "origem": "/DocumentStatus/DocumentResponse/DocumentReference/UUID",
  "decisao": "mapeado",
  "destino": "HLM:MensagemEstado/RespostaDocumento.uuidDocumento",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-ubl-mensagem-de-estado",
  "origem": "/DocumentStatus/DocumentResponse/DocumentReference/IssueDate",
  "decisao": "mapeado",
  "destino": "HLM:MensagemEstado/RespostaDocumento.ReferenciaDocumento.dataEmissao",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-ubl-mensagem-de-estado",
  "origem": "/DocumentStatus/DocumentResponse/DocumentReference/DocumentTypeCode",
  "decisao": "mapeado",
  "destino": "HLM:MensagemEstado/RespostaDocumento.tipoDocumento",
  "passo": "G"
 },
 {
  "fonte": "cius-pt-ubl-mensagem-de-estado",
  "origem": "/DocumentStatus/DocumentResponse/DocumentReference/DocumentStatusCode",
  "decisao": "mapeado",
  "destino": "HLM:MensagemEstado/RespostaDocumento.estadoDocumento",
  "passo": "G"
 },
 {
  "fonte": "fm-dart",
  "origem": "Article.internalId, BaseEntity.fields, Client.internalId, Delivery.internalId, DeliveryConfirmation.internalId, DeliveryItem.internalId, Seller.internalId, Zone.internalId, FileInfo.file",
  "decisao": "descartado",
  "motivo": "identificadores técnicos ou objetos internos da aplicação",
  "passo": "G"
 },
 {
  "fonte": "fm-dart",
  "origem": "Article.registrationDate",
  "decisao": "mapeado",
  "destino": "HLM:ExportacaoFm/ArtigoStock.dataRegisto",
  "passo": "G"
 },
 {
  "fonte": "fm-dart",
  "origem": "Article.code",
  "decisao": "mapeado",
  "destino": "HLM:ExportacaoFm/ArtigoStock.Artigo.codigo",
  "passo": "G"
 },
 {
  "fonte": "fm-dart",
  "origem": "Article.articleCode",
  "decisao": "mapeado",
  "destino": "HLM:ExportacaoFm/ArtigoStock.codigoAuxiliar",
  "nota": "dúvida: pode ser o código auxiliar do STK",
  "passo": "G"
 },
 {
  "fonte": "fm-dart",
  "origem": "Article.barCode",
  "decisao": "mapeado",
  "destino": "HLM:ExportacaoFm/ArtigoStock.Artigo.codigoBarras",
  "passo": "G"
 },
 {
  "fonte": "fm-dart",
  "origem": "Article.description",
  "decisao": "mapeado",
  "destino": "HLM:ExportacaoFm/ArtigoStock.Artigo.nome",
  "passo": "G"
 },
 {
  "fonte": "fm-dart",
  "origem": "Article.reference",
  "decisao": "mapeado",
  "destino": "HLM:ExportacaoFm/ArtigoStock.referencia",
  "passo": "G"
 },
 {
  "fonte": "fm-dart",
  "origem": "Article.artForm",
  "decisao": "mapeado",
  "destino": "HLM:ExportacaoFm/ArtigoStock.formaArtigo",
  "passo": "G"
 },
 {
  "fonte": "fm-dart",
  "origem": "Article.supplier",
  "decisao": "mapeado",
  "destino": "HLM:ExportacaoFm/ArtigoStock.nomeFornecedor",
  "passo": "G"
 },
 {
  "fonte": "fm-dart",
  "origem": "Article.unit",
  "decisao": "mapeado",
  "destino": "HLM:ExportacaoFm/ArtigoStock.unidadeMedida",
  "passo": "G"
 },
 {
  "fonte": "fm-dart",
  "origem": "Article.saleIva",
  "decisao": "mapeado",
  "destino": "HLM:ExportacaoFm/ArtigoStock.taxaIva",
  "passo": "G"
 },
 {
  "fonte": "fm-dart",
  "origem": "Article.ecoTaxa",
  "decisao": "mapeado",
  "destino": "HLM:ExportacaoFm/ArtigoStock.ecoTaxa",
  "passo": "G"
 },
 {
  "fonte": "fm-dart",
  "origem": "Article.costPrice",
  "decisao": "mapeado",
  "destino": "HLM:ExportacaoFm/ArtigoStock.precoCusto",
  "passo": "G"
 },
 {
  "fonte": "fm-dart",
  "origem": "Article.costDiscount",
  "decisao": "mapeado",
  "destino": "HLM:ExportacaoFm/ArtigoStock.descontoCusto",
  "passo": "G"
 },
 {
  "fonte": "fm-dart",
  "origem": "Article.salePrice",
  "decisao": "mapeado",
  "destino": "HLM:ExportacaoFm/ArtigoStock.precoVendaComIva",
  "nota": "dúvida: confirmar se é com ou sem IVA",
  "passo": "G"
 },
 {
  "fonte": "fm-dart",
  "origem": "Article.ppPrice",
  "decisao": "mapeado",
  "destino": "HLM:ExportacaoFm/ArtigoStock.precoPublico",
  "passo": "G"
 },
 {
  "fonte": "fm-dart",
  "origem": "Article.isCar",
  "decisao": "mapeado",
  "destino": "HLM:ExportacaoFm/ArtigoStock.emVeiculo",
  "passo": "G"
 },
 {
  "fonte": "fm-dart",
  "origem": "Article.observations",
  "decisao": "mapeado",
  "destino": "HLM:ExportacaoFm/ArtigoStock.observacoes",
  "passo": "G"
 },
 {
  "fonte": "fm-dart",
  "origem": "Article.discount2",
  "decisao": "mapeado",
  "destino": "HLM:ExportacaoFm/ArtigoStock.desconto2",
  "passo": "G"
 },
 {
  "fonte": "fm-dart",
  "origem": "Article.weight",
  "decisao": "mapeado",
  "destino": "HLM:ExportacaoFm/ArtigoStock.peso",
  "passo": "G"
 },
 {
  "fonte": "fm-dart",
  "origem": "Article.familyCode",
  "decisao": "mapeado",
  "destino": "HLM:ExportacaoFm/ArtigoStock.codigoFamilia",
  "passo": "G"
 },
 {
  "fonte": "fm-dart",
  "origem": "Article.costPriceNoIva",
  "decisao": "mapeado",
  "destino": "HLM:ExportacaoFm/ArtigoStock.precoCustoSemIva",
  "passo": "G"
 },
 {
  "fonte": "fm-dart",
  "origem": "Article.costPriceWithIva",
  "decisao": "mapeado",
  "destino": "HLM:ExportacaoFm/ArtigoStock.precoCustoComIva",
  "passo": "G"
 },
 {
  "fonte": "fm-dart",
  "origem": "Article.supplierCode",
  "decisao": "mapeado",
  "destino": "HLM:ExportacaoFm/ArtigoStock.codigoFornecedor",
  "passo": "G"
 },
 {
  "fonte": "fm-dart",
  "origem": "Article.familyDescription",
  "decisao": "mapeado",
  "destino": "HLM:ExportacaoFm/ArtigoStock.descricaoFamilia",
  "passo": "G"
 },
 {
  "fonte": "fm-dart",
  "origem": "Article.costPriceNoIva2",
  "decisao": "mapeado",
  "destino": "HLM:ExportacaoFm/ArtigoStock.precoCusto2SemIva",
  "passo": "G"
 },
 {
  "fonte": "fm-dart",
  "origem": "Article.costPriceWithIva2",
  "decisao": "mapeado",
  "destino": "HLM:ExportacaoFm/ArtigoStock.precoCusto2ComIva",
  "passo": "G"
 },
 {
  "fonte": "fm-dart",
  "origem": "Article.service",
  "decisao": "mapeado",
  "destino": "HLM:ExportacaoFm/ArtigoStock.servico",
  "nota": "String na fonte, booleano no STK; ficou booleano",
  "passo": "G"
 },
 {
  "fonte": "fm-dart",
  "origem": "Article.carRegistration",
  "decisao": "mapeado",
  "destino": "HLM:ExportacaoFm/ArtigoStock.matriculaVeiculo",
  "passo": "G"
 },
 {
  "fonte": "fm-dart",
  "origem": "Article.stockQuantity",
  "decisao": "mapeado",
  "destino": "HLM:ExportacaoFm/ArtigoStock.quantidadeStock",
  "passo": "G"
 },
 {
  "fonte": "fm-dart",
  "origem": "Article.stockOutQuantity",
  "decisao": "mapeado",
  "destino": "HLM:ExportacaoFm/ArtigoStock.quantidadeStockFora",
  "passo": "G"
 },
 {
  "fonte": "fm-dart",
  "origem": "Article.carQuantityTotal",
  "decisao": "fundido",
  "destino": "HLM:ExportacaoFm/ProdutoVeiculo.quantidadeTotal",
  "passo": "G"
 },
 {
  "fonte": "fm-dart",
  "origem": "Article.carQuantityNormal",
  "decisao": "fundido",
  "destino": "HLM:ExportacaoFm/ProdutoVeiculo.quantidadeNormal",
  "passo": "G"
 },
 {
  "fonte": "fm-dart",
  "origem": "Article.carQuantityOut",
  "decisao": "fundido",
  "destino": "HLM:ExportacaoFm/ProdutoVeiculo.quantidadeFora",
  "passo": "G"
 },
 {
  "fonte": "fm-dart",
  "origem": "Client.registrationDate",
  "decisao": "mapeado",
  "destino": "HLM:ExportacaoFm/ClienteVenda.dataRegisto",
  "passo": "G"
 },
 {
  "fonte": "fm-dart",
  "origem": "Client.code",
  "decisao": "mapeado",
  "destino": "HLM:ExportacaoFm/ClienteVenda.codigo",
  "passo": "G"
 },
 {
  "fonte": "fm-dart",
  "origem": "Client.name",
  "decisao": "mapeado",
  "destino": "HLM:ExportacaoFm/ClienteVenda.Entidade.nome",
  "passo": "G"
 },
 {
  "fonte": "fm-dart",
  "origem": "Client.address",
  "decisao": "mapeado",
  "destino": "HLM:ExportacaoFm/ClienteVenda.Morada.rua",
  "passo": "G"
 },
 {
  "fonte": "fm-dart",
  "origem": "Client.city",
  "decisao": "mapeado",
  "destino": "HLM:ExportacaoFm/ClienteVenda.Morada.localidade",
  "passo": "G"
 },
 {
  "fonte": "fm-dart",
  "origem": "Client.zipCode",
  "decisao": "mapeado",
  "destino": "HLM:ExportacaoFm/ClienteVenda.Morada.codigoPostal",
  "passo": "G"
 },
 {
  "fonte": "fm-dart",
  "origem": "Client.zipCodeLoc",
  "decisao": "mapeado",
  "destino": "HLM:ExportacaoFm/ClienteVenda.designacaoPostal",
  "passo": "G"
 },
 {
  "fonte": "fm-dart",
  "origem": "Client.nif",
  "decisao": "mapeado",
  "destino": "HLM:ExportacaoFm/ClienteVenda.Entidade.nif",
  "passo": "G"
 },
 {
  "fonte": "fm-dart",
  "origem": "Client.phoneNumber",
  "decisao": "mapeado",
  "destino": "HLM:ExportacaoFm/ClienteVenda.ContactoTelefonico.telemovel",
  "passo": "G"
 },
 {
  "fonte": "fm-dart",
  "origem": "Client.zone",
  "decisao": "mapeado",
  "destino": "HLM:ExportacaoFm/ClienteVenda.zona",
  "passo": "G"
 },
 {
  "fonte": "fm-dart",
  "origem": "Client.chargeLocation",
  "decisao": "mapeado",
  "destino": "HLM:ExportacaoFm/ClienteVenda.localCobranca",
  "passo": "G"
 },
 {
  "fonte": "fm-dart",
  "origem": "Client.email",
  "decisao": "mapeado",
  "destino": "HLM:ExportacaoFm/ClienteVenda.Contacto.email",
  "passo": "G"
 },
 {
  "fonte": "fm-dart",
  "origem": "Client.notes",
  "decisao": "mapeado",
  "destino": "HLM:ExportacaoFm/ClienteVenda.observacoes",
  "passo": "G"
 },
 {
  "fonte": "fm-dart",
  "origem": "Client.fixePhoneNumber",
  "decisao": "mapeado",
  "destino": "HLM:ExportacaoFm/ClienteVenda.ContactoTelefonico.telefone",
  "passo": "G"
 },
 {
  "fonte": "fm-dart",
  "origem": "Client.sellerCode",
  "decisao": "mapeado",
  "destino": "HLM:ExportacaoFm/ClienteVenda.codigoVendedor",
  "passo": "G"
 },
 {
  "fonte": "fm-dart",
  "origem": "Client.orderNumber",
  "decisao": "mapeado",
  "destino": "HLM:ExportacaoFm/ClienteVenda.numeroOrdem",
  "passo": "G"
 },
 {
  "fonte": "fm-dart",
  "origem": "Client.dateOfBirth",
  "decisao": "mapeado",
  "destino": "HLM:ExportacaoFm/ClienteVenda.dataNascimento",
  "passo": "G"
 },
 {
  "fonte": "fm-dart",
  "origem": "Client.citizenCard",
  "decisao": "mapeado",
  "destino": "HLM:ExportacaoFm/ClienteVenda.CartaoCidadao.numero",
  "passo": "G"
 },
 {
  "fonte": "fm-dart",
  "origem": "Client.citizenCardExpirationDate",
  "decisao": "mapeado",
  "destino": "HLM:ExportacaoFm/ClienteVenda.CartaoCidadao.dataValidade",
  "passo": "G"
 },
 {
  "fonte": "fm-dart",
  "origem": "Client.name2",
  "decisao": "mapeado",
  "destino": "HLM:ExportacaoFm/ClienteVenda.SegundoTitular.nome",
  "passo": "G"
 },
 {
  "fonte": "fm-dart",
  "origem": "Client.address2",
  "decisao": "mapeado",
  "destino": "HLM:ExportacaoFm/ClienteVenda.MoradaSegundoTitular.rua",
  "passo": "G"
 },
 {
  "fonte": "fm-dart",
  "origem": "Client.city2",
  "decisao": "mapeado",
  "destino": "HLM:ExportacaoFm/ClienteVenda.MoradaSegundoTitular.localidade",
  "passo": "G"
 },
 {
  "fonte": "fm-dart",
  "origem": "Client.zipCode2",
  "decisao": "mapeado",
  "destino": "HLM:ExportacaoFm/ClienteVenda.MoradaSegundoTitular.codigoPostal",
  "passo": "G"
 },
 {
  "fonte": "fm-dart",
  "origem": "Client.zipCodeLoc2",
  "decisao": "mapeado",
  "destino": "HLM:ExportacaoFm/ClienteVenda.designacaoPostalSegundoTitular",
  "passo": "G"
 },
 {
  "fonte": "fm-dart",
  "origem": "Client.citizenCard2",
  "decisao": "mapeado",
  "destino": "HLM:ExportacaoFm/ClienteVenda.CartaoCidadaoSegundoTitular.numero",
  "passo": "G"
 },
 {
  "fonte": "fm-dart",
  "origem": "Client.citizenCardExpirationDate2",
  "decisao": "mapeado",
  "destino": "HLM:ExportacaoFm/ClienteVenda.CartaoCidadaoSegundoTitular.dataValidade",
  "passo": "G"
 },
 {
  "fonte": "fm-dart",
  "origem": "Client.nif2",
  "decisao": "mapeado",
  "destino": "HLM:ExportacaoFm/ClienteVenda.SegundoTitular.nif",
  "passo": "G"
 },
 {
  "fonte": "fm-dart",
  "origem": "Client.fixePhoneNumber2",
  "decisao": "mapeado",
  "destino": "HLM:ExportacaoFm/ClienteVenda.ContactoSegundoTitular.telefone",
  "passo": "G"
 },
 {
  "fonte": "fm-dart",
  "origem": "Client.receivingDay",
  "decisao": "mapeado",
  "destino": "HLM:ExportacaoFm/ClienteVenda.diaRecebimento",
  "passo": "G"
 },
 {
  "fonte": "fm-dart",
  "origem": "Client.isNew",
  "decisao": "mapeado",
  "destino": "HLM:ExportacaoFm/ClienteVenda.novo",
  "passo": "G"
 },
 {
  "fonte": "fm-dart",
  "origem": "Company.prop",
  "decisao": "mapeado",
  "destino": "HLM:ExportacaoFm/Configuracao.ParametroEmpresa.nome",
  "passo": "G"
 },
 {
  "fonte": "fm-dart",
  "origem": "Company.value",
  "decisao": "mapeado",
  "destino": "HLM:ExportacaoFm/Configuracao.ParametroEmpresa.valor",
  "passo": "G"
 },
 {
  "fonte": "fm-dart",
  "origem": "Config.prop",
  "decisao": "mapeado",
  "destino": "HLM:ExportacaoFm/Configuracao.ParametroAplicacao.nome",
  "passo": "G"
 },
 {
  "fonte": "fm-dart",
  "origem": "Config.value",
  "decisao": "mapeado",
  "destino": "HLM:ExportacaoFm/Configuracao.ParametroAplicacao.valor",
  "passo": "G"
 },
 {
  "fonte": "fm-dart",
  "origem": "SellerProperty.propertyName",
  "decisao": "mapeado",
  "destino": "HLM:ExportacaoFm/Configuracao.ParametroVendedor.nome",
  "passo": "G"
 },
 {
  "fonte": "fm-dart",
  "origem": "SellerProperty.propertyValue",
  "decisao": "mapeado",
  "destino": "HLM:ExportacaoFm/Configuracao.ParametroVendedor.valor",
  "passo": "G"
 },
 {
  "fonte": "fm-dart",
  "origem": "Delivery.registrationDate",
  "decisao": "mapeado",
  "destino": "HLM:Entrega/DadosEntrega.dataRegisto",
  "passo": "G"
 },
 {
  "fonte": "fm-dart",
  "origem": "Delivery.clientBuyer",
  "decisao": "mapeado",
  "destino": "HLM:Entrega/Comprador",
  "nota": "composição do SM ClienteVenda com o papel Comprador",
  "passo": "G"
 },
 {
  "fonte": "fm-dart",
  "origem": "Delivery.clientDelivery",
  "decisao": "mapeado",
  "destino": "HLM:Entrega/Destinatario",
  "nota": "composição do SM ClienteVenda com o papel Destinatario",
  "passo": "G"
 },
 {
  "fonte": "fm-dart",
  "origem": "Delivery.articles",
  "decisao": "mapeado",
  "destino": "HLM:Entrega/LinhaEntrega",
  "nota": "composição 0..*",
  "passo": "G"
 },
 {
  "fonte": "fm-dart",
  "origem": "Delivery.deliveryNumber",
  "decisao": "mapeado",
  "destino": "HLM:Entrega/DadosEntrega.numeroEntrega",
  "passo": "G"
 },
 {
  "fonte": "fm-dart",
  "origem": "Delivery.invoiceNumber",
  "decisao": "mapeado",
  "destino": "HLM:Entrega/DadosEntrega.numeroFatura",
  "passo": "G"
 },
 {
  "fonte": "fm-dart",
  "origem": "Delivery.deliveryGuideNumber",
  "decisao": "mapeado",
  "destino": "HLM:Entrega/DadosEntrega.numeroGuiaTransporte",
  "passo": "G"
 },
 {
  "fonte": "fm-dart",
  "origem": "Delivery.contractNumber",
  "decisao": "mapeado",
  "destino": "HLM:Entrega/DadosEntrega.numeroContrato",
  "passo": "G"
 },
 {
  "fonte": "fm-dart",
  "origem": "Delivery.documentSaleNumber",
  "decisao": "mapeado",
  "destino": "HLM:Entrega/DadosEntrega.numeroDocumentoVenda",
  "passo": "G"
 },
 {
  "fonte": "fm-dart",
  "origem": "Delivery.documentType",
  "decisao": "mapeado",
  "destino": "HLM:Entrega/DadosEntrega.tipoDocumento",
  "nota": "valores admitidos desconhecidos",
  "passo": "G"
 },
 {
  "fonte": "fm-dart",
  "origem": "Delivery.status",
  "decisao": "mapeado",
  "destino": "HLM:Entrega/DadosEntrega.estado",
  "passo": "G"
 },
 {
  "fonte": "fm-dart",
  "origem": "Delivery.date",
  "decisao": "mapeado",
  "destino": "HLM:Entrega/DadosEntrega.data",
  "passo": "G"
 },
 {
  "fonte": "fm-dart",
  "origem": "DeliveryConfirmation.document",
  "decisao": "mapeado",
  "destino": "HLM:Entrega/ConfirmacaoEntrega.documentoConfirmado",
  "passo": "G"
 },
 {
  "fonte": "fm-dart",
  "origem": "DeliveryConfirmation.contract",
  "decisao": "mapeado",
  "destino": "HLM:Entrega/ConfirmacaoEntrega.contratoConfirmado",
  "passo": "G"
 },
 {
  "fonte": "fm-dart",
  "origem": "DeliveryConfirmation.delivery",
  "decisao": "mapeado",
  "destino": "HLM:Entrega/ConfirmacaoEntrega.entregaConfirmada",
  "passo": "G"
 },
 {
  "fonte": "fm-dart",
  "origem": "DeliveryConfirmation.originalPrice",
  "decisao": "mapeado",
  "destino": "HLM:Entrega/ConfirmacaoEntrega.precoOriginal",
  "passo": "G"
 },
 {
  "fonte": "fm-dart",
  "origem": "DeliveryConfirmation.signal",
  "decisao": "mapeado",
  "destino": "HLM:Entrega/ConfirmacaoEntrega.sinal",
  "passo": "G"
 },
 {
  "fonte": "fm-dart",
  "origem": "DeliveryConfirmation.installment",
  "decisao": "mapeado",
  "destino": "HLM:Entrega/ConfirmacaoEntrega.prestacao",
  "passo": "G"
 },
 {
  "fonte": "fm-dart",
  "origem": "DeliveryItem.article",
  "decisao": "mapeado",
  "destino": "HLM:Entrega/LinhaEntrega.Artigo",
  "nota": "referência ao artigo; só os dados canónicos (USM Artigo)",
  "passo": "G"
 },
 {
  "fonte": "fm-dart",
  "origem": "DeliveryItem.seriesNumber",
  "decisao": "mapeado",
  "destino": "HLM:Entrega/LinhaEntrega.numeroSerie",
  "passo": "G"
 },
 {
  "fonte": "fm-dart",
  "origem": "DeliveryItem.quantity",
  "decisao": "mapeado",
  "destino": "HLM:Entrega/LinhaEntrega.quantidade",
  "passo": "G"
 },
 {
  "fonte": "fm-dart",
  "origem": "DeliveryItem.customPrice",
  "decisao": "mapeado",
  "destino": "HLM:Entrega/LinhaEntrega.precoPersonalizado",
  "passo": "G"
 },
 {
  "fonte": "fm-dart",
  "origem": "DeliveryItem.customDiscount",
  "decisao": "mapeado",
  "destino": "HLM:Entrega/LinhaEntrega.descontoPersonalizado",
  "passo": "G"
 },
 {
  "fonte": "fm-dart",
  "origem": "FileInfo.name",
  "decisao": "mapeado",
  "destino": "HLM:ExportacaoFm/CabecalhoExportacao.nomeFicheiro",
  "passo": "G"
 },
 {
  "fonte": "fm-dart",
  "origem": "FileInfo.size",
  "decisao": "mapeado",
  "destino": "HLM:ExportacaoFm/CabecalhoExportacao.tamanhoFicheiro",
  "passo": "G"
 },
 {
  "fonte": "fm-dart",
  "origem": "FileInfo.lastModified",
  "decisao": "mapeado",
  "destino": "HLM:ExportacaoFm/CabecalhoExportacao.dataModificacao",
  "passo": "G"
 },
 {
  "fonte": "fm-dart",
  "origem": "FileInfo.nCli",
  "decisao": "mapeado",
  "destino": "HLM:ExportacaoFm/CabecalhoExportacao.numeroClientes",
  "passo": "G"
 },
 {
  "fonte": "fm-dart",
  "origem": "FileInfo.nArt",
  "decisao": "mapeado",
  "destino": "HLM:ExportacaoFm/CabecalhoExportacao.numeroArtigos",
  "passo": "G"
 },
 {
  "fonte": "fm-dart",
  "origem": "FileInfo.nDlv",
  "decisao": "mapeado",
  "destino": "HLM:ExportacaoFm/CabecalhoExportacao.numeroEntregas",
  "passo": "G"
 },
 {
  "fonte": "fm-dart",
  "origem": "FileInfo.nItem",
  "decisao": "mapeado",
  "destino": "HLM:ExportacaoFm/CabecalhoExportacao.numeroLinhasEntrega",
  "passo": "G"
 },
 {
  "fonte": "fm-dart",
  "origem": "HeaderInfo.nCli",
  "decisao": "fundido",
  "destino": "HLM:ExportacaoFm/CabecalhoExportacao.numeroClientes",
  "nota": "String na fonte",
  "passo": "G"
 },
 {
  "fonte": "fm-dart",
  "origem": "HeaderInfo.nArt",
  "decisao": "fundido",
  "destino": "HLM:ExportacaoFm/CabecalhoExportacao.numeroArtigos",
  "passo": "G"
 },
 {
  "fonte": "fm-dart",
  "origem": "HeaderInfo.nArtVeic",
  "decisao": "mapeado",
  "destino": "HLM:ExportacaoFm/CabecalhoExportacao.numeroArtigosVeiculo",
  "passo": "G"
 },
 {
  "fonte": "fm-dart",
  "origem": "HeaderInfo.nZone",
  "decisao": "mapeado",
  "destino": "HLM:ExportacaoFm/CabecalhoExportacao.numeroZonas",
  "passo": "G"
 },
 {
  "fonte": "fm-dart",
  "origem": "Seller.registrationDate",
  "decisao": "mapeado",
  "destino": "HLM:ExportacaoFm/Vendedor.dataRegisto",
  "passo": "G"
 },
 {
  "fonte": "fm-dart",
  "origem": "Seller.code",
  "decisao": "mapeado",
  "destino": "HLM:ExportacaoFm/Vendedor.codigo",
  "passo": "G"
 },
 {
  "fonte": "fm-dart",
  "origem": "Seller.name",
  "decisao": "mapeado",
  "destino": "HLM:ExportacaoFm/Vendedor.Entidade.nome",
  "passo": "G"
 },
 {
  "fonte": "fm-dart",
  "origem": "Seller.address",
  "decisao": "mapeado",
  "destino": "HLM:ExportacaoFm/Vendedor.Morada.rua",
  "passo": "G"
 },
 {
  "fonte": "fm-dart",
  "origem": "Seller.city",
  "decisao": "mapeado",
  "destino": "HLM:ExportacaoFm/Vendedor.Morada.localidade",
  "passo": "G"
 },
 {
  "fonte": "fm-dart",
  "origem": "Seller.zipCode",
  "decisao": "mapeado",
  "destino": "HLM:ExportacaoFm/Vendedor.Morada.codigoPostal",
  "passo": "G"
 },
 {
  "fonte": "fm-dart",
  "origem": "Seller.zipCodeLoc",
  "decisao": "mapeado",
  "destino": "HLM:ExportacaoFm/Vendedor.designacaoPostal",
  "passo": "G"
 },
 {
  "fonte": "fm-dart",
  "origem": "Seller.nif",
  "decisao": "mapeado",
  "destino": "HLM:ExportacaoFm/Vendedor.Entidade.nif",
  "passo": "G"
 },
 {
  "fonte": "fm-dart",
  "origem": "Seller.seriesNumber",
  "decisao": "mapeado",
  "destino": "HLM:ExportacaoFm/Vendedor.serie",
  "passo": "G"
 },
 {
  "fonte": "fm-dart",
  "origem": "Seller.seriesNumberStartingDate",
  "decisao": "mapeado",
  "destino": "HLM:ExportacaoFm/Vendedor.dataInicioSerie",
  "passo": "G"
 },
 {
  "fonte": "fm-dart",
  "origem": "Seller.commissionOfSaleOfProduct",
  "decisao": "mapeado",
  "destino": "HLM:ExportacaoFm/Vendedor.comissaoVendaPronto",
  "passo": "G"
 },
 {
  "fonte": "fm-dart",
  "origem": "Seller.commissionOfSaleOfInstallment",
  "decisao": "mapeado",
  "destino": "HLM:ExportacaoFm/Vendedor.comissaoVendaPrestacao",
  "passo": "G"
 },
 {
  "fonte": "fm-dart",
  "origem": "Seller.commissionOfCharge",
  "decisao": "mapeado",
  "destino": "HLM:ExportacaoFm/Vendedor.comissaoCobranca",
  "passo": "G"
 },
 {
  "fonte": "fm-dart",
  "origem": "Seller.phoneNumber",
  "decisao": "mapeado",
  "destino": "HLM:ExportacaoFm/Vendedor.ContactoTelefonico.telemovel",
  "passo": "G"
 },
 {
  "fonte": "fm-dart",
  "origem": "Seller.carRegistration",
  "decisao": "mapeado",
  "destino": "HLM:ExportacaoFm/Vendedor.Veiculo.matricula",
  "passo": "G"
 },
 {
  "fonte": "fm-dart",
  "origem": "Seller.car",
  "decisao": "mapeado",
  "destino": "HLM:ExportacaoFm/Vendedor.Veiculo.marca",
  "passo": "G"
 },
 {
  "fonte": "fm-dart",
  "origem": "Seller.carModel",
  "decisao": "mapeado",
  "destino": "HLM:ExportacaoFm/Vendedor.Veiculo.modelo",
  "passo": "G"
 },
 {
  "fonte": "fm-dart",
  "origem": "Seller.transportGuideNumber",
  "decisao": "mapeado",
  "destino": "HLM:ExportacaoFm/Vendedor.numeroGuiaTransporte",
  "passo": "G"
 },
 {
  "fonte": "fm-dart",
  "origem": "Seller.transportGuideExtraNumber",
  "decisao": "mapeado",
  "destino": "HLM:ExportacaoFm/Vendedor.numeroGuiaTransporteExtra",
  "passo": "G"
 },
 {
  "fonte": "fm-dart",
  "origem": "Seller.familyCodeExtra",
  "decisao": "mapeado",
  "destino": "HLM:ExportacaoFm/Vendedor.codigoFamiliaExtra",
  "passo": "G"
 },
 {
  "fonte": "fm-dart",
  "origem": "Seller.processReceiptsPermissions",
  "decisao": "mapeado",
  "destino": "HLM:ExportacaoFm/Vendedor.trataRecebimentos",
  "passo": "G"
 },
 {
  "fonte": "fm-dart",
  "origem": "Seller.senderNif",
  "decisao": "mapeado",
  "destino": "HLM:ExportacaoFm/Vendedor.nifEmissor",
  "passo": "G"
 },
 {
  "fonte": "fm-dart",
  "origem": "Zone.code",
  "decisao": "mapeado",
  "destino": "HLM:ExportacaoFm/Zona.codigo",
  "passo": "G"
 },
 {
  "fonte": "fm-dart",
  "origem": "Zone.name",
  "decisao": "mapeado",
  "destino": "HLM:ExportacaoFm/Zona.nome",
  "passo": "G"
 },
 {
  "fonte": "fm-dart",
  "origem": "Status-valores",
  "decisao": "mapeado",
  "destino": "Regra:RP-ENTFM-ESTADO",
  "passo": "G"
 },
 {
  "fonte": "fm-registos",
  "origem": "VDM.Codigo Vendedor, VDM.Nome Vendedor, VDM.Morada Vendedor, VDM.Localidade Vendedor, VDM.Codigo Postal vendedor, VDM.Telemovel Vendedor, VDM.NIF Vendedor, VDM.Serie Numerações, VDM.Data Inicio Serie, VDM.Comissao Venda Pronto, VDM.Comissao Venda Prestacao, VDM.Comissao Cobranca, VDM.Matricula, VDM.Veiculo, VDM.Modelo, VDM.Numero Guia Transporte, VDM.Numero Guia Transporte Extra, VDM.Codigo Familia Extra, VDM.Trata Recebimentos, VDM.Contribuinte do Emissor",
  "decisao": "fundido",
  "destino": "HLM:ExportacaoFm/Vendedor",
  "nota": "o mesmo significado que o campo correspondente de Seller (fm-dart), já mapeado",
  "passo": "G"
 },
 {
  "fonte": "fm-registos",
  "origem": "VDM.Telfone Vendedor",
  "decisao": "mapeado",
  "destino": "HLM:ExportacaoFm/Vendedor.ContactoTelefonico.telefone",
  "passo": "G"
 },
 {
  "fonte": "fm-registos",
  "origem": "VDM.Nº Ultimo Cliente",
  "decisao": "mapeado",
  "destino": "HLM:ExportacaoFm/Vendedor.numeroUltimoCliente",
  "passo": "G"
 },
 {
  "fonte": "fm-registos",
  "origem": "VDM.Prefixo ATCUD",
  "decisao": "mapeado",
  "destino": "HLM:ExportacaoFm/Vendedor.prefixoAtcud",
  "passo": "G"
 },
 {
  "fonte": "fm-registos",
  "origem": "VDM.Numero Digitos Serie",
  "decisao": "mapeado",
  "destino": "HLM:ExportacaoFm/Vendedor.numeroDigitosSerie",
  "passo": "G"
 },
 {
  "fonte": "fm-registos",
  "origem": "VDM.Nº Ult. Encomenda, VDM.Nº ult. Fatura, VDM.Nº Ult. Fatura Recibo, VDM.Nº Ult. Nota Credito, VDM.Nº Ult. Alteração enc., VDM.Nº Ult Recebimento, VDM.Num Ult. Recibo, VDM.Num Ult Entrada em CC",
  "decisao": "mapeado",
  "destino": "HLM:ExportacaoFm/Vendedor.NumeracaoDocumento.ultimoNumero",
  "nota": "um campo plano por tipo de documento passa a uma ocorrência de NumeracaoDocumento, com tipoDocumento = ENCOMENDA, FATURA, FATURA_RECIBO, NOTA_CREDITO, ALTERACAO_ENCOMENDA, RECEBIMENTO, RECIBO ou ENTRADA_CC",
  "passo": "G"
 },
 {
  "fonte": "fm-registos",
  "origem": "VDM.Data ULt Enomenda, VDM.Data Ult. Fatura, VDM.Data Ult. Fatura Recibo, VDM.Data Ult. Nota Credito, VDM.Data Ult Alteração  Encomenda, VDM.Data Ult . Recebimento, VDM.Data Ult Recibo, VDM.Data Ult. Entrada CC",
  "decisao": "mapeado",
  "destino": "HLM:ExportacaoFm/Vendedor.NumeracaoDocumento.dataUltimo",
  "nota": "Data Ult Recibo e Data Ult. Entrada CC são N(10) na fonte (provável erro); ficaram como data",
  "passo": "G"
 },
 {
  "fonte": "fm-registos",
  "origem": "VDM.Prefixo ATCUD Fatura, VDM.Prefixo ATCUD Fatura/ Recibo, VDM.Prefixo ATCUD Nota Credito, VDM.Prefixo ATCUD Encomenda, VDM.Prefixo ATCUD Recibo",
  "decisao": "mapeado",
  "destino": "HLM:ExportacaoFm/Vendedor.NumeracaoDocumento.prefixoAtcud",
  "passo": "G"
 },
 {
  "fonte": "fm-registos",
  "origem": "CLI.Codigo Cliente, CLI.Nome Cliente, CLI.Morada Cliente, CLI.Localidade Cliente, CLI.Codigo Postal cliente, CLI.Zona, CLI.Telefone Cliente, CLI.Telemovel Cliente, CLI.Data Abertura Ficha, CLI.Contribuinte Cliente, CLI.Codigo Vendedor, CLI.Numero Ordem, CLI.Email Cliente, CLI.Data Nascimento Cliente, CLI.Local Cobrança, CLI.Nome 2 Titular, CLI.Morada 2 Titular, CLI.Localidade 2 Titular, CLI.Cod Postal 2 Titular, CLI.Nº CC 2 Titular, CLI.Nº CC Cliente, CLI.Data Validade CC, CLI.Data Validade CC 2 Titular, CLI.Telefone 2 Titular, CLI.Contribuinte 2 Titular, CLI.Dia Recebimento",
  "decisao": "fundido",
  "destino": "HLM:ExportacaoFm/ClienteVenda",
  "nota": "o mesmo significado que o campo de Client indicado nos nomes alternativos; o código postal do registo junta codigoPostal e designacaoPostal",
  "passo": "G"
 },
 {
  "fonte": "fm-registos",
  "origem": "YCL.Codigo Cliente",
  "decisao": "mapeado",
  "destino": "HLM:ExportacaoFm/SaldoCliente.codigoCliente",
  "passo": "G"
 },
 {
  "fonte": "fm-registos",
  "origem": "YCL.Saldo",
  "decisao": "mapeado",
  "destino": "HLM:ExportacaoFm/SaldoCliente.saldo",
  "passo": "G"
 },
 {
  "fonte": "fm-registos",
  "origem": "YCL.Valor Total Vendas",
  "decisao": "mapeado",
  "destino": "HLM:ExportacaoFm/SaldoCliente.totalVendas",
  "passo": "G"
 },
 {
  "fonte": "fm-registos",
  "origem": "YCL.Valor Saldo Inicial",
  "decisao": "mapeado",
  "destino": "HLM:ExportacaoFm/SaldoCliente.saldoInicial",
  "passo": "G"
 },
 {
  "fonte": "fm-registos",
  "origem": "YCL.Valor Pago Saldo Inicial",
  "decisao": "mapeado",
  "destino": "HLM:ExportacaoFm/SaldoCliente.pagoSaldoInicial",
  "passo": "G"
 },
 {
  "fonte": "fm-registos",
  "origem": "YCL.Data Saldo Inicial",
  "decisao": "mapeado",
  "destino": "HLM:ExportacaoFm/SaldoCliente.dataSaldoInicial",
  "passo": "G"
 },
 {
  "fonte": "fm-registos",
  "origem": "STK.Codigo Artigo, STK.Codigo Axiliar, STK.Codigp EAN, STK.Descricao, STK.Referencia, STK.Unidade Medida, STK.Data Criação ficha, STK.Preço Venda com Iva, STK.% Desconto2, STK.Taxa de Iva, STK.Quantidade em stock, STK.Quantidade em stock Out, STK.Peso, STK.Codigo Familia, STK.Preço Custo sem Iva, STK.Preço Custo com Iva, STK.Codigo Fornecedor, STK.Nome Fornecedor, STK.Descricção Familia, STK.Serviço",
  "decisao": "fundido",
  "destino": "HLM:ExportacaoFm/ArtigoStock",
  "nota": "o mesmo significado que o campo correspondente de Article (fm-dart)",
  "passo": "G"
 },
 {
  "fonte": "fm-registos",
  "origem": "STK.% Desconto1",
  "decisao": "mapeado",
  "destino": "HLM:ExportacaoFm/ArtigoStock.desconto1",
  "passo": "G"
 },
 {
  "fonte": "fm-registos",
  "origem": "STK.Preço Venda 1 sem Iva",
  "decisao": "mapeado",
  "destino": "HLM:ExportacaoFm/ArtigoStock.precoVendaSemIva",
  "passo": "G"
 },
 {
  "fonte": "fm-registos",
  "origem": "STK.Preço Venda 2 com IVA",
  "decisao": "mapeado",
  "destino": "HLM:ExportacaoFm/ArtigoStock.precoVenda2ComIva",
  "passo": "G"
 },
 {
  "fonte": "fm-registos",
  "origem": "STK.Preço Venda 2 sem IVA",
  "decisao": "mapeado",
  "destino": "HLM:ExportacaoFm/ArtigoStock.precoVenda2SemIva",
  "passo": "G"
 },
 {
  "fonte": "fm-registos",
  "origem": "STK.Exporta OBS",
  "decisao": "mapeado",
  "destino": "HLM:ExportacaoFm/ArtigoStock.exportaObservacoes",
  "passo": "G"
 },
 {
  "fonte": "fm-registos",
  "origem": "AUX.ID",
  "decisao": "mapeado",
  "destino": "HLM:ExportacaoFm/Auxiliar.identificador",
  "passo": "G"
 },
 {
  "fonte": "fm-registos",
  "origem": "AUX.Texto",
  "decisao": "mapeado",
  "destino": "HLM:ExportacaoFm/Auxiliar.texto",
  "passo": "G"
 },
 {
  "fonte": "fm-registos",
  "origem": "PRV.Matricula",
  "decisao": "mapeado",
  "destino": "HLM:ExportacaoFm/ProdutoVeiculo.matricula",
  "passo": "G"
 },
 {
  "fonte": "fm-registos",
  "origem": "PRV.Codigo Artigo",
  "decisao": "mapeado",
  "destino": "HLM:ExportacaoFm/ProdutoVeiculo.codigoArtigo",
  "passo": "G"
 },
 {
  "fonte": "fm-registos",
  "origem": "PRV.Quantidade Total",
  "decisao": "mapeado",
  "destino": "HLM:ExportacaoFm/ProdutoVeiculo.quantidadeTotal",
  "passo": "G"
 },
 {
  "fonte": "fm-registos",
  "origem": "PRV.Quantidade Normal",
  "decisao": "mapeado",
  "destino": "HLM:ExportacaoFm/ProdutoVeiculo.quantidadeNormal",
  "passo": "G"
 },
 {
  "fonte": "fm-registos",
  "origem": "PRV.Quantidade Fora",
  "decisao": "mapeado",
  "destino": "HLM:ExportacaoFm/ProdutoVeiculo.quantidadeFora",
  "passo": "G"
 },
 {
  "fonte": "fm-registos",
  "origem": "VDM-2-COMPRIMENTO",
  "decisao": "mapeado",
  "destino": "Regra:RP-VEND-NOME",
  "passo": "G"
 },
 {
  "fonte": "fm-registos",
  "origem": "VDM-3-COMPRIMENTO",
  "decisao": "mapeado",
  "destino": "Regra:RP-VEND-RUA",
  "passo": "G"
 },
 {
  "fonte": "fm-registos",
  "origem": "VDM-4-COMPRIMENTO",
  "decisao": "mapeado",
  "destino": "Regra:RP-VEND-LOCALIDADE",
  "passo": "G"
 },
 {
  "fonte": "fm-registos",
  "origem": "VDM-5-COMPRIMENTO",
  "decisao": "mapeado",
  "destino": "Regra:RP-VEND-CP",
  "passo": "G"
 },
 {
  "fonte": "fm-registos",
  "origem": "VDM-6-COMPRIMENTO",
  "decisao": "mapeado",
  "destino": "Regra:RP-VEND-TELEFONE",
  "passo": "G"
 },
 {
  "fonte": "fm-registos",
  "origem": "VDM-7-COMPRIMENTO",
  "decisao": "mapeado",
  "destino": "Regra:RP-VEND-TELEMOVEL",
  "passo": "G"
 },
 {
  "fonte": "fm-registos",
  "origem": "VDM-8-COMPRIMENTO",
  "decisao": "mapeado",
  "destino": "Regra:RP-VEND-NIF",
  "passo": "G"
 },
 {
  "fonte": "fm-registos",
  "origem": "VDM-10-COMPRIMENTO",
  "decisao": "mapeado",
  "destino": "Regra:RP-VEND-SERIE",
  "passo": "G"
 },
 {
  "fonte": "fm-registos",
  "origem": "VDM-15-COMPRIMENTO",
  "decisao": "mapeado",
  "destino": "Regra:RP-VEIC-MATRICULA",
  "passo": "G"
 },
 {
  "fonte": "fm-registos",
  "origem": "VDM-16-COMPRIMENTO",
  "decisao": "mapeado",
  "destino": "Regra:RP-VEIC-MARCA",
  "passo": "G"
 },
 {
  "fonte": "fm-registos",
  "origem": "VDM-17-COMPRIMENTO",
  "decisao": "mapeado",
  "destino": "Regra:RP-VEIC-MODELO",
  "passo": "G"
 },
 {
  "fonte": "fm-registos",
  "origem": "VDM-24-COMPRIMENTO",
  "decisao": "mapeado",
  "destino": "Regra:RP-VEND-ATCUD",
  "passo": "G"
 },
 {
  "fonte": "fm-registos",
  "origem": "VDM-33-COMPRIMENTO",
  "decisao": "mapeado",
  "destino": "Regra:RP-VEND-FAMEXTRA",
  "passo": "G"
 },
 {
  "fonte": "fm-registos",
  "origem": "VDM-37-COMPRIMENTO",
  "decisao": "mapeado",
  "destino": "Regra:RP-VEND-DIGITOS",
  "passo": "G"
 },
 {
  "fonte": "fm-registos",
  "origem": "VDM-38-COMPRIMENTO, VDM-39-COMPRIMENTO, VDM-40-COMPRIMENTO, VDM-41-COMPRIMENTO, VDM-42-COMPRIMENTO",
  "decisao": "mapeado",
  "destino": "Regra:RP-NUM-ATCUD",
  "passo": "G"
 },
 {
  "fonte": "fm-registos",
  "origem": "VDM-43-COMPRIMENTO",
  "decisao": "mapeado",
  "destino": "Regra:RP-VEND-NIFEMISSOR",
  "passo": "G"
 },
 {
  "fonte": "fm-registos",
  "origem": "CLI-2-COMPRIMENTO",
  "decisao": "mapeado",
  "destino": "Regra:RP-CLI-NOME",
  "passo": "G"
 },
 {
  "fonte": "fm-registos",
  "origem": "CLI-3-COMPRIMENTO",
  "decisao": "mapeado",
  "destino": "Regra:RP-CLI-RUA",
  "passo": "G"
 },
 {
  "fonte": "fm-registos",
  "origem": "CLI-4-COMPRIMENTO",
  "decisao": "mapeado",
  "destino": "Regra:RP-CLI-LOCALIDADE",
  "passo": "G"
 },
 {
  "fonte": "fm-registos",
  "origem": "CLI-5-COMPRIMENTO",
  "decisao": "mapeado",
  "destino": "Regra:RP-CLI-CP",
  "passo": "G"
 },
 {
  "fonte": "fm-registos",
  "origem": "CLI-6-COMPRIMENTO",
  "decisao": "mapeado",
  "destino": "Regra:RP-CLI-ZONA",
  "passo": "G"
 },
 {
  "fonte": "fm-registos",
  "origem": "CLI-7-COMPRIMENTO",
  "decisao": "mapeado",
  "destino": "Regra:RP-CLI-TELEFONE",
  "passo": "G"
 },
 {
  "fonte": "fm-registos",
  "origem": "CLI-8-COMPRIMENTO",
  "decisao": "mapeado",
  "destino": "Regra:RP-CLI-TELEMOVEL",
  "passo": "G"
 },
 {
  "fonte": "fm-registos",
  "origem": "CLI-10-COMPRIMENTO",
  "decisao": "mapeado",
  "destino": "Regra:RP-CLI-NIF",
  "passo": "G"
 },
 {
  "fonte": "fm-registos",
  "origem": "CLI-13-COMPRIMENTO",
  "decisao": "mapeado",
  "destino": "Regra:RP-CLI-EMAIL",
  "passo": "G"
 },
 {
  "fonte": "fm-registos",
  "origem": "CLI-15-COMPRIMENTO",
  "decisao": "mapeado",
  "destino": "Regra:RP-CLI-COBRANCA",
  "passo": "G"
 },
 {
  "fonte": "fm-registos",
  "origem": "CLI-16-COMPRIMENTO",
  "decisao": "mapeado",
  "destino": "Regra:RP-CLI-NOME2",
  "passo": "G"
 },
 {
  "fonte": "fm-registos",
  "origem": "CLI-17-COMPRIMENTO",
  "decisao": "mapeado",
  "destino": "Regra:RP-CLI-RUA2",
  "passo": "G"
 },
 {
  "fonte": "fm-registos",
  "origem": "CLI-18-COMPRIMENTO",
  "decisao": "mapeado",
  "destino": "Regra:RP-CLI-LOCALIDADE2",
  "passo": "G"
 },
 {
  "fonte": "fm-registos",
  "origem": "CLI-19-COMPRIMENTO",
  "decisao": "mapeado",
  "destino": "Regra:RP-CLI-CP2",
  "passo": "G"
 },
 {
  "fonte": "fm-registos",
  "origem": "CLI-20-COMPRIMENTO",
  "decisao": "mapeado",
  "destino": "Regra:RP-CLI-CC2",
  "passo": "G"
 },
 {
  "fonte": "fm-registos",
  "origem": "CLI-21-COMPRIMENTO",
  "decisao": "mapeado",
  "destino": "Regra:RP-CLI-CC",
  "passo": "G"
 },
 {
  "fonte": "fm-registos",
  "origem": "CLI-24-COMPRIMENTO",
  "decisao": "mapeado",
  "destino": "Regra:RP-CLI-TELEFONE2",
  "passo": "G"
 },
 {
  "fonte": "fm-registos",
  "origem": "CLI-25-COMPRIMENTO",
  "decisao": "mapeado",
  "destino": "Regra:RP-CLI-NIF2",
  "passo": "G"
 },
 {
  "fonte": "fm-registos",
  "origem": "STK-1-COMPRIMENTO",
  "decisao": "mapeado",
  "destino": "Regra:RP-STK-CODIGO",
  "passo": "G"
 },
 {
  "fonte": "fm-registos",
  "origem": "STK-2-COMPRIMENTO",
  "decisao": "mapeado",
  "destino": "Regra:RP-STK-AUXILIAR",
  "passo": "G"
 },
 {
  "fonte": "fm-registos",
  "origem": "STK-3-COMPRIMENTO",
  "decisao": "mapeado",
  "destino": "Regra:RP-STK-EAN",
  "passo": "G"
 },
 {
  "fonte": "fm-registos",
  "origem": "STK-4-COMPRIMENTO",
  "decisao": "mapeado",
  "destino": "Regra:RP-STK-DESCRICAO",
  "passo": "G"
 },
 {
  "fonte": "fm-registos",
  "origem": "STK-5-COMPRIMENTO",
  "decisao": "mapeado",
  "destino": "Regra:RP-STK-REFERENCIA",
  "passo": "G"
 },
 {
  "fonte": "fm-registos",
  "origem": "STK-6-COMPRIMENTO",
  "decisao": "mapeado",
  "destino": "Regra:RP-STK-UNIDADE",
  "passo": "G"
 },
 {
  "fonte": "fm-registos",
  "origem": "STK-16-COMPRIMENTO",
  "decisao": "mapeado",
  "destino": "Regra:RP-STK-FAMILIA",
  "passo": "G"
 },
 {
  "fonte": "fm-registos",
  "origem": "STK-20-COMPRIMENTO",
  "decisao": "mapeado",
  "destino": "Regra:RP-STK-FORNECEDOR",
  "passo": "G"
 },
 {
  "fonte": "fm-registos",
  "origem": "STK-21-COMPRIMENTO",
  "decisao": "mapeado",
  "destino": "Regra:RP-STK-DESCFAMILIA",
  "passo": "G"
 },
 {
  "fonte": "fm-registos",
  "origem": "AUX-2-COMPRIMENTO",
  "decisao": "mapeado",
  "destino": "Regra:RP-AUX-TEXTO",
  "passo": "G"
 },
 {
  "fonte": "fm-registos",
  "origem": "PRV-1-COMPRIMENTO",
  "decisao": "mapeado",
  "destino": "Regra:RP-PRV-MATRICULA",
  "passo": "G"
 },
 {
  "fonte": "fm-registos",
  "origem": "PRV-2-COMPRIMENTO",
  "decisao": "mapeado",
  "destino": "Regra:RP-PRV-ARTIGO",
  "passo": "G"
 }
]
```

## Itens do inventário desta camada ainda sem mapeamento

```json
[
{"fonte":"cius-pt-schematron","id":"BR-52","texto":"Each Additional supporting document (BG-24) shall contain a Supporting document reference (BT-122).","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"Additional_supporting_documents","elementos":["BG-24","BT-122"],"expressao":"exists(cbc:ID)"},
{"fonte":"cius-pt-schematron","id":"BR-CIUS-PT-38","texto":"The Buyer identifier (BT-46) shall be filled.","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"Buyer","elementos":["BT-46"],"expressao":"report (dispara quando verdadeiro): exists(cac:Party/cac:PartyIdentification) and not(cac:Party/cac:PartyIdentification/cbc:ID)"},
{"fonte":"cius-pt-schematron","id":"BR-CIUS-PT-39","texto":"The Buyer trading name (BT-45) shall be filled.","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"Buyer","elementos":["BT-45"],"expressao":"report (dispara quando verdadeiro): exists(cac:Party/cac:PartyName) and not(cac:Party/cac:PartyName/cbc:Name)"},
{"fonte":"cius-pt-schematron","id":"BR-CIUS-PT-40","texto":"The Buyer contact point (BT-56) or the Buyer contact telephone number (BT-57) or the Buyer contact email address (BT-58) shall be filled.","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"Buyer","elementos":["BT-56","BT-57","BT-58"],"expressao":"report (dispara quando verdadeiro): exists(cac:Party/cac:Contact) and (not(cac:Party/cac:Contact/cbc:Name) and not(cac:Party/cac:Contact/cbc:Telephone) and not(cac:Party/cac:Contact/cbc:ElectronicMail))"},
{"fonte":"cius-pt-schematron","id":"BR-63","texto":"The Buyer electronic address (BT-49) shall have a Scheme identifier.","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"Buyer_electronic_address","elementos":["BT-49"],"expressao":"exists(@schemeID)"},
{"fonte":"cius-pt-schematron","id":"BR-11","texto":"The Buyer postal address shall contain a Buyer country code (BT-55).","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"Buyer_postal_address","elementos":["BT-55"],"expressao":"exists(cac:Country/cbc:IdentificationCode)"},
{"fonte":"cius-pt-schematron","id":"BR-CIUS-PT-41","texto":"The Buyer address line 3 (BT-163) shall be filled.","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"Buyer_postal_address","elementos":["BT-163"],"expressao":"report (dispara quando verdadeiro): exists(cac:AddressLine) and not(cac:AddressLine/cbc:Line)"},
{"fonte":"cius-pt-schematron","id":"BR-CIUS-PT-29","texto":"The Contract reference (BT-12) shall be filled.","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"Contract_Document_Reference","elementos":["BT-12"],"expressao":"exists(cbc:ID)"},
{"fonte":"cius-pt-schematron","id":"BR-CIUS-PT-46","texto":"The Deliver to party name (BT-70) shall be filled.","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"Delivery","elementos":["BT-70"],"expressao":"report (dispara quando verdadeiro): (exists(cac:DeliveryParty) and not(cac:DeliveryParty/cac:PartyName)) or (exists(cac:DeliveryParty/cac:PartyName) and not(cac:DeliveryParty/cac:PartyName/cbc:Name))"},
{"fonte":"cius-pt-schematron","id":"BR-CIUS-PT-21","texto":"Each Deliver to address (BG-15) shall contain a Seller address line 1 (BT-75).","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"Deliver_to_address","elementos":["BG-15","BT-75"],"expressao":"exists(cbc:StreetName)"},
{"fonte":"cius-pt-schematron","id":"BR-CIUS-PT-22","texto":"Each Deliver to address (BG-15) shall contain a Seller city (BT-77).","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"Deliver_to_address","elementos":["BG-15","BT-77"],"expressao":"exists(cbc:CityName)"},
{"fonte":"cius-pt-schematron","id":"BR-CIUS-PT-23","texto":"Each Deliver to address (BG-15) shall contain a Seller post code (BT-78).","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"Deliver_to_address","elementos":["BG-15","BT-78"],"expressao":"exists(cbc:PostalZone)"},
{"fonte":"cius-pt-schematron","id":"BR-57","texto":"Each Deliver to address (BG-15) shall contain a Deliver to country code (BT-80).","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"Deliver_to_address","elementos":["BG-15","BT-80"],"expressao":"exists(cac:Country/cbc:IdentificationCode)"},
{"fonte":"cius-pt-schematron","id":"BR-CIUS-PT-45","texto":"The Deliver to address line 3 (BT-165) shall be filled.","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"Deliver_to_address","elementos":["BT-165"],"expressao":"report (dispara quando verdadeiro): exists(cac:AddressLine) and not(cac:AddressLine/cbc:Line)"},
{"fonte":"cius-pt-schematron","id":"BR-CIUS-PT-26","texto":"The Despatch advice reference (BT-16) shall be filled.","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"Despatch_Document_Reference","elementos":["BT-16"],"expressao":"exists(cbc:ID)"},
{"fonte":"cius-pt-schematron","id":"BR-31","texto":"Each Document level allowance (BG-20) shall have a Document level allowance amount (BT-92).","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"Document_level_allowances","elementos":["BG-20","BT-92"],"expressao":"exists(cbc:Amount) "},
{"fonte":"cius-pt-schematron","id":"BR-32","texto":"Each Document level allowance (BG-20) shall have a Document level allowance VAT category code (BT-95).","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"Document_level_allowances","elementos":["BG-20","BT-95"],"expressao":"exists(cac:TaxCategory/cbc:ID)"},
{"fonte":"cius-pt-schematron","id":"BR-33","texto":"Each Document level allowance (BG-20) shall have a Document level allowance reason (BT-97) or a Document level allowance reason code (BT-98).","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"Document_level_allowances","elementos":["BG-20","BT-97","BT-98"],"expressao":"exists(cbc:AllowanceChargeReason) or exists(cbc:AllowanceChargeReasonCode)"},
{"fonte":"cius-pt-schematron","id":"BR-CO-21","texto":"Each Document level allowance (BG-20) shall contain a Document level allowance reason (BT-97) or a Document level allowance reason code (BT-98), or both.","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"Document_level_allowances","elementos":["BG-20","BT-97","BT-98"],"expressao":"exists(cbc:AllowanceChargeReason) or exists(cbc:AllowanceChargeReasonCode)"},
{"fonte":"cius-pt-schematron","id":"BR-CIUS-PT-19","texto":"Each Document level allowance (BG-20) shall have a tax scheme.","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"Document_level_allowances","elementos":["BG-20"],"expressao":"exists(cac:TaxCategory/cac:TaxScheme/cbc:ID)"},
{"fonte":"cius-pt-schematron","id":"BR-36","texto":"Each Document level charge (BG-21) shall have a Document level charge amount (BT-99).","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"Document_level_charges","elementos":["BG-21","BT-99"],"expressao":"exists(cbc:Amount)"},
{"fonte":"cius-pt-schematron","id":"BR-37","texto":"Each Document level charge (BG-21) shall have a Document level charge VAT category code (BT-102).","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"Document_level_charges","elementos":["BG-21","BT-102"],"expressao":"exists(cac:TaxCategory/cbc:ID)"},
{"fonte":"cius-pt-schematron","id":"BR-38","texto":"Each Document level charge (BG-21) shall have a Document level charge reason (BT-104) or a Document level charge reason code (BT-105).","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"Document_level_charges","elementos":["BG-21","BT-104","BT-105"],"expressao":"exists(cbc:AllowanceChargeReason) or exists(cbc:AllowanceChargeReasonCode)"},
{"fonte":"cius-pt-schematron","id":"BR-CO-22","texto":"Each Document level charge (BG-21) shall contain a Document level charge reason (BT-104) or a Document level charge reason code (BT-105), or both.","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"Document_level_charges","elementos":["BG-21","BT-104","BT-105"],"expressao":"exists(cbc:AllowanceChargeReason) or exists(cbc:AllowanceChargeReasonCode)"},
{"fonte":"cius-pt-schematron","id":"BR-CIUS-PT-20","texto":"Each Document level charge (BG-21) shall have a tax scheme.","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"Document_level_charges","elementos":["BG-21"],"expressao":"exists(cac:TaxCategory/cac:TaxScheme/cbc:ID)"},
{"fonte":"cius-pt-schematron","id":"BR-13","texto":"An Invoice shall have the Invoice total amount without VAT (BT-109).","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"Document_totals","elementos":["BT-109"],"expressao":"exists(cbc:TaxExclusiveAmount)"},
{"fonte":"cius-pt-schematron","id":"BR-14","texto":"An Invoice shall have the Invoice total amount with VAT (BT-112).","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"Document_totals","elementos":["BT-112"],"expressao":"exists(cbc:TaxInclusiveAmount)"},
{"fonte":"cius-pt-schematron","id":"BR-15","texto":"An Invoice shall have the Amount due for payment (BT-115).","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"Document_totals","elementos":["BT-115"],"expressao":"exists(cbc:PayableAmount)"},
{"fonte":"cius-pt-schematron","id":"BR-01","texto":"An Invoice shall have a Specification identifier (BT-24).","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"Invoice","elementos":["BT-24"],"expressao":"exists(cbc:CustomizationID)"},
{"fonte":"cius-pt-schematron","id":"BR-02","texto":"An Invoice shall have an Invoice number (BT-1).","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"Invoice","elementos":["BT-1"],"expressao":"exists(cbc:ID)"},
{"fonte":"cius-pt-schematron","id":"BR-03","texto":"An Invoice shall have an Invoice issue date (BT-2).","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"Invoice","elementos":["BT-2"],"expressao":"exists(cbc:IssueDate)"},
{"fonte":"cius-pt-schematron","id":"BR-04","texto":"An Invoice shall have an Invoice type code (BT-3).","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"Invoice","elementos":["BT-3"],"expressao":"exists(cbc:InvoiceTypeCode) or exists(cbc:CreditNoteTypeCode)"},
{"fonte":"cius-pt-schematron","id":"BR-05","texto":"An Invoice shall have an Invoice currency code (BT-5).","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"Invoice","elementos":["BT-5"],"expressao":"exists(cbc:DocumentCurrencyCode)"},
{"fonte":"cius-pt-schematron","id":"BR-06","texto":"An Invoice shall contain the Seller name (BT-27).","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"Invoice","elementos":["BT-27"],"expressao":"exists(cac:AccountingSupplierParty/cac:Party/cac:PartyLegalEntity/cbc:RegistrationName)"},
{"fonte":"cius-pt-schematron","id":"BR-CIUS-PT-01","texto":"An Invoice shall contain the Seller VAT identifier (BT-31).","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"Invoice","elementos":["BT-31"],"expressao":"exists(cac:AccountingSupplierParty/cac:Party/cac:PartyTaxScheme/cbc:CompanyID)"},
{"fonte":"cius-pt-schematron","id":"BR-CIUS-PT-02","texto":"An Invoice shall contain the Seller VAT tax scheme (VAT).","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"Invoice","expressao":"(cac:AccountingSupplierParty/cac:Party/cac:PartyTaxScheme/cac:TaxScheme/cbc:ID) = 'VAT'"},
{"fonte":"cius-pt-schematron","id":"BR-07","texto":"An Invoice shall contain the Buyer name (BT-44).","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"Invoice","elementos":["BT-44"],"expressao":"exists(cac:AccountingCustomerParty/cac:Party/cac:PartyLegalEntity/cbc:RegistrationName)"},
{"fonte":"cius-pt-schematron","id":"BR-CIUS-PT-03","texto":"An Invoice shall contain the Buyer VAT identifier (BT-48).","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"Invoice","elementos":["BT-48"],"expressao":"exists(cac:AccountingCustomerParty/cac:Party/cac:PartyTaxScheme/cbc:CompanyID)"},
{"fonte":"cius-pt-schematron","id":"BR-CIUS-PT-04","texto":"An Invoice shall contain the Buyer VAT tax scheme (VAT).","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"Invoice","expressao":"(cac:AccountingCustomerParty/cac:Party/cac:PartyTaxScheme/cac:TaxScheme/cbc:ID) = 'VAT'"},
{"fonte":"cius-pt-schematron","id":"BR-08","texto":"An Invoice shall contain the Seller postal address (BG-5).","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"Invoice","elementos":["BG-5"],"expressao":"exists(cac:AccountingSupplierParty/cac:Party/cac:PostalAddress)"},
{"fonte":"cius-pt-schematron","id":"BR-10","texto":"An Invoice shall contain the Buyer postal address (BG-8).","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"Invoice","elementos":["BG-8"],"expressao":"exists(cac:AccountingCustomerParty/cac:Party/cac:PostalAddress)"},
{"fonte":"cius-pt-schematron","id":"BR-16","texto":"An Invoice shall have at least one Invoice line (BG-25)","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"Invoice","elementos":["BG-25"],"expressao":"exists(cac:InvoiceLine) or exists(cac:CreditNoteLine)"},
{"fonte":"cius-pt-schematron","id":"BR-CIUS-PT-10","texto":"An Invoice shall contain the Document Totals (BG-22).","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"Invoice","elementos":["BG-22"],"expressao":"exists(cac:LegalMonetaryTotal)"},
{"fonte":"cius-pt-schematron","id":"BR-CIUS-PT-11","texto":"An Invoice shall contain the Total VAT amount (BT-110).","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"Invoice","elementos":["BT-110"],"expressao":"exists(cac:TaxTotal/cbc:TaxAmount)"},
{"fonte":"cius-pt-schematron","id":"BR-21","texto":"Each Invoice line (BG-25) shall have an Invoice line identifier (BT-126).","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"Invoice_Line ","elementos":["BG-25","BT-126"],"expressao":"exists(cbc:ID)"},
{"fonte":"cius-pt-schematron","id":"BR-22","texto":"Each Invoice line (BG-25) shall have an Invoiced quantity (BT-129).","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"Invoice_Line ","elementos":["BG-25","BT-129"],"expressao":"exists(cbc:InvoicedQuantity) or exists(cbc:CreditedQuantity)"},
{"fonte":"cius-pt-schematron","id":"BR-23","texto":"An Invoice line (BG-25) shall have an Invoiced quantity unit of measure code (BT-130).","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"Invoice_Line ","elementos":["BG-25","BT-130"],"expressao":"report (dispara quando verdadeiro): (exists(cbc:InvoicedQuantity) and not(cbc:InvoicedQuantity/@unitCode)) or (exists(cbc:CreditedQuantity) and not(cbc:CreditedQuantity/@unitCode))"},
{"fonte":"cius-pt-schematron","id":"BR-24","texto":"Each Invoice line (BG-25) shall have an Invoice line net amount (BT-131).","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"Invoice_Line ","elementos":["BG-25","BT-131"],"expressao":"exists(cbc:LineExtensionAmount)"},
{"fonte":"cius-pt-schematron","id":"BR-25","texto":"Each Invoice line (BG-25) shall contain the Item name (BT-153).","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"Invoice_Line ","elementos":["BG-25","BT-153"],"expressao":"exists(cac:Item/cbc:Name)"},
{"fonte":"cius-pt-schematron","id":"BR-26","texto":"Each Invoice line (BG-25) shall contain the Item net price (BT-146).","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"Invoice_Line ","elementos":["BG-25","BT-146"],"expressao":"exists(cac:Price/cbc:PriceAmount)"},
{"fonte":"cius-pt-schematron","id":"BR-CIUS-PT-09","texto":"Each Invoice line (BG-25) shall have a tax scheme.","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"Invoice_Line ","elementos":["BG-25"],"expressao":"exists(cac:Item/cac:ClassifiedTaxCategory/cac:TaxScheme/cbc:ID)"},
{"fonte":"cius-pt-schematron","id":"BR-CIUS-PT-51","texto":"The Referenced purchase order line reference (BT-132) shall be filled.","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"Invoice_Line ","elementos":["BT-132"],"expressao":"report (dispara quando verdadeiro): exists(cac:OrderLineReference) and not(cac:OrderLineReference/cbc:LineID)"},
{"fonte":"cius-pt-schematron","id":"BR-CIUS-PT-52","texto":"The Invoice line object identifier (BT-128) shall be filled.","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"Invoice_Line ","elementos":["BT-128"],"expressao":"report (dispara quando verdadeiro): exists(cac:DocumentReference) and not(cac:DocumentReference/cbc:ID)"},
{"fonte":"cius-pt-schematron","id":"BR-41","texto":"Each Invoice line allowance (BG-27) shall have an Invoice line allowance amount (BT-136).","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"Invoice_line_allowances","elementos":["BG-27","BT-136"],"expressao":"exists(cbc:Amount)"},
{"fonte":"cius-pt-schematron","id":"BR-42","texto":"Each Invoice line allowance (BG-27) shall have an Invoice line allowance reason (BT-139) or an Invoice line allowance reason code (BT-140).","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"Invoice_line_allowances","elementos":["BG-27","BT-139","BT-140"],"expressao":"exists(cbc:AllowanceChargeReason) or exists(cbc:AllowanceChargeReasonCode)"},
{"fonte":"cius-pt-schematron","id":"BR-CO-23","texto":"Each Invoice line allowance (BG-27) shall contain an Invoice line allowance reason (BT-139) or an Invoice line allowance reason code (BT-140), or both.","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"Invoice_line_allowances","elementos":["BG-27","BT-139","BT-140"],"expressao":"exists(cbc:AllowanceChargeReason) or exists(cbc:AllowanceChargeReasonCode)"},
{"fonte":"cius-pt-schematron","id":"BR-43","texto":"Each Invoice line charge (BG-28) shall have an Invoice line charge amount (BT-141).","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"Invoice_line_charges","elementos":["BG-28","BT-141"],"expressao":"exists(cbc:Amount)"},
{"fonte":"cius-pt-schematron","id":"BR-44","texto":"Each Invoice line charge shall have an Invoice line charge reason or an invoice line allowance reason code.","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"Invoice_line_charges","expressao":"exists(cbc:AllowanceChargeReason) or exists(cbc:AllowanceChargeReasonCode)"},
{"fonte":"cius-pt-schematron","id":"BR-CO-24","texto":"Each Invoice line charge (BG-28) shall contain an Invoice line charge reason (BT-144) or an Invoice line charge reason code (BT-145), or both.","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"Invoice_line_charges","elementos":["BG-28","BT-144","BT-145"],"expressao":"exists(cbc:AllowanceChargeReason) or exists(cbc:AllowanceChargeReasonCode)"},
{"fonte":"cius-pt-schematron","id":"BR-CIUS-PT-53","texto":"The Item Buyer's identifier (BT-156) shall be filled.","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"Invoice_Line_Item ","elementos":["BT-156"],"expressao":"report (dispara quando verdadeiro): exists(cac:BuyersItemIdentification) and not(cac:BuyersItemIdentification/cbc:ID)"},
{"fonte":"cius-pt-schematron","id":"BR-CIUS-PT-54","texto":"The Item Seller's identifier (BT-155) shall be filled.","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"Invoice_Line_Item ","elementos":["BT-155"],"expressao":"report (dispara quando verdadeiro): exists(cac:SellersItemIdentification) and not(cac:SellersItemIdentification/cbc:ID)"},
{"fonte":"cius-pt-schematron","id":"BR-CIUS-PT-55","texto":"The Item standard identifier (BT-157) shall be filled.","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"Invoice_Line_Item ","elementos":["BT-157"],"expressao":"report (dispara quando verdadeiro): exists(cac:StandardItemIdentification) and not(cac:StandardItemIdentification/cbc:ID)"},
{"fonte":"cius-pt-schematron","id":"BR-CIUS-PT-56","texto":"The Item country of origin (BT-159) shall be filled.","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"Invoice_Line_Item ","elementos":["BT-159"],"expressao":"report (dispara quando verdadeiro): exists(cac:OriginCountry) and not(cac:OriginCountry/cbc:IdentificationCode)"},
{"fonte":"cius-pt-schematron","id":"BR-CIUS-PT-57","texto":"The Item classification identifier (BT-158) shall be filled.","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"Invoice_Line_Item ","elementos":["BT-158"],"expressao":"report (dispara quando verdadeiro): exists(cac:CommodityClassification) and not(cac:CommodityClassification/cbc:ItemClassificationCode)"},
{"fonte":"cius-pt-schematron","id":"BR-CIUS-PT-59","texto":"The Item price discount (BT-147) shall be filled.","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"Invoice_Line_Price ","elementos":["BT-147"],"expressao":"report (dispara quando verdadeiro): exists(cac:AllowanceCharge[cbc:ChargeIndicator='false']) and not(cac:AllowanceCharge/cbc:Amount)"},
{"fonte":"cius-pt-schematron","id":"BR-54","texto":"Each Item attribute (BG-32) shall contain an Item attribute name (BT-160) and an Item attribute value (BT-161).","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"Item_attributes","elementos":["BG-32","BT-160","BT-161"],"expressao":"exists(cbc:Name) and exists(cbc:Value)"},
{"fonte":"cius-pt-schematron","id":"BR-65","texto":"The Item classification identifier (BT-158) shall have a Scheme identifier.","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"Item_classification_identifier","elementos":["BT-158"],"expressao":"exists(@listID)"},
{"fonte":"cius-pt-schematron","id":"BR-64","texto":"The Item standard identifier (BT-157) shall have a Scheme identifier.","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"Item_standard_identifier","elementos":["BT-157"],"expressao":"exists(@schemeID)"},
{"fonte":"cius-pt-schematron","id":"BR-CIUS-PT-24","texto":"The Purchase order reference (BT-13) or the Sales order reference (BT-14) shall be filled, or both.","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"Order_Reference","elementos":["BT-13","BT-14"],"expressao":"exists(cbc:ID) or exists(cbc:SalesOrderID)"},
{"fonte":"cius-pt-schematron","id":"BR-CIUS-PT-28","texto":"The Tender or lot reference (BT-17) shall be filled.","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"Originator_Document_Reference","elementos":["BT-17"],"expressao":"exists(cbc:ID)"},
{"fonte":"cius-pt-schematron","id":"BR-CIUS-PT-32","texto":"The Payee name (BT-59) shall be filled.","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"Payee","elementos":["BT-59"],"expressao":"report (dispara quando verdadeiro): exists(cac:PartyName) and not(cac:PartyName/cbc:Name)"},
{"fonte":"cius-pt-schematron","id":"BR-CIUS-PT-42","texto":"The Payee identifier (BT-60) or the Bank assigned creditor identifier (BT-90) shall be filled.","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"Payee","elementos":["BT-60","BT-90"],"expressao":"report (dispara quando verdadeiro): exists(cac:PartyIdentification) and not(cac:PartyIdentification/cbc:ID)"},
{"fonte":"cius-pt-schematron","id":"BR-CIUS-PT-43","texto":"The Payee legal registration identifier (BT-61) shall be filled.","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"Payee","elementos":["BT-61"],"expressao":"report (dispara quando verdadeiro): exists(cac:PartyLegalEntity) and not(cac:PartyLegalEntity/cbc:CompanyID)"},
{"fonte":"cius-pt-schematron","id":"BR-CIUS-PT-47","texto":"The Payment account identifier (BT-84) or the Payment account name (BT-85) or the Payment service provider identifier (BT-86) shall be filled.","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"Payment_instructions","elementos":["BT-84","BT-85","BT-86"],"expressao":"report (dispara quando verdadeiro): exists(cac:PayeeFinancialAccount) and (not(cac:PayeeFinancialAccount/cbc:ID) and not(cac:PayeeFinancialAccount/cbc:Name) and not(cac:PayeeFinancialAccount/cac:FinancialInstitutionBranch/cbc:ID))"},
{"fonte":"cius-pt-schematron","id":"BR-CIUS-PT-48","texto":"The Payment service provider identifier (BT-86) shall be filled.","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"Payment_instructions","elementos":["BT-86"],"expressao":"report (dispara quando verdadeiro): exists(cac:PayeeFinancialAccount/cac:FinancialInstitutionBranch) and not(cac:PayeeFinancialAccount/cac:FinancialInstitutionBranch/cbc:ID)"},
{"fonte":"cius-pt-schematron","id":"BR-CIUS-PT-49","texto":"The Mandate reference identifier (BT-89) or the Debited account identifier (BT-91) shall be filled.","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"Payment_instructions","elementos":["BT-89","BT-91"],"expressao":"report (dispara quando verdadeiro): exists(cac:PaymentMandate) and (not(cac:PaymentMandate/cbc:ID) and not(cac:PaymentMandate/cac:PayerFinancialAccount/cbc:ID))"},
{"fonte":"cius-pt-schematron","id":"BR-CIUS-PT-50","texto":"The Debited account identifier (BT-91) shall be filled.","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"Payment_instructions","elementos":["BT-91"],"expressao":"report (dispara quando verdadeiro): exists(cac:PaymentMandate/cac:PayerFinancialAccount) and not(cac:PaymentMandate/cac:PayerFinancialAccount/cbc:ID)"},
{"fonte":"cius-pt-schematron","id":"BR-CIUS-PT-60","texto":"The Payment card primary account number (BT-87) and the card Network identifier shall be filled.","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"Payment_instructions","elementos":["BT-87"],"expressao":"report (dispara quando verdadeiro): exists(cac:CardAccount) and (not(cac:CardAccount/cbc:PrimaryAccountNumberID) or not(cac:CardAccount/cbc:NetworkID))"},
{"fonte":"cius-pt-schematron","id":"BR-CIUS-PT-61","texto":"The Payment terms (BT-20) shall be filled.","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"Payment_terms","elementos":["BT-20"],"expressao":"exists(cbc:Note)"},
{"fonte":"cius-pt-schematron","id":"BR-55","texto":"Each Preceding Invoice reference (BG-3) shall contain a Preceding Invoice reference (BT-25).","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"Preceding_Invoice","elementos":["BG-3","BT-25"],"expressao":"exists(cac:InvoiceDocumentReference/cbc:ID)"},
{"fonte":"cius-pt-schematron","id":"BR-CIUS-PT-33","texto":"The Project reference (BT-11) shall be filled.","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"Project_Reference","elementos":["BT-11"],"expressao":"exists(cbc:ID)"},
{"fonte":"cius-pt-schematron","id":"BR-CIUS-PT-27","texto":"The Receiving advice reference (BT-15) shall be filled.","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"Receipt_Document_Reference","elementos":["BT-15"],"expressao":"exists(cbc:ID)"},
{"fonte":"cius-pt-schematron","id":"BR-CO-26","texto":"In order for the buyer to automatically identify a supplier, the Seller identifier (BT-29), the Seller legal registration identifier (BT-30) and/or the Seller VAT identifier (BT-31) shall be present.","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"Seller","elementos":["BT-29","BT-30","BT-31"],"expressao":"exists(cac:Party/cac:PartyTaxScheme/cbc:CompanyID) or exists(cac:Party/cac:PartyIdentification/cbc:ID) or exists(cac:Party/cac:PartyLegalEntity/cbc:CompanyID)"},
{"fonte":"cius-pt-schematron","id":"BR-CIUS-PT-34","texto":"The Seller identifier (BT-29) or the Bank assigned creditor identifier (BT-90) shall be filled.","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"Seller","elementos":["BT-29","BT-90"],"expressao":"report (dispara quando verdadeiro): exists(cac:Party/cac:PartyIdentification) and not(cac:Party/cac:PartyIdentification/cbc:ID)"},
{"fonte":"cius-pt-schematron","id":"BR-CIUS-PT-35","texto":"The Seller trading name (BT-28) shall be filled.","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"Seller","elementos":["BT-28"],"expressao":"report (dispara quando verdadeiro): exists(cac:Party/cac:PartyName) and not(cac:Party/cac:PartyName/cbc:Name)"},
{"fonte":"cius-pt-schematron","id":"BR-CIUS-PT-36","texto":"The Seller contact point (BT-41) or the Seller contact telephone number (BT-42) or the Seller contact email address (BT-43) shall be filled.","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"Seller","elementos":["BT-41","BT-42","BT-43"],"expressao":"report (dispara quando verdadeiro): exists(cac:Party/cac:Contact) and (not(cac:Party/cac:Contact/cbc:Name) and not(cac:Party/cac:Contact/cbc:Telephone) and not(cac:Party/cac:Contact/cbc:ElectronicMail))"},
{"fonte":"cius-pt-schematron","id":"BR-62","texto":"The Seller electronic address (BT-34) shall have a Scheme identifier.","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"Seller_electronic_address","elementos":["BT-34"],"expressao":"exists(@schemeID)"},
{"fonte":"cius-pt-schematron","id":"BR-CIUS-PT-05","texto":"The Seller postal address (BG-5) shall contain a Seller address line 1 (BT-35).","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"Seller_postal_address","elementos":["BG-5","BT-35"],"expressao":"exists(cbc:StreetName)"},
{"fonte":"cius-pt-schematron","id":"BR-CIUS-PT-06","texto":"The Seller postal address (BG-5) shall contain a Seller city (BT-37).","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"Seller_postal_address","elementos":["BG-5","BT-37"],"expressao":"exists(cbc:CityName)"},
{"fonte":"cius-pt-schematron","id":"BR-CIUS-PT-07","texto":"The Seller postal address (BG-5) shall contain a Seller post code (BT-38).","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"Seller_postal_address","elementos":["BG-5","BT-38"],"expressao":"exists(cbc:PostalZone)"},
{"fonte":"cius-pt-schematron","id":"BR-09","texto":"The Seller postal address (BG-5) shall contain a Seller country code (BT-40).","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"Seller_postal_address","elementos":["BG-5","BT-40"],"expressao":"exists(cac:Country/cbc:IdentificationCode)"},
{"fonte":"cius-pt-schematron","id":"BR-CIUS-PT-37","texto":"The Seller address line 3 (BT-162) shall be filled.","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"Seller_postal_address","elementos":["BT-162"],"expressao":"report (dispara quando verdadeiro): exists(cac:AddressLine) and not(cac:AddressLine/cbc:Line)"},
{"fonte":"cius-pt-schematron","id":"BR-56","texto":"Each Seller tax representative party (BG-11) shall have a Seller tax representative VAT identifier (BT-63).","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"Tax_Representative","elementos":["BG-11","BT-63"],"expressao":"exists(cac:PartyTaxScheme[cac:TaxScheme/cbc:ID = 'VAT']/cbc:CompanyID)"},
{"fonte":"cius-pt-schematron","id":"BR-CIUS-PT-44","texto":"The Tax representative address line 3 (BT-164) shall be filled.","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"Tax_Representative_postal_address","elementos":["BT-164"],"expressao":"report (dispara quando verdadeiro): exists(cac:AddressLine) and not(cac:AddressLine/cbc:Line)"},
{"fonte":"cius-pt-schematron","id":"BR-45","texto":"Each VATBReakdown (BG-23) shall have a VAT category taxable amount (BT-116).","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"VAT_breakdown","elementos":["BG-23","BT-116"],"expressao":"exists(cbc:TaxableAmount)"},
{"fonte":"cius-pt-schematron","id":"BR-46","texto":"Each VATBReakdown (BG-23) shall have a VAT category tax amount (BT-117).","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"VAT_breakdown","elementos":["BG-23","BT-117"],"expressao":"exists(cbc:TaxAmount)"},
{"fonte":"cius-pt-schematron","id":"BR-48","texto":"Each VATBReakdown (BG-23) shall have a VAT category rate (BT-119).","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"VAT_breakdown","elementos":["BG-23","BT-119"],"expressao":"exists(cac:TaxCategory/cbc:Percent)"},
{"fonte":"cius-pt-schematron","id":"BR-CIUS-PT-08","texto":"Each VATBReakdown (BG-23) shall have a tax scheme.","categoria":"presenca","natureza":"RE","gravidade":"erro","contexto":"VAT_breakdown","elementos":["BG-23"],"expressao":"exists(cac:TaxCategory/cac:TaxScheme/cbc:ID)"},
{"fonte":"cius-pt-schematron","id":"UBL-SR-33","texto":"Supporting document description shall occur maximum once","categoria":"cardinalidade","natureza":"RE","gravidade":"aviso","contexto":"Additional_supporting_documents","expressao":"(count(cbc:DocumentType) <= 1)"},
{"fonte":"cius-pt-schematron","id":"UBL-SR-25","texto":"Deliver to party name shall occur maximum once","categoria":"cardinalidade","natureza":"RE","gravidade":"aviso","contexto":"Deliver_to","expressao":"(count(cac:DeliveryParty/cac:PartyName/cbc:Name) <= 1)"},
{"fonte":"cius-pt-schematron","id":"UBL-SR-30","texto":"Document level allowance reason shall occur maximum once","categoria":"cardinalidade","natureza":"RE","gravidade":"aviso","contexto":"Document_level_allowances","expressao":"(count(cbc:AllowanceChargeReason) <= 1)"},
{"fonte":"cius-pt-schematron","id":"UBL-SR-31","texto":"Document level charge reason shall occur maximum once","categoria":"cardinalidade","natureza":"RE","gravidade":"aviso","contexto":"Document_level_charges","expressao":"(count(cbc:AllowanceChargeReason) <= 1)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-001","texto":"A UBL invoice should not include extensions","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(ext:UBLExtensions)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-003","texto":"A UBL invoice should not include the ProfileExecutionID","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cbc:ProfileExecutionID)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-004","texto":"A UBL invoice should not include the CopyIndicator","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cbc:CopyIndicator)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-005","texto":"A UBL invoice should not include the UUID","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cbc:UUID)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-006","texto":"A UBL invoice should not include the IssueTime","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cbc:IssueTime)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-007","texto":"A UBL invoice should not include the PricingCurrencyCode","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cbc:PricingCurrencyCode)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-008","texto":"A UBL invoice should not include the PaymentCurrencyCode","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cbc:PaymentCurrencyCode)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-009","texto":"A UBL invoice should not include the PaymentAlternativeCurrencyCode","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cbc:PaymentAlternativeCurrencyCode)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-010","texto":"A UBL invoice should not include the AccountingCostCode","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cbc:AccountingCostCode)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-011","texto":"A UBL invoice should not include the LineCountNumeric","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cbc:LineCountNumeric)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-012","texto":"A UBL invoice should not include the InvoicePeriod StartTime","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoicePeriod/cbc:StartTime)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-013","texto":"A UBL invoice should not include the InvoicePeriod EndTime","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoicePeriod/cbc:EndTime)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-014","texto":"A UBL invoice should not include the InvoicePeriod DurationMeasure","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoicePeriod/cbc:DurationMeasure)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-015","texto":"A UBL invoice should not include the InvoicePeriod Description","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoicePeriod/cbc:Description)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-016","texto":"A UBL invoice should not include the OrderReference CopyIndicator","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:OrderReference/cbc:CopyIndicator)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-017","texto":"A UBL invoice should not include the OrderReference UUID","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:OrderReference/cbc:UUID)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-018","texto":"A UBL invoice should not include the OrderReference IssueDate","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:OrderReference/cbc:IssueDate)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-019","texto":"A UBL invoice should not include the OrderReference IssueTime","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:OrderReference/cbc:IssueTime)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-020","texto":"A UBL invoice should not include the OrderReference CustomerReference","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:OrderReference/cbc:CustomerReference)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-021","texto":"A UBL invoice should not include the OrderReference OrderTypeCode","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:OrderReference/cbc:OrderTypeCode)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-022","texto":"A UBL invoice should not include the OrderReference DocumentReference","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:OrderReference/cbc:DocumentReference)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-023","texto":"A UBL invoice should not include the BillingReference CopyIndicator","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:BillingReference/cac:InvoiceDocumentReference/cbc:CopyIndicator)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-024","texto":"A UBL invoice should not include the BillingReference UUID","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:BillingReference/cac:InvoiceDocumentReference/cbc:UUID)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-025","texto":"A UBL invoice should not include the BillingReference IssueTime","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:BillingReference/cac:InvoiceDocumentReference/cbc:IssueTime)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-026","texto":"A UBL invoice should not include the BillingReference DocumentTypeCode","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:BillingReference/cac:InvoiceDocumentReference/cbc:DocumentTypeCode)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-027","texto":"A UBL invoice should not include the BillingReference DocumentType","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:BillingReference/cac:InvoiceDocumentReference/cbc:DocumentType)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-028","texto":"A UBL invoice should not include the BillingReference Xpath","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:BillingReference/cac:InvoiceDocumentReference/cbc:Xpath)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-029","texto":"A UBL invoice should not include the BillingReference LanguageID","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:BillingReference/cac:InvoiceDocumentReference/cbc:LanguageID)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-030","texto":"A UBL invoice should not include the BillingReference LocaleCode","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:BillingReference/cac:InvoiceDocumentReference/cbc:LocaleCode)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-031","texto":"A UBL invoice should not include the BillingReference VersionID","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:BillingReference/cac:InvoiceDocumentReference/cbc:VersionID)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-032","texto":"A UBL invoice should not include the BillingReference DocumentStatusCode","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:BillingReference/cac:InvoiceDocumentReference/cbc:DocumentStatusCode)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-033","texto":"A UBL invoice should not include the BillingReference DocumenDescription","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:BillingReference/cac:InvoiceDocumentReference/cbc:DocumentDescription)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-034","texto":"A UBL invoice should not include the BillingReference Attachment","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:BillingReference/cac:InvoiceDocumentReference/cac:Attachment)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-035","texto":"A UBL invoice should not include the BillingReference ValidityPeriod","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:BillingReference/cac:InvoiceDocumentReference/cac:ValidityPeriod)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-036","texto":"A UBL invoice should not include the BillingReference IssuerParty","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:BillingReference/cac:InvoiceDocumentReference/cac:IssuerParty)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-037","texto":"A UBL invoice should not include the BillingReference ResultOfVerification","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:BillingReference/cac:InvoiceDocumentReference/cac:ResultOfVerification)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-038","texto":"A UBL invoice should not include the BillingReference SelfBilledInvoiceDocumentReference","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:BillingReference/cac:SelfBilledInvoiceDocumentReference)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-039","texto":"A UBL invoice should not include the BillingReference CreditNoteDocumentReference","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:BillingReference/cac:CreditNoteDocumentReference)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-040","texto":"A UBL invoice should not include the BillingReference SelfBilledCreditNoteDocumentReference","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:BillingReference/cac:SelfBilledCreditNoteDocumentReference)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-041","texto":"A UBL invoice should not include the BillingReference DebitNoteDocumentReference","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:BillingReference/cac:DebitNoteDocumentReference)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-042","texto":"A UBL invoice should not include the BillingReference ReminderDocumentReference","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:BillingReference/cac:ReminderDocumentReference)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-043","texto":"A UBL invoice should not include the BillingReference AdditionalDocumentReference","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:BillingReference/cac:AdditionalDocumentReference)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-044","texto":"A UBL invoice should not include the BillingReference BillingReferenceLine","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:BillingReference/cac:BillingReferenceLine)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-045","texto":"A UBL invoice should not include the DespatchDocumentReference CopyIndicator","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:DespatchDocumentReference/cbc:CopyIndicator)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-046","texto":"A UBL invoice should not include the DespatchDocumentReference UUID","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:DespatchDocumentReference/cbc:UUID)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-047","texto":"A UBL invoice should not include the DespatchDocumentReference IssueDate","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:DespatchDocumentReference/cbc:IssueDate)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-048","texto":"A UBL invoice should not include the DespatchDocumentReference IssueTime","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:DespatchDocumentReference/cbc:IssueTime)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-049","texto":"A UBL invoice should not include the DespatchDocumentReference DocumentTypeCode","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:DespatchDocumentReference/cbc:DocumentTypeCode)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-050","texto":"A UBL invoice should not include the DespatchDocumentReference DocumentType","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:DespatchDocumentReference/cbc:DocumentType)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-051","texto":"A UBL invoice should not include the DespatchDocumentReference Xpath","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:DespatchDocumentReference/cbc:Xpath)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-052","texto":"A UBL invoice should not include the DespatchDocumentReference LanguageID","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:DespatchDocumentReference/cbc:LanguageID)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-053","texto":"A UBL invoice should not include the DespatchDocumentReference LocaleCode","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:DespatchDocumentReference/cbc:LocaleCode)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-054","texto":"A UBL invoice should not include the DespatchDocumentReference VersionID","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:DespatchDocumentReference/cbc:VersionID)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-055","texto":"A UBL invoice should not include the DespatchDocumentReference DocumentStatusCode","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:DespatchDocumentReference/cbc:DocumentStatusCode)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-056","texto":"A UBL invoice should not include the DespatchDocumentReference DocumentDescription","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:DespatchDocumentReference/cbc:DocumentDescription)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-057","texto":"A UBL invoice should not include the DespatchDocumentReference Attachment","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:DespatchDocumentReference/cac:Attachment)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-058","texto":"A UBL invoice should not include the DespatchDocumentReference ValidityPeriod","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:DespatchDocumentReference/cac:ValidityPeriod)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-059","texto":"A UBL invoice should not include the DespatchDocumentReference IssuerParty","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:DespatchDocumentReference/cac:IssuerParty)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-060","texto":"A UBL invoice should not include the DespatchDocumentReference ResultOfVerification","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:DespatchDocumentReference/cac:ResultOfVerification)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-061","texto":"A UBL invoice should not include the ReceiptDocumentReference CopyIndicator","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:ReceiptDocumentReference/cbc:CopyIndicator)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-062","texto":"A UBL invoice should not include the ReceiptDocumentReference UUID","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:ReceiptDocumentReference/cbc:UUID)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-063","texto":"A UBL invoice should not include the ReceiptDocumentReference IssueDate","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:ReceiptDocumentReference/cbc:IssueDate)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-064","texto":"A UBL invoice should not include the ReceiptDocumentReference IssueTime","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:ReceiptDocumentReference/cbc:IssueTime)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-065","texto":"A UBL invoice should not include the ReceiptDocumentReference DocumentTypeCode","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:ReceiptDocumentReference/cbc:DocumentTypeCode)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-066","texto":"A UBL invoice should not include the ReceiptDocumentReference DocumentType","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:ReceiptDocumentReference/cbc:DocumentType)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-067","texto":"A UBL invoice should not include the ReceiptDocumentReference Xpath","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:ReceiptDocumentReference/cbc:Xpath)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-068","texto":"A UBL invoice should not include the ReceiptDocumentReference LanguageID","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:ReceiptDocumentReference/cbc:LanguageID)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-069","texto":"A UBL invoice should not include the ReceiptDocumentReference LocaleCode","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:ReceiptDocumentReference/cbc:LocaleCode)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-070","texto":"A UBL invoice should not include the ReceiptDocumentReference VersionID","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:ReceiptDocumentReference/cbc:VersionID)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-071","texto":"A UBL invoice should not include the ReceiptDocumentReference DocumentStatusCode","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:ReceiptDocumentReference/cbc:DocumentStatusCode)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-072","texto":"A UBL invoice should not include the ReceiptDocumentReference DocumentDescription","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:ReceiptDocumentReference/cbc:DocumentDescription)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-073","texto":"A UBL invoice should not include the ReceiptDocumentReference Attachment","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:ReceiptDocumentReference/cac:Attachment)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-074","texto":"A UBL invoice should not include the ReceiptDocumentReference ValidityPeriod","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:ReceiptDocumentReference/cac:ValidityPeriod)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-075","texto":"A UBL invoice should not include the ReceiptDocumentReference IssuerParty","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:ReceiptDocumentReference/cac:IssuerParty)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-076","texto":"A UBL invoice should not include the ReceiptDocumentReference ResultOfVerification","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:ReceiptDocumentReference/cac:ResultOfVerification)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-077","texto":"A UBL invoice should not include the StatementDocumentReference","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:StatementDocumentReference)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-078","texto":"A UBL invoice should not include the OriginatorDocumentReference CopyIndicator","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:OriginatorDocumentReference/cbc:CopyIndicator)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-079","texto":"A UBL invoice should not include the OriginatorDocumentReference UUID","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:OriginatorDocumentReference/cbc:UUID)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-080","texto":"A UBL invoice should not include the OriginatorDocumentReference IssueDate","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:OriginatorDocumentReference/cbc:IssueDate)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-081","texto":"A UBL invoice should not include the OriginatorDocumentReference IssueTime","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:OriginatorDocumentReference/cbc:IssueTime)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-082","texto":"A UBL invoice should not include the OriginatorDocumentReference DocumentTypeCode","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:OriginatorDocumentReference/cbc:DocumentTypeCode)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-083","texto":"A UBL invoice should not include the OriginatorDocumentReference DocumentType","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:OriginatorDocumentReference/cbc:DocumentType)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-084","texto":"A UBL invoice should not include the OriginatorDocumentReference Xpath","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:OriginatorDocumentReference/cbc:Xpath)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-085","texto":"A UBL invoice should not include the OriginatorDocumentReference LanguageID","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:OriginatorDocumentReference/cbc:LanguageID)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-086","texto":"A UBL invoice should not include the OriginatorDocumentReference LocaleCode","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:OriginatorDocumentReference/cbc:LocaleCode)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-087","texto":"A UBL invoice should not include the OriginatorDocumentReference VersionID","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:OriginatorDocumentReference/cbc:VersionID)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-088","texto":"A UBL invoice should not include the OriginatorDocumentReference DocumentStatusCode","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:OriginatorDocumentReference/cbc:DocumentStatusCode)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-089","texto":"A UBL invoice should not include the OriginatorDocumentReference DocumentDescription","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:OriginatorDocumentReference/cbc:DocumentDescription)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-090","texto":"A UBL invoice should not include the OriginatorDocumentReference Attachment","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:OriginatorDocumentReference/cac:Attachment)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-091","texto":"A UBL invoice should not include the OriginatorDocumentReference ValidityPeriod","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:OriginatorDocumentReference/cac:ValidityPeriod)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-092","texto":"A UBL invoice should not include the OriginatorDocumentReference IssuerParty","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:OriginatorDocumentReference/cac:IssuerParty)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-093","texto":"A UBL invoice should not include the OriginatorDocumentReference ResultOfVerification","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:OriginatorDocumentReference/cac:ResultOfVerification)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-094","texto":"A UBL invoice should not include the ContractDocumentReference CopyIndicator","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:ContractDocumentReference/cbc:CopyIndicator)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-095","texto":"A UBL invoice should not include the ContractDocumentReference UUID","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:ContractDocumentReference/cbc:UUID)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-096","texto":"A UBL invoice should not include the ContractDocumentReference IssueDate","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:ContractDocumentReference/cbc:IssueDate)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-097","texto":"A UBL invoice should not include the ContractDocumentReference IssueTime","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:ContractDocumentReference/cbc:IssueTime)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-098","texto":"A UBL invoice should not include the ContractDocumentReference DocumentTypeCode","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:ContractDocumentReference/cbc:DocumentTypeCode)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-099","texto":"A UBL invoice should not include the ContractDocumentReference DocumentType","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:ContractDocumentReference/cbc:DocumentType)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-100","texto":"A UBL invoice should not include the ContractDocumentReference Xpath","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:ContractDocumentReference/cbc:Xpath)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-101","texto":"A UBL invoice should not include the ContractDocumentReference LanguageID","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:ContractDocumentReference/cbc:LanguageID)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-102","texto":"A UBL invoice should not include the ContractDocumentReference LocaleCode","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:ContractDocumentReference/cbc:LocaleCode)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-103","texto":"A UBL invoice should not include the ContractDocumentReference VersionID","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:ContractDocumentReference/cbc:VersionID)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-104","texto":"A UBL invoice should not include the ContractDocumentReference DocumentStatusCode","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:ContractDocumentReference/cbc:DocumentStatusCode)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-105","texto":"A UBL invoice should not include the ContractDocumentReference DocumentDescription","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:ContractDocumentReference/cbc:DocumentDescription)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-106","texto":"A UBL invoice should not include the ContractDocumentReference Attachment","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:ContractDocumentReference/cac:Attachment)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-107","texto":"A UBL invoice should not include the ContractDocumentReference ValidityPeriod","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:ContractDocumentReference/cac:ValidityPeriod)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-108","texto":"A UBL invoice should not include the ContractDocumentReference IssuerParty","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:ContractDocumentReference/cac:IssuerParty)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-109","texto":"A UBL invoice should not include the ContractDocumentReference ResultOfVerification","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:ContractDocumentReference/cac:ResultOfVerification)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-110","texto":"A UBL invoice should not include the AdditionalDocumentReference CopyIndicator","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AdditionalDocumentReference/cbc:CopyIndicator)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-111","texto":"A UBL invoice should not include the AdditionalDocumentReference UUID","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AdditionalDocumentReference/cbc:UUID)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-112","texto":"A UBL invoice should not include the AdditionalDocumentReference IssueDate","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AdditionalDocumentReference/cbc:IssueDate)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-113","texto":"A UBL invoice should not include the AdditionalDocumentReference IssueTime","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AdditionalDocumentReference/cbc:IssueTime)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-114","texto":"A UBL invoice should not include the AdditionalDocumentReference DocumentType","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AdditionalDocumentReference/cbc:DocumentType)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-115","texto":"A UBL invoice should not include the AdditionalDocumentReference Xpath","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AdditionalDocumentReference/cbc:Xpath)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-116","texto":"A UBL invoice should not include the AdditionalDocumentReference LanguageID","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AdditionalDocumentReference/cbc:LanguageID)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-117","texto":"A UBL invoice should not include the AdditionalDocumentReference LocaleCode","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AdditionalDocumentReference/cbc:LocaleCode)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-118","texto":"A UBL invoice should not include the AdditionalDocumentReference VersionID","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AdditionalDocumentReference/cbc:VersionID)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-119","texto":"A UBL invoice should not include the AdditionalDocumentReference DocumentStatusCode","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AdditionalDocumentReference/cbc:DocumentStatusCode)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-121","texto":"A UBL invoice should not include the AdditionalDocumentReference Attachment External DocumentHash","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AdditionalDocumentReference/cac:Attachment/cac:ExternalReference/cbc:DocumentHash)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-122","texto":"A UBL invoice should not include the AdditionalDocumentReference Attachment External HashAlgorithmMethod","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AdditionalDocumentReference/cac:Attachment/cac:ExternalReference/cbc:HashAlgorithmMethod)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-123","texto":"A UBL invoice should not include the AdditionalDocumentReference Attachment External ExpiryDate","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AdditionalDocumentReference/cac:Attachment/cac:ExternalReference/cbc:ExpiryDate)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-124","texto":"A UBL invoice should not include the AdditionalDocumentReference Attachment External ExpiryTime","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AdditionalDocumentReference/cac:Attachment/cac:ExternalReference/cbc:ExpiryTime)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-125","texto":"A UBL invoice should not include the AdditionalDocumentReference Attachment External MimeCode","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AdditionalDocumentReference/cac:Attachment/cac:ExternalReference/cbc:MimeCode)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-127","texto":"A UBL invoice should not include the AdditionalDocumentReference Attachment External EncodingCode","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AdditionalDocumentReference/cac:Attachment/cac:ExternalReference/cbc:EncodingCode)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-129","texto":"A UBL invoice should not include the AdditionalDocumentReference Attachment External FileName","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AdditionalDocumentReference/cac:Attachment/cac:ExternalReference/cbc:FileName)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-130","texto":"A UBL invoice should not include the AdditionalDocumentReference Attachment External Descriprion","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AdditionalDocumentReference/cac:Attachment/cac:ExternalReference/cbc:Description)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-131","texto":"A UBL invoice should not include the AdditionalDocumentReference ValidityPeriod","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AdditionalDocumentReference/cac:ValidityPeriod)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-132","texto":"A UBL invoice should not include the AdditionalDocumentReference IssuerParty","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AdditionalDocumentReference/cac:IssuerParty)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-133","texto":"A UBL invoice should not include the AdditionalDocumentReference ResultOfVerification","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AdditionalDocumentReference/cac:ResultOfVerification)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-134","texto":"A UBL invoice should not include the ProjectReference UUID","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:ProjectReference/cbc:UUID)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-135","texto":"A UBL invoice should not include the ProjectReference IssueDate","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:ProjectReference/cbc:IssueDate)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-136","texto":"A UBL invoice should not include the ProjectReference WorkPhaseReference","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:ProjectReference/cac:WorkPhaseReference)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-137","texto":"A UBL invoice should not include the Signature","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:Signature)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-138","texto":"A UBL invoice should not include the AccountingSupplierParty CustomerAssignedAccountID","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingSupplierParty/cbc:CustomerAssignedAccountID)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-139","texto":"A UBL invoice should not include the AccountingSupplierParty AdditionalAccountID","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingSupplierParty/cbc:AdditionalAccountID)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-140","texto":"A UBL invoice should not include the AccountingSupplierParty DataSendingCapability","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingSupplierParty/cbc:DataSendingCapability)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-141","texto":"A UBL invoice should not include the AccountingSupplierParty Party MarkCareIndicator","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingSupplierParty/cac:Party/cbc:MarkCareIndicator)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-142","texto":"A UBL invoice should not include the AccountingSupplierParty Party MarkAttentionIndicator","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingSupplierParty/cac:Party/cbc:MarkAttentionIndicator)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-143","texto":"A UBL invoice should not include the AccountingSupplierParty Party WebsiteURI","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingSupplierParty/cac:Party/cbc:WebsiteURI)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-144","texto":"A UBL invoice should not include the AccountingSupplierParty Party LogoReferenceID","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingSupplierParty/cac:Party/cbc:LogoReferenceID)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-145","texto":"A UBL invoice should not include the AccountingSupplierParty Party IndustryClassificationCode","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingSupplierParty/cac:Party/cbc:IndustryClassificationCode)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-146","texto":"A UBL invoice should not include the AccountingSupplierParty Party Language","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingSupplierParty/cac:Party/cac:Language)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-147","texto":"A UBL invoice should not include the AccountingSupplierParty Party PostalAddress ID","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingSupplierParty/cac:Party/cac:PostalAddress/cbc:ID)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-148","texto":"A UBL invoice should not include the AccountingSupplierParty Party PostalAddress AddressTypeCode","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingSupplierParty/cac:Party/cac:PostalAddress/cbc:AddressTypeCode)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-150","texto":"A UBL invoice should not include the AccountingSupplierParty Party PostalAddress Postbox","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingSupplierParty/cac:Party/cac:PostalAddress/cbc:Postbox)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-151","texto":"A UBL invoice should not include the AccountingSupplierParty Party PostalAddress Floor","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingSupplierParty/cac:Party/cac:PostalAddress/cbc:Floor)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-152","texto":"A UBL invoice should not include the AccountingSupplierParty Party PostalAddress Room","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingSupplierParty/cac:Party/cac:PostalAddress/cbc:Room)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-153","texto":"A UBL invoice should not include the AccountingSupplierParty Party PostalAddress BlockName","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingSupplierParty/cac:Party/cac:PostalAddress/cbc:BlockName)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-154","texto":"A UBL invoice should not include the AccountingSupplierParty Party PostalAddress BuildingName","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingSupplierParty/cac:Party/cac:PostalAddress/cbc:BuildingName)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-155","texto":"A UBL invoice should not include the AccountingSupplierParty Party PostalAddress BuildingNumber","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingSupplierParty/cac:Party/cac:PostalAddress/cbc:BuildingNumber)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-156","texto":"A UBL invoice should not include the AccountingSupplierParty Party PostalAddress InhouseMail","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingSupplierParty/cac:Party/cac:PostalAddress/cbc:InhouseMail)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-157","texto":"A UBL invoice should not include the AccountingSupplierParty Party PostalAddress Department","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingSupplierParty/cac:Party/cac:PostalAddress/cbc:Department)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-158","texto":"A UBL invoice should not include the AccountingSupplierParty Party PostalAddress MarkAttention","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingSupplierParty/cac:Party/cac:PostalAddress/cbc:MarkAttention)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-159","texto":"A UBL invoice should not include the AccountingSupplierParty Party PostalAddress MarkCare","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingSupplierParty/cac:Party/cac:PostalAddress/cbc:MarkCare)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-160","texto":"A UBL invoice should not include the AccountingSupplierParty Party PostalAddress PlotIdentification","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingSupplierParty/cac:Party/cac:PostalAddress/cbc:PlotIdentification)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-161","texto":"A UBL invoice should not include the AccountingSupplierParty Party PostalAddress CitySubdivisionName","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingSupplierParty/cac:Party/cac:PostalAddress/cbc:CitySubdivisionName)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-162","texto":"A UBL invoice should not include the AccountingSupplierParty Party PostalAddress CountrySubentityCode","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingSupplierParty/cac:Party/cac:PostalAddress/cbc:CountrySubentityCode)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-163","texto":"A UBL invoice should not include the AccountingSupplierParty Party PostalAddress Region","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingSupplierParty/cac:Party/cac:PostalAddress/cbc:Region)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-164","texto":"A UBL invoice should not include the AccountingSupplierParty Party PostalAddress District","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingSupplierParty/cac:Party/cac:PostalAddress/cbc:District)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-165","texto":"A UBL invoice should not include the AccountingSupplierParty Party PostalAddress TimezoneOffset","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingSupplierParty/cac:Party/cac:PostalAddress/cbc:TimezoneOffset)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-166","texto":"A UBL invoice should not include the AccountingSupplierParty Party PostalAddress Country Name","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingSupplierParty/cac:Party/cac:PostalAddress/cac:Country/cbc:Name)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-167","texto":"A UBL invoice should not include the AccountingSupplierParty Party PostalAddress LocationCoordinate","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingSupplierParty/cac:Party/cac:PostalAddress/cac:LocationCoordinate)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-168","texto":"A UBL invoice should not include the AccountingSupplierParty Party PhysicalLocation","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingSupplierParty/cac:Party/cac:PhysicalLocation)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-169","texto":"A UBL invoice should not include the AccountingSupplierParty Party PartyTaxScheme RegistrationName","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingSupplierParty/cac:Party/cac:PartyTaxScheme/cbc:RegistrationName)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-170","texto":"A UBL invoice should not include the AccountingSupplierParty Party PartyTaxScheme TaxLevelCode","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingSupplierParty/cac:Party/cac:PartyTaxScheme/cbc:TaxLevelCode)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-171","texto":"A UBL invoice should not include the AccountingSupplierParty Party PartyTaxScheme ExemptionReasonCode","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingSupplierParty/cac:Party/cac:PartyTaxScheme/cbc:ExemptionReasonCode)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-172","texto":"A UBL invoice should not include the AccountingSupplierParty Party PartyTaxScheme ExemptionReason","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingSupplierParty/cac:Party/cac:PartyTaxScheme/cbc:ExemptionReason)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-173","texto":"A UBL invoice should not include the AccountingSupplierParty Party PartyTaxScheme RegistrationAddress","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingSupplierParty/cac:Party/cac:PartyTaxScheme/cac:RegistrationAddress)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-174","texto":"A UBL invoice should not include the AccountingSupplierParty Party PartyTaxScheme TaxScheme Name","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingSupplierParty/cac:Party/cac:PartyTaxScheme/cac:TaxScheme/cbc:Name)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-175","texto":"A UBL invoice should not include the AccountingSupplierParty Party PartyTaxScheme TaxScheme TaxTypeCode","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingSupplierParty/cac:Party/cac:PartyTaxScheme/cac:TaxScheme/cbc:TaxTypeCode)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-176","texto":"A UBL invoice should not include the AccountingSupplierParty Party PartyTaxScheme TaxScheme CurrencyCode","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingSupplierParty/cac:Party/cac:PartyTaxScheme/cac:TaxScheme/cbc:CurrencyCode)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-177","texto":"A UBL invoice should not include the AccountingSupplierParty Party PartyTaxScheme TaxScheme JurisdictionRegionAddress","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingSupplierParty/cac:Party/cac:PartyTaxScheme/cac:TaxScheme/cac:JurisdictionRegionAddress)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-178","texto":"A UBL invoice should not include the AccountingSupplierParty Party PartyLegalEntity RegistrationDate","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingSupplierParty/cac:Party/cac:PartyLegalEntity/cbc:RegistrationDate)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-179","texto":"A UBL invoice should not include the AccountingSupplierParty Party PartyLegalEntity RegistrationExpirationDate","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingSupplierParty/cac:Party/cac:PartyLegalEntity/cbc:RegistrationExpirationDate)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-180","texto":"A UBL invoice should not include the AccountingSupplierParty Party PartyLegalEntity CompanyLegalFormCode","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingSupplierParty/cac:Party/cac:PartyLegalEntity/cbc:CompanyLegalFormCode)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-181","texto":"A UBL invoice should not include the AccountingSupplierParty Party PartyLegalEntity SoleProprietorshipIndicator","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingSupplierParty/cac:Party/cac:PartyLegalEntity/cbc:SoleProprietorshipIndicator)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-182","texto":"A UBL invoice should not include the AccountingSupplierParty Party PartyLegalEntity CompanyLiquidationStatusCode","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingSupplierParty/cac:Party/cac:PartyLegalEntity/cbc:CompanyLiquidationStatusCode)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-183","texto":"A UBL invoice should not include the AccountingSupplierParty Party PartyLegalEntity CorporationStockAmount","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingSupplierParty/cac:Party/cac:PartyLegalEntity/cbc:CorporationStockAmount)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-184","texto":"A UBL invoice should not include the AccountingSupplierParty Party PartyLegalEntity FullyPaidSharesIndicator","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingSupplierParty/cac:Party/cac:PartyLegalEntity/cbc:FullyPaidSharesIndicator)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-185","texto":"A UBL invoice should not include the AccountingSupplierParty Party PartyLegalEntity RegistrationAddress","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingSupplierParty/cac:Party/cac:PartyLegalEntity/cac:RegistrationAddress)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-186","texto":"A UBL invoice should not include the AccountingSupplierParty Party PartyLegalEntity CorporateRegistrationScheme","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingSupplierParty/cac:Party/cac:PartyLegalEntity/cac:CorporateRegistrationScheme)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-187","texto":"A UBL invoice should not include the AccountingSupplierParty Party PartyLegalEntity HeadOfficeParty","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingSupplierParty/cac:Party/cac:PartyLegalEntity/cac:HeadOfficeParty)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-188","texto":"A UBL invoice should not include the AccountingSupplierParty Party PartyLegalEntity ShareholderParty","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingSupplierParty/cac:Party/cac:PartyLegalEntity/cac:ShareholderParty)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-189","texto":"A UBL invoice should not include the AccountingSupplierParty Party Contact ID","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingSupplierParty/cac:Party/cac:Contact/cbc:ID)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-190","texto":"A UBL invoice should not include the AccountingSupplierParty Party Contact Telefax","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingSupplierParty/cac:Party/cac:Contact/cbc:Telefax)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-191","texto":"A UBL invoice should not include the AccountingSupplierParty Party Contact Note","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingSupplierParty/cac:Party/cac:Contact/cbc:Note)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-192","texto":"A UBL invoice should not include the AccountingSupplierParty Party Contact OtherCommunication","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingSupplierParty/cac:Party/cac:Contact/cac:OtherCommunication)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-193","texto":"A UBL invoice should not include the AccountingSupplierParty Party Person","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingSupplierParty/cac:Party/cac:Person)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-194","texto":"A UBL invoice should not include the AccountingSupplierParty Party AgentParty","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingSupplierParty/cac:Party/cac:AgentParty)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-195","texto":"A UBL invoice should not include the AccountingSupplierParty Party ServiceProviderParty","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingSupplierParty/cac:Party/cac:ServiceProviderParty)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-196","texto":"A UBL invoice should not include the AccountingSupplierParty Party PowerOfAttorney","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingSupplierParty/cac:Party/cac:PowerOfAttorney)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-197","texto":"A UBL invoice should not include the AccountingSupplierParty Party FinancialAccount","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingSupplierParty/cac:Party/cac:FinancialAccount)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-198","texto":"A UBL invoice should not include the AccountingSupplierParty DespatchContact","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingSupplierParty/cac:DespatchContact)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-199","texto":"A UBL invoice should not include the AccountingSupplierParty AccountingContact","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingSupplierParty/cac:AccountingContact)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-200","texto":"A UBL invoice should not include the AccountingSupplierParty SellerContact","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingSupplierParty/cac:SellerContact)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-201","texto":"A UBL invoice should not include the AccountingCustomerParty CustomerAssignedAccountID","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingCustomerParty/cbc:CustomerAssignedAccountID)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-202","texto":"A UBL invoice should not include the AccountingCustomerParty SupplierAssignedAccountID","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingCustomerParty/cbc:SupplierAssignedAccountID)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-203","texto":"A UBL invoice should not include the AccountingCustomerParty AdditionalAccountID","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingCustomerParty/cbc:AdditionalAccountID)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-204","texto":"A UBL invoice should not include the AccountingCustomerParty Party MarkCareIndicator","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingCustomerParty/cac:Party/cbc:MarkCareIndicator)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-205","texto":"A UBL invoice should not include the AccountingCustomerParty Party MarkAttentionIndicator","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingCustomerParty/cac:Party/cbc:MarkAttentionIndicator)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-206","texto":"A UBL invoice should not include the AccountingCustomerParty Party WebsiteURI","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingCustomerParty/cac:Party/cbc:WebsiteURI)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-207","texto":"A UBL invoice should not include the AccountingCustomerParty Party LogoReferenceID","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingCustomerParty/cac:Party/cbc:LogoReferenceID)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-208","texto":"A UBL invoice should not include the AccountingCustomerParty Party IndustryClassificationCode","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingCustomerParty/cac:Party/cbc:IndustryClassificationCode)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-209","texto":"A UBL invoice should not include the AccountingCustomerParty Party Language","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingCustomerParty/cac:Party/cac:Language)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-210","texto":"A UBL invoice should not include the AccountingCustomerParty Party PostalAddress ID","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingCustomerParty/cac:Party/cac:PostalAddress/cbc:ID)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-211","texto":"A UBL invoice should not include the AccountingCustomerParty Party PostalAddress AddressTypeCode","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingCustomerParty/cac:Party/cac:PostalAddress/cbc:AddressTypeCode)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-213","texto":"A UBL invoice should not include the AccountingCustomerParty Party PostalAddress Postbox","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingCustomerParty/cac:Party/cac:PostalAddress/cbc:Postbox)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-214","texto":"A UBL invoice should not include the AccountingCustomerParty Party PostalAddress Floor","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingCustomerParty/cac:Party/cac:PostalAddress/cbc:Floor)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-215","texto":"A UBL invoice should not include the AccountingCustomerParty Party PostalAddress Room","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingCustomerParty/cac:Party/cac:PostalAddress/cbc:Room)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-216","texto":"A UBL invoice should not include the AccountingCustomerParty Party PostalAddress BlockName","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingCustomerParty/cac:Party/cac:PostalAddress/cbc:BlockName)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-217","texto":"A UBL invoice should not include the AccountingCustomerParty Party PostalAddress BuildingName","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingCustomerParty/cac:Party/cac:PostalAddress/cbc:BuildingName)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-218","texto":"A UBL invoice should not include the AccountingCustomerParty Party PostalAddress BuildingNumber","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingCustomerParty/cac:Party/cac:PostalAddress/cbc:BuildingNumber)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-219","texto":"A UBL invoice should not include the AccountingCustomerParty Party PostalAddress InhouseMail","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingCustomerParty/cac:Party/cac:PostalAddress/cbc:InhouseMail)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-220","texto":"A UBL invoice should not include the AccountingCustomerParty Party PostalAddress Department","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingCustomerParty/cac:Party/cac:PostalAddress/cbc:Department)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-221","texto":"A UBL invoice should not include the AccountingCustomerParty Party PostalAddress MarkAttention","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingCustomerParty/cac:Party/cac:PostalAddress/cbc:MarkAttention)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-222","texto":"A UBL invoice should not include the AccountingCustomerParty Party PostalAddress MarkCare","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingCustomerParty/cac:Party/cac:PostalAddress/cbc:MarkCare)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-223","texto":"A UBL invoice should not include the AccountingCustomerParty Party PostalAddress PlotIdentification","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingCustomerParty/cac:Party/cac:PostalAddress/cbc:PlotIdentification)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-224","texto":"A UBL invoice should not include the AccountingCustomerParty Party PostalAddress CitySubdivisionName","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingCustomerParty/cac:Party/cac:PostalAddress/cbc:CitySubdivisionName)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-225","texto":"A UBL invoice should not include the AccountingCustomerParty Party PostalAddress CountrySubentityCode","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingCustomerParty/cac:Party/cac:PostalAddress/cbc:CountrySubentityCode)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-226","texto":"A UBL invoice should not include the AccountingCustomerParty Party PostalAddress Region","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingCustomerParty/cac:Party/cac:PostalAddress/cbc:Region)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-227","texto":"A UBL invoice should not include the AccountingCustomerParty Party PostalAddress District","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingCustomerParty/cac:Party/cac:PostalAddress/cbc:District)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-228","texto":"A UBL invoice should not include the AccountingCustomerParty Party PostalAddress TimezoneOffset","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingCustomerParty/cac:Party/cac:PostalAddress/cbc:TimezoneOffset)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-229","texto":"A UBL invoice should not include the AccountingCustomerParty Party PostalAddress Country Name","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingCustomerParty/cac:Party/cac:PostalAddress/cac:Country/cbc:Name)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-230","texto":"A UBL invoice should not include the AccountingCustomerParty Party PostalAddress LocationCoordinate","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingCustomerParty/cac:Party/cac:PostalAddress/cac:LocationCoordinate)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-231","texto":"A UBL invoice should not include the AccountingCustomerParty Party PhysicalLocation","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingCustomerParty/cac:Party/cac:PhysicalLocation)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-232","texto":"A UBL invoice should not include the AccountingCustomerParty Party PartyTaxScheme RegistrationName","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingCustomerParty/cac:Party/cac:PartyTaxScheme/cbc:RegistrationName)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-233","texto":"A UBL invoice should not include the AccountingCustomerParty Party PartyTaxScheme TaxLevelCode","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingCustomerParty/cac:Party/cac:PartyTaxScheme/cbc:TaxLevelCode)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-234","texto":"A UBL invoice should not include the AccountingCustomerParty Party PartyTaxScheme ExemptionReasonCode","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingCustomerParty/cac:Party/cac:PartyTaxScheme/cbc:ExemptionReasonCode)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-235","texto":"A UBL invoice should not include the AccountingCustomerParty Party PartyTaxScheme ExemptionReason","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingCustomerParty/cac:Party/cac:PartyTaxScheme/cbc:ExemptionReason)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-236","texto":"A UBL invoice should not include the AccountingCustomerParty Party PartyTaxScheme RegistrationAddress","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingCustomerParty/cac:Party/cac:PartyTaxScheme/cac:RegistrationAddress)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-237","texto":"A UBL invoice should not include the AccountingCustomerParty Party PartyTaxScheme TaxScheme Name","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingCustomerParty/cac:Party/cac:PartyTaxScheme/cac:TaxScheme/cbc:Name)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-238","texto":"A UBL invoice should not include the AccountingCustomerParty Party PartyTaxScheme TaxScheme TaxTypeCode","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingCustomerParty/cac:Party/cac:PartyTaxScheme/cac:TaxScheme/cbc:TaxTypeCode)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-239","texto":"A UBL invoice should not include the AccountingCustomerParty Party PartyTaxScheme TaxScheme CurrencyCode","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingCustomerParty/cac:Party/cac:PartyTaxScheme/cac:TaxScheme/cbc:CurrencyCode)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-240","texto":"A UBL invoice should not include the AccountingCustomerParty Party PartyTaxScheme TaxScheme JurisdictionRegionAddress","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingCustomerParty/cac:Party/cac:PartyTaxScheme/cac:TaxScheme/cac:JurisdictionRegionAddress)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-241","texto":"A UBL invoice should not include the AccountingCustomerParty Party PartyLegalEntity RegistrationDate","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingCustomerParty/cac:Party/cac:PartyLegalEntity/cbc:RegistrationDate)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-242","texto":"A UBL invoice should not include the AccountingCustomerParty Party PartyLegalEntity RegistrationExpirationDate","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingCustomerParty/cac:Party/cac:PartyLegalEntity/cbc:RegistrationExpirationDate)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-243","texto":"A UBL invoice should not include the AccountingCustomerParty Party PartyLegalEntity CompanyLegalFormCode","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingCustomerParty/cac:Party/cac:PartyLegalEntity/cbc:CompanyLegalFormCode)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-244","texto":"A UBL invoice should not include the AccountingCustomerParty Party PartyLegalEntity CompanyLegalForm","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingCustomerParty/cac:Party/cac:PartyLegalEntity/cbc:CompanyLegalForm)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-245","texto":"A UBL invoice should not include the AccountingCustomerParty Party PartyLegalEntity SoleProprietorshipIndicator","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingCustomerParty/cac:Party/cac:PartyLegalEntity/cbc:SoleProprietorshipIndicator)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-246","texto":"A UBL invoice should not include the AccountingCustomerParty Party PartyLegalEntity CompanyLiquidationStatusCode","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingCustomerParty/cac:Party/cac:PartyLegalEntity/cbc:CompanyLiquidationStatusCode)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-247","texto":"A UBL invoice should not include the AccountingCustomerParty Party PartyLegalEntity CorporationStockAmount","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingCustomerParty/cac:Party/cac:PartyLegalEntity/cbc:CorporationStockAmount)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-248","texto":"A UBL invoice should not include the AccountingCustomerParty Party PartyLegalEntity FullyPaidSharesIndicator","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingCustomerParty/cac:Party/cac:PartyLegalEntity/cbc:FullyPaidSharesIndicator)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-249","texto":"A UBL invoice should not include the AccountingCustomerParty Party PartyLegalEntity RegistrationAddress","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingCustomerParty/cac:Party/cac:PartyLegalEntity/cac:RegistrationAddress)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-250","texto":"A UBL invoice should not include the AccountingCustomerParty Party PartyLegalEntity CorporateRegistrationScheme","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingCustomerParty/cac:Party/cac:PartyLegalEntity/cac:CorporateRegistrationScheme)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-251","texto":"A UBL invoice should not include the AccountingCustomerParty Party PartyLegalEntity HeadOfficeParty","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingCustomerParty/cac:Party/cac:PartyLegalEntity/cac:HeadOfficeParty)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-252","texto":"A UBL invoice should not include the AccountingCustomerParty Party PartyLegalEntity ShareholderParty","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingCustomerParty/cac:Party/cac:PartyLegalEntity/cac:ShareholderParty)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-253","texto":"A UBL invoice should not include the AccountingCustomerParty Party Contact ID","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingCustomerParty/cac:Party/cac:Contact/cbc:ID)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-254","texto":"A UBL invoice should not include the AccountingCustomerParty Party Contact Telefax","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingCustomerParty/cac:Party/cac:Contact/cbc:Telefax)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-255","texto":"A UBL invoice should not include the AccountingCustomerParty Party Contact Note","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingCustomerParty/cac:Party/cac:Contact/cbc:Note)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-256","texto":"A UBL invoice should not include the AccountingCustomerParty Party Contact OtherCommunication","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingCustomerParty/cac:Party/cac:Contact/cac:OtherCommunication)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-257","texto":"A UBL invoice should not include the AccountingCustomerParty Party Person","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingCustomerParty/cac:Party/cac:Person)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-258","texto":"A UBL invoice should not include the AccountingCustomerParty Party AgentParty","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingCustomerParty/cac:Party/cac:AgentParty)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-259","texto":"A UBL invoice should not include the AccountingCustomerParty Party ServiceProviderParty","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingCustomerParty/cac:Party/cac:ServiceProviderParty)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-260","texto":"A UBL invoice should not include the AccountingCustomerParty Party PowerOfAttorney","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingCustomerParty/cac:Party/cac:PowerOfAttorney)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-261","texto":"A UBL invoice should not include the AccountingCustomerParty Party FinancialAccount","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingCustomerParty/cac:Party/cac:FinancialAccount)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-262","texto":"A UBL invoice should not include the AccountingCustomerParty DeliveryContact","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingCustomerParty/cac:DeliveryContact)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-263","texto":"A UBL invoice should not include the AccountingCustomerParty AccountingContact","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingCustomerParty/cac:AccountingContact)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-264","texto":"A UBL invoice should not include the AccountingCustomerParty BuyerContact","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AccountingCustomerParty/cac:BuyerContact)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-265","texto":"A UBL invoice should not include the PayeeParty MarkCareIndicator","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:PayeeParty/cbc:MarkCareIndicator)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-266","texto":"A UBL invoice should not include the PayeeParty MarkAttentionIndicator","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:PayeeParty/cbc:MarkAttentionIndicator)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-267","texto":"A UBL invoice should not include the PayeeParty WebsiteURI","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:PayeeParty/cbc:WebsiteURI)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-268","texto":"A UBL invoice should not include the PayeeParty LogoReferenceID","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:PayeeParty/cbc:LogoReferenceID)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-269","texto":"A UBL invoice should not include the PayeeParty EndpointID","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:PayeeParty/cbc:EndpointID)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-270","texto":"A UBL invoice should not include the PayeeParty IndustryClassificationCode","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:PayeeParty/cbc:IndustryClassificationCode)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-271","texto":"A UBL invoice should not include the PayeeParty Language","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:PayeeParty/cac:Language)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-272","texto":"A UBL invoice should not include the PayeeParty PostalAddress","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:PayeeParty/cac:PostalAddress)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-273","texto":"A UBL invoice should not include the PayeeParty PhysicalLocation","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:PayeeParty/cac:PhysicalLocation)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-274","texto":"A UBL invoice should not include the PayeeParty PartyTaxScheme","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:PayeeParty/cac:PartyTaxScheme)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-275","texto":"A UBL invoice should not include the PayeeParty PartyLegalEntity RegistrationName","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:PayeeParty/cac:PartyLegalEntity/cbc:RegistrationName)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-276","texto":"A UBL invoice should not include the PayeeParty PartyLegalEntity RegistrationDate","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:PayeeParty/cac:PartyLegalEntity/cbc:RegistrationDate)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-277","texto":"A UBL invoice should not include the PayeeParty PartyLegalEntity RegistrationExpirationDate","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:PayeeParty/cac:PartyLegalEntity/cbc:RegistrationExpirationDate)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-278","texto":"A UBL invoice should not include the PayeeParty PartyLegalEntity CompanyLegalFormCode","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:PayeeParty/cac:PartyLegalEntity/cbc:CompanyLegalFormCode)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-279","texto":"A UBL invoice should not include the PayeeParty PartyLegalEntity CompanyLegalForm","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:PayeeParty/cac:PartyLegalEntity/cbc:CompanyLegalForm)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-280","texto":"A UBL invoice should not include the PayeeParty PartyLegalEntity SoleProprietorshipIndicator","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:PayeeParty/cac:PartyLegalEntity/cbc:SoleProprietorshipIndicator)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-281","texto":"A UBL invoice should not include the PayeeParty PartyLegalEntity CompanyLiquidationStatusCode","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:PayeeParty/cac:PartyLegalEntity/cbc:CompanyLiquidationStatusCode)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-282","texto":"A UBL invoice should not include the PayeeParty PartyLegalEntity CorporationStockAmount","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:PayeeParty/cac:PartyLegalEntity/cbc:CorporationStockAmount)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-283","texto":"A UBL invoice should not include the PayeeParty PartyLegalEntity FullyPaidSharesIndicator","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:PayeeParty/cac:PartyLegalEntity/cbc:FullyPaidSharesIndicator)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-284","texto":"A UBL invoice should not include the PayeeParty PartyLegalEntity RegistrationAddress","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:PayeeParty/cac:PartyLegalEntity/cac:RegistrationAddress)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-285","texto":"A UBL invoice should not include the PayeeParty PartyLegalEntity CorporateRegistrationScheme","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:PayeeParty/cac:PartyLegalEntity/cac:CorporateRegistrationScheme)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-286","texto":"A UBL invoice should not include the PayeeParty PartyLegalEntity HeadOfficeParty","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:PayeeParty/cac:PartyLegalEntity/cac:HeadOfficeParty)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-287","texto":"A UBL invoice should not include the PayeeParty PartyLegalEntity ShareholderParty","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:PayeeParty/cac:PartyLegalEntity/cac:ShareholderParty)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-288","texto":"A UBL invoice should not include the PayeeParty Contact","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:PayeeParty/cac:Contact)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-289","texto":"A UBL invoice should not include the PayeeParty Person","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:PayeeParty/cac:Person)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-290","texto":"A UBL invoice should not include the PayeeParty AgentParty","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:PayeeParty/cac:AgentParty)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-291","texto":"A UBL invoice should not include the PayeeParty ServiceProviderParty","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:PayeeParty/cac:ServiceProviderParty)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-292","texto":"A UBL invoice should not include the PayeeParty PowerOfAttorney","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:PayeeParty/cac:PowerOfAttorney)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-293","texto":"A UBL invoice should not include the PayeeParty FinancialAccount","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:PayeeParty/cac:FinancialAccount)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-294","texto":"A UBL invoice should not include the BuyerCustomerParty","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:BuyerCustomerParty)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-295","texto":"A UBL invoice should not include the SellerCustomerParty","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:SellerCustomerParty)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-296","texto":"A UBL invoice should not include the TaxRepresentativeParty MarkCareIndicator","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:TaxRepresentativeParty/cbc:MarkCareIndicator)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-297","texto":"A UBL invoice should not include the TaxRepresentativeParty MarkAttentionIndicator","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:TaxRepresentativeParty/cbc:MarkAttentionIndicator)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-298","texto":"A UBL invoice should not include the TaxRepresentativeParty WebsiteURI","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:TaxRepresentativeParty/cbc:WebsiteURI)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-299","texto":"A UBL invoice should not include the TaxRepresentativeParty LogoReferenceID","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:TaxRepresentativeParty/cbc:LogoReferenceID)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-300","texto":"A UBL invoice should not include the TaxRepresentativeParty EndpointID","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:TaxRepresentativeParty/cbc:EndpointID)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-301","texto":"A UBL invoice should not include the TaxRepresentativeParty IndustryClassificationCode","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:TaxRepresentativeParty/cbc:IndustryClassificationCode)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-302","texto":"A UBL invoice should not include the TaxRepresentativeParty PartyIdentification","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:TaxRepresentativeParty/cac:PartyIdentification)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-303","texto":"A UBL invoice should not include the TaxRepresentativeParty Language","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:TaxRepresentativeParty/cac:Language)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-304","texto":"A UBL invoice should not include the TaxRepresentativeParty PostalAddress ID","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:TaxRepresentativeParty/cac:PostalAddress/cbc:ID)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-305","texto":"A UBL invoice should not include the TaxRepresentativeParty PostalAddress AddressTypeCode","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:TaxRepresentativeParty/cac:PostalAddress/cbc:AddressTypeCode)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-307","texto":"A UBL invoice should not include the TaxRepresentativeParty PostalAddress Postbox","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:TaxRepresentativeParty/cac:PostalAddress/cbc:Postbox)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-308","texto":"A UBL invoice should not include the TaxRepresentativeParty PostalAddress Floor","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:TaxRepresentativeParty/cac:PostalAddress/cbc:Floor)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-309","texto":"A UBL invoice should not include the TaxRepresentativeParty PostalAddress Room","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:TaxRepresentativeParty/cac:PostalAddress/cbc:Room)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-310","texto":"A UBL invoice should not include the TaxRepresentativeParty PostalAddress BlockName","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:TaxRepresentativeParty/cac:PostalAddress/cbc:BlockName)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-311","texto":"A UBL invoice should not include the TaxRepresentativeParty PostalAddress BuildingName","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:TaxRepresentativeParty/cac:PostalAddress/cbc:BuildingName)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-312","texto":"A UBL invoice should not include the TaxRepresentativeParty PostalAddress BuildingNumber","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:TaxRepresentativeParty/cac:PostalAddress/cbc:BuildingNumber)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-313","texto":"A UBL invoice should not include the TaxRepresentativeParty PostalAddress InhouseMail","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:TaxRepresentativeParty/cac:PostalAddress/cbc:InhouseMail)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-314","texto":"A UBL invoice should not include the TaxRepresentativeParty PostalAddress Department","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:TaxRepresentativeParty/cac:PostalAddress/cbc:Department)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-315","texto":"A UBL invoice should not include the TaxRepresentativeParty PostalAddress MarkAttention","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:TaxRepresentativeParty/cac:PostalAddress/cbc:MarkAttention)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-316","texto":"A UBL invoice should not include the TaxRepresentativeParty PostalAddress MarkCare","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:TaxRepresentativeParty/cac:PostalAddress/cbc:MarkCare)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-317","texto":"A UBL invoice should not include the TaxRepresentativeParty PostalAddress PlotIdentification","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:TaxRepresentativeParty/cac:PostalAddress/cbc:PlotIdentification)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-318","texto":"A UBL invoice should not include the TaxRepresentativeParty PostalAddress CitySubdivisionName","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:TaxRepresentativeParty/cac:PostalAddress/cbc:CitySubdivisionName)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-319","texto":"A UBL invoice should not include the TaxRepresentativeParty PostalAddress CountrySubentityCode","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:TaxRepresentativeParty/cac:PostalAddress/cbc:CountrySubentityCode)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-320","texto":"A UBL invoice should not include the TaxRepresentativeParty PostalAddress Region","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:TaxRepresentativeParty/cac:PostalAddress/cbc:Region)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-321","texto":"A UBL invoice should not include the TaxRepresentativeParty PostalAddress District","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:TaxRepresentativeParty/cac:PostalAddress/cbc:District)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-322","texto":"A UBL invoice should not include the TaxRepresentativeParty PostalAddress TimezoneOffset","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:TaxRepresentativeParty/cac:PostalAddress/cbc:TimezoneOffset)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-323","texto":"A UBL invoice should not include the TaxRepresentativeParty PostalAddress Country Name","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:TaxRepresentativeParty/cac:PostalAddress/cac:Country/cbc:Name)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-324","texto":"A UBL invoice should not include the TaxRepresentativeParty PostalAddress LocationCoordinate","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:TaxRepresentativeParty/cac:PostalAddress/cac:LocationCoordinate)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-325","texto":"A UBL invoice should not include the TaxRepresentativeParty PhysicalLocation","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:TaxRepresentativeParty/cac:PhysicalLocation)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-326","texto":"A UBL invoice should not include the TaxRepresentativeParty PartyTaxScheme RegistrationName","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:TaxRepresentativeParty/cac:PartyTaxScheme/cbc:RegistrationName)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-327","texto":"A UBL invoice should not include the TaxRepresentativeParty PartyTaxScheme TaxLevelCode","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:TaxRepresentativeParty/cac:PartyTaxScheme/cbc:TaxLevelCode)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-328","texto":"A UBL invoice should not include the TaxRepresentativeParty PartyTaxScheme ExemptionReasonCode","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:TaxRepresentativeParty/cac:PartyTaxScheme/cbc:ExemptionReasonCode)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-329","texto":"A UBL invoice should not include the TaxRepresentativeParty PartyTaxScheme ExemptionReason","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:TaxRepresentativeParty/cac:PartyTaxScheme/cbc:ExemptionReason)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-330","texto":"A UBL invoice should not include the TaxRepresentativeParty PartyTaxScheme RegistrationAddress","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:TaxRepresentativeParty/cac:PartyTaxScheme/cac:RegistrationAddress)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-331","texto":"A UBL invoice should not include the TaxRepresentativeParty PartyTaxScheme TaxScheme Name","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:TaxRepresentativeParty/cac:PartyTaxScheme/cac:TaxScheme/cbc:Name)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-332","texto":"A UBL invoice should not include the TaxRepresentativeParty PartyTaxScheme TaxScheme TaxTypeCode","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:TaxRepresentativeParty/cac:PartyTaxScheme/cac:TaxScheme/cbc:TaxTypeCode)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-333","texto":"A UBL invoice should not include the TaxRepresentativeParty PartyTaxScheme TaxScheme CurrencyCode","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:TaxRepresentativeParty/cac:PartyTaxScheme/cac:TaxScheme/cbc:CurrencyCode)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-334","texto":"A UBL invoice should not include the TaxRepresentativeParty PartyTaxScheme TaxScheme JurisdictionRegionAddress","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:TaxRepresentativeParty/cac:PartyTaxScheme/cac:TaxScheme/cac:JurisdictionRegionAddress)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-335","texto":"A UBL invoice should not include the TaxRepresentativeParty PartyLegalEntity","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:TaxRepresentativeParty/cac:PartyLegalEntity)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-336","texto":"A UBL invoice should not include the TaxRepresentativeParty Contact","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:TaxRepresentativeParty/cac:Contact)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-337","texto":"A UBL invoice should not include the TaxRepresentativeParty Person","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:TaxRepresentativeParty/cac:Person)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-338","texto":"A UBL invoice should not include the TaxRepresentativeParty AgentParty","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:TaxRepresentativeParty/cac:AgentParty)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-339","texto":"A UBL invoice should not include the TaxRepresentativeParty ServiceProviderParty","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:TaxRepresentativeParty/cac:ServiceProviderParty)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-340","texto":"A UBL invoice should not include the TaxRepresentativeParty PowerOfAttorney","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:TaxRepresentativeParty/cac:PowerOfAttorney)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-341","texto":"A UBL invoice should not include the TaxRepresentativeParty FinancialAccount","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:TaxRepresentativeParty/cac:FinancialAccount)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-342","texto":"A UBL invoice should not include the Delivery ID","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:Delivery/cbc:ID)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-343","texto":"A UBL invoice should not include the Delivery Quantity","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:Delivery/cbc:Quantity)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-346","texto":"A UBL invoice should not include the Delivery ActualDeliveryTime","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:Delivery/cbc:ActualDeliveryTime)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-347","texto":"A UBL invoice should not include the Delivery LatestDeliveryDate","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:Delivery/cbc:LatestDeliveryDate)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-348","texto":"A UBL invoice should not include the Delivery LatestDeliveryTime","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:Delivery/cbc:LatestDeliveryTime)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-349","texto":"A UBL invoice should not include the Delivery ReleaseID","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:Delivery/cbc:ReleaseID)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-350","texto":"A UBL invoice should not include the Delivery TrackingID","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:Delivery/cbc:TrackingID)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-351","texto":"A UBL invoice should not include the Delivery DeliveryLocation Description","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:Delivery/cac:DeliveryLocation/cbc:Description)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-352","texto":"A UBL invoice should not include the Delivery DeliveryLocation Conditions","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:Delivery/cac:DeliveryLocation/cbc:Conditions)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-353","texto":"A UBL invoice should not include the Delivery DeliveryLocation CountrySubentity","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:Delivery/cac:DeliveryLocation/cbc:CountrySubentity)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-354","texto":"A UBL invoice should not include the Delivery DeliveryLocation CountrySubentityCode","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:Delivery/cac:DeliveryLocation/cbc:CountrySubentityCode)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-355","texto":"A UBL invoice should not include the Delivery DeliveryLocation LocationTypeCode","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:Delivery/cac:DeliveryLocation/cbc:LocationTypeCode)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-357","texto":"A UBL invoice should not include the Delivery DeliveryLocation Name","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:Delivery/cac:DeliveryLocation/cbc:Name)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-358","texto":"A UBL invoice should not include the Delivery DeliveryLocation ValidationPeriod","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:Delivery/cac:DeliveryLocation/cac:ValidationPeriod)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-359","texto":"A UBL invoice should not include the Delivery DeliveryLocation Address ID","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:Delivery/cac:DeliveryLocation/cac:Address/cbc:ID)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-360","texto":"A UBL invoice should not include the Delivery DeliveryLocation Address AddressTypeCode","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:Delivery/cac:DeliveryLocation/cac:Address/cbc:AddressTypeCode)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-362","texto":"A UBL invoice should not include the Delivery DeliveryLocation Address Postbox","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:Delivery/cac:DeliveryLocation/cac:Address/cbc:Postbox)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-363","texto":"A UBL invoice should not include the Delivery DeliveryLocation Address Floor","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:Delivery/cac:DeliveryLocation/cac:Address/cbc:Floor)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-364","texto":"A UBL invoice should not include the Delivery DeliveryLocation Address Room","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:Delivery/cac:DeliveryLocation/cac:Address/cbc:Room)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-365","texto":"A UBL invoice should not include the Delivery DeliveryLocation Address BlockName","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:Delivery/cac:DeliveryLocation/cac:Address/cbc:BlockName)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-366","texto":"A UBL invoice should not include the Delivery DeliveryLocation Address BuildingName","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:Delivery/cac:DeliveryLocation/cac:Address/cbc:BuildingName)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-367","texto":"A UBL invoice should not include the Delivery DeliveryLocation Address BuildingNumber","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:Delivery/cac:DeliveryLocation/cac:Address/cbc:BuildingNumber)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-368","texto":"A UBL invoice should not include the Delivery DeliveryLocation Address InhouseMail","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:Delivery/cac:DeliveryLocation/cac:Address/cbc:InhouseMail)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-369","texto":"A UBL invoice should not include the Delivery DeliveryLocation Address Department","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:Delivery/cac:DeliveryLocation/cac:Address/cbc:Department)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-370","texto":"A UBL invoice should not include the Delivery DeliveryLocation Address MarkAttention","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:Delivery/cac:DeliveryLocation/cac:Address/cbc:MarkAttention)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-371","texto":"A UBL invoice should not include the Delivery DeliveryLocation Address MarkCare","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:Delivery/cac:DeliveryLocation/cac:Address/cbc:MarkCare)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-372","texto":"A UBL invoice should not include the Delivery DeliveryLocation Address PlotIdentification","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:Delivery/cac:DeliveryLocation/cac:Address/cbc:PlotIdentification)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-373","texto":"A UBL invoice should not include the Delivery DeliveryLocation Address CitySubdivisionName","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:Delivery/cac:DeliveryLocation/cac:Address/cbc:CitySubdivisionName)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-374","texto":"A UBL invoice should not include the Delivery DeliveryLocation Address CountrySubentityCode","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:Delivery/cac:DeliveryLocation/cac:Address/cbc:CountrySubentityCode)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-375","texto":"A UBL invoice should not include the Delivery DeliveryLocation Address Region","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:Delivery/cac:DeliveryLocation/cac:Address/cbc:Region)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-376","texto":"A UBL invoice should not include the Delivery DeliveryLocation Address District","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:Delivery/cac:DeliveryLocation/cac:Address/cbc:District)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-377","texto":"A UBL invoice should not include the Delivery DeliveryLocation Address TimezoneOffset","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:Delivery/cac:DeliveryLocation/cac:Address/cbc:TimezoneOffset)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-378","texto":"A UBL invoice should not include the Delivery DeliveryLocation Address Country Name","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:Delivery/cac:DeliveryLocation/cac:Address/cac:Country/cbc:Name)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-379","texto":"A UBL invoice should not include the Delivery DeliveryLocation Address LocationCoordinate","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:Delivery/cac:DeliveryLocation/cac:Address/cac:LocationCoordinate)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-380","texto":"A UBL invoice should not include the Delivery DeliveryLocation SubsidiaryLocation","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:Delivery/cac:DeliveryLocation/cac:SubsidiaryLocation)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-381","texto":"A UBL invoice should not include the Delivery DeliveryLocation LocationCoordinate","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:Delivery/cac:DeliveryLocation/cac:LocationCoordinate)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-382","texto":"A UBL invoice should not include the Delivery AlternativeDeliveryLocation","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:Delivery/cac:AlternativeDeliveryLocation)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-383","texto":"A UBL invoice should not include the Delivery RequestedDeliveryPeriod","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:Delivery/cac:RequestedDeliveryPeriod)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-384","texto":"A UBL invoice should not include the Delivery PromisedDeliveryPeriod","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:Delivery/cac:PromisedDeliveryPeriod)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-385","texto":"A UBL invoice should not include the Delivery CarrierParty","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:Delivery/cac:CarrierParty)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-386","texto":"A UBL invoice should not include the DeliveryParty MarkCareIndicator","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:Delivery/cac:DeliveryParty/cbc:MarkCareIndicator)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-387","texto":"A UBL invoice should not include the DeliveryParty MarkAttentionIndicator","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:Delivery/cac:DeliveryParty/cbc:MarkAttentionIndicator)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-388","texto":"A UBL invoice should not include the DeliveryParty WebsiteURI","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:Delivery/cac:DeliveryParty/cbc:WebsiteURI)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-389","texto":"A UBL invoice should not include the DeliveryParty LogoReferenceID","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:Delivery/cac:DeliveryParty/cbc:LogoReferenceID)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-390","texto":"A UBL invoice should not include the DeliveryParty EndpointID","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:Delivery/cac:DeliveryParty/cbc:EndpointID)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-391","texto":"A UBL invoice should not include the DeliveryParty IndustryClassificationCode","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:Delivery/cac:DeliveryParty/cbc:IndustryClassificationCode)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-392","texto":"A UBL invoice should not include the DeliveryParty PartyIdentification","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:Delivery/cac:DeliveryParty/cac:PartyIdentification)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-393","texto":"A UBL invoice should not include the DeliveryParty Language","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:Delivery/cac:DeliveryParty/cac:Language)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-394","texto":"A UBL invoice should not include the DeliveryParty PostalAddress","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:Delivery/cac:DeliveryParty/cac:PostalAddress)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-395","texto":"A UBL invoice should not include the DeliveryParty PhysicalLocation","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:Delivery/cac:DeliveryParty/cac:PhysicalLocation)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-396","texto":"A UBL invoice should not include the DeliveryParty PartyTaxScheme","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:Delivery/cac:DeliveryParty/cac:PartyTaxScheme)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-397","texto":"A UBL invoice should not include the DeliveryParty PartyLegalEntity","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:Delivery/cac:DeliveryParty/cac:PartyLegalEntity)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-398","texto":"A UBL invoice should not include the DeliveryParty Contact","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:Delivery/cac:DeliveryParty/cac:Contact)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-399","texto":"A UBL invoice should not include the DeliveryParty Person","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:Delivery/cac:DeliveryParty/cac:Person)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-400","texto":"A UBL invoice should not include the DeliveryParty AgentParty","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:Delivery/cac:DeliveryParty/cac:AgentParty)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-401","texto":"A UBL invoice should not include the DeliveryParty ServiceProviderParty","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:Delivery/cac:DeliveryParty/cac:ServiceProviderParty)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-402","texto":"A UBL invoice should not include the DeliveryParty PowerOfAttorney","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:Delivery/cac:DeliveryParty/cac:PowerOfAttorney)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-403","texto":"A UBL invoice should not include the DeliveryParty FinancialAccount","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:Delivery/cac:DeliveryParty/cac:FinancialAccount)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-404","texto":"A UBL invoice should not include the Delivery NotifyParty","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:Delivery/cac:NotifyParty)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-405","texto":"A UBL invoice should not include the Delivery Despatch","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:Delivery/cac:Despatch)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-406","texto":"A UBL invoice should not include the Delivery DeliveryTerms","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:Delivery/cac:DeliveryTerms)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-409","texto":"A UBL invoice should not include the Delivery Shipment","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:Delivery/cac:Shipment)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-410","texto":"A UBL invoice should not include the DeliveryTerms","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:DeliveryTerms)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-411","texto":"A UBL invoice should not include the PaymentMeans ID","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:PaymentMeans/cbc:ID)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-412","texto":"A UBL invoice should not include the PaymentMeans PaymentDueDate","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:PaymentMeans/cbc:PaymentDueDate)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-413","texto":"A UBL invoice should not include the PaymentMeans PaymentChannelCode","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:PaymentMeans/cbc:PaymentChannelCode)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-414","texto":"A UBL invoice should not include the PaymentMeans InstructionID","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:PaymentMeans/cbc:InstructionID)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-415","texto":"A UBL invoice should not include the PaymentMeans CardAccount CardTypeCode","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:PaymentMeans/cac:CardAccount/cbc:CardTypeCode)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-416","texto":"A UBL invoice should not include the PaymentMeans CardAccount ValidityStartDate","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:PaymentMeans/cac:CardAccount/cbc:ValidityStartDate)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-417","texto":"A UBL invoice should not include the PaymentMeans CardAccount ExpiryDate","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:PaymentMeans/cac:CardAccount/cbc:ExpiryDate)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-418","texto":"A UBL invoice should not include the PaymentMeans CardAccount IssuerID","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:PaymentMeans/cac:CardAccount/cbc:IssuerID)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-419","texto":"A UBL invoice should not include the PaymentMeans CardAccount IssuerNumberID","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:PaymentMeans/cac:CardAccount/cbc:IssuerNumberID)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-420","texto":"A UBL invoice should not include the PaymentMeans CardAccount CV2ID","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:PaymentMeans/cac:CardAccount/cbc:CV2ID)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-421","texto":"A UBL invoice should not include the PaymentMeans CardAccount CardChipCode","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:PaymentMeans/cac:CardAccount/cbc:CardChipCode)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-422","texto":"A UBL invoice should not include the PaymentMeans CardAccount ChipApplicationID","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:PaymentMeans/cac:CardAccount/cbc:ChipApplicationID)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-423","texto":"A UBL invoice should not include the PaymentMeans PayerFinancialAccount","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:PaymentMeans/cac:PayerFinancialAccount)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-424","texto":"A UBL invoice should not include the PaymentMeans PayeeFinancialAccount AliasName","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:PaymentMeans/cac:PayeeFinancialAccount/cbc:AliasName)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-425","texto":"A UBL invoice should not include the PaymentMeans PayeeFinancialAccount AccountTypeCode","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:PaymentMeans/cac:PayeeFinancialAccount/cbc:AccountTypeCode)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-427","texto":"A UBL invoice should not include the PaymentMeans PayeeFinancialAccount CurrencyCode","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:PaymentMeans/cac:PayeeFinancialAccount/cbc:CurrencyCode)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-428","texto":"A UBL invoice should not include the PaymentMeans PayeeFinancialAccount PaymentNote","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:PaymentMeans/cac:PayeeFinancialAccount/cbc:PaymentNote)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-429","texto":"A UBL invoice should not include the PaymentMeans PayeeFinancialAccount FinancialInstitutionBranch Name","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:PaymentMeans/cac:PayeeFinancialAccount/cac:FinancialInstitutionBranch/cbc:Name)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-430","texto":"A UBL invoice should not include the PaymentMeans PayeeFinancialAccount FinancialInstitutionBranch FinancialInstitution Name","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:PaymentMeans/cac:PayeeFinancialAccount/cac:FinancialInstitutionBranch/cac:FinancialInstitution/cbc:Name)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-431","texto":"A UBL invoice should not include the PaymentMeans PayeeFinancialAccount FinancialInstitutionBranch FinancialInstitution Address","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:PaymentMeans/cac:PayeeFinancialAccount/cac:FinancialInstitutionBranch/cac:FinancialInstitution/cac:Address)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-432","texto":"A UBL invoice should not include the PaymentMeans PayeeFinancialAccount FinancialInstitutionBranch Address","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:PaymentMeans/cac:PayeeFinancialAccount/cac:FinancialInstitutionBranch/cac:Address)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-433","texto":"A UBL invoice should not include the PaymentMeans PayeeFinancialAccount Country","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:PaymentMeans/cac:PayeeFinancialAccount/cac:Country)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-434","texto":"A UBL invoice should not include the PaymentMeans CreditAccount","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:PaymentMeans/cac:CreditAccount)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-435","texto":"A UBL invoice should not include the PaymentMeans PaymentMandate MandateTypeCode","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:PaymentMeans/cac:PaymentMandate/cbc:MandateTypeCode)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-438","texto":"A UBL invoice should not include the PaymentMeans PaymentMandate SignatureID","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:PaymentMeans/cac:PaymentMandate/cbc:SignatureID)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-439","texto":"A UBL invoice should not include the PaymentMeans PaymentMandate PayerParty","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:PaymentMeans/cac:PaymentMandate/cac:PayerParty)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-440","texto":"A UBL invoice should not include the PaymentMeans PaymentMandate PayerFinancialAccount Name","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:PaymentMeans/cac:PaymentMandate/cac:PayerFinancialAccount/cbc:Name)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-441","texto":"A UBL invoice should not include the PaymentMeans PaymentMandate PayerFinancialAccount AliasName","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:PaymentMeans/cac:PaymentMandate/cac:PayerFinancialAccount/cbc:AliasName)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-442","texto":"A UBL invoice should not include the PaymentMeans PaymentMandate PayerFinancialAccount AccountTypeCode","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:PaymentMeans/cac:PaymentMandate/cac:PayerFinancialAccount/cbc:AccountTypeCode)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-444","texto":"A UBL invoice should not include the PaymentMeans PaymentMandate PayerFinancialAccount CurrencyCode","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:PaymentMeans/cac:PaymentMandate/cac:PayerFinancialAccount/cbc:CurrencyCode)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-445","texto":"A UBL invoice should not include the PaymentMeans PaymentMandate PayerFinancialAccount PaymentNote","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:PaymentMeans/cac:PaymentMandate/cac:PayerFinancialAccount/cbc:PaymentNote)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-446","texto":"A UBL invoice should not include the PaymentMeans PaymentMandate PayerFinancialAccount FinancialInstitutionBranch","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:PaymentMeans/cac:PaymentMandate/cac:PayerFinancialAccount/cac:FinancialInstitutionBranch)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-447","texto":"A UBL invoice should not include the PaymentMeans PaymentMandate PayerFinancialAccount Country","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:PaymentMeans/cac:PaymentMandate/cac:PayerFinancialAccount/cac:Country)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-448","texto":"A UBL invoice should not include the PaymentMeans PaymentMandate ValidityPeriod","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:PaymentMeans/cac:PaymentMandate/cac:ValidityPeriod)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-449","texto":"A UBL invoice should not include the PaymentMeans PaymentMandate PaymentReversalPeriod","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:PaymentMeans/cac:PaymentMandate/cac:PaymentReversalPeriod)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-450","texto":"A UBL invoice should not include the PaymentMeans PaymentMandate Clause","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:PaymentMeans/cac:PaymentMandate/cac:Clause)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-451","texto":"A UBL invoice should not include the PaymentMeans TradeFinancing","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:PaymentMeans/cac:TradeFinancing)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-452","texto":"A UBL invoice should not include the PaymentTerms ID","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:PaymentTerms/cbc:ID)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-453","texto":"A UBL invoice should not include the PaymentTerms PaymentMeansID","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:PaymentTerms/cbc:PaymentMeansID)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-454","texto":"A UBL invoice should not include the PaymentTerms PrepaidPaymentReferenceID","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:PaymentTerms/cbc:PrepaidPaymentReferenceID)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-455","texto":"A UBL invoice should not include the PaymentTerms ReferenceEventCode","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:PaymentTerms/cbc:ReferenceEventCode)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-456","texto":"A UBL invoice should not include the PaymentTerms SettlementDiscountPercent","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:PaymentTerms/cbc:SettlementDiscountPercent)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-457","texto":"A UBL invoice should not include the PaymentTerms PenaltySurchargePercent","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:PaymentTerms/cbc:PenaltySurchargePercent)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-458","texto":"A UBL invoice should not include the PaymentTerms PaymentPercent","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:PaymentTerms/cbc:PaymentPercent)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-459","texto":"A UBL invoice should not include the PaymentTerms Amount","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:PaymentTerms/cbc:Amount)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-460","texto":"A UBL invoice should not include the PaymentTerms SettlementDiscountAmount","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:PaymentTerms/cbc:SettlementDiscountAmount)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-461","texto":"A UBL invoice should not include the PaymentTerms PenaltyAmount","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:PaymentTerms/cbc:PenaltyAmount)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-462","texto":"A UBL invoice should not include the PaymentTerms PaymentTermsDetailsURI","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:PaymentTerms/cbc:PaymentTermsDetailsURI)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-463","texto":"A UBL invoice should not include the PaymentTerms PaymentDueDate","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:PaymentTerms/cbc:PaymentDueDate)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-464","texto":"A UBL invoice should not include the PaymentTerms InstallmentDueDate","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:PaymentTerms/cbc:InstallmentDueDate)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-465","texto":"A UBL invoice should not include the PaymentTerms InvoicingPartyReference","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:PaymentTerms/cbc:InvoicingPartyReference)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-466","texto":"A UBL invoice should not include the PaymentTerms SettlementPeriod","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:PaymentTerms/cac:SettlementPeriod)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-467","texto":"A UBL invoice should not include the PaymentTerms PenaltyPeriod","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:PaymentTerms/cac:PenaltyPeriod)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-468","texto":"A UBL invoice should not include the PaymentTerms ExchangeRate","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:PaymentTerms/cac:ExchangeRate)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-469","texto":"A UBL invoice should not include the PaymentTerms ValidityPeriod","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:PaymentTerms/cac:ValidityPeriod)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-470","texto":"A UBL invoice should not include the PrepaidPayment","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:PrepaidPayment)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-471","texto":"A UBL invoice should not include the AllowanceCharge ID","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AllowanceCharge/cbc:ID)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-472","texto":"A UBL invoice should not include the AllowanceCharge PrepaidIndicator","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AllowanceCharge/cbc:PrepaidIndicator)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-474","texto":"A UBL invoice should not include the AllowanceCharge AccountingCostCode","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AllowanceCharge/cbc:AccountingCostCode)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-475","texto":"A UBL invoice should not include the AllowanceCharge AccountingCost","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AllowanceCharge/cbc:AccountingCost)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-476","texto":"A UBL invoice should not include the AllowanceCharge PerUnitAmount","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AllowanceCharge/cbc:PerUnitAmount)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-477","texto":"A UBL invoice should not include the AllowanceCharge TaxCategory Name","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AllowanceCharge/cac:TaxCategory/cbc:Name)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-478","texto":"A UBL invoice should not include the AllowanceCharge TaxCategory BaseUnitMeasure","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AllowanceCharge/cac:TaxCategory/cbc:BaseUnitMeasure)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-479","texto":"A UBL invoice should not include the AllowanceCharge TaxCategory PerUnitAmount","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AllowanceCharge/cac:TaxCategory/cbc:PerUnitAmount)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-480","texto":"A UBL invoice should not include the AllowanceCharge TaxCategory TaxExemptionReasonCode","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AllowanceCharge/cac:TaxCategory/cbc:TaxExemptionReasonCode)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-481","texto":"A UBL invoice should not include the AllowanceCharge TaxCategory TaxExemptionReason","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AllowanceCharge/cac:TaxCategory/cbc:TaxExemptionReason)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-482","texto":"A UBL invoice should not include the AllowanceCharge TaxCategory TierRange","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AllowanceCharge/cac:TaxCategory/cbc:TierRange)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-483","texto":"A UBL invoice should not include the AllowanceCharge TaxCategory TierRatePercent","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AllowanceCharge/cac:TaxCategory/cbc:TierRatePercent)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-484","texto":"A UBL invoice should not include the AllowanceCharge TaxCategory TaxScheme Name","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AllowanceCharge/cac:TaxCategory/cac:TaxScheme/cbc:Name)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-485","texto":"A UBL invoice should not include the AllowanceCharge TaxCategory TaxScheme TaxTypeCode","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AllowanceCharge/cac:TaxCategory/cac:TaxScheme/cbc:TaxTypeCode)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-486","texto":"A UBL invoice should not include the AllowanceCharge TaxCategory TaxScheme CurrencyCode","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AllowanceCharge/cac:TaxCategory/cac:TaxScheme/cbc:CurrencyCode)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-487","texto":"A UBL invoice should not include the AllowanceCharge TaxCategory TaxScheme JurisdiccionRegionAddress","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AllowanceCharge/cac:TaxCategory/cac:TaxScheme/cac:JurisdiccionRegionAddress)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-488","texto":"A UBL invoice should not include the AllowanceCharge TaxTotal","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AllowanceCharge/cac:TaxTotal)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-489","texto":"A UBL invoice should not include the AllowanceCharge PaymentMeans","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:AllowanceCharge/cac:PaymentMeans)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-490","texto":"A UBL invoice should not include the TaxExchangeRate","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:TaxExchangeRate)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-491","texto":"A UBL invoice should not include the PricingExchangeRate","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:PricingExchangeRate)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-492","texto":"A UBL invoice should not include the PaymentExchangeRate","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:PaymentExchangeRate)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-493","texto":"A UBL invoice should not include the PaymentAlternativeExchangeRate","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:PaymentAlternativeExchangeRate)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-494","texto":"A UBL invoice should not include the TaxTotal RoundingAmount","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:TaxTotal/cbc:RoundingAmount)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-495","texto":"A UBL invoice should not include the TaxTotal TaxEvidenceIndicator","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:TaxTotal/cbc:TaxEvidenceIndicator)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-496","texto":"A UBL invoice should not include the TaxTotal TaxIncludedIndicator","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:TaxTotal/cbc:TaxIncludedIndicator)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-498","texto":"A UBL invoice should not include the TaxTotal TaxSubtotal TransactionCurrencyTaxAmount","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:TaxTotal/cac:TaxSubtotal/cbc:TransactionCurrencyTaxAmount)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-499","texto":"A UBL invoice should not include the TaxTotal TaxSubtotal Percent","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:TaxTotal/cac:TaxSubtotal/cbc:Percent)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-500","texto":"A UBL invoice should not include the TaxTotal TaxSubtotal BaseUnitMeasure","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:TaxTotal/cac:TaxSubtotal/cbc:BaseUnitMeasure)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-501","texto":"A UBL invoice should not include the TaxTotal TaxSubtotal PerUnitAmount","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:TaxTotal/cac:TaxSubtotal/cbc:PerUnitAmount)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-502","texto":"A UBL invoice should not include the TaxTotal TaxSubtotal TierRange","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:TaxTotal/cac:TaxSubtotal/cbc:TierRange)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-503","texto":"A UBL invoice should not include the TaxTotal TaxSubtotal TierRatePercent","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:TaxTotal/cac:TaxSubtotal/cbc:TierRatePercent)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-504","texto":"A UBL invoice should not include the TaxTotal TaxSubtotal TaxCategory Name","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:TaxTotal/cac:TaxSubtotal/cac:TaxCategory/cbc:Name)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-505","texto":"A UBL invoice should not include the TaxTotal TaxSubtotal TaxCategory BaseUnitMeasure","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:TaxTotal/cac:TaxSubtotal/cac:TaxCategory/cbc:BaseUnitMeasure)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-506","texto":"A UBL invoice should not include the TaxTotal TaxSubtotal TaxCategory PerUnitAmount","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:TaxTotal/cac:TaxSubtotal/cac:TaxCategory/cbc:PerUnitAmount)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-507","texto":"A UBL invoice should not include the TaxTotal TaxSubtotal TaxCategory TierRange","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:TaxTotal/cac:TaxSubtotal/cac:TaxCategory/cbc:TierRange)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-508","texto":"A UBL invoice should not include the TaxTotal TaxSubtotal TaxCategory TierRatePercent","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:TaxTotal/cac:TaxSubtotal/cac:TaxCategory/cbc:TierRatePercent)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-509","texto":"A UBL invoice should not include the TaxTotal TaxSubtotal TaxCategory TaxScheme Name","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:TaxTotal/cac:TaxSubtotal/cac:TaxCategory/cac:TaxScheme/cbc:Name)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-510","texto":"A UBL invoice should not include the TaxTotal TaxSubtotal TaxCategory TaxScheme TaxTypeCode","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:TaxTotal/cac:TaxSubtotal/cac:TaxCategory/cac:TaxScheme/cbc:TaxTypeCode)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-511","texto":"A UBL invoice should not include the TaxTotal TaxSubtotal TaxCategory TaxScheme CurrencyCode","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:TaxTotal/cac:TaxSubtotal/cac:TaxCategory/cac:TaxScheme/cbc:CurrencyCode)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-512","texto":"A UBL invoice should not include the TaxTotal TaxSubtotal TaxCategory TaxScheme JurisdiccionRegionAddress","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:TaxTotal/cac:TaxSubtotal/cac:TaxCategory/cac:TaxScheme/cac:JurisdiccionRegionAddress)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-513","texto":"A UBL invoice should not include the WithholdingTaxTotal","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:WithholdingTaxTotal)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-514","texto":"A UBL invoice should not include the LegalMonetaryTotal PayableAlternativeAmount","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:LegalMonetaryTotal/cbc:PayableAlternativeAmount)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-515","texto":"A UBL invoice should not include the InvoiceLine UUID","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cbc:UUID)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-516","texto":"A UBL invoice should not include the InvoiceLine TaxPointDate","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cbc:TaxPointDate)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-517","texto":"A UBL invoice should not include the InvoiceLine AccountingCostCode","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cbc:AccountingCostCode)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-518","texto":"A UBL invoice should not include the InvoiceLine PaymentPurposeCode","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cbc:PaymentPurposeCode)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-519","texto":"A UBL invoice should not include the InvoiceLine FreeOfChargeIndicator","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cbc:FreeOfChargeIndicator)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-520","texto":"A UBL invoice should not include the InvoiceLine InvoicePeriod StartTime","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:InvoicePeriod/cbc:StartTime)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-521","texto":"A UBL invoice should not include the InvoiceLine InvoicePeriod EndTime","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:InvoicePeriod/cbc:EndTime)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-522","texto":"A UBL invoice should not include the InvoiceLine InvoicePeriod DurationMeasure","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:InvoicePeriod/cbc:DurationMeasure)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-523","texto":"A UBL invoice should not include the InvoiceLine InvoicePeriod DescriptionCode","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:InvoicePeriod/cbc:DescriptionCode)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-524","texto":"A UBL invoice should not include the InvoiceLine InvoicePeriod Description","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:InvoicePeriod/cbc:Description)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-525","texto":"A UBL invoice should not include the InvoiceLine OrderLineReference SalesOrderLineID","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:OrderLineReference/cbc:SalesOrderLineID)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-526","texto":"A UBL invoice should not include the InvoiceLine OrderLineReference UUID","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:OrderLineReference/cbc:UUID)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-527","texto":"A UBL invoice should not include the InvoiceLine OrderLineReference LineStatusCode","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:OrderLineReference/cbc:LineStatusCode)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-528","texto":"A UBL invoice should not include the InvoiceLine OrderLineReference OrderReference","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:OrderLineReference/cbc:OrderReference)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-529","texto":"A UBL invoice should not include the InvoiceLine DespatchLineReference","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:DespatchLineReference)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-530","texto":"A UBL invoice should not include the InvoiceLine ReceiptLineReference","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:ReceiptLineReference)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-531","texto":"A UBL invoice should not include the InvoiceLine BillingReference","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:BillingReference)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-532","texto":"A UBL invoice should not include the InvoiceLine DocumentReference CopyIndicator","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:DocumentReference/cbc:CopyIndicator)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-533","texto":"A UBL invoice should not include the InvoiceLine DocumentReference UUID","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:DocumentReference/cbc:UUID)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-534","texto":"A UBL invoice should not include the InvoiceLine DocumentReference IssueDate","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:DocumentReference/cbc:IssueDate)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-535","texto":"A UBL invoice should not include the InvoiceLine DocumentReference IssueTime","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:DocumentReference/cbc:IssueTime)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-537","texto":"A UBL invoice should not include the InvoiceLine DocumentReference DocumentType","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:DocumentReference/cbc:DocumentType)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-538","texto":"A UBL invoice should not include the InvoiceLine DocumentReference Xpath","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:DocumentReference/cbc:Xpath)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-539","texto":"A UBL invoice should not include the InvoiceLine DocumentReference LanguageID","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:DocumentReference/cbc:LanguageID)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-540","texto":"A UBL invoice should not include the InvoiceLine DocumentReference LocaleCode","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:DocumentReference/cbc:LocaleCode)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-541","texto":"A UBL invoice should not include the InvoiceLine DocumentReference VersionID","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:DocumentReference/cbc:VersionID)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-542","texto":"A UBL invoice should not include the InvoiceLine DocumentReference DocumentStatusCode","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:DocumentReference/cbc:DocumentStatusCode)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-543","texto":"A UBL invoice should not include the InvoiceLine DocumentReference DocumentDescription","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:DocumentReference/cbc:DocumentDescription)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-544","texto":"A UBL invoice should not include the InvoiceLine DocumentReference Attachment","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:DocumentReference/cac:Attachment)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-545","texto":"A UBL invoice should not include the InvoiceLine DocumentReference ValidityPeriod","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:DocumentReference/cac:ValidityPeriod)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-546","texto":"A UBL invoice should not include the InvoiceLine DocumentReference IssuerParty","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:DocumentReference/cac:IssuerParty)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-547","texto":"A UBL invoice should not include the InvoiceLine DocumentReference ResultOfVerification","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:DocumentReference/cac:ResultOfVerification)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-548","texto":"A UBL invoice should not include the InvoiceLine PricingReference","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:PricingReference)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-549","texto":"A UBL invoice should not include the InvoiceLine OriginatorParty","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:OriginatorParty)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-550","texto":"A UBL invoice should not include the InvoiceLine Delivery","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:Delivery)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-551","texto":"A UBL invoice should not include the InvoiceLine PaymentTerms","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:PaymentTerms)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-552","texto":"A UBL invoice should not include the InvoiceLine AllowanceCharge ID","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:AllowanceCharge/cbc:ID)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-553","texto":"A UBL invoice should not include the InvoiceLine AllowanceCharge PrepaidIndicator","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:AllowanceCharge/cbc:PrepaidIndicator)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-555","texto":"A UBL invoice should not include the InvoiceLine AllowanceCharge AccountingCostCode","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:AllowanceCharge/cbc:AccountingCostCode)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-556","texto":"A UBL invoice should not include the InvoiceLine AllowanceCharge AccountingCost","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:AllowanceCharge/cbc:AccountingCost)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-557","texto":"A UBL invoice should not include the InvoiceLine AllowanceCharge PerUnitAmount","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:AllowanceCharge/cbc:PerUnitAmount)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-558","texto":"A UBL invoice should not include the InvoiceLine AllowanceCharge TaxCategory","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:AllowanceCharge/cac:TaxCategory)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-559","texto":"A UBL invoice should not include the InvoiceLine AllowanceCharge TaxTotal","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:AllowanceCharge/cac:TaxTotal)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-560","texto":"A UBL invoice should not include the InvoiceLine AllowanceCharge PaymentMeans","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:AllowanceCharge/cac:PaymentMeans)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-561","texto":"A UBL invoice should not include the InvoiceLine TaxTotal","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:TaxTotal)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-562","texto":"A UBL invoice should not include the InvoiceLine WithholdingTaxTotal","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:WithholdingTaxTotal)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-563","texto":"A UBL invoice should not include the InvoiceLine Item PackQuantity","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:Item/cbc:PackQuantity)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-565","texto":"A UBL invoice should not include the InvoiceLine Item CatalogueIndicator","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:Item/cbc:CatalogueIndicator)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-566","texto":"A UBL invoice should not include the InvoiceLine Item HazardousRiskIndicator","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:Item/cbc:HazardousRiskIndicator)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-568","texto":"A UBL invoice should not include the InvoiceLine Item Keyword","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:Item/cbc:Keyword)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-569","texto":"A UBL invoice should not include the InvoiceLine Item BrandName","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:Item/cbc:BrandName)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-570","texto":"A UBL invoice should not include the InvoiceLine Item ModelName","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:Item/cbc:ModelName)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-571","texto":"A UBL invoice should not include the InvoiceLine Item BuyersItemIdentification ExtendedID","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:Item/cac:BuyersItemIdentification/cbc:ExtendedID)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-572","texto":"A UBL invoice should not include the InvoiceLine Item BuyersItemIdentification BareCodeSymbologyID","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:Item/cac:BuyersItemIdentification/cbc:BareCodeSymbologyID)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-573","texto":"A UBL invoice should not include the InvoiceLine Item BuyersItemIdentification PhysicalAttribute","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:Item/cac:BuyersItemIdentification/cac:PhysicalAttribute)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-574","texto":"A UBL invoice should not include the InvoiceLine Item BuyersItemIdentification MeasurementDimension","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:Item/cac:BuyersItemIdentification/cac:MeasurementDimension)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-575","texto":"A UBL invoice should not include the InvoiceLine Item BuyersItemIdentification IssuerParty","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:Item/cac:BuyersItemIdentification/cac:IssuerParty)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-576","texto":"A UBL invoice should not include the InvoiceLine Item SellersItemIdentification ExtendedID","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:Item/cac:SellersItemIdentification/cbc:ExtendedID)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-577","texto":"A UBL invoice should not include the InvoiceLine Item SellersItemIdentification BareCodeSymbologyID","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:Item/cac:SellersItemIdentification/cbc:BareCodeSymbologyID)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-578","texto":"A UBL invoice should not include the InvoiceLine Item SellersItemIdentification PhysicalAttribute","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:Item/cac:SellersItemIdentification/cac:PhysicalAttribute)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-579","texto":"A UBL invoice should not include the InvoiceLine Item SellersItemIdentification MeasurementDimension","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:Item/cac:SellersItemIdentification/cac:MeasurementDimension)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-580","texto":"A UBL invoice should not include the InvoiceLine Item SellersItemIdentification IssuerParty","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:Item/cac:SellersItemIdentification/cac:IssuerParty)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-581","texto":"A UBL invoice should not include the InvoiceLine Item ManufacturersItemIdentification","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:Item/cac:ManufacturersItemIdentification)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-582","texto":"A UBL invoice should not include the InvoiceLine Item StandardItemIdentification ExtendedID","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:Item/cac:StandardItemIdentification/cbc:ExtendedID)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-583","texto":"A UBL invoice should not include the InvoiceLine Item StandardItemIdentification BareCodeSymbologyID","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:Item/cac:StandardItemIdentification/cbc:BareCodeSymbologyID)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-584","texto":"A UBL invoice should not include the InvoiceLine Item StandardItemIdentification PhysicalAttribute","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:Item/cac:StandardItemIdentification/cac:PhysicalAttribute)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-585","texto":"A UBL invoice should not include the InvoiceLine Item StandardItemIdentification MeasurementDimension","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:Item/cac:StandardItemIdentification/cac:MeasurementDimension)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-586","texto":"A UBL invoice should not include the InvoiceLine Item StandardItemIdentification IssuerParty","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:Item/cac:StandardItemIdentification/cac:IssuerParty)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-587","texto":"A UBL invoice should not include the InvoiceLine Item CatalogueItemIdentification","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:Item/cac:CatalogueItemIdentification)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-588","texto":"A UBL invoice should not include the InvoiceLine Item AdditionalItemIdentification","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:Item/cac:AdditionalItemIdentification)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-589","texto":"A UBL invoice should not include the InvoiceLine Item CatalogueDocumentReference","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:Item/cac:CatalogueDocumentReference)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-590","texto":"A UBL invoice should not include the InvoiceLine Item ItemSpecificationDocumentReference","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:Item/cac:ItemSpecificationDocumentReference)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-591","texto":"A UBL invoice should not include the InvoiceLine Item OriginCountry Name","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:Item/cac:OriginCountry/cbc:Name)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-592","texto":"A UBL invoice should not include the InvoiceLine Item CommodityClassification NatureCode","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:Item/cac:CommodityClassification/cbc:NatureCode)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-593","texto":"A UBL invoice should not include the InvoiceLine Item CommodityClassification CargoTypeCode","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:Item/cac:CommodityClassification/cbc:CargoTypeCode)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-594","texto":"A UBL invoice should not include the InvoiceLine Item CommodityClassification CommodityCode","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:Item/cac:CommodityClassification/cbc:CommodityCode)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-595","texto":"A UBL invoice should not include the InvoiceLine Item TransactionConditions","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:Item/cac:TransactionConditions)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-596","texto":"A UBL invoice should not include the InvoiceLine Item HazardousItem","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:Item/cac:HazardousItem)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-597","texto":"A UBL invoice should not include the InvoiceLine Item ClassifiedTaxCategory Name","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:Item/cac:ClassifiedTaxCategory/cbc:Name)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-598","texto":"A UBL invoice should not include the InvoiceLine Item ClassifiedTaxCategory BaseUnitMeasure","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:Item/cac:ClassifiedTaxCategory/cbc:BaseUnitMeasure)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-599","texto":"A UBL invoice should not include the InvoiceLine Item ClassifiedTaxCategory PerUnitAmount","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:Item/cac:ClassifiedTaxCategory/cbc:PerUnitAmount)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-600","texto":"A UBL invoice should not include the InvoiceLine Item ClassifiedTaxCategory TaxExemptionReasonCode","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:Item/cac:ClassifiedTaxCategory/cbc:TaxExemptionReasonCode)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-601","texto":"A UBL invoice should not include the InvoiceLine Item ClassifiedTaxCategory TaxExemptionReason","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:Item/cac:ClassifiedTaxCategory/cbc:TaxExemptionReason)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-602","texto":"A UBL invoice should not include the InvoiceLine Item ClassifiedTaxCategory TierRange","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:Item/cac:ClassifiedTaxCategory/cbc:TierRange)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-603","texto":"A UBL invoice should not include the InvoiceLine Item ClassifiedTaxCategory TierRatePercent","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:Item/cac:ClassifiedTaxCategory/cbc:TierRatePercent)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-604","texto":"A UBL invoice should not include the InvoiceLine Item ClassifiedTaxCategory TaxScheme Name","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:Item/cac:ClassifiedTaxCategory/cac:TaxScheme/cbc:Name)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-605","texto":"A UBL invoice should not include the InvoiceLine Item ClassifiedTaxCategory TaxScheme TaxTypeCode","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:Item/cac:ClassifiedTaxCategory/cac:TaxScheme/cbc:TaxTypeCode)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-606","texto":"A UBL invoice should not include the InvoiceLine Item ClassifiedTaxCategory TaxScheme CurrencyCode","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:Item/cac:ClassifiedTaxCategory/cac:TaxScheme/cbc:CurrencyCode)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-607","texto":"A UBL invoice should not include the InvoiceLine Item ClassifiedTaxCategory TaxScheme JurisdiccionRegionAddress","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:Item/cac:ClassifiedTaxCategory/cac:TaxScheme/cac:JurisdiccionRegionAddress)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-608","texto":"A UBL invoice should not include the InvoiceLine Item AdditionalItemProperty ID","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:Item/cac:AdditionalItemProperty/cbc:ID)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-609","texto":"A UBL invoice should not include the InvoiceLine Item AdditionalItemProperty NameCode","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:Item/cac:AdditionalItemProperty/cbc:NameCode)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-610","texto":"A UBL invoice should not include the InvoiceLine Item AdditionalItemProperty TestMethod","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:Item/cac:AdditionalItemProperty/cbc:TestMethod)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-611","texto":"A UBL invoice should not include the InvoiceLine Item AdditionalItemProperty ValueQuantity","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:Item/cac:AdditionalItemProperty/cbc:ValueQuantity)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-612","texto":"A UBL invoice should not include the InvoiceLine Item AdditionalItemProperty ValueQualifier","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:Item/cac:AdditionalItemProperty/cbc:ValueQualifier)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-613","texto":"A UBL invoice should not include the InvoiceLine Item AdditionalItemProperty ImportanceCode","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:Item/cac:AdditionalItemProperty/cbc:ImportanceCode)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-614","texto":"A UBL invoice should not include the InvoiceLine Item AdditionalItemProperty ListValue","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:Item/cac:AdditionalItemProperty/cbc:ListValue)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-615","texto":"A UBL invoice should not include the InvoiceLine Item AdditionalItemProperty UsabilityPeriod","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:Item/cac:AdditionalItemProperty/cac:UsabilityPeriod)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-616","texto":"A UBL invoice should not include the InvoiceLine Item AdditionalItemProperty ItemPropertyGroup","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:Item/cac:AdditionalItemProperty/cac:ItemPropertyGroup)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-617","texto":"A UBL invoice should not include the InvoiceLine Item AdditionalItemProperty RangeDimension","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:Item/cac:AdditionalItemProperty/cac:RangeDimension)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-618","texto":"A UBL invoice should not include the InvoiceLine Item AdditionalItemProperty ItemPropertyRange","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:Item/cac:AdditionalItemProperty/cac:ItemPropertyRange)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-619","texto":"A UBL invoice should not include the InvoiceLine Item ManufacturerParty","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:Item/cac:ManufacturerParty)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-621","texto":"A UBL invoice should not include the InvoiceLine Item OriginAddress","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:Item/cac:OriginAddress)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-622","texto":"A UBL invoice should not include the InvoiceLine Item ItemInstance","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:Item/cac:ItemInstance)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-623","texto":"A UBL invoice should not include the InvoiceLine Item Certificate","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:Item/cac:Certificate)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-624","texto":"A UBL invoice should not include the InvoiceLine Item Dimension","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:Item/cac:Dimension)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-625","texto":"A UBL invoice should not include the InvoiceLine Item Price PriceChangeReason","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:Item/cac:Price/cbc:PriceChangeReason)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-626","texto":"A UBL invoice should not include the InvoiceLine Item Price PriceTypeCode","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:Item/cac:Price/cbc:PriceTypeCode)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-627","texto":"A UBL invoice should not include the InvoiceLine Item Price PriceType","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:Item/cac:Price/cbc:PriceType)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-628","texto":"A UBL invoice should not include the InvoiceLine Item Price OrderableUnitFactorRate","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:Item/cac:Price/cbc:OrderableUnitFactorRate)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-629","texto":"A UBL invoice should not include the InvoiceLine Item Price ValidityPeriod","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:Item/cac:Price/cbc:ValidityPeriod)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-630","texto":"A UBL invoice should not include the InvoiceLine Item Price PriceList","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:Item/cac:Price/cbc:PriceList)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-631","texto":"A UBL invoice should not include the InvoiceLine Item Price OrderableUnitFactorRate","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:Item/cac:Price/cbc:OrderableUnitFactorRate)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-632","texto":"A UBL invoice should not include the InvoiceLine Item Price AllowanceCharge ID","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:Item/cac:Price/cac:AllowanceCharge/cbc:ID)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-633","texto":"A UBL invoice should not include the InvoiceLine Item Price AllowanceCharge AllowanceChargeReasonCode","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:Item/cac:Price/cac:AllowanceCharge/cbc:AllowanceChargeReasonCode)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-634","texto":"A UBL invoice should not include the InvoiceLine Item Price AllowanceCharge AllowanceChargeReason","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:Item/cac:Price/cac:AllowanceCharge/cbc:AllowanceChargeReason)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-636","texto":"A UBL invoice should not include the InvoiceLine Item Price AllowanceCharge PrepaidIndicator","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:Item/cac:Price/cac:AllowanceCharge/cbc:PrepaidIndicator)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-638","texto":"A UBL invoice should not include the InvoiceLine Item Price AllowanceCharge AccountingCostCode","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:Item/cac:Price/cac:AllowanceCharge/cbc:AccountingCostCode)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-639","texto":"A UBL invoice should not include the InvoiceLine Item Price AllowanceCharge AccountingCost","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:Item/cac:Price/cac:AllowanceCharge/cbc:AccountingCost)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-640","texto":"A UBL invoice should not include the InvoiceLine Item Price AllowanceCharge PerUnitAmount","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:Item/cac:Price/cac:AllowanceCharge/cbc:PerUnitAmount)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-641","texto":"A UBL invoice should not include the InvoiceLine Item Price AllowanceCharge TaxCategory","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:Item/cac:Price/cac:AllowanceCharge/cac:TaxCategory)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-642","texto":"A UBL invoice should not include the InvoiceLine Item Price AllowanceCharge TaxTotal","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:Item/cac:Price/cac:AllowanceCharge/cac:TaxTotal)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-643","texto":"A UBL invoice should not include the InvoiceLine Item Price AllowanceCharge PaymentMeans","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:Item/cac:Price/cac:AllowanceCharge/cac:PaymentMeans)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-644","texto":"A UBL invoice should not include the InvoiceLine Item Price PricingExchangeRate","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:Item/cac:Price/cac:PricingExchangeRate)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-645","texto":"A UBL invoice should not include the InvoiceLine DeliveryTerms","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:DeliveryTerms)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-646","texto":"A UBL invoice should not include the InvoiceLine SubInvoiceLine","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:SubInvoiceLine)"},
{"fonte":"cius-pt-schematron","id":"UBL-CR-647","texto":"A UBL invoice should not include the InvoiceLine ItemPriceExtension","categoria":"presenca","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"not(cac:InvoiceLine/cac:ItemPriceExtension)"},
{"fonte":"cius-pt-schematron","id":"UBL-DT-18","texto":"Name attribute should not be present","categoria":"cardinalidade","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"count(//@name) - count(//cbc:PaymentMeansCode/@name) <= 0"},
{"fonte":"cius-pt-schematron","id":"UBL-SR-01","texto":"Contract identifier shall occur maximum once.","categoria":"cardinalidade","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"(count(cac:ContractDocumentReference/cbc:ID) <= 1)"},
{"fonte":"cius-pt-schematron","id":"UBL-SR-02","texto":"Receive advice identifier shall occur maximum once","categoria":"cardinalidade","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"(count(cac:ReceiptDocumentReference/cbc:ID) <= 1)"},
{"fonte":"cius-pt-schematron","id":"UBL-SR-03","texto":"Despatch advice identifier shall occur maximum once","categoria":"cardinalidade","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"(count(cac:DespatchDocumentReference/cbc:ID) <= 1)"},
{"fonte":"cius-pt-schematron","id":"UBL-SR-04","texto":"Invoice object identifier shall occur maximum once","categoria":"cardinalidade","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"(count(cac:AdditionalDocumentReference[cbc:DocumentTypeCode='130']/cbc:ID) <= 1)"},
{"fonte":"cius-pt-schematron","id":"UBL-SR-05","texto":"Payment terms shall occur maximum once","categoria":"cardinalidade","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"(count(cac:PaymentTerms/cbc:Note) <= 1)"},
{"fonte":"cius-pt-schematron","id":"UBL-SR-06","texto":"Preceding invoice reference shall occur maximum once","categoria":"cardinalidade","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"(count(cac:InvoiceDocumentReference) <= 1)"},
{"fonte":"cius-pt-schematron","id":"UBL-SR-08","texto":"Invoice period shall occur maximum once","categoria":"cardinalidade","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"(count(cac:InvoicePeriod) <= 1)"},
{"fonte":"cius-pt-schematron","id":"UBL-SR-09","texto":"Seller name shall occur maximum once","categoria":"cardinalidade","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"(count(cac:AccountingSupplierParty/cac:Party/cac:PartyLegalEntity/cbc:RegistrationName) <= 1)"},
{"fonte":"cius-pt-schematron","id":"UBL-SR-10","texto":"Seller trader name shall occur maximum once","categoria":"cardinalidade","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"(count(cac:AccountingSupplierParty/cac:Party/cac:PartyName/cbc:Name) <= 1)"},
{"fonte":"cius-pt-schematron","id":"UBL-SR-11","texto":"Seller legal registration identifier shall occur maximum once","categoria":"cardinalidade","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"(count(cac:AccountingSupplierParty/cac:Party/cac:PartyLegalEntity/cbc:CompanyID) <= 1)"},
{"fonte":"cius-pt-schematron","id":"UBL-SR-12","texto":"Seller VAT identifier shall occur maximum once","categoria":"cardinalidade","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"(count(cac:AccountingSupplierParty/cac:Party/cac:PartyTaxScheme[cac:TaxScheme/cbc:ID='VAT']/cbc:CompanyID) <= 1)"},
{"fonte":"cius-pt-schematron","id":"UBL-SR-13","texto":"Seller tax registration shall occur maximum once","categoria":"cardinalidade","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"(count(cac:AccountingSupplierParty/cac:Party/cac:PartyTaxScheme[cac:TaxScheme/cbc:ID!='VAT']/cbc:ID) <= 1)"},
{"fonte":"cius-pt-schematron","id":"UBL-SR-15","texto":"Buyer name shall occur maximum once","categoria":"cardinalidade","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"(count(cac:AccountingCustomerParty/cac:Party/cac:PartyLegalEntity/cbc:RegistrationName) <= 1)"},
{"fonte":"cius-pt-schematron","id":"UBL-SR-16","texto":"Buyer identifier shall occur maximum once","categoria":"cardinalidade","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"(count(cac:AccountingCustomerParty/cac:Party/cac:PartyIdentification/cbc:ID) <= 1)"},
{"fonte":"cius-pt-schematron","id":"UBL-SR-17","texto":"Buyer legal registration identifier shall occur maximum once","categoria":"cardinalidade","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"(count(cac:AccountingCustomerParty/cac:Party/cac:PartyLegalEntity/cbc:CompanyID) <= 1)"},
{"fonte":"cius-pt-schematron","id":"UBL-SR-18","texto":"Buyer VAT identifier shall occur maximum once","categoria":"cardinalidade","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"(count(cac:AccountingCustomerParty/cac:Party/cac:PartyTaxScheme/cbc:CompanyID) <= 1)"},
{"fonte":"cius-pt-schematron","id":"UBL-SR-29","texto":"Bank creditor reference shall occur maximum once","categoria":"cardinalidade","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"(count(cac:PayeeParty/cac:PartyIdentification/cbc:ID) <= 1)"},
{"fonte":"cius-pt-schematron","id":"UBL-SR-39","texto":"Project reference shall occur maximum once.","categoria":"cardinalidade","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"(count(cac:ProjectReference/cbc:ID) <= 1)"},
{"fonte":"cius-pt-schematron","id":"UBL-SR-40","texto":"Buyer trade name shall occur maximum once","categoria":"cardinalidade","natureza":"RE","gravidade":"aviso","contexto":"Invoice","expressao":"(count(cac:AccountingCustomerParty/cac:Party/cac:PartyName/cbc:Name) <= 1)"},
{"fonte":"cius-pt-schematron","id":"UBL-SR-34","texto":"Invoice line note shall occur maximum once","categoria":"cardinalidade","natureza":"RE","gravidade":"aviso","contexto":"Invoice_line","expressao":"(count(cbc:Note) <= 1)"},
{"fonte":"cius-pt-schematron","id":"UBL-SR-35","texto":"Referenced purchase order line identifier shall occur maximum once","categoria":"cardinalidade","natureza":"RE","gravidade":"aviso","contexto":"Invoice_line","expressao":"(count(cac:OrderLineReference/cbc:LineID) <= 1)"},
{"fonte":"cius-pt-schematron","id":"UBL-SR-36","texto":"Invoice line period shall occur maximum once","categoria":"cardinalidade","natureza":"RE","gravidade":"aviso","contexto":"Invoice_line","expressao":"(count(cac:InvoicePeriod) <= 1)"},
{"fonte":"cius-pt-schematron","id":"UBL-SR-37","texto":"Item price discount shall occur maximum once","categoria":"cardinalidade","natureza":"RE","gravidade":"aviso","contexto":"Invoice_line","expressao":"(count(cac:Price/cac:AllowanceCharge/cbc:Amount) <= 1)"},
{"fonte":"cius-pt-schematron","id":"UBL-SR-38","texto":"Invoiced item VAT exemption reason text shall occur maximum once","categoria":"cardinalidade","natureza":"RE","gravidade":"aviso","contexto":"Invoice_line","expressao":"(count(cac:Item/cac:ClassifiedTaxCategory/cbc:TaxExemptionReason) <= 1)"},
{"fonte":"cius-pt-schematron","id":"UBL-SR-26","texto":"Payment reference shall occur maximum once","categoria":"cardinalidade","natureza":"RE","gravidade":"aviso","contexto":"Payment_instructions","expressao":"(count(cbc:PaymentID) <= 1)"},
{"fonte":"cius-pt-schematron","id":"UBL-SR-27","texto":"Payment means text shall occur maximum once","categoria":"cardinalidade","natureza":"RE","gravidade":"aviso","contexto":"Payment_instructions","expressao":"(count(cbc:InstructionNote) <= 1)"},
{"fonte":"cius-pt-schematron","id":"UBL-SR-28","texto":"Mandate reference identifier shall occur maximum once","categoria":"cardinalidade","natureza":"RE","gravidade":"aviso","contexto":"Payment_instructions","expressao":"(count(cac:PaymentMandate/cbc:ID) <= 1)"},
{"fonte":"cius-pt-schematron","id":"UBL-SR-32","texto":"VAT exemption reason text shall occur maximum once","categoria":"cardinalidade","natureza":"RE","gravidade":"aviso","contexto":"Tax_subtotal","expressao":"(count(cac:TaxCategory/cbc:TaxExemptionReason) <= 1)"}
]
```

## Informação adicional (outra fonte)

(nenhuma)

## Pedido

Quero criar uma nova projecao

## Formato da resposta

```json
{"operacoes": [{"op": "…", "…": "…"}], "notas": ["…"]}
```

Responde só com o JSON, sem texto à volta.
