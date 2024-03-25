from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ConfigurationConfig(AppConfig):
    name = "geoluminate.contrib.configuration"
    label = "configuration"
    verbose_name = _("Geoluminate Configuration")
