from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from geoluminate.menus import MenuItem, SettingsMenu, SubMenu
from geoluminate.utils import icon

SettingsMenu.add_items(
    SubMenu(
        _("profile"),
        weight=1,
        children=[
            MenuItem(_("Public Profile"), reverse("contributor-profile"), icon=icon("person")),
            MenuItem(_("affiliations"), reverse("contributor-affiliations"), icon="fas fa-building-user"),
            MenuItem(_("identifiers"), reverse("contributor-identifiers"), icon="fa fa-fingerprint"),
        ],
    )
)


# AccountSubMenu = SettingsMenu.submenus["Account"]


# AccountSubMenu.children.append(
#     MenuItem(_("identifiers"), reverse("user:contributor-identifiers"), icon="fa fa-fingerprint"),
# )
