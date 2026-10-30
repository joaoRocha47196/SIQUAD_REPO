"""Resolution of paths in the ECM structure.

A path is relative to a model (the model where a rule lives, or the HLM in a projection or a
profile) and is made of the roles of the compositions to follow, optionally ending in a property:

    Leitura.Medicao.valor      (from the HLM Dispositivo)
    Linha.numero               (from the SM Linhas)
    Linhas.Linha               (from the HLM Fatura: ends in a model, the collection)
    valor                      (from the USM Medicao)

The role of a composition is, by default, the name of the composed model; a composition may
declare another one ("papel").
"""
from dataclasses import dataclass, field

from ecv import config


class PathError(ValueError):
    pass


@dataclass
class Resolution:
    origin: tuple                                   # (level, name) where the path starts
    path: str
    steps: list = field(default_factory=list)       # [(role, level, name, cardinality)]
    prop: dict | None = None                        # the final property, if the path ends in one
    owner: tuple | None = None                      # (level, name) of the model that holds the property

    @property
    def target(self):
        """(level, name) of the last model reached."""
        return (self.steps[-1][1], self.steps[-1][2]) if self.steps else self.origin

    @property
    def ends_in_model(self):
        return self.prop is None

    @property
    def repeatable(self):
        """True when the path crosses a repeatable composition (it denotes a collection)."""
        return any(config.is_repeatable(card) for *_, card in self.steps)

    @property
    def property_key(self):
        if self.prop is None:
            return None
        return property_key(self.owner[0], self.owner[1], self.prop["nome"])

    @property
    def type(self):
        return self.prop.get("tipo") if self.prop else None


def property_key(level, owner, name):
    """Unique key of a property in the graph: 'USM:Medicao.valor'."""
    return f"{level}:{owner}.{name}"


def resolve(decl, level, name, path):
    """Resolve a path from (level, name). Raises PathError if it does not exist."""
    if not path:
        raise PathError("caminho vazio")
    if decl.model(level, name) is None:
        raise PathError(f"o nó de partida {level} {name} não existe")
    segments = path.split(".")
    res = Resolution(origin=(level, name), path=path)
    current = (level, name)
    for i, seg in enumerate(segments):
        last = i == len(segments) - 1
        comp = next((c for c in decl.compositions(*current) if c[0] == seg), None)
        if comp is not None:
            role, child_level, child, card = comp
            if decl.model(child_level, child) is None:
                raise PathError(f"'{seg}' em '{path}' refere {child_level} {child}, que não está declarado")
            res.steps.append((role, child_level, child, card))
            current = (child_level, child)
            continue
        if last:
            prop = decl.get_property(*current, seg)
            if prop is not None:
                res.prop = prop
                res.owner = current
                return res
        raise PathError(f"'{seg}' não é uma composição nem uma propriedade de {current[0]} {current[1]} "
                        f"(caminho '{path}' a partir de {level} {name})")
    return res


def try_resolve(decl, level, name, path):
    try:
        return resolve(decl, level, name, path)
    except PathError:
        return None


def all_property_paths(decl, level, name, prefix="", visited=()):
    """Paths of every property reachable from a model."""
    if (level, name) in visited:
        return []
    out = [f"{prefix}{p['nome']}" for p in decl.properties(level, name)]
    for role, child_level, child, _ in decl.compositions(level, name):
        out.extend(all_property_paths(decl, child_level, child, f"{prefix}{role}.", visited + ((level, name),)))
    return out


def occurrences(decl, hlm):
    """Every model reachable from a HLM, with the path (prefix) of each occurrence: [(prefix, level, name)].

    The HLM itself has prefix ''. A model appears once per path that reaches it (the USM Morada
    appears as 'Emitente.Morada' and as 'Cliente.Morada').
    """
    out = [("", "HLM", hlm)]

    def descend(level, name, prefix):
        for role, child_level, child, _ in decl.compositions(level, name):
            p = f"{prefix}{role}"
            out.append((p, child_level, child))
            descend(child_level, child, p + ".")

    descend("HLM", hlm, "")
    return out


def join(prefix, path):
    return f"{prefix}.{path}" if prefix else path


def expand(decl, hlm, pattern):
    """Expand a projection path ('Leitura.*', 'Identificacao.estado') into property paths."""
    if pattern == "*":
        return all_property_paths(decl, "HLM", hlm)
    if pattern.endswith(".*"):
        base = pattern[:-2]
        res = resolve(decl, "HLM", hlm, base)
        if not res.ends_in_model:
            raise PathError(f"'{pattern}': '{base}' é uma propriedade, não um modelo")
        return all_property_paths(decl, *res.target, prefix=base + ".")
    res = resolve(decl, "HLM", hlm, pattern)
    if res.ends_in_model:
        raise PathError(f"'{pattern}' termina num modelo; use '{pattern}.*'")
    return [pattern]
