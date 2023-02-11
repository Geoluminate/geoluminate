from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class LiteratureConfig(AppConfig):
    name = 'literature'
    verbose_name = _('Literature')
