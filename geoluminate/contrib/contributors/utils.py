from .models import Contributor

# def add_current_user_as_contributor(sender, instance, created, **kwargs):
#     """Add the current user as a contributor to the new dataset."""
#     if created:
#         instance.contributors.add(instance.user)


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
