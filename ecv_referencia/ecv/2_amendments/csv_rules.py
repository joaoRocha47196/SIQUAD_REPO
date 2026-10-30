"""Rules from a table: a CSV of known mappings becomes one RIR per row (operations 'adicionar_regra').

Typical case: the postal code that each parish of a city admits. The table

    pais;localidade;freguesia;codigoPostal
    PT;LISBOA;AJUDA;^(1300|1349)-[0-9]{3}$
    PT;LISBOA;ALCANTARA;^(1300|1350)-[0-9]{3}$

with target column 'codigoPostal' and operator PATTERN becomes, for each row, the RIR

    Se Morada.pais = PT e Morada.localidade = LISBOA e Morada.freguesia = AJUDA
    → Morada.codigoPostal segue o padrão ^(1300|1349)-[0-9]{3}$

Every column except the target (and the optional 'mensagem' and 'id' columns) is a condition term
(EQUALS). The column names are paths relative to the model where the rules live. Values that look
like numbers or booleans are typed. With RANGE, the target cell is 'minimum..maximum'; with IN, a list
separated by '|'.
"""
import csv
import io
import re
import unicodedata

from ecv.shared.errors import AmendmentError

SPECIAL_COLUMNS = ("mensagem", "id")


def _typed(value):
    v = value.strip()
    if v.lower() in ("true", "verdadeiro"):
        return True
    if v.lower() in ("false", "falso"):
        return False
    if re.fullmatch(r"-?\d+", v):
        return int(v)
    if re.fullmatch(r"-?\d+\.\d+", v):
        return float(v)
    return v


def _target_value(operator, cell):
    if operator == "RANGE":
        low, sep, high = cell.partition("..")
        if not sep:
            raise AmendmentError(f"com RANGE, a célula do alvo é 'mínimo..máximo' (recebido {cell!r})")
        return [_typed(low), _typed(high)]
    if operator == "IN":
        return [_typed(x) for x in cell.split("|") if x.strip()]
    if operator in ("PATTERN", "STARTS_WITH", "ENDS_WITH", "CONTAINS"):
        return cell.strip()
    return _typed(cell)


def _rule_id(prefix, values, n):
    """'RIR-CP' + ['PT', 'LISBOA'] -> 'RIR-CP-PT-LISBOA' (accents and other characters become '-')."""
    prefix = prefix.rstrip("-")
    tail = "-".join(re.sub(r"[^A-Z0-9]+", "-", unidecode(str(v)).upper()).strip("-") for v in values if str(v).strip())
    return f"{prefix}-{tail}" if tail else f"{prefix}-{n}"


def unidecode(text):
    return unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()


def read_table(text):
    """(header, rows) of a CSV separated by ';' or ','."""
    dialect = csv.Sniffer().sniff(text.splitlines()[0], delimiters=";,\t") if text.strip() else csv.excel
    rows = [r for r in csv.reader(io.StringIO(text), dialect) if any(c.strip() for c in r)]
    if len(rows) < 2:
        raise AmendmentError("o CSV precisa de uma linha de cabeçalho e pelo menos uma linha de dados")
    return [h.strip() for h in rows[0]], rows[1:]


def operations_from_csv(text, level, model, target, operator, id_prefix, message="{alvo} não corresponde ao valor esperado para {condicao}.",
                        prop=None):
    """The 'adicionar_regra' operations for every row of the table.

    level, model: where the rules live ({nivel, modelo}; optionally on a property 'prop').
    target: the column whose value is the restriction; operator: the restriction's operator.
    message: template of the non-conformity message ({alvo}, {condicao} and any column name)."""
    header, rows = read_table(text)
    if target not in header:
        raise AmendmentError(f"a coluna alvo '{target}' não está no cabeçalho {header}")
    conditions = [h for h in header if h not in (target,) + SPECIAL_COLUMNS]
    if not conditions:
        raise AmendmentError("é preciso pelo menos uma coluna de condição além do alvo")
    operations = []
    for n, row in enumerate(rows, start=1):
        cells = dict(zip(header, row + [""] * (len(header) - len(row))))
        terms = [{"propriedade": c, "operador": "EQUALS", "valor": _typed(cells[c])} for c in conditions if cells[c].strip()]
        condition_text = " e ".join(f"{t['propriedade']} = {t['valor']}" for t in terms)
        rule_id = cells.get("id", "").strip() or _rule_id(id_prefix, [cells[c] for c in conditions], n)
        text_message = cells.get("mensagem", "").strip() or message.format(alvo=target, condicao=condition_text, **cells)
        rule = {"id": rule_id, "natureza": "inferencia_restritiva", "condicao": terms,
                "restricao": {"propriedade": target, "operador": operator, "valor": _target_value(operator, cells[target]),
                              "mensagem": text_message}}
        where = {"nivel": level, "modelo": model, **({"propriedade": prop} if prop else {})}
        operations.append({"op": "adicionar_regra", "onde": where, "regra": rule})
    return operations
