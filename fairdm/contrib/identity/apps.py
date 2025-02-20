from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class FairDMIdentityConfig(AppConfig):
    name = "fairdm.contrib.identity"
    label = "identity"
    verbose_name = _("Identity")
