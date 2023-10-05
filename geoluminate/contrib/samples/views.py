from auto_datatables.views import AutoTableMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView

from geoluminate.contrib.core.views import BaseListView, ProjectBaseView
from geoluminate.tables import ClientSideProcessing

from .models import Sample
from .tables import SampleTable

list_view = BaseListView.as_view(
    table=SampleTable,
    # filter=ProjectFilter,
)


class SampleList(TemplateView, AutoTableMixin):
    template_name = "auto_datatables/base.html"
    table = SampleTable


class SampleDetail(ProjectBaseView):
    model = Sample
    template_name = "core/sample_detail.html.html"
    contributor_key = "samples"
    panels = [  # noqa: RUF012
        ("fas fa-circle-info", _("About"), "core/pages/descriptions.html"),
        ("fas fa-users", _("Contributors"), "core/pages/contributors.html"),
        ("fas fa-timeline", _("Timeline"), "core/pages/timeline.html"),
        ("fas fa-map-location-dot", _("Map"), "geoluminate/components/map.html"),
        ("fas fa-database", _("Samples"), "core/snippets/sample_list.html"),
        ("fas fa-flask-vial", _("Measurements"), "core/snippets/sample_list.html"),
        ("fas fa-comments", _("Discussion"), "geoluminate/components/comments.html"),
        ("fas fa-paperclip", _("Attachments"), "geoluminate/components/comments.html"),
    ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tables"] = {
            "samples": SampleTable(
                url=reverse("sample-list", kwargs={"dataset_uuid": self.object.uuid}),
                config_class=ClientSideProcessing(buttons=[], dom="pt"),
                layout_overrides={},
            ),
        }
        return context


class SampleEdit(LoginRequiredMixin, SampleDetail):
    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        if self.object:
            context_data["change"] = True
        else:
            context_data["add"] = True
        return context_data

    def form_valid(self, form):
        if extra_data := self.get_extra_data():
            if extra_data.get("add") is True:
                form.instance.save()
            if extra_data.get("delete") is True:
                form.instance.delete()
                return JsonResponse({"success_url": self.get_success_url()})
        return super().form_valid(form)

    def get_object(self, queryset=None):
        if self.extra_context["add"] is False:
            return super().get_object(queryset)

    # def form_valid(self, form):
    #     if extra_data := self.get_extra_data():
    #         if extra_data.get("delete") is True:
    #             self.object.delete()
    #             success_url = self.get_success_url()
    #             response_data = {"success_url": force_str(success_url)} if success_url else {}
    #             return JsonResponse(response_data)
    #     return super().form_valid(form)


# class MeasurementDetailView(DetailView):
#     model = Sample
#     template_name = "core/sample_detail.html.html"
#     slug_field = "uuid"

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         return context

#     # function that will extract fields from self.model using a list of fields names
#     def get_key_dates(self, fields):
#         key_dates = []
#         for field in fields:
#             # f = self.model._meta.get_field(field)
#             key_dates.append(
#                 {
#                     "field": field,
#                     "value": getattr(self.object, field),
#                     "label": self.model._meta.get_field(field).verbose_name,
#                 }
#             )
#         return key_dates

#     def get_queryset(self):
#         return super().get_queryset()
