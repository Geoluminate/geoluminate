from django import template
from django.core.exceptions import FieldDoesNotExist
from django.db import models

# import flatattrs
from django.template.loader import render_to_string
from django.urls import reverse
from quantityfield import settings as qsettings

from fairdm.registry import registry

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
    if isinstance(unit, str):
        # if a string is passed, create a unit from it (e.g. "m" or "m/s")
        u = ureg.Unit(unit)
    elif isinstance(unit, ureg.Unit):
        # if a unit is passed, use it directly (e.g. calling the value directly on an instance instance.value.units)
        u = unit

    return f"{u:~H}"


@register.simple_tag
def get_registry_info(arg):
    if isinstance(arg, type) and issubclass(arg, models.Model):  # Model class
        model_class = arg

    elif isinstance(arg, models.QuerySet):  # QuerySet
        model_class = arg.model
    elif isinstance(arg, models.Model):  # Model instance
        model_class = arg._meta.model
    else:
        raise TypeError("Argument must be a Django model class, queryset, or model instance.")

    return registry.get_model(model_class)


# @register.simple_tag
# def render_field(obj, fname):
#     """Takes an object and a single field and renders it using the correct template based on the field type."""
#     FMAP = {
#         models.ForeignKey: "components/fields/relation.html",
#     }
#     field = obj._meta.get_field(fname)
#     value = getattr(obj, fname)
#     # if field.choices:
#     # return getattr(obj, f"get_{fname}_display")()
#     if field.one_to_many:
#         return render_to_string("components/fields/one_to_many.html", {"field": field, "value": value.all()})
#     if field.is_relation:
#         return render_to_string("components/fields/relation.html", {"field": field, "value": value})
#     if field.is_quantity:
#         return f"{value:~H}"
#     return value


@register.simple_tag
def render_field(obj, fname):
    """Takes an object and a single field and renders it using the correct template based on the field type."""

    templates = ["fieldsets/fields/default.html"]

    try:
        field = obj._meta.get_field(fname)
        field_type = field.__class__.__name__.lower()
        templates = [f"fieldsets/fields/{field_type}.html", *templates]
    except FieldDoesNotExist:
        field = None

    value = getattr(obj, fname)

    choice_label = None
    if field and field.choices:
        choice_label = dict(field.choices).get(value)

    return render_to_string(
        templates,
        {
            "field": field,
            "value": value,
            "choice_label": choice_label,
        },
    )


@register.inclusion_tag("fieldsets/fieldset.html")
def render_fieldsets(obj, fieldsets):
    """Renders a list of fieldsets for the given object."""

    return {
        "object": obj,
        "fieldsets": fieldsets,
    }


@register.inclusion_tag("fieldsets/row.html")
def render_row(obj, row):
    if isinstance(row, str):
        row = [row]
    return {
        "fields": row,
        "object": obj,
    }


@register.simple_tag
def display_url(url):
    return url.replace("https://", "").replace("http://", "").replace("www.", "")


@register.simple_tag
def get_field(obj, fname):
    try:
        return obj._meta.get_field(fname)
    except FieldDoesNotExist:
        return None


@register.simple_tag
def get_field_and_value(obj, fname):
    return {
        "field": obj._meta.get_field(fname),
        "value": getattr(obj, fname),
    }


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
