from .models import Contributor


def current_user_has_role(request, obj, role):
    """Returns True if the current user has the specified role for the given object.

    Args:
        request (Request): The request object.
        obj (Project, Dataset, Sample): A database object containing a list of contributors.
        role (str, list): The role/s to check for.

    Returns:
        bool: True if the contributor has the specified roles.
    """
    current_user = request.user
    if not current_user.is_authenticated:
        return False

    if not isinstance(role, list):
        role = [role]

    return obj.contributors.filter(profile__user=current_user, roles__contains=role).exists()


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
            identifiers__scheme="ORCID",
            identifiers__identifier=csljson_author.get("ORCID"),
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
