# Verificação: specs e invariantes

A verificação antecede a materialização (tese, Secção "Verificação da declaração"). Faz-se em dois níveis:

1. **Specs:** cada entidade isolada (atributos obrigatórios, forma, nomes). Inclui a validação contra o [JSON Schema](../../declaracao/ecv.schema.json) quando o pacote `jsonschema` está instalado.
2. **Invariantes:** o que só se verifica com todas as entidades carregadas.

Um **erro** impede a materialização. Um **aviso** não a impede, mas é apresentado.

```
python -m ecv verificar          # todas as declarações de specs/exemplos
```

## Specs

| Código | Entidade | Verifica |
|---|---|---|
| S-SCHEMA | toda a declaração | Forma contra `specs/declaracao/ecv.schema.json` |
| S-DECL | declaração | exatamente um HLM (e o cabeçalho `declaracao.hlm` indica-o); `usm` existe e não está vazia; nomes únicos em cada secção |
| S-MOD | HLM, SM, USM | PascalCase; descrição ≥ 10; o HLM sem propriedades e com composição; o USM com propriedades e sem composição; o SM com composição ou propriedades |
| S-COMP | composição | Um de `sm` ou `usm`, coerente com o nível; cardinalidade válida; papel em PascalCase e único |
| S-PROP | propriedade | camelCase; tipo base; descrição ≥ 5; nomes únicos e diferentes dos papéis |
| S-REGRA | regra | Natureza válida; id `TIPO-…` coerente com a natureza; descrição; mensagem na restrição (RP, RIR) ou na regra (RIC); `conclusao` só em RIC |
| S-RESTR | restrição | Operador do catálogo; um alvo (exceto numa função); mensagem ≥ 10 |
| S-TERMO | termo | Operador do catálogo; propriedade (exceto numa função); contexto declarado |
| S-VALOR | restrição e termo | Forma do valor exigida pelo operador (lista, intervalo, regex válida, …) |
| S-CHAMADA | chamada | Função declarada; número de argumentos; caminho para alvos e literal para parâmetros; coleções |
| S-FUNC | função | camelCase; descrição; parâmetros com papel e tipo; contextos declarados; retorno booleano |
| S-CTX | contexto externo | camelCase; tipo base; descrição |
| S-PROJ | projeção | PascalCase; HLM declarado; listas |
| S-PERFIL | perfil | PascalCase; projeção declarada; HLM coerente; cada fixação tem `propriedade` ou `contexto` e `valor` |

## Invariantes

| | Invariante | Gravidade | Origem |
|---|---|---|---|
| I1 | A composição é acíclica. | erro | tese |
| I2 | Todos os modelos compostos estão declarados. | erro | tese |
| I3 | Todos os caminhos de uma regra (termos e argumentos) resolvem a partir do nó onde a regra vive; uma regra declarada numa propriedade só lê essa propriedade. | erro | tese |
| I4 | Uma RP tem restrição e não tem condição; uma RIR tem condição e restrição; uma RIC tem condição e mensagem de conclusão, sem restrição. | erro | tese |
| I5 | O operador é admissível para o tipo base; EXT_FUNCTION só para funções com contextos externos (e FUNCTION para as restantes); um contexto comparado é do tipo da propriedade. | erro | tese |
| I6 | A condição não lê o alvo da restrição da mesma regra. | erro | tese |
| I7 | Os valores usados numa condição (EQUALS, IN) pertencem aos valores plausíveis da propriedade; senão, a regra nunca se aplica. | aviso | tese |
| I8 | Uma regra de um SM ou HLM que só lê um filho não repetível poderia viver nesse filho; uma regra de um modelo que só lê uma propriedade poderia viver nela. | aviso | tese |
| I9 | Os caminhos das projeções e dos perfis existem no HLM; uma propriedade não é obrigatória e permitida ao mesmo tempo; os valores fixados são plausíveis. | erro | tese |
| I10 | Num perfil, uma regra cuja condição lê propriedades nem projetadas nem fixadas não é avaliável. | aviso | tese (Seleção, Figura "Propriedade usada na aplicabilidade mas não projetada") |
| I11 | Os `contextosExternos` declarados numa regra coincidem com os que ela usa. | aviso | esta versão |
| I12 | A descrição de uma regra coincide com a derivada. | aviso | esta versão |
| I13 | Funções e contextos declarados são usados. | aviso | esta versão |

## Avisos esperados nos exemplos

A declaração do Dispositivo tem exatamente dois avisos, ambos intencionais; as restantes não têm nenhum (ver [exemplos](../../exemplos/README.md)):

- **I7:** RIR-TEMP-CAMARA-CELSIUS usa `ambiente = CAMARA_FRIGORIFICA`, que não é plausível.
- **I10:** o perfil TesteLaboratorio deixa 28 RIR não avaliáveis, porque não projeta nem fixa `ambiente`.
