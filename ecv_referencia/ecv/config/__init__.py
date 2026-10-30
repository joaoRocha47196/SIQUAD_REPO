"""The single configuration of the ECV, read from ecv/config/ecv.config.json.

It is the only source of the closed vocabulary (base types, operators, rule types, cardinalities,
levels), the naming conventions, the view colours, the file locations and the default values
(Neo4j, server, view thresholds). Every other module reads these names; no value is repeated in code.

The JSON keeps the vocabulary of the ECV (in Portuguese), because it is the vocabulary of the
declarations and of the thesis; the constants below give it English names for the code.
"""
import json
import os
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CONFIG_FILE = Path(__file__).with_name("ecv.config.json")

with CONFIG_FILE.open(encoding="utf-8") as _f:
    CONFIG = json.load(_f)

BASE_TYPES = tuple(CONFIG["tiposBase"])
VALUE_FORMS = CONFIG["formasValor"]
OPERATORS = CONFIG["operadores"]
FUNCTION_OPERATORS = tuple(CONFIG["operadoresFuncao"])
OPERATORS_BY_TYPE = CONFIG["operadoresPorTipo"]
CONTEXT_OPERATORS = tuple(op for op, d in OPERATORS.items() if d["contexto"])
SELECTION_OPERATORS = tuple(CONFIG["operadoresSelecao"])

RULE_TYPES = CONFIG["tiposRegra"]
NATURES = {d["natureza"]: t for t, d in RULE_TYPES.items() if d["natureza"]}   # nature -> RP | RIR | RIC
RULE_TYPE_NAMES = {t: d["nome"] for t, d in RULE_TYPES.items()}
RULE_TYPE_ORDER = {t: i for i, t in enumerate(t for t in RULE_TYPES if t != "RE")}
RESTRICTION_FORMS = CONFIG["formasRestricao"]
CONCLUSION_TYPES = CONFIG["tiposConclusao"]

CARDINALITIES = tuple(CONFIG["cardinalidades"])
LEVELS = tuple(CONFIG["niveis"])
PARAMETER_ROLES = tuple(CONFIG["funcoes"]["papeisParametro"])
PARAMETER_ROLE_NAMES = CONFIG["funcoes"]["papeisParametro"]
FUNCTION_RETURNS = tuple(CONFIG["funcoes"]["retornos"])
METADATA_SM = CONFIG["metainformacao"]

NAME_PATTERNS = {k: re.compile(v) for k, v in CONFIG["nomes"].items()}
COLORS = CONFIG["cores"]
VIEWS = CONFIG["vistas"]
INGESTION = CONFIG["ingestao"]
SERVER = CONFIG["servidor"]


def path(name):
    """Absolute path of an entry of 'caminhos' (relative to the repository root).

    The environment variable ECV_CAMINHO_<NAME> (for example ECV_CAMINHO_DOMINIOS) overrides the
    configured value: it lets a trial run use another folder of domains without touching the real one."""
    return ROOT / os.environ.get(f"ECV_CAMINHO_{name.upper()}", CONFIG["caminhos"][name])


def example_declarations():
    """The example declarations (one per HLM), ordered by file name."""
    return sorted(path("exemplos").glob(CONFIG["caminhos"]["padraoDeclaracoes"]))


def data_root():
    """The folder that holds the source data (data/), outside the repository of the code."""
    return path("raizDados").resolve()


def neo4j_setting(field):
    """Default Neo4j connection setting: the environment variable if set, otherwise the configured value."""
    n = CONFIG["neo4j"]
    return os.environ.get(n["variaveisAmbiente"][field], n[field])


def is_repeatable(cardinality):
    """A composition is repeatable when its maximum is '*'."""
    return CONFIG["cardinalidades"].get(cardinality, {}).get("maximo") == "*"


def is_mandatory(cardinality):
    return CONFIG["cardinalidades"].get(cardinality, {}).get("minimo", 0) >= 1
