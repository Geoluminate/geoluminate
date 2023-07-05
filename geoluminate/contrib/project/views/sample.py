from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.utils.translation import gettext_lazy as _
from django.views.generic import UpdateView
from django.views.generic.base import RedirectView
from django.views.generic.detail import DetailView
from formset.views import FileUploadMixin, FormViewMixin

from geoluminate.views import LargeTableView

from ..models import Sample


class SampleDataTable(LargeTableView):
    model = Sample
    fields = ["id", "get_absolute_url_button", "name"]
    extra_attributes = {
        "get_absolute_url_button": {"title": "", "orderable": "false"},
        # "start_date": {"title": _("Start")},
        # "end_date": {"title": _("End")},
    }


class SampleDetailView(DetailView):
    model = Sample
    template_name = "sample/detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context["key_dates"] = self.get_key_dates(["start_date", "end_date"])
        # context["contributors"] = Contributor.objects.filter(dataset__project=self.object).distinct()
        return context

    # function that will extract fields from self.model using a list of fields names
    def get_key_dates(self, fields):
        key_dates = []
        for field in fields:
            # f = self.model._meta.get_field(field)
            key_dates.append(
                {
                    "field": field,
                    "value": getattr(self.object, field),
                    "label": self.model._meta.get_field(field).verbose_name,
                }
            )
        return key_dates

    def get_queryset(self):
        return super().get_queryset()
