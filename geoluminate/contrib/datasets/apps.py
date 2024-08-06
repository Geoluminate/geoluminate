from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class DatasetsConfig(AppConfig):
    name = "geoluminate.contrib.datasets"
    label = "datasets"
    verbose_name = _("Datasets")

    # dataset = {"filterset_class": "datasets.filters.DatasetFilter", "filterset_fields": {"title": ["icontains"]}}

    def ready(self) -> None:
        from actstream import registry

        registry.register(self.get_model("Dataset"))

        return super().ready()
