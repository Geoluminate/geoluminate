from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class DjangoLicensingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'django_licensing'
    verbose_name = _("licensing")
