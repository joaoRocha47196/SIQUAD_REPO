"""Export of an in-memory graph as a self-contained Cypher script (for the Neo4j Browser or cypher-shell):
uniqueness constraints, nodes and edges. To reload from scratch, run cypher/clear.cypher first."""
import json
from collections import defaultdict

from .model import key_of, load_model


def literal(value):
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)):
        return repr(value)
    if isinstance(value, list):
        return "[" + ", ".join(literal(x) for x in value) + "]"
    return json.dumps(str(value), ensure_ascii=False)


def map_literal(props):
    return "{" + ", ".join(f"{k}: {literal(v)}" for k, v in props.items() if v is not None) + "}"


def constraint_statements():
    """One uniqueness constraint per label, on the key defined by the model."""
    return [f"CREATE CONSTRAINT ecv_{label.lower()} IF NOT EXISTS FOR (n:{label}) REQUIRE n.{spec['chave']} IS UNIQUE;"
            for label, spec in load_model()["nos"].items()]


def clear_statements():
    labels = " OR ".join(f"n:{label}" for label in load_model()["nos"])
    return [f"MATCH (n) WHERE {labels} DETACH DELETE n;"]


def _node_ref(node, var):
    key = key_of(node.label)
    return f"({var}:{node.label} {{{key}: {literal(node.props[key])}}})"


def export(graph, origin=None):
    out = ["// Grafo de conhecimento de validação (ECV), gerado pela ECV de referência.",
           f"// Declarações: {origin}" if origin else "// Declarações: (memória)",
           "// Ordem: restrições de unicidade, nós, arestas.", "",
           "// ---------------------------------------------------------------- restrições"]
    out += constraint_statements()
    out += ["", "// ---------------------------------------------------------------- nós"]
    by_label = defaultdict(list)
    for node in graph.nodes():
        by_label[node.label].append(node)
    for label in load_model()["nos"]:
        nodes = by_label.get(label, [])
        if nodes:
            out.append(f"// {label} ({len(nodes)})")
            out += [f"CREATE (:{':'.join(n.labels)} {map_literal(n.props)});" for n in nodes]
    out += ["", "// ---------------------------------------------------------------- arestas"]
    by_type = defaultdict(list)
    for edge in graph.edges:
        by_type[edge.type].append(edge)
    for edge_type in load_model()["arestas"]:
        edges = by_type.get(edge_type, [])
        if edges:
            out.append(f"// {edge_type} ({len(edges)})")
            for e in edges:
                props = f" {map_literal(e.props)}" if e.props else ""
                out.append(f"MATCH {_node_ref(e.source, 'a')}, {_node_ref(e.target, 'b')} CREATE (a)-[:{edge_type}{props}]->(b);")
    return "\n".join(out) + "\n"
