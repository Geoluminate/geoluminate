from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ProjectConfig(AppConfig):
    name = "geoluminate.contrib.project"
    label = "project"
    verbose_name = _("Project")
    verbose_name_plural = _("Projects")

    def ready(self):
        # This installs the comment_will_be_posted signal
        from . import signals  # noqa
