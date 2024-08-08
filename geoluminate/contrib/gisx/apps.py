from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class TectonicPlateConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "geoluminate.contrib.gis"
    verbose_name = _("GIS")
    verbose_name_plural = _("GIS")
