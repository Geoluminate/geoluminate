from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from simple_menu import Menu, MenuItem

Menu.add_item(
    "sidebar",
    MenuItem(
        _("Database"),
        reverse("database_table"),
        weight=1,
        icon="fa-database",
    ),
)

Menu.add_item(
    "sidebar",
    MenuItem(
        _("Map"),
        reverse("viewer"),
        weight=2,
        icon="fa-map-marked-alt",
    ),
)
