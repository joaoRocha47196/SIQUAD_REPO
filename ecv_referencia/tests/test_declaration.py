"""Verification of a declaration: the examples are valid and each invariant detects what it should."""
import unittest
from pathlib import Path

from ecv import config
from ecv.ingestion import Declaration, derive, verify

ROOT = Path(__file__).resolve().parents[1]
EXAMPLES = config.example_declarations()
DEVICE = ROOT / "specs" / "exemplos" / "dispositivo.ecv.json"
SKELETON = ROOT / "specs" / "declaracao" / "esqueleto.ecv.json"


def codes(data):
    return {p.code for p in verify(Declaration(data)).problems}


def minimal():
    return {
        "funcoes": [{"nome": "f", "descricao": "Função de teste com contexto.", "contextosExternos": ["hoje"],
                     "parametros": [{"nome": "x", "tipo": "data", "papel": "alvo"}], "retorno": "booleano"}],
        "contextosExternos": [{"nome": "hoje", "tipo": "data", "descricao": "Data de hoje para testes."}],
        "usm": [{"nome": "Coisa", "descricao": "Coisa de teste com duas propriedades.", "propriedades": [
            {"nome": "tipo", "tipo": "texto", "descricao": "Tipo da coisa",
             "regras": [{"id": "RP-TIPO", "natureza": "plausibilidade", "descricao": "Coisa.tipo ∈ {A, B}",
                         "restricao": {"propriedade": "tipo", "operador": "IN", "valor": ["A", "B"],
                                       "mensagem": "O tipo tem de ser A ou B."}}]},
            {"nome": "valor", "tipo": "decimal", "descricao": "Valor da coisa"},
            {"nome": "data", "tipo": "data", "descricao": "Data da coisa"}]}],
        "sm": [{"nome": "Grupo", "descricao": "Grupo de coisas de teste.", "composicao": [{"usm": "Coisa", "cardinalidade": "1..1"}]}],
        "hlm": [{"nome": "Topo", "descricao": "Modelo de topo de teste.", "composicao": [{"sm": "Grupo", "cardinalidade": "1..1"}]}],
        "projecoes": [{"nome": "Tudo", "hlm": "Topo", "obrigatorias": ["Grupo.*"], "permitidas": []}],
        "perfis": [{"nome": "SoA", "projecao": "Tudo", "fixa": [{"propriedade": "Grupo.Coisa.tipo", "valor": "A"}]}],
    }


def rir(**kw):
    r = {"id": "RIR-X", "natureza": "inferencia_restritiva", "descricao": "x",
         "condicao": [{"propriedade": "tipo", "operador": "EQUALS", "valor": "A"}],
         "restricao": {"propriedade": "valor", "operador": "RANGE", "valor": [0, 10], "mensagem": "Fora da gama de teste."}}
    r.update(kw)
    return r


class TestExamples(unittest.TestCase):
    def test_three_declarations(self):
        self.assertEqual([p.name for p in EXAMPLES], ["dispositivo.ecv.json", "fatura.ecv.json", "ordem_instalacao.ecv.json"])

    def test_examples_without_errors(self):
        for f in EXAMPLES + [SKELETON]:
            report = verify(Declaration.load(f))
            self.assertTrue(report.valid, (f.name, [str(p) for p in report.errors]))

    def test_only_intended_anomalies(self):
        # see specs/exemplos/README.md
        report = verify(Declaration.load(DEVICE))
        self.assertEqual({p.code for p in report.warnings}, {"I7", "I10"})

    def test_one_hlm_per_declaration(self):
        for f in EXAMPLES:
            d = Declaration.load(f)
            self.assertEqual(len(d.hlm), 1, f.name)
            self.assertEqual(d.data["declaracao"]["hlm"], next(iter(d.hlm)))

    def test_two_hlm_is_an_error(self):
        d = minimal()
        d["hlm"].append({"nome": "Outro", "descricao": "Segundo HLM de teste.", "composicao": [{"sm": "Grupo", "cardinalidade": "1..1"}]})
        self.assertIn("S-DECL", codes(d))

    def test_descriptions_are_derived(self):
        for f in EXAMPLES:
            for site in Declaration.load(f).rules():
                self.assertEqual(site.rule["descricao"], derive(site.rule, site.level, site.model), site.id)

    def test_description_from_the_thesis(self):
        site = Declaration.load(DEVICE).rule("RIR-TEMP-REFRIG-CELSIUS")
        self.assertEqual(site.rule["descricao"],
                         "Se Identificacao.tipoDispositivo = TEMPERATURA e Leitura.Medicao.unidadeMedida = °C e "
                         "Leitura.Instalacao.ambiente = REFRIGERACAO → Leitura.Medicao.valor entre -30 e 0")

    def test_schema_matches_configuration(self):
        import json
        schema = json.loads(config.path("esquemaDeclaracao").read_text(encoding="utf-8"))["$defs"]
        self.assertEqual(schema["tipoBase"]["enum"], list(config.BASE_TYPES))
        self.assertEqual(schema["cardinalidade"]["enum"], list(config.CARDINALITIES))
        self.assertEqual(set(schema["operadorTipificado"]["enum"]) | set(schema["operadorFuncao"]["enum"]), set(config.OPERATORS))


class TestInvariants(unittest.TestCase):
    def test_minimal_is_valid(self):
        self.assertFalse({c for c in codes(minimal()) if not c.startswith("I1")}, codes(minimal()))

    def test_i4_rp_with_condition(self):
        d = minimal()
        d["usm"][0]["propriedades"][0]["regras"][0]["condicao"] = [{"propriedade": "tipo", "operador": "EQUALS", "valor": "A"}]
        self.assertIn("I4", codes(d))

    def test_i4_ric_with_restriction(self):
        d = minimal()
        d["usm"][0]["regras"] = [rir(id="RIC-X", natureza="inferencia_conclusiva", mensagem="Conclusão de teste.")]
        self.assertIn("I4", codes(d))

    def test_i6_condition_reads_target(self):
        d = minimal()
        d["usm"][0]["regras"] = [rir(condicao=[{"propriedade": "valor", "operador": "GT", "valor": 100}])]
        self.assertIn("I6", codes(d))

    def test_i5_incompatible_operator(self):
        d = minimal()
        d["usm"][0]["regras"] = [rir(restricao={"propriedade": "tipo", "operador": "RANGE", "valor": [0, 1],
                                                "mensagem": "Operador errado para texto."})]
        self.assertIn("I5", codes(d))

    def test_i5_ext_function(self):
        d = minimal()
        d["usm"][0]["regras"] = [rir(restricao={"operador": "FUNCTION", "mensagem": "Função sem EXT_FUNCTION.",
                                                "chamada": {"funcao": "f", "argumentos": [{"caminho": "data"}]}})]
        self.assertIn("I5", codes(d))

    def test_i3_missing_path(self):
        d = minimal()
        d["usm"][0]["regras"] = [rir(restricao={"propriedade": "naoExiste", "operador": "GT", "valor": 1,
                                                "mensagem": "Caminho inexistente."})]
        self.assertIn("I3", codes(d))

    def test_i3_property_rule_reads_another(self):
        d = minimal()
        d["usm"][0]["propriedades"][1]["regras"] = [rir()]
        self.assertIn("I3", codes(d))

    def test_i7_implausible_value(self):
        d = minimal()
        d["usm"][0]["regras"] = [rir(condicao=[{"propriedade": "tipo", "operador": "EQUALS", "valor": "Z"}])]
        self.assertIn("I7", codes(d))

    def test_i8_could_live_lower(self):
        d = minimal()
        r = rir(condicao=[{"propriedade": "Coisa.tipo", "operador": "EQUALS", "valor": "A"}],
                restricao={"propriedade": "Coisa.valor", "operador": "GT", "valor": 0, "mensagem": "Tem de ser positivo."})
        d["sm"][0]["regras"] = [r]
        self.assertIn("I8", codes(d))

    def test_i9_mandatory_and_permitted(self):
        d = minimal()
        d["projecoes"][0]["permitidas"] = ["Grupo.Coisa.valor"]
        self.assertIn("I9", codes(d))

    def test_i9_fixed_value_implausible(self):
        d = minimal()
        d["perfis"][0]["fixa"][0]["valor"] = "Z"
        self.assertIn("I9", codes(d))

    def test_i10_condition_outside_projection(self):
        d = minimal()
        d["usm"][0]["regras"] = [rir()]
        d["projecoes"][0]["obrigatorias"] = ["Grupo.Coisa.valor"]
        d["perfis"][0]["fixa"] = []
        self.assertIn("I10", codes(d))

    def test_hlm_without_properties(self):
        d = minimal()
        d["hlm"][0]["propriedades"] = [{"nome": "x", "tipo": "texto", "descricao": "Proibida aqui"}]
        self.assertIn("S-MOD", codes(d))

    def test_message_belongs_to_restriction(self):
        d = minimal()
        r = rir()
        r["mensagem"] = "Mensagem no sítio errado."
        d["usm"][0]["regras"] = [r]
        self.assertIn("S-REGRA", codes(d))


if __name__ == "__main__":
    unittest.main()
