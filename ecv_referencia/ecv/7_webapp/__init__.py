"""7 · Web application: every operation of modules 0 to 6 on a page, without the command line.

Receives: HTTP requests from the browser (pages and forms) or from scripts (/api/...).
Needs: the workspace (dominios/), the GraphDatabase of the active scope (memory or Neo4j) and the request
queues to the LLM.
Produces: pages and JSON; the actions change the domain's files through modules 0, 1, 2 and 6 (never directly).

    routes.py       the table of endpoints (method, path, handler, description)
    server.py       router, logging and errors around the handlers; serve()
    http.py         Request and Response
    context.py      AppContext: workspace, database, active scope, view catalogue
    logs.py         the server log (console, registos/servidor.log, the Registo tab)
    pages/          layout (tabs, scope selector) and HTML components
    handlers/       one module per tab: home, inventory, builder, amendments, requests, functions, database, views, validation

    python -m ecv servidor [--neo4j] [--ambito <dominio>] [--porta 8000]
"""
from .server import make_app, serve

__all__ = ["make_app", "serve"]
