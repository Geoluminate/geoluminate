from django.conf import settings
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from geoluminate.api.serializers import (
    DatasetSerializer,
    ProjectSerializer,
    SampleSerializer,
)
from geoluminate.tables import GeoluminateTable, ServerSideProcessing

from .models import Project


class ProjectTable(GeoluminateTable):
    config_class = ServerSideProcessing
    url = reverse_lazy("project-list")
    serializer_class = ProjectSerializer
    model = Project

    # hidden_fields = ["image"]
    search_fields = ["title"]
    # search_panes = ["status"]
    # filter_fields = ["user"]
    row_template = "handlebars/project.html"

    extra_attributes = {  # noqa: RUF012
        "web_url": {"title": ""},
        # "start_date": {"title": _("Start")},
        # "end_date": {"title": _("End")},
    }
