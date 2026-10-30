"""Test instances of a HLM, in the scenario of a profile (or of the HLM alone).

    skeleton(g, profile, hlm)                 -> {descricao, perfil | hlm, contextos, instancia}: the instance with every
                                                 available path, a placeholder value per base type and the profile's fixed values
    instance_prompt(g, profile, hlm, text)    -> a short prompt: the structure (path, type, cardinality, mandatory / allowed /
                                                 fixed), the rules with their text, the contexts and the skeleton; nothing else
    request_instance(domain, g, ...)          -> LlmRequest "instancia" in the domain's queue
    register_instance(domain, request, g)     -> the instance is saved in dominios/<d>/instancias/<name>.json and validated
    save_instance(domain, name, example)      -> the same, for an instance written by hand

An instance file has the format of the validation examples, so it can be validated in Validação like them.
"""
import json
import re

from ecv import config
from ecv.shared.errors import RequestError
from ecv.shared.llm_requests import RequestQueue
from ecv.views.viewmodels import common as K

from .engine import validate
from .scenario import Scenario

PLACEHOLDERS = {"texto": "", "inteiro": 0, "decimal": 0.0, "data": "AAAA-MM-DD", "dataHora": "AAAA-MM-DDThh:mm:ssZ",
                "booleano": False}


def folder(domain):
    return domain.folder / "instancias"


def _scenario(g, profile=None, hlm=None):
    return Scenario(g, profile or None, None if profile else hlm)


def _status(scenario, path):
    if path in scenario.fixed:
        return "fixado no perfil"
    if scenario.projected is None:
        return "disponível (sem perfil)"
    if path in scenario.mandatory:
        return "obrigatório"
    return "permitido" if path in scenario.projected else "fora da projeção"


def _set(node, segments, value, repeatable):
    for i, segment in enumerate(segments[:-1]):
        prefix = ".".join(segments[:i + 1])
        child = node.get(segment)
        if child is None:
            child = [{}] if prefix in repeatable else {}
            node[segment] = child
        node = child[0] if isinstance(child, list) else child
    node[segments[-1]] = value


def skeleton(g, profile=None, hlm=None):
    scenario = _scenario(g, profile, hlm)
    repeatable = {p for p, r in scenario.models.items() if config.is_repeatable(r.get("cardinalidade"))}
    instance = {}
    for path, row in scenario.properties.items():
        if scenario.available(path):
            value = scenario.fixed.get(path, PLACEHOLDERS.get(row.get("tipoBase"), ""))
            _set(instance, path.split("."), value, repeatable)
    contexts = {r["nome"]: r["valor"] for r in scenario.context_rows()}
    head = {"perfil": profile} if profile else {"hlm": scenario.hlm}
    return {"descricao": "", **head, "contextos": contexts, "instancia": instance}


def _structure_lines(scenario):
    lines = []
    for row in scenario.tree[1:]:
        path = row["caminho"]
        if not scenario.available(path):
            continue
        if row["tipo"] == "Propriedade":
            fixed = f" = {json.dumps(scenario.fixed[path], ensure_ascii=False)}" if path in scenario.fixed else ""
            lines.append(f"- {path}: {row.get('tipoBase') or '?'}, {_status(scenario, path)}{fixed}"
                         + (f" — {row['descricao']}" if row.get("descricao") else ""))
        else:
            lines.append(f"- {path} ({row['tipo']} {row['nome']}, cardinalidade {row.get('cardinalidade') or '1..1'})")
    return "\n".join(lines)


def _rule_lines(g, scenario):
    out = []
    for rule, prefixes in K.rules_of_hlm(g, scenario.hlm):
        if scenario.projected is not None and not any(scenario.available(p) for p in prefixes if p):
            if all(p for p in prefixes):
                continue
        out.append(f"- {rule['id']} ({rule.label}): {rule.get('descricao') or ''} [em: {', '.join(sorted(set(p or '(raiz)' for p in prefixes)))}]")
    return "\n".join(out) or "(nenhuma)"


def instance_prompt(g, profile=None, hlm=None, text=""):
    scenario = _scenario(g, profile, hlm)
    template = (config.path("promptsValidacao") / "instancia_teste.md").read_text(encoding="utf-8")
    values = {"CENARIO": (f"perfil {profile} (projeção {scenario.projection}) do HLM {scenario.hlm}" if profile
                          else f"HLM {scenario.hlm}, sem perfil (todas as propriedades disponíveis, todas as regras)"),
              "PEDIDO": text.strip() or "Uma instância válida, com valores plausíveis.",
              "ESTRUTURA": _structure_lines(scenario), "REGRAS": _rule_lines(g, scenario),
              "CONTEXTOS": "\n".join(f"- {r['nome']}: {json.dumps(r['valor'], ensure_ascii=False)} ({r['origem']})" for r in scenario.context_rows()) or "(nenhum)",
              "ESQUELETO": json.dumps(skeleton(g, profile, hlm), ensure_ascii=False, indent=1)}
    for key, value in values.items():
        template = template.replace("{{" + key + "}}", value)
    return template


def instance_name(text):
    words = re.findall(r"[a-z0-9]+", (text or "instancia").lower().translate(str.maketrans("áàâãéêíóôõúç", "aaaaeeiooouc")))
    return "_".join(words[:6]) or "instancia"


def request_instance(domain, g, profile=None, hlm=None, text="", name=None):
    prompt = instance_prompt(g, profile, hlm, text)
    name = name or instance_name(text or (profile or hlm))
    return RequestQueue.for_domain(domain).create("instancia", f"Instância de teste {name}", prompt, dominio=domain.id,
                                                  perfil=profile or "", hlm=hlm or "", nome=name, pedido=text)


def save_instance(domain, name, example):
    if not isinstance(example, dict) or not isinstance(example.get("instancia"), dict):
        raise RequestError("a instância tem a forma {descricao, perfil | hlm, contextos, instancia}")
    target = folder(domain) / f"{instance_name(name)}.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(example, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    return target


def saved(domain):
    """{name: example} of the domain's test instances."""
    f = folder(domain)
    return {x.stem: json.loads(x.read_text(encoding="utf-8")) for x in sorted(f.glob("*.json"))} if f.exists() else {}


def validate_saved(g, example, name=None):
    return validate(g, example["instancia"], profile=example.get("perfil") or None, hlm=None if example.get("perfil") else example.get("hlm"),
                    contexts=example.get("contextos") or {}, name=name, description=example.get("descricao"))


def register_instance(domain, request, g=None):
    """Save the instance of the response (completed with the request's scenario) and validate it when a graph is given."""
    try:
        response = request.response_json()
        example = response if isinstance(response, dict) and "instancia" in response else {"instancia": response}
        if request.meta.get("perfil"):
            example.setdefault("perfil", request.meta["perfil"])
        elif request.meta.get("hlm"):
            example.setdefault("hlm", request.meta["hlm"])
        example.setdefault("descricao", request.meta.get("pedido") or "")
        target = save_instance(domain, request.meta.get("nome") or request.id, example)
    except Exception as e:  # noqa: BLE001 - any failure rejects the request
        request.mark_rejected(str(e))
        raise RequestError(str(e)) from e
    summary = f"instância gravada em {target.relative_to(domain.folder.parent.parent)}"
    if g is not None:
        vm = validate_saved(g, example, target.stem)
        summary += f"; {'válida' if vm['valida'] else 'inválida'} ({', '.join(f'{k}: {v}' for k, v in vm['resumo'].items())})"
    result = {"resumo": summary, "ficheiro": str(target)}
    request.mark_applied(result)
    return result
