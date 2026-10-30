"""AppContext: what the server keeps between requests.

    workspace     the domains (dominios/)
    database      GraphDatabase: the graph of the active scope (memory or Neo4j), rebuilt when its files change
    scope         the active scope: 'exemplos' (the example declarations), a domain id, or one declaration file
                  ('<exemplos|domain>::<file>': the views of that declaration alone)
    catalogue     the views that exist for the graph (module 5), computed once per database version
    log           the server log
"""
import threading

from ecv import config
from ecv.graph.database import GraphDatabase, Scope
from ecv.shared.errors import DomainError
from ecv.shared.workspace import Workspace
from ecv.views import links
from ecv.views.catalog import catalog
from ecv.views.viewmodels import build

EXAMPLES = "exemplos"
SEPARATOR = "::"                     # '<base scope>::<declaration file>'


def base_scope(name):
    return name.split(SEPARATOR, 1)[0]


class AppContext:
    def __init__(self, database=None, log=None, scope=EXAMPLES, workspace=None):
        self.workspace = workspace or Workspace()
        links.EDIT_BASE = "/alteracoes"            # the views link rules and properties to their edit forms
        self.database = database or GraphDatabase()
        self.log = log
        self._lock = threading.RLock()
        self._catalogue = (None, {})
        self._viewmodels = {}
        self.use_scope(scope)

    # ------------------------------------------------------------------ scopes
    def scopes(self):
        out = [Scope(EXAMPLES, "Declarações de exemplo", config.example_declarations)]
        for domain_id in self.workspace.domain_ids():
            domain = self.workspace.domain(domain_id)
            out.append(Scope(domain_id, f"Domínio {domain.name}", lambda d=domain: d.declaration_files()))
        return out

    def declaration_scopes(self, base):
        """One scope per declaration file of a base scope (the examples or a domain)."""
        scope = next(s for s in self.scopes() if s.name == base)
        return [Scope(f"{base}{SEPARATOR}{f.name}", f"Declaração {f.name}", lambda f=f: [f]) for f in scope.files()]

    def scope(self, name):
        candidates = self.scopes()
        if SEPARATOR in name and any(s.name == base_scope(name) for s in candidates):
            candidates = self.declaration_scopes(base_scope(name))
        found = next((s for s in candidates if s.name == name), None)
        if found is None:
            raise DomainError(f"âmbito desconhecido: {name}")
        return found

    def use_scope(self, name):
        with self._lock:
            rebuilt = self.database.use(self.scope(name))
            if rebuilt and self.log:
                self.log.event(f"base de dados construída: âmbito {name}, {self.database.info.seconds} s")
            return rebuilt

    @property
    def scope_name(self):
        return self.database.scope.name

    @property
    def domain(self):
        """The active domain, or None when the scope is the example declarations."""
        base = base_scope(self.scope_name)
        return None if base == EXAMPLES else self.workspace.domain(base)

    @property
    def declaration_file(self):
        """The declaration file of a one-declaration scope, or None."""
        return self.scope_name.split(SEPARATOR, 1)[1] if SEPARATOR in self.scope_name else None

    def require_domain(self):
        if self.domain is None:
            raise DomainError("escolha um domínio no seletor de âmbito (no topo da página)")
        return self.domain

    # ------------------------------------------------------------------ graph and views
    def refresh(self):
        """Rebuild the database if the files of the scope changed (called before every request)."""
        with self._lock:
            if self.database.refresh() and self.log:
                self.log.event(f"declarações alteradas no disco: base de dados reconstruída ({self.database.info.seconds} s)")

    @property
    def graph(self):
        return self.database.graph

    def catalogue(self):
        """{page: ViewEntry} for the current graph (links of the views point only to these pages)."""
        with self._lock:
            version, entries = self._catalogue
            if version != self.database.version:
                entries = {entry.page: entry for entry in catalog(self.graph)}
                self._catalogue = (self.database.version, entries)
                self._viewmodels = {}
            links.set_existing(entries)
            return entries

    def viewmodel(self, page):
        entry = self.catalogue().get(page)
        if entry is None:
            return None, None
        with self._lock:
            if page not in self._viewmodels:
                self._viewmodels[page] = build(self.graph, entry.viewmodel, **entry.params)
            return entry, self._viewmodels[page]
