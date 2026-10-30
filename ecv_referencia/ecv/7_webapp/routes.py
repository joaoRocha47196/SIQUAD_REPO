"""The endpoints of the web application: one line per route (method, path, handler, what it does).

Paths with <name> take that segment as a parameter. Every page has a JSON counterpart under /api/
for the same data. This table is also shown on the page /rotas.
"""
from dataclasses import dataclass

from .handlers import amendments, builder, database, functions, home, instances, inventory, requests, validation, views


@dataclass(frozen=True)
class Route:
    method: str
    path: str
    handler: object
    description: str
    tab: str = ""


ROUTES = [
    # overview and scope
    Route("GET", "/", home.overview, "Visão geral: âmbito ativo, base de dados, domínios e passos, pedidos pendentes", "inicio"),
    Route("POST", "/ambito", home.select_scope, "Muda o âmbito ativo (exemplos ou um domínio); a base de dados é reconstruída"),
    Route("GET", "/rotas", home.routes_page, "Esta tabela de rotas", "inicio"),
    Route("GET", "/registo", home.log_page, "Registo do servidor: pedidos HTTP e ações", "registo"),
    Route("GET", "/api/registo", home.log_api, "Registo do servidor (JSON)"),
    # 0 · inventory
    Route("GET", "/inventario", inventory.page, "Inventários do domínio: fontes, grupos, elementos e regras", "inventario"),
    Route("POST", "/inventario/extrair", inventory.extract, "Fase 0: corre os adaptadores e escreve os inventários"),
    Route("GET", "/api/inventario", inventory.api, "Inventários do domínio (JSON; ?fonte=)"),
    # 1 · declaration (steps)
    Route("GET", "/declaracao", builder.page, "1. Extração (fontes, documentos, adaptadores) e 2. Geração; estado das camadas A a F", "declaracao"),
    Route("POST", "/declaracao/dominio", builder.create_domain, "Cria um domínio novo (dominios/<id>/dominio.json) e passa a trabalhar nele"),
    Route("POST", "/declaracao/fonte", builder.add_source, "Acrescenta ou muda uma fonte: documentos anexados (multipart) ou caminho; adaptador"),
    Route("POST", "/declaracao/fonte/remover", builder.remove_source, "Remove uma fonte de dominio.json"),
    Route("POST", "/declaracao/adaptador", builder.request_adapter, "Pede ao LLM a criação de um adaptador (fila global)"),
    Route("POST", "/declaracao/extrair", builder.extract, "1. Extração: corre os adaptadores e escreve os inventários"),
    Route("POST", "/declaracao/preparar", builder.prepare, "2. Geração: cria o pedido ao LLM (prompt.md)"),
    Route("POST", "/declaracao/verificar", builder.verify, "Corre as verificações de um passo ou camada"),
    Route("POST", "/declaracao/aceitar", builder.accept, "Aceita o passo ou a camada (se as verificações passam)"),
    Route("GET", "/declaracao/ficheiro/<nome>", builder.declaration_file, "Uma declaração do domínio (JSON)"),
    Route("GET", "/declaracao/cypher/<nome>", builder.cypher_load, "Carga Cypher (Neo4j) de uma declaração ou de todas (nome 'todas'); grava em saidas/"),
    Route("POST", "/declaracao/estaticas", builder.static_views, "Gera as vistas estáticas de uma declaração ou de todas em dominios/<d>/saidas/"),
    Route("GET", "/estaticas/<dominio>/<declaracao>/<pagina>", builder.static_file, "Uma página (ou ViewModel) das vistas estáticas geradas"),
    Route("GET", "/mapeamento", builder.mapping_page, "Mapeamento das fontes para as declarações e cobertura por passo", "declaracao"),
    Route("GET", "/api/declaracao", builder.api, "Estado dos passos do domínio (JSON)"),
    # 2 · amendments
    Route("GET", "/alteracoes", amendments.page, "Alterações: linguagem natural, operações, tabela CSV, vocabulário", "alteracoes"),
    Route("POST", "/alteracoes/pedido", amendments.natural_language, "Pedido em linguagem natural: cria um pedido ao LLM"),
    Route("POST", "/alteracoes/operacoes", amendments.operations, "Pré-visualiza ou aplica operações (JSON)"),
    Route("POST", "/alteracoes/csv", amendments.csv_table, "Tabela CSV de mapeamentos conhecidos: gera regras RIR"),
    Route("GET", "/api/operacoes", amendments.vocabulary_api, "Vocabulário de operações (JSON)"),
    Route("POST", "/api/alteracoes", amendments.operations_api, "Aplica operações {operacoes, passo?, aplicar?} (JSON)"),
    # requests to the LLM
    Route("GET", "/pedidos", requests.list_page, "Pedidos ao LLM: filas dos domínios e fila global", "pedidos"),
    Route("GET", "/pedidos/<fila>/<pedido>", requests.detail, "Um pedido: prompt, resposta, resultado", "pedidos"),
    Route("GET", "/pedidos/<fila>/<pedido>/prompt.md", requests.prompt_file, "O prompt de um pedido (texto)"),
    Route("POST", "/pedidos/<fila>/<pedido>/resposta", requests.save_response, "Guarda a resposta colada"),
    Route("POST", "/pedidos/<fila>/<pedido>/registar", requests.register, "Aplica a resposta (passo, alteração ou função)"),
    Route("GET", "/api/pedidos", requests.api, "Pedidos de todas as filas (JSON)"),
    # functions
    Route("GET", "/funcoes", functions.page, "Funções declaradas e implementadas; pedir implementação", "funcoes"),
    Route("POST", "/funcoes/pedir", functions.request_implementation, "Cria o pedido de implementação de uma função (fila global)"),
    Route("GET", "/api/funcoes", functions.api, "Funções declaradas, com o estado da implementação (JSON)"),
    # 3/4 · database
    Route("GET", "/base", database.page, "Base de dados: backend, âmbito, declarações ingeridas, contagens", "base"),
    Route("POST", "/base/reconstruir", database.rebuild, "Reconstrói a base de dados a partir dos ficheiros"),
    Route("POST", "/base/fusao", database.preview_merge, "Pré-visualiza a fusão de uma declaração colada (sem escrever)"),
    Route("GET", "/pesquisa", database.search_page, "Pesquisa no grafo e modelos semelhantes", "base"),
    Route("GET", "/api/base", database.status_api, "Estado da base de dados (JSON)"),
    Route("GET", "/api/pesquisa", database.search_api, "Pesquisa no grafo (JSON; ?q=)"),
    Route("GET", "/api/semelhantes", database.similar_api, "Modelos com propriedades semelhantes (JSON; ?p=a,b,c)"),
    # 5 · views
    Route("GET", "/vistas", views.catalogue_page, "Catálogo das vistas do grafo ativo", "vistas"),
    Route("GET", "/vistas/<pagina>", views.view_page, "Uma vista, construída a pedido a partir do ViewModel", "vistas"),
    Route("GET", "/api/vistas", views.catalogue_api, "Catálogo das vistas (JSON)"),
    Route("GET", "/api/vm/<pagina>", views.viewmodel_api, "O ViewModel de uma vista do catálogo (JSON)"),
    Route("POST", "/api/vm", views.build_api, "Constrói um ViewModel {viewmodel, parametros} (JSON)"),
    # 6 · validation
    Route("GET", "/validacao", validation.page, "Validação de uma instância: formulário e exemplos", "validacao"),
    Route("POST", "/validacao", validation.run, "Valida a instância e mostra o resultado", "validacao"),
    Route("POST", "/api/validar", validation.api, "Valida {instancia, perfil | hlm, contextos} (JSON)"),
    Route("GET", "/instancias", instances.page, "Instâncias de teste: esqueleto a partir da estrutura e do perfil; gravadas", "instancias"),
    Route("POST", "/instancias/pedido", instances.request_instance, "Cria o pedido ao LLM de uma instância de teste (contexto mínimo)"),
    Route("POST", "/instancias/gravar", instances.save, "Valida e, com acao=gravar, grava a instância em dominios/<d>/instancias/"),
    Route("POST", "/instancias/validar", instances.validate, "Valida uma instância gravada"),
]
