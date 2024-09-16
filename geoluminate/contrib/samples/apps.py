from contextlib import suppress

from django.apps import AppConfig
from django.contrib import admin
from django.utils.translation import gettext_lazy as _


class SamplesConfig(AppConfig):
    name = "geoluminate.contrib.samples"
    label = "samples"
    verbose_name = _("Samples")

    def ready(self) -> None:
        from actstream import registry

        # make sure the Sample model is registered with actstream
        registry.register(self.get_model("Sample"))

        # register the sample children with the admin site
        self.register_sample_children()

        return super().ready()

    def register_sample_children(self):
        from .admin import SampleAdmin
        from .models import Sample

        for model in Sample.get_subclasses():
            with suppress(admin.sites.AlreadyRegistered):
                admin.site.register(model, SampleAdmin)
