"""5 · Views: ViewModels (queries on the graph that return the data of a view, as JSON) and their rendering
as HTML pages.

Receives: a graph (memory or Neo4j) and the parameters of a view.
Produces: the ViewModel (JSON) and, from it, the page (HTML). Never changes the graph.

    viewmodels/     one query per kind of view (REGISTRY) and the equivalent Cypher
    catalog.py      which views exist for a graph (derived from the graph itself)
    links.py        page names and links between views
    presentation/   ViewModel -> HTML (one renderer per kind of view)
    static_site.py  every view of a graph written to a folder (examples for the documentation)
"""
