from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UsersConfig(AppConfig):
    name = "geoluminate.contrib.users"
    label = "users"
    verbose_name = _("Users")

    def ready(self):
        from . import receivers  # noqa: F401
