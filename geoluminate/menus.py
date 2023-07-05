from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from simple_menu import Menu, MenuItem

# from geoluminate.contrib.projects.models import


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
        title=_("Projects"),
        url=reverse("ProjectDataTable:view"),
        weight=1,
        icon="fa-project-diagram",
    ),
)

Sidebar.add_item(
    MenuItem(
        title=_("Datasets"),
        url=reverse("DatasetDataTable:view"),
        weight=2,
        icon="fa-folder-open",
    ),
)

Sidebar.add_item(
    MenuItem(
        title=_("Samples"),
        # check=lambda request: request.user.is_staff,
        url=reverse("SampleDataTable:view"),
        weight=3,
        icon="fa-database",
    ),
)

Sidebar.add_item(
    MenuItem(
        title=_("Sites"),
        url=reverse("viewer"),
        weight=4,
        icon="fa-map-marked-alt",
    ),
)

Sidebar.add_item(
    MenuItem(
        title=_("API"),
        url=reverse("swagger-ui"),
        weight=5,
        icon="fa-gears",
    ),
)
