from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from simple_menu import MenuItem

ContributorNav = [
    MenuItem(
        _("Profile"),
        reverse_lazy("user:profile_edit"),
        icon="fa-solid fa-user",
    ),
    MenuItem(
        _("Network"),
        reverse_lazy("user:profile_edit"),
        icon="fa-solid fa-circle-nodes",
    ),
    MenuItem(
        _("Timeline"),
        reverse_lazy("user:profile_edit"),
        icon="fa-solid fa-chart-line",
    ),
    MenuItem(
        _("Projects"),
        url=reverse_lazy("user:projects"),
        icon="fas fa-project-diagram",
    ),
    MenuItem(
        _("Datasets"),
        url=reverse_lazy("user:datasets"),
        icon="fas fa-folder-open",
    ),
    MenuItem(
        _("Samples"),
        url=reverse_lazy("user:reviews"),
        icon="fas fa-database",
    ),
    MenuItem(
        _("Map"),
        reverse_lazy("user:affiliations"),
        icon="fas fa-map-location-dot",
    ),
    MenuItem(
        _("Activity"),
        reverse_lazy("user:affiliations"),
        icon="fa-solid fa-bars-staggered",
    ),
]
