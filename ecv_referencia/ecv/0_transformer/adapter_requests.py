"""Requests to create an adapter for a source format without one (kind "adaptador", global queue pedidos/).

    request_adapter(name, description, sample_path) -> LlmRequest: prompt with the format, a sample of the source,
                                                       the inventory format, the rule categories and an example adapter
    (the LLM answers with resposta.py: a module with NAME, DESCRIPTION and adapt(path))
    register_adapter(request) -> the module is checked (it compiles, defines NAME = the requested name and adapt)
                                 and written to ecv/0_transformer/adapters/a_<name>.py; the adapters are reloaded
"""
import inspect
import re
from pathlib import Path

from ecv.shared.errors import RequestError
from ecv.shared.llm_requests import RequestQueue

from . import adapters, classification, inventory

PROMPTS = Path(__file__).parent / "prompts"
SAMPLE_CHARACTERS = 6000


def module_file(name):
    """'csv.produtos' -> 'a_csv_produtos.py'."""
    return "a_" + re.sub(r"[^a-z0-9]+", "_", name.lower()).strip("_") + ".py"


def _sample(path):
    if not path:
        return "(sem amostra: o formato está só descrito acima)"
    p = Path(path)
    if p.is_dir():
        files = sorted(x for x in p.rglob("*") if x.is_file())[:5]
        return "Pasta com os ficheiros: " + ", ".join(str(x.relative_to(p)) for x in files) + "\n\n" + (_sample(files[0]) if files else "")
    text = p.read_bytes()[:SAMPLE_CHARACTERS].decode("utf-8", errors="replace")
    return f"Ficheiro `{p.name}` (primeiros {SAMPLE_CHARACTERS} caracteres):\n\n```\n{text}\n```"


def adapter_prompt(name, description, sample_path=None):
    values = {"NOME": name, "DESCRICAO": description.strip() or "(sem descrição)", "AMOSTRA": _sample(sample_path),
              "INVENTARIO": "```python\n" + inspect.getsource(inventory) + "\n```",
              "CLASSIFICACAO": "\n".join(f"- {k}: {v[0]}, {v[1]}" for k, v in classification.CATEGORIES.items()),
              "EXEMPLO": inspect.getsource(adapters.text), "FICHEIRO": module_file(name)}
    template = (PROMPTS / "criar_adaptador.md").read_text(encoding="utf-8")
    for key, value in values.items():
        template = template.replace("{{" + key + "}}", value)
    return template


def request_adapter(name, description, sample_path=None):
    if not re.fullmatch(r"[a-z0-9_]+\.[a-z0-9_]+", name or ""):
        raise RequestError("o nome do adaptador é <formato>.<variante>, em minúsculas (por exemplo csv.produtos)")
    if name in adapters.ADAPTERS and name not in adapters.CREATED:
        raise RequestError(f"o adaptador {name} já existe")
    prompt = adapter_prompt(name, description, sample_path)
    return RequestQueue.global_queue().create("adaptador", f"Criar o adaptador {name}", prompt, adaptador=name,
                                              ficheiro=module_file(name), amostra=str(sample_path or ""))


def _strip_code_fences(text):
    t = text.strip()
    if t.startswith("```"):
        t = t.split("\n", 1)[1] if "\n" in t else ""
        if t.rstrip().endswith("```"):
            t = t.rstrip()[:-3]
    return t.strip() + "\n"


def register_adapter(request):
    """Check the response module and install it; the request is marked applied or rejected."""
    name = request.meta["adaptador"]
    code = _strip_code_fences(request.response_text() or "")
    target = adapters.FOLDER / request.meta["ficheiro"]
    previous = target.read_text(encoding="utf-8") if target.exists() else None
    try:
        compile(code, request.meta["ficheiro"], "exec")
        if not re.search(r"^NAME\s*=\s*['\"]" + re.escape(name) + r"['\"]", code, re.M) or "def adapt(" not in code:
            raise RequestError(f'o módulo tem de definir NAME = "{name}" e adapt(path)')
        target.write_text(code, encoding="utf-8")
        try:
            adapters.load(reload=True)
            if name not in adapters.ADAPTERS:
                raise RequestError(f"depois de carregar o módulo, o adaptador {name} continua sem registo")
            sample = request.meta.get("amostra")
            if sample and Path(sample).exists():
                adapters.ADAPTERS[name](sample)
        except Exception:
            if previous is None:
                target.unlink()
            else:
                target.write_text(previous, encoding="utf-8")
            adapters.load(reload=True)
            raise
    except SyntaxError as e:
        request.mark_rejected(f"o código não compila: {e}")
        raise RequestError(f"o código não compila: {e}") from e
    except Exception as e:  # noqa: BLE001 - any failure of the module rejects the request
        request.mark_rejected(str(e))
        raise RequestError(str(e)) from e
    result = {"resumo": f"adaptador {name} instalado em {request.meta['ficheiro']}" + (" e experimentado na amostra" if request.meta.get("amostra") else ""),
              "ficheiro": str(target)}
    request.mark_applied(result)
    return result
