from django import template

# from django.conf import settings
from django.template.loader import render_to_string
from django.templatetags.static import static
from quantityfield import settings

from geoluminate.models import GlobalConfiguration
from geoluminate.utils import get_filter_params

register = template.Library()
ureg = settings.DJANGO_PINT_UNIT_REGISTER


@register.simple_tag(takes_context=True)
def is_active(context, url):
    if context["request"].path.startswith(url):
        return "active"
    return ""


@register.simple_tag
def menu(menu, template=None):
    """Renders a menu"""
    if not template:
        template = menu.template_name
    return render_to_string(template, {"menu": menu})


@register.filter
def unit(unit):
    """Renders HTML of the specified unit"""
    u = ureg.Unit(unit)
    return f"{u:~H}"


@register.simple_tag
def logo():
    """Gets the correct URL for the logo as set in `GlobalConfiguration`."""
    logo = GlobalConfiguration.get_solo().logo
    if logo:
        return logo.url
    return static("geoluminate/img/brand/logo.svg")


@register.simple_tag
def icon():
    """Gets the correct URL for the icon as set in `GlobalConfiguration`."""
    icon = GlobalConfiguration.get_solo().icon
    if icon:
        return icon.url
    return static("geoluminate/img/brand/icon.svg")


@register.filter
def verbose_name(instance, field_name=None):
    """
    Returns verbose_name for a field.
    """
    if field_name:
        return instance._meta.get_field(field_name).verbose_name.capitalize()
    return instance._meta.verbose_name


@register.filter
def addstr(arg1, arg2):
    """concatenate arg1 & arg2"""
    return str(arg1) + str(arg2)


@register.filter
def get_obj_attr(obj):
    try:
        value = obj.field.queryset.get(pk=obj.initial)
    except AttributeError:
        value = obj.initial

    if getattr(obj.field, "choices", False):
        for choice in obj.field.choices:
            if value == choice[0]:
                value = choice[1]

    return '<tr><td class="w-50">{}:</td><td>{}</td></tr>'.format(obj.name.replace("_", " ").title(), value)


@register.simple_tag(takes_context=True)
def filter_params(context):
    """Returns curent filter params as a string"""
    request = context["request"]
    return get_filter_params(request)
