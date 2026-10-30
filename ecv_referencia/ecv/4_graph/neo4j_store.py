"""Neo4j storage: writing (constraints, nodes and edges in batches) and reading through the common
Graph interface.

Requires the 'neo4j' package (pip install neo4j). Writes use UNWIND batches, one per set of node
labels and one per (edge type, source label, target label), because labels cannot be parameters.
"""
from collections import defaultdict

from ecv import config

from .base import Edge, Graph, Node
from .cypher_export import clear_statements, constraint_statements
from .model import key_of


def connect(uri, user, password):
    try:
        from neo4j import GraphDatabase
    except ImportError as e:  # pragma: no cover
        raise RuntimeError("Falta o pacote 'neo4j': pip install neo4j") from e
    driver = GraphDatabase.driver(uri, auth=(user, password))
    driver.verify_connectivity()
    return driver


def _batches(rows, size):
    for i in range(0, len(rows), size):
        yield rows[i:i + size]


def prepare(driver, database=None, clear=False):
    """Create the uniqueness constraints (and, if asked, delete the ECV nodes first)."""
    with driver.session(database=database) as s:
        if clear:
            for q in clear_statements():
                s.run(q).consume()
        for q in constraint_statements():
            s.run(q).consume()


def append(driver, nodes, edges, database=None):
    """Create the given nodes and edges (edge ends may already exist). Returns (nodes, edges) written."""
    size = config.INGESTION["loteUnwind"]
    with driver.session(database=database) as s:
        by_labels = defaultdict(list)
        for node in nodes:
            by_labels[node.labels].append({k: v for k, v in node.props.items() if v is not None})
        for labels, rows in by_labels.items():
            label_text = ":".join(f"`{lb}`" for lb in labels)
            for batch in _batches(rows, size):
                s.run(f"UNWIND $rows AS r CREATE (n:{label_text}) SET n = r", rows=batch).consume()
        groups = defaultdict(list)
        for e in edges:
            ka, kb = key_of(e.source.label), key_of(e.target.label)
            groups[(e.type, e.source.label, ka, e.target.label, kb)].append(
                {"a": e.source.props[ka], "b": e.target.props[kb], "p": e.props})
        for (edge_type, la, ka, lb, kb), rows in groups.items():
            for batch in _batches(rows, size):
                s.run(f"UNWIND $rows AS r MATCH (a:`{la}` {{`{ka}`: r.a}}) MATCH (b:`{lb}` {{`{kb}`: r.b}}) "
                      f"CREATE (a)-[e:`{edge_type}`]->(b) SET e = r.p", rows=batch).consume()
    return len(nodes), len(edges)


def import_graph(graph, driver, database=None, clear=True):
    """Load a complete in-memory graph into Neo4j (by default after deleting the ECV nodes)."""
    prepare(driver, database, clear)
    return append(driver, graph.nodes(), graph.edges, database)


def counts(driver, database=None):
    """(nodes per main label, edges per type) as stored in Neo4j."""
    with driver.session(database=database) as s:
        nodes = {}
        for r in s.run("MATCH (n) RETURN [l IN labels(n) WHERE l <> 'Regra'][0] AS l, count(*) AS c"):
            if r["l"]:
                nodes[r["l"]] = r["c"]
        edges = {r["t"]: r["c"] for r in s.run("MATCH ()-[e]->() RETURN type(e) AS t, count(*) AS c")}
    return nodes, edges


class Neo4jGraph(Graph):
    """The four operations of the Graph interface over a Neo4j database, with a per-instance cache."""

    def __init__(self, driver, database=None):
        self.driver = driver
        self.database = database
        self._cache = {}

    def _query(self, q, **params):
        with self.driver.session(database=self.database) as s:
            return list(s.run(q, **params))

    @staticmethod
    def _node(element_id, labels, props):
        return Node(element_id, tuple(sorted(labels, key=lambda lb: lb == "Regra")), dict(props))

    def nodes(self, label):
        k = ("nodes", label)
        if k not in self._cache:
            rows = self._query(f"MATCH (n:`{label}`) RETURN elementId(n) AS id, labels(n) AS l, properties(n) AS p")
            self._cache[k] = [self._node(r["id"], r["l"], r["p"]) for r in rows]
        return self._cache[k]

    def node(self, label, key):
        k = ("node", label, key)
        if k not in self._cache:
            rows = self._query(f"MATCH (n:`{label}` {{`{key_of(label)}`: $v}}) "
                               "RETURN elementId(n) AS id, labels(n) AS l, properties(n) AS p", v=key)
            self._cache[k] = self._node(rows[0]["id"], rows[0]["l"], rows[0]["p"]) if rows else None
        return self._cache[k]

    def _edges(self, node, edge_type, outgoing):
        k = ("out" if outgoing else "in", node.id, edge_type)
        if k not in self._cache:
            pattern = "(a)-[r]->(b)" if outgoing else "(b)-[r]->(a)"
            where = " AND type(r) = $t" if edge_type else ""
            rows = self._query(f"MATCH {pattern} WHERE elementId(a) = $id{where} "
                               "RETURN type(r) AS t, properties(r) AS rp, elementId(b) AS bid, labels(b) AS bl, "
                               "properties(b) AS bp", id=node.id, t=edge_type)
            edges = []
            for r in rows:
                other = self._node(r["bid"], r["bl"], r["bp"])
                edges.append(Edge(r["t"], node, other, dict(r["rp"])) if outgoing else Edge(r["t"], other, node, dict(r["rp"])))
            self._cache[k] = edges
        return self._cache[k]

    def outgoing(self, node, edge_type=None):
        return self._edges(node, edge_type, True)

    def incoming(self, node, edge_type=None):
        return self._edges(node, edge_type, False)
