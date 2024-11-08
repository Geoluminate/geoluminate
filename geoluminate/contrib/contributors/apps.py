from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ContributorsConfig(AppConfig):
    name = "geoluminate.contrib.contributors"
    label = "contributors"
    verbose_name = _("Community")

    def ready(self):
        from actstream import registry

        # registry.register(self.get_model("Contributor"))
        registry.register(self.get_model("Person"))
        registry.register(self.get_model("Organization"))
        return super().ready()
