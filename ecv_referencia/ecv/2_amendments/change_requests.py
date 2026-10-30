"""Change requests in natural language: the prompt that asks the LLM to translate a request into operations.

    "Coloca a morada de entrega num USM próprio"   ->  prompt (alteracoes.md: request, vocabulary, declarations, mapping,
                                                       and, when given, the review guidance, the specification, the
                                                       uncovered inventory items and information from another source)
                                                    ->  LLM response {"operacoes": [...], "notas": [...]}
                                                    ->  operations applied by the engine (deterministic)
"""
import json

from ecv import config

from .declaration_set import DeclarationSet
from .operations import describe


def _json_block(x):
    return "```json\n" + json.dumps(x, ensure_ascii=False, indent=1) + "\n```"


def change_prompt(domain, request_text, step_label, guidance="", preferred_operations=None, specification="", inventory="",
                  extra_information=""):
    """The full prompt of a change request for the domain."""
    ds = DeclarationSet.load(domain.folder)
    template = (config.path("promptsAlteracoes") / "alteracoes.md").read_text(encoding="utf-8")
    preferred = (f"Operações mais usadas nesta camada: {', '.join(preferred_operations)}. Qualquer operação do vocabulário pode ser usada."
                 if preferred_operations else "")
    values = {"PASSO": step_label, "ORIENTACAO": guidance or "(sem orientação de camada)", "OPERACOES": describe(),
              "OPERACOES_CAMADA": preferred, "ESPECIFICACOES": specification or "(não incluída)",
              "DECLARACOES": _json_block(list(ds.declarations.values())), "MAPEAMENTO": _json_block(ds.mapping),
              "INVENTARIO": inventory or "(não incluído)", "INFORMACAO": extra_information.strip() or "(nenhuma)",
              "PEDIDO": request_text}
    for key, value in values.items():
        template = template.replace("{{" + key + "}}", value)
    return template


def focused_prompt(request_text, layer_label, guidance, operation_names, context, index, extra_information=""):
    """The prompt of a change request with only the chosen context (the entities the request is about), an index of
    names, and the operations of the layer with an example of each: no full specification, no full declarations."""
    from ecv.config import OPERATORS
    from .guides import prefill
    from .operations import vocabulary
    ops = vocabulary()["operacoes"]
    names = [n for n in operation_names if n in ops] or list(ops)
    template = (config.path("promptsAlteracoes") / "alteracao_focada.md").read_text(encoding="utf-8")
    examples = "\n".join("```json\n" + json.dumps(prefill(None, n, {}), ensure_ascii=False) + "\n```" for n in names
                         if n not in ("remover_composicao", "alterar_composicao", "substituir_regra", "mover_regra"))
    values = {"CAMADA": layer_label, "ORIENTACAO": guidance or "", "PEDIDO": request_text,
              "INFORMACAO": extra_information.strip() or "(nenhuma)", "CONTEXTO": _json_block(context) if context else "(nenhum)",
              "INDICE": index, "OPERACOES": describe(names), "EXEMPLOS": examples, "OPERADORES": ", ".join(OPERATORS)}
    for key, value in values.items():
        template = template.replace("{{" + key + "}}", value)
    return template
