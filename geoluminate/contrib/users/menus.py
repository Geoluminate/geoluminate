from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from simple_menu import MenuItem

from geoluminate.menus import GeoluminateMenuBase


class AccountSidebar(GeoluminateMenuBase):
    """This menu populates the sidebar in the account settings section. It provides links to the different sections that
    allow the user to control their account."""

    menu_name = "account_sidebar"


AccountSidebar.add_items(
    MenuItem(
        _("My Profile"),
        reverse("user:profile"),
        icon="fas fa-user",
    ),
    # MenuItem(
    #     _("Affiliations"),
    #     reverse("user:affiliations"),
    #     icon="fas fa-university",
    # ),
    # MenuItem(
    #     _("Identifiers"),
    #     reverse("user:affiliations"),
    #     icon="fa-solid fa-id-badge",
    # ),
    # MenuItem(
    #     _("Account Settings"),
    #     url="",
    #     icon="fas fa-user-gear",
    # ),
    # MenuItem(
    #     _("Authentication"),
    #     reverse("user:account"),
    #     icon="fas fa-shield",
    # ),
    MenuItem(
        _("Emails"),
        reverse("account_email"),
        icon="fas fa-envelope",
    ),
    MenuItem(
        _("Notifications"),
        reverse("account_email"),
        icon="fas fa-bell",
    ),
    MenuItem(
        title=_("Connected Accounts"),
        url=reverse("socialaccount_connections"),
        icon="fas fa-link",
    ),
    MenuItem(
        title=_("Code of Conduct"),
        url=reverse("code_of_conduct"),
        icon="fas fa-file-contract",
    ),
)
