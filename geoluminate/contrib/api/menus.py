from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from simple_menu import Menu, MenuItem

Menu.add_item(
    "sidebar",
    MenuItem(
        _("API"),
        reverse("swagger-ui"),
        weight=3,
        icon="fa-project-diagram",
    ),
)
