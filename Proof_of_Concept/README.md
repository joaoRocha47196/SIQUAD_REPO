# Proof_of_Concept

Esta pasta contém a primeira prova de conceito da dissertação, construída sobre ficheiros Schematron e as suas fases.

O Schematron separa as regras do esquema: cada regra vive num ficheiro próprio, declara a que elementos se aplica e pode ser ativada parcialmente através de fases (por exemplo, um conjunto de regras para a faturação e outro para a expedição). A prova de conceito explorou esta ideia, inspirada no trabalho de Ali (2019), que leva o modelo de regras do Schematron para o JSON, e permitiu testar, numa fase inicial, dois princípios que a dissertação manteve:

- a regra deve existir fora do esquema e do código que consome os dados;
- a mesma informação pode ser avaliada com subconjuntos diferentes de regras, consoante o objetivo da validação.

Mostrou também os seus limites: as fases agrupam regras de um documento, mas não permitem dizer que a morada de uma fatura e a de um equipamento são a mesma coisa, nem relacionar regras entre modelos diferentes. Estes limites conduziram à organização proposta na ECV, em que os modelos e as regras são declarados uma vez e reutilizados, e a seleção do que se aplica é feita por perfis.

Esta pasta é mantida como registo histórico; a implementação final está em [`../ecv_referencia`](../ecv_referencia).
