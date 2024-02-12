from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ProjectsConfig(AppConfig):
    name = "geoluminate.contrib.projects"
    label = "projects"
    verbose_name = _("Projects")
