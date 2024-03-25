from django import template

register = template.Library()


@register.filter
def role(contributions, roles):
    """Returns all contributors with the specified roles.

    Args:
        roles (str): A comma separated list of roles to filter by.
    """
    return contributions.filter(roles__contains=roles.split(","))
