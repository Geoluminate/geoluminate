from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UsersConfig(AppConfig):
    name = "geoluminate.contrib.users"
    label = "users"
    verbose_name = _("Authentication and Authorization")

    def ready(self):
        from actstream import registry

        from . import receivers  # noqa: F401

        registry.register(self.get_model("User"))
        return super().ready()
