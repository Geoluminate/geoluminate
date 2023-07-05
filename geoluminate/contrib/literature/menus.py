from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from simple_menu import MenuItem

from geoluminate.menus import Sidebar

Sidebar.add_item(
    MenuItem(
        title=_("Literature"),
        url=reverse("literature:list"),
        weight=5,
        icon="fa-book",
        children=(
            MenuItem(
                title=_("Catalogue"),
                url=reverse("literature:list"),
                icon="fa-list",
            ),
            MenuItem(
                title=_("Authors"),
                url=reverse("literature:author_list"),
                icon="fa-users",
            ),
        ),
    ),
)
