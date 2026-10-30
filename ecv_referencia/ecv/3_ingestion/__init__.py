"""3 · Ingestion: ECV declaration -> graph, one declaration (one HLM) at a time, without duplicates.

    load ──▶ verify ──▶ materialise ──▶ plan the merge ──▶ apply
    (declaration) (verification) (materialization) (merge.plan_merge) (memory or Neo4j)

Receives: declaration files (or Declaration objects) and a target graph.
Produces: the target graph with the new nodes and edges, and one IngestionResult per declaration
(verification report and merge plan).
"""
from dataclasses import dataclass, field

from ecv.graph.memory import MemoryGraph

from .declaration import Declaration, RuleSite
from .descriptions import derive
from .materialization import MaterializationError, Materializer, materialize
from .merge import Conflict, MergePlan, apply_to_memory, plan_merge
from .verification import Problem, Report, verify


@dataclass
class IngestionResult:
    """What happened to one declaration: the verification report and the merge plan (if it got there)."""
    origin: str
    report: Report
    plan: MergePlan | None = None
    applied: bool = False

    @property
    def accepted(self):
        return self.applied

    def summary(self):
        if not self.report.valid:
            return f"{self.origin}: REJEITADA na verificação ({self.report.summary()})"
        text = f"{self.origin}: verificação {self.report.summary()}"
        if self.plan is not None:
            text += "\n  " + self.plan.summary()
        return text


@dataclass
class Ingestion:
    graph: object
    results: list = field(default_factory=list)

    @property
    def valid(self):
        return all(r.accepted for r in self.results)


def _as_declaration(d):
    return d if isinstance(d, Declaration) else Declaration.load(d)


def prepare(d):
    """Load and verify a declaration; materialise it if valid. Returns (declaration, result, graph or None)."""
    decl = _as_declaration(d)
    report = verify(decl)
    result = IngestionResult(decl.name, report)
    if not report.valid:
        return decl, result, None
    return decl, result, Materializer(decl).run()


def ingest(declarations, target=None):
    """Ingest declarations (paths or Declaration), in order, into a MemoryGraph (a new one by default)."""
    target = target if target is not None else MemoryGraph()
    ingestion = Ingestion(target)
    for d in declarations:
        _, result, new = prepare(d)
        if new is not None:
            result.plan = plan_merge(target, new, result.origin)
            if result.plan.valid:
                apply_to_memory(target, result.plan)
                result.applied = True
        ingestion.results.append(result)
    return ingestion


def ingest_neo4j(declarations, driver, database=None, clear=False):
    """Ingest declarations into Neo4j: plan each merge against what is already there and write only what is new."""
    from ecv.graph.neo4j_store import Neo4jGraph, append, prepare as prepare_database
    prepare_database(driver, database, clear)
    results = []
    for d in declarations:
        _, result, new = prepare(d)
        if new is not None:
            result.plan = plan_merge(Neo4jGraph(driver, database), new, result.origin)   # fresh read per declaration
            if result.plan.valid:
                append(driver, result.plan.new_nodes, result.plan.new_edges, database)
                result.applied = True
        results.append(result)
    return results


__all__ = ["Declaration", "RuleSite", "verify", "Report", "Problem", "derive", "materialize", "Materializer",
           "MaterializationError", "plan_merge", "MergePlan", "Conflict", "apply_to_memory", "ingest",
           "ingest_neo4j", "Ingestion", "IngestionResult", "prepare"]
