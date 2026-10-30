"""GraphDatabase: the database behind the web application.

The declaration files are the source of truth. The database is the graph they become once ingested,
kept for queries: every view, validation and search reads it through the Graph interface.

    declaration files ──ingest (module 3)──▶ MemoryGraph ──(backend neo4j)──▶ Neo4j
          (scope)                              │                                  │
                                               └──────────── Graph interface ─────┘──▶ views, validation, search

A scope is a named set of declaration files: the example declarations, or the declarations of one
domain. The database holds one scope at a time and is rebuilt when the files of the scope change
(their paths and modification times form the fingerprint), so a change applied by the builder or
the amendments module is visible in the next request.

Backends:
    memoria   the graph lives in the server process (no dependencies)
    neo4j     the graph is written to Neo4j (cleared and loaded on each rebuild) and queried with Cypher;
              the views can then also be run as Cypher (module 5, viewmodels/cypher)
"""
import threading
import time
from dataclasses import dataclass, field

from ecv import config
from ecv.ingestion import Declaration, ingest, plan_merge, prepare

from .memory import MemoryGraph

BACKENDS = ("memoria", "neo4j")


@dataclass
class Scope:
    name: str
    title: str
    files: callable                 # () -> list of declaration paths, in ingestion order

    def fingerprint(self):
        return tuple((str(f), f.stat().st_mtime_ns) for f in self.files() if f.exists())


@dataclass
class BuildInfo:
    scope: str
    files: list
    seconds: float
    built_at: str
    results: list = field(default_factory=list)       # IngestionResult per declaration

    @property
    def rejected(self):
        return [r for r in self.results if not r.accepted]


class GraphDatabase:
    def __init__(self, backend="memoria", uri=None, user=None, password=None, database=None):
        if backend not in BACKENDS:
            raise ValueError(f"backend desconhecido: {backend} ({', '.join(BACKENDS)})")
        self.backend = backend
        self.neo4j = {"uri": uri or config.neo4j_setting("uri"), "utilizador": user or config.neo4j_setting("utilizador"),
                      "base": database or config.neo4j_setting("base")}
        self._password = password or config.neo4j_setting("senha")
        self._driver = None
        self._lock = threading.RLock()
        self.scope = None
        self._fingerprint = None
        self.memory = None            # the last ingested MemoryGraph (also used for merge previews)
        self.graph = None             # what the queries read: MemoryGraph or Neo4jGraph
        self.info = None
        self.version = 0              # incremented on every rebuild (callers cache per version)

    # ------------------------------------------------------------------ connection
    @property
    def driver(self):
        if self._driver is None:
            from .neo4j_store import connect
            self._driver = connect(self.neo4j["uri"], self.neo4j["utilizador"], self._password)
        return self._driver

    def close(self):
        if self._driver is not None:
            self._driver.close()
            self._driver = None

    # ------------------------------------------------------------------ building
    def use(self, scope):
        """Select the scope (rebuilds if it is another scope or its files changed)."""
        with self._lock:
            if self.scope is None or scope.name != self.scope.name:
                self.scope, self._fingerprint = scope, None
            return self.refresh()

    def refresh(self, force=False):
        """Rebuild when the scope's files changed. Returns True when it rebuilt."""
        with self._lock:
            fingerprint = self.scope.fingerprint()
            if not force and fingerprint == self._fingerprint:
                return False
            self._build(fingerprint)
            return True

    def _build(self, fingerprint):
        start = time.time()
        files = list(self.scope.files())
        ingestion = ingest(files)
        self.memory = ingestion.graph
        if self.backend == "neo4j":
            from .neo4j_store import Neo4jGraph, import_graph
            import_graph(self.memory, self.driver, self.neo4j["base"], clear=True)
            self.graph = Neo4jGraph(self.driver, self.neo4j["base"])
        else:
            self.graph = self.memory
        self._fingerprint = fingerprint
        self.version += 1
        self.info = BuildInfo(self.scope.name, [str(f) for f in files], round(time.time() - start, 2),
                              time.strftime("%Y-%m-%dT%H:%M:%S"), ingestion.results)

    # ------------------------------------------------------------------ reading
    def counts(self):
        if self.backend == "neo4j":
            from .neo4j_store import counts
            return counts(self.driver, self.neo4j["base"])
        return self.memory.counts()

    def status(self):
        nodes, edges = self.counts() if self.graph is not None else ({}, {})
        info = self.info
        return {
            "backend": self.backend,
            "neo4j": self.neo4j if self.backend == "neo4j" else None,
            "ambito": self.scope.name if self.scope else None,
            "tituloAmbito": self.scope.title if self.scope else None,
            "versao": self.version,
            "construido": info.built_at if info else None,
            "segundos": info.seconds if info else None,
            "ficheiros": info.files if info else [],
            "declaracoes": [{"origem": r.origin, "aceite": r.accepted, "resumo": r.summary()} for r in info.results] if info else [],
            "rejeitadas": len(info.rejected) if info else 0,
            "nos": nodes, "arestas": edges,
        }

    def preview_merge(self, declaration_data, origin="declaração colada"):
        """What a declaration would add to the current graph (new, reused, conflicts), without writing."""
        decl = Declaration(declaration_data, origin)
        _, result, new = prepare(decl)
        if new is not None:
            result.plan = plan_merge(self.graph, new, origin)
        return result


def memory_graph(files):
    """A one-off in-memory graph of some declaration files (for the CLI and the tests)."""
    return ingest(files).graph if files else MemoryGraph()
