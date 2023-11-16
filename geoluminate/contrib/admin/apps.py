from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AdminConfig(AppConfig):
    name = "geoluminate.contrib.admin"
    label = "geoluminate_admin"
    verbose_name = _("Admin")
