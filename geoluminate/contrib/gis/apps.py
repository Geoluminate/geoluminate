from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class GISConfig(AppConfig):
    name = "geoluminate.contrib.gis"
    label = "gis"
    verbose_name = _("GIS")

    def ready(self) -> None:
        from actstream import registry

        registry.register(self.get_model("Location"))

        return super().ready()
