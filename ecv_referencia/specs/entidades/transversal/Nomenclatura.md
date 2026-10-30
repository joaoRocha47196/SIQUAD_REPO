# Nomenclatura

| O quê | Regra | Exemplos | Verificação |
|---|---|---|---|
| HLM, SM, USM | PascalCase, sem acentos, singular | `Fatura`, `InformacaoGeografica`, `Linha` | S-MOD |
| SM de coleção | plural do elemento | `Linhas` (elemento `Linha`) | (convenção) |
| Papel de composição | PascalCase; por omissão, o nome do modelo | `Requerente`, `Origem`, `Destino` | S-COMP |
| Propriedade | camelCase, sem acentos | `codigoPostal`, `dataUltimaManutencao`, `tipoIVA` | S-PROP |
| Nome alternativo | o nome tal como aparece na fonte | `zipCode`, `postalCode`, `CP`, `deviceId`, `reading` | — |
| Regra | `TIPO-ASSUNTO[-QUALIFICADOR]`, maiúsculas e algarismos com hífens; o tipo é `RP`, `RIR` ou `RIC` e coincide com a natureza | `RP-LAT`, `RIR-TEMP-REFRIG-CELSIUS`, `RIC-MANUT`, `RIR-CP-LX-AJUDA` | S-REGRA |
| Natureza | `plausibilidade`, `inferencia_restritiva`, `inferencia_conclusiva` | — | S-REGRA |
| Valores enumerados | MAIÚSCULAS, sem acentos, `_` entre palavras | `REFRIGERACAO`, `NAO_FIAVEL`, `AVENIDAS_NOVAS` | (convenção) |
| Conclusão de uma RIC | `tipo`: `ACAO` ou `ESTADO`; `valor` em maiúsculas | `ACAO` `MANUTENCAO`; `ESTADO` `DIFERIDA` | S-REGRA |
| Função | camelCase; um predicado ("verdadeira quando …") | `somaIgualA`, `dentroDe`, `excedeDiasDesdeHoje` | S-FUNC |
| Contexto externo | camelCase | `dataDeHoje`, `chaveDispositivo`, `seriesComunicadasAT` | S-CTX |
| Projeção | PascalCase, nome da utilização | `FaturaSimplificada`, `DispositivoProducao` | S-PROJ |
| Perfil | PascalCase, nome do cenário | `RefrigeracaoLote`, `EmissaoSimplificada` | S-PERFIL |
| Ficheiro de declaração | `<hlm em snake_case>.ecv.json` | `ordem_instalacao.ecv.json` | — |

## Assuntos usados nos identificadores das regras

| Assunto | Significado |
|---|---|
| `TEMP`, `HUM`, `PRES`, `VEL` | temperatura, humidade, pressão, velocidade |
| `UN` | unidade de medida |
| `REFRIG`, `ESTUFA`, `ARMAZEM`, `SERVIDORES`, `EXTERIOR`, `INCIN`, `CAMARA` | ambiente de instalação |
| `CELSIUS`, `KELVIN`, `FAHRENHEIT` (ou `C`, `K`, `F`), `HPA`, `BAR`, `MS`, `KMH` | unidade |
| `CP` | código postal; `LX` Lisboa |
| `IVA` (`ISE`, `RED`, `INT`, `NOR`) | tipo de IVA |
| `FS`, `FT` | fatura simplificada, fatura |
| `LIN` | linhas |
| `MANUT`, `REDE`, `MED` | manutenção, rede, medição |

## Mensagens e descrições

- A **mensagem de não conformidade** (na restrição) é autocontida: diz o que falhou e o que é esperado, sem identificadores. Exemplo: "O código postal português tem de ter o formato 0000-000, sem começar por zero."
- A **mensagem de conclusão** (numa RIC) começa pela conclusão e explica o motivo. Exemplo: "Ação MANUTENCAO: o nível de bateria está baixo e …".
- A **descrição** da regra é derivada (ver [Regra.md](../ecr/Regra.md)).
- A **descrição de modelos e propriedades** é precisa. Uma descrição vaga ("Valor", "Dados") aparece como tal nas vistas, e é aí que se corrige.
