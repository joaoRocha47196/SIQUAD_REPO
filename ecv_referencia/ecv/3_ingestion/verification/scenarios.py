"""Scenario checks: projections (I9), profiles (fixed values, I9; applicability, I10) and unused
functions and contexts (I13)."""
from ecv import config

from .. import paths as P
from .. import rule_parts as R

MODEL_NAME = config.NAME_PATTERNS["modelo"]


class ScenarioChecks:
    """Mixin of Verifier: expects self.decl, self.report and self.plausible_values (RuleChecks)."""

    def check_projections(self):
        for name, proj in self.decl.projections.items():
            where = f"projeção {name}"
            if not MODEL_NAME.match(name):
                self.report.error("S-PROJ", where, "nome em PascalCase")
            hlm = proj.get("hlm")
            if hlm not in self.decl.hlm:
                self.report.error("S-PROJ", where, f"HLM '{hlm}' não declarado")
                continue
            expanded = {}
            for key in ("obrigatorias", "permitidas"):
                if not isinstance(proj.get(key), list):
                    self.report.error("S-PROJ", where, f"'{key}' é uma lista (pode ser vazia)")
                    continue
                expanded[key] = set()
                for pattern in proj[key]:
                    try:
                        expanded[key] |= set(P.expand(self.decl, hlm, pattern))
                    except P.PathError as e:
                        self.report.error("I9", where, f"{key}: {e}")
            both = expanded.get("obrigatorias", set()) & expanded.get("permitidas", set())
            if both:
                self.report.error("I9", where, f"propriedades simultaneamente obrigatórias e permitidas: {sorted(both)}")

    def projected_paths(self, projection):
        proj = self.decl.projections.get(projection, {})
        out = set()
        for key in ("obrigatorias", "permitidas"):
            for pattern in proj.get(key, []):
                try:
                    out |= set(P.expand(self.decl, proj["hlm"], pattern))
                except (P.PathError, KeyError):
                    pass
        return out

    def check_profiles(self):
        for name, profile in self.decl.profiles.items():
            where = f"perfil {name}"
            if not MODEL_NAME.match(name):
                self.report.error("S-PERFIL", where, "nome em PascalCase")
            proj = self.decl.projections.get(profile.get("projecao"))
            if proj is None:
                self.report.error("S-PERFIL", where, f"projeção '{profile.get('projecao')}' não declarada")
                continue
            hlm = proj.get("hlm")
            if "hlm" in profile and profile["hlm"] != hlm:
                self.report.error("S-PERFIL", where, f"o HLM do perfil ({profile['hlm']}) difere do da projeção ({hlm})")
            fixed = self._check_fixed_values(where, profile, hlm)
            self.check_profile_applicability(name, hlm, self.projected_paths(profile["projecao"]), fixed)

    def _check_fixed_values(self, where, profile, hlm):
        fixed = set()
        for fx in profile.get("fixa", []):
            keys = [k for k in ("propriedade", "contexto") if k in fx]
            if len(keys) != 1 or "valor" not in fx:
                self.report.error("S-PERFIL", where, "cada fixação tem exatamente um de 'propriedade' ou 'contexto', e 'valor'")
                continue
            if "contexto" in fx:
                if fx["contexto"] not in self.decl.contexts:
                    self.report.error("S-PERFIL", where, f"contexto externo '{fx['contexto']}' não declarado")
                continue
            res = P.try_resolve(self.decl, "HLM", hlm, fx["propriedade"])
            if res is None or res.ends_in_model:
                self.report.error("I9", where, f"'{fx['propriedade']}' não é uma propriedade do HLM {hlm}")
                continue
            fixed.add(fx["propriedade"])
            plausible = self.plausible_values(*res.owner, res.prop["nome"])
            if plausible is not None and fx["valor"] not in plausible:
                self.report.error("I9", where, f"o valor fixado {fx['valor']!r} para {fx['propriedade']} não é plausível")
        return fixed

    def check_profile_applicability(self, name, hlm, projected, fixed):
        """I10: relevant rules whose condition reads properties neither projected nor fixed in the profile.

        Grouped by the set of missing properties, so there is one warning per cause."""
        available = projected | fixed
        groups = {}
        for prefix, level, model in P.occurrences(self.decl, hlm):
            for site in self.decl.rules():
                if (site.level, site.model) != (level, model) or not R.condition(site.rule):
                    continue
                read = []
                for x in R.paths_read(site.rule):
                    full = P.join(prefix, x["caminho"])
                    res = P.try_resolve(self.decl, "HLM", hlm, full)
                    if res is not None and not res.ends_in_model:
                        read.append((x["parte"], full))
                missing = sorted({p for part, p in read if part == "termo" and p not in available})
                relevant = any(p in available for _, p in read)
                if missing and relevant:
                    groups.setdefault(tuple(missing), []).append(site.id)
        for missing, ids in groups.items():
            self.report.warning("I10", f"perfil {name}",
                                f"{len(ids)} regra(s) não avaliável(is), porque a condição lê {list(missing)}, "
                                f"que não está na projeção nem é fixado no perfil: {', '.join(ids)}")

    def check_unused(self):
        called = {c["funcao"] for site in self.decl.rules() for _, _, c in R.function_calls(site.rule)
                  if isinstance(c, dict) and c.get("funcao")}
        for f in self.decl.functions:
            if f not in called:
                self.report.warning("I13", f"função {f}", "declarada mas não chamada por nenhuma regra")
        used = set()
        for site in self.decl.rules():
            used |= set(R.contexts_used(self.decl, site.rule))
        for profile in self.decl.profiles.values():
            used |= {fx["contexto"] for fx in profile.get("fixa", []) if "contexto" in fx}
        for ctx in self.decl.contexts:
            if ctx not in used:
                self.report.warning("I13", f"contexto {ctx}", "declarado mas não usado")
