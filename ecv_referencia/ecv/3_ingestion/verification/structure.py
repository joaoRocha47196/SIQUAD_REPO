"""Structure checks: JSON Schema, the declaration header, contexts, functions, models, compositions,
properties and acyclicity (specs of each entity, invariants I1 and I2)."""
import json

from ecv import config

MODEL_NAME = config.NAME_PATTERNS["modelo"]
PROPERTY_NAME = config.NAME_PATTERNS["propriedade"]
FUNCTION_NAME = config.NAME_PATTERNS["funcao"]
CONTEXT_NAME = config.NAME_PATTERNS["contexto"]


class StructureChecks:
    """Mixin of Verifier: expects self.decl (Declaration) and self.report (Report)."""

    def check_schema(self):
        """General shape against specs/declaracao/ecv.schema.json (only when the jsonschema package is installed)."""
        try:
            import jsonschema
        except ImportError:
            return
        path = config.path("esquemaDeclaracao")
        if not path.exists():
            return
        schema = json.loads(path.read_text(encoding="utf-8"))
        for err in jsonschema.Draft202012Validator(schema).iter_errors(self.decl.data):
            where = "/".join(str(x) for x in err.absolute_path) or "declaração"
            self.report.error("S-SCHEMA", where, err.message[:300])

    def check_header(self):
        data = self.decl.data
        if not data.get("usm"):
            self.report.error("S-DECL", "declaração", "a lista 'usm' é obrigatória e não pode estar vazia")
        if config.INGESTION["umHlmPorDeclaracao"]:
            hlms = [m.get("nome") for m in data.get("hlm", [])]
            if len(hlms) != 1:
                self.report.error("S-DECL", "declaração", f"uma declaração descreve exatamente um HLM (tem {len(hlms)}: {hlms}); "
                                  "os modelos partilhados repetem-se em cada declaração e a ingestão funde-os")
            header_hlm = data.get("declaracao", {}).get("hlm")
            if hlms and header_hlm is not None and header_hlm != hlms[0]:
                self.report.error("S-DECL", "declaração", f"o cabeçalho indica o HLM '{header_hlm}', mas a declaração descreve '{hlms[0]}'")
        for section in ("usm", "sm", "hlm", "funcoes", "contextosExternos", "projecoes", "perfis"):
            seen = set()
            for entity in data.get(section, []):
                name = entity.get("nome")
                if name is None:
                    self.report.error("S-DECL", section, "entidade sem 'nome'")
                elif name in seen:
                    self.report.error("S-DECL", f"{section} {name}", "nome repetido na mesma secção")
                seen.add(name)

    def check_contexts(self):
        for name, ctx in self.decl.contexts.items():
            where = f"contexto {name}"
            if not CONTEXT_NAME.match(name):
                self.report.error("S-CTX", where, "nome em camelCase")
            if ctx.get("tipo") not in config.BASE_TYPES:
                self.report.error("S-CTX", where, f"tipo tem de ser um de {config.BASE_TYPES}")
            if len(ctx.get("descricao", "")) < 10:
                self.report.error("S-CTX", where, "descrição com pelo menos 10 caracteres")

    def check_functions(self):
        for name, f in self.decl.functions.items():
            where = f"função {name}"
            if not FUNCTION_NAME.match(name):
                self.report.error("S-FUNC", where, "nome em camelCase")
            if len(f.get("descricao", "")) < 10:
                self.report.error("S-FUNC", where, "descrição com pelo menos 10 caracteres")
            if f.get("retorno") not in config.FUNCTION_RETURNS:
                self.report.error("S-FUNC", where, "o retorno de uma função de validação é 'booleano'")
            params = f.get("parametros")
            if not isinstance(params, list) or not params:
                self.report.error("S-FUNC", where, "'parametros' é uma lista não vazia")
                params = []
            for p in params:
                if p.get("papel") not in config.PARAMETER_ROLES:
                    self.report.error("S-FUNC", where, f"parâmetro {p.get('nome')}: papel 'alvo' ou 'parametro'")
                if not p.get("tipo"):
                    self.report.error("S-FUNC", where, f"parâmetro {p.get('nome')}: sem tipo")
            if not isinstance(f.get("contextosExternos"), list):
                self.report.error("S-FUNC", where, "'contextosExternos' é uma lista (vazia se não usar nenhum)")
            for ctx in f.get("contextosExternos", []) or []:
                if ctx not in self.decl.contexts:
                    self.report.error("S-FUNC", where, f"contexto externo '{ctx}' não declarado")

    def check_models(self):
        for level, name, m in self.decl.all_models():
            where = f"{level} {name}"
            self._check_model_shape(level, name, m, where)
            roles = self._check_compositions(level, m, where)
            self._check_model_properties(m, roles, where)
        self.check_acyclic()

    def _check_model_shape(self, level, name, m, where):
        if not MODEL_NAME.match(name):
            self.report.error("S-MOD", where, "nome em PascalCase, sem acentos")
        if len(m.get("descricao", "")) < 10:
            self.report.error("S-MOD", where, "descrição com pelo menos 10 caracteres")
        if level == "HLM" and m.get("propriedades"):
            self.report.error("S-MOD", where, "um HLM não declara propriedades: é só composição de SM")
        if level == "USM" and m.get("composicao"):
            self.report.error("S-MOD", where, "um USM não compõe outros modelos")
        if level == "USM" and not m.get("propriedades"):
            self.report.error("S-MOD", where, "um USM tem pelo menos uma propriedade")
        if level == "HLM" and not m.get("composicao"):
            self.report.error("S-MOD", where, "um HLM tem pelo menos uma composição")
        if level == "SM" and not m.get("composicao") and not m.get("propriedades"):
            self.report.error("S-MOD", where, "um SM compõe pelo menos um USM ou declara propriedades residuais")

    def _check_compositions(self, level, m, where):
        roles = set()
        for c in m.get("composicao", []):
            keys = [k for k in ("sm", "usm") if k in c]
            if len(keys) != 1:
                self.report.error("S-COMP", where, "cada composição tem exatamente um de 'sm' ou 'usm'")
                continue
            key = keys[0]
            expected = {"HLM": "sm", "SM": "usm"}.get(level)
            if key != expected:
                self.report.error("S-COMP", where, f"um {level} compõe '{expected}', não '{key}'")
            if c.get("cardinalidade") not in config.CARDINALITIES:
                self.report.error("S-COMP", where, f"cardinalidade de {c[key]}: uma de {config.CARDINALITIES}")
            if self.decl.model(key.upper(), c[key]) is None:
                self.report.error("I2", where, f"compõe {key.upper()} {c[key]}, que não está declarado")
            role = c.get("papel", c[key])
            if not MODEL_NAME.match(role):
                self.report.error("S-COMP", where, f"papel '{role}' em PascalCase")
            if role in roles:
                self.report.error("S-COMP", where, f"papel '{role}' repetido: use 'papel' para distinguir as ocorrências")
            roles.add(role)
        return roles

    def _check_model_properties(self, m, roles, where):
        names = set()
        for p in m.get("propriedades", []):
            self.check_property(where, p)
            if p.get("nome") in names:
                self.report.error("S-PROP", where, f"propriedade '{p.get('nome')}' repetida")
            if p.get("nome") in roles:
                self.report.error("S-PROP", where, f"'{p.get('nome')}' é ao mesmo tempo papel e propriedade")
            names.add(p.get("nome"))

    def check_property(self, where, p):
        name = p.get("nome", "?")
        w = f"{where}.{name}"
        if not PROPERTY_NAME.match(name):
            self.report.error("S-PROP", w, "nome em camelCase")
        if p.get("tipo") not in config.BASE_TYPES:
            self.report.error("S-PROP", w, f"tipo tem de ser um de {config.BASE_TYPES}")
        if len(p.get("descricao", "")) < 5:
            self.report.error("S-PROP", w, "descrição com pelo menos 5 caracteres")
        if not isinstance(p.get("nomesAlternativos", []), list):
            self.report.error("S-PROP", w, "'nomesAlternativos' é uma lista")

    def check_acyclic(self):
        """I1: with the levels HLM → SM → USM composition is acyclic by construction; checked anyway,
        for declarations that break the level rule."""
        state = {}

        def visit(node, stack):
            if state.get(node) == 1:
                self.report.error("I1", f"{node[0]} {node[1]}", "a composição tem um ciclo: "
                                  + " → ".join(f"{a} {b}" for a, b in stack + [node]))
                return
            if state.get(node) == 2:
                return
            state[node] = 1
            for _, child_level, child, _ in self.decl.compositions(*node):
                visit((child_level, child), stack + [node])
            state[node] = 2

        for level, name, _ in self.decl.all_models():
            visit((level, name), [])
