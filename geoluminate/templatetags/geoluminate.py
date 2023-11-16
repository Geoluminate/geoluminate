from django import template
from django.conf import settings
from django.db import models
from django.template.loader import render_to_string
from django.templatetags.static import static
from django.urls import reverse_lazy
from django.utils.safestring import mark_safe
from quantityfield import settings as qsettings

from geoluminate.contrib.core.forms import GenericDescriptionForm
from geoluminate.utils import get_filter_params

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
def brand(icon_or_logo: str):
    """Returns either the website logo or icon static url for use in img tags"""
    if icon_or_logo == "icon":
        return static("img/brand/icon.svg")
    elif icon_or_logo == "logo":
        return static("img/brand/logo.svg")
    raise ValueError("icon_or_logo must be either 'icon' or 'logo'")


@register.simple_tag
def icon(object_str: str):
    """Retrieves the default icon for a given object."""
    # deliberate nonsense as default because fontawesome already does a good job of alerting the dev to a non-existing icon
    default = "fa-solid fa-"
    return settings.GEOLUMINATE_ICONS.get(object_str, default)


@register.filter
def verbose_name(instance, field_name=None):
    """
    Returns verbose_name for a field.
    """
    if field_name:
        return instance._meta.get_field(field_name).verbose_name.capitalize()
    return instance._meta.verbose_name


@register.filter
def verbose_name_plural(model_or_queryset):
    """
    Returns verbose_name_plural for a given model.
    """
    if isinstance(model_or_queryset, models.QuerySet):
        return model_or_queryset.model._meta.verbose_name_plural
    return model_or_queryset._meta.verbose_name_plural


@register.filter
def addstr(arg1, arg2):
    """concatenate arg1 & arg2"""
    return str(arg1) + str(arg2)


@register.simple_tag
def render_profile_image(profile, width=75, height=None, extra_classes=""):
    """Renders a default img tag for the given profile. If the profile.image is None, renders a default icon if no image is set."""
    if profile and profile.image:
        el = f'<img src="{profile.image.url}" class="rounded-circle {extra_classes}"'
        if height:
            el += f' height="{height}"'
        if width:
            el += f' width="{width}"'
        return mark_safe(el + " />")
    else:
        default_icon = (
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" fill="currentColor" class="bi bi-person-fill'
            f' {extra_classes}" viewBox="0 0 16 16"><path d="M11 6a3 3 0 1 1-6 0 3 3 0 0 1 6 0z"/><path'
            ' fill-rule="evenodd" d="M0 8a8 8 0 1 1 16 0A8 8 0 0 1 0 8zm8-7a7 7 0 0 0-5.468 11.37C3.242 11.226 4.805'
            ' 10 8 10s4.757 1.225 5.468 2.37A7 7 0 0 0 8 1z"/></svg>'
        )

        return mark_safe(default_icon)


@register.simple_tag
def render_contributor_icon(contributor, extra_classes=""):
    return render_to_string(
        "contributors/icon.html", context={"contributor": contributor, "extra_classes": extra_classes}
    )


@register.simple_tag(takes_context=True)
def filter_params(context):
    """Returns curent filter params as a string"""
    request = context["request"]
    return get_filter_params(request)


@register.inclusion_tag("core/description_form.html", takes_context=True)
def render_description_form(context, obj):
    context.update({"form": GenericDescriptionForm(obj=obj)})
    return context


@register.simple_tag
def create_url(object_list):
    model = object_list.model
    return reverse_lazy(f"{model._meta.model_name}s:add")


@register.simple_tag(takes_context=True)
def page_menu(context):
    if context.get("page_menu") or context.get("actions_menu"):
        return render_to_string("menu/page_menu.html", context=context.flatten())
    return ""
