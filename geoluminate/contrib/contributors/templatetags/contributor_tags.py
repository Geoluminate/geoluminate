from django import template

from ..utils import contributor_by_role

register = template.Library()


@register.filter
def role(contributions, roles):
    """Returns all contributors with the specified roles.

    Args:

        contributions (list): A list of Contribution objects (e.g. list(Contribution.objects.all())).
        roles (str): A comma separated list of roles to filter by.
    """
    return contributor_by_role(contributions, roles)
