"""The cycle of a domain, as the web application and the CLI call it.

    prepare_generation(domain)                    -> LlmRequest "passo" G (prompt.md: full specification + all the inventory)
    (the LLM answers: resposta.json in the request folder, by commit or pasted in the web app)
    register_generation_response(domain, request) -> the declarations and the mapping created from the response; checks; G "em revisão"
    accept_step(domain, "G")                       -> the review layers may start
    request_changes(domain, text, layer, extra)    -> LlmRequest "alteracao": natural language (and information from another source) -> operations
    register_change_response(domain, request)
    apply_operations_to_domain(domain, ops, layer) -> operations given directly (web form, CSV, file)
    accept_step(domain, layer)                     -> the layer's checks pass: the next layer may be accepted

Nothing here talks to an LLM: a request is a folder (shared/llm_requests.py), answered outside.
"""
import copy

from ecv.amendments import DeclarationSet, apply_operations, parse_operations
from ecv.shared.errors import AmendmentError, RequestError, StepError
from ecv.shared.llm_requests import RequestQueue

from .build_process import GENERATION, layer_ids, step
from .checks import check_step
from .package import generation_prompt, layer_change_prompt, size_summary
from .reference import complete_reused_models


def _queue(domain):
    return RequestQueue.for_domain(domain)


def _require_open(domain, step_id):
    if domain.step_state(step_id) == "aceite":
        raise StepError(f"{_label(step_id)} já foi aceite; para mudar as declarações, faça um pedido de alterações")


def _label(step_id):
    return {"0": "a fase 0", GENERATION: "a geração (fase G)"}.get(step_id, f"o passo {step_id}")


def _require_declarations(domain):
    if not domain.declaration_files():
        raise StepError("ainda não há declarações: a geração (fase G) cria-as")


# ---------------------------------------------------------------------- generation
def prepare_generation(domain):
    """Write the generation prompt (everything at once) as a new request to the LLM."""
    domain.require_previous_accepted(GENERATION)
    text = generation_prompt(domain)
    request = _queue(domain).create("passo", f"Fase G: {step(GENERATION)['nome']}", text, step=GENERATION,
                                    dominio=domain.id, tamanho=size_summary(text))
    domain.add_request_to_step(GENERATION, request.id)
    domain.set_step_state(GENERATION, "em curso")
    return request


def _response_declarations(response):
    """The declarations of a response: {"declaracoes": [...]}, a bare list, or a single declaration."""
    if isinstance(response, list):
        return response
    if "declaracoes" in response:
        return response["declaracoes"]
    return [response] if response.get("hlm") else []


def _one_per_hlm(d):
    """A declaration with several HLM becomes one declaration per HLM (with its projections and profiles; the
    shared sections are repeated, as a declaration is complete)."""
    hlms = d.get("hlm") or []
    if len(hlms) <= 1:
        return [d]
    out = []
    for h in hlms:
        projections = [x for x in d.get("projecoes", []) if x.get("hlm") == h["nome"]]
        names = {x["nome"] for x in projections}
        part = {**copy.deepcopy(d), "hlm": [copy.deepcopy(h)], "projecoes": copy.deepcopy(projections),
                "perfis": [copy.deepcopy(x) for x in d.get("perfis", []) if x.get("projecao") in names]}
        part["declaracao"] = {**(d.get("declaracao") or {}), "hlm": h["nome"],
                              "nome": f'{(d.get("declaracao") or {}).get("nome", "Declaração")} — {h["nome"]}'}
        out.append(part)
    return out


def _declarations_from_response(domain, response):
    ds = DeclarationSet.empty(domain.folder)
    for d in (x for given in _response_declarations(response) for x in _one_per_hlm(given)):
        d.setdefault("$schema", ds.schema_reference())
        d.setdefault("declaracao", {})
        hlm = d["declaracao"].get("hlm") or d["hlm"][0]["nome"]
        d["declaracao"]["hlm"] = hlm
        ds.declarations[hlm] = d
    if not ds.declarations:
        raise AmendmentError("a resposta da geração não tem declarações (campo 'declaracoes')")
    mapping = response.get("mapeamento", []) if isinstance(response, dict) else []
    ds.mapping = [{**x, "passo": GENERATION} for x in mapping]
    ds.refresh()
    completed = complete_reused_models(domain, ds)
    done = [f"{len(ds.declarations)} declaração(ões): {', '.join(ds.declarations)}", f"{len(ds.mapping)} entradas de mapeamento"]
    if completed:
        done.append(f"modelos reutilizados completados com as regras das declarações de referência ({len(completed)}): " + ", ".join(completed))
    return ds, done


def register_generation_response(domain, request):
    """Create the declarations from the generation response, replacing the previous ones (a generation can be
    registered again at any time); nothing is written if it fails (the request is rejected)."""
    try:
        ds, done = _declarations_from_response(domain, request.response_json())
    except (AmendmentError, RequestError, KeyError) as e:
        request.mark_rejected(str(e))
        raise
    ds.save()
    response = request.response_json()
    notes = (response.get("notas") or []) if isinstance(response, dict) else []
    if notes:
        done.append(f"{len(notes)} nota(s) para a revisão")
    check = check_step(domain, GENERATION)
    domain.set_step_state(GENERATION, "em revisão")
    request.mark_applied({"resumo": check.summary(), "feitas": done, "notas": notes, "verificacao": check.to_dict()})
    return done, check


# ---------------------------------------------------------------------- acceptance and checks
def accept_step(domain, step_id):
    if step_id == "0":
        domain.set_step_state("0", "aceite")
        return None
    domain.require_previous_accepted(step_id)
    if step_id != GENERATION:
        _require_declarations(domain)
    check = check_step(domain, step_id)
    if not check.valid:
        raise StepError(f"{_label(step_id)} não pode ser aceite: " + check.summary() + "\n" + check.text())
    domain.set_step_state(step_id, "aceite", verificacao=check.summary())
    return check


def verify_step(domain, step_id=None):
    return check_step(domain, step_id or domain.current_step())


def _reopen(domain, step_id):
    """A change to the declarations puts an accepted layer back in review."""
    if step_id in layer_ids() and domain.step_state(step_id) == "aceite":
        domain.set_step_state(step_id, "em revisão", nota="reaberto por alterações")
    elif step_id in layer_ids() and domain.step_state(step_id) == "por iniciar":
        domain.set_step_state(step_id, "em revisão")


# ---------------------------------------------------------------------- changes (review layers)
def _layer(domain, step_id):
    step_id = step_id or domain.current_step()
    if step_id not in layer_ids():
        step_id = layer_ids()[0]
    return step_id


def request_changes(domain, text, step_id=None, extra_information="", selection=None):
    """A change described in natural language (optionally with information from another source) becomes a request:
    the LLM answers with operations."""
    _require_declarations(domain)
    step_id = _layer(domain, step_id)
    prompt = layer_change_prompt(domain, text, step_id, extra_information, selection)
    request = _queue(domain).create("alteracao", text.strip().splitlines()[0][:80], prompt, step=step_id,
                                    dominio=domain.id, pedido=text, tamanho=size_summary(prompt),
                                    informacaoAdicional=bool(extra_information.strip()), contexto=selection or {})
    (request.folder / "pedido.md").write_text(text + (f"\n\n## Informação adicional\n\n{extra_information}" if extra_information.strip() else ""),
                                              encoding="utf-8")
    return request


def apply_operations_to_domain(domain, operations, step_id=None, save=True):
    """Apply operations (all or nothing); with save=False, only preview what they do."""
    _require_declarations(domain)
    step_id = _layer(domain, step_id)
    trial = DeclarationSet.load(domain.folder).copy()
    done = apply_operations(trial, operations, step_id)
    if not save:
        return done, None
    trial.save()
    _reopen(domain, step_id)
    return done, check_step(domain, step_id)


def register_change_response(domain, request):
    try:
        operations = parse_operations(request.response_json())
        done, check = apply_operations_to_domain(domain, operations, request.step)
    except (AmendmentError, RequestError) as e:
        request.mark_rejected(str(e))
        raise
    request.mark_applied({"resumo": check.summary(), "feitas": done, "verificacao": check.to_dict()})
    return done, check


def register_response(domain, request):
    """Register a domain request, whatever its kind."""
    if request.kind == "passo":
        return register_generation_response(domain, request)
    if request.kind == "alteracao":
        return register_change_response(domain, request)
    raise RequestError(f"um pedido do tipo {request.kind} não pertence a um domínio")
