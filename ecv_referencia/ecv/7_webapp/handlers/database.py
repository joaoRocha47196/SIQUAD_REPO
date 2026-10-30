"""Base de dados (modules 3 and 4): what the web application queries.

The declaration files are the source of truth. The database is the graph of the active scope: the files
ingested (module 3) into memory or into Neo4j (module 4). It is rebuilt when a file of the scope changes;
nothing written here changes the files (a declaration becomes permanent only through the steps or the
amendments of a domain).
"""
import json

from ecv.ecv_builder import search

from ..http import Response
from ..pages import layout
from ..pages.components import button_form, e, field, keyvalues, message, pre, section, table, textarea, where_box

LEVEL_ORDER = ("HLM", "SM", "USM", "Propriedade", "RP", "RIR", "RIC", "Restricao", "CondicaoAplicabilidade", "Funcao",
               "ContextoExterno", "Projecao", "Perfil", "Declaracao")


def _counts_table(counts, order=()):
    keys = [k for k in order if k in counts] + sorted(k for k in counts if k not in order)
    return table(["", "Quantidade"], [[e(k), str(counts[k])] for k in keys])


def page(app, request, extra=""):
    s = app.database.status()
    where = (f'Neo4j · <code>{e(s["neo4j"]["uri"])}</code> · base {e(s["neo4j"]["base"] or "(predefinida)")}'
             if s["backend"] == "neo4j" else "memória do servidor")
    body = message(request.get("aviso"), "ok") + extra
    body += section("Estado", keyvalues([("Backend", where), ("Âmbito", e(s["tituloAmbito"])), ("Versão", str(s["versao"])),
                                         ("Construída", f'{e(s["construido"])} ({s["segundos"]} s)'),
                                         ("Ficheiros", str(len(s["ficheiros"])))])
                    + "<p>" + button_form("/base/reconstruir", "Reconstruir a partir dos ficheiros") + "</p>")
    body += section("Declarações ingeridas", table(["Origem", "Resultado"],
                    [[e(d["origem"]), ("✔ " if d["aceite"] else "✘ ") + f'<span class="mono">{e(d["resumo"])}</span>'] for d in s["declaracoes"]]))
    body += section("Nós", _counts_table(s["nos"], LEVEL_ORDER)) + section("Arestas", _counts_table(s["arestas"]))
    body += section("Pré-visualizar a fusão de uma declaração",
                    '<form method="post" action="/base/fusao">' + field("Declaração (JSON)", textarea("declaracao", "", 10))
                    + '<p><button>Pré-visualizar</button></p></form>'
                    + '<p class="note">Mostra o que a declaração acrescentaria ao grafo (nós novos, reutilizados, conflitos), sem escrever.</p>')
    body += where_box([('A ingestão (verificação, fusão, duplicados)', 'ecv/3_ingestion/'), ('O modelo do grafo', 'ecv/4_graph/graph_model.json'), ('A base de dados (memória ou Neo4j)', 'ecv/4_graph/'), ('A carga em Cypher', 'ecv/4_graph/cypher/'), ('As declarações ingeridas', 'dominios/<d>/declaracoes/*.ecv.json · specs/exemplos/'), ('A configuração do Neo4j', 'ecv/config/ecv.config.json (secção neo4j)'), ('Esta página', 'ecv/7_webapp/handlers/database.py')])
    return Response.html(layout.page(app, "base", "Base de dados", body, request.path,
                                     "Declarações (ficheiros) → ingestão → grafo integrado, sem duplicados → consultas das vistas, da validação e da pesquisa."))


def rebuild(app, request):
    app.database.refresh(force=True)
    app.log.event(f"base de dados reconstruída a pedido ({app.database.info.seconds} s)")
    return Response.redirect("/base?aviso=Base+de+dados+reconstru%C3%ADda", note="reconstruída")


def _plan_text(result):
    lines = [result.summary()]
    if not result.report.valid:
        lines += [str(p) for p in result.report.problems]
    if result.plan is not None:
        lines += ["", f"novos ({len(result.plan.new_nodes)}):"] + [f"  {n.id}" for n in result.plan.new_nodes[:300]]
        lines += ["", f"reutilizados ({len(result.plan.reused)}):"] + [f"  {x}" for x in result.plan.reused[:300]]
        for c in result.plan.conflicts:
            lines += ["", f"CONFLITO {c.node}: {c.reason}"] + [f"  {d}" for d in c.details]
    return "\n".join(lines)


def preview_merge(app, request):
    text = request.form().get("declaracao", "")
    try:
        data = json.loads(text)
    except ValueError as err:
        return page(app, request, message(f"JSON inválido: {err}", "error"))
    result = app.database.preview_merge(data, (data.get("declaracao") or {}).get("nome", "declaração colada"))
    return page(app, request, section("Resultado da pré-visualização", pre(_plan_text(result))))


def _search_graphs(app):
    graphs = [("âmbito ativo", app.graph)]
    if app.domain is not None:
        from ecv.ecv_builder.reference import reference_graph
        graphs.append(("referência", reference_graph(exclude=app.domain.id)))
    return graphs


def _node_link(r):
    label, name, key = r["rotulo"], r["nome"], r["chave"]
    if label in ("HLM", "SM", "USM"):
        return f'<a href="/vistas/{e(label.lower())}_{e(name)}.html">{e(name)}</a>'
    if label in ("RP", "RIR", "RIC"):
        return f'<a href="/vistas/regra_{e(key)}.html">{e(key)}</a>'
    return e(key or name)


def search_page(app, request):
    q, props = request.get("q", ""), request.get("p", "")
    body = (f'<form method="get"><input name="q" value="{e(q)}" size="50" placeholder="nome, nome alternativo ou descrição"> '
            '<button>Pesquisar</button></form>')
    if q:
        found = [{**r, "grafo": name} for name, g in _search_graphs(app) for r in search.search(g, q)]
        body += section(f"{len(found)} resultado(s) para «{q}»", table(["", "Grafo", "Tipo", "Entidade", "Onde", "Descrição"],
                        [["★" if r["exato"] else "", e(r["grafo"]), e(r["rotulo"]), _node_link(r) if r["grafo"] == "âmbito ativo" else e(r["chave"]),
                          e(r.get("dono") or ""), e(r.get("descricao"))] for r in found]))
    body += section("Modelos com propriedades semelhantes",
                    f'<form method="get"><input name="p" value="{e(props)}" size="70" placeholder="propriedades separadas por vírgulas (ex.: rua, codigoPostal, localidade)"> '
                    '<button>Procurar</button></form>')
    if props:
        wanted = [x.strip() for x in props.split(",") if x.strip()]
        found = sorted(({**r, "grafo": name} for name, g in _search_graphs(app) for r in search.similar_models(g, wanted, threshold=0.1)),
                       key=lambda r: -r["semelhanca"])
        body += table(["Semelhança", "Grafo", "Modelo", "Em comum", "Propriedades do modelo"],
                      [[f'{r["semelhanca"]:.2f}', e(r["grafo"]), f'{e(r["nivel"])} {e(r["nome"])}', e(", ".join(r["comuns"])),
                        e(", ".join(r["propriedades"]))] for r in found])
    return Response.html(layout.page(app, "base", "Pesquisa", body, request.path, "Antes de criar um modelo, confirmar se já existe."))


def status_api(app, request):
    return Response.json(app.database.status())


def search_api(app, request):
    return Response.json([{**r, "grafo": name} for name, g in _search_graphs(app) for r in search.search(g, request.get("q", ""))])


def similar_api(app, request):
    wanted = [x.strip() for x in request.get("p", "").split(",") if x.strip()]
    threshold = float(request.get("limiar", 0.3))
    return Response.json([{**r, "grafo": name} for name, g in _search_graphs(app) for r in search.similar_models(g, wanted, threshold=threshold)])
