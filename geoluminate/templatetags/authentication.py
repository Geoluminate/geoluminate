from allauth.account.models import EmailAddress
from allauth.utils import get_form_class
from crispy_forms.utils import render_crispy_form
from django import template
from django.conf import settings
from django.template.context_processors import csrf

register = template.Library()


@register.simple_tag(takes_context=True)
def can_add_email(context):
    return EmailAddress.objects.can_add_email(context["request"].user)


@register.filter(name="has_group")
def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists()
