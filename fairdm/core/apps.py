from contextlib import suppress

from django.apps import AppConfig, apps
from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from fairdm.metadata import Authority, Citation
from fairdm.registry import registry as fairdm_registry


class FairDMCoreConfig(AppConfig):
    name = "fairdm.core"
    label = "fairdm_core"
    verbose_name = _("FairDM")
    authority = Authority(
        name=_("FairDM Core Development"),
        short_name="FairDM",
        website="https://fairdm.org",
    )
    citation = Citation(
        text="FairDM Core Development Team (2021). FairDM: A FAIR Data Management Tool. https://fairdm.org",
        doi="https://doi.org/10.5281/zenodo.123456",
    )
    repository_url = "https://github.com/FAIR-DM/fairdm"

    def ready(self) -> None:
        # self.register_core_models()
        # self.register_actstream()
        # self.register_sample_children()
        return super().ready()

    # def register_actstream(self):
    #     from actstream import registry

    #     registry.register(self.get_model("Project"))
    #     registry.register(self.get_model("Dataset"))
    #     for model in fairdm_registry.samples:
    #         registry.register(model["class"])

    def register_core_models(self):
        from fairdm.core.models import Measurement, Sample
        from fairdm.registry import registry

        for model in apps.get_models():
            if issubclass(model, Sample | Measurement) and model not in [Sample, Measurement]:
                registry.register(model)

    def register_sample_children(self):
        from .admin import SampleAdmin

        # Register all subclasses of Sample with the admin site
        for model in fairdm_registry.samples:
            with suppress(admin.sites.AlreadyRegistered):
                admin.site.register(model["class"], SampleAdmin)
