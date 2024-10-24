from django import template

register = template.Library()


@register.filter
def role(contributions, roles=None):
    """Returns all contributors with the specified roles.

    Args:
        roles (str): A comma separated list of roles to filter by.
    """
    if not roles:
        return contributions.all()
    # croles = contributions.values_list("roles", flat=True)
    # return
    return contributions.all()
    # return contributions.filter(roles__contains=roles.split(","))
