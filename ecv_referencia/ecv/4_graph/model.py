"""The graph model (graph_model.json): node labels with their key and attributes, edge types with
their ends, attributes and owner (for merging). Also checks that a graph conforms to it."""
import json
from functools import lru_cache
from pathlib import Path

MODEL_FILE = Path(__file__).with_name("graph_model.json")


@lru_cache(maxsize=1)
def load_model():
    with MODEL_FILE.open(encoding="utf-8") as f:
        return json.load(f)


def key_of(label):
    """The attribute that identifies a node of this label ('nome', 'chave' or 'id')."""
    return load_model()["nos"][label]["chave"]


def extra_labels(label):
    return tuple(load_model()["nos"][label].get("rotulosExtra", []))


def edge_owner(edge_type):
    """'origem' (the source node owns the edge) or 'regra' (the rule named in the edge's 'regra' attribute)."""
    return load_model()["arestas"][edge_type].get("dono")


def conformance(graph):
    """Deviations of an in-memory graph from the model: unknown labels or types, unexpected ends or attributes."""
    model = load_model()
    problems = []
    for node in graph.nodes():
        spec = model["nos"].get(node.label)
        if spec is None:
            problems.append(f"rótulo desconhecido: {node.label}")
            continue
        extra = set(node.props) - set(spec["atributos"])
        if extra:
            problems.append(f"{node.id}: atributos fora do modelo {sorted(extra)}")
    for edge in graph.edges:
        spec = model["arestas"].get(edge.type)
        if spec is None:
            problems.append(f"tipo de aresta desconhecido: {edge.type}")
            continue
        if edge.source.label not in spec["de"] or edge.target.label not in spec["para"]:
            problems.append(f"{edge.type}: {edge.source.label} → {edge.target.label} não previsto")
        extra = set(edge.props) - set(spec["atributos"])
        if extra:
            problems.append(f"{edge.type} {edge.source.id} → {edge.target.id}: atributos fora do modelo {sorted(extra)}")
    return problems
