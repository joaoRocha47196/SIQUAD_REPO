"""Structural validation of an instance against the HLM and the projection (the structural rules, RE),
after applying the values the profile fixes."""
from ecv import config

from .instance import abstract_path, collect, has_base_type, join

PROBLEM_TYPES = ("falta", "excluída", "desconhecida", "tipo", "cardinalidade", "fixado")


class StructureCheck:
    def __init__(self, scenario, instance):
        self.scenario = scenario
        self.instance = instance
        self.problems = []

    def add(self, kind, path, text):
        self.problems.append({"tipo": kind, "caminho": path, "problema": text})

    def run(self):
        self.apply_fixed_values()
        self.check_node(self.instance)
        self.check_mandatory()
        return self.problems

    # ------------------------------------------------------------------ fixed values
    def apply_fixed_values(self):
        """Each property fixed by the profile goes into the instance; another value there is a problem ('fixado')."""
        for path, value in self.scenario.fixed.items():
            self._fix(self.instance, path.split("."), value, "")

    def _fix(self, node, segments, value, prefix):
        first = segments[0]
        if len(segments) == 1:
            current = node.get(first)
            if current is not None and current != value:
                self.add("fixado", join(prefix, first), f"a instância traz {current!r}, mas o perfil fixa {value!r}")
            node[first] = value
            return
        model = self.scenario.models.get(abstract_path(join(prefix, first)))
        if node.get(first) is None:
            if model is None or config.is_repeatable(model.get("cardinalidade")):
                return
            node[first] = {}
        items = node[first] if isinstance(node[first], list) else [node[first]]
        for i, item in enumerate(items):
            if isinstance(item, dict):
                self._fix(item, segments[1:], value, join(prefix, first) + (f"[{i}]" if isinstance(node[first], list) else ""))

    # ------------------------------------------------------------------ shape
    def check_node(self, node, abstract="", concrete=""):
        if not isinstance(node, dict):
            self.add("tipo", concrete or "(raiz)", "esperava-se um objeto (um modelo)")
            return
        for key, value in node.items():
            a, c = join(abstract, key), join(concrete, key)
            if a in self.scenario.models:
                self._check_composition(a, c, value)
            elif a in self.scenario.properties:
                self._check_property(a, c, value)
            else:
                self.add("desconhecida", c, "não existe no modelo")

    def _check_composition(self, abstract, concrete, value):
        card = self.scenario.models[abstract].get("cardinalidade")
        repeatable = config.is_repeatable(card)
        if isinstance(value, list):
            if not repeatable:
                self.add("cardinalidade", concrete, f"lista numa composição {card} (não repetível)")
            for i, item in enumerate(value):
                self.check_node(item, abstract, f"{concrete}[{i}]")
        else:
            if repeatable:
                self.add("cardinalidade", concrete, f"composição repetível ({card}): esperava-se uma lista")
            self.check_node(value, abstract, concrete)

    def _check_property(self, abstract, concrete, value):
        if value is None:
            return
        base_type = self.scenario.properties[abstract].get("tipoBase")
        if not has_base_type(base_type, value):
            self.add("tipo", concrete, f"{value!r} não é do tipo {base_type}")
        if not self.scenario.available(abstract):
            self.add("excluída", concrete, f"a projeção {self.scenario.projection} não inclui esta propriedade")

    def check_mandatory(self):
        for path in self.scenario.mandatory:
            for concrete, value in collect(self.instance, path.split(".")):
                if value is None:
                    self.add("falta", concrete, f"obrigatória na projeção {self.scenario.projection}")
