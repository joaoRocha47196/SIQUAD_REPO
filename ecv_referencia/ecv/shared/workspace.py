"""The workspace: the folder of domains, each one the files of one transformation (source data -> declarations).

    dominios/<d>/
        dominio.json        sources, exclusions, uses, scenarios (written by a person)
        estado.json         the state of phase 0, phase G and the review layers A to F
        inventario/         one inventory per source (phase 0)
        declaracoes/        one declaration per HLM (step A onwards)
        mapeamento.json     each element and rule of the sources -> its place in the declarations (or discarded)
        reservatorio.json   models, functions and contexts created but not yet used by any declaration
        notas.md            review notes written by a person (included in the next prompts)
        pedidos/            requests to the LLM and their responses (shared/llm_requests.py)

The files are the source of truth (versioned in git); everything else (the graph, the views) is derived.
"""
import datetime
import json
from functools import lru_cache
from pathlib import Path

from ecv import config

from .errors import DomainError, StepError

STEP_STATES = ("por iniciar", "em curso", "em revisão", "aceite")


def now():
    return datetime.datetime.now().isoformat(timespec="seconds")


@lru_cache(maxsize=1)
def step_ids():
    """'0' (extraction), 'G' (generation) and 'A' to 'F' (review layers), in order (from the build process of module 1)."""
    build_process = json.loads(config.path("processoConstrucao").read_text(encoding="utf-8"))
    return tuple(f["id"] for f in build_process["fases"])


def read_json(path, default=None):
    path = Path(path)
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else default


def write_json(path, data):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")


class Domain:
    def __init__(self, domain_id, root=None):
        self.id = domain_id
        self.folder = Path(root or config.path("dominios")) / domain_id
        if not self.definition_file.exists():
            raise DomainError(f"o domínio '{domain_id}' não existe (falta {self.definition_file})")
        self.definition = read_json(self.definition_file)
        self.state = self._load_state()

    # ------------------------------------------------------------------ files
    @property
    def definition_file(self):
        return self.folder / "dominio.json"

    @property
    def state_file(self):
        return self.folder / "estado.json"

    @property
    def inventory_folder(self):
        return self.folder / "inventario"

    @property
    def declarations_folder(self):
        return self.folder / "declaracoes"

    @property
    def mapping_file(self):
        return self.folder / "mapeamento.json"

    @property
    def reservoir_file(self):
        return self.folder / "reservatorio.json"

    @property
    def notes_file(self):
        return self.folder / "notas.md"

    @property
    def requests_folder(self):
        return self.folder / "pedidos"

    @property
    def name(self):
        return self.definition.get("nome", self.id)

    def sources(self):
        return self.definition.get("fontes", [])

    @property
    def uploads_folder(self):
        """Where the documents attached in the web application are kept (dominios/<d>/fontes/)."""
        return self.folder / "fontes"

    def save_definition(self):
        write_json(self.definition_file, self.definition)

    def set_source(self, source):
        """Add a source to dominio.json, or replace the one with the same id."""
        if not source.get("id") or not source.get("adaptador") or not source.get("caminho"):
            raise DomainError("uma fonte tem id, adaptador e caminho")
        sources = self.definition.setdefault("fontes", [])
        i = next((n for n, s in enumerate(sources) if s["id"] == source["id"]), None)
        if i is None:
            sources.append(source)
        else:
            sources[i] = {**sources[i], **source}
        self.save_definition()

    def remove_source(self, source_id):
        self.definition["fontes"] = [s for s in self.sources() if s["id"] != source_id]
        self.save_definition()

    def source_role(self, source_id):
        """'principal' or 'complementar' (a complementary source only confirms cardinalities and descriptions in step A)."""
        return next((s.get("passoA", "principal") for s in self.sources() if s["id"] == source_id), "principal")

    def inventory_files(self):
        return sorted(self.inventory_folder.glob("*.json")) if self.inventory_folder.exists() else []

    def inventories(self):
        """{source id: inventory (JSON dict)}."""
        return {f.stem: read_json(f) for f in self.inventory_files()}

    def declaration_files(self):
        return sorted(self.declarations_folder.glob("*.ecv.json")) if self.declarations_folder.exists() else []

    def notes(self):
        return self.notes_file.read_text(encoding="utf-8") if self.notes_file.exists() else ""

    def save_notes(self, text):
        self.notes_file.write_text(text, encoding="utf-8")

    def fingerprint(self):
        """Changes whenever a declaration, the mapping or the state changes (used to rebuild derived graphs)."""
        files = self.declaration_files() + [self.mapping_file, self.state_file]
        return tuple((str(f), f.stat().st_mtime_ns) for f in files if f.exists())

    # ------------------------------------------------------------------ state of the steps
    def _load_state(self):
        state = read_json(self.state_file) or {"dominio": self.id, "passos": {}}
        for step in step_ids():
            state["passos"].setdefault(step, {"estado": "por iniciar"})
        return state

    def save_state(self):
        write_json(self.state_file, self.state)

    def step_state(self, step):
        return self.state["passos"][step]["estado"]

    def set_step_state(self, step, state, **extra):
        entry = self.state["passos"].setdefault(step, {})
        entry["estado"] = state
        entry["atualizado"] = now()
        entry.update(extra)
        self.save_state()

    def add_request_to_step(self, step, request_id):
        entry = self.state["passos"].setdefault(step, {"estado": "por iniciar"})
        entry.setdefault("pedidos", []).append(request_id)
        self.save_state()

    def require_previous_accepted(self, step):
        ids = step_ids()
        i = ids.index(step)
        if i and self.step_state(ids[i - 1]) != "aceite":
            raise StepError(f"o passo {step} só começa depois de aceite o passo {ids[i - 1]} "
                            f"(estado atual: {self.step_state(ids[i - 1])})")

    def current_step(self):
        """The first phase or layer after phase 0 that is not accepted (the last one when all are)."""
        ids = step_ids()
        return next((s for s in ids[1:] if self.step_state(s) != "aceite"), ids[-1])


class Workspace:
    """The folder of domains."""

    def __init__(self, root=None):
        self.root = Path(root or config.path("dominios"))

    def domain_ids(self):
        if not self.root.exists():
            return []
        return sorted(p.name for p in self.root.iterdir() if (p / "dominio.json").exists())

    def domain(self, domain_id):
        return Domain(domain_id, self.root)

    def create_domain(self, domain_id, name, description, sources=(), uses=(), scenarios=()):
        if not domain_id or not domain_id.replace("_", "").isalnum() or domain_id != domain_id.lower():
            raise DomainError("o identificador do domínio tem só letras minúsculas, algarismos e _")
        folder = self.root / domain_id
        if (folder / "dominio.json").exists():
            raise DomainError(f"o domínio '{domain_id}' já existe")
        write_json(folder / "dominio.json", {"id": domain_id, "nome": name, "descricao": description, "fontes": list(sources),
                                             "excluidos": [], "utilizacoes": list(uses), "cenarios": list(scenarios),
                                             "mapeamentos": [], "metainformacao": {}})
        return self.domain(domain_id)
