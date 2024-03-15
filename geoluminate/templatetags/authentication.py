from allauth.account.models import EmailAddress
from django import template
from django.conf import settings

register = template.Library()


@register.simple_tag(takes_context=True)
def can_add_email(context):
    return EmailAddress.objects.can_add_email(context["request"].user)


@register.filter(name="has_group")
def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists()


@register.simple_tag(takes_context=True)
def authentication_form(context, form_key):
    auth_forms = settings.ACCOUNT_FORMS
    form_class = auth_forms.get(form_key)
    request = context.get("request")
    return form_class(request)
