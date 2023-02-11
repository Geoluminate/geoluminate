from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ResearchProjectConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'research_project'
    verbose_name = _("research project")
