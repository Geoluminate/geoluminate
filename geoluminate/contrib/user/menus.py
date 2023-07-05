from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from simple_menu import MenuItem

from geoluminate.menus import GeoluminateMenuBase


class UserToolbar(GeoluminateMenuBase):
    menu_name = "user_toolbar"


UserToolbar.add_items(
    MenuItem(
        _("Profile"),
        reverse("user:profile-edit"),
        icon="fas fa-user",
    ),
    MenuItem(
        _("Dashboard"),
        reverse("user:dashboard"),
        icon="fas fa-th-large",
    ),
    MenuItem(
        _("Projects"),
        reverse("user:projects"),
        icon="fa-solid fa-folder-open",
    ),
    MenuItem(
        _("Account"),
        reverse("user:account"),
        icon="fas fa-cogs",
    ),
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
#         _("Organisations"),
#         reverse("user:organisations"),
#         icon=" fas fa-university",
#     ),
# )

# UserToolbar.add_item(
#     MenuItem(
#         _("Review"),
#         reverse("user:review"),
#         icon="fas fa-file-pen",
#     ),
# )
