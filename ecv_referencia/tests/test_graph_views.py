"""Ingestion (materialisation and merge), conformance with the graph model, ViewModels, views and Neo4j."""
import copy
import json
import os
import re
import tempfile
import unittest
from pathlib import Path

from ecv import config
from ecv.graph.cypher_export import export
from ecv.graph.model import conformance
from ecv.ingestion import Declaration, ingest
from ecv.views.static_site import generate
from ecv.views.viewmodels import REGISTRY, build
from ecv.views.viewmodels.cypher_runner import statements

EXAMPLES = config.example_declarations()


def graph():
    ingestion = ingest(EXAMPLES)
    assert ingestion.valid, [r.summary() for r in ingestion.results]
    return ingestion.graph


class TestMerge(unittest.TestCase):
    def test_shared_models_are_not_repeated(self):
        g = graph()
        nodes, _ = g.counts()
        self.assertEqual((nodes["HLM"], nodes["SM"], nodes["USM"], nodes["Propriedade"]), (3, 9, 9, 43))
        self.assertEqual(nodes["Declaracao"], 3)
        self.assertEqual(sum(nodes.values()), 430)
        self.assertEqual(len(g.nodes("USM")), len({n["nome"] for n in g.nodes("USM")}))

    def test_ingesting_again_adds_nothing(self):
        g = graph()
        before = len(g.nodes()), len(g.edges)
        ingestion = ingest(EXAMPLES, g)
        self.assertTrue(all(r.plan.valid and not r.plan.new_nodes and not r.plan.new_edges for r in ingestion.results))
        self.assertEqual((len(g.nodes()), len(g.edges)), before)

    def test_order_does_not_matter(self):
        self.assertEqual(graph().counts(), ingest(list(reversed(EXAMPLES))).graph.counts())

    def test_different_shared_model_is_a_conflict(self):
        g = graph()
        data = copy.deepcopy(Declaration.load(EXAMPLES[1]).data)        # fatura
        data["declaracao"]["nome"] = "Fatura alterada"
        address = next(u for u in data["usm"] if u["nome"] == "Morada")
        address["propriedades"].append({"nome": "andar", "tipo": "texto", "descricao": "Andar da morada."})
        before = len(g.nodes())
        result = ingest([Declaration(data, "alterada")], g).results[0]
        self.assertFalse(result.accepted)
        self.assertIn("USM:Morada", [c.node for c in result.plan.conflicts])
        self.assertEqual(len(g.nodes()), before)

    def test_changed_rule_is_a_conflict(self):
        g = graph()
        data = copy.deepcopy(Declaration.load(EXAMPLES[2]).data)        # ordem de instalação
        data["declaracao"]["nome"] = "Ordem alterada"
        address = next(u for u in data["usm"] if u["nome"] == "Morada")
        country = next(p for p in address["propriedades"] if p["nome"] == "pais")
        country["regras"][0]["restricao"]["mensagem"] = "Outra mensagem."
        result = ingest([Declaration(data, "alterada")], g).results[0]
        self.assertFalse(result.accepted)
        self.assertTrue(any(c.node.startswith("Restricao:") for c in result.plan.conflicts))


class TestGraph(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.g = graph()

    def test_conforms_to_the_model(self):
        self.assertEqual(conformance(self.g), [])

    def test_restriction_has_one_target(self):
        for r in self.g.nodes("Restricao"):
            self.assertLessEqual(len(self.g.outgoing(r, "RESTRINGE")), 1)
            if r["forma"] == "tipificada":
                self.assertEqual(len(self.g.outgoing(r, "RESTRINGE")), 1)
            else:
                self.assertEqual(len(self.g.outgoing(r, "CHAMA")), 1)

    def test_rule_types(self):
        expected = {"RP": (True, False), "RIR": (True, True), "RIC": (False, True)}
        for r in self.g.nodes("Regra"):
            shape = (bool(self.g.outgoing(r, "RESTRITA_POR")), bool(self.g.outgoing(r, "CONDICIONADA_POR")))
            self.assertEqual(shape, expected[r.label], r["id"])

    def test_cypher_export(self):
        text = export(self.g)
        self.assertIn("CREATE CONSTRAINT ecv_hlm", text)
        self.assertEqual(text.count("CREATE (:"), len(self.g.nodes()))


class TestViewModels(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.g = graph()

    def test_decision_flags_anomalies(self):
        vm = build(self.g, "decisao", alvo="USM:Medicao.valor")
        m = vm["matriz"]
        self.assertEqual(m["dimensaoLinhas"], "ambiente")
        states = {(row["rotulo"], c["estado"]) for row in m["linhas"] for c in row["celulas"]}
        self.assertIn(("EXTERIOR", "incoerente"), states)
        self.assertTrue(next(row for row in m["linhas"] if row["rotulo"] == "LABORATORIO")["semRegras"])
        self.assertFalse(next(row for row in m["linhas"] if row["rotulo"] == "CAMARA_FRIGORIFICA")["plausivel"])
        self.assertEqual([r["id"] for r in vm["propriedade"]["rp"]], ["RP-VALOR-FISICO"])
        self.assertEqual({d["nome"] for d in vm["dimensoes"] if d["rp"]}, {"tipoDispositivo", "unidadeMedida", "ambiente"})

    def test_tree_coverage(self):
        vm = build(self.g, "decisao", alvo="USM:Medicao.valor", filtro={"tipoDispositivo": "TEMPERATURA", "unidadeMedida": "°C"})
        uncovered = vm["arvore"]["cobertura"]["naoCobertos"]
        self.assertTrue(any(a <= 70 <= b for a, b in uncovered))        # 70 °C is not covered (thesis)

    def test_hlm_model(self):
        vm = build(self.g, "modelo", nivel="HLM", nome="Dispositivo")
        self.assertEqual([b["nome"] for b in vm["blocos"]], ["Identificacao", "Leitura", "Localizacao", "Diagnostico"])
        self.assertEqual({p["nome"] for p in vm["projecoes"]}, {"DispositivoTeste", "DispositivoProducao"})
        self.assertNotIn("usadoPor", vm)

    def test_model_with_rules(self):
        vm = build(self.g, "modelo", nivel="HLM", nome="Fatura", regras=True)
        self.assertGreater(vm["contagem"]["RP"], 10)
        for card in (f for f in vm["regras"] if f["tipo"] == "RIC"):
            self.assertTrue(card["condicao"] and card["mensagem"] and card["conclusao"]["valor"])

    def test_specific_model_address(self):
        vm = build(self.g, "modelo", nivel="USM", nome="Morada", regras=True)
        self.assertEqual(len(vm["usadoPor"]["caminhos"]), 5)
        self.assertEqual(vm["usadoPor"]["hlm"], ["Dispositivo", "Fatura", "OrdemInstalacao"])

    def test_dependencies_by_value(self):
        vm = build(self.g, "dependencias", propriedade="SM:Identificacao.tipoDispositivo")
        by_value = {v["valor"]: v for v in vm["valores"]}
        self.assertEqual(set(by_value), {"TEMPERATURA", "HUMIDADE", "PRESSAO", "VELOCIDADE"})
        self.assertIn("RIR-TEMP-REFRIG-CELSIUS", by_value["TEMPERATURA"]["regras"])
        self.assertNotIn("RIR-TEMP-REFRIG-CELSIUS", by_value["HUMIDADE"]["regras"])
        card = next(x for x in vm["regras"] if x["id"] == "RIR-TEMP-REFRIG-CELSIUS")
        self.assertEqual([t["foco"] for t in card["condicao"]], [True, False, False])

    def test_rule_chain_up_to_the_hlm(self):
        vm = build(self.g, "regra", id="RP-PAIS")
        self.assertEqual({n["nome"] for n in vm["subgrafoModelos"]["nos"] if n["rotulo"] == "HLM"}, {"Dispositivo", "Fatura", "OrdemInstalacao"})
        vm = build(self.g, "regra", id="RP-IDENT")
        self.assertEqual([n["chave"] for n in vm["subgrafoModelos"]["nos"]],
                         ["Propriedade:SM:Identificacao.identificador", "SM:Identificacao", "HLM:Dispositivo"])

    def test_profile_static_selection(self):
        vm = build(self.g, "perfil", perfil="RefrigeracaoLote")
        state = {(row["regra"], row["ocorrencia"]): row["estado"] for row in vm["regras"]}
        self.assertEqual(state[("RIR-TEMP-REFRIG-CELSIUS", "")], "sempre aplicável")
        self.assertEqual(state[("RIR-TEMP-ESTUFA-CELSIUS", "")], "nunca aplicável")

    def test_profile_outside_projection(self):
        vm = build(self.g, "perfil", perfil="TesteLaboratorio")
        self.assertEqual({row["regra"]: row["estado"] for row in vm["regras"]}["RIR-TEMP-REFRIG-CELSIUS"], "não avaliável")

    def test_impact(self):
        vm = build(self.g, "impacto", propriedade="SM:Identificacao.tipoDispositivo")
        self.assertEqual(vm["contagem"]["RP"], 1)
        self.assertGreater(vm["contagem"]["RIR"], 30)

    def test_static_site_has_no_broken_links(self):
        with tempfile.TemporaryDirectory() as d:
            done = generate(self.g, d)
            self.assertGreater(len(done), 200)
            pages = {entry.page for entry, _ in done} | {"index"}
            for entry, _ in done:
                json.loads((Path(d) / f"{entry.page}.json").read_text(encoding="utf-8"))
                self.assertTrue((Path(d) / f"{entry.page}.html").exists())
            for f in Path(d).glob("*.html"):
                for target in re.findall(r'href="([A-Za-z0-9_\-]+)\.(?:html|json)', f.read_text(encoding="utf-8")):
                    self.assertIn(target, pages, f"{f.name} → {target}")

    def test_every_viewmodel_has_its_cypher(self):
        for name, entry in REGISTRY.items():
            self.assertTrue(statements(entry["cypher"]), name)


@unittest.skipUnless(os.environ.get("NEO4J_URI"), "defina NEO4J_URI (e NEO4J_USER, NEO4J_PASSWORD) para testar com Neo4j")
class TestNeo4j(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from ecv.graph.neo4j_store import connect
        cls.driver = connect(config.neo4j_setting("uri"), config.neo4j_setting("utilizador"), config.neo4j_setting("senha"))

    @classmethod
    def tearDownClass(cls):
        cls.driver.close()

    def test_incremental_ingestion_and_same_viewmodels(self):
        from ecv.graph.neo4j_store import Neo4jGraph
        from ecv.ingestion import ingest_neo4j
        first = ingest_neo4j(EXAMPLES, self.driver, clear=True)
        self.assertTrue(all(r.accepted for r in first))
        self.assertGreater(len(first[1].plan.reused), 50)         # the invoice reuses what the device brought
        second = ingest_neo4j(EXAMPLES, self.driver)                # again: nothing new
        self.assertTrue(all(not r.plan.new_nodes and not r.plan.new_edges for r in second))
        g, gn = graph(), Neo4jGraph(self.driver)
        self.assertEqual(len(gn.nodes("Regra")), len(g.nodes("Regra")))
        for name, params in [("modelo", {"nivel": "HLM", "nome": "Fatura", "regras": True}), ("modelo", {"nivel": "USM", "nome": "Morada"}),
                             ("decisao", {"alvo": "USM:Medicao.valor"}), ("dependencias", {"propriedade": "SM:Identificacao.tipoDispositivo"}),
                             ("perfil", {"perfil": "RefrigeracaoLote"}), ("regra", {"id": "RIR-LX-LOCALIDADE"}), ("regra", {"id": "RP-SOMA"})]:
            a = json.dumps(build(g, name, **params), sort_keys=True, ensure_ascii=False)
            b = json.dumps(build(gn, name, **params), sort_keys=True, ensure_ascii=False)
            self.assertEqual(a, b, (name, params))

    def test_cypher_queries_run(self):
        from ecv.views.viewmodels.cypher_runner import run
        params = {"hlm": "Dispositivo", "nivel": "USM", "nome": "Morada", "alvo": "USM:Medicao.valor", "id": "RIR-TEMP-REFRIG-CELSIUS",
                  "propriedade": "SM:Identificacao.tipoDispositivo", "perfil": "RefrigeracaoLote",
                  "alvos": ["USM:Medicao.valor"], "projecoes": None}
        for f in sorted({r["cypher"] for r in REGISTRY.values()} | {"regras_modelo.cypher"}):
            self.assertTrue(any(run(self.driver, f, **params)), f)

    def test_database_backend_neo4j(self):
        from ecv.graph.database import GraphDatabase, Scope
        db = GraphDatabase("neo4j")
        db.use(Scope("exemplos", "Exemplos", config.example_declarations))
        self.assertEqual(db.status()["nos"]["HLM"], 3)
        self.assertEqual(build(db.graph, "modelo", nivel="USM", nome="Morada"), build(graph(), "modelo", nivel="USM", nome="Morada"))
        db.close()


if __name__ == "__main__":
    unittest.main()
