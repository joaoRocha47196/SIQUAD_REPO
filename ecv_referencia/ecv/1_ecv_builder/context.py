"""The context of the prompts of module 1.

Generation (phase G) receives everything at once:
    inventory      groups, elements and rules of every source (complementary sources: only cardinalities and descriptions)
    domain data    the uses, scenarios, known mappings and metadata of dominio.json
    existing       the models and functions of the reference declarations (to reuse)
    declarations   the current declarations and mapping (when the generation is repeated)
    notes          the review notes of the domain

A review layer (steps A to F) gives a change request its slice of the inventory: the items of the layer's
categories that the mapping does not mention yet.
"""
import json

from ecv.amendments import DeclarationSet

from . import search
from .build_process import STEP_CATEGORIES
from .reference import reference_graph

GROUP_FIELDS = ("id", "nome", "nomeOrigem", "descricao", "pai", "cardinalidade", "elementos")
ELEMENT_FIELDS = ("id", "nome", "descricao", "tipo", "tipoOrigem", "cardinalidade", "grupo", "nomesAlternativos", "valoresAdmitidos")
COMPLEMENTARY_GROUP_FIELDS = ("id", "nome", "cardinalidade", "pai")
COMPLEMENTARY_ELEMENT_FIELDS = ("id", "descricao", "cardinalidade")
RULE_FIELDS = ("id", "texto", "categoria", "natureza", "gravidade", "contexto", "elementos", "expressao")


def json_block(x):
    return "```json\n" + json.dumps(x, ensure_ascii=False, indent=1) + "\n```"


def lines_block(records):
    """Compact JSON: one record per line (the prompt stays readable and much smaller)."""
    return "```json\n[\n" + ",\n".join(json.dumps(r, ensure_ascii=False, separators=(",", ":")) for r in records) + "\n]\n```"


REUSE_NOTE = ("Um modelo reutiliza-se com o MESMO nome e fica IGUAL ao que está aqui: a mesma descrição e as mesmas propriedades "
              "(nome, tipo, descrição, nomes alternativos, notas) e composições, porque a fusão compara tudo isto e rejeita diferenças. "
              "Reutilizar traz também as regras que já vivem nele (regrasQueVivemNele): o código junta-as à declaração, não as repitas, "
              "mas confirma que valem para este domínio. Se o modelo ou as suas regras não servem tal e qual, cria-se outro, com outro nome, "
              "e regista-se a razão numa nota. Os nomes dos HLM existentes também estão ocupados. As funções reutilizam-se pelo nome, "
              "com os mesmos parâmetros.")


def _element_record(element, complementary):
    fields = COMPLEMENTARY_ELEMENT_FIELDS if complementary else ELEMENT_FIELDS
    record = {k: element[k] for k in fields if element.get(k)}
    if record.get("nome") == record.get("descricao") or (record.get("descricao") or "").startswith(record.get("nome", "#")):
        record.pop("nome", None)
    if not complementary and element.get("notas") and len(element["notas"]) < 90:
        record["notas"] = element["notas"]
    return record


def rule_record(rule):
    return {k: rule[k] for k in RULE_FIELDS if rule.get(k)}


class GenerationContext:
    def __init__(self, domain):
        self.domain = domain
        self.inventories = domain.inventories()
        self.ds = DeclarationSet.load(domain.folder) if domain.declaration_files() else None

    def inventory(self):
        out = []
        for source_id, inv in self.inventories.items():
            complementary = self.domain.source_role(source_id) == "complementar"
            out.append(f"### Fonte {source_id}: {inv['fonte'].get('nome')} ({inv['fonte'].get('tipo')})"
                       + (" — complementar: só para confirmar cardinalidades e descrições" if complementary else "")
                       + f"\n\nPapel: {inv['fonte'].get('papel')}")
            if inv["fonte"].get("texto"):
                out.append("Texto da fonte, tal como está escrito:\n\n" + inv["fonte"]["texto"].strip())
            if inv["grupos"]:
                fields = COMPLEMENTARY_GROUP_FIELDS if complementary else GROUP_FIELDS
                out.append(f"Grupos ({len(inv['grupos'])}):\n" + lines_block([{k: g[k] for k in fields if g.get(k)} for g in inv["grupos"]]))
            if inv["elementos"]:
                out.append(f"Elementos ({len(inv['elementos'])}):\n" + lines_block([_element_record(x, complementary) for x in inv["elementos"]]))
            if inv["regras"]:
                out.append(f"Regras ({len(inv['regras'])}):\n" + lines_block([rule_record(r) for r in inv["regras"]]))
        return "\n\n".join(out)

    def domain_data(self):
        d = self.domain.definition
        return json_block({k: d.get(k) for k in ("utilizacoes", "cenarios", "mapeamentos", "metainformacao") if d.get(k)})

    def existing(self):
        g = reference_graph(exclude=self.domain.id)
        return (REUSE_NOTE + "\n\n### Modelos\n" + lines_block(search.existing_models(g))
                + "\n\n### Funções e contextos externos\n" + json_block(search.existing_functions(g)))

    def notes(self):
        return self.domain.notes() or "(nenhuma)"

    def declarations(self):
        if self.ds is None:
            return "(ainda não há declarações)"
        return json_block(list(self.ds.declarations.values())) + "\n\nMapeamento atual:\n" + json_block(self.ds.mapping)


def layer_inventory(domain, step):
    """The items of a review layer's categories that the mapping does not mention yet (for a change request)."""
    ds = DeclarationSet.load(domain.folder)
    mapped = {(x["fonte"], x["origem"]) for x in ds.mapping}
    records = []
    for source_id, inv in domain.inventories().items():
        if step == "A":
            records += [{"fonte": source_id, **_element_record(x, False)} for x in inv["elementos"] if (source_id, x["id"]) not in mapped]
        elif step in STEP_CATEGORIES:
            records += [{"fonte": source_id, **rule_record(r)} for r in inv["regras"]
                        if r["categoria"] in STEP_CATEGORIES[step] and (source_id, r["id"]) not in mapped]
    return records
