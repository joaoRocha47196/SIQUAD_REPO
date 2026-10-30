"""Verification of an ECV declaration, before anything is materialised.

Two levels (thesis, section "Verificação da declaração"):
  1. specs: each entity on its own (required attributes, shape, names);
  2. invariants: what can only be checked with every entity loaded (I1 to I13).

An error stops materialisation; a warning does not, but is reported. I1 to I9 follow the table of
invariants of the thesis; I10 to I13 were added in this reference version (specs/declaracao/README.md).
"""
from .report import Problem, Report
from .rules import RuleChecks
from .scenarios import ScenarioChecks
from .structure import StructureChecks
from .value_forms import form_error


class Verifier(StructureChecks, RuleChecks, ScenarioChecks):
    def __init__(self, decl):
        self.decl = decl
        self.report = Report()

    def run(self):
        self.check_schema()
        self.check_header()
        self.check_contexts()
        self.check_functions()
        self.check_models()
        self.check_rules()
        self.check_projections()
        self.check_profiles()
        self.check_unused()
        return self.report


def verify(decl):
    """Verify a Declaration and return its Report."""
    return Verifier(decl).run()


__all__ = ["verify", "Verifier", "Report", "Problem", "form_error"]
