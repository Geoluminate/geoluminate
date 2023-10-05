from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from simple_menu import MenuItem

from geoluminate.menus import GeoluminateMenuBase


class AccountSidebar(GeoluminateMenuBase):
    """This menu populates the sidebar in the account settings section. It provides links to the different sections that
    allow the user to control their account."""

    menu_name = "account_sidebar"


AccountSidebar.add_items(
    # MenuItem(
    #     _("Dashboard"),
    #     url=reverse("user:dashboard"),
    #     icon="fas fa-table-cells-large",
    # ),
    MenuItem(
        _("Your Contributions"),
        url="",
    ),
    MenuItem(
        _("Projects"),
        url=reverse("user:projects"),
        icon="fas fa-project-diagram",
    ),
    MenuItem(
        _("Datasets"),
        url=reverse("user:datasets"),
        icon="fas fa-folder-open",
    ),
    MenuItem(
        _("Reviews"),
        url=reverse("user:reviews"),
        icon="fas fa-book-open-reader",
    ),
    MenuItem(
        _("Public Information"),
        url="",
    ),
    MenuItem(
        _("Contributor Profile"),
        reverse("user:profile_edit"),
        icon="fas fa-user",
    ),
    MenuItem(
        _("Affiliations"),
        reverse("user:affiliations"),
        icon="fas fa-university",
    ),
    MenuItem(
        _("Identifiers"),
        reverse("user:affiliations"),
        icon="fa-solid fa-id-badge",
    ),
    MenuItem(
        _("Account Settings"),
        url="",
        icon="fas fa-cogs",
    ),
    MenuItem(
        _("Authentication"),
        reverse("user:account"),
        icon="fas fa-shield",
    ),
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
        _("Agreements"),
        url="",
    ),
    MenuItem(
        title=_("Code of Conduct"),
        url=reverse("code_of_conduct"),
        icon="fas fa-file-contract",
    ),
)
