"""The checks of the generation (phase G) and of each review layer (A to F).

Always:
    verification       each declaration against the specs (module 3); errors block
    cobertura          inventory items not yet in the mapping: in G, every element and rule (informative);
                       in a layer, the elements (A) or the rules of the layer's categories (B to E), and it blocks
    fusao              the domain's declarations merged with each other; a conflict blocks
    conflitosComReferencia   the domain merged over the reference declarations (examples, other domains)
G and A:
    destinosInexistentes   mapping destinations that are not a path of the declaration; blocks
    partilhadosDiferentes  a shared model that differs between two declarations; blocks
    semelhantesNoGrafo     a new USM that looks like a model of the reference (reuse it?)
G and C:  valoresAdmitidosSemRP   source elements with allowed values whose property has no RP
G and D:  coerencia               terms outside the plausible values, incompatible rules, repeated conditions
G and E:  funcoesSemelhantes      functions with the name or the parameters of a function of the reference
"""
import json
import re
from dataclasses import dataclass, field

from ecv.amendments import DeclarationSet
from ecv.graph.base import read_json
from ecv.ingestion import Declaration, ingest, verify
from ecv.ingestion import paths
from ecv.views.viewmodels import build

from . import search
from .build_process import GENERATION, STEP_CATEGORIES
from .reference import reference_files, reference_graph

BLOCKING = ("cobertura", "destinosInexistentes", "partilhadosDiferentes", "fusao")
MAPPED = ("mapeado", "fundido")
MAX_LINES = 200


@dataclass
class StepCheck:
    """The result of the checks of a step."""
    declarations: int
    errors: int
    warnings: int
    lines: list
    extra: dict = field(default_factory=dict)
    with_coverage: bool = False
    coverage_blocks: bool = True

    @property
    def valid(self):
        blocking = BLOCKING if self.coverage_blocks else tuple(k for k in BLOCKING if k != "cobertura")
        return not self.errors and not any(self.extra.get(k) for k in blocking)

    def summary(self):
        text = f"{self.declarations} declaração(ões); {self.errors} erro(s), {self.warnings} aviso(s)"
        if self.with_coverage:
            text += f"; cobertura em falta: {len(self.extra.get('cobertura', []))}"
        return text

    def text(self):
        lines = list(self.lines)
        for key, items in self.extra.items():
            if items:
                lines.append(f"== {key} ({len(items)})")
                lines += [f"  {x}" for x in items[:MAX_LINES]]
                if len(items) > MAX_LINES:
                    lines.append(f"  … (+{len(items) - MAX_LINES})")
        return self.summary() + "\n" + "\n".join(lines)

    def to_dict(self):
        return {"resumo": self.summary(), "valido": self.valid, "erros": self.errors, "avisos": self.warnings,
                "extra": self.extra, "texto": self.text()}


def _destination(ds, entry):
    """(declaration, HLM, path) of a mapping destination 'HLM:<name>/<path>', or None."""
    m = re.match(r"^HLM:(\w+)/(.+)$", entry.get("destino") or "")
    if not m:
        return None
    d = ds.declarations.get(m.group(1))
    return (d, m.group(1), m.group(2)) if d is not None else (None, m.group(1), m.group(2))


class StepChecker:
    def __init__(self, domain, step):
        self.domain = domain
        self.step = step
        self.ds = DeclarationSet.load(domain.folder)
        self._graph = None

    @property
    def ingestion(self):
        if self._graph is None:
            self._graph = ingest(self.domain.declaration_files())
        return self._graph

    def run(self):
        lines, errors, warnings = [], 0, 0
        for f in self.domain.declaration_files():
            report = verify(Declaration.load(f))
            errors += len(report.errors)
            warnings += len(report.warnings)
            lines.append(f"== {f.name}: {report.summary()}")
            lines += [str(p) for p in report.problems]
        check = StepCheck(len(self.domain.declaration_files()), errors, warnings, lines, with_coverage=self.step not in (None, "0"),
                          coverage_blocks=self.step != GENERATION)
        if check.with_coverage:
            check.extra = self._step_checks()
        return check

    def _step_checks(self):
        extra = {"cobertura": self.coverage()}
        if self.step in (GENERATION, "A"):
            extra["destinosInexistentes"] = self.missing_destinations()
            extra["partilhadosDiferentes"] = self.differing_shared_models()
            extra["semelhantesNoGrafo"] = self.similar_to_reference()
        if self.step in (GENERATION, "C"):
            extra["valoresAdmitidosSemRP"] = self.allowed_values_without_rp()
        if self.step in (GENERATION, "D"):
            extra["coerencia"] = self.coherence()
        if self.step in (GENERATION, "E"):
            extra["funcoesSemelhantes"] = self.similar_functions()
        extra["fusao"] = [r.summary() for r in self.ingestion.results if not r.accepted]
        extra["conflitosComReferencia"] = self.reference_conflicts()
        return extra

    # ------------------------------------------------------------------ every step
    def coverage(self):
        """Inventory items of the step that the mapping does not mention yet."""
        mapped = {(x["fonte"], x["origem"]) for x in self.ds.mapping if x.get("decisao") != "adiado"}
        missing = []
        for source_id, inv in self.domain.inventories().items():
            if self.step == GENERATION:
                items = [r["id"] for r in inv["regras"]]
                if self.domain.source_role(source_id) != "complementar":
                    items = [x["id"] for x in inv["elementos"]] + items
            elif self.step == "A":
                if self.domain.source_role(source_id) == "complementar":
                    continue
                items = [e["id"] for e in inv["elementos"]]
            elif self.step in STEP_CATEGORIES:
                items = [r["id"] for r in inv["regras"] if r["categoria"] in STEP_CATEGORIES[self.step]]
            else:
                items = []
            missing += [f"{source_id}:{i}" for i in items if (source_id, i) not in mapped]
        return missing

    def reference_conflicts(self):
        """The domain merged over the reference declarations (nothing saved): what it redefines differently."""
        ingestion = ingest(list(reference_files(exclude=self.domain.id)) + self.domain.declaration_files())
        names = {f.name for f in self.domain.declaration_files()}
        return [r.summary() for r in ingestion.results if not r.accepted and any(n in r.summary() for n in names)]

    # ------------------------------------------------------------------ step A
    def missing_destinations(self):
        bad = []
        for entry in self.ds.mapping:
            dest = _destination(self.ds, entry)
            if dest is None or entry.get("decisao") not in MAPPED:
                continue
            d, hlm, path = dest
            if d is None or paths.try_resolve(Declaration(d), "HLM", hlm, path) is None:
                bad.append(f"{entry['fonte']}:{entry['origem']} → {entry['destino']}")
        return bad

    def differing_shared_models(self):
        seen, different = {}, []
        for hlm, d in self.ds.declarations.items():
            for section in ("usm", "sm"):
                for m in d.get(section, []):
                    key = (section, m["nome"])
                    text = json.dumps(m, sort_keys=True, ensure_ascii=False)
                    if key in seen and seen[key][1] != text:
                        different.append(f"{section.upper()} {m['nome']} difere entre {seen[key][0]} e {hlm}")
                    seen.setdefault(key, (hlm, text))
        return different

    def similar_to_reference(self):
        g, ref = self.ingestion.graph, reference_graph(exclude=self.domain.id)
        found = []
        for m in g.nodes("USM"):
            props = [e.target["nome"] for e in g.outgoing(m, "CONTEM")]
            for s in search.similar_models(ref, props, threshold=0.5):
                if s["nome"] != m["nome"]:
                    found.append(f"USM {m['nome']} parece-se com {s['nivel']} {s['nome']} do grafo de referência "
                                 f"({s['semelhanca']}: {', '.join(s['comuns'])})")
        return found

    # ------------------------------------------------------------------ steps C, D, E
    def allowed_values_without_rp(self):
        g = self.ingestion.graph
        values = {(k, e["id"]): e["valoresAdmitidos"] for k, inv in self.domain.inventories().items()
                  for e in inv["elementos"] if e.get("valoresAdmitidos")}
        missing = []
        for entry in self.ds.mapping:
            key = (entry["fonte"], entry["origem"])
            dest = _destination(self.ds, entry)
            if key not in values or entry.get("decisao") not in MAPPED or dest is None or dest[0] is None:
                continue
            d, hlm, path = dest
            res = paths.try_resolve(Declaration(d), "HLM", hlm, path)
            if res is None or res.ends_in_model:
                continue
            node = g.node("Propriedade", paths.property_key(res.owner[0], res.owner[1], res.prop["nome"]))
            has_rp = node is not None and any(r.label == "RP" for restriction in g.sources(node, "RESTRINGE")
                                              for r in g.sources(restriction, "RESTRITA_POR"))
            if not has_rp:
                missing.append(f"{entry['fonte']}:{entry['origem']} → {entry['destino']} (valores {values[key][:6]}…) sem RP")
        return missing

    def coherence(self):
        c = build(self.ingestion.graph, "coerencia")
        return ([f"termo fora dos plausíveis: {x['regra']} lê {x['propriedade']} = {x['valores']} (plausíveis {x['plausiveis'][:6]}…)"
                 for x in c["foraDosPlausiveis"]]
                + [f"regras incompatíveis em {x['propriedade']}: {', '.join(r['id'] for r in x['regras'])}" for x in c["incompativeis"]]
                + [f"mesma condição ({x['condicao']}): {', '.join(x['regras'])}" for x in c["mesmaCondicao"]])

    def similar_functions(self):
        def signature(f):
            return tuple(sorted((p.get("tipo"), p.get("papel"), bool(p.get("colecao"))) for p in read_json(f.get("parametros"), [])))
        ref = reference_graph(exclude=self.domain.id)
        found = []
        for f in self.ingestion.graph.nodes("Funcao"):
            for r in ref.nodes("Funcao"):
                if r["nome"] == f["nome"] and signature(r) != signature(f):
                    found.append(f"a função {f['nome']} existe no grafo de referência com outros parâmetros (conflito na fusão)")
                elif r["nome"] != f["nome"] and signature(r) == signature(f) and r.get("retorno") == f.get("retorno"):
                    found.append(f"a função {f['nome']} tem os mesmos parâmetros que {r['nome']} do grafo de referência: "
                                 f"é a mesma? ({r.get('descricao')})")
        return found


def check_step(domain, step=None):
    return StepChecker(domain, step).run()
