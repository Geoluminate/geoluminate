from django.conf import settings
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from simple_menu import Menu, MenuItem

from geoluminate.utils import icon

LABELS = settings.GEOLUMINATE_LABELS


class GeoluminateMenuBase:
    menu_name = ""

    @classmethod
    def add_item(c, item):
        """
        add_item adds MenuItems to the menu identified by 'name'
        """
        Menu.add_item(c.menu_name, item)

    @classmethod
    def add_items(c, *args):
        """
        add_item adds MenuItems to the menu identified by 'name'
        """
        for menu_item in args:
            if isinstance(menu_item, MenuItem):
                c.add_item(menu_item)
            else:
                raise TypeError(f"add_items expected a MenuItem, but got {type(menu_item)}")


class NavWidgets(GeoluminateMenuBase):
    menu_name = "nav"


class Sidebar(GeoluminateMenuBase):
    menu_name = "sidebar"


Sidebar.add_item(
    MenuItem(
        title=LABELS["project"]["verbose_name_plural"],
        url=reverse("projects:list"),
        weight=1,
        icon=icon("project"),
        description=_(
            "Discover conceptual, active, and archived research projects shared by our community members. Filter through diverse research interests, engage with active contributors, establish new connections and embark on collaborative journeys of discovery."
        ),
    ),
)

Sidebar.add_item(
    MenuItem(
        title=LABELS["dataset"]["verbose_name_plural"],
        url=reverse("datasets:list"),
        weight=2,
        icon=icon("dataset"),
        description=_(
            "Delve into our extensive collection of quality-controlled datasets, spanning historical archives to recently published and upcoming releases. Filter through a diverse array of domain specific concepts and discover valuable resources for your future research endeavors."
        ),
    ),
)

# Sidebar.add_item(
#     MenuItem(
#         title=LABELS["sample"]["verbose_name_plural"],
#         url=reverse("samples:list"),
#         weight=3,
#         icon=icon("sample"),
#         description=_(
#             "Find exactly what you need to advance your data analytics workflow by exploring our extensive collection of samples. Filter through diverse sample types, measured properties, locations and more to find the perfect supplement for your current and future research."
#         ),
#     ),
# )

# Sidebar.add_item(
#     MenuItem(
#         title=_("Measurements"),
#         url=reverse("viewer"),
#         weight=4,
#         icon=icon("measurement"),
#         children=measurements.menu,
#     ),
# )

Sidebar.add_item(
    MenuItem(
        title=_("Explorer"),
        url=reverse("viewer"),
        weight=5,
        icon=icon("map"),
        description=_(
            "Explore our extensive collection of projects, datasets, samples and measurements using our interactive map and data viewer. Create complex filters, visualize data, and gain valuable insight into our database."
        ),
    ),
)

Sidebar.add_item(
    MenuItem(
        title=_("Literature"),
        url="/literature/",
        weight=6,
        icon=icon("literature"),
        children=[
            MenuItem(
                title=_("GHFDB Catalogue"),
                url=reverse("review:literature_list"),
                weight=5,
                icon=icon("literature"),
                description=_(
                    "Explore published and unpublished literature that are directly related to datasets hosted on this platform."
                ),
            ),
            MenuItem(
                title=_("Literature Review"),
                url=reverse("review:list"),
                weight=5,
                icon=icon("review"),
                description=_(
                    "Browse historic literature that have been reviewed by our community members in order to create digital datasets that you can use in your future research projects. Discover literature that are open to review, contribute to the growth of our database and gain appropriate credit and exposure for your contributions."
                ),
            ),
        ],
    ),
)

Sidebar.add_item(
    MenuItem(
        title=_("Contributors"),
        url=reverse("contributor:list"),
        weight=7,
        icon=icon("contributors"),
        description=_(
            "Search active, inactive and past contributors who have contributed to the growth of our database and online community. Discover like-minded professionals, establish new connections, and collaborate together on future projects."
        ),
    ),
)

Sidebar.add_item(
    MenuItem(
        title=_("API"),
        url=reverse("swagger-ui"),
        weight=8,
        icon="fa-solid fa-gears",
        description=_(
            "Explore our API documentation to learn how to interact programatically with our database and access our extensive collection of datasets, samples, projects and more. Integrate our online resources into your custom applications, notebooks and workflows."
        ),
    ),
)
