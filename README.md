# SIQUAD_REPO

Repositório da dissertação de mestrado **Estratificação do Conhecimento de Validação (ECV)**, de João Rocha (ISEL, Mestrado em Engenharia Informática e de Computadores).

A dissertação propõe uma forma única de representar o conhecimento que define o que é um dado válido: os modelos de dados, as regras que se aplicam a esses modelos e as utilizações (perfis) em que cada regra é exigida. Esta representação é independente do formato e da tecnologia em que o conhecimento foi originalmente escrito (CSV, JSON Schema, XML, Schematron, código…), pode ser obtida a partir de fontes heterogéneas ou de uma descrição em linguagem natural com o apoio de um LLM, e é organizada num grafo sobre o qual se constroem vistas, se avaliam instâncias e se analisa o impacto de alterações.

## Organização do repositório

| Pasta | O que contém |
|---|---|
| [`ecv_referencia/`](ecv_referencia/) | A implementação de referência da ECV: a extração das fontes, a geração da declaração ECV com um LLM, a verificação, o grafo, as vistas, as alterações, a validação de instâncias e a aplicação Web que reúne tudo. É o resultado final do trabalho. |
| [`documentacao/`](documentacao/) | A documentação técnica da implementação (páginas HTML navegáveis) e as vistas estáticas geradas a partir das declarações de exemplo. |
| [`DATA/`](DATA/) | As fontes de dados públicas usadas na avaliação: o CIUS-PT (faturação eletrónica) e os Smart Data Models (dispositivos IoT). |
| [`Proof_of_Concept/`](Proof_of_Concept/) | A primeira prova de conceito, sobre os ficheiros Schematron e as suas fases, que deu origem à ideia de separar a regra do esquema e de a aplicar consoante o objetivo. |
| [`WebApp_Graph_Exploration/`](WebApp_Graph_Exploration/) | O protótipo inicial da aplicação Web, construído para a conferência IV 2026, que explorava sobre o Neo4j o grafo do conhecimento de validação. |
| `Artigos/` | Os artigos publicados no âmbito da dissertação (DoCEIS 2026, sobre o caso IoT, e IV 2026, sobre o suporte visual à validação). |

## Por onde começar

1. Ler o `README.md` de [`ecv_referencia/`](ecv_referencia/) e arrancar a aplicação Web (é preciso apenas Python 3.10 ou superior).
2. Abrir `documentacao/site/index.html` no navegador para conhecer a solução e os módulos.
3. Abrir `documentacao/vistas/index.html` para ver, sem instalar nada, as vistas geradas a partir das declarações de exemplo.

## Artigos

- J. Rocha *et al.*, "A Unified Validation Framework for Heterogeneous Data Models", DoCEIS & YEF-ECE 2026.
- J. Rocha *et al.*, "Visual support for data model validation: a framework and case study", IV 2026.
