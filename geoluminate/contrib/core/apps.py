from django.apps import AppConfig


class CoreConfig(AppConfig):
    name = "geoluminate.contrib.core"
    label = "core"
    verbose_name = "core"

    def ready(self):
        # This installs the comment_will_be_posted signal
        from . import receivers  # noqa: F401
