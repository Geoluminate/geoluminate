import json

from django.apps import apps
from django.conf import settings
from django.db import models, transaction
from django.db.models import CharField, F, Value
from easy_thumbnails.files import get_thumbnailer

from fairdm.contrib.contributors.models import ContributorIdentifier

from .models import Contributor, Person


def dictget(data, path, default=""):
    """
    Navigate `data`, a multidimensional array (list or dictionary), and returns
    the object at `path`.
    """
    value = data
    try:
        for key in path:
            value = value[key]
        return value  # noqa: TRY300
    except (KeyError, IndexError, TypeError):
        return default


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

    if contribution_obj := obj.contributors.filter(contributor=current_user).first():
        return any([role in contribution_obj.roles for role in role])

    return False


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


def contributor_from_orcid_data(data, person=None):
    Person = apps.get_model("contributors", "Person")
    orcid = dictget(data, ["orcid-identifier", "path"])

    # if a person is explicitly passed, use it, otherwise try to find an existing person by ORCID, otherwise create a new person instance
    person = person or Person.objects.filter(identifiers__type="ORCID", identifiers__value=orcid).first() or Person()

    with transaction.atomic():
        person.name = dictget(data, ["person", "name", "credit-name", "value"])
        person.first_name = dictget(data, ["person", "name", "given-names", "value"])
        person.last_name = dictget(data, ["person", "name", "family-name", "value"])
        person.profile = dictget(data, ["person", "biography", "content"])

        if other_names := dictget(data, ["person", "other-names", "other-name"]):
            person.alternative_names = [name["content"] for name in other_names]

        if links := dictget(data, ["person", "researcher-urls", "researcher-url"]):
            person.links = [link["url"]["value"] for link in links]

        person.save()

        # WARNING: I don't like this. We shouldn't update the identifier with a new person object if it already exists.
        ContributorIdentifier.objects.update_or_create(type="ORCID", value=orcid, defaults={"related": person})

        # NOTE: need to work out the format for external-identifiers in ORCID

        # identifiers = dictget(data, ["person", "external-identifiers"], [])
        # for id_type, content in identifiers.items():
        #     # value is either list or string
        #     value = dictget(content, ["all"])
        #     if isinstance(value, list):
        #         value = value[0]
        #     ContributorIdentifier.objects.update_or_create(
        #         type=id_type,
        #         value=dictget(content, ["preferred"]) or value,  # utilize preferred value if available
        #         defaults={"content_object": person},
        # )

    return person


def contributor_from_ror_data(data, org=None):
    Organization = apps.get_model("contributors", "Organization")
    ror_id = dictget(data, ["id"]).split("/")[-1]

    # if an org is explicitly passed, use it, otherwise try to find an existing org by ROR ID, otherwise create a new org instance
    org = (
        org or Organization.objects.filter(identifiers__type="ROR", identifiers__value=ror_id).first() or Organization()
    )

    with transaction.atomic():
        org.ror = data
        org.name = dictget(data, ["name"])
        org.alternative_names = dictget(data, ["aliases"]) + dictget(data, ["acronyms"], [])
        org.city = dictget(data, ["addresses", 0, "city"])
        org.country = dictget(data, ["country", "country_name"])
        links = dictget(data, ["links"])
        if wiki_url := dictget(data, ["wikipedia_url"]):
            links.append(wiki_url)
        if links:
            org.links = links

        org.save()
        ContributorIdentifier.objects.update_or_create(type="ROR", value=ror_id, defaults={"content_object": org})

        identifiers = dictget(data, ["external_ids"], [])
        for id_type, content in identifiers.items():
            # value is either list or string
            value = dictget(content, ["all"])
            if isinstance(value, list):
                value = value[0]
            ContributorIdentifier.objects.update_or_create(
                type=id_type,
                value=dictget(content, ["preferred"]) or value,  # utilize preferred value if available
                defaults={"content_object": org},
            )

    tags = dictget(data, ["types"], [])
    address = dictget(data, ["addresses", 0])

    return org
