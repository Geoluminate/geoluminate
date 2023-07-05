from django.utils.translation import gettext_lazy as _
from django.views.generic.detail import DetailView

from geoluminate.views import SmallTableView

from ..models import Dataset


class DatasetDataTable(SmallTableView):
    model = Dataset
    fields = ["id", "get_absolute_url_button", "name", "description", "start_date", "end_date"]
    search_fields = ["name"]
    stateSave = False
    extra_attributes = {
        "get_absolute_url_button": {"title": "", "orderable": "false"},
        "start_date": {"title": _("Start")},
        "end_date": {"title": _("End")},
    }


class DatasetDetailView(DetailView):
    model = Dataset
    template_name = "datasets/detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["key_dates"] = self.get_key_dates(["start_date", "end_date"])
        return context

    def get_key_dates(self, fields):
        key_dates = []
        for field in fields:
            key_dates.append(
                {
                    "field": field,
                    "value": getattr(self.object, field),
                    "label": self.model._meta.get_field(field).verbose_name,
                }
            )
        return key_dates

    def get_queryset(self):
        return super().get_queryset().prefetch_related("contributors")
