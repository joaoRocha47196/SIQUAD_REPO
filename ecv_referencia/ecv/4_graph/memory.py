"""The graph in memory: the direct result of materialising declarations. No dependencies."""
from collections import defaultdict

from .base import Edge, Graph, Node


class MemoryGraph(Graph):
    def __init__(self):
        self._nodes = {}                          # id -> Node
        self._by_label = defaultdict(list)
        self._outgoing = defaultdict(list)        # id -> [Edge]
        self._incoming = defaultdict(list)
        self.edges = []

    # ------------------------------------------------------------------ building
    @staticmethod
    def node_id(label, key):
        return f"{label}:{key}"

    def add_node(self, label, key, props, extra_labels=()):
        nid = self.node_id(label, key)
        if nid in self._nodes:
            raise ValueError(f"nó repetido: {nid}")
        node = Node(nid, (label,) + tuple(extra_labels), dict(props))
        self._nodes[nid] = node
        for lb in node.labels:
            self._by_label[lb].append(node)
        return node

    def add_edge(self, edge_type, source, target, props=None):
        edge = Edge(edge_type, source, target, {k: v for k, v in (props or {}).items() if v is not None})
        self.edges.append(edge)
        self._outgoing[source.id].append(edge)
        self._incoming[target.id].append(edge)
        return edge

    # ------------------------------------------------------------------ interface
    def nodes(self, label=None):
        if label is None:
            return list(self._nodes.values())
        return list(self._by_label.get(label, []))

    def node(self, label, key):
        return self._nodes.get(self.node_id(label, key))

    def outgoing(self, node, edge_type=None):
        return [e for e in self._outgoing.get(node.id, []) if edge_type is None or e.type == edge_type]

    def incoming(self, node, edge_type=None):
        return [e for e in self._incoming.get(node.id, []) if edge_type is None or e.type == edge_type]

    # ------------------------------------------------------------------ statistics
    def counts(self):
        """(nodes per main label, edges per type)."""
        nodes = defaultdict(int)
        for n in self._nodes.values():
            nodes[n.label] += 1
        edges = defaultdict(int)
        for e in self.edges:
            edges[e.type] += 1
        return dict(nodes), dict(edges)
