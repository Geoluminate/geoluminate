from django.apps import AppConfig
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class CoreConfig(AppConfig):
    name = "geoluminate.contrib.core"
    label = "core"
    verbose_name = "core"

    def ready(self):
        # This installs the comment_will_be_posted signal
        from . import receivers  # noqa
