from django.db import transaction
from licensing.models import License

from geoluminate.contrib.contributors.models import Contributor
from geoluminate.contrib.datasets.models import Dataset


def parse_author_object(author_object):
    """Parse an author object into a Contributor object.

    data = {
        "ORCID": "http://orcid.org/0000-0003-3762-7336",
        "authenticated-orcid": false,
        "given": "S",
        "family": "Jennings",
        "sequence": "first",
        "affiliation": [
            {
                "name": "Department of Earth Sciences, University of Adelaide, North Terrace, SA 5005, Australia"
            }
        ]
    }

    Args:
        author_object (object): An author object.

    Returns:
        geoluminate.contrib.contributors.models.Contributor: A Contributor object.
    """

    # initialise a new contributor object
    contributor = Contributor.objects.create()

    # add the name to the contributor object
    contributor.name = author_object["given"] + " " + author_object["family"]

    # return the contributor object
    return contributor


def parse_author_list(author_list):
    """Parse a list of author objects into a list of Contributor objects.

    Args:
        author_list (list): A list of author objects.

    Returns:
        list: A list of Contributor objects.
    """

    # initialise a list to store the parsed authors
    parsed_authors = []

    # iterate over the authors
    for author in author_list:
        contributor = parse_author_object(author)

        # add the contributor to the list of parsed authors
        parsed_authors.append(contributor)

    # return the list of parsed authors
    return parsed_authors


def parse_author_str(author_str):
    """Parse a string of authors into a list of Contributor objects.

    Args:
        author_str (str): A string of authors, separated by commas.

    Returns:
        list: A list of Contributor objects.
    """

    # split the string into a list of authors
    authors = author_str.split(",")

    # initialise a list to store the parsed authors
    parsed_authors = []

    # iterate over the authors
    for author in authors:
        # split the author into a list of names
        names = author.split(" ")

        # initialise a new contributor object
        contributor = Contributor.objects.create()

        # iterate over the names
        for name in names:
            # add the name to the contributor object
            contributor.name = name

        # add the contributor to the list of parsed authors
        parsed_authors.append(contributor)

    # return the list of parsed authors
    return parsed_authors


def dataset_from_literature(literature):
    """Create a new dataset from a literature object.

    Args:
        literature (geoluminate.contrib.reviews.models.Literature): The literature object to create a dataset from.

    Returns:
        geoluminate.contrib.datasets.models.Dataset: The new dataset object.
    """

    with transaction.atomic():
        license = License.objects.get(name="CC BY 4.0")  # noqa: A001
        # initialise a new dataset object
        dataset = Dataset.objects.create(
            title=literature.title,
            reference=literature,
            license=license,
        )

        # # loop over the authors in csl_obj and create a new Contribution object for each
        # contributions = []
        # for author in csl_obj["author"]:
        #     contribution = dataset.contributors.create(
        #         roles=[PersonalRoles.RESEARCHER, PersonalRoles.PROJECT_MEMBER, PersonalRoles.DATA_COLLECTOR],
        #         data=author,
        #     )

        #     contributions.append(contribution)

        #     if author.get("ORCID"):
        #         contribution.identifiers.create(
        #             scheme="ORCID",
        #             identifier=author["ORCID"],
        # )

    return dataset
