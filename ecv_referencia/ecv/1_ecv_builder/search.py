"""Search in the graph, to confirm whether an entity already exists before creating it (no duplicates).

  search(g, text)              -> nodes whose name, key, description or alternative names contain the text
                                  (ignoring case and accents), by label;
  similar_models(g, props)     -> USM and SM whose properties (names and alternative names) overlap the given
                                  ones (Jaccard index), most similar first;
  existing_models(g)           -> every HLM, USM and SM with what the merge compares (for the step A prompt);
  existing_functions(g)        -> functions and external contexts (for the step E prompt).

Only the Graph interface is used: it works on the in-memory graph and on Neo4j.
"""
import re
import unicodedata

from ecv.graph.base import read_json

LABELS = ("HLM", "SM", "USM", "Propriedade", "Regra", "Funcao", "ContextoExterno", "Projecao", "Perfil", "Declaracao")


def normalise(t):
    t = unicodedata.normalize("NFKD", str(t or "")).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", " ", t).strip()


def _name_tokens(n):
    """'codigoPostal' -> 'codigo postal'; 'zip_code' -> 'zip code'."""
    n = re.sub(r"([a-z])([A-Z])", r"\1 \2", str(n or ""))
    return normalise(n)


def search(g, text, labels=LABELS, limit=200):
    q = normalise(text)
    if not q:
        return []
    out = []
    for label in labels:
        for n in g.nodes(label):
            fields = [n.get("nome"), n.get("chave"), n.get("id"), n.get("descricao"), " ".join(n.get("nomesAlternativos") or [])]
            haystack = " | ".join(normalise(c) + " " + _name_tokens(c) for c in fields if c)
            if q in haystack:
                out.append({"rotulo": n.label, "nome": n.name, "chave": n.get("chave") or n.get("id") or n.get("nome"),
                            "descricao": n.get("descricao"), "dono": n.get("dono"),
                            "exato": normalise(n.name) == q or _name_tokens(n.name) == q})
                if len(out) >= limit:
                    return out
    return sorted(out, key=lambda x: (not x["exato"], LABELS.index(x["rotulo"]) if x["rotulo"] in LABELS else 9, x["nome"] or ""))


def _signature(g, m):
    names = set()
    for e in g.outgoing(m, "CONTEM"):
        p = e.target
        names.add(_name_tokens(p["nome"]))
        names |= {_name_tokens(x) for x in (p.get("nomesAlternativos") or []) if len(str(x)) < 40}
    return names


def similar_models(g, properties, threshold=0.4, exclude=None):
    """USM and SM whose property names overlap the given ones; exclude = (level, name) of the model itself."""
    wanted = {_name_tokens(p) for p in properties}
    out = []
    for level in ("USM", "SM"):
        for m in g.nodes(level):
            if exclude and (level, m["nome"]) == tuple(exclude):
                continue
            names = {_name_tokens(e.target["nome"]) for e in g.outgoing(m, "CONTEM")}
            if not names:
                continue
            common = wanted & _signature(g, m)
            union = wanted | names
            j = len(common) / len(union) if union else 0
            if j >= threshold:
                out.append({"nivel": level, "nome": m["nome"], "semelhanca": round(j, 2), "comuns": sorted(common),
                            "propriedades": sorted(names), "descricao": m.get("descricao")})
    return sorted(out, key=lambda x: -x["semelhanca"])


def _property_summary(p):
    fields = (("nome", p["nome"]), ("tipo", p.get("tipo")), ("descricao", p.get("descricao")),
              ("nomesAlternativos", read_json(p.get("nomesAlternativos"), [])), ("notas", p.get("notas")))
    return {k: v for k, v in fields if v}


def _composition_line(e):
    role = f' papel {e.get("papel")}' if e.get("papel") != e.target["nome"] else ""
    return f'{e.target.label} {e.target["nome"]} [{e.get("cardinalidade")}]' + role


def existing_models(g):
    """The HLM, USM and SM of the graph, with everything the merge compares (a reused model must stay equal):
    description and notes of the model; name, type, description, alternative names and notes of each property;
    composition; the rules that live in it; who uses it."""
    out = []
    for level in ("HLM", "USM", "SM"):
        for m in sorted(g.nodes(level), key=lambda n: n["nome"]):
            props = sorted(g.outgoing(m, "CONTEM"), key=lambda e: e.get("ordem", 0))
            parts = sorted(g.outgoing(m, "COMPOSTO_POR"), key=lambda e: e.get("ordem", 0))
            item = {"nivel": level, "nome": m["nome"], "descricao": m.get("descricao")}
            if m.get("notas"):
                item["notas"] = m["notas"]
            if level != "HLM":
                item["propriedades"] = [_property_summary(e.target) for e in props]
            item["composicao"] = [_composition_line(e) for e in parts]
            rules = sorted({r["id"] for r in g.sources(m, "ASSOCIADA_A")} | {r["id"] for e in props for r in g.sources(e.target, "ASSOCIADA_A")})
            if rules:
                item["regrasQueVivemNele"] = rules
            if level != "HLM":
                item["usadoPor"] = sorted({x["nome"] for x in g.sources(m, "COMPOSTO_POR")})
            out.append(item)
    return out


def existing_functions(g):
    return {"funcoes": [{"nome": f["nome"], "descricao": f.get("descricao"), "parametros": read_json(f.get("parametros"), []),
                         "contextosExternos": sorted(c["nome"] for c in g.targets(f, "DEPENDE_DE"))}
                        for f in sorted(g.nodes("Funcao"), key=lambda x: x["nome"])],
            "contextosExternos": [{"nome": c["nome"], "tipo": c.get("tipo"), "descricao": c.get("descricao"), "fonte": c.get("fonte")}
                                  for c in sorted(g.nodes("ContextoExterno"), key=lambda x: x["nome"])]}
