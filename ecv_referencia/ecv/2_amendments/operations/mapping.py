"""The mapping of the sources: where each element and rule of an inventory went (or why it was discarded)."""
from . import operation

MAPPING_FIELDS = ("fonte", "origem", "decisao", "destino", "motivo", "nota")


@operation("mapear")
def map_entry(ds, op, step=None):
    entry = {k: op[k] for k in MAPPING_FIELDS if op.get(k) is not None}
    if step:
        entry["passo"] = step
    ds.mapping = [x for x in ds.mapping if (x["fonte"], x["origem"]) != (entry["fonte"], entry["origem"])] + [entry]
    return f"mapeado {entry['fonte']}:{entry['origem']} ({entry['decisao']})"
