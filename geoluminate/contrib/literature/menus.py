from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from simple_menu import Menu, MenuItem

Menu.add_item(
    "sidebar",
    MenuItem(
        _("Literature"),
        reverse("literature:list"),
        weight=5,
        icon="fa-book",
        children=(
            MenuItem(
                _("Catalogue"),
                reverse("literature:list"),
                icon="fa-list",
            ),
            MenuItem(
                _("Authors"),
                reverse("literature:author_list"),
                icon="fa-users",
            ),
        ),
    ),
)
