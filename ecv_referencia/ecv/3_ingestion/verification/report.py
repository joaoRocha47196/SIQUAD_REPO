"""The verification report: a list of problems, each an error (blocks materialisation) or a warning."""
from dataclasses import dataclass


@dataclass
class Problem:
    code: str          # spec code (S-...) or invariant (I1 ... I13)
    severity: str      # "erro" | "aviso"
    where: str
    message: str

    def __str__(self):
        return f"[{self.severity.upper():5}] {self.code:6} {self.where}: {self.message}"


class Report:
    def __init__(self):
        self.problems = []

    def error(self, code, where, message):
        self.problems.append(Problem(code, "erro", where, message))

    def warning(self, code, where, message):
        self.problems.append(Problem(code, "aviso", where, message))

    @property
    def errors(self):
        return [p for p in self.problems if p.severity == "erro"]

    @property
    def warnings(self):
        return [p for p in self.problems if p.severity == "aviso"]

    @property
    def valid(self):
        return not self.errors

    def summary(self):
        return f"{len(self.errors)} erro(s), {len(self.warnings)} aviso(s)"
