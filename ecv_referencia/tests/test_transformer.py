"""Module 0: the adapters of the known formats and the classification of source rules."""
import shutil
import unittest

from ecv import config
from ecv.transformer import ADAPTERS, classify
from ecv.transformer.adapters import cius_pt

DATA = config.data_root()


@unittest.skipUnless((DATA / "data").exists(), "pasta data/ do repositório não disponível")
class TestAdapters(unittest.TestCase):
    def test_cius_pt(self):
        rules = cius_pt.schematron(DATA / "data/CIS_PT_SCHEMATRON/urn_feap.gov.pt_cius-pt_schematron")
        self.assertGreater(len(rules.rules), 1000)
        br06 = next(r for r in rules.rules if r.id == "BR-06")
        self.assertEqual((br06.category, br06.nature, br06.elements), ("presenca", "RE", ["BT-27"]))
        if shutil.which("pdftotext"):
            guide = cius_pt.guide(DATA / "data/CIS_PT_SCHEMATRON/guia_modelo_dados_semanticos_dos_documentos_fe_cius-pt_v1.1.pdf",
                                  cius_pt.english_names(rules))
            bt3 = next(e for e in guide.elements if e.id == "BT-3")
            self.assertEqual(bt3.allowed_values, ["380", "381", "383", "386", "389"])
            self.assertIn("Seller name", next(e for e in guide.elements if e.id == "BT-27").alternative_names)

    def test_fm_and_smart_data_models(self):
        dart = ADAPTERS["fm.dart"](DATA / "data/FM/model")
        self.assertEqual(next(e for e in dart.elements if e.id == "Delivery.articles").source_type, "List<DeliveryItem>")
        sdm = ADAPTERS["json_schema.smart_data_models"](DATA / "data/SDM_Device")
        self.assertIn("GSMA-Commons", {g.id for g in sdm.groups})
        self.assertTrue(any(r.id == "Device.batteryLevel-GAMA-1" for r in sdm.rules))


class TestClassification(unittest.TestCase):
    def test_classify(self):
        self.assertEqual(classify("Value added tax point date (BT-7) and code (BT-8) are mutually exclusive.")[0], "exclusao")
        self.assertEqual(classify("In case the Amount due for payment (BT-115) is positive, ...")[0], "condicional")
        self.assertEqual(classify("An Invoice shall have an Invoice number (BT-1).")[0], "presenca")


if __name__ == "__main__":
    unittest.main()
