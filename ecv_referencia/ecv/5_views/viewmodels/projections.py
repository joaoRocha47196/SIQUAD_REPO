"""ViewModel 'projecoes': the projection matrix of a HLM (the structural rules, RE) and the profiles that use them."""
from ecv.graph.base import read_json

from . import common as K


def _profiles(g, projections, marks):
    out = []
    for p in projections:
        for profile in sorted(g.sources(p, "USA"), key=lambda x: x["nome"]):
            fixed = []
            for e in g.outgoing(profile, "FIXA"):
                if e.target.label == "ContextoExterno":
                    fixed.append({"contexto": e.target["nome"], "valor": read_json(e.get("valor"))})
                else:
                    fixed.append({"caminho": e.get("caminho"), "valor": read_json(e.get("valor")),
                                  "projetada": marks.get((p["nome"], e.get("caminho")), "-") != "-"})
            fixed.sort(key=lambda x: ("contexto" in x, x.get("caminho") or x.get("contexto")))
            out.append({"perfil": profile["nome"], "projecao": p["nome"], "descricao": profile.get("descricao"), "fixa": fixed})
    return out


def projections(g, hlm):
    """Projection matrix: each property (path) per projection, mandatory/permitted/excluded.

    Graph: Projecao -PROJETA-> HLM; Projecao -OBRIGATORIA|PERMITIDA {caminho}-> Propriedade;
    Perfil -USA-> Projecao; Perfil -FIXA {caminho|valor}-> Propriedade|ContextoExterno.
    """
    root = K.hlm_node(g, hlm)
    projs = sorted(g.sources(root, "PROJETA"), key=lambda p: p["nome"])
    marks = {}
    for p in projs:
        for edge_type, mark in (("OBRIGATORIA", "O"), ("PERMITIDA", "P")):
            for e in g.outgoing(p, edge_type):
                marks[(p["nome"], e.get("caminho"))] = mark
    rows = []
    for path, _ in K.property_paths(g, hlm):
        cells = {p["nome"]: marks.get((p["nome"], path), "-") for p in projs}
        rows.append({"caminho": path, "celulas": cells, "difere": len(set(cells.values())) > 1})
    return {"vista": "projecoes", "titulo": f"Matriz de projeções do HLM {hlm}", "hlm": hlm,
            "projecoes": [{"nome": p["nome"], "descricao": p.get("descricao")} for p in projs],
            "linhas": rows, "perfis": _profiles(g, projs, marks)}
