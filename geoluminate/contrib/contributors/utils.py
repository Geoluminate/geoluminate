from django.db.models import QuerySet

from .models import Contributor

#     if created:
#         instance.contributors.add(instance.user)


def has_role(contributor, role):
    """Returns True if the contributor has the specified role.

    Args:
        contributor (Contributor): A Contributor object.
        role (str, list): The role/s to check for.

    Returns:
        bool: True if the contributor has the specified roles.
    """
    if isinstance(role, str):
        role = [role]
    return any(r in contributor.roles for r in role)


def contributor_by_role(contributors, roles):
    """Returns all contributors with the specified roles.

    Args:

        contributions (list): A list of Contribution objects (e.g. list(Contribution.objects.all())).
        roles (str): A comma separated list of roles to filter by.
    """
    roles = roles.split(",")
    if isinstance(contributors, QuerySet):
        return contributors.filter(roles__in=roles)
    elif isinstance(contributors, list):
        matched = []
        # contributions is a list of Contributions
        for c in contributors:
            if any(role in c.roles for role in roles):
                matched.append(c)
        return matched
    return []


def contributor_to_csljson(contributor):
    """Parse a Contributor object into a CSL-JSON author object.

    Args:
        contributor (Contributor): A Contributor object.

    Returns:
        dict: A CSL-JSON author object.
    """

    csljson = {
        "name": contributor.name,
        "given": contributor.given,
        "family": contributor.family,
    }

    ORCID = contributor.identifiers.filter(scheme="ORCID").first()
    if ORCID:
        csljson["ORCID"] = ORCID.identifier

    affiliation = contributor.default_affiliation()
    if affiliation:
        csljson["affiliation"] = affiliation

    return csljson


def csljson_to_contributor(csljson_author):
    """Parse a CSL-JSON author object into a Contributor object.

    Args:
        author (dict): A CSL-JSON author object.

    Returns:
        Contributor: A Contributor object.
    """

    if csljson_author.get("ORCID"):
        # try to get the contributor by their ORCID
        contributor = Contributor.objects.filter(
            identifiers__scheme="ORCID", identifiers__identifier=csljson_author.get("ORCID")
        ).first()

        if contributor:
            return contributor

    # initialise a new contributor object
    contributor = Contributor.objects.create()

    # add the name to the contributor object
    contributor.name = csljson_author.get("literal")

    # add the ORCID to the contributor object
    contributor.orcid = csljson_author.get("ORCID")

    # return the contributor object
    return contributor
