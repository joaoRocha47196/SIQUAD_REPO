"""Evaluation of the rules (RP, RIR, RIC) of the HLM on an instance, in each concrete occurrence of the
node where each rule lives (the issuer's address and the client's; every invoice line).

States of a rule in one occurrence:
  não conforme      the condition holds (or it is an RP) and the restriction fails
  conforme          the condition holds (or it is an RP) and the restriction is met
  conclusão         an RIC whose condition holds
  não aplicável     the condition does not hold (or reads a value the instance does not carry)
  sem valor         the restriction targets a property the instance does not carry (mandatoriness is the projection's)
  não avaliável     an external context or a function implementation is missing, or a term is outside the projection
  fora da projeção  the restriction reads a property the projection does not include (nor the profile fixes),
                    or the node where the rule lives is entirely outside the projection
  ausente           the node where the rule lives is not in the instance (and the projection includes it)
"""
from ecv.graph.base import read_json
from ecv.views.viewmodels import common as K
from ecv.views.viewmodels.evaluation import evaluate

from .functions import call as call_function
from .instance import collect, first_value, join

STATES = ("não conforme", "conforme", "conclusão", "não aplicável", "sem valor", "não avaliável", "fora da projeção", "ausente")


class RuleEvaluator:
    def __init__(self, scenario, instance):
        self.scenario = scenario
        self.g = scenario.g
        self.instance = instance

    def run(self):
        rows = []
        for rule, prefixes in K.rules_of_hlm(self.g, self.scenario.hlm):
            home = self.g.first_target(rule, "ASSOCIADA_A")
            base = {"regra": rule["id"], "tipo": rule.label, "descricao": rule.get("descricao"),
                    "vive": f"{home.label} {home.get('chave') or home.name}" if home else None}
            for prefix in prefixes:
                rows += self._occurrences(rule, prefix, base)
        return rows

    def _occurrences(self, rule, prefix, base):
        nodes = [(c, n) for c, n in collect(self.instance, prefix.split(".")) if n is not None] if prefix else [("", self.instance)]
        if not nodes:
            outside = not self.scenario.available(prefix)
            return [{**base, "ocorrencia": prefix, "estado": "fora da projeção" if outside else "ausente",
                     "detalhe": f"a projeção {self.scenario.projection} não inclui {prefix}" if outside else f"{prefix} não está na instância"}]
        return [{**base, "ocorrencia": path or "(HLM)", **self.evaluate(rule, node, prefix)} for path, node in nodes]

    # ------------------------------------------------------------------ one occurrence
    def evaluate(self, rule, node, prefix):
        restriction = K.restriction_of(self.g, rule)
        outside = [p for p in self.scenario.restriction_paths(restriction, prefix) if not self.scenario.available(p)]
        if outside:
            return {"estado": "fora da projeção", "detalhe": f"a restrição lê {', '.join(outside)}, que a projeção não inclui"}
        condition, terms, reason = self.condition(rule, node, prefix)
        if condition == "não avaliável":
            return {"estado": "não avaliável", "termos": terms, "detalhe": reason}
        if condition in ("falsa", "sem valor"):
            return {"estado": "não aplicável", "termos": terms, "detalhe": reason or "a condição não se verifica"}
        if rule.label == "RIC":
            return {"estado": "conclusão", "termos": terms, "mensagem": rule.get("mensagem"),
                    "conclusao": {"tipo": rule.get("conclusaoTipo"), "valor": rule.get("conclusaoValor")}}
        state, value, detail = self.restriction(rule, node, prefix)
        out = {"estado": state, "termos": terms, "valor": value, "detalhe": detail}
        if state == "não conforme":
            out["mensagem"] = restriction.get("mensagem") if restriction is not None else None
        return out

    def arguments(self, call_edge, node, prefix):
        """Values of the arguments of a call (in parameter order), and the abstract paths read."""
        function = call_edge.target
        params = read_json(function.get("parametros"), [])
        args, read = [], []
        for i, a in enumerate(read_json(call_edge.get("argumentos"), [])):
            param = params[i] if i < len(params) else {}
            if "literal" in a:
                args.append(a["literal"])
                continue
            read.append(join(prefix, a["caminho"]))
            values = [v for _, v in collect(node, a["caminho"].split("."))]
            if param.get("colecao") or param.get("tipo") == "modelo":
                args.append([v for v in values if v is not None])
            else:
                args.append(values[0] if values else None)
        return function["nome"], args, read

    def restriction(self, rule, node, prefix):
        """(state, value, detail) of the rule's restriction in this occurrence."""
        restriction = K.restriction_of(self.g, rule)
        if restriction is None:
            return "conforme", None, None
        if restriction.get("forma") == "funcao":
            edge = next(iter(self.g.outgoing(restriction, "CHAMA")), None)
            name, args, _ = self.arguments(edge, node, prefix)
            result, reason = call_function(name, args, self.scenario.contexts)
            if result is None:
                return "não avaliável", args, reason
            return ("conforme" if result else "não conforme"), args, f"{edge.get('chamada')} → {'verdadeira' if result else 'falsa'}"
        edge = next(iter(self.g.outgoing(restriction, "RESTRINGE")), None)
        value = first_value(node, edge.get("caminho"))
        if value is None:
            return "sem valor", None, f"{edge.get('caminho')} não está na instância"
        result = evaluate(edge.get("operador"), value, read_json(edge.get("valor")))
        if result is None:
            return "não avaliável", value, f"o operador {edge.get('operador')} não se aplica a {value!r}"
        return ("conforme" if result else "não conforme"), value, edge.get("texto")

    def condition(self, rule, node, prefix):
        """('verdadeira' | 'falsa' | 'sem valor' | 'não avaliável', evaluated terms, reason)."""
        condition = K.condition_of(self.g, rule)
        if condition is None:
            return "verdadeira", [], None
        parts = [(e.get("ordem", 0), "typed", e) for e in self.g.outgoing(condition, "TERMO")] + \
                [(e.get("termo") if e.get("termo") is not None else 99, "function", e) for e in self.g.outgoing(condition, "CHAMA")]
        terms = []
        for _, form, edge in sorted(parts, key=lambda x: x[0]):
            outcome = self._typed_term(edge, node, prefix) if form == "typed" else self._function_term(edge, node, prefix)
            terms.append(outcome["termo"])
            if outcome["estado"] != "verdadeira":
                return outcome["estado"], terms, outcome.get("motivo")
        return "verdadeira", terms, None

    def _typed_term(self, edge, node, prefix):
        path = join(prefix, edge.get("caminho"))
        if not self.scenario.available(path):
            return {"estado": "não avaliável", "motivo": f"o termo lê {path}, que não está na projeção nem fixado no perfil",
                    "termo": {"texto": edge.get("texto"), "valor": None, "resultado": "fora da projeção"}}
        value = first_value(node, edge.get("caminho"))
        if edge.get("contexto"):
            expected = self.scenario.contexts.get(edge.get("contexto"))
            if expected is None:
                return {"estado": "não avaliável", "motivo": f"falta o contexto externo {edge.get('contexto')}",
                        "termo": {"texto": edge.get("texto"), "valor": value, "resultado": "não avaliável"}}
        else:
            expected = read_json(edge.get("valor"))
        if value is None:
            return {"estado": "sem valor", "motivo": f"a instância não traz {edge.get('caminho')}",
                    "termo": {"texto": edge.get("texto"), "valor": None, "resultado": "sem valor"}}
        result = evaluate(edge.get("operador"), value, expected)
        return {"estado": "verdadeira" if result else "falsa",
                "termo": {"texto": edge.get("texto"), "valor": value, "resultado": "verdadeiro" if result else "falso"}}

    def _function_term(self, edge, node, prefix):
        name, args, read = self.arguments(edge, node, prefix)
        outside = [p for p in read if not self.scenario.available(p)]
        if outside:
            return {"estado": "não avaliável", "motivo": f"a função lê {', '.join(outside)}, fora da projeção",
                    "termo": {"texto": edge.get("chamada"), "valor": args, "resultado": "fora da projeção"}}
        result, reason = call_function(name, args, self.scenario.contexts)
        if result is None:
            return {"estado": "não avaliável", "motivo": reason,
                    "termo": {"texto": edge.get("chamada"), "valor": args, "resultado": "não avaliável"}}
        return {"estado": "verdadeira" if result else "falsa",
                "termo": {"texto": edge.get("chamada"), "valor": args, "resultado": "verdadeiro" if result else "falso"}}
