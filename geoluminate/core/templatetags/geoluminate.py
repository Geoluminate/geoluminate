from django import template
from django.db import models

# import flatattrs
from django.forms.utils import flatatt
from django.template.loader import render_to_string
from django.templatetags.static import static
from django.utils.safestring import mark_safe
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
def brand(icon_or_logo: str):
    """Returns either the website logo or icon static url for use in img tags"""
    if icon_or_logo == "icon":
        return static("img/brand/icon.svg")
    elif icon_or_logo == "logo":
        return static("img/brand/logo.svg")
    raise ValueError("icon_or_logo must be either 'icon' or 'logo'")


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
def avatar(profile=None, width="48px", **kwargs):
    """Renders a default img tag for the given profile. If the profile.image is None, renders a default icon if no image is set."""

    if not profile:
        return render_to_string("icons/user.svg")

    if profile.image:
        return mark_safe(f'<img src="{profile.image.url}" width="{width}" {flatatt(kwargs)} />')
    else:
        return render_to_string("icons/user.svg")


@register.simple_tag(takes_context=True)
def page_menu(context):
    if context.get("page_menu") or context.get("actions_menu"):
        return render_to_string("menu/page_menu.html", context=context.flatten())
    return ""


@register.inclusion_tag("core/follow_button.html", takes_context=True)
def follow_button(context, obj):
    """Renders a follow button for the given object"""
    context.update({"object": obj})
    return context


@register.inclusion_tag("core/share_button.html", takes_context=True)
def share_button(context, obj=None, summary=None):
    """Renders a share button for the given object"""
    if obj:
        context.update({"object": obj})
    context.update({"summary": summary})
    return context


@register.simple_tag
def modal_form_attrs(**kwargs):
    attrs = {
        "data-bs-toggle": "modal",
        "data-bs-target": "#formModal",
        "hx-target": "#formModal .modal-body",
        "hx-push-url": "false",
    }
    attrs.update(kwargs)
    return flatatt(attrs)


@register.simple_tag
def render_fields(obj, fields):
    def iter_func():
        for f in fields:
            mf = obj._meta.get_field(f)
            # if mf is a ManyToManyField, we need to get the related objects
            if mf.many_to_many:
                related_objects = getattr(obj, f).all()
                yield (mf.verbose_name, ", ".join([obj for obj in related_objects]), mf.help_text)
            # if mf is a ForeignKey, get the related object and create a link using the get_absolute_url method
            elif mf.is_relation:
                related = getattr(obj, f)
                if related:
                    yield (mf.verbose_name, related, mf.help_text)
                else:
                    yield (mf.verbose_name, "-", mf.help_text)

            else:
                value = getattr(obj, f)
                if value is None:
                    value = "-"
                yield (mf.verbose_name, value, mf.help_text)

    return iter_func


@register.simple_tag
def sidebar_section(obj, heading, fields):
    template = "core/sidebar_section.html"
    fields = render_fields(obj, fields)
    return render_to_string(template, {"heading": heading, "fields": fields})
