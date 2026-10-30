"""Materialisation: ECV declaration -> graph (the nodes and edges of graph_model.json).

Walks a verified declaration and creates one node per entity and one edge per relation. The result
is a MemoryGraph with this declaration only; the merge (merge.py) then adds it to the existing
graph without duplicates.

Order: declaration -> external contexts -> functions -> models and properties -> rules
(restriction, condition, calls) -> projections -> profiles.
"""
import json

from ecv.graph.memory import MemoryGraph

from . import paths as P
from . import rule_parts as R
from .descriptions import format_call, format_check, format_term
from .verification import verify


class MaterializationError(Exception):
    def __init__(self, report):
        self.report = report
        super().__init__("a declaração tem erros e não pode ser materializada: " + report.summary())


def _json(v):
    return json.dumps(v, ensure_ascii=False)


def _range_bounds(op, v):
    if op == "RANGE" and isinstance(v, list) and len(v) == 2 and all(isinstance(x, (int, float)) for x in v):
        return {"minimo": v[0], "maximo": v[1]}
    return {}


class Materializer:
    def __init__(self, decl):
        self.decl = decl
        self.graph = MemoryGraph()

    # ------------------------------------------------------------------ node lookups
    def model_node(self, level, name):
        return self.graph.node(level, name)

    def property_node(self, level, owner, name):
        return self.graph.node("Propriedade", P.property_key(level, owner, name))

    def target_node(self, res):
        """Node reached by a resolved path: the property, or the last model."""
        if res.prop is not None:
            return self.property_node(res.owner[0], res.owner[1], res.prop["nome"])
        return self.model_node(*res.target)

    def resolve(self, site, path):
        return P.resolve(self.decl, site.level, site.model, path)

    # ------------------------------------------------------------------ run
    def run(self):
        self.add_declaration()
        self.add_contexts()
        self.add_functions()
        self.add_models()
        self.add_rules()
        self.add_projections()
        self.add_profiles()
        return self.graph

    def add_declaration(self):
        header = self.decl.data.get("declaracao", {})
        hlm = header.get("hlm") or next(iter(self.decl.hlm), None)
        props = {"nome": header.get("nome") or self.decl.origin or "declaração", "versao": header.get("versao"),
                 "descricao": header.get("descricao"), "dominios": header.get("dominios"), "hlm": hlm}
        self.declaration_node = self.graph.add_node("Declaracao", props["nome"], {k: v for k, v in props.items() if v is not None})

    def add_contexts(self):
        for c in self.decl.contexts.values():
            self.graph.add_node("ContextoExterno", c["nome"],
                                {k: c.get(k) for k in ("nome", "tipo", "descricao", "fonte") if c.get(k) is not None})

    def add_functions(self):
        for f in self.decl.functions.values():
            node = self.graph.add_node("Funcao", f["nome"], {
                "nome": f["nome"], "descricao": f.get("descricao"),
                "parametros": _json(f.get("parametros", [])), "retorno": f.get("retorno"),
                **({"notas": f["notas"]} if f.get("notas") else {})})
            for c in f.get("contextosExternos", []):
                self.graph.add_edge("DEPENDE_DE", node, self.graph.node("ContextoExterno", c))

    def add_models(self):
        for level, name, m in self.decl.all_models():
            props = {"nome": name, "descricao": m.get("descricao")}
            if m.get("notas"):
                props["notas"] = m["notas"]
            self.graph.add_node(level, name, props)
        for h in self.decl.hlm:
            self.graph.add_edge("DESCREVE", self.declaration_node, self.model_node("HLM", h))
        for level, name, m in self.decl.all_models():
            node = self.model_node(level, name)
            for i, p in enumerate(m.get("propriedades", [])):
                self._add_property(node, level, name, i, p)
            for i, (role, child_level, child, card) in enumerate(self.decl.compositions(level, name)):
                self.graph.add_edge("COMPOSTO_POR", node, self.model_node(child_level, child),
                                    {"cardinalidade": card, "papel": role, "ordem": i})

    def _add_property(self, model_node, level, owner, order, p):
        props = {"chave": P.property_key(level, owner, p["nome"]), "nome": p["nome"], "dono": owner,
                 "nivelDono": level, "tipo": p.get("tipo"), "descricao": p.get("descricao"),
                 "nomesAlternativos": p.get("nomesAlternativos", [])}
        if p.get("notas"):
            props["notas"] = p["notas"]
        node = self.graph.add_node("Propriedade", props["chave"], props)
        self.graph.add_edge("CONTEM", model_node, node, {"ordem": order})

    # ------------------------------------------------------------------ rules
    def add_rules(self):
        for site in self.decl.rules():
            self.add_rule(site)

    def add_rule(self, site):
        rule, rule_type = site.rule, site.type
        props = {"id": rule["id"], "natureza": rule["natureza"], "tipo": rule_type, "descricao": rule.get("descricao"),
                 "alcance": site.scope}
        contexts = R.contexts_used(self.decl, rule)
        if contexts:
            props["contextosExternos"] = contexts
        if rule.get("notas"):
            props["notas"] = rule["notas"]
        if rule_type == "RIC":
            conclusion = rule.get("conclusao") or {}
            props.update({"mensagem": rule.get("mensagem"), "conclusaoTipo": conclusion.get("tipo"),
                          "conclusaoValor": conclusion.get("valor")})
        node = self.graph.add_node(rule_type, rule["id"], props, extra_labels=("Regra",))
        home = (self.property_node(site.level, site.model, site.prop["nome"]) if site.prop is not None
                else self.model_node(site.level, site.model))
        self.graph.add_edge("ASSOCIADA_A", node, home)
        if R.restriction(rule) is not None:
            self.add_restriction(site, node, R.restriction(rule))
        if R.condition(rule):
            self.add_condition(site, node, R.condition(rule))

    def add_call(self, site, source, part, op, call_spec, term=None):
        function = self.graph.node("Funcao", call_spec["funcao"])
        self.graph.add_edge("CHAMA", source, function, {
            "chamada": format_call(call_spec), "argumentos": _json(call_spec.get("argumentos", [])),
            "operador": op, "termo": term, "regra": site.id})
        for position, path in R.path_arguments(call_spec):
            res = self.resolve(site, path)
            self.graph.add_edge("LE", function, self.target_node(res), {
                "caminho": path, "regra": site.id, "posicao": position, "parte": part, "colecao": res.repeatable})

    def add_restriction(self, site, rule_node, restriction):
        op = restriction["operador"]
        props = {"id": f"{site.id}#restricao", "regra": site.id, "operador": op, "mensagem": restriction.get("mensagem")}
        if R.is_function(restriction):
            props.update({"forma": "funcao", "descricao": format_call(restriction["chamada"])})
        else:
            props.update({"forma": "tipificada", "valor": _json(restriction.get("valor")),
                          "descricao": format_check(restriction["propriedade"], op, restriction.get("valor"))})
        node = self.graph.add_node("Restricao", props["id"], props)
        self.graph.add_edge("RESTRITA_POR", rule_node, node)
        if R.is_function(restriction):
            self.add_call(site, node, "restricao", op, restriction["chamada"])
            return
        res = self.resolve(site, restriction["propriedade"])
        self.graph.add_edge("RESTRINGE", node, self.target_node(res), {
            "operador": op, "valor": _json(restriction.get("valor")), "caminho": restriction["propriedade"],
            "texto": format_check(res.prop["nome"], op, restriction.get("valor")),
            **_range_bounds(op, restriction.get("valor"))})

    def add_condition(self, site, rule_node, terms):
        node = self.graph.add_node("CondicaoAplicabilidade", f"{site.id}#condicao", {
            "id": f"{site.id}#condicao", "regra": site.id, "termos": len(terms),
            "descricao": " e ".join(format_term(t) for t in terms)})
        self.graph.add_edge("CONDICIONADA_POR", rule_node, node)
        for k, term in enumerate(terms):
            if R.is_function(term):
                self.add_call(site, node, "termo", term["operador"], term["chamada"], term=k)
                continue
            res = self.resolve(site, term["propriedade"])
            props = {"ordem": k, "operador": term["operador"], "caminho": term["propriedade"],
                     "texto": format_check(res.prop["nome"], term["operador"], term.get("valor"), term.get("contexto"))}
            if "contexto" in term:
                props["contexto"] = term["contexto"]
                self.graph.add_edge("DEPENDE_DE", node, self.graph.node("ContextoExterno", term["contexto"]), {"termo": k})
            else:
                props["valor"] = _json(term.get("valor"))
                props.update(_range_bounds(term["operador"], term.get("valor")))
            self.graph.add_edge("TERMO", node, self.target_node(res), props)

    # ------------------------------------------------------------------ projections and profiles
    def add_projections(self):
        for proj in self.decl.projections.values():
            props = {"nome": proj["nome"], "descricao": proj.get("descricao")}
            if proj.get("notas"):
                props["notas"] = proj["notas"]
            node = self.graph.add_node("Projecao", proj["nome"], props)
            self.graph.add_edge("PROJETA", node, self.model_node("HLM", proj["hlm"]))
            for key, edge_type in (("obrigatorias", "OBRIGATORIA"), ("permitidas", "PERMITIDA")):
                seen = set()
                for pattern in proj.get(key, []):
                    for path in P.expand(self.decl, proj["hlm"], pattern):
                        if path in seen:
                            continue
                        seen.add(path)
                        res = P.resolve(self.decl, "HLM", proj["hlm"], path)
                        self.graph.add_edge(edge_type, node, self.target_node(res), {"caminho": path})

    def add_profiles(self):
        for profile in self.decl.profiles.values():
            props = {"nome": profile["nome"], "descricao": profile.get("descricao")}
            if profile.get("notas"):
                props["notas"] = profile["notas"]
            node = self.graph.add_node("Perfil", profile["nome"], props)
            self.graph.add_edge("USA", node, self.graph.node("Projecao", profile["projecao"]))
            hlm = self.decl.projections[profile["projecao"]]["hlm"]
            for fx in profile.get("fixa", []):
                if "contexto" in fx:
                    self.graph.add_edge("FIXA", node, self.graph.node("ContextoExterno", fx["contexto"]),
                                        {"valor": _json(fx["valor"])})
                else:
                    res = P.resolve(self.decl, "HLM", hlm, fx["propriedade"])
                    self.graph.add_edge("FIXA", node, self.target_node(res),
                                        {"caminho": fx["propriedade"], "valor": _json(fx["valor"])})


def materialize(decl, verify_first=True):
    """Verify the declaration and materialise it. Raises MaterializationError when it has errors."""
    if verify_first:
        report = verify(decl)
        if not report.valid:
            raise MaterializationError(report)
    return Materializer(decl).run()
