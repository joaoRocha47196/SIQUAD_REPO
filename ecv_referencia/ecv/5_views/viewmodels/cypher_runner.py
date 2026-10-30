"""Running, directly in Neo4j, the Cypher queries equivalent to the ViewModels (folder cypher/).

Each file may hold several statements separated by ';'. Returns, for each statement, its rows.
"""
from pathlib import Path

FOLDER = Path(__file__).parent / "cypher"


def statements(file_name):
    text = (FOLDER / file_name).read_text(encoding="utf-8")
    lines = [line for line in text.splitlines() if not line.strip().startswith("//")]
    return [q.strip() for q in "\n".join(lines).split(";") if q.strip()]


def run(driver, file_name, database=None, **params):
    results = []
    with driver.session(database=database) as s:
        for q in statements(file_name):
            results.append([dict(r) for r in s.run(q, **params)])
    return results
