from django import template
from django.db.models import QuerySet

register = template.Library()


@register.filter
def role(contributions, roles):
    """Returns all contributors with the specified roles.

    Args:

        contributions (list): A list of Contribution objects (e.g. list(Contribution.objects.all())).
        roles (str): A comma separated list of roles to filter by.
    """
    roles = roles.split(",")
    if isinstance(contributions, QuerySet):
        return contributions.filter(role__in=roles)
    elif isinstance(contributions, list):
        matched = []
        # contributions is a list of Contributions
        for c in contributions:
            if any(role in c.roles for role in roles):
                matched.append(c)
        return matched
    return []
