"""Requests to implement a declared function (kind "funcao", global queue pedidos/).

    request_implementation(g, name)  -> LlmRequest: prompt with the declaration of the function, the rules that
                                        call it, the contract and an example module
    (the LLM answers with resposta.py: a module with @implements("<name>"))
    register_implementation(request) -> the module is checked (it compiles, registers the name) and written to
                                        ecv/6_validation/functions/<file>; the registry is reloaded

The declaration says what the function means; the implementation says how the engine evaluates it.
"""
import json
import re
from pathlib import Path

from ecv import config
from ecv.graph.base import read_json
from ecv.shared.errors import RequestError
from ecv.shared.llm_requests import RequestQueue

from . import functions

FUNCTIONS_FOLDER = Path(functions.__file__).parent


def module_file(name):
    """'naoPosteriorAHoje' -> 'f_nao_posterior_a_hoje.py' (one module per requested function)."""
    return "f_" + re.sub(r"(?<!^)([A-Z])", r"_\1", name).lower() + ".py"


def declared_functions(g):
    """Every declared function of the graph, with its implementation state."""
    out = []
    for f in sorted(g.nodes("Funcao"), key=lambda x: x["nome"]):
        callers = sorted({e.props.get("regra") for e in g.incoming(f, "CHAMA") if e.props.get("regra")})
        out.append({"nome": f["nome"], "descricao": f.get("descricao"), "parametros": read_json(f.get("parametros"), []),
                    "retorno": f.get("retorno"), "contextosExternos": sorted(c["nome"] for c in g.targets(f, "DEPENDE_DE")),
                    "implementada": f["nome"] in functions.REGISTRY, "modulo": functions.SOURCES.get(f["nome"]),
                    "regras": callers})
    return out


def _function_block(item):
    return "```json\n" + json.dumps({k: item[k] for k in ("nome", "descricao", "parametros", "retorno", "contextosExternos")},
                                    ensure_ascii=False, indent=1) + "\n```"


def implementation_prompt(g, name):
    item = next((x for x in declared_functions(g) if x["nome"] == name), None)
    if item is None:
        raise RequestError(f"a função {name} não está declarada no grafo")
    rules = []
    for rule_id in item["regras"]:
        rule = next((r for r in g.rules() if r.get("id") == rule_id), None)
        if rule is not None:
            rules.append(f"- {rule_id}: {rule.get('descricao') or ''}")
    template = (config.path("promptsValidacao") / "implementar_funcao.md").read_text(encoding="utf-8")
    values = {"FUNCAO": _function_block(item), "REGRAS": "\n".join(rules) or "(nenhuma regra a chama ainda)",
              "AUXILIARES": (FUNCTIONS_FOLDER / "support.py").read_text(encoding="utf-8"),
              "EXEMPLO": (FUNCTIONS_FOLDER / "dates.py").read_text(encoding="utf-8"), "FICHEIRO": module_file(name)}
    for key, value in values.items():
        template = template.replace("{{" + key + "}}", value)
    return template


def request_implementation(g, name):
    prompt = implementation_prompt(g, name)
    return RequestQueue.global_queue().create("funcao", f"Implementar a função {name}", prompt, funcao=name, ficheiro=module_file(name))


def _strip_code_fences(text):
    t = text.strip()
    if t.startswith("```"):
        t = t.split("\n", 1)[1] if "\n" in t else ""
        if t.rstrip().endswith("```"):
            t = t.rstrip()[:-3]
    return t.strip() + "\n"


def register_implementation(request):
    """Check the response module and install it; the request is marked applied or rejected."""
    name = request.meta["funcao"]
    code = _strip_code_fences(request.response_text() or "")
    try:
        compile(code, request.meta["ficheiro"], "exec")
        if f'@implements("{name}")' not in code:
            raise RequestError(f'o módulo não regista a função com @implements("{name}")')
        target = FUNCTIONS_FOLDER / request.meta["ficheiro"]
        previous = target.read_text(encoding="utf-8") if target.exists() else None
        target.write_text(code, encoding="utf-8")
        try:
            functions.load(reload=True)
            if name not in functions.REGISTRY:
                raise RequestError(f"depois de carregar o módulo, a função {name} continua sem implementação")
        except Exception:
            if previous is None:
                target.unlink()
            else:
                target.write_text(previous, encoding="utf-8")
            functions.load(reload=True)
            raise
    except SyntaxError as e:
        request.mark_rejected(f"o código não compila: {e}")
        raise RequestError(f"o código não compila: {e}") from e
    except Exception as e:  # noqa: BLE001 - any failure of the module rejects the request
        request.mark_rejected(str(e))
        raise RequestError(str(e)) from e
    result = {"resumo": f"{name} implementada em {request.meta['ficheiro']}", "ficheiro": str(target)}
    request.mark_applied(result)
    return result
