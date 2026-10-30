# Caminhos

Um caminho refere uma propriedade (ou um modelo) a partir de um nó. É formado pelos **papéis** das composições a percorrer, separados por pontos, seguidos opcionalmente do **nome de uma propriedade**.

## De onde parte o caminho

| Onde aparece | Relativo a | Exemplo |
|---|---|---|
| Regra que vive num HLM | o HLM | `Leitura.Medicao.valor`, `Cabecalho.totalFatura`, `Linhas.Linha` |
| Regra que vive num SM | o SM | `Morada.localidade`, `InformacaoGeografica.latitude`, `Linha.numero` (SM Linhas) |
| Regra que vive num USM | o USM | `pais`, `codigoPostal` |
| Regra que vive numa propriedade | o modelo dono da propriedade | `latitude` (só pode ler a própria propriedade) |
| Projeção | o HLM | `Identificacao.estado`, `Leitura.Medicao.*` |
| Perfil (`fixa`) | o HLM da projeção | `Leitura.Instalacao.ambiente` |

## Segmentos

- Cada segmento intermédio é o **papel** de uma composição. Por omissão, o papel é o nome do modelo composto. Com `papel` explícito, usa-se o papel: `Requerente.Entidade.nif` (OrdemInstalacao compõe Cliente com o papel Requerente).
- O último segmento é uma propriedade ou um papel. Se for um papel, o caminho termina num modelo. Isto só é admitido em argumentos de funções (instâncias de uma coleção: `Linhas.Linha`, `Localizacao`).
- Um caminho que atravessa uma composição repetível (`1..*`, `0..*`) é uma **coleção**: `Linhas.Linha.valor` é a lista dos valores de todas as linhas.

## Na descrição das regras

Na descrição derivada, os caminhos aparecem prefixados com o nome do nó onde a regra vive, exceto no HLM: `Morada.pais`, `Diagnostico.nivelBateria`, mas `Identificacao.tipoDispositivo` numa regra do HLM Dispositivo. É a "ligação ao modelo" da tese.

## Nas projeções: `*`

| Forma | Expande para |
|---|---|
| `X.*` | todas as propriedades, a qualquer profundidade, abaixo de X |
| `*` | todas as propriedades do HLM |
| `X.Y.prop` | só essa propriedade, nesse caminho |

`X.*` sobre um caminho que termina numa propriedade é um erro; um caminho sem `*` tem de terminar numa propriedade.

## Ocorrências

O mesmo modelo pode ser alcançado por vários caminhos no mesmo HLM. Por exemplo, na Fatura, Morada é alcançada por `Emitente.Morada` e `Cliente.Morada`. Cada caminho é uma **ocorrência**. A propriedade é a mesma (o mesmo nó no grafo), mas a projeção e o perfil referem ocorrências: as arestas `OBRIGATORIA`, `PERMITIDA` e `FIXA` guardam o `caminho`. Uma regra que vive num modelo reutilizado aplica-se em cada ocorrência. A vista `perfil` avalia-a por ocorrência.

## Chaves no grafo

| Entidade | Chave | Exemplo |
|---|---|---|
| Propriedade | `<nível do dono>:<dono>.<nome>` | `USM:Medicao.valor`, `SM:Cabecalho.totalFatura` |
| Restrição | `<id da regra>#restricao` | `RP-LAT#restricao` |
| Condição | `<id da regra>#condicao` | `RIR-FS#condicao` |
| Restantes | `nome` (modelos, funções, contextos, projeções, perfis) ou `id` (regras) | `Morada`, `RIC-MANUT` |

## Implementação

`ecv/3_ingestion/paths.py` contém as funções `resolver` (resolve um caminho a partir de um nó, com os passos, a propriedade final, se é coleção e o tipo), `expandir` (o `*` das projeções), `ocorrencias` (os caminhos de todos os nós de um HLM) e `chave_propriedade`.
