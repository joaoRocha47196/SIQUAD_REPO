# Pedido de alterações (contexto focado) → operações

## Objetivo

Traduzir um pedido de alterações, escrito em linguagem natural, numa lista de operações do vocabulário fechado. O código aplica-as de forma determinística às declarações do domínio. O contexto abaixo foi escolhido pela pessoa: são as entidades a que o pedido se refere (e as que ajudam a escrever as operações). Não alteres nada que o pedido não diga; se for ambíguo, escolhe a interpretação mínima e explica-a em `notas`. Se precisares de uma entidade que não está no contexto, usa o índice; se faltar informação, pede-a em `notas` em vez de a inventar.

Camada: {{CAMADA}}

{{ORIENTACAO}}

## Pedido

{{PEDIDO}}

## Informação adicional (outra fonte)

{{INFORMACAO}}

## Contexto escolhido (as entidades, tal como estão nas declarações)

{{CONTEXTO}}

## Índice do que existe (nomes, para referir entidades fora do contexto)

{{INDICE}}

## Operações desta camada

{{OPERACOES}}

### Forma dos campos (exemplos)

{{EXEMPLOS}}

Regras que o código verifica: nomes em português sem acentos (modelos PascalCase, propriedades e funções camelCase, regras TIPO-ASSUNTO[-QUALIFICADOR]); uma RP vive na propriedade e só a lê; uma RIR tem condição (termos com E) e uma restrição com um só alvo, e a condição não lê o alvo; caminhos relativos ao nó onde a regra vive; a mensagem de não conformidade está na restrição; a descrição das regras é derivada pelo código (não a escrevas). Operadores: {{OPERADORES}}.

## Formato da resposta

```json
{"operacoes": [{"op": "…", "…": "…"}], "notas": ["…"]}
```

Responde só com o JSON, sem texto à volta.
