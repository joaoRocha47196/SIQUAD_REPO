"""The web application: every tab and the whole cycle of a domain through HTTP (steps, changes, CSV, functions)."""
import json
import re
import unittest

from ecv.validation import functions
from ecv.validation.function_requests import FUNCTIONS_FOLDER

from .support import FIXTURES, TemporaryWorkspace, TestServer


class TestExampleScope(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = TestServer()

    @classmethod
    def tearDownClass(cls):
        cls.server.close()

    def test_every_tab_answers(self):
        for path in ("/", "/rotas", "/vistas", "/base", "/pesquisa?q=morada", "/pesquisa?p=rua,codigoPostal", "/validacao",
                     "/funcoes", "/pedidos", "/registo"):
            status, _, _ = self.server.request(path)
            self.assertEqual(status, 200, path)

    def test_domain_tabs_ask_for_a_domain(self):
        status, text, _ = self.server.request("/inventario")
        self.assertEqual(status, 400)
        self.assertIn("escolha um domínio", text)

    def test_unknown_path_is_404_and_logged(self):
        status, _, _ = self.server.request("/nao-existe")
        self.assertEqual(status, 404)
        self.assertTrue(any(e["path"] == "/nao-existe" and e["status"] == 404 for e in self.server.app.log.recent()))

    def test_every_view_of_the_catalogue_renders(self):
        _, catalogue = self.server.json("/api/vistas")
        self.assertGreater(len(catalogue), 100)
        for page in catalogue:
            status, _, _ = self.server.request(f"/vistas/{page}.html")
            self.assertEqual(status, 200, page)

    def test_viewmodel_api_matches_build(self):
        status, vm = self.server.json("/api/vm/hlm_Fatura")
        self.assertEqual(status, 200)
        status, built = self.server.json("/api/vm", {"viewmodel": "modelo", "parametros": {"nivel": "HLM", "nome": "Fatura"}})
        self.assertEqual(vm, built)

    def test_views_link_only_to_existing_pages(self):
        _, catalogue = self.server.json("/api/vistas")
        _, text, _ = self.server.request("/vistas/hlm_Fatura.html")
        for href in re.findall(r'href="([^"#?/:]+)\.html', text):
            self.assertIn(href, catalogue)

    def test_validation_form_and_api(self):
        status, vm = self.server.json("/api/validar", {"exemplo": "fatura_simplificada_valida"})
        self.assertEqual(status, 200)
        self.assertEqual(vm["vista"], "validacao")
        status, text, _ = self.server.request("/validacao", {"cenario": "hlm:Fatura", "instancia": "{}", "contextos": "{}"})
        self.assertEqual(status, 200)

    def test_merge_preview_does_not_write(self):
        before = self.server.app.database.version
        from ecv import config
        data = config.example_declarations()[0].read_text(encoding="utf-8")
        status, text, _ = self.server.request("/base/fusao", {"declaracao": data})
        self.assertEqual(status, 200)
        self.assertIn("reutilizados", text)
        self.assertEqual(self.server.app.database.version, before)


class TestDomainCycle(unittest.TestCase):
    """Phase 0 accepted -> generation by one request and response -> accepted -> review layers: changes by operations,
    CSV and natural language with information from another source -> function implementation request."""

    @classmethod
    def setUpClass(cls):
        cls.workspace = TemporaryWorkspace("iot").__enter__()
        cls.server = TestServer(scope="iot")

    @classmethod
    def tearDownClass(cls):
        cls.server.close()
        cls.workspace.__exit__(None, None, None)

    def _path(self, url):
        return url.split(self.server.base, 1)[1]

    def test_cycle(self):
        status, text, _ = self.server.request("/inventario?fonte=sdm-device")
        self.assertEqual(status, 200)
        self.assertIn("Elementos (146)", text)

        # the review layers do not prepare requests: only the generation does
        status, text, _ = self.server.request("/declaracao/preparar", {"passo": "A"})
        self.assertEqual(status, 400)

        # generation: one request with the whole inventory; the response creates the declarations
        status, _, url = self.server.request("/declaracao/preparar", {"passo": "G"})
        self.assertRegex(url, r"/pedidos/iot/\d{3}-passo-G$")
        request_url = self._path(url)
        _, prompt, _ = self.server.request(request_url + "/prompt.md")
        self.assertIn("# Especificação da ECV (versão para o LLM)", prompt)
        self.assertIn("Regras (64)", prompt)                                 # the inventory rules are in the same prompt
        self.assertNotIn("{{", prompt)
        response = (FIXTURES / "iot" / "G_resposta.json").read_text(encoding="utf-8")
        self.server.request(request_url + "/resposta", {"resposta": response})
        status, text, _ = self.server.request(request_url + "/registar", {})
        self.assertIn("Aplicado", text)
        # right after the generation (no step accepted), the views of one declaration
        status, text, _ = self.server.request("/vistas?ambito=iot::camara.ecv.json")
        self.assertEqual(status, 200)
        self.assertIn("Declaração camara.ecv.json", text)
        _, catalogue = self.server.json("/api/vistas")
        self.assertIn("hlm_Camara", catalogue)
        self.assertNotIn("hlm_DispositivoIot", catalogue)
        self.assertEqual(self.server.request("/vistas/hlm_Camara.html")[0], 200)
        self.server.request("/vistas?ambito=iot")
        _, db = self.server.json("/api/base")
        self.assertEqual(len(db["declaracoes"]), 11)
        self.assertEqual(db["rejeitadas"], 0)
        for step in ("G", "A"):
            self.server.request("/declaracao/aceitar", {"passo": step})
        _, steps = self.server.json("/api/declaracao")
        self.assertEqual((steps["passos"]["G"]["estado"], steps["passos"]["A"]["estado"]), ("aceite", "aceite"))

        # review of layer D: a rule written as an operation (preview writes nothing, apply writes)
        operation = {"op": "adicionar_regra", "onde": {"nivel": "SM", "modelo": "LeituraMedicao"},
                     "regra": {"id": "RIR-UNIDADE-HUMIDADE", "natureza": "inferencia_restritiva",
                               "condicao": [{"propriedade": "tipoMedicao", "operador": "EQUALS", "valor": "HUMIDADE"}],
                               "restricao": {"propriedade": "Medicao.unidadeMedida", "operador": "IN", "valor": ["%"],
                                             "mensagem": "A humidade mede-se em %."}}}
        ops = json.dumps({"operacoes": [operation]})
        status, text, _ = self.server.request("/alteracoes?camada=D&op=adicionar_regra&modelo=SM:LeituraMedicao")
        self.assertIn("Operação adicionar_regra", text)                      # the guided form
        self.assertIn("Construir a regra", text)                             # the rule builder: type, condition, restriction or conclusion
        self.assertIn("Medicao.unidadeMedida", text)                          # the paths the model reaches through its composition
        status, text, _ = self.server.request("/alteracoes/operacoes", {"operacoes": ops, "passo": "D", "acao": "previsualizar"})
        self.assertIn("Pré-visualização", text, text[text.find("msg-"):text.find("msg-") + 300])
        status, text, _ = self.server.request("/alteracoes/operacoes", {"operacoes": ops, "passo": "D", "acao": "aplicar"})
        self.assertIn("Operações aplicadas", text)
        _, steps = self.server.json("/api/declaracao")
        self.assertEqual(steps["passos"]["D"]["estado"], "em revisão")

        # a CSV of known mappings becomes RIR rules
        table = "tipoMedicao;unidadeMedida\nTEMPERATURA;°C|K|°F\nPRESSAO;hPa|bar"
        status, text, _ = self.server.request("/alteracoes/csv", {"tabela": table, "modelo": "SM:LeituraMedicao",
                                                                  "alvo": "unidadeMedida", "operador": "IN", "prefixo": "RIR-CSV",
                                                                  "passo": "D", "acao": "previsualizar"})
        self.assertIn("Operações geradas (2)", text)

        # natural language with information from another source -> a change request of the layer
        status, _, url = self.server.request("/alteracoes/pedido", {"texto": "Acrescenta as gamas desta tabela.", "passo": "C",
                                                                   "informacao": "unidade;minimo;maximo\n%;0;100"})
        self.assertRegex(url, r"/pedidos/iot/\d{3}-alteracao-C$")
        _, prompt, _ = self.server.request(self._path(url) + "/prompt.md")
        for fragment in ("adicionar_regra", "unidade;minimo;maximo", "C · Plausibilidade (RP)"):
            self.assertIn(fragment, prompt)

        # test instances: the skeleton comes from the structure; a request carries only the scenario's context
        status, text, _ = self.server.request("/instancias?cenario=hlm:Camara")
        self.assertEqual(status, 200)
        self.assertIn("Instância de teste (JSON)", text)
        status, _, url = self.server.request("/instancias/pedido", {"cenario": "hlm:Camara", "pedido": "Uma câmara válida", "nome": "camara_valida"})
        self.assertRegex(url, r"/pedidos/iot/\d{3}-instancia$")
        _, prompt, _ = self.server.request(self._path(url) + "/prompt.md")
        self.assertIn("## Estrutura", prompt)
        self.assertNotIn("Especificação da ECV", prompt)
        example = {"descricao": "teste", "hlm": "Camara", "instancia": {}}
        self.server.request(self._path(url) + "/resposta", {"resposta": json.dumps(example)})
        status, text, _ = self.server.request(self._path(url) + "/registar", {})
        self.assertIn("instância gravada", text)
        self.assertTrue((self.workspace.domain_folder / "instancias" / "camara_valida.json").exists())
        status, text, _ = self.server.request("/instancias/validar", {"nome": "camara_valida"})
        self.assertIn("Validação de camara_valida", text)
        _, text, _ = self.server.request("/validacao")                      # the saved test instances are offered in Validação
        self.assertIn("teste: camara_valida", text)

        # outputs of a declaration: the Cypher load and the static views
        status, text, _ = self.server.request("/declaracao/cypher/camara.ecv.json")
        self.assertEqual(status, 200)
        self.assertIn("CREATE CONSTRAINT", text)
        status, text, _ = self.server.request("/declaracao/estaticas", {"nome": "camara.ecv.json"})
        self.assertIn("vistas estáticas de camara.ecv.json", text)
        status, text, _ = self.server.request("/estaticas/iot/camara/index.html")
        self.assertEqual(status, 200)
        self.assertEqual(self.server.request("/estaticas/iot/camara/..%2Festado.json")[0], 404)
        # the projection helper rebuilds the JSON once the page is loaded (the textarea comes after the script)
        status, text, _ = self.server.request("/alteracoes?camada=B&op=definir_projecao&hlm=Camara")
        self.assertIn("DOMContentLoaded", text)
        self.assertNotIn("Pedido em linguagem natural", text)

        # every view of the domain renders
        _, catalogue = self.server.json("/api/vistas")
        for page in catalogue:
            status, _, _ = self.server.request(f"/vistas/{page}.html")
            self.assertEqual(status, 200, page)

    def test_new_domain_sources_and_adapters(self):
        from ecv.transformer import adapters
        text = (FIXTURES.parent.parent / "dados_teste" / "biblioteca" / "descricao_biblioteca.md").read_bytes()
        try:
            status, _, url = self.server.request("/declaracao/dominio", {"id": "biblioteca_teste", "nome": "Biblioteca"})
            self.assertIn("/declaracao", url)
            status, text_page, _ = self.server.upload("/declaracao/fonte", {"id": "descricao", "adaptador": "texto.markdown", "papel": "texto"},
                                                      [("ficheiro", "descricao.md", text)])
            self.assertIn("Fonte descricao gravada", text_page)
            self.assertTrue((self.workspace.root / "dominios" / "biblioteca_teste" / "fontes" / "descricao.md").exists())
            status, text_page, _ = self.server.request("/declaracao/extrair", {})
            self.assertIn("1 inventário(s) escritos", text_page)
            _, inventory = self.server.json("/api/inventario?fonte=descricao")
            self.assertIn("Emprestimo", [g["id"] for g in inventory["grupos"]])
            # a format without an adapter: a request to the LLM, answered with a module that is installed
            status, _, url = self.server.request("/declaracao/adaptador", {"nome": "csv.teste", "descricao": "uma tabela"})
            self.assertRegex(url, r"/pedidos/global/\d{3}-adaptador$")
            code = ('from ..inventory import Group, Inventory\n\nNAME = "csv.teste"\nDESCRIPTION = "teste"\n\n\n'
                    'def adapt(path):\n    return Inventory({"nome": "t", "tipo": "csv"}, [Group("G", "G")])\n')
            self.server.request(self._path(url) + "/resposta", {"resposta": code})
            status, text_page, _ = self.server.request(self._path(url) + "/registar", {})
            self.assertIn("Aplicado", text_page)
            self.assertIn("csv.teste", adapters.ADAPTERS)
        finally:
            (adapters.FOLDER / "a_csv_teste.py").unlink(missing_ok=True)
            adapters.load(reload=True)
            self.server.app.use_scope("iot")

    def test_function_implementation_request(self):
        self.server.app.use_scope("exemplos")
        try:
            status, _, url = self.server.request("/funcoes/pedir", {"nome": "dentroDe"})
            self.assertRegex(url, r"/pedidos/global/\d{3}-funcao$")
            request_url = url.split(self.server.base, 1)[1]
            _, prompt, _ = self.server.request(request_url + "/prompt.md")
            self.assertIn('"nome": "dentroDe"', prompt)
            code = ('from ecv.validation.functions import implements\n\n\n@implements("dentroDe")\n'
                    'def within(value, minimum, maximum, *, contexts):\n    """Teste."""\n    return minimum <= value <= maximum\n')
            self.server.request(request_url + "/resposta", {"resposta": code})
            status, text, _ = self.server.request(request_url + "/registar", {})
            self.assertIn("Aplicado", text)
            self.assertEqual(functions.SOURCES["dentroDe"], "f_dentro_de")
        finally:
            (FUNCTIONS_FOLDER / "f_dentro_de.py").unlink(missing_ok=True)
            functions.load(reload=True)
            self.server.app.use_scope("iot")


if __name__ == "__main__":
    unittest.main()
