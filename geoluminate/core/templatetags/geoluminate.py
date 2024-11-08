from django import template
from django.db import models

# import flatattrs
from django.template.loader import render_to_string
from django.urls import reverse
from quantityfield import settings as qsettings

register = template.Library()
ureg = qsettings.DJANGO_PINT_UNIT_REGISTER
ureg.default_format = ".2f~P"


@register.simple_tag(takes_context=True)
def is_active(context, url):
    if context["request"].path.startswith(url):
        return "active"
    return ""


@register.filter
def unit(unit):
    """Renders HTML of the specified unit"""
    u = ureg.Unit(unit)
    return f"{u:~H}"


@register.simple_tag
def render_field(obj, fname):
    """Takes an object and a single field and renders it using the correct template based on the field type."""
    FMAP = {
        models.ForeignKey: "components/fields/relation.html",
    }
    field = obj._meta.get_field(fname)
    value = getattr(obj, fname)
    # if field.choices:
    # return getattr(obj, f"get_{fname}_display")()
    if field.one_to_many:
        return render_to_string("components/fields/one_to_many.html", {"field": field, "value": value.all()})
    if field.is_relation:
        return render_to_string("components/fields/relation.html", {"field": field, "value": value})
    if field.is_quantity:
        return f"{value:~H}"
    return value


@register.simple_tag
def get_field(obj, fname):
    return (obj._meta.get_field(fname), getattr(obj, fname))


@register.simple_tag
def get_fields(obj, fields):
    return [(obj._meta.get_field(f), getattr(obj, f)) for f in fields]


@register.simple_tag
def edit_url(obj, fields=None):
    url = reverse(f"{obj._meta.model_name}-update", kwargs={"pk": obj.pk})  # Adjust the URL name as needed
    if fields:
        return f"{url}?fields={','.join(fields)}"
    return url


@register.simple_tag
def avatar_url(contributor, **kwargs):
    """Renders a default img tag for the given profile. If the profile.image is None, renders a default icon if no image is set."""

    if not contributor:
        # for anonymous users
        return render_to_string("icons/user.svg")

    if contributor.image:
        return contributor.image.url
    else:
        return render_to_string("icons/user.svg")
