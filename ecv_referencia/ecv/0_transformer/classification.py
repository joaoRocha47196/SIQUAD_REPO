"""Classification of source rules by category, and the mapping of source types to ECV base types.

The category of a rule is the hint for the step that handles it: presence and cardinality go to B,
format, values and range to C, conditional and exclusion to D, calculation and cross-document to E.
"""
import re

CATEGORIES = {
    "presenca":      ("RE", "o elemento ou grupo tem de existir (obrigatoriedade): exprime-se numa projeção"),
    "cardinalidade": ("RE", "número máximo ou mínimo de ocorrências: cardinalidade da composição ou projeção"),
    "formato":       ("RP", "formato do valor (padrão, comprimento, casas decimais): RP tipificada"),
    "valores":       ("RP", "lista fechada de valores admitidos: RP IN"),
    "gama":          ("RP", "mínimo e máximo: RP RANGE"),
    "condicional":   ("RIR", "só se aplica quando outra informação tem um dado valor: RIR (ou RIC, se concluir)"),
    "exclusao":      ("RIR", "dois elementos mutuamente exclusivos ou que dependem um do outro: RIR"),
    "calculo":       ("FN", "relação aritmética entre vários elementos (somas, totais): restrição por função"),
    "cruzada":       ("FN", "coerência entre coleções ou documentos: restrição por função"),
    "outra":         ("?", "não classificada: decidir no passo C, D ou E"),
}

# (category, pattern on the text, pattern on the expression), tried in order
_RULES = [
    ("exclusao", r"mutually exclusive|mutuamente exclusiv|shall not both|não podem coexistir", None),
    ("condicional", r"\bif\b|\bwhen\b|in case|where the|that contains|se\b.*então|quando|caso", None),
    ("calculo", r"\bsum\b|\btotal\b.*=|=.*\+|multipl|soma|igual a.*\+|\bx\b.*=|rounded|arredond", r"sum\(|round\("),
    ("valores", r"only allows the following|following values|valores admitidos|code list|lista de códigos|shall be coded|enum", None),
    ("formato", r"format|formato|pattern|regex|decimals|casas decimais|length|comprimento|characters|tamanho", r"matches\("),
]


def classify(text, expression=""):
    """Probable category of a rule from its text (and expression), and the ECR nature it corresponds to."""
    t = (text or "").lower()
    x = (expression or "").lower()
    category = "outra"
    for name, text_pattern, expression_pattern in _RULES:
        if re.search(text_pattern, t) or (expression_pattern and re.search(expression_pattern, x)):
            category = name
            break
    else:
        if re.search(r"maximum once|at most|no máximo|occur maximum|count\(", t + " " + x):
            category = "cardinalidade"
        elif re.search(r"minimum|maximum|between|entre .* e |greater|less|superior|inferior|>=|<=", t):
            category = "gama"
        elif re.search(r"shall (have|contain|be (filled|provided|present))|must (have|contain)|deve conter|obrigat", t):
            category = "presenca"
        elif re.search(r"should not include|não deve incluir", t):
            category = "presenca"
    return category, CATEGORIES[category][0]


BASE_TYPE_MAP = {
    # CIUS-PT (EN 16931): semantic data types
    "T": "texto", "I": "texto", "C": "texto", "D": "data", "A": "decimal", "U": "decimal", "P": "decimal",
    "Q": "decimal", "B": "texto", "O": "texto",
    # Dart
    "String": "texto", "int": "inteiro", "double": "decimal", "num": "decimal", "bool": "booleano", "DateTime": "data",
    # JSON Schema
    "string": "texto", "integer": "inteiro", "number": "decimal", "boolean": "booleano",
}


def base_type(source_type):
    """The ECV base type of a source type (None when unknown)."""
    if source_type is None:
        return None
    t = str(source_type).strip()
    if t in BASE_TYPE_MAP:
        return BASE_TYPE_MAP[t]
    if re.match(r"^N\(\d+\.\d+\)$", t):
        return "decimal"
    if re.match(r"^N(\(\d+\))?$", t):
        return "inteiro"
    return {"C": "texto", "D": "data", "L": "booleano"}.get(t, None)


def term_ids(text):
    """BT-n and BG-n identifiers mentioned in a text (EN 16931 / CIUS-PT semantic model)."""
    return sorted(set(re.findall(r"\b(B[TG]-\d+)\b", text or "")), key=lambda x: (x[:2], int(x[3:])))
