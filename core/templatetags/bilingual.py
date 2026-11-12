"""Template helpers for the English / Bangla interface.

    {% load bilingual %}
    {% t "Find a donor" "রক্তদাতা খুঁজুন" %}      fixed text written in the template
    {{ form_label|tr }}                            text produced by Python code (looked up in core/bn.py)
    {{ 42|lnum }} / {{ date|date:"j M Y"|lnum }}   Bangla digits when Bangla is active
"""
import re

from django import template
from django.utils import translation
from django.utils.html import escape
from django.utils.safestring import SafeString, mark_safe

from core.bn import BN

register = template.Library()

_DIGITS = str.maketrans("0123456789", "০১২৩৪৫৬৭৮৯")


def is_bn():
    return (translation.get_language() or "en").startswith("bn")


@register.simple_tag
def t(english, bangla):
    return bangla if is_bn() else english


@register.filter
def tr(value):
    """Translate a string produced by Python (labels, help texts, messages, choice names)."""
    if value is None or value == "":
        return value
    text = str(value)
    if not is_bn():
        return value
    hit = BN.get(text.strip())
    if hit is None:
        return value
    if isinstance(value, SafeString):
        return mark_safe(hit)
    return hit


@register.filter
def lnum(value):
    if value is None:
        return ""
    text = str(value)
    if not is_bn():
        return value
    return text.translate(_DIGITS)


@register.filter
def lang_is_bn(_value=None):
    return is_bn()


@register.filter
def place(obj):
    if obj is None:
        return ""
    if is_bn() and getattr(obj, "name_bn", ""):
        return obj.name_bn
    return obj.name


@register.filter
def plural_en(count, words="unit,units"):
    """English plural helper that is a no-op for Bangla."""
    one, many = words.split(",")
    return one if str(count) == "1" else many


@register.filter
def first_para(text):
    """First paragraph of a plain-text body."""
    return (text or "").strip().split("\n\n")[0]


_NUMBERED = re.compile(r"^\s*\d+[.)]\s+")


@register.filter
def prose(text):
    """Turn the plain-text pages (About, Terms, ...) into tidy HTML.

    * a short first line without end punctuation followed by more lines becomes a heading,
    * a block where every line starts with "1." / "2." becomes an ordered list,
    * everything else is a paragraph (single line breaks kept).
    """
    out = []
    for block in re.split(r"\n\s*\n", (text or "").strip()):
        lines = [ln.strip() for ln in block.splitlines() if ln.strip()]
        if not lines:
            continue
        if all(_NUMBERED.match(ln) for ln in lines):
            items = "".join(f"<li>{escape(_NUMBERED.sub('', ln))}</li>" for ln in lines)
            out.append(f"<ol>{items}</ol>")
            continue
        if len(lines) > 1 and len(lines[0]) <= 60 and not lines[0].endswith((".", "।", ":", "!", "?")):
            out.append(f"<h2>{escape(lines[0])}</h2>")
            lines = lines[1:]
        out.append("<p>" + "<br>".join(escape(ln) for ln in lines) + "</p>")
    return mark_safe("\n".join(out))
