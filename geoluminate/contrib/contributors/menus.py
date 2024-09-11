from account_management.menus import UserManagementMenu
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from flex_menu import Menu, MenuItem

UserManagementMenu.add_child(
    Menu(
        "ProfileMenu",
        label=_("Profile"),
        children=[
            MenuItem(_("Your Profile"), view_name="contributor-profile", icon="user"),
            MenuItem(_("Recent Activity"), reverse("contributor-profile")),
            MenuItem(_("Following"), reverse("contributor-profile")),
            MenuItem(_("Database Admin"), reverse("admin:index")),
        ],
    ),
    position=0,
)


# SettingsMenu.add_items(
#     SubMenu(
#         _("profile"),
#         weight=1,
#         children=[
#             MenuItem(_("Public Profile"), reverse("contributor-profile"), icon=icon("person")),
#             MenuItem(_("affiliations"), reverse("contributor-affiliations"), icon="fas fa-building-user"),
#             MenuItem(_("identifiers"), reverse("contributor-identifiers"), icon="fa fa-fingerprint"),
#         ],
#     )
# )


# AccountSubMenu = SettingsMenu.submenus["Account"]


# AccountSubMenu.children.append(
#     MenuItem(_("identifiers"), reverse("user:contributor-identifiers"), icon="fa fa-fingerprint"),
# )
