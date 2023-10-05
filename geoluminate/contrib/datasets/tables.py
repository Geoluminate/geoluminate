from django.conf import settings
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from geoluminate.api.serializers import (
    DatasetSerializer,
    ProjectSerializer,
    SampleSerializer,
)
from geoluminate.tables import GeoluminateTable, ServerSideProcessing

from .models import Dataset, Measurement, Project, Sample


class DatasetTable(GeoluminateTable):
    config_class = ServerSideProcessing
    url = reverse_lazy("dataset-list")
    model = Dataset
    serializer_class = DatasetSerializer
    # row_template = "handlebars/dataset.html"
    row_template = "handlebars/project.html"

    # visible_fields = ["absolute_url", "title"]
    search_fields = ["title"]

    extra_attributes = {  # noqa: RUF012
        "web_url": {"title": ""},
        # "start_date": {"title": _("Start")},
        # "end_date": {"title": _("End")},
    }
