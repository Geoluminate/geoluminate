import json

from allauth.socialaccount.providers.orcid.provider import extract_from_dict
from django.conf import settings
from django.db import models
from django.db.models import CharField, F, Value
from easy_thumbnails.files import get_thumbnailer

from .models import Contributor, Person


def get_contributor_avatar(contributor):
    """Returns the avatar URL for a given contributor.

    Args:
        contributor (Contributor): A Contributor object.

    Returns:
        str: The URL of the contributor's avatar.
    """
    if not contributor.image:
        return None

    return get_thumbnailer(contributor.image)["thumb"].url


def get_avatar_url(comment):
    if comment.user is not None:
        try:
            return get_contributor_avatar(comment.user)
        except Exception:
            pass
    return get_contributor_avatar(comment)


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

    return obj.contributions.filter(contributor=current_user, roles__contains=role).exists()


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


def user_network(contributor):
    # get list of content_types that the contributor has contributed to
    object_ids = contributor.contributions.values_list("object_id", flat=True)

    # get all contributions to those content_types
    data = (
        contributor.get_related_contributions()
        .values("profile", "object_id")
        .annotate(
            id=models.F("profile__id"),
            label=models.F("profile__name"),
            image=models.F("profile__image"),
        )
        .values("id", "label", "object_id", "image")
    )

    models.Concat(
        F("model__user_first_name"),
        Value(" "),
        F("model__user_last_name"),
        output_field=CharField(),
    )

    # get unique contributors and count the number of times they appear in the queryset
    nodes_qs = data.values("id", "label", "image").annotate(value=models.Count("id")).distinct()

    nodes = []
    for d in nodes_qs:
        if d["image"]:
            d["image"] = settings.MEDIA_URL + d["image"]
        nodes.append(d)

    print("Nodes: ", nodes)

    object_ids = {d["object_id"] for d in data}

    edges = []
    for obj in object_ids:
        ids = list({i["id"] for i in data if i["object_id"] == obj})

        ids.sort()

        # get list of unique id pairs
        pairs = []
        for i in range(len(ids)):
            for j in range(i + 1, len(ids)):
                pairs.append((ids[i], ids[j]))

        edges += pairs

    # count the number of times each pair appears in edges
    edges = [{"from": f, "to": t, "value": edges.count((f, t))} for f, t in set(edges)]

    vis_js = {"nodes": list(nodes), "edges": edges}
    print(edges)
    # serialize nodes queryset to json

    return json.dumps(vis_js)


# def related_contributions(self):
#     """Returns a queryset of all contributions related to datasets contributed to by the current contributor."""

#     dataset_ids = self.contributions.filter(
#         content_type=ContentType.objects.get_for_model(Dataset),
#     ).values_list("object_id", flat=True)

#     return Contribution.objects.filter(object_id__in=dataset_ids)


def contributor_from_orcid_id(orcid_id):
    """Returns a contributor object from an ORCID ID."""
    contributor = Person.objects.filter(identifiers__type="ORCID", identifiers__value=orcid_id).first()

    if contributor is None:
        c = Person()
        c.identifiers.create(type="ORCID", value=orcid_id)


def contributor_from_orcid_data(data):
    common_fields = dict(
        email=extract_from_dict(data, ["person", "emails", "email", 0, "email"]),
        last_name=extract_from_dict(data, ["person", "name", "family-name", "value"]),
        first_name=extract_from_dict(data, ["person", "name", "given-names", "value"]),
    )
