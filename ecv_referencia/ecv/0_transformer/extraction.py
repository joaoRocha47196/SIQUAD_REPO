"""Phase 0 for a domain: run the adapter of each source and write one inventory per source.

The sources are listed in dominio.json (`fontes`): id, adapter, path relative to the data root (a glob)
and role. A source with `nomesDe` runs after the source it takes the English names from.
"""
import glob

from ecv import config
from ecv.shared.errors import DomainError
from ecv.shared.workspace import now

from .adapters import ADAPTERS, NAME_SOURCES


class Extractor:
    def __init__(self, domain):
        self.domain = domain
        self.inventories = {}

    def source_path(self, source):
        matches = sorted(glob.glob(str(config.data_root() / source["caminho"])))
        if not matches:
            raise DomainError(f"fonte {source['id']}: {source['caminho']} não existe em {config.data_root()}")
        return matches[0]

    def extract_source(self, source):
        adapter_name = source["adaptador"]
        if adapter_name not in ADAPTERS:
            raise DomainError(f"fonte {source['id']}: adaptador '{adapter_name}' desconhecido; disponíveis: {sorted(ADAPTERS)}")
        path = self.source_path(source)
        if "nomesDe" in source:
            hint = NAME_SOURCES[adapter_name](self.inventories[source["nomesDe"]])
            inventory = ADAPTERS[adapter_name](path, hint)
        else:
            inventory = ADAPTERS[adapter_name](path)
        inventory.source.update({"id": source["id"], "papel": source.get("papel"), "caminho": source["caminho"], "extraido": now()})
        inventory.save(self.domain.inventory_folder / f"{source['id']}.json")
        self.inventories[source["id"]] = inventory
        return f"{source['id']}: {inventory.summary()}"

    def run(self):
        """Extract every source; phase 0 becomes 'em revisão'. Returns one summary line per source."""
        sources = sorted(self.domain.sources(), key=lambda s: "nomesDe" in s)
        summary = [self.extract_source(s) for s in sources]
        self.domain.set_step_state("0", "em revisão", resumo=summary)
        return summary


def extract(domain):
    return Extractor(domain).run()
