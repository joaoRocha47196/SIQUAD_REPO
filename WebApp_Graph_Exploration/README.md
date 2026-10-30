# WebApp_Graph_Exploration

Esta pasta contém o protótipo inicial da aplicação Web, desenvolvido durante a preparação do artigo "Visual support for data model validation: a framework and case study", apresentado na conferência IV 2026.

O protótipo carregava o conhecimento de validação num grafo Neo4j e oferecia uma interface navegável sobre ele: os modelos, as propriedades, as regras e as relações entre eles, consultados e explorados diretamente na base de dados de grafos. Demonstrou o valor do grafo como suporte à pesquisa, à consulta e à análise do conhecimento, num cenário próximo do que seria uma utilização real.

A experiência mostrou, também, que uma interface sobre o grafo, por si só, acabava por reproduzir a navegação que o próprio grafo já permitia, sem que estivessem definidas as operações e as finalidades que deviam orientar essa exploração. Esta conclusão esteve na origem das vistas dirigidas à finalidade da implementação final, em [`../ecv_referencia`](../ecv_referencia), cuja aplicação Web mantém o grafo em memória para se concentrar no funcionamento das operações.

Esta pasta é mantida como registo histórico do trabalho.
