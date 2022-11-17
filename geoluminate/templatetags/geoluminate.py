from django import template
from geoluminate.models import GlobalConfiguration
from django.templatetags.static import static
from django.shortcuts import render
from django.template.loader import render_to_string

register = template.Library()


@register.simple_tag
def menu(menu, template=None):
    """Renders a menu"""
    if not template:
        template = menu.template_name
    return render_to_string(template, {'menu': menu})


@register.simple_tag
def logo():
    """Gets the correct URL for the logo as set in `GlobalConfiguration`."""
    logo = GlobalConfiguration.get_solo().logo
    if logo:
        return logo.url
    return static('geoluminate/logo.svg')


@register.simple_tag
def icon():
    """Gets the correct URL for the icon as set in `GlobalConfiguration`."""
    icon = GlobalConfiguration.get_solo().icon
    if icon:
        return icon.url
    return static('geoluminate/icon.svg')


@register.simple_tag
def verbose_name(instance, field_name):
    """
    Returns verbose_name for a field.
    """
    return instance._meta.get_field(field_name).verbose_name.capitalize()


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

    if getattr(obj.field, 'choices', False):
        for choice in obj.field.choices:
            if value == choice[0]:
                value = choice[1]

    return '<tr><td class="w-50">{}:</td><td>{}</td></tr>'.format(
        obj.name.replace('_', ' ').title(), value)


@register.inclusion_tag('geoluminate/bootstrap/tab.html', takes_context=True)
def tab(context, name, active=False):
    context['name'] = name
    context['active'] = active
    return context


@register.inclusion_tag('geoluminate/bootstrap/panel.html', takes_context=True)
def panel(context, name, template, active=False):
    context['name'] = name
    context['template'] = template
    context['active'] = active
    return context


@register.simple_tag(takes_context=True)
def filter_params(context):
    """Returns curent filter params as a string"""
    request = context['request']
    params = request.GET.copy()
    params.pop('page', True)
    if params:
        return '&' + params.urlencode()
    else:
        return ''
