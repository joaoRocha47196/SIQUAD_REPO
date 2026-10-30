"""The prompts of module 1.

Generation (phase G): comum.md + G_geracao.md, with
    {{DOMINIO}} {{PRINCIPIOS_COMUNS}}        the domain and the common principles (build process)
    {{OBJETIVO}} {{PERGUNTA}}                the phase (build process)
    {{CAMADAS}}                              for each layer A to F: what it is, its principles and its procedure (build process)
    {{ESPECIFICACOES}}                       the internal specification, in full (specs_bundle)
    {{EXISTENTES}} {{DADOS_DOMINIO}} {{DECLARACOES}} {{NOTAS}} {{DADOS}}   context.GenerationContext
    {{FORMATO}}                              the response format and an example (build process)

A change request of a layer: module 2's focused prompt (alteracao_focada.md): the request, the information from another
source, the context the person chose (models, properties, rules, projections...), an index of names and the layer's
operations with an example of each. Neither the full specification nor the full declarations.
"""
from . import specs_bundle
from .context import GenerationContext, json_block, layer_inventory
from .build_process import GENERATION, common_principles, layers, prompt_template, step




def bullet_list(items):
    return "\n".join(f"- {x}" for x in items)


def numbered_list(items):
    return "\n".join(f"{i}. {x}" for i, x in enumerate(items, start=1))


def fill(template, values):
    for key, value in values.items():
        template = template.replace("{{" + key + "}}", value)
    return template


def layers_text():
    out = []
    for layer in layers():
        out.append(f"### {layer['id']} · {layer['nome']}\n\n{layer['camada']}\n\nPrincípios:\n{bullet_list(layer['principios'])}\n\n"
                   f"Procedimento:\n{numbered_list(layer['comoProceder'])}")
    return "\n\n".join(out)


def generation_prompt(domain):
    definition = step(GENERATION)
    context = GenerationContext(domain)
    response = definition["formatoResposta"]
    values = {
        "DOMINIO": f"{domain.definition['nome']}: {domain.definition['descricao']}",
        "PRINCIPIOS_COMUNS": bullet_list(common_principles()),
        "OBJETIVO": definition["objetivo"],
        "PERGUNTA": definition["pergunta"],
        "CAMADAS": layers_text(),
        "ESPECIFICACOES": specs_bundle.text(),
        "EXISTENTES": context.existing(),
        "DADOS_DOMINIO": context.domain_data(),
        "DECLARACOES": context.declarations(),
        "NOTAS": context.notes(),
        "DADOS": context.inventory(),
        "FORMATO": response["descricao"] + "\n\n" + json_block(response["exemplo"]),
    }
    return fill(prompt_template("comum.md") + "\n" + prompt_template(definition["prompt"]), values)


def review_guidance(step_id):
    """The guidance of a review layer for a change request: what the layer is, its principles and procedure."""
    layer = step(step_id)
    return (f"Camada em revisão: {layer['id']} · {layer['nome']}. {layer['camada']}\n\nPrincípios da camada:\n{bullet_list(layer['principios'])}\n\n"
            f"Procedimento da camada:\n{numbered_list(layer['comoProceder'])}")


def layer_change_prompt(domain, request_text, step_id, extra_information="", selection=None):
    """A focused change request: the request, the layer's operations, the chosen context and an index of names."""
    from ecv.amendments import DeclarationSet
    from ecv.amendments import guides
    from ecv.amendments.change_requests import focused_prompt
    layer = step(step_id)
    ds = DeclarationSet.load(domain.folder)
    context = guides.context_of(ds, selection or {})
    uncovered = layer_inventory(domain, step_id)
    if uncovered and not selection:
        context["itensDoInventarioSemMapeamento"] = uncovered[:60]
    guidance = f"{layer['camada']}\n\nPrincípios:\n{bullet_list(layer['principios'])}"
    return focused_prompt(request_text, f"{step_id} · {layer['nome']}", guidance, layer.get("alteracoes") or [], context,
                          guides.names_index(ds), extra_information)


def size_summary(text):
    """Characters, lines and an estimate of tokens (about 4 characters per token for this mixed text)."""
    return {"caracteres": len(text), "tokensEstimados": len(text) // 4, "linhas": text.count("\n") + 1}
