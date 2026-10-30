"""Inventário (module 0): the sources of the domain, phase 0 (extraction) and each inventory."""
from ecv import transformer

from ..http import Response, url
from ..pages.components import button_form, e, keyvalues, message, section, state, table, where_box
from ..pages import layout

MAX_ROWS = 2000


def _matches(item, q):
    return not q or q.lower() in " ".join(str(v) for v in item.values() if v).lower()


def _sources_table(domain, inventories):
    rows = []
    for s in domain.sources():
        inv = inventories.get(s["id"])
        counts = f'{len(inv["grupos"])} / {len(inv["elementos"])} / {len(inv["regras"])}' if inv else "—"
        rows.append([f'<a href="{url("/inventario", fonte=s["id"])}">{e(s["id"])}</a>' if inv else e(s["id"]),
                     f"<code>{e(s['adaptador'])}</code>", f"<code>{e(s['caminho'])}</code>", e(s.get("passoA", "principal")),
                     e(s.get("papel")), counts])
    return table(["Fonte", "Adaptador", "Caminho", "Papel na geração", "Descrição", "Grupos / elementos / regras"], rows)


def _phase0(domain):
    st = domain.step_state("0")
    summary = domain.state["passos"]["0"].get("resumo") or []
    actions = button_form("/inventario/extrair", "Extrair inventários", css="primary",
                          confirm="Reescreve os inventários do domínio a partir das fontes. Continuar?")
    if st == "em revisão":
        actions += button_form("/declaracao/aceitar", "Aceitar a fase 0", {"passo": "0", "voltar": "/inventario"})
    return keyvalues([("Estado", state(st)), ("Última extração", e(domain.state["passos"]["0"].get("atualizado") or "—"))]) \
        + ("<pre>" + e("\n".join(summary)) + "</pre>" if summary else "") + f"<p>{actions}</p>"


def _inventory_detail(source_id, inv, category, q):
    f = inv["fonte"]
    by_category = inv.get("contagens", {}).get("regrasPorCategoria", {})
    filters = " · ".join(f'<a href="{url("/inventario", fonte=source_id, categoria=c, q=q)}">{e(c)}</a> {n}' for c, n in by_category.items())
    out = keyvalues([("Fonte", e(f.get("nome"))), ("Tipo", e(f.get("tipo"))), ("Caminho", f'<code>{e(f.get("caminho"))}</code>'),
                     ("Extraído", e(f.get("extraido"))), ("Regras por categoria", filters or "—")])
    out += (f'<form method="get" action="/inventario"><input type="hidden" name="fonte" value="{e(source_id)}">'
            f'<input name="q" value="{e(q)}" size="40" placeholder="filtrar (id, nome, descrição, texto)"> <button>Filtrar</button></form>')
    groups = [g for g in inv["grupos"] if _matches(g, q)]
    if groups and not category:
        out += section(f"Grupos ({len(groups)})", table(["Id", "Nome", "Origem", "Pai", "Cardinalidade", "Elementos"],
                       [[e(g["id"]), e(g["nome"]), e(g.get("nomeOrigem")), e(g.get("pai")), e(g.get("cardinalidade")),
                         e(", ".join(g.get("elementos", [])[:30]))] for g in groups[:MAX_ROWS]]))
    elements = [x for x in inv["elementos"] if _matches(x, q)]
    if elements and not category:
        out += section(f"Elementos ({len(elements)})", table(["Id", "Nome", "Descrição", "Tipo", "Cardinalidade", "Grupo", "Nomes alternativos", "Valores admitidos"],
                       [[e(x["id"]), e(x.get("nome")), e(x.get("descricao")), e(f'{x.get("tipo") or ""} {x.get("tipoOrigem") or ""}'),
                         e(x.get("cardinalidade")), e(x.get("grupo")), e(", ".join(x.get("nomesAlternativos") or [])),
                         e(", ".join(map(str, x.get("valoresAdmitidos") or []))[:200])] for x in elements[:MAX_ROWS]]))
    rules = [r for r in inv["regras"] if (not category or r["categoria"] == category) and _matches(r, q)]
    if rules:
        out += section(f"Regras ({len(rules)}{' · ' + category if category else ''})",
                       table(["Id", "Texto", "Categoria", "Natureza provável", "Gravidade", "Contexto", "Elementos", "Expressão"],
                             [[e(r["id"]), e(r["texto"]), e(r["categoria"]), e(r.get("natureza")), e(r.get("gravidade")), e(r.get("contexto")),
                               e(", ".join(r.get("elementos") or [])), f'<code>{e((r.get("expressao") or "")[:300])}</code>'] for r in rules[:MAX_ROWS]]))
    return out


def page(app, request):
    domain = app.require_domain()
    inventories = domain.inventories()
    source_id = request.get("fonte")
    body = message(request.get("aviso"), request.get("tipo", "ok"))
    body += section("Fase 0: extração", _phase0(domain))
    body += section("Fontes (dominio.json)", _sources_table(domain, inventories))
    if source_id:
        if source_id not in inventories:
            body += message(f"a fonte {source_id} ainda não tem inventário", "warn")
        else:
            body += section(f"Inventário {source_id}", _inventory_detail(source_id, inventories[source_id], request.get("categoria"), request.get("q", "")))
    body += where_box([('A definição das fontes', 'dominios/<d>/dominio.json'), ('Os adaptadores (registo ADAPTERS)', 'ecv/0_transformer/adapters/__init__.py'), ('A extração', 'ecv/0_transformer/extraction.py'), ('O formato do inventário', 'ecv/0_transformer/inventory.py'), ('A classificação das regras por categoria', 'ecv/0_transformer/classification.py'), ('Os inventários', 'dominios/<d>/inventario/<fonte>.json'), ('Esta página', 'ecv/7_webapp/handlers/inventory.py')])
    return Response.html(layout.page(app, "inventario", f"Inventário · {domain.name}", body, request.path,
                              "Módulo 0: cada fonte do domínio, lida pelo seu adaptador, num inventário de grupos, elementos e regras."))



def extract(app, request):
    domain = app.require_domain()
    summary = transformer.extract(domain)
    app.log.event(f"{domain.id}: fase 0 extraída ({'; '.join(summary)})")
    return Response.redirect(url("/inventario", aviso=f"{len(summary)} inventário(s) escritos; reveja e aceite a fase 0"),
                             note="extração")



def api(app, request):
    domain = app.require_domain()
    inventories = domain.inventories()
    source_id = request.get("fonte")
    return Response.json(inventories[source_id] if source_id else {k: v.get("contagens") for k, v in inventories.items()})
