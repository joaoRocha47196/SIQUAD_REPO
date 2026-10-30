"""The common graph interface: nodes, edges and the four read operations every consumer uses.

ViewModels, the merge planner and the validation engine only call ``nodes``, ``node``, ``outgoing``
and ``incoming`` (and the shortcuts built on them). There are two implementations: MemoryGraph
(no dependencies) and Neo4jGraph (the same operations translated to Cypher), so every query runs
unchanged on both.

Node and edge properties keep the names of the graph model (graph_model.json), which is the
vocabulary of the ECV: ``nome``, ``chave``, ``descricao``, ...
"""
import json
from dataclasses import dataclass, field


@dataclass(frozen=True)
class Node:
    id: str
    labels: tuple
    props: dict = field(default_factory=dict, compare=False, hash=False)

    @property
    def label(self):
        """The main label: the first one that is not the generic 'Regra'."""
        for label in self.labels:
            if label != "Regra":
                return label
        return self.labels[0]

    def has(self, label):
        return label in self.labels

    def __getitem__(self, key):
        return self.props[key]

    def get(self, key, default=None):
        return self.props.get(key, default)

    @property
    def name(self):
        return self.props.get("nome") or self.props.get("id") or self.props.get("chave")


@dataclass(frozen=True)
class Edge:
    type: str
    source: Node
    target: Node
    props: dict = field(default_factory=dict, compare=False, hash=False)

    def get(self, key, default=None):
        return self.props.get(key, default)

    def value(self):
        """The edge's 'valor' attribute, decoded from JSON."""
        v = self.props.get("valor")
        return json.loads(v) if isinstance(v, str) else v


class Graph:
    """Read operations on the graph. Subclasses implement the first four."""

    def nodes(self, label):
        raise NotImplementedError

    def node(self, label, key):
        raise NotImplementedError

    def outgoing(self, node, edge_type=None):
        raise NotImplementedError

    def incoming(self, node, edge_type=None):
        raise NotImplementedError

    # ------------------------------------------------------------------ shortcuts
    def targets(self, node, edge_type):
        return [e.target for e in self.outgoing(node, edge_type)]

    def sources(self, node, edge_type):
        return [e.source for e in self.incoming(node, edge_type)]

    def first_target(self, node, edge_type):
        found = self.targets(node, edge_type)
        return found[0] if found else None

    def rules(self):
        return self.nodes("Regra")


def read_json(value, default=None):
    """Decode a property stored as JSON text (lists and objects are stored as text in Neo4j)."""
    if value is None:
        return default
    if isinstance(value, str):
        try:
            return json.loads(value)
        except ValueError:
            return value
    return value


def logical_id(node):
    """Identity of a node independent of the storage: '<label>:<key>' (e.g. 'USM:Morada')."""
    from .model import key_of
    return f"{node.label}:{node.props[key_of(node.label)]}"
