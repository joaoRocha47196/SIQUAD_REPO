"""ViewModel 'regra': the full card of a rule and its subgraph (thesis, figures 'Ligações de cada tipo
de regra' and 'A regra RIR-TEMP-REFRIG-CELSIUS no grafo').

The subgraph has two parts, drawn separately:
  - the rule subgraph (horizontal): Regra -> Restricao / CondicaoAplicabilidade -> Propriedade, Funcao -> ContextoExterno;
  - the model subgraph (vertical): each property (or model) involved -> the model that holds it -> ... -> every HLM.
Nothing is left out: every link and all the text of each element.
"""
from ecv.graph.base import read_json

from . import common as K


def _function_info(g, name):
    f = g.node("Funcao", name)
    return {"nome": name, "descricao": f.get("descricao"), "parametros": read_json(f.get("parametros"), []),
            "retorno": f.get("retorno"),
            "contextos": [_context_info(g, c["nome"]) for c in sorted(g.targets(f, "DEPENDE_DE"), key=lambda c: c["nome"])]}


def _context_info(g, name):
    c = g.node("ContextoExterno", name)
    return {"nome": name, "tipo": c.get("tipo"), "descricao": c.get("descricao"), "fonte": c.get("fonte")}


def _node_info(n):
    if n.label == "Propriedade":
        return K.property_info(n)
    return {"rotulo": n.label, "nome": n.name, "descricao": n.get("descricao")}


class RuleSubgraph:
    """Collects the nodes and edges of the rule subgraph and the graph nodes involved (properties and models read)."""

    def __init__(self, g):
        self.g = g
        self.nodes, self.edges, self.involved = [], [], {}

    def add_node(self, key, label, text, detail=None):
        if not any(n["chave"] == key for n in self.nodes):
            self.nodes.append({"chave": key, "rotulo": label, "texto": text, "detalhe": detail})
        return key

    def add_edge(self, a, b, edge_type, text=None):
        self.edges.append({"de": a, "para": b, "tipo": edge_type, "texto": text})

    def involve(self, node):
        self.involved[K.node_key(node)] = node
        return node

    def add_call(self, source, call):
        fn = self.add_node(f"Funcao:{call['funcao']}", "Funcao", call["funcao"], call.get("descricaoFuncao"))
        self.add_edge(source, fn, "CHAMA", call["chamada"])
        for a in call["argumentos"]:
            target = (self.g.node("Propriedade", a["alvo"]) if a["rotuloAlvo"] == "Propriedade"
                      else self.g.node(a["rotuloAlvo"], a["alvo"]))
            self.involve(target)
            p = self.add_node(K.node_key(target), target.label, a["alvo"], target.get("descricao"))
            self.add_edge(fn, p, "LE", f"argumento: {a['caminho']}" + (" (coleção)" if a.get("colecao") else ""))
        for c in call["contextos"]:
            x = self.add_node(f"ContextoExterno:{c}", "ContextoExterno", c, self.g.node("ContextoExterno", c).get("descricao"))
            self.add_edge(fn, x, "DEPENDE_DE")


def _restriction(g, sub, rule_key, rule_node, card):
    r = card.get("restricao")
    if r is None:
        return None
    rule_id = card["id"]
    out = {**r, "descricao": K.restriction_of(g, rule_node).get("descricao")}
    node_key = sub.add_node(f"Restricao:{rule_id}", "Restricao", f"{rule_id}#restricao", r.get("texto"))
    sub.add_edge(rule_key, node_key, "RESTRITA_POR")
    if r.get("forma") == "funcao" and r.get("chamada"):
        out["funcao"] = _function_info(g, r["chamada"]["funcao"])
        sub.add_call(node_key, r["chamada"])
    elif r.get("propriedade"):
        p = sub.involve(g.node("Propriedade", r["propriedade"]))
        out["alvo"] = K.property_info(p)
        sub.add_node(K.node_key(p), "Propriedade", p["chave"], p.get("descricao"))
        sub.add_edge(node_key, K.node_key(p), "RESTRINGE", r.get("texto"))
    return out


def _condition(g, sub, rule_key, rule_node, card):
    if not card.get("condicao"):
        return None
    rule_id = card["id"]
    cond = K.condition_of(g, rule_node)
    out = {"descricao": cond.get("descricao"), "termos": []}
    node_key = sub.add_node(f"Condicao:{rule_id}", "CondicaoAplicabilidade", f"{rule_id}#condicao", cond.get("descricao"))
    sub.add_edge(rule_key, node_key, "CONDICIONADA_POR")
    for t in card["condicao"]:
        term = dict(t)
        if t["forma"] == "funcao":
            term["funcao"] = _function_info(g, t["chamada"]["funcao"])
            sub.add_call(node_key, t["chamada"])
        else:
            p = sub.involve(g.node("Propriedade", t["propriedade"]))
            term["alvo"] = K.property_info(p)
            sub.add_node(K.node_key(p), "Propriedade", p["chave"], p.get("descricao"))
            sub.add_edge(node_key, K.node_key(p), "TERMO", f"termo {t['ordem'] + 1}: {t['texto']}")
            if t.get("contexto"):
                term["contextoInfo"] = _context_info(g, t["contexto"])
                x = sub.add_node(f"ContextoExterno:{t['contexto']}", "ContextoExterno", t["contexto"],
                                 g.node("ContextoExterno", t["contexto"]).get("descricao"))
                sub.add_edge(node_key, x, "DEPENDE_DE", f"termo {t['ordem'] + 1}")
        out["termos"].append(term)
    return out


def rule(g, id):
    node = next((r for r in g.nodes("Regra") if r["id"] == id), None)
    if node is None:
        raise ValueError(f"regra '{id}' não existe")
    card = K.rule_card(g, node)
    sub = RuleSubgraph(g)
    rule_key = sub.add_node(f"R:{id}", card["tipo"], id, card.get("descricao"))
    home = sub.involve(g.first_target(node, "ASSOCIADA_A"))
    home_key = sub.add_node(K.node_key(home), home.label, home["chave"] if home.label == "Propriedade" else home.name,
                            home.get("descricao"))
    sub.add_edge(rule_key, home_key, "ASSOCIADA_A", "vive em (alcance)")
    restriction = _restriction(g, sub, rule_key, node, card)
    condition = _condition(g, sub, rule_key, node, card)
    model_nodes, model_edges = K.model_chain(g, list(sub.involved.values()))
    return {"vista": "regra", "titulo": f"Regra {id}", "regra": card, "restricao": restriction, "condicao": condition,
            "viveEm": {**_node_info(home), "chave": K.node_key(home), "rotulo": home.label,
                       "hlm": K.hlms_using(g, home if home.label != "Propriedade" else K.owner(g, home))},
            "subgrafoRegra": {"nos": sub.nodes, "arestas": sub.edges},
            "subgrafoModelos": {"nos": model_nodes, "arestas": model_edges}}
