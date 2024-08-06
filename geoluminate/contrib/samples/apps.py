from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class SamplesConfig(AppConfig):
    name = "geoluminate.contrib.samples"
    label = "samples"
    verbose_name = _("Samples")

    def ready(self) -> None:
        from actstream import registry

        registry.register(self.get_model("Sample"))
        registry.register(self.get_model("Location"))

        return super().ready()
