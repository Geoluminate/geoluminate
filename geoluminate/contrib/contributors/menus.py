from account_management.menus import AccountMenu, FloatingAccountMenu
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from flex_menu import Menu, MenuItem


def get_contibutor_url(request):
    return reverse_lazy("contributor-detail", args=[request.user.id])


AccountMenu.add_children(
    [
        Menu(
            "ProfileMenu",
            label=_("Profile"),
            children=[
                MenuItem(_("Edit Profile"), view_name="contributor-profile", icon="user"),
                MenuItem(_("Recent Activity"), view_name="contributor-profile", icon="activity"),
                MenuItem(_("Following"), view_name="contributor-profile", icon="star-solid"),
                MenuItem(_("Identifiers"), view_name="contributor-identifiers", icon="identifier"),
                MenuItem(_("Affiliations"), view_name="contributor-affiliations", icon="organization"),
            ],
        ),
    ],
    position=0,
)


FloatingAccountMenu.add_children(
    [
        MenuItem(_("Profile"), url=get_contibutor_url, icon="user"),
        MenuItem(_("Manage Account"), view_name="account-management", icon="activity"),
        MenuItem(_("Recent Activity"), view_name="contributor-profile", icon="activity"),
        MenuItem(_("Database Admin"), view_name="admin:index", icon="administration"),
    ],
    position=0,
)
