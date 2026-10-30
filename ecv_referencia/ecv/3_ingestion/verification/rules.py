"""Rule checks: identifier and nature, the shape of each rule type (I4), restrictions and terms
(paths, operators per base type, value forms: I3, I5), plausible values (I7), the position of the
rule (I8), derived contexts (I11) and descriptions (I12)."""
from ecv import config

from .. import paths as P
from .. import rule_parts as R
from ..descriptions import derive
from .value_forms import form_error

RULE_ID = config.NAME_PATTERNS["regra"]


class RuleChecks:
    """Mixin of Verifier: expects self.decl (Declaration) and self.report (Report)."""

    def plausible_values(self, level, model, prop_name):
        """Plausible values of a property (RP with IN or EQUALS on it), or None."""
        prop = self.decl.get_property(level, model, prop_name)
        if not prop:
            return None
        values = None
        for r in prop.get("regras", []):
            if r.get("natureza") != "plausibilidade":
                continue
            rs = R.restriction(r) or {}
            if rs.get("operador") == "IN":
                values = (values or set()) | set(rs.get("valor", []))
            elif rs.get("operador") == "EQUALS":
                values = (values or set()) | {rs.get("valor")}
        return values

    def check_rules(self):
        ids = {}
        for site in self.decl.rules():
            self.check_rule(site, ids)

    def check_rule(self, site, ids):
        rule = site.rule
        rule_id = rule.get("id", "?")
        where = f"{rule_id} ({site.scope})"
        if rule_id in ids:
            self.report.error("S-REGRA", where, f"identificador repetido (também em {ids[rule_id]})")
        ids[rule_id] = site.scope
        rule_type = config.NATURES.get(rule.get("natureza"))
        if rule_type is None:
            self.report.error("S-REGRA", where, f"natureza tem de ser uma de {list(config.NATURES)}")
            return
        if not RULE_ID.match(rule_id):
            self.report.error("S-REGRA", where, "id na forma TIPO-ASSUNTO[-QUALIFICADOR], em maiúsculas")
        elif rule_id.split("-")[0] != rule_type:
            self.report.error("S-REGRA", where, f"o prefixo do id tem de ser {rule_type} (natureza {rule.get('natureza')})")
        if not rule.get("descricao"):
            self.report.warning("S-REGRA", where, "sem descrição (é derivada ao registar ou com python -m ecv descricoes --escrever)")
        self._check_rule_shape(rule, rule_type, where)

        restriction, condition = R.restriction(rule), R.condition(rule)
        if restriction is not None:
            self.check_restriction(site, where, restriction)
        for k, term in enumerate(condition):
            self.check_term(site, f"{where} termo {k + 1}", term)

        read = [x["caminho"] for x in R.paths_read(rule)]
        if site.prop is not None:            # a rule on a property only reads that property
            others = [p for p in read if p != site.prop["nome"]]
            if others:
                self.report.error("I3", where, f"vive na propriedade {site.prop['nome']} mas lê {others}; "
                                  "deve viver no nó mais baixo que contém tudo o que lê")
        targets = set(R.restriction_paths(rule)) if not R.is_function(restriction) else set()
        common = targets & set(R.condition_paths(rule))
        if common:
            self.report.error("I6", where, f"a condição lê o alvo da restrição: {sorted(common)}")
        self.check_position(site, where, read)

        used = R.contexts_used(self.decl, rule)
        if "contextosExternos" in rule and sorted(rule["contextosExternos"]) != sorted(used):
            self.report.warning("I11", where, f"contextosExternos declarados {rule['contextosExternos']} ≠ usados {used}")
        derived = derive(rule, site.level, site.model)
        if rule.get("descricao") and rule["descricao"] != derived:
            self.report.warning("I12", where, f"a descrição não corresponde à derivada: '{derived}'")

    def _check_rule_shape(self, rule, rule_type, where):
        """I4: an RP has a restriction and no condition; an RIR has both; an RIC has a condition and a conclusion."""
        restriction, condition = R.restriction(rule), R.condition(rule)
        if rule_type == "RP" and (restriction is None or condition):
            self.report.error("I4", where, "uma RP tem restrição e não tem condição de aplicabilidade")
        if rule_type == "RIR" and (restriction is None or not condition):
            self.report.error("I4", where, "uma RIR tem condição de aplicabilidade e restrição")
        if rule_type == "RIC":
            if restriction is not None or not condition:
                self.report.error("I4", where, "uma RIC tem condição de aplicabilidade e não tem restrição")
            if len(rule.get("mensagem", "")) < 10:
                self.report.error("I4", where, "uma RIC tem mensagem de conclusão (pelo menos 10 caracteres)")
            c = rule.get("conclusao")
            if c is not None and (c.get("tipo") not in config.CONCLUSION_TYPES or not c.get("valor")):
                self.report.error("S-REGRA", where, "conclusao = {tipo: ACAO|ESTADO, valor}")
        elif "mensagem" in rule:
            self.report.error("S-REGRA", where, "numa RP ou numa RIR a mensagem pertence à restrição, não à regra")
        if "conclusao" in rule and rule_type != "RIC":
            self.report.error("S-REGRA", where, "só uma RIC tem 'conclusao'")

    def _resolve_or_report(self, site, where, path, code="I3"):
        res = P.try_resolve(self.decl, site.level, site.model, path)
        if res is None:
            try:
                P.resolve(self.decl, site.level, site.model, path)
            except P.PathError as e:
                self.report.error(code, where, str(e))
        return res

    def check_restriction(self, site, where, restriction):
        op = restriction.get("operador")
        if len(restriction.get("mensagem", "")) < 10:
            self.report.error("S-RESTR", where, "a restrição tem mensagem de não conformidade (pelo menos 10 caracteres)")
        if op not in config.OPERATORS:
            self.report.error("S-RESTR", where, f"operador '{op}' fora do catálogo")
            return
        if op in config.FUNCTION_OPERATORS:
            if "propriedade" in restriction:
                self.report.error("S-RESTR", where, "numa restrição por função os alvos são os argumentos da chamada")
            self.check_call(site, where, op, restriction.get("chamada"))
            return
        if not restriction.get("propriedade"):
            self.report.error("S-RESTR", where, "uma restrição tipificada tem exatamente um alvo ('propriedade')")
            return
        res = self._resolve_or_report(site, where, restriction["propriedade"])
        if res is None:
            return
        if res.ends_in_model:
            self.report.error("S-RESTR", where, f"o alvo '{restriction['propriedade']}' é um modelo; use uma função para coleções")
            return
        self.check_operator(where, op, res.type, restriction.get("valor"))

    def check_term(self, site, where, term):
        op = term.get("operador")
        if op not in config.OPERATORS:
            self.report.error("S-TERMO", where, f"operador '{op}' fora do catálogo")
            return
        if op in config.FUNCTION_OPERATORS:
            self.check_call(site, where, op, term.get("chamada"))
            return
        if not term.get("propriedade"):
            self.report.error("S-TERMO", where, "um termo tipificado tem 'propriedade'")
            return
        res = self._resolve_or_report(site, where, term["propriedade"])
        if res is None:
            return
        if res.ends_in_model:
            self.report.error("S-TERMO", where, f"'{term['propriedade']}' é um modelo, não uma propriedade")
            return
        if "contexto" in term:
            self._check_context_term(where, term, op, res)
            return
        self.check_operator(where, op, res.type, term.get("valor"))
        if op in ("EQUALS", "IN"):            # I7: values of the condition within the plausible values
            plausible = self.plausible_values(*res.owner, res.prop["nome"])
            used = term.get("valor") if op == "IN" else [term.get("valor")]
            if plausible is not None and isinstance(used, list):
                outside = [v for v in used if v not in plausible]
                if outside:
                    self.report.warning("I7", where, f"{term['propriedade']}: {outside} não pertence(m) aos valores plausíveis "
                                        f"{sorted(map(str, plausible))}; a regra nunca se aplica a esses valores")

    def _check_context_term(self, where, term, op, res):
        if "valor" in term:
            self.report.error("S-TERMO", where, "um termo compara com 'valor' ou com 'contexto', não com ambos")
        ctx = self.decl.contexts.get(term["contexto"])
        if ctx is None:
            self.report.error("S-TERMO", where, f"contexto externo '{term['contexto']}' não declarado")
        elif ctx.get("tipo") != res.type:
            self.report.error("I5", where, f"o contexto {term['contexto']} ({ctx.get('tipo')}) não é comparável com {res.type}")
        if op not in config.CONTEXT_OPERATORS:
            self.report.error("I5", where, f"{op} não compara com um contexto externo")
        if op not in config.OPERATORS_BY_TYPE.get(res.type, []):
            self.report.error("I5", where, f"{op} não é admissível para o tipo {res.type}")

    def check_operator(self, where, op, base_type, value):
        if op not in config.OPERATORS_BY_TYPE.get(base_type, []):
            self.report.error("I5", where, f"{op} não é admissível para o tipo base {base_type}")
            return
        reason = form_error(op, value, base_type)
        if reason:
            self.report.error("S-VALOR", where, f"{op}: {reason} (recebido {value!r})")

    def check_call(self, site, where, op, call_spec):
        if not isinstance(call_spec, dict) or not call_spec.get("funcao"):
            self.report.error("S-CHAMADA", where, f"{op} exige 'chamada': {{funcao, argumentos}}")
            return
        f = self.decl.functions.get(call_spec["funcao"])
        if f is None:
            self.report.error("S-CHAMADA", where, f"a função '{call_spec['funcao']}' não está declarada em 'funcoes'")
            return
        external = bool(f.get("contextosExternos"))
        if external and op != "EXT_FUNCTION":
            self.report.error("I5", where, f"{call_spec['funcao']} usa contexto externo: o operador é EXT_FUNCTION")
        if not external and op != "FUNCTION":
            self.report.error("I5", where, f"{call_spec['funcao']} não usa contexto externo: o operador é FUNCTION")
        args, params = call_spec.get("argumentos", []), f.get("parametros", [])
        if len(args) != len(params):
            self.report.error("S-CHAMADA", where, f"{call_spec['funcao']} tem {len(params)} parâmetro(s); recebeu {len(args)}")
            return
        for arg, param in zip(args, params):
            self._check_argument(site, where, arg, param)

    def _check_argument(self, site, where, arg, param):
        if "caminho" in arg:
            if param.get("papel") != "alvo":
                self.report.error("S-CHAMADA", where, f"{param['nome']} é um parâmetro literal; recebeu o caminho {arg['caminho']}")
            res = self._resolve_or_report(site, where, arg["caminho"])
            if res is None:
                return
            if param.get("colecao") and not res.repeatable:
                self.report.error("S-CHAMADA", where, f"{param['nome']} espera uma coleção; '{arg['caminho']}' não atravessa uma composição repetível")
            if not param.get("colecao") and res.repeatable:
                self.report.error("S-CHAMADA", where, f"{param['nome']} espera um valor; '{arg['caminho']}' é uma coleção")
            if param.get("tipo") == "modelo" and not res.ends_in_model:
                self.report.error("S-CHAMADA", where, f"{param['nome']} espera um modelo (as instâncias); '{arg['caminho']}' é uma propriedade")
        elif "literal" in arg:
            if param.get("papel") != "parametro":
                self.report.error("S-CHAMADA", where, f"{param['nome']} é um alvo (caminho); recebeu um literal")
        else:
            self.report.error("S-CHAMADA", where, "cada argumento é {caminho} ou {literal}")

    def check_position(self, site, where, read):
        """I8: the rule lives on the lowest node that contains everything it reads."""
        if site.prop is not None or not read:
            return
        resolved = [P.try_resolve(self.decl, site.level, site.model, p) for p in read]
        if any(x is None for x in resolved):
            return
        if all(not x.steps for x in resolved) and len(set(read)) == 1 and site.level in ("SM", "USM"):
            self.report.warning("I8", where, f"só lê {read[0]}: poderia viver na propriedade")
            return
        first_steps = {x.steps[0] if x.steps else None for x in resolved}
        if len(first_steps) == 1:
            step = next(iter(first_steps))
            if step is not None and not config.is_repeatable(step[3]):
                self.report.warning("I8", where, f"só lê dentro de {step[1]} {step[2]} (não repetível): poderia viver nesse nó")
