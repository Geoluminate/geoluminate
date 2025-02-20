from django import template

register = template.Library()


@register.filter
def by_role(contributions, roles=None):
    """Returns all contributors with the specified roles.

    Args:
        roles (str): A comma separated list of roles to filter by.
    """
    if not roles:
        return contributions
    if isinstance(roles, str):
        roles = roles.split(",")
    return [c for c in contributions if any(role in c.roles for role in roles)]


@register.filter
def has_role(contribution, roles=None):
    """Returns True if the contributor has the specified role."""
    if not roles:
        return contribution
    if isinstance(roles, str):
        roles = roles.split(",")
    return any(role in contribution.roles for role in roles)
