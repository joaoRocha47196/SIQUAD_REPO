# Pedido de alterações → operações

## Objetivo

Traduzir um pedido de alterações, escrito em linguagem natural pela pessoa que revê as declarações, numa lista de operações do vocabulário fechado, que o código aplica de forma determinística às declarações do domínio. O pedido pode corrigir o que existe ou acrescentar informação nova (de uma tabela, de um documento ou de outra fonte, dada em "Informação adicional"). Não alteres nada que o pedido não diga; se o pedido for ambíguo, escolhe a interpretação mínima e explica-a em `notas`.

Camada em revisão: {{PASSO}}.

## Orientação da camada

{{ORIENTACAO}}

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

{{OPERACOES}}

{{OPERACOES_CAMADA}}

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

{{ESPECIFICACOES}}

## Declarações atuais do domínio

{{DECLARACOES}}

## Mapeamento atual

{{MAPEAMENTO}}

## Itens do inventário desta camada ainda sem mapeamento

{{INVENTARIO}}

## Informação adicional (outra fonte)

{{INFORMACAO}}

## Pedido

{{PEDIDO}}

## Formato da resposta

```json
{"operacoes": [{"op": "…", "…": "…"}], "notas": ["…"]}
```

Responde só com o JSON, sem texto à volta.
