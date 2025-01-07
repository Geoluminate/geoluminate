from django.utils.translation import gettext_lazy as _
from flex_menu import Menu, MenuItem
from literature.models import LiteratureItem

from geoluminate.contrib.core.models import Sample
from geoluminate.models import Contributor, Dataset, Measurement, Project

DatabaseMenu = Menu(
    "DatabaseMenu",
    label=_("Database"),
    root_template="geoluminate/menus/database/root.html",
    template="geoluminate/menus/database/menu.html",
    children=[
        Menu(
            "DatabaseExploreMenu",
            label=_("Explore"),
            root_template="geoluminate/menus/database/root.html",
            template="geoluminate/menus/database/menu.html",
            children=[
                MenuItem(
                    _("Projects"),
                    view_name="project-list",
                    icon="project",
                    count=Project.objects.count,
                    description=_(
                        "Discover planned, active, and historic research projects shared by our community members."
                    ),
                ),
                MenuItem(
                    _("Datasets"),
                    view_name="dataset-list",
                    icon="dataset",
                    count=Dataset.objects.count,
                    description=_(
                        "Browse quality-controlled datasets that meet the high standards required by our community."
                    ),
                ),
                MenuItem(
                    _("Samples"),
                    view_name="sample-list",
                    icon="sample",
                    count=Sample.objects.count,
                    description=_(
                        "Explore tabular data collections for specific sample types collected by this portal."
                    ),
                ),
                MenuItem(
                    _("Measurements"),
                    view_name="measurement-list",
                    icon="measurement",
                    count=Measurement.objects.count,
                    description=_(
                        "Explore tabular data collections for specific sample types collected by this portal."
                    ),
                ),
                MenuItem(
                    _("Literature"),
                    view_name="reference-list",
                    icon="literature",
                    count=LiteratureItem.objects.count,
                    description=_("Explore related published and unpublished literature relevant to this portal."),
                ),
            ],
        ),
        Menu(
            "DatabaseMoreMenu",
            label=_("More"),
            root_template="geoluminate/menus/database/root.html",
            template="geoluminate/menus/database/menu.html",
            children=[
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
                        "View the API documentation and learn how to interact programatically with this portal."
                    ),
                ),
            ],
        ),
    ],
)

ProjectMenu = Menu(
    "ProjectMenu",
    label=_("Project"),
    root_template="geoluminate/menus/detail/root.html",
    children=[
        MenuItem(_("Overview"), view_name="project-detail", icon="grid", template="geoluminate/menus/detail/menu.html"),
    ],
)

DatasetMenu = Menu(
    "DatasetMenu",
    label=_("Dataset"),
    root_template="geoluminate/menus/detail/root.html",
    children=[
        MenuItem(_("Overview"), icon="grid", view_name="dataset-detail", template="geoluminate/menus/detail/menu.html"),
    ],
)

SampleMenu = Menu(
    "SampleMenu",
    label=_("Sample"),
    root_template="geoluminate/menus/detail/root.html",
    children=[
        MenuItem(_("Overview"), view_name="sample-detail", icon="grid", template="geoluminate/menus/detail/menu.html"),
    ],
)

ContributorMenu = Menu(
    "ContributorMenu",
    label=_("Contributor"),
    root_template="geoluminate/menus/detail/root.html",
    children=[
        MenuItem(_("Overview"), view_name="person-detail", icon="grid", template="geoluminate/menus/detail/menu.html"),
    ],
)
