from django import template

register = template.Library()

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

    if getattr(obj.field,'choices',False):
        for choice in obj.field.choices:
            if value == choice[0]:
                value = choice[1]

    return '<tr><td class="w-50">{}:</td><td>{}</td></tr>'.format(obj.name.replace('_',' ').title(),value)

@register.inclusion_tag('core/bootstrap/tab.html', takes_context=True)
def tab(context, name, active=False):
    context['name'] = name
    context['active'] = active
    return context

@register.inclusion_tag('core/bootstrap/panel.html', takes_context=True)
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
        return '&'+params.urlencode()
    else:
        return ''