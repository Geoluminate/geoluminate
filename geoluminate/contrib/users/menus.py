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


# SubMenu(
#     _("Create new"),
#     weight=1.5,
#     children=[
#         MenuItem(_("project"), url=reverse("project-create"), icon="plus"),
#         MenuItem(_("dataset"), url=reverse("dataset-create"), icon="plus"),
#     ],
# ),

# AccountSidebar.add_items(
# SubMenu(
#     _("General"),
#     weight=2,
#     children=[
#         MenuItem(_("appearance"), view_name="user:appearance-settings"),
#         MenuItem(_("notifications"), view_name="user:notifications-settings"),
#         MenuItem(_("privacy"), view_name="contributor-profile"),
#     ],
# ),
# SubMenu(
#     _("Agreements"),
#     weight=4,
#     children=[
#         MenuItem(_("Code of Conduct"), url=reverse("user:code_of_conduct")),
#         # MenuItem(_("Terms of Use"), url=reverse("user:terms"), icon="fas fa-file-contract"),
#     ],
# ),
# )
