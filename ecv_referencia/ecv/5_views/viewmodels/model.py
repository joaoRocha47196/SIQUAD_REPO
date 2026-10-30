"""ViewModel 'modelo': the view of a model (HLM, SM or USM), with or without its rules.

It is the base of three views:
  - HLM model view             (hlm_<HLM>):   tree + structure table, link to the projections;
  - model view with rules      (regras_<HLM>): the same table with the rules column and the groupings;
  - specific model view        (sm_<SM>, usm_<USM>): who uses it, tree to the leaves, table with rules.

Graph: (model)-COMPOSTO_POR*->(SM|USM)-CONTEM->(Propriedade); (Regra)-ASSOCIADA_A->(node);
Regra -RESTRITA_POR-> Restricao -RESTRINGE|CHAMA->; Regra -CONDICIONADA_POR-> Condicao -TERMO|CHAMA->;
upwards, COMPOSTO_POR backwards to the HLMs; Projecao -PROJETA-> HLM.
"""
from ecv import config
from ecv.graph.base import read_json

from . import common as K
from .decision import rules_for_target


def discriminating_keys(g):
    """Keys of the properties read by some term (by TERMO, or as argument of a function in a term)."""
    keys = set()
    for c in g.nodes("CondicaoAplicabilidade"):
        keys |= {e.target["chave"] for e in g.outgoing(c, "TERMO")}
    for f in g.nodes("Funcao"):
        keys |= {e.target["chave"] for e in g.outgoing(f, "LE") if e.get("parte") == "termo" and e.target.label == "Propriedade"}
    return keys


def _nested_tree(g, node, path, role, card, discriminating, with_users):
    props = [{**K.property_info(p), "caminho": K.join(path, p["nome"]),
              "nomesAlternativos": list(p.get("nomesAlternativos") or []), "discriminante": p["chave"] in discriminating}
             for p in K.properties(g, node)]
    children = []
    for edge, child in K.children(g, node):
        child_role = edge.get("papel") or child["nome"]
        children.append(_nested_tree(g, child, K.join(path, child_role), child_role, edge.get("cardinalidade"),
                                     discriminating, with_users))
    out = {"nivel": node.label, "nome": node["nome"], "papel": role, "cardinalidade": card, "caminho": path,
           "descricao": node.get("descricao"), "propriedades": props, "filhos": children}
    if with_users and node.label != "HLM":
        out["usadoPor"] = K.hlms_using(g, node)
    return out


def _rir_by_target(g, cards, minimum):
    groups = {}
    for card in cards:
        key = (card.get("alvo") or {}).get("chave") or "?"
        groups.setdefault(key, {"alvo": key, "nome": (card.get("alvo") or {}).get("nome"), "regras": []})["regras"].append(card)
    for group in groups.values():
        p = g.node("Propriedade", group["alvo"])
        group["decisao"] = bool(p is not None and len(rules_for_target(g, p)) >= minimum)
    return list(groups.values())


def _path_text(path):
    """'OrdemInstalacao › Cliente (papel Requerente) › Morada': each step by model name and, if different, the role."""
    parts = [path[0]["nome"]]
    for previous, step in zip(path, path[1:]):
        role = previous.get("papel")
        parts.append(step["nome"] if not role or role == step["nome"] else f'{step["nome"]} (papel {role})')
    return " › ".join(parts)


def _blocks(rows, level, name):
    """The model's own properties and each direct composition: what the view expands or collapses."""
    blocks, current = [], None
    for row in rows[1:]:
        if row["profundidade"] == 1 and row["tipo"] != "Propriedade":
            current = {"nome": row["nome"], "nivel": row["tipo"], "papel": row.get("papel"),
                       "cardinalidade": row.get("cardinalidade"), "linhas": []}
            blocks.append(current)
        elif current is None:
            current = {"nome": name, "nivel": level, "proprio": True, "linhas": []}
            blocks.append(current)
        current["linhas"].append(row)
    for b in blocks:
        b["resumoPropriedades"] = [r["nome"] for r in b["linhas"] if r["tipo"] == "Propriedade"]
    return blocks


def _functions_and_contexts(g, cards):
    used = {fn for c in cards for fn in c["funcoes"]}
    functions = [{"nome": f["nome"], "descricao": f.get("descricao"), "parametros": read_json(f.get("parametros"), []),
                  "contextos": sorted(c["nome"] for c in g.targets(f, "DEPENDE_DE")),
                  "regras": sorted(x["id"] for x in cards if f["nome"] in x["funcoes"])}
                 for f in sorted(g.nodes("Funcao"), key=lambda x: x["nome"]) if f["nome"] in used]
    used_contexts = {c for card in cards for c in card["contextosExternos"]}
    contexts = [{"nome": c["nome"], "tipo": c.get("tipo"), "descricao": c.get("descricao"), "fonte": c.get("fonte"),
                 "regras": sorted(x["id"] for x in cards if c["nome"] in x["contextosExternos"]),
                 "fixadoPor": sorted(({"perfil": e.source["nome"], "valor": read_json(e.get("valor"))}
                                      for e in g.incoming(c, "FIXA")), key=lambda x: x["perfil"])}
                for c in sorted(g.nodes("ContextoExterno"), key=lambda x: x["nome"]) if c["nome"] in used_contexts]
    return functions, contexts


def model(g, nivel, nome, regras=False):
    root = K.model_node(g, nivel, nome)
    discriminating = discriminating_keys(g)
    minimum = config.VIEWS["decisaoMinimoRIR"]
    specific = nivel != "HLM"

    rows, all_cards = [], {}
    for r in K.tree_from(g, root):
        row = K.without_node(r)
        node = r["no"]
        if r["tipo"] == "Propriedade":
            row.update({"chave": node["chave"], "dono": node.get("dono"), "discriminante": node["chave"] in discriminating})
        if regras:
            cards = [K.rule_card(g, rule) for rule in K.rules_on(g, node)]
            for card in cards:
                all_cards.setdefault(card["id"], card).setdefault("ocorrencias", []).append(r["caminho"] or nome)
            row["regras"] = [c for c in cards if c["tipo"] != "RIR"]
            row["rir"] = _rir_by_target(g, [c for c in cards if c["tipo"] == "RIR"], minimum)
        rows.append(row)

    vm = {"vista": "modelo", "titulo": f"{'Modelo com regras' if regras and not specific else 'Modelo'} {nivel} {nome}",
          "nivel": nivel, "nome": nome, "descricao": root.get("descricao"), "comRegras": regras, "especifico": specific,
          "arvore": _nested_tree(g, root, "", None, None, discriminating, specific),
          "raiz": rows[0], "blocos": _blocks(rows, nivel, nome)}
    if nivel == "HLM":
        vm["projecoes"] = [{"nome": p["nome"], "descricao": p.get("descricao"),
                            "perfis": sorted(x["nome"] for x in g.sources(p, "USA"))}
                           for p in sorted(g.sources(root, "PROJETA"), key=lambda p: p["nome"])]
    if specific:
        vm["usadoPor"] = {"hlm": K.hlms_using(g, root),
                          "caminhos": [{"passos": p, "texto": _path_text(p)} for p in K.paths_to_hlm(g, root) if len(p) > 1]}
    if regras:
        cards = sorted(all_cards.values(), key=lambda c: (K.RULE_TYPE_ORDER.get(c["tipo"], 9), c["id"]))
        vm["regras"] = cards
        vm["contagem"] = {t: sum(1 for c in cards if c["tipo"] == t) for t in K.RULE_TYPE_ORDER}
        vm["contagem"]["FN"] = sum(1 for c in cards if c["funcao"])
        vm["funcoes"], vm["contextos"] = _functions_and_contexts(g, cards)
    return vm
