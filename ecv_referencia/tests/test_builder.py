"""Module 1 and the exchange with the LLM: the generation and the review by layers on a small domain, the request
queue, the internal specification and the search used to reuse models."""
import json
import os
import shutil
import tempfile
import unittest
from pathlib import Path

from ecv import config, ecv_builder
from ecv.ecv_builder import search, specs_bundle
from ecv.ingestion import ingest
from ecv.shared.errors import RequestError, StepError
from ecv.shared.llm_requests import RequestQueue, _strip_fences
from ecv.shared.workspace import Workspace


class SmallDomain:
    """A domain 'teste' with one source of two elements and one rule, in a temporary folder of domains."""

    def __enter__(self):
        self.root = Path(tempfile.mkdtemp())
        self.saved = os.environ.get("ECV_CAMINHO_DOMINIOS")
        os.environ["ECV_CAMINHO_DOMINIOS"] = str(self.root)
        folder = self.root / "teste"
        (folder / "inventario").mkdir(parents=True)
        (folder / "dominio.json").write_text(json.dumps({"id": "teste", "nome": "Teste", "descricao": "Domínio de teste.",
                                                         "fontes": [], "utilizacoes": ["validar"], "cenarios": []}), encoding="utf-8")
        (folder / "inventario" / "f.json").write_text(json.dumps({
            "fonte": {"id": "f", "nome": "f"}, "grupos": [], "elementos": [{"id": "x1", "nome": "rua"}, {"id": "x2", "nome": "lixo"}],
            "regras": [{"id": "R1", "texto": "rua obrigatória", "categoria": "presenca"}]}), encoding="utf-8")
        return Workspace().domain("teste")

    def __exit__(self, *exc):
        if self.saved is None:
            os.environ.pop("ECV_CAMINHO_DOMINIOS", None)
        else:
            os.environ["ECV_CAMINHO_DOMINIOS"] = self.saved
        shutil.rmtree(self.root)


class TestGenerationAndReview(unittest.TestCase):
    def _generate(self, domain, mapping):
        ecv_builder.accept_step(domain, "0")
        request = ecv_builder.prepare_generation(domain)
        declaration = json.loads(config.example_declarations()[2].read_text(encoding="utf-8"))   # ordem_instalacao
        request.save_response("```json\n" + json.dumps({"declaracoes": [declaration], "mapeamento": mapping}) + "\n```")
        return request, ecv_builder.register_response(domain, request)

    def test_generation_prompt_has_everything(self):
        with SmallDomain() as domain:
            with self.assertRaises(StepError):
                ecv_builder.prepare_generation(domain)            # phase 0 not yet accepted
            ecv_builder.accept_step(domain, "0")
            prompt = ecv_builder.prepare_generation(domain).prompt()
            self.assertIn(specs_bundle.text().splitlines()[0], prompt)     # the internal specification, in full
            for layer in ("A · Estrutura (ECM)", "B · Projeções (RE)", "D · Inferência (RIR e RIC)", "F · Perfis de execução"):
                self.assertIn(layer, prompt)
            self.assertIn("rua obrigatória", prompt)                       # the inventory rules come with the elements
            self.assertNotIn("{{", prompt)
            self.assertEqual(domain.step_state("G"), "em curso")

    def test_generation_then_review_by_layers(self):
        with SmallDomain() as domain:
            mapping = [{"fonte": "f", "origem": "x1", "decisao": "mapeado", "destino": "HLM:OrdemInstalacao/Requerente.Morada.rua"}]
            request, (_, check) = self._generate(domain, mapping)
            self.assertEqual(request.state, "aplicado")
            self.assertEqual(sorted(check.extra["cobertura"]), ["f:R1", "f:x2"])
            self.assertTrue(check.valid)                                     # coverage does not block the generation
            ecv_builder.accept_step(domain, "G")
            with self.assertRaises(StepError):
                ecv_builder.accept_step(domain, "A")                         # layer A: x2 is neither mapped nor discarded
            _, check = ecv_builder.apply_operations_to_domain(domain, [
                {"op": "mapear", "fonte": "f", "origem": "x2", "decisao": "descartado", "motivo": "teste"}], "A")
            self.assertEqual(check.extra["cobertura"], [])
            ecv_builder.accept_step(domain, "A")
            self.assertEqual(Workspace().domain("teste").step_state("A"), "aceite")

    def test_change_request_carries_layer_and_other_source(self):
        with SmallDomain() as domain:
            self._generate(domain, [])
            ecv_builder.accept_step(domain, "G")
            change = ecv_builder.request_changes(domain, "Acrescenta as regras da tabela.", "B", "pais;obrigatorio\nPT;sim")
            prompt = change.prompt()
            self.assertIn("Acrescenta as regras da tabela.", prompt)
            self.assertIn("pais;obrigatorio", prompt)                       # information from another source
            self.assertIn("B · Projeções (RE)", prompt)                      # the layer's guidance
            self.assertIn("rua obrigatória", prompt)                         # the layer's uncovered inventory rule
            self.assertNotIn(specs_bundle.text().splitlines()[0], prompt)      # focused: no full specification
            self.assertIn("HLM OrdemInstalacao", prompt)                     # the index of names
            self.assertNotIn("{{", prompt)
            focused = ecv_builder.request_changes(domain, "Muda a mensagem.", "C", "", {"modelo": "USM:Morada", "propriedade": "pais"}).prompt()
            self.assertIn('"propriedade"', focused)                         # the chosen property, as it is in the declarations
            self.assertIn("RP-PAIS", focused)

    def test_rejected_response_writes_nothing(self):
        with SmallDomain() as domain:
            ecv_builder.accept_step(domain, "0")
            request = ecv_builder.prepare_generation(domain)
            request.save_response(json.dumps({"declaracoes": []}))
            with self.assertRaises(Exception):
                ecv_builder.register_response(domain, request)
            self.assertEqual(request.state, "rejeitado")
            self.assertEqual(domain.declaration_files(), [])


class TestRequestQueue(unittest.TestCase):
    def test_numbering_states_and_fences(self):
        with tempfile.TemporaryDirectory() as d:
            queue = RequestQueue(d)
            first = queue.create("passo", "Passo A", "prompt", step="A")
            second = queue.create("funcao", "Função", "prompt")
            self.assertEqual((first.id, second.id), ("001-passo-A", "002-funcao"))
            self.assertEqual(first.state, "pendente")
            (first.folder / "resposta.json").write_text("{}", encoding="utf-8")          # answered in the repository
            self.assertEqual(queue.get(first.id).state, "respondido")
            with self.assertRaises(RequestError):
                first.save_response("not json")
            second.save_response("def f():\n    return 1\n")
            self.assertEqual(second.response_file.name, "resposta.py")
        self.assertEqual(_strip_fences('```json\n{"a": 1}\n```'), '{"a": 1}')


class TestInternalSpecification(unittest.TestCase):
    def test_bundle_is_current(self):
        self.assertTrue(specs_bundle.is_current(), "python -m ecv specs")

    def test_bundle_has_no_presentation(self):
        text = specs_bundle.build()
        self.assertNotIn("```mermaid", text)
        self.assertNotIn("](", text)
        self.assertFalse(any(line.lstrip().startswith("|") for line in text.splitlines()))
        for section in ("## Vocabulário fechado", "## A declaração ECV", "## Modelos (ECM)", "## Regras (ECR)"):
            self.assertIn(section, text)


class TestSearch(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.g = ingest(config.example_declarations()).graph

    def test_search_and_similar_models(self):
        self.assertTrue(any(r["chave"] == "USM:Morada.codigoPostal" for r in search.search(self.g, "codigo postal")))
        self.assertEqual(search.similar_models(self.g, ["rua", "codigoPostal", "localidade", "pais"])[0]["nome"], "Morada")

    def test_existing_models_for_the_prompt(self):
        models = {(m["nivel"], m["nome"]): m for m in search.existing_models(self.g)}
        self.assertIn("RP-PAIS", models[("USM", "Morada")]["regrasQueVivemNele"])


if __name__ == "__main__":
    unittest.main()
