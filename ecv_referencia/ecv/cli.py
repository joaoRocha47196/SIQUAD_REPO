"""Command line: the same operations as the web application, for scripts and tests.

    python -m ecv servidor [--neo4j] [--ambito <dominio>] [--porta N]     the web application
    python -m ecv verificar [decl ...]                                    specs and invariants of each declaration
    python -m ecv descricoes <decl> [--escrever]                          derive the rule descriptions
    python -m ecv grafo [decl ...] [--cypher saida.cypher]                ingest in memory; conformance; Cypher script
    python -m ecv importar [decl ...] [--limpar]                          ingest into Neo4j (only what is new)
    python -m ecv vm <viewmodel> [decl ...] [k=v ...] [--neo4j]           a ViewModel as JSON
    python -m ecv cypher <consulta> [k=v ...]                             the equivalent Cypher query, in Neo4j
    python -m ecv vistas [decl ...] [-o pasta]                            the static views (HTML + JSON)
    python -m ecv validar <instancia.json | exemplo> [--perfil P | --hlm H] [--contexto k=v ...]
    python -m ecv specs [--verificar]                                     write (or check) the internal specification
    python -m ecv inventario extrair|aceitar <dominio>                    phase 0
    python -m ecv passo preparar|registar <dominio> G [pedido]                  the generation (phase G)
    python -m ecv passo verificar|aceitar <dominio> <G|A..F>               checks and acceptance
    python -m ecv pedidos listar [<dominio>|global] | responder <fila> <pedido> <ficheiro>
    python -m ecv alteracoes pedir <dominio> <texto.md> [--passo A..F] [--informacao ficheiro] | aplicar <dominio> <operacoes.json> [--passo P] [--ver]
    python -m ecv funcoes listar | pedir <nome> | registar <pedido>
    python -m ecv docs                                                    fill the generated blocks of the Markdown files
    python -m ecv documentacao [--saida pasta]                            the documentation site (documentacao/site/)

Without declarations, the commands use the example declarations (specs/exemplos), in order.
Neo4j credentials: config (ecv/config/ecv.config.json) or NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD, NEO4J_DATABASE.
"""
import argparse
import json
import sys
from pathlib import Path

from ecv import config
from ecv.shared.errors import EcvError, StepError


def _declarations(items):
    return [Path(x) for x in items] if items else config.example_declarations()


def _split(items):
    """Positional arguments: declaration files and 'k=v' parameters (values as JSON when they parse)."""
    files, params = [], {}
    for x in items:
        if "=" in x and not x.endswith(".json"):
            k, _, v = x.partition("=")
            try:
                params[k] = json.loads(v)
            except ValueError:
                params[k] = v
        else:
            files.append(x)
    return files, params


def _driver():
    from ecv.graph.neo4j_store import connect
    return connect(config.neo4j_setting("uri"), config.neo4j_setting("utilizador"), config.neo4j_setting("senha"))


def _graph(args, files):
    if getattr(args, "neo4j", False):
        from ecv.graph.neo4j_store import Neo4jGraph
        return Neo4jGraph(_driver(), config.neo4j_setting("base"))
    from ecv.ingestion import ingest
    return ingest(_declarations(files)).graph


def _print_json(data):
    print(json.dumps(data, ensure_ascii=False, indent=1, default=str))


def _domain(name):
    from ecv.shared.workspace import Workspace
    return Workspace().domain(name)


# ---------------------------------------------------------------------- declarations, graph, views
def cmd_verificar(args):
    from ecv.ingestion import Declaration, verify
    errors = 0
    for f in _declarations(args.declaracoes):
        report = verify(Declaration.load(f))
        print(f"== {Path(f).name}: {report.summary()}")
        for p in report.problems:
            print("  ", p)
        errors += len(report.errors)
    return 1 if errors else 0


def cmd_descricoes(args):
    from ecv.ingestion import Declaration, derive
    from ecv.shared.json_format import dumps
    decl = Declaration.load(args.declaracao)
    changed = 0
    for site in decl.rules():
        new = derive(site.rule, site.level, site.model)
        if site.rule.get("descricao") != new:
            print(f"{site.id}: {new}")
            site.rule["descricao"] = new
            changed += 1
    if args.escrever and changed:
        Path(args.declaracao).write_text(dumps(decl.data), encoding="utf-8")
    print(f"{changed} descrição(ões) {'atualizada(s)' if args.escrever else 'a atualizar'}")
    return 0


def cmd_grafo(args):
    from ecv.graph.cypher_export import export
    from ecv.graph.model import conformance
    from ecv.ingestion import ingest
    files = _declarations(args.declaracoes)
    ingestion = ingest(files)
    for r in ingestion.results:
        print(r.summary())
    nodes, edges = ingestion.graph.counts()
    print("nós:", nodes)
    print("arestas:", edges)
    problems = conformance(ingestion.graph)
    print(f"conformidade com o modelo do grafo: {len(problems)} desvio(s)")
    for p in problems:
        print("  ", p)
    if args.cypher:
        Path(args.cypher).parent.mkdir(parents=True, exist_ok=True)
        Path(args.cypher).write_text(export(ingestion.graph, ", ".join(Path(f).name for f in files)), encoding="utf-8")
        print("Cypher escrito em", args.cypher)
    return 0 if ingestion.valid and not problems else 1


def cmd_importar(args):
    from ecv.ingestion import ingest_neo4j
    driver = _driver()
    results = ingest_neo4j(_declarations(args.declaracoes), driver, config.neo4j_setting("base"), clear=args.limpar)
    for r in results:
        print(r.summary())
    driver.close()
    return 0 if all(r.accepted for r in results) else 1


def cmd_vm(args):
    from ecv.views.viewmodels import build
    files, params = _split(args.argumentos)
    _print_json(build(_graph(args, files), args.nome, **params))
    return 0


def cmd_cypher(args):
    from ecv.views.viewmodels.cypher_runner import run
    _, params = _split(args.parametros)
    name = args.nome if args.nome.endswith(".cypher") else args.nome + ".cypher"
    _print_json(run(_driver(), name, config.neo4j_setting("base"), **params))
    return 0


def cmd_vistas(args):
    from ecv.views.static_site import generate
    folder = Path(args.saida or config.path("saidaVistas"))
    files = _declarations(args.declaracoes)
    done = generate(_graph(args, args.declaracoes), folder, origin=", ".join(Path(f).name for f in files))
    print(f"{len(done)} vistas em {folder}")
    return 0


def cmd_validar(args):
    from ecv import validation
    g = _graph(args, args.declaracoes)
    _, contexts = _split(args.contexto or [])
    path = Path(args.instancia)
    if not path.exists() and args.instancia in validation.examples():
        vm = validation.validate_example(g, args.instancia, contexts)
    else:
        data = json.loads(path.read_text(encoding="utf-8"))
        if "instancia" in data:
            contexts = {**data.get("contextos", {}), **contexts}
            args.perfil, args.hlm = args.perfil or data.get("perfil"), args.hlm or data.get("hlm")
            data = data["instancia"]
        vm = validation.validate(g, data, profile=args.perfil, hlm=args.hlm, contexts=contexts, name=path.stem)
    _print_json(vm)
    return 0 if vm["valida"] else 1


def cmd_specs(args):
    from ecv.ecv_builder import specs_bundle
    if args.verificar:
        current = specs_bundle.is_current()
        print("a especificação interna está atualizada" if current else "a especificação interna está desatualizada: python -m ecv specs")
        return 0 if current else 1
    path, size = specs_bundle.write()
    print(f"{path} ({size} caracteres)")
    return 0


# ---------------------------------------------------------------------- domains, steps, requests
def cmd_inventario(args):
    from ecv import ecv_builder, transformer
    domain = _domain(args.dominio)
    if args.acao == "extrair":
        for line in transformer.extract(domain):
            print(line)
    else:
        ecv_builder.accept_step(domain, "0")
        print("fase 0 aceite")
    return 0


def _print_check(check):
    print(check.text())
    return 0 if check.valid else 1


def cmd_passo(args):
    from ecv import ecv_builder
    from ecv.shared.llm_requests import RequestQueue
    domain = _domain(args.dominio)
    if args.acao == "preparar":
        if args.passo != "G":
            raise StepError("os passos A a F são de revisão: use python -m ecv alteracoes pedir|aplicar")
        r = ecv_builder.prepare_generation(domain)
        print(f"pedido {r.id}: {r.prompt_file} ({r.meta['tamanho']['caracteres']} caracteres)")
        print(f"resposta esperada em {r.response_file}")
        return 0
    if args.acao == "registar":
        queue = RequestQueue.for_domain(domain)
        request = queue.get(args.pedido) if args.pedido else next(
            r for r in reversed(queue.requests()) if r.kind == "passo" and r.step == args.passo)
        done, check = ecv_builder.register_response(domain, request)
        print("\n".join(done))
        return _print_check(check)
    if args.acao == "verificar":
        return _print_check(ecv_builder.verify_step(domain, args.passo))
    check = ecv_builder.accept_step(domain, args.passo)
    print(f"passo {args.passo} aceite" + (f": {check.summary()}" if check else ""))
    return 0


def _queue(name):
    from ecv.shared.llm_requests import RequestQueue
    return RequestQueue.global_queue() if name == "global" else RequestQueue.for_domain(_domain(name))


def cmd_pedidos(args):
    if args.acao == "listar":
        from ecv.shared.workspace import Workspace
        names = [args.fila] if args.fila else Workspace().domain_ids() + ["global"]
        for name in names:
            for r in _queue(name).requests():
                print(f"{name:12} {r.id:24} {r.state:10} {r.title}")
        return 0
    request = _queue(args.fila).get(args.pedido)
    request.save_response(Path(args.ficheiro).read_text(encoding="utf-8"))
    print(f"resposta guardada em {request.response_file}")
    return 0


def cmd_alteracoes(args):
    from ecv import ecv_builder
    from ecv.amendments import parse_operations
    domain = _domain(args.dominio)
    if args.acao == "pedir":
        extra = Path(args.informacao).read_text(encoding="utf-8") if args.informacao else ""
        r = ecv_builder.request_changes(domain, Path(args.ficheiro).read_text(encoding="utf-8"), args.passo, extra)
        print(f"pedido {r.id}: {r.prompt_file}")
        return 0
    ops = parse_operations(json.loads(Path(args.ficheiro).read_text(encoding="utf-8")))
    done, check = ecv_builder.apply_operations_to_domain(domain, ops, args.passo, save=not args.ver)
    print("\n".join(done))
    return _print_check(check) if check else 0


def cmd_funcoes(args):
    from ecv.validation import function_requests as F
    g = _graph(args, [])
    if args.acao == "listar":
        for f in F.declared_functions(g):
            print(f"{f['nome']:28} {'implementada (' + f['modulo'] + ')' if f['implementada'] else 'sem implementação'}")
        return 0
    if args.acao == "pedir":
        r = F.request_implementation(g, args.nome)
        print(f"pedido {r.id}: {r.prompt_file}")
        return 0
    print(F.register_implementation(_queue("global").get(args.nome))["resumo"])
    return 0


def cmd_docs(args):
    from ecv.tools.readme_blocks import update
    for f in update():
        print("atualizado:", f)
    return 0


def cmd_documentacao(args):
    from ecv.tools.documentation import generate
    folder, n = generate(args.saida)
    print(f"{n} páginas em {folder}")
    return 0


def cmd_servidor(args):
    from ecv.webapp import make_app, serve
    app = make_app("neo4j" if args.neo4j else "memoria", args.ambito)
    serve(app, args.endereco, args.porta)
    return 0


# ---------------------------------------------------------------------- parser
def build_parser():
    parser = argparse.ArgumentParser(prog="python -m ecv", description="ECV de referência")
    sub = parser.add_subparsers(dest="comando", required=True)

    def add(name, fn, help_text):
        p = sub.add_parser(name, help=help_text)
        p.set_defaults(f=fn)
        return p

    p = add("verificar", cmd_verificar, "specs e invariantes de cada declaração")
    p.add_argument("declaracoes", nargs="*")
    p = add("descricoes", cmd_descricoes, "deriva as descrições das regras")
    p.add_argument("declaracao")
    p.add_argument("--escrever", action="store_true")
    p = add("grafo", cmd_grafo, "ingere em memória, conformidade, exporta Cypher")
    p.add_argument("declaracoes", nargs="*")
    p.add_argument("--cypher")
    p = add("importar", cmd_importar, "ingere no Neo4j (só o que é novo)")
    p.add_argument("declaracoes", nargs="*")
    p.add_argument("--limpar", action="store_true")
    p = add("vm", cmd_vm, "um ViewModel em JSON")
    p.add_argument("nome")
    p.add_argument("argumentos", nargs="*")
    p.add_argument("--neo4j", action="store_true")
    p = add("cypher", cmd_cypher, "a consulta Cypher equivalente a um ViewModel, no Neo4j")
    p.add_argument("nome")
    p.add_argument("parametros", nargs="*")
    p = add("vistas", cmd_vistas, "as vistas estáticas (HTML + JSON)")
    p.add_argument("declaracoes", nargs="*")
    p.add_argument("-o", "--saida")
    p.add_argument("--neo4j", action="store_true")
    p = add("validar", cmd_validar, "valida uma instância contra as regras")
    p.add_argument("instancia")
    p.add_argument("declaracoes", nargs="*")
    p.add_argument("--perfil")
    p.add_argument("--hlm")
    p.add_argument("--contexto", nargs="*")
    p.add_argument("--neo4j", action="store_true")
    p = add("specs", cmd_specs, "escreve (ou verifica) a especificação interna para o LLM")
    p.add_argument("--verificar", action="store_true")
    p = add("inventario", cmd_inventario, "fase 0 de um domínio")
    p.add_argument("acao", choices=["extrair", "aceitar"])
    p.add_argument("dominio")
    p = add("passo", cmd_passo, "a geração (G) e a revisão por camadas (A a F)")
    p.add_argument("acao", choices=["preparar", "registar", "verificar", "aceitar"])
    p.add_argument("dominio")
    p.add_argument("passo")
    p.add_argument("pedido", nargs="?")
    p = add("pedidos", cmd_pedidos, "pedidos ao LLM")
    p.add_argument("acao", choices=["listar", "responder"])
    p.add_argument("fila", nargs="?")
    p.add_argument("pedido", nargs="?")
    p.add_argument("ficheiro", nargs="?")
    p = add("alteracoes", cmd_alteracoes, "alterações a um domínio")
    p.add_argument("acao", choices=["pedir", "aplicar"])
    p.add_argument("dominio")
    p.add_argument("ficheiro")
    p.add_argument("--passo")
    p.add_argument("--informacao", help="ficheiro com informação de outra fonte (pedir)")
    p.add_argument("--ver", action="store_true", help="só pré-visualizar")
    p = add("funcoes", cmd_funcoes, "funções declaradas e implementações")
    p.add_argument("acao", choices=["listar", "pedir", "registar"])
    p.add_argument("nome", nargs="?", help="nome da função (pedir) ou id do pedido (registar)")
    p.add_argument("--neo4j", action="store_true")
    add("docs", cmd_docs, "preenche os blocos gerados dos ficheiros Markdown")
    p = add("documentacao", cmd_documentacao, "gera a documentação técnica (documentacao/site/)")
    p.add_argument("--saida")
    p = add("servidor", cmd_servidor, "a aplicação web")
    p.add_argument("--neo4j", action="store_true")
    p.add_argument("--ambito", default="exemplos")
    p.add_argument("--endereco")
    p.add_argument("--porta", type=int)
    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)
    try:
        return args.f(args)
    except EcvError as e:
        print(f"erro: {e}", file=sys.stderr)
        return 2
