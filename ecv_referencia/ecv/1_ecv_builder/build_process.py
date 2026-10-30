"""The build process of a domain's declarations (build_process.json):

    0      extraction (module 0): one inventory per source
    G      generation: the complete declarations in one request to the LLM (full specification + all the inventory)
    A–F    review layers (structure, projections, plausibility, inference, functions, profiles): each layer is reviewed
           and corrected through change requests (natural language, operations, CSV tables, information from other sources)

Each phase and layer has what it is, its principles and procedure, checks, views, review questions and preferred
operations; the cycle says what happens in each stage."""
import json
from functools import lru_cache

from ecv import config

# Rule categories of the inventory that each review layer covers (the category is a hint, not a decision).
STEP_CATEGORIES = {"B": ("presenca", "cardinalidade"), "C": ("formato", "valores", "gama"),
                   "D": ("condicional", "exclusao", "outra"), "E": ("calculo", "cruzada")}
GENERATION = "G"


@lru_cache(maxsize=1)
def process_definition():
    return json.loads(config.path("processoConstrucao").read_text(encoding="utf-8"))


def step_ids():
    return [f["id"] for f in process_definition()["fases"]]


def step(step_id):
    found = next((f for f in process_definition()["fases"] if f["id"] == step_id), None)
    if found is None:
        raise KeyError(f"passo desconhecido: {step_id}; passos: {step_ids()}")
    return found


def layers():
    """The review layers A to F."""
    return [f for f in process_definition()["fases"] if f.get("tipo") == "revisao"]


def layer_ids():
    return [f["id"] for f in layers()]


def common_principles():
    return process_definition()["principiosComuns"]


def cycle():
    return process_definition()["ciclo"]


def prompt_template(name):
    """A prompt file of module 1 (comum.md or G_geracao.md)."""
    return (config.path("promptsPassos") / name).read_text(encoding="utf-8")
