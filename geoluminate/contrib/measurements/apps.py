from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class MeasurementsConfig(AppConfig):
    name = "geoluminate.contrib.measurements"
    label = "measurements"
    verbose_name = _("Measurements")
