"""Fill the generated blocks of the Markdown files from the example declarations (specs/exemplos, one per HLM).

A generated block has the form

    <!-- gerar:KIND:ARGUMENT -->
    (content replaced)
    <!-- /gerar -->

so the examples in the specs and the READMEs are always those of the declarations (python -m ecv docs).
The declarations are combined by the name of each entity (shared models appear once), as the ingestion
merges them.
"""
import re

from ecv import config
from ecv.ingestion import Declaration, ingest
from ecv.ingestion import rule_parts as R
from ecv.ingestion.descriptions import format_call
from ecv.shared.json_format import dumps

SECTIONS = ("contextosExternos", "funcoes", "usm", "sm", "hlm", "projecoes", "perfis")
BLOCK = re.compile(r"(<!-- gerar:([a-z\-]+):?([^ ]*) -->\n)(.*?)(<!-- /gerar -->)", re.S)
SKIPPED_FOLDERS = ("site", "vistas", "processamento_teste", "pedidos")


def combine(paths):
    """A read-only Declaration with the entities of every declaration (the first occurrence of each name)."""
    data = {s: [] for s in SECTIONS}
    for path in paths:
        d = Declaration.load(path).data
        for s in SECTIONS:
            names = {x["nome"] for x in data[s]}
            data[s] += [x for x in d.get(s, []) if x["nome"] not in names]
    return Declaration(data)


def _cell(x):
    return str(x).replace("|", "\\|").replace("\n", " ")


def md_table(header, rows):
    out = ["| " + " | ".join(header) + " |", "|" + "|".join("---" for _ in header) + "|"]
    out += ["| " + " | ".join(_cell(c) for c in row) + " |" for row in rows]
    return "\n".join(out)


def md_json(data):
    return "```json\n" + dumps(data).rstrip() + "\n```"


def _composition_text(role, child, card):
    return f"{role if role == child else role + ' (' + child + ')'} [{card}]"


class BlockWriter:
    def __init__(self, decl):
        self.d = decl

    # ------------------------------------------------------------------ JSON of one entity
    def rule_json(self, rule_id):
        return md_json(self.d.rule(rule_id).rule)

    def model_json(self, level, name, without_rules=False):
        m = dict(self.d.model(level, name))
        if without_rules:
            n = len(m.get("regras", []))
            m.pop("regras", None)
            if n:
                m["regras"] = [f"... {n} regra(s) omitida(s) neste excerto ..."]
            if "propriedades" in m:
                m["propriedades"] = [{k: v for k, v in p.items() if k != "regras"} for p in m["propriedades"]]
        return md_json(m)

    def property_json(self, key):
        level, rest = key.split(":")
        owner, name = rest.split(".")
        return md_json(self.d.get_property(level, owner, name))

    def section_json(self, section, name):
        found = next((x for x in self.d.data.get(section, []) if x.get("nome") == name), None)
        if found is None:
            raise KeyError(f"{section} {name}")
        return md_json(found)

    # ------------------------------------------------------------------ tables
    def _rules(self, kind):
        return [site for site in self.d.rules() if site.type == kind]

    def hlm_table(self):
        rows = []
        for name, m in self.d.hlm.items():
            parts = ", ".join(_composition_text(role, child, card) for role, _, child, card in self.d.compositions("HLM", name))
            rules = m.get("regras", [])
            rows.append([name, m["descricao"], parts, ", ".join(r["id"] for r in rules[:6]) + (f" … (+{len(rules) - 6})" if len(rules) > 6 else "")])
        return md_table(["HLM", "Descrição", "Composição (papel, SM, cardinalidade)", "Regras que vivem no HLM"], rows)

    def sm_table(self):
        rows = []
        for name, m in self.d.sm.items():
            parts = ", ".join(_composition_text(role, child, card) for role, _, child, card in self.d.compositions("SM", name)) or "—"
            residual = ", ".join(p["nome"] for p in m.get("propriedades", [])) or "—"
            used = ", ".join(f"{level} {parent}" for level, parent in self.d.parents("SM", name)) or "—"
            rows.append([name, m["descricao"], parts, residual, used, ", ".join(r["id"] for r in m.get("regras", [])) or "—"])
        return md_table(["SM", "Descrição", "Compõe (USM)", "Propriedades residuais", "Composto por", "Regras no SM"], rows)

    def usm_table(self):
        rows = []
        for name, m in self.d.usm.items():
            used = ", ".join(parent for _, parent in self.d.parents("USM", name))
            n = len(m.get("regras", [])) + sum(len(p.get("regras", [])) for p in m["propriedades"])
            rows.append([name, m["descricao"], ", ".join(p["nome"] for p in m["propriedades"]), used, n])
        return md_table(["USM", "Descrição", "Propriedades", "Composto pelos SM", "N.º de regras"], rows)

    def properties_table(self):
        rows = [[f"`{level}:{name}.{p['nome']}`", p["tipo"], p["descricao"], ", ".join(p.get("nomesAlternativos", [])) or "—", len(p.get("regras", []))]
                for level, name, m in self.d.all_models() for p in m.get("propriedades", [])]
        return md_table(["Chave", "Tipo", "Descrição", "Nomes alternativos", "Regras na propriedade"], rows)

    def compositions_table(self):
        rows = []
        for level in ("HLM", "SM"):
            for name in self.d.models(level):
                for role, child_level, child, card in self.d.compositions(level, name):
                    reading = "repetível (coleção)" if config.is_repeatable(card) else ("opcional" if card.startswith("0") else "singular")
                    rows.append([f"{level} {name}", f"{child_level} {child}", role, card, reading])
        return md_table(["Modelo que compõe", "Modelo composto", "Papel (segmento do caminho)", "Cardinalidade", "Leitura"], rows)

    def rp_table(self, form):
        rows = []
        for site in self._rules("RP"):
            restriction = R.restriction(site.rule)
            if (form == "funcao") == R.is_function(restriction):
                rows.append([site.id, site.scope, site.rule["descricao"], restriction["mensagem"]])
        return md_table(["Regra", "Vive em", "Restrição (descrição)", "Mensagem de não conformidade"], rows)

    def rir_table(self, arg):
        rows = []
        for site in self._rules("RIR"):
            restriction = R.restriction(site.rule)
            target = restriction.get("propriedade") or format_call(restriction["chamada"])
            if arg.startswith("id="):
                if not site.id.startswith(arg[3:]):
                    continue
            elif arg and not target.endswith(arg):
                continue
            rows.append([site.id, site.scope, site.rule["descricao"], restriction["mensagem"]])
        return md_table(["Regra", "Vive em", "Descrição (Se … → …)", "Mensagem de não conformidade"], rows)

    def ric_table(self):
        rows = [[site.id, site.scope, site.rule["descricao"], site.rule["mensagem"], ", ".join(R.contexts_used(self.d, site.rule)) or "—"]
                for site in self._rules("RIC")]
        return md_table(["Regra", "Vive em", "Descrição", "Mensagem de conclusão", "Contextos externos"], rows)

    def functions_table(self):
        rows = []
        for f in self.d.functions.values():
            params = ", ".join(f"{p['nome']}: {p['tipo']}" + (" (literal)" if p["papel"] == "parametro" else "") + (" [coleção]" if p.get("colecao") else "")
                               for p in f["parametros"])
            uses = [site.id for site in self.d.rules() for _, _, call in R.function_calls(site.rule) if call["funcao"] == f["nome"]]
            operator = "EXT_FUNCTION" if f["contextosExternos"] else "FUNCTION"
            rows.append([f["nome"], f["descricao"], params, ", ".join(f["contextosExternos"]) or "—", operator, ", ".join(uses)])
        return md_table(["Função", "Verdadeira quando", "Parâmetros", "Contextos externos", "Operador", "Regras"], rows)

    def contexts_table(self):
        rows = []
        for c in self.d.contexts.values():
            functions = [f["nome"] for f in self.d.functions.values() if c["nome"] in f["contextosExternos"]]
            terms = [site.id for site in self.d.rules() for t in R.condition(site.rule) if t.get("contexto") == c["nome"]]
            profiles = [f"{p['nome']} = {fx['valor']}" for p in self.d.profiles.values() for fx in p["fixa"] if fx.get("contexto") == c["nome"]]
            rows.append([c["nome"], c["tipo"], c["descricao"], c.get("fonte", ""), ", ".join(functions) or "—", ", ".join(terms) or "—", ", ".join(profiles) or "—"])
        return md_table(["Contexto", "Tipo", "Descrição", "Fonte", "Usado pelas funções", "Usado em termos (regras)", "Fixado por perfis"], rows)

    def projections_table(self):
        rows = [[p["nome"], p["hlm"], p.get("descricao", ""), ", ".join(p["obrigatorias"]) or "—", ", ".join(p["permitidas"]) or "—"]
                for p in self.d.projections.values()]
        return md_table(["Projeção", "HLM", "Descrição", "Obrigatórias", "Permitidas"], rows)

    def profiles_table(self):
        rows = []
        for p in self.d.profiles.values():
            fixed = "; ".join(f"{x.get('propriedade') or 'contexto ' + x['contexto']} = {x['valor']}" for x in p["fixa"]) or "— (seleção dinâmica)"
            rows.append([p["nome"], p["projecao"], p.get("descricao", ""), fixed])
        return md_table(["Perfil", "Projeção", "Descrição", "Valores fixados"], rows)

    def operators_table(self):
        counts = {op: [0, 0] for op in config.OPERATORS}
        for site in self.d.rules():
            restriction = R.restriction(site.rule)
            if restriction:
                counts[restriction["operador"]][0] += 1
            for term in R.condition(site.rule):
                counts[term["operador"]][1] += 1
        rows = [[op, d["grupo"], d["forma"], ", ".join(t for t, ops in config.OPERATORS_BY_TYPE.items() if op in ops) or "qualquer tipo",
                 counts[op][0], counts[op][1]] for op, d in config.OPERATORS.items()]
        return md_table(["Operador", "Grupo", "Forma do valor", "Tipos base", "Restrições nos exemplos", "Termos nos exemplos"], rows)

    def counts(self):
        kinds = {}
        for site in self.d.rules():
            kinds[site.type] = kinds.get(site.type, 0) + 1
        properties = sum(len(m.get("propriedades", [])) for _, _, m in self.d.all_models())
        return md_table(["Entidade", "Quantidade"], [
            ["HLM", len(self.d.hlm)], ["SM", len(self.d.sm)], ["USM", len(self.d.usm)], ["Propriedades", properties],
            ["RP", kinds.get("RP", 0)], ["RIR", kinds.get("RIR", 0)], ["RIC", kinds.get("RIC", 0)],
            ["Funções", len(self.d.functions)], ["Contextos externos", len(self.d.contexts)],
            ["Projeções", len(self.d.projections)], ["Perfis", len(self.d.profiles)]])

    def graph_counts(self):
        nodes, edges = ingest(config.example_declarations()).graph.counts()
        ln, le = list(nodes.items()), list(edges.items())
        rows = []
        for i in range(max(len(ln), len(le))):
            a = ln[i] if i < len(ln) else ("", "")
            b = le[i] if i < len(le) else ("", "")
            rows.append([a[0], a[1], b[0], b[1]])
        rows.append(["**total**", f"**{sum(nodes.values())}**", "**total**", f"**{sum(edges.values())}**"])
        return md_table(["Nós", "", "Arestas", ""], rows)

    # ------------------------------------------------------------------ dispatch
    def write(self, kind, arg):
        json_sections = {"json-funcao": "funcoes", "json-contexto": "contextosExternos", "json-projecao": "projecoes", "json-perfil": "perfis"}
        if kind == "json-regra":
            return self.rule_json(arg)
        if kind in ("json-hlm", "json-sm", "json-usm"):
            return self.model_json(kind.split("-")[1].upper(), arg)
        if kind in ("json-hlm-resumo", "json-sm-resumo", "json-usm-resumo"):
            return self.model_json(kind.split("-")[1].upper(), arg, without_rules=True)
        if kind == "json-propriedade":
            return self.property_json(arg)
        if kind in json_sections:
            return self.section_json(json_sections[kind], arg)
        if kind == "tabela-rp":
            return self.rp_table(arg)
        if kind == "tabela-rir":
            return self.rir_table(arg)
        tables = {"tabela-hlm": self.hlm_table, "tabela-sm": self.sm_table, "tabela-usm": self.usm_table,
                  "tabela-propriedades": self.properties_table, "tabela-composicoes": self.compositions_table,
                  "tabela-ric": self.ric_table, "tabela-funcoes": self.functions_table, "tabela-contextos": self.contexts_table,
                  "tabela-projecoes": self.projections_table, "tabela-perfis": self.profiles_table,
                  "tabela-operadores": self.operators_table, "contagens": self.counts, "quantidades-grafo": self.graph_counts}
        if kind in tables:
            return tables[kind]()
        raise KeyError(f"bloco desconhecido: {kind}")


def markdown_files():
    return [f for f in sorted(config.ROOT.rglob("*.md")) if not any(p in f.relative_to(config.ROOT).parts for p in SKIPPED_FOLDERS)]


def update():
    """Rewrite every generated block; returns the files changed."""
    writer = BlockWriter(combine(config.example_declarations()))
    changed = []
    for f in markdown_files():
        text = f.read_text(encoding="utf-8")
        new = BLOCK.sub(lambda m: m.group(1) + writer.write(m.group(2), m.group(3)) + "\n" + m.group(5), text)
        if new != text:
            f.write_text(new, encoding="utf-8")
            changed.append(str(f.relative_to(config.ROOT)))
    return changed


def stale():
    """Files whose generated blocks differ from what update() would write (used by a test)."""
    writer = BlockWriter(combine(config.example_declarations()))
    out = []
    for f in markdown_files():
        text = f.read_text(encoding="utf-8")
        if BLOCK.sub(lambda m: m.group(1) + writer.write(m.group(2), m.group(3)) + "\n" + m.group(5), text) != text:
            out.append(str(f.relative_to(config.ROOT)))
    return out
