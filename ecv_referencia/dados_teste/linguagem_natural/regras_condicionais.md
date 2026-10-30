# Pedidos de regras condicionais (camada D) em linguagem natural

Cada pedido é para colar no separador Alterações › D, no campo "Pedido em linguagem natural", depois de escolher o modelo indicado (o contexto do pedido fica só com esse modelo e as propriedades que o pedido refere). Servem para testar se o LLM traduz o texto nas operações certas (`adicionar_regra` com RIR ou RIC) sem receber a declaração completa.

## Faturação (domínio faturacao)

1. Modelo `CategoriaIva`: se o código da categoria for E (isento), o motivo de isenção e o código do motivo de isenção são obrigatórios.
2. Modelo `CategoriaIva`: se o código da categoria for S, o motivo de isenção não pode estar preenchido.
3. Modelo `Morada`: se o país for PT, o código postal segue o padrão 0000-000 (`^[0-9]{4}-[0-9]{3}$`).
4. Modelo `LinhaDocumento`: se a unidade de medida for H87 (peça), a quantidade é um número inteiro.
5. Modelo `Morada`: quando a localidade é LISBOA, a freguesia é obrigatória.

## IoT (domínio iot)

6. Modelo `Medicao` (ou o equivalente na declaração): se a unidade for CEL, o valor está entre -50 e 150.
7. Modelo `Identificacao`: se o estado for AVARIADO, a data da última manutenção é obrigatória.
8. Uma regra que conclui: se a temperatura medida for superior a 8 e o ambiente for REFRIGERACAO, o alarme fica ATIVO (RIC).

## Pedido com informação de outra fonte

9. Colar o conteúdo de `../csv/codigo_postal_por_pais.csv` em "Informação adicional" e pedir: "Cria uma regra por país com o formato do código postal da tabela, no modelo Morada."

O resultado esperado de cada pedido é uma lista de operações que passa a pré-visualização sem erros; a verificação da camada D mostra as regras novas e a vista de decisão de cada modelo mostra a tabela.
