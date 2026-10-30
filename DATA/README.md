# DATA

Fontes de dados públicas usadas na avaliação da dissertação, tal como foram publicadas pelas entidades que as mantêm.

| Pasta | O que contém | Origem |
|---|---|---|
| `CIS_PT_SCHEMATRON/` | O CIUS-PT, a especificação portuguesa da fatura eletrónica (norma EN 16931): o guia do modelo de dados semântico (PDF), o Schematron com as regras de validação (versão 2.1.1) e os modelos UBL 2.1 anotados da fatura, da nota de crédito e da mensagem de estado. | Autoridade Tributária e Aduaneira, Portal das Finanças: [comunicação dos elementos dos documentos de faturação](https://info.portaldasfinancas.gov.pt/pt/apoio_ao_contribuinte/Negocios/Faturacao/Regras_mecanismos_comunicacao/e_Fatura/e_Fatura_Comunicacao_elementos_docs_faturacao_2022_seguintes/Paginas/default.aspx) |
| `SDM_Device/` | Os esquemas JSON Schema do conjunto Device dos Smart Data Models (dispositivo, modelo de dispositivo, medição, operação e modelos especializados) e as definições comuns. | [smart-data-models/dataModel.Device](https://github.com/smart-data-models/dataModel.Device) (commit `df7f550`) e [smart-data-models/data-models](https://github.com/smart-data-models/data-models) |

Os domínios da implementação de referência (`ecv_referencia/dominios/<domínio>/dominio.json`) indicam, para cada fonte, o caminho dentro desta pasta e o adaptador que a lê.
