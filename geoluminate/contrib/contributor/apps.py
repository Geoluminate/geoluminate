from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ContributorConfig(AppConfig):
    name = "geoluminate.contrib.contributor"
    label = "contributor"
    verbose_name = _("Contributor")
