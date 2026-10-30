"""The internal specification: one file with everything the LLM needs to write a declaration.

The specs in specs/ are written for people (diagrams, tables, examples taken from the example
declarations, links, the graph edges of each entity). The LLM needs the rules of the format, not the
presentation: this module builds, from the same files, a single compact text (specs/ecv_specs.md):

  - the closed vocabulary, read from the configuration (types, operators and value forms, operators per
    type, cardinalities, rule types, naming patterns, metadata SM);
  - the declaration structure (one declaration, one HLM; every section and field);
  - each ECM and ECR entity: description, attributes, sketch in the declaration, can / cannot, details,
    verifications;
  - naming, paths, catalogue and the verification codes.

Removed: mermaid diagrams, the graph edges, the generated tables of the example declarations, links and
the parts that only explain the thesis or the repository. Tables become lists. Every step prompt
includes this file in full, so the LLM can map any inventory element or rule to the right construct.

    python -m ecv specs        rewrites the file; a test checks it is up to date
"""
import re

from ecv import config

DECLARATION_SECTIONS = ("Uma declaração, um HLM", "Estrutura geral", "Todas as possibilidades, secção a secção")
ENTITY_FILES = [
    ("Modelos (ECM)", ["ecm/HLM.md", "ecm/SM.md", "ecm/USM.md", "ecm/Propriedade.md", "ecm/Composicao.md"]),
    ("Regras (ECR)", ["ecr/Regra.md", "ecr/RP.md", "ecr/RIR.md", "ecr/RIC.md", "ecr/Restricao.md", "ecr/CondicaoAplicabilidade.md",
                      "ecr/Funcao.md", "ecr/ContextoExterno.md", "ecr/RE_Projecao.md", "ecr/Perfil.md"]),
    ("Convenções e verificação", ["transversal/Nomenclatura.md", "transversal/Caminhos.md", "transversal/Catalogo.md",
                                  "transversal/Verificacao.md"]),
]
DROPPED_SECTIONS = ("Diagrama", "Ligações no grafo", "Exemplos das declarações de exemplo", "Nas declarações de exemplo",
                    "Conjuntos de Regras de Plausibilidade da tese",
                    "No grafo", "Correspondência com a tese", "Ciclo de avaliação")
DROPPED_LINE_PREFIXES = ("No grafo:", "Relação com a tese:")


# ---------------------------------------------------------------------- markdown clean-up
def _remove_generated_blocks(text):
    return re.sub(r"<!-- gerar:[^>]*-->\n.*?<!-- /gerar -->\n?", "", text, flags=re.S)


def _remove_mermaid(text):
    return re.sub(r"```mermaid\n.*?```\n?", "", text, flags=re.S)


def _unlink(text):
    """[text](target) -> text."""
    return re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)


def _table_to_list(lines):
    """A markdown table as a list: one item per row, '<first cell> — <header>: <cell>; ...'."""
    cells = [[c.strip() for c in line.strip().strip("|").split("|")] for line in lines]
    header, rows = cells[0], [r for r in cells[2:] if any(r)]
    out = []
    for row in rows:
        first = row[0]
        rest = [f"{h.lower()}: {v}" for h, v in zip(header[1:], row[1:]) if v and v != "—"]
        out.append(f"- {first}" + (" — " + "; ".join(rest) if rest else ""))
    return out


def _tables_to_lists(text):
    out, table = [], []
    for line in text.splitlines():
        if line.lstrip().startswith("|"):
            table.append(line)
            continue
        if table:
            out += _table_to_list(table) if len(table) >= 2 else table
            table = []
        out.append(line)
    if table:
        out += _table_to_list(table)
    return "\n".join(out)


def _sections(text):
    """[(level, title, body lines)] of a markdown text (level 0 for what comes before the first heading)."""
    sections, current = [], (0, "", [])
    in_code = False
    for line in text.splitlines():
        if line.startswith("```"):
            in_code = not in_code
        m = None if in_code else re.match(r"^(#{1,6}) (.+)$", line)
        if m:
            sections.append(current)
            current = (len(m.group(1)), m.group(2).strip(), [])
        else:
            current[2].append(line)
    sections.append(current)
    return sections


def _keep(sections, dropped=DROPPED_SECTIONS):
    """Drop the sections whose title starts with a dropped title, with their subsections."""
    out, skip_below = [], None
    for level, title, body in sections:
        if skip_below is not None and level > skip_below:
            continue
        skip_below = None
        if level and any(title.startswith(d) for d in dropped):
            skip_below = level
            continue
        out.append((level, title, body))
    return out


def _without_empty_headings(sections):
    """Drop headings left with no text and no subsections (after their content was removed)."""
    out = []
    for i, (level, title, body) in enumerate(sections):
        has_text = any(line.strip() for line in body if not line.startswith(DROPPED_LINE_PREFIXES))
        next_level = sections[i + 1][0] if i + 1 < len(sections) else 0
        if level and not has_text and next_level <= level:
            continue
        out.append((level, title, body))
    return out


def _render(sections, shift):
    sections = _without_empty_headings(_without_empty_headings(sections))
    out = []
    for level, title, body in sections:
        if level:
            out.append("#" * min(level + shift, 6) + " " + title)
        lines = [line for line in body if not line.startswith(DROPPED_LINE_PREFIXES)]
        out.append("\n".join(lines).strip("\n"))
    text = "\n\n".join(part for part in out if part.strip())
    return re.sub(r"\n{3,}", "\n\n", text)


def clean(text, shift=1, dropped=DROPPED_SECTIONS):
    text = _unlink(_remove_mermaid(_remove_generated_blocks(text)))
    return _tables_to_lists(_render(_keep(_sections(text), dropped), shift))


# ---------------------------------------------------------------------- the parts of the bundle
def vocabulary():
    """The closed vocabulary, exactly as configured."""
    c = config.CONFIG
    lines = ["## Vocabulário fechado", "",
             "Tipos base: " + ", ".join(config.BASE_TYPES) + ".",
             "Cardinalidades das composições: " + ", ".join(config.CARDINALITIES) + ".", "",
             "Operadores (forma do valor; tipos base em que se admitem):"]
    for op, d in config.OPERATORS.items():
        types = [t for t, ops in config.OPERATORS_BY_TYPE.items() if op in ops] or ["qualquer (função)"]
        lines.append(f"- {op}: {d['descricao'].rstrip('.')}. Valor: {c['formasValor'][d['forma']].rstrip('.')}. Tipos: {', '.join(types)}."
                     + (" Pode comparar com um contexto externo." if d["contexto"] else ""))
    lines += ["", "Tipos de regra:"]
    for t, d in config.RULE_TYPES.items():
        lines.append(f"- {t} ({d['nome']}; natureza {d['natureza'] or 'expressa pela projeção'}): {d['descricao']}")
    lines += ["", "Tipos de conclusão de uma RIC: " + ", ".join(f"{k} ({v})" for k, v in config.CONCLUSION_TYPES.items()) + ".",
              "Papéis dos parâmetros de uma função: " + ", ".join(f"{k} ({v})" for k, v in config.PARAMETER_ROLE_NAMES.items()) + ".", "",
              "Nomes (expressões regulares):"]
    lines += [f"- {k}: `{v}`" for k, v in c["nomes"].items() if k != "data"]
    m = config.METADATA_SM
    lines += ["", f"SM de metainformação: {m['nome']} ({m['cardinalidade']}), composto pelos HLM principais, com as propriedades:"]
    lines += [f"- {p['nome']} ({p['tipo']}): {p['descricao']}" for p in m["propriedades"]]
    return "\n".join(lines)


def declaration_structure():
    text = (config.path("specs") / "declaracao" / "README.md").read_text(encoding="utf-8")
    sections = [s for s in _sections(_unlink(_remove_generated_blocks(text)))]
    keep, inside = [], False
    for level, title, body in sections:
        if level == 2:
            inside = title in DECLARATION_SECTIONS
        if inside:
            keep.append((level, title, body))
    return "## A declaração ECV\n\n" + _tables_to_lists(_render(keep, 1))


def entity_specs():
    out = []
    for group, files in ENTITY_FILES:
        out.append(f"## {group}")
        for rel in files:
            text = (config.path("specs") / "entidades" / rel).read_text(encoding="utf-8")
            out.append(clean(text, shift=2))
    return "\n\n".join(out)


def build():
    header = ("# Especificação da ECV (versão para o LLM)\n\n"
              "Este texto é gerado a partir das specs do repositório (specs/) por ecv/1_ecv_builder/specs_bundle.py. "
              "Contém as regras completas do formato da Declaração ECV: o vocabulário fechado, a estrutura da declaração, "
              "cada entidade (ECM e ECR), os caminhos, os nomes e as verificações que o código faz a cada resposta. "
              "Tudo o que se produz tem de as cumprir.")
    return "\n\n".join([header, vocabulary(), declaration_structure(), entity_specs()]).rstrip() + "\n"


def bundle_path():
    return config.path("specsInternas")


def write():
    path = bundle_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    text = build()
    path.write_text(text, encoding="utf-8")
    return path, len(text)


def is_current():
    path = bundle_path()
    return path.exists() and path.read_text(encoding="utf-8") == build()


def text():
    """The bundle as it is on disk (built if missing)."""
    path = bundle_path()
    if not path.exists():
        write()
    return path.read_text(encoding="utf-8")
