from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from geoluminate.tables import GeoluminateTable, ServerSideProcessing

from .models import Sample

# class MeasurementDataTable(GeoluminateTable):
#     table_config_class = ServerSideProcessing
#     model = Sample
#     fields = ["id", "get_absolute_url_button", "title"]
#     # extra_attributes = {
#     #     "get_absolute_url_button": {"title": "", "orderable": "false"},
#     # }


class SampleTable(GeoluminateTable):
    config_class = ServerSideProcessing
    url = reverse_lazy("sample-list")
    model = Sample
    # serializer_class = SampleSerializer

    # visible_fields = ["absolute_url", "title"]
    search_fields = ["title"]

    extra_attributes = {  # noqa: RUF012
        # "get_absolute_url": {"title": ""},
        # "start_date": {"title": _("Start")},
        # "end_date": {"title": _("End")},
    }
