from allauth.account.models import EmailAddress
from allauth.utils import get_form_class
from crispy_forms.utils import render_crispy_form
from django import template
from django.conf import settings
from django.template.context_processors import csrf

register = template.Library()


@register.simple_tag(takes_context=True)
def authentication_form(context, key):
    """Renders a named authentication form by the given key. Possible values are those listed in settings"""
    form = get_form_class(settings.ACCOUNT_FORMS, key, False)
    if not form:
        raise KeyError(
            f"Could not find form using the lookup key: {key}. Possible values are"
            f" {list(settings.ACCOUNT_FORMS.keys())}"
        )
    return render_crispy_form(form, context=csrf(context["request"]))


@register.inclusion_tag("authentication/modal_link.html")
def auth_link(modal_id, link_text, classes=""):
    return {"modal_id": modal_id, "link_text": link_text, "classes": classes}


@register.simple_tag(takes_context=True)
def can_add_email(context):
    return EmailAddress.objects.can_add_email(context["request"].user)


@register.filter(name="has_group")
def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists()
