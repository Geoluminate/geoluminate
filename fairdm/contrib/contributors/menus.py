from account_management.menus import AccountMenu, FloatingAccountMenu
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from flex_menu import Menu, MenuItem
from flex_menu.utils import user_is_anonymous, user_is_authenticated


def get_contributor_url(request):
    return reverse_lazy("contributor-detail", args=[request.user.id])


AccountMenu.insert(
    [
        Menu(
            "ProfileMenu",
            label=_("Profile"),
            children=[
                MenuItem(_("Edit Profile"), view_name="contributor-profile", icon="user"),
                MenuItem(_("Preferences"), view_name="contributor-identifiers", icon="preferences"),
                MenuItem(_("Identifiers"), view_name="contributor-identifiers", icon="identifier"),
                MenuItem(_("Affiliations"), view_name="contributor-affiliations", icon="organization"),
            ],
        ),
        Menu(
            "ActivityMenu",
            label=_("Activity"),
            children=[
                MenuItem(_("Recent Activity"), view_name="home", icon="activity"),
                MenuItem(_("Following"), view_name="home", icon="star-solid"),
                MenuItem(_("Followed by"), view_name="home", icon="identifier"),
            ],
        ),
    ],
    position=0,
)


FloatingAccountMenu.insert(
    [
        MenuItem(_("Profile"), url=get_contributor_url, icon="user"),
        MenuItem(_("Manage Account"), view_name="account-management", icon="activity"),
        MenuItem(_("Recent Activity"), view_name="contributor-profile", icon="activity"),
        MenuItem(_("Database Admin"), view_name="admin:index", icon="administration"),
        MenuItem(_("Log in"), view_name="account_login", icon="login", check=user_is_anonymous),
        MenuItem(_("Log out"), view_name="account_logout", icon="logout", check=user_is_authenticated),
    ],
    position=0,
)
