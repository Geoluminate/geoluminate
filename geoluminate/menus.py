from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from simple_menu import Menu, MenuItem

Menu.add_item(
    "toolbar",
    MenuItem(
        _("Database"),
        reverse("database_table"),
        weight=1,
        icon="fa-database",
    ),
)

Menu.add_item(
    "toolbar",
    MenuItem(
        _("Map"),
        reverse("viewer"),
        weight=2,
        icon="fa-map-marked-alt",
    ),
)

Menu.add_item(
    "toolbar",
    MenuItem(
        _("History"),
        reverse("database_history"),
        weight=6,
        icon="fa-history",
    ),
)
