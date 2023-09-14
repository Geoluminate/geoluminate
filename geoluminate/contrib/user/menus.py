from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from simple_menu import MenuItem

from geoluminate.menus import GeoluminateMenuBase


class UserToolbar(GeoluminateMenuBase):
    """This menu populates the user toolbar which opens as a slide in menu on the right side of the screen.
    It is triggered by the user toolbar button in the top right corner of the screen."""

    menu_name = "user_toolbar"


UserToolbar.add_items(
    MenuItem(
        _("Profile"),
        reverse("user:profile_edit"),
        icon="fas fa-user",
    ),
    # MenuItem(
    #     _("Dashboard"),
    #     reverse("user:dashboard"),
    #     icon="fas fa-th-large",
    # ),
    MenuItem(
        _("Projects"),
        reverse("user:projects"),
        icon="fa-solid fa-folder-open",
    ),
    # MenuItem(
    #     _("Account"),
    #     reverse("account"),
    #     icon="fas fa-cogs",
    # ),
    MenuItem(
        title=_("Administration"),
        url=reverse("admin:index"),
        check=lambda request: request.user.is_staff,
        icon="fas fa-user-shield",
    ),
    MenuItem(
        title=_("Logout"),
        url=reverse("account_logout"),
        weight=100,
        check=lambda request: request.user.is_authenticated,
        icon="fas fa-right-from-bracket",
        extra_classes="mt-auto bg-primary-subtle",
    ),
)


# UserToolbar.add_item(
#     MenuItem(
#         _("Review"),
#         reverse("user:review"),
#         icon="fas fa-file-pen",
#     ),
# )


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
        _("Account Settings"),
        url="",
        icon="fas fa-cogs",
    ),
    MenuItem(
        _("Profile"),
        reverse("user:profile_edit"),
        icon="fas fa-user",
    ),
    MenuItem(
        _("Affiliations"),
        reverse("user:affiliations"),
        icon="fas fa-university",
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
