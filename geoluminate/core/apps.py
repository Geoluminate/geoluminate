from django.apps import AppConfig


class CoreConfig(AppConfig):
    name = "geoluminate.core"
    label = "core"
    verbose_name = "core"

    def ready(self):
        # This installs the comment_will_be_posted signal
        from . import receivers  # noqa: F401
