"""The validation scenario: the HLM, the projection and the fixed values of a profile, and the values
of the external contexts with their origin."""
import datetime

from ecv.graph.base import read_json
from ecv.views.viewmodels import common as K

from .instance import join


class Scenario:
    """Read from the graph: Perfil -USA-> Projecao -PROJETA-> HLM; OBRIGATORIA and PERMITIDA (expanded paths);
    Perfil -FIXA-> Propriedade | ContextoExterno. Without a profile: the HLM alone (everything available)."""

    def __init__(self, g, profile=None, hlm=None, contexts=None):
        self.g = g
        self.profile, self.projection = profile, None
        self.projected, self.fixed, self.mandatory = None, {}, []
        profile_contexts = {}
        if profile:
            hlm, profile_contexts = self._read_profile(profile)
        elif not hlm:
            raise ValueError("indique o perfil ou o HLM")
        elif g.node("HLM", hlm) is None:
            raise ValueError(f"o HLM '{hlm}' não existe")
        self.hlm = hlm
        self.tree = K.tree(g, hlm)
        self.models = {r["caminho"]: r for r in self.tree if r["tipo"] != "Propriedade" and r["caminho"]}
        self.properties = {r["caminho"]: r for r in self.tree if r["tipo"] == "Propriedade"}
        self._resolve_contexts(contexts or {}, profile_contexts)

    def _read_profile(self, name):
        node = self.g.node("Perfil", name)
        if node is None:
            raise ValueError(f"o perfil '{name}' não existe")
        projection = self.g.first_target(node, "USA")
        self.projection = projection["nome"]
        hlm = self.g.first_target(projection, "PROJETA")["nome"]
        self.mandatory = sorted({e.get("caminho") for e in self.g.outgoing(projection, "OBRIGATORIA")})
        self.projected = set(self.mandatory) | {e.get("caminho") for e in self.g.outgoing(projection, "PERMITIDA")}
        contexts = {}
        for e in self.g.outgoing(node, "FIXA"):
            if e.target.label == "ContextoExterno":
                contexts[e.target["nome"]] = read_json(e.get("valor"))
            else:
                self.fixed[e.get("caminho")] = read_json(e.get("valor"))
        return hlm, contexts

    def _resolve_contexts(self, requested, from_profile):
        """Profile values win over the request, which wins over the defaults (today, the server clock)."""
        now = datetime.datetime.now().replace(microsecond=0)
        defaults = {"dataDeHoje": now.date().isoformat(), "relogioServidor": now.isoformat()}
        self.used_contexts = {c for r, _ in K.rules_of_hlm(self.g, self.hlm) for c in (r.get("contextosExternos") or [])}
        self.contexts, self.context_origin = {}, {}
        for name in sorted(self.used_contexts | set(requested) | set(from_profile)):
            for origin, source in (("fixado no perfil", from_profile), ("indicado no pedido", requested), ("por omissão", defaults)):
                if source.get(name) is not None:
                    self.contexts[name], self.context_origin[name] = source[name], origin
                    break

    def available(self, path):
        """The property is projected or fixed in the profile; a model, if some of its properties are."""
        if self.projected is None or path in self.projected or path in self.fixed:
            return True
        return path in self.models and any(c.startswith(path + ".") for c in self.projected | set(self.fixed))

    def restriction_paths(self, restriction, prefix):
        """Abstract paths (from the HLM) the restriction reads."""
        if restriction is None:
            return []
        if restriction.get("forma") == "funcao":
            return [join(prefix, a["caminho"]) for c in self.g.outgoing(restriction, "CHAMA")
                    for a in read_json(c.get("argumentos"), []) if "caminho" in a]
        return [join(prefix, e.get("caminho")) for e in self.g.outgoing(restriction, "RESTRINGE")]

    def context_rows(self):
        return [{"nome": k, "valor": self.contexts.get(k), "origem": self.context_origin.get(k, "em falta")}
                for k in sorted(set(self.contexts) | self.used_contexts)]
