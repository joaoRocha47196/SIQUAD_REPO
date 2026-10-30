# ecv_referencia — implementação de referência da ECV

Esta pasta contém a implementação final da Estratificação do Conhecimento de Validação (ECV). Reúne, numa única implementação, todos os componentes desenvolvidos ao longo da dissertação.

## O que faz

- **Extração das fontes.** Lê as fontes de um domínio, cada uma no seu formato (PDF, Schematron, XML, JSON Schema, texto em linguagem natural), através de adaptadores, e reúne tudo num inventário comum. Para um formato sem adaptador, é possível pedir a um LLM que o escreva.
- **Geração da declaração ECV.** Sobre o inventário e a especificação das entidades, prepara um pedido a um LLM, que devolve a declaração ECV: os modelos (HLM, SM e USM), as regras (de plausibilidade, de inferência restritiva e conclusiva), as funções, as projeções e os perfis.
- **Verificação e grafo.** Verifica a declaração contra a especificação e integra-a num grafo, reutilizando o que já existe.
- **Vistas.** Constrói, a partir do grafo, vistas orientadas a cada finalidade: a estrutura dos modelos, as regras, as tabelas de decisão, as projeções e perfis, as dependências e o impacto de uma alteração.
- **Alterações.** Permite rever e completar a declaração por operações conhecidas (formulários, tabelas CSV de mapeamentos), sempre verificadas.
- **Validação.** Avalia uma instância no cenário de um perfil, regra a regra, e gera instâncias de teste a partir da estrutura do modelo.
- **Aplicação Web.** Dá acesso a todas estas operações sem linha de comandos. Funciona localmente, com o grafo em memória, e serve para comprovar as funcionalidades.

## Como executar

```bash
cd ecv_referencia
pip install -r requirements.txt     # opcional: jsonschema e o controlador do Neo4j
python -m ecv servidor              # aplicação Web em http://127.0.0.1:8000
```

A linha de comandos (`python -m ecv --help`) faz as mesmas operações. A documentação técnica está na pasta [`../documentacao`](../documentacao).

## Organização

| Pasta | O que contém |
|---|---|
| `ecv/` | O código, em módulos numerados pela ordem do processo: `0_transformer` (extração), `1_ecv_builder` (geração), `2_amendments` (alterações), `3_ingestion` (verificação e integração), `4_graph` (grafo e base de dados), `5_views` (vistas), `6_validation` (validação e funções), `7_webapp` (aplicação Web). |
| `specs/` | A especificação de cada entidade da ECV, o esquema da declaração e as declarações de exemplo. |
| `dominios/` | Os domínios trabalhados (faturação, IoT e biblioteca): fontes, inventários, declarações geradas, mapeamento e pedidos ao LLM. |
| `pedidos/` | Os pedidos ao LLM para implementar funções e criar adaptadores. |
| `dados_teste/` | Dados para experimentar: tabelas CSV de mapeamentos, pedidos em linguagem natural e a descrição de uma biblioteca. |
| `tests/` | Os testes automáticos. |
