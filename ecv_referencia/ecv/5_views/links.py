"""Page names of the views and the links between them.

Every renderer links to other views through these functions. The page set (EXISTING) is filled
with the catalogue of the graph being shown: a link to a page that does not exist is rendered as
plain text, so there are never broken links.
"""
import re
from html import escape

EXISTING = set()
EDIT_BASE = None          # set by the web application ("/alteracoes"): the views then link each rule and property to its edit form


def edit_link(layer, op, title="editar", **selection):
    """'✎' link to the guided form of an operation (only in the web application)."""
    if not EDIT_BASE:
        return ""
    from urllib.parse import urlencode
    query = urlencode({"camada": layer, "op": op, **{k: v for k, v in selection.items() if v}})
    return f' <a class="edit" href="{EDIT_BASE}?{query}" title="{_e(title)}">✎</a>'


def _e(x):
    return escape("" if x is None else str(x))


def slug(text):
    return re.sub(r"[^A-Za-z0-9_-]+", "_", str(text)).strip("_")


def _property_slug(key):
    """'USM:Medicao.valor' -> 'Medicao_valor'."""
    return slug(key.split(":", 1)[-1].replace(".", "_"))


def model_page(level, name):
    return f"{level.lower()}_{slug(name)}"


def rules_page(hlm):
    return f"regras_{slug(hlm)}"


def projections_page(hlm):
    return f"projecoes_{slug(hlm)}"


def gaps_page(hlm):
    return f"lacunas_{slug(hlm)}"


def decision_page(key):
    return f"decisao_{_property_slug(key)}"


def dependencies_page(key):
    return f"dependencias_{_property_slug(key)}"


def impact_page(key):
    return f"impacto_{_property_slug(key)}"


def rule_page(rule_id):
    return f"regra_{slug(rule_id)}"


def profile_page(name):
    return f"perfil_{slug(name)}"


def validation_page(example):
    return f"validacao_{slug(example)}"


def set_existing(pages):
    EXISTING.clear()
    EXISTING.update(pages)
    EXISTING.add("index")


def exists(page):
    return page in EXISTING


def href(page, anchor=None):
    """Address of the page (relative), or None when it does not exist."""
    if not exists(page):
        return None
    return f"{page}.html" + (f"#{anchor}" if anchor else "")


def link(page, text, anchor=None, css="", title=None, raw_text=False):
    t = text if raw_text else _e(text)
    tt = f' title="{_e(title)}"' if title else ""
    cl = f' class="{css}"' if css else ""
    h = href(page, anchor)
    return f'<a href="{_e(h)}"{cl}{tt}>{t}</a>' if h else (f'<span{cl}{tt}>{t}</span>' if cl or tt else t)


def property_anchor(key):
    return "p-" + slug(key)


def property_link(key, text=None, owner=None, owner_level=None):
    """Link to a property: its row in the view of the model that holds it."""
    owner_level = owner_level or key.split(":", 1)[0]
    owner = owner or key.split(":", 1)[1].split(".")[0]
    return link(model_page(owner_level, owner), text or key.split(":", 1)[-1], anchor=property_anchor(key), css="prop",
                title=key)


def rule_link(card, text=None):
    """Coloured chip of a rule (by category: RP, RIR, RIC or FN), linking to its card."""
    from .presentation.html import chip
    category = card.get("categoria") or card.get("tipo")
    return chip(category, text or card["id"], card.get("descricao"), href(rule_page(card["id"])))


def is_property_key(key):
    return bool(key) and key.count(":") == 1 and "." in key


def target_link(key, name=None):
    """Target of a restriction: a property (link to its row) or, for a function over a collection, a model."""
    if is_property_key(key):
        return property_link(key, name)
    return _e(name or key or "—")
