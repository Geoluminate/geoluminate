import logging
from contextlib import suppress

from django.conf import settings
from django.urls import reverse
from django.urls.exceptions import NoReverseMatch
from django.utils.translation import gettext_lazy as _
from flex_menu import Menu, MenuItem
from literature.models import LiteratureItem

from geoluminate.contrib.samples.models import Sample
from geoluminate.models import Contributor, Dataset, Measurement, Project

LABELS = settings.GEOLUMINATE_LABELS


logger = logging.getLogger(__name__)


def is_staff_user(request):
    return request.user.is_staff


def check_url(viewname):
    """Check to see if a url can be resolved. Return false if not."""

    def inner(request):
        with suppress(NoReverseMatch):
            return reverse(viewname)

    return inner


DatabaseMenu = Menu(
    "DatabaseMenu",
    label=_("Database"),
    root_template="geoluminate/menus/database/root.html",
    template="geoluminate/menus/database/menu.html",
    children=[
        MenuItem(
            _("Projects"),
            view_name="project-list",
            icon="project",
            count=Project.objects.count,
            description=_(
                "Discover conceptual, active, and archived research projects shared by our community members. Filter through diverse research interests, engage with active contributors, establish new connections and embark on collaborative journeys of discovery."
            ),
        ),
        MenuItem(
            _("Datasets"),
            view_name="dataset-list",
            icon="dataset",
            count=Dataset.objects.count,
            description=_(
                "Delve into our extensive collection of quality-controlled datasets, spanning historical archives to recently published and upcoming releases. Filter through a diverse array of domain specific concepts and discover valuable resources for your future research endeavors."
            ),
        ),
        MenuItem(
            _("Samples"),
            view_name="sample-type-list",
            icon="sample",
            count=Sample.objects.count,
            description=_(
                "Find exactly what you need to advance your data analytics workflow by exploring our extensive collection of samples. Filter through diverse sample types, measured properties, locations and more to find the perfect supplement for your current and future research."
            ),
        ),
        MenuItem(
            _("Measurements"),
            view_name="measurement-type-list",
            icon="measurement",
            count=Measurement.objects.count,
            description=_(
                "Find exactly what you need to advance your data analytics workflow by exploring our extensive collection of samples. Filter through diverse sample types, measured properties, locations and more to find the perfect supplement for your current and future research."
            ),
        ),
        # MenuItem(
        #     _("Explorer"),
        #     view_name="viewer",
        #     icon="map",
        #     description=_(
        #         "Explore our extensive collection of projects, datasets, samples and measurements using our interactive map and data viewer. Create complex filters, visualize data, and gain valuable insight into our database."
        #     ),
        # ),
        MenuItem(
            _("References"),
            view_name="reference-list",
            icon="literature",
            count=LiteratureItem.objects.count,
            description=_(
                "Explore published and unpublished literature that are directly related to datasets hosted on this platform."
            ),
        ),
        MenuItem(
            _("Contributors"),
            view_name="contributor-list",
            icon="contributors",
            count=Contributor.objects.count,
            description=_(
                "Search active, inactive and past contributors who have contributed to the growth of our database and online community. Discover like-minded professionals, establish new connections, and collaborate together on future projects."
            ),
        ),
        MenuItem(
            _("API"),
            view_name="api:swagger-ui",
            icon="api",
            description=_(
                "Explore our API documentation to learn how to interact programatically with our database and access our extensive collection of datasets, samples, projects and more. Integrate our online resources into your custom applications, notebooks and workflows."
            ),
        ),
        # MenuItem(
        #     _("Vocabularies"),
        #     view_name="vocabularies:list",
        #     icon="vocabularies",
        #     description=_(
        #         "Explore our API documentation to learn how to interact programatically with our database and access our extensive collection of datasets, samples, projects and more. Integrate our online resources into your custom applications, notebooks and workflows."
        #     ),
        # ),
    ],
)


ProjectDetailMenu = Menu(
    "ProjectDetailMenu",
    label=_("Project"),
    root_template="geoluminate/menus/detail/root.html",
)

DatasetDetailMenu = Menu(
    "DatasetDetailMenu",
    label=_("Dataset"),
    root_template="geoluminate/menus/detail/root.html",
)

SampleDetailMenu = Menu(
    "SampleDetailMenu",
    label=_("Sample"),
    root_template="geoluminate/menus/detail/root.html",
)

ContributorDetailMenu = Menu(
    "ContributorDetailMenu",
    label=_("Contributor"),
    root_template="geoluminate/menus/detail/root.html",
)
