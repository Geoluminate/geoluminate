from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from simple_menu import Menu, MenuItem

from geoluminate.measurements import measurements
from geoluminate.utils import icon


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
        title=_("Measurements"),
        url=reverse("viewer"),
        weight=5,
        icon="fa-flask",
        children=measurements.menu,
    ),
)

Sidebar.add_item(
    MenuItem(
        title=_("Explorer"),
        url=reverse("viewer"),
        weight=5,
        icon="fa-map-marked-alt",
    ),
)

Sidebar.add_item(
    MenuItem(
        title=_("Literature"),
        url="/literature/",
        weight=5,
        icon="fa-book",
        children=[
            MenuItem(
                title=_("GHFDB Catalogue"),
                url=reverse("review:literature_list"),
                weight=5,
                icon="fa-book",
            ),
            MenuItem(
                title=_("Literature Review"),
                url=reverse("review:list"),
                weight=5,
                icon=icon("review"),
            ),
        ],
    ),
)

# Sidebar.add_item(
#     MenuItem(
#         title=_("Reviews"),
#         url=reverse("review:list"),
#         weight=5,
#         icon="fas fa-book-open",
#     ),
# )

Sidebar.add_item(
    MenuItem(
        title=_("Contributors"),
        url=reverse("contributor:list"),
        weight=6,
        icon="fa-user-group",
    ),
)

Sidebar.add_item(
    MenuItem(
        title=_("API"),
        url=reverse("swagger-ui"),
        weight=7,
        icon="fa-gears",
    ),
)
