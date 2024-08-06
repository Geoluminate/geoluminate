from classytags.arguments import Argument
from classytags.core import Options
from classytags.helpers import InclusionTag
from classytags.utils import flatten_context
from django import template
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.db import models

# import flatattrs
from django.forms.utils import flatatt
from django.template.loader import render_to_string
from django.templatetags.static import static
from django.urls import reverse, reverse_lazy
from django.utils.safestring import mark_safe
from quantityfield import settings as qsettings

register = template.Library()
ureg = qsettings.DJANGO_PINT_UNIT_REGISTER
ureg.default_format = ".2f~P"


class EditableObjectBlock(InclusionTag):
    """
    Templatetag that links a content extracted from a generic django model
    to the model admin changeform.

    The rendered content is to be specified in the enclosed block.
    """

    template = "geoluminate/components/sidebar/card.html"
    name = "render_editable"
    options = Options(
        Argument("instance"),
        Argument("edit_fields", default=None, required=False),
        Argument("view_name", default="{app_label}:{model_name}_edit", required=False),
        blocks=[("endrender_editable", "nodelist")],
    )

    def render_tag(self, context, **kwargs):
        """
        Renders the block and then inject the resulting HTML in the template
        context
        """
        context.push()
        template = self.get_template(context, **kwargs)
        data = self.get_context(context, **kwargs)
        data["content"] = kwargs["nodelist"].render(data)
        data["rendered_content"] = data["content"]
        output = render_to_string(template, flatten_context(data))
        context.pop()
        if kwargs.get("varname"):
            context[kwargs["varname"]] = output
            return ""
        else:
            return output

    def get_context(self, context, **kwargs):
        """
        Uses _get_empty_context and adds the `instance` object to the local
        context. Context here is to be intended as the context of the nodelist
        in the block.
        """
        kwargs.pop("varname")
        kwargs.pop("nodelist")
        extra_context = self._get_empty_context(context, **kwargs)
        extra_context["instance"] = kwargs.get("instance")
        extra_context["render_model_block"] = True
        return extra_context


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
def icon(icon: str, **kwargs):
    """Retrieves the default icon for a given object."""
    icon = settings.GEOLUMINATE_ICONS.get(icon)
    extra_classes = kwargs.pop("class", "")
    attrs = flatatt(kwargs)
    return mark_safe(f'<i class="{icon} {extra_classes}" {attrs}></i>')


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


@register.inclusion_tag("contributors/avatar.html")
def render_contributor_icon(profile, width="48px", **kwargs):
    " ".join([f'{k}="{v}"' for k, v in kwargs.items()])
    return {"profile": profile, "attrs": 'width="{width}" {attrs}'}


@register.simple_tag
def create_url(object_list):
    model = object_list.model
    return reverse_lazy(f"{model._meta.model_name}s:add")


@register.simple_tag(takes_context=True)
def page_menu(context):
    if context.get("page_menu") or context.get("actions_menu"):
        return render_to_string("menu/page_menu.html", context=context.flatten())
    return ""


@register.filter
def content_type(obj):
    if not obj:
        return False
    return ContentType.objects.get_for_model(obj)


@register.simple_tag
def update_object(instance, fields):
    content_type = ContentType.objects.get_for_model(instance).pk
    url = reverse(
        "update_object",
        kwargs={"content_type_id": content_type, "object_id": instance.pk},
    )
    return f"{url}?fields={fields}"


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
def description_url(instance, dtype=None):
    type_map = {
        "project": "p",
        "dataset": "d",
        "sample": "s",
    }
    # get model name from instance
    model_name = instance._meta.model_name
    object_type = type_map.get(model_name)
    if dtype:
        return reverse(
            "description-edit",
            kwargs={"pk": instance.pk, "object_type": object_type, "dtype": dtype},
        )
    return reverse("description-add", kwargs={"pk": instance.pk, "object_type": object_type})


@register.simple_tag(takes_context=True)
def urlx(context, view_name, **kwargs):
    # doesn't work. OLD
    view_kwargs = context["view_kwargs"]
    model = view_kwargs.pop("base_model")
    letter = model._meta.model_name[0]
    view_kwargs.update(kwargs)
    return reverse(view_name, kwargs={"model": letter, **view_kwargs})


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
def svg(icon: str, **kwargs):
    """Retrieves the default icon for a given object."""
    svg_str = render_to_string(f"icons/{icon}.svg")
    first, sep, rest = svg_str.partition("><")
    defaults = {
        "height": "1em",
        "fill": "currentColor",
    }
    defaults.update(kwargs)
    attrs = flatatt(defaults)
    return mark_safe(f"{first}{attrs}{sep}{rest}")


@register.simple_tag
def render_fields(obj, fields):
    def iter_func():
        for f in fields:
            mf = obj._meta.get_field(f)
            # if mf is a ManyToManyField, we need to get the related objects
            if mf.many_to_many:
                related_objects = getattr(obj, f).all()
                yield (mf.verbose_name, ", ".join([obj.__html__() for obj in related_objects]))
            # if mf is a ForeignKey, get the related object and create a link using the get_absolute_url method
            elif mf.is_relation:
                related = getattr(obj, f)
                if related:
                    yield (mf.verbose_name, related.__html__())
                else:
                    yield (mf.verbose_name, "-")

            else:
                yield (mf.verbose_name, mf.value_to_string(obj))

    return iter_func
