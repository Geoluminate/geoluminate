from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from simple_menu import Menu, MenuItem

# menu group for unauthenticated users
Menu.add_item(
    "user_navbar_widget",
    MenuItem(
        "User",
        reverse("user:profile"),
        check=lambda request: not request.user.is_authenticated,
        children=(
            MenuItem(
                _("Login"),
                reverse("account_login"),
                icon="fas fa-user",
            ),
            MenuItem(
                _("Register"),
                reverse("account_signup"),
                icon="fas fa-th-large",
            ),
        ),
    ),
)


# menu group for authenticated users
Menu.add_item(
    "user_navbar_widget",
    MenuItem(
        "User",
        reverse("user:profile"),
        check=lambda request: request.user.is_authenticated,
        children=(
            MenuItem(
                _("Profile"),
                reverse("user:profile"),
                icon="fas fa-user",
            ),
            MenuItem(
                _("Dashboard"),
                reverse("user:dashboard"),
                icon="fas fa-th-large",
            ),
            MenuItem(
                _("Settings"),
                reverse("user:account"),
                icon="fas fa-cogs",
            ),
        ),
    ),
)


# menu group for staff users
Menu.add_item(
    "user_navbar_widget",
    MenuItem(
        "Staff",
        reverse("user:profile"),
        check=lambda request: request.user.is_staff,
        children=(
            MenuItem(
                _("Admin"),
                reverse("admin:index"),
                icon="fas fa-user-shield",
            ),
            MenuItem(
                _("Edit Page"),
                reverse("user:dashboard"),
                icon="fas fa-pencil-alt",
            ),
        ),
    ),
)


# menu group for authenticated users to logout or provide feedback
Menu.add_item(
    "user_navbar_widget",
    MenuItem(
        "User",
        reverse("user:profile"),
        check=lambda request: request.user.is_authenticated,
        children=(
            MenuItem(
                _("Profile"),
                reverse("user:profile"),
                icon="fas fa-user",
            ),
            MenuItem(
                _("Dashboard"),
                reverse("user:dashboard"),
                icon="fas fa-th-large",
            ),
            MenuItem(
                _("Settings"),
                reverse("user:account"),
                icon="fas fa-cogs",
            ),
        ),
    ),
)
