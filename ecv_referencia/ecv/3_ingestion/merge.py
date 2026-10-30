"""Merge: add the graph of one declaration to an existing graph, without duplicates.

Each declaration describes one HLM and repeats, in full, the shared models (USM Morada, SM Cliente,
...), functions and external contexts it depends on. When ingesting, each node is looked up in the
existing graph by its logical identity ('<label>:<key>'):

  - not there            -> new node, with every edge it owns;
  - there and equal      -> reused; its edges are already there;
  - there and different  -> conflict (the same entity with another definition).

"Equal" compares the node's signature: its attributes and the edges it owns. The owner of each edge
comes from graph_model.json: 'origem' (the source node) or 'regra' (the rule named in the edge's
'regra' attribute, for the LE edges that leave a shared Funcao). So a shared model with one more
property, a different composition or a changed rule is detected instead of silently summed.

With conflicts nothing is added (policy 'rejeitar' in the configuration). Planning only reads the
target through the Graph interface, so it works the same against memory and Neo4j; applying the
plan depends on the target.
"""
import json
from dataclasses import dataclass, field

from ecv import config
from ecv.graph.base import logical_id
from ecv.graph.model import edge_owner, key_of


def _edge_owner_id(edge):
    """Identity of the owner of an edge: the source node, or 'Regra:<id>' for edges owned by a rule."""
    if edge_owner(edge.type) == "regra":
        return f"Regra:{edge.props.get('regra')}"
    return logical_id(edge.source)


def _node_owner_id(node):
    """The owner identity of a node (rules own by their id, like the LE edges)."""
    return f"Regra:{node['id']}" if node.has("Regra") else logical_id(node)


def _defined(props):
    return {k: v for k, v in props.items() if v is not None}


def _edge_signature(edge):
    return (edge.type, logical_id(edge.source), logical_id(edge.target),
            json.dumps(_defined(edge.props), sort_keys=True, ensure_ascii=False))


def _owned_edges(graph, node):
    """Edges the node owns, read through the Graph interface (memory or Neo4j)."""
    owned = [e for e in graph.outgoing(node) if edge_owner(e.type) == "origem"]
    if node.has("Regra"):
        rule_id = node["id"]
        functions = {}
        for part in graph.targets(node, "RESTRITA_POR") + graph.targets(node, "CONDICIONADA_POR"):
            for f in graph.targets(part, "CHAMA"):
                functions[f.id] = f
        for f in functions.values():
            owned += [e for e in graph.outgoing(f, "LE") if e.get("regra") == rule_id]
    return owned


@dataclass
class Conflict:
    node: str
    reason: str
    details: list = field(default_factory=list)

    def __str__(self):
        shown = "".join(f"\n      {d}" for d in self.details[:8])
        more = f"\n      … (+{len(self.details) - 8})" if len(self.details) > 8 else ""
        return f"  CONFLITO {self.node}: {self.reason}{shown}{more}"


@dataclass
class MergePlan:
    origin: str
    new_nodes: list = field(default_factory=list)
    reused: list = field(default_factory=list)
    new_edges: list = field(default_factory=list)
    conflicts: list = field(default_factory=list)

    @property
    def valid(self):
        return not self.conflicts

    def reused_by_label(self):
        counts = {}
        for item in self.reused:
            label = item.split(":", 1)[0]
            counts[label] = counts.get(label, 0) + 1
        return counts

    def summary(self):
        reused = ", ".join(f"{k} {v}" for k, v in sorted(self.reused_by_label().items())) or "nenhum"
        text = (f"{self.origin}: {len(self.new_nodes)} nó(s) novo(s), {len(self.new_edges)} aresta(s) nova(s), "
                f"{len(self.reused)} nó(s) já existente(s) e iguais ({reused})")
        if self.conflicts:
            text += f"; {len(self.conflicts)} conflito(s): nada acrescentado\n" + "\n".join(map(str, self.conflicts))
        return text

    def to_dict(self):
        return {"origem": self.origin, "valido": self.valid, "resumo": self.summary().split("\n")[0],
                "novos": [n.id for n in self.new_nodes], "reutilizados": self.reused,
                "conflitos": [{"no": c.node, "motivo": c.reason, "detalhe": c.details} for c in self.conflicts]}


def _property_differences(new, existing):
    pn, pe = _defined(new.props), _defined(existing.props)
    return [f"atributo {k}: existente {pe.get(k)!r} ≠ novo {pn.get(k)!r}"
            for k in sorted(set(pn) | set(pe)) if pn.get(k) != pe.get(k)]


def _format_signature(sig):
    edge_type, source, target, props = sig
    return f"({source})-[{edge_type} {props}]->({target})" if props != "{}" else f"({source})-[{edge_type}]->({target})"


def plan_merge(target, new, origin="declaração"):
    """Compare the graph 'new' (one materialised declaration) with 'target' and return the MergePlan."""
    plan = MergePlan(origin)
    existing = {}                                  # logical id -> (new node, node in the target)
    for node in new.nodes():
        found = target.node(node.label, node.props[key_of(node.label)])
        if found is None:
            plan.new_nodes.append(node)
        else:
            existing[logical_id(node)] = (node, found)

    new_owners = {logical_id(n) for n in plan.new_nodes} | {_node_owner_id(n) for n in plan.new_nodes}
    for node, found in existing.values():
        differences = _property_differences(node, found)
        in_new = {_edge_signature(e) for e in _owned_edges(new, node)}
        in_target = {_edge_signature(e) for e in _owned_edges(target, found)}
        differences += [f"aresta só na nova declaração: {_format_signature(s)}" for s in sorted(in_new - in_target)]
        differences += [f"aresta só no grafo existente: {_format_signature(s)}" for s in sorted(in_target - in_new)]
        if differences:
            plan.conflicts.append(Conflict(logical_id(node), "já existe com outra definição", differences))
        else:
            plan.reused.append(logical_id(node))

    plan.new_edges = [e for e in new.edges if _edge_owner_id(e) in new_owners]
    return plan


def apply_to_memory(target, plan):
    """Add the plan's new nodes and edges to a MemoryGraph."""
    if not plan.valid and config.INGESTION["conflitos"] == "rejeitar":
        raise ValueError("o plano tem conflitos: " + plan.summary())
    for node in plan.new_nodes:
        target.add_node(node.label, node.props[key_of(node.label)], node.props,
                        extra_labels=tuple(lb for lb in node.labels if lb != node.label))
    for edge in plan.new_edges:
        source = target.node(edge.source.label, edge.source.props[key_of(edge.source.label)])
        dest = target.node(edge.target.label, edge.target.props[key_of(edge.target.label)])
        target.add_edge(edge.type, source, dest, edge.props)
    return len(plan.new_nodes), len(plan.new_edges)
