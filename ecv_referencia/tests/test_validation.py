"""Validation of instances: functions and engine (structure, rules, profiles and contexts)."""
import copy
import unittest

from ecv import config, validation
from ecv.ingestion import ingest
from ecv.validation.functions import call


class TestFunctions(unittest.TestCase):
    def test_dates_and_contexts(self):
        self.assertEqual(call("naoPosteriorAHoje", ["2026-09-30"], {"dataDeHoje": "2026-09-30"}), (True, None))
        self.assertEqual(call("naoPosteriorAHoje", ["2026-10-01"], {"dataDeHoje": "2026-09-30"})[0], False)
        r, reason = call("naoPosteriorAHoje", ["2026-10-01"], {})
        self.assertIsNone(r)
        self.assertIn("dataDeHoje", reason)
        self.assertTrue(call("desfasamentoInferiorA", ["2026-09-30T12:04:00Z", 300], {"relogioServidor": "2026-09-30T12:00:00Z"})[0])
        self.assertFalse(call("excedeDiasDesdeHoje", ["2026-09-25", 7], {"dataDeHoje": "2026-09-30"})[0])

    def test_collections_and_documents(self):
        self.assertTrue(call("somaIgualA", [[12.5, 7.5], 20], {})[0])
        self.assertFalse(call("valoresConsecutivos", [[1, 3]], {})[0])
        self.assertTrue(call("digitoControloValido", ["123456789"], {})[0])
        self.assertFalse(call("digitoControloValido", ["123456780"], {})[0])
        self.assertTrue(call("atcudValido", ["AB12CD34-1", "FT"], {"seriesComunicadasAT": "FT=AB12CD34"})[0])
        self.assertTrue(call("dentroDe", [38.7, -9.1, [[38.8, -9.25], [38.8, -9.05], [38.68, -9.05], [38.68, -9.25]]], {})[0])
        self.assertIn("não tem implementação", call("naoExiste", [], {})[1])


class TestEngine(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.g = ingest(config.example_declarations()).graph

    def states(self, vm):
        return {(row["regra"], row["ocorrencia"]): row["estado"] for row in vm["regras"]}

    def test_examples(self):
        expected = {"fatura_simplificada_valida": True, "fatura_at_com_erros": False, "fatura_at_incompleta": False,
                    "dispositivo_refrigeracao": False, "dispositivo_teste_laboratorio": False, "ordem_instalacao": False}
        for name, valid in expected.items():
            self.assertEqual(validation.validate_example(self.g, name)["valida"], valid, name)

    def test_values_fixed_by_the_profile(self):
        vm = validation.validate_example(self.g, "fatura_simplificada_valida")
        self.assertEqual(vm["instanciaAvaliada"]["Cabecalho"]["tipoDocumento"], "FS")
        state = self.states(vm)
        self.assertEqual(state[("RIR-FS-NUM", "Cabecalho")], "conforme")
        self.assertEqual(state[("RP-NIF", "Cliente.Entidade")], "fora da projeção")
        ex = validation.examples()["fatura_simplificada_valida"]
        instance = copy.deepcopy(ex["instancia"])
        instance["Cabecalho"]["tipoDocumento"] = "FT"
        vm = validation.validate(self.g, instance, profile="EmissaoSimplificada", contexts=ex["contextos"])
        self.assertEqual([p["tipo"] for p in vm["estrutura"]], ["fixado"])

    def test_rules_per_occurrence(self):
        vm = validation.validate_example(self.g, "fatura_at_com_erros")
        state = self.states(vm)
        self.assertEqual(state[("RIR-IVA-NOR", "Linhas.Linha[1]")], "não conforme")
        self.assertEqual(state[("RIR-IVA-NOR", "Linhas.Linha[0]")], "conforme")
        self.assertEqual(state[("RP-NIF-DC", "Cliente.Entidade")], "não conforme")
        self.assertEqual(state[("RP-NIF-DC", "Emitente.Entidade")], "conforme")
        self.assertEqual(state[("RP-DATAEMISSAO", "Cabecalho")], "não conforme")  # dataDeHoje fixada no perfil
        self.assertEqual(state[("RP-SOMA", "(HLM)")], "não conforme")
        self.assertIn({"tipo": "desconhecida", "caminho": "observacoes", "problema": "não existe no modelo"}, vm["estrutura"])
        contexts = {c["nome"]: c["origem"] for c in vm["contextos"]}
        self.assertEqual(contexts["dataDeHoje"], "fixado no perfil")
        self.assertEqual(contexts["hashAnterior"], "indicado no pedido")

    def test_missing_contexts_and_mandatory(self):
        vm = validation.validate_example(self.g, "fatura_at_incompleta")
        state = self.states(vm)
        self.assertEqual(state[("RP-HASH", "Cabecalho")], "não avaliável")
        self.assertIn("Cliente.Entidade.nif", [p["caminho"] for p in vm["estrutura"] if p["tipo"] == "falta"])

    def test_conclusions_and_lists(self):
        vm = validation.validate_example(self.g, "dispositivo_refrigeracao")
        self.assertEqual([c["regra"] for c in vm["conclusoes"]], ["RIC-MANUT"])
        vm = validation.validate_example(self.g, "ordem_instalacao")
        state = self.states(vm)
        self.assertEqual(state[("RP-AREA", "Localizacao[0].InformacaoGeografica")], "conforme")
        self.assertEqual(state[("RP-AREA", "Localizacao[1].InformacaoGeografica")], "não conforme")

    def test_structure_types_and_cardinality(self):
        vm = validation.validate(self.g, {"Pedido": {"numeroOrdem": 7}, "Localizacao": {"indicacaoAcesso": "x"}}, hlm="OrdemInstalacao")
        kinds = {p["tipo"] for p in vm["estrutura"]}
        self.assertEqual(kinds, {"tipo", "cardinalidade"})

    def test_view(self):
        from ecv.views.presentation import render_page
        from ecv.views.viewmodels import build
        h = render_page(build(self.g, "validacao", exemplo="fatura_at_com_erros"))
        self.assertIn("Instância inválida", h)
        self.assertIn("RIR-IVA-NOR", h)


if __name__ == "__main__":
    unittest.main()
