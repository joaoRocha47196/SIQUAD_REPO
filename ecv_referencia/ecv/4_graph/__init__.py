"""4 · Graph: the graph model (graph_model.json), the common read interface and its two stores.

    base.py           Node, Edge and the Graph interface (nodes, node, outgoing, incoming)
    memory.py         MemoryGraph: no dependencies; used by tests, the CLI and the memory database
    neo4j_store.py    writing in batches and Neo4jGraph (the same interface over Cypher)
    cypher_export.py  the graph as a Cypher script
    database.py       GraphDatabase: the database of the web application (memory or Neo4j),
                      rebuilt from the declaration files

The declarations (JSON files) are the source of truth; the graph is what they become once
ingested: one integrated, deduplicated model that every query (views, validation, search) reads.
"""
from .base import Edge, Graph, Node, logical_id, read_json
from .memory import MemoryGraph

__all__ = ["Edge", "Graph", "Node", "MemoryGraph", "logical_id", "read_json"]
