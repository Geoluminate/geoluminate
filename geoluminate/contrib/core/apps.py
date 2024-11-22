from contextlib import suppress

from django.apps import AppConfig
from django.contrib import admin
from django.utils.translation import gettext_lazy as _


class CoreConfig(AppConfig):
    name = "geoluminate.contrib.core"
    label = "fairdm"
    verbose_name = _("FairDM")

    def ready(self) -> None:
        from actstream import registry

        # regsiter core models with actstream (follow/unfollow system)
        registry.register(self.get_model("Project"))
        registry.register(self.get_model("Dataset"))
        for model in self.get_model("Sample").get_subclasses():
            registry.register(model)

        self.register_sample_children()
        return super().ready()

    def register_sample_children(self):
        from .admin import SampleAdmin
        from .models import Sample

        # Register all subclasses of Sample with the admin site
        for model in Sample.get_subclasses():
            with suppress(admin.sites.AlreadyRegistered):
                admin.site.register(model, SampleAdmin)
