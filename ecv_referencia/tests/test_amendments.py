"""Module 2: the operations keep the declarations consistent; a batch is all or nothing; CSV tables become RIR."""
import copy
import shutil
import tempfile
import unittest
from pathlib import Path

from ecv import config
from ecv.amendments import DeclarationSet, apply_operations, operations_from_csv
from ecv.ingestion import Declaration, verify
from ecv.shared.errors import AmendmentError


class TestOperations(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        (self.tmp / "declaracoes").mkdir()
        for f in config.example_declarations():
            shutil.copy(f, self.tmp / "declaracoes" / f.name)
        self.ds = DeclarationSet.load(self.tmp)

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def assert_valid(self):
        for hlm, d in self.ds.declarations.items():
            report = verify(Declaration(copy.deepcopy(d)))
            self.assertTrue(report.valid, (hlm, [str(p) for p in report.errors]))

    def test_renaming_a_shared_model_changes_every_declaration(self):
        apply_operations(self.ds, [{"op": "renomear_modelo", "nivel": "USM", "de": "Morada", "para": "MoradaPostal"}])
        for d in self.ds.declarations.values():
            self.assertFalse(any(m["nome"] == "Morada" for m in d["usm"]))
        self.assertEqual(len(self.ds.containing("USM", "MoradaPostal")), 3)

    def test_extract_and_rename(self):
        apply_operations(self.ds, [
            {"op": "extrair_usm", "de": {"nivel": "SM", "modelo": "Localizacao"}, "propriedades": ["indicacaoAcesso"],
             "novo": {"nome": "Acesso", "descricao": "Indicações de acesso a um local."}, "cardinalidade": "0..1"},
            {"op": "renomear_propriedade", "nivel": "USM", "modelo": "Acesso", "de": "indicacaoAcesso", "para": "indicacao"}])
        self.assertEqual(len(self.ds.containing("USM", "Acesso")), 2)          # Dispositivo and OrdemInstalacao
        self.assertIn({"usm": "Acesso", "cardinalidade": "0..1"}, self.ds.definition("SM", "Localizacao")["composicao"])
        self.assert_valid()

    def test_composing_copies_into_the_declaration(self):
        apply_operations(self.ds, [{"op": "compor", "pai": {"nivel": "SM", "nome": "Cabecalho"},
                                    "filho": {"nivel": "USM", "nome": "InformacaoGeografica"}, "cardinalidade": "0..1", "papel": "LocalEmissao"}])
        self.assertTrue(any(m["nome"] == "InformacaoGeografica" for m in self.ds.declarations["Fatura"]["usm"]))
        self.assert_valid()

    def test_rule_with_a_new_function(self):
        apply_operations(self.ds, [
            {"op": "definir_funcao", "funcao": {"nome": "naoVazio", "descricao": "Verdadeira quando o texto não é vazio.",
                                              "parametros": [{"nome": "t", "tipo": "texto", "papel": "alvo"}],
                                              "contextosExternos": [], "retorno": "booleano"}},
            {"op": "adicionar_regra", "onde": {"nivel": "USM", "modelo": "Morada", "propriedade": "rua"},
             "regra": {"id": "RP-RUA-NAO-VAZIA", "natureza": "plausibilidade",
                       "restricao": {"operador": "FUNCTION", "chamada": {"funcao": "naoVazio", "argumentos": [{"caminho": "rua"}]},
                                     "mensagem": "A rua não pode ser vazia."}}}])
        for d in self.ds.containing("USM", "Morada"):
            self.assertTrue(any(f["nome"] == "naoVazio" for f in d["funcoes"]))
        self.assert_valid()

    def test_merge_models(self):
        apply_operations(self.ds, [
            {"op": "criar_modelo", "nivel": "USM", "nome": "Endereco", "descricao": "Endereço postal (duplicado de teste).",
             "propriedades": [{"nome": "rua", "tipo": "texto", "descricao": "Rua"}], "declaracoes": ["Fatura"]},
            {"op": "compor", "pai": {"nivel": "SM", "nome": "Cabecalho"}, "filho": {"nivel": "USM", "nome": "Endereco"}, "cardinalidade": "0..1"},
            {"op": "fundir_modelos", "nivel": "USM", "de": ["Endereco"], "para": "Morada"}])
        self.assertIsNone(self.ds.definition("USM", "Endereco"))
        self.assertIn({"usm": "Morada", "cardinalidade": "0..1"}, self.ds.definition("SM", "Cabecalho")["composicao"])
        self.assert_valid()

    def test_invalid_operation(self):
        with self.assertRaises(AmendmentError):
            apply_operations(self.ds, [{"op": "mover_propriedade", "de": {"nivel": "USM", "modelo": "Morada"},
                                        "para": {"nivel": "USM", "modelo": "NaoExiste"}, "nome": "rua"}])
        with self.assertRaises(AmendmentError):
            apply_operations(self.ds, [{"op": "inventada"}])


class TestCsvRules(unittest.TestCase):
    TABLE = "pais;localidade;freguesia;codigoPostal\nPT;LISBOA;AJUDA;^(1300|1349)-[0-9]{3}$\nPT;LISBOA;ALCANTARA;^(1300|1350)-[0-9]{3}$\n"

    def test_one_rir_per_row(self):
        ops = operations_from_csv(self.TABLE, "USM", "Morada", "codigoPostal", "PATTERN", "RIR-CP-LX-")
        self.assertEqual(len(ops), 2)
        rule = ops[0]["regra"]
        self.assertEqual(rule["natureza"], "inferencia_restritiva")
        self.assertEqual([t["propriedade"] for t in rule["condicao"]], ["pais", "localidade", "freguesia"])
        self.assertEqual(rule["restricao"], {"propriedade": "codigoPostal", "operador": "PATTERN", "valor": "^(1300|1349)-[0-9]{3}$",
                                             "mensagem": rule["restricao"]["mensagem"]})

    def test_rules_are_valid_in_the_examples(self):
        tmp = Path(tempfile.mkdtemp())
        try:
            (tmp / "declaracoes").mkdir()
            for f in config.example_declarations():
                shutil.copy(f, tmp / "declaracoes" / f.name)
            ds = DeclarationSet.load(tmp)
            table = "pais;localidade;codigoPostal\nPT;LISBOA;^1[0-9]{3}-[0-9]{3}$\nPT;PORTO;^4[0-9]{3}-[0-9]{3}$\n"
            apply_operations(ds, operations_from_csv(table, "USM", "Morada", "codigoPostal", "PATTERN", "RIR-CSV-"))
            for hlm, d in ds.declarations.items():
                report = verify(Declaration(copy.deepcopy(d)))
                self.assertTrue(report.valid, (hlm, [str(p) for p in report.errors]))
        finally:
            shutil.rmtree(tmp)

    def test_missing_target_column(self):
        with self.assertRaises(AmendmentError):
            operations_from_csv(self.TABLE, "USM", "Morada", "naoExiste", "PATTERN", "RIR-")


if __name__ == "__main__":
    unittest.main()
