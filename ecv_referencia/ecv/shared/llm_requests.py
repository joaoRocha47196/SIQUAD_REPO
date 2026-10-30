"""Requests to the LLM: how the application and the LLM exchange work.

The application never calls an LLM by itself. Every task that needs one (a step of the declaration, a
change request in natural language, the implementation of a function) becomes a request: a folder
with the full prompt and, when it arrives, the response.

    <queue>/<NNN>-<kind>[-<step>]/
        pedido.json     id, kind, title, step, state, created, response file, result
        prompt.md       the complete prompt (written by the application)
        resposta.json   the response (JSON) - or resposta.py for a function implementation
        resultado.json  what the application did with the response (written when it is registered)

There are two ways to answer a request, with the same result:
  1. In the repository: the LLM (for example Claude Code working on this repository) reads prompt.md,
     writes the response file in the same folder and commits it; after a `git pull`, the web
     application shows the request as answered.
  2. In the web application: the person copies the prompt to any LLM and pastes the response into
     the request page, which saves the response file.

States: pendente (no response yet) -> respondido (response file present) -> aplicado | rejeitado
(the application registered it, or could not; resultado.json says why). A rejected request can be
answered again.

Queues: each domain has one (dominios/<d>/pedidos: steps and changes); function implementations,
which are code and not part of a domain, use the global queue (pedidos/ at the repository root).
"""
import json
from dataclasses import dataclass
from pathlib import Path

from ecv import config

from .errors import RequestError
from .workspace import now, read_json, write_json

KINDS = {"passo": "Passo da declaração", "alteracao": "Pedido de alterações", "funcao": "Implementação de uma função",
         "adaptador": "Criação de um adaptador", "instancia": "Instância de teste"}
STATES = ("pendente", "respondido", "aplicado", "rejeitado")
RESPONSE_FILES = {"passo": "resposta.json", "alteracao": "resposta.json", "funcao": "resposta.py", "adaptador": "resposta.py",
                  "instancia": "resposta.json"}


@dataclass
class LlmRequest:
    folder: Path
    meta: dict

    @property
    def id(self):
        return self.meta["id"]

    @property
    def kind(self):
        return self.meta["tipo"]

    @property
    def step(self):
        return self.meta.get("passo")

    @property
    def title(self):
        return self.meta.get("titulo", self.id)

    @property
    def prompt_file(self):
        return self.folder / "prompt.md"

    @property
    def response_file(self):
        return self.folder / self.meta.get("ficheiroResposta", RESPONSE_FILES[self.kind])

    @property
    def result_file(self):
        return self.folder / "resultado.json"

    @property
    def state(self):
        """The stored state, or 'respondido' when a response file appeared after a pull."""
        stored = self.meta.get("estado", "pendente")
        if stored == "pendente" and self.response_file.exists():
            return "respondido"
        return stored

    def prompt(self):
        return self.prompt_file.read_text(encoding="utf-8")

    def has_response(self):
        return self.response_file.exists()

    def response_text(self):
        return self.response_file.read_text(encoding="utf-8") if self.has_response() else None

    def response_json(self):
        """The response decoded as JSON (raises RequestError when it is not valid JSON)."""
        text = self.response_text()
        if text is None:
            raise RequestError(f"o pedido {self.id} ainda não tem resposta ({self.response_file.name})")
        try:
            return json.loads(_strip_fences(text))
        except ValueError as e:
            raise RequestError(f"a resposta do pedido {self.id} não é JSON válido: {e}") from e

    def result(self):
        return read_json(self.result_file)

    def save_response(self, text):
        """Store a response (pasted in the web application or given on the command line)."""
        text = _strip_fences(text) if self.response_file.suffix == ".json" else text
        if self.response_file.suffix == ".json":
            try:
                json.loads(text)
            except ValueError as e:
                raise RequestError(f"a resposta não é JSON válido: {e}") from e
        self.response_file.write_text(text if text.endswith("\n") else text + "\n", encoding="utf-8")
        self._set(estado="respondido", respondido=now())

    def mark_applied(self, result):
        write_json(self.result_file, result)
        self._set(estado="aplicado", aplicado=now(), resumo=result.get("resumo"))

    def mark_rejected(self, reason):
        write_json(self.result_file, {"erro": reason})
        self._set(estado="rejeitado", rejeitado=now(), resumo=reason[:300])

    def _set(self, **values):
        self.meta.update(values)
        write_json(self.folder / "pedido.json", self.meta)

    def to_dict(self):
        return {**self.meta, "estado": self.state, "pasta": str(self.folder)}


def _strip_fences(text):
    """An LLM often wraps JSON in ```json fences: remove them."""
    t = text.strip()
    if t.startswith("```"):
        t = t.split("\n", 1)[1] if "\n" in t else ""
        if t.rstrip().endswith("```"):
            t = t.rstrip()[:-3]
    return t.strip()


class RequestQueue:
    def __init__(self, folder):
        self.folder = Path(folder)

    @classmethod
    def for_domain(cls, domain):
        return cls(domain.requests_folder)

    @classmethod
    def global_queue(cls):
        return cls(config.path("pedidosGlobais"))

    def requests(self):
        if not self.folder.exists():
            return []
        found = []
        for meta_file in sorted(self.folder.glob("*/pedido.json")):
            found.append(LlmRequest(meta_file.parent, read_json(meta_file)))
        return found

    def get(self, request_id):
        meta_file = self.folder / request_id / "pedido.json"
        if not meta_file.exists():
            raise RequestError(f"o pedido '{request_id}' não existe em {self.folder}")
        return LlmRequest(meta_file.parent, read_json(meta_file))

    def create(self, kind, title, prompt_text, step=None, **extra):
        if kind not in KINDS:
            raise RequestError(f"tipo de pedido desconhecido: {kind}")
        number = len(list(self.folder.glob("*/pedido.json"))) + 1 if self.folder.exists() else 1
        request_id = f"{number:03d}-{kind}" + (f"-{step}" if step else "")
        folder = self.folder / request_id
        folder.mkdir(parents=True, exist_ok=False)
        (folder / "prompt.md").write_text(prompt_text, encoding="utf-8")
        meta = {"id": request_id, "tipo": kind, "titulo": title, "passo": step, "estado": "pendente", "criado": now(),
                "ficheiroResposta": RESPONSE_FILES[kind], **extra}
        write_json(folder / "pedido.json", meta)
        return LlmRequest(folder, meta)
