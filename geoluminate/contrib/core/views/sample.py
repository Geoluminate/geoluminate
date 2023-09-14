from auto_datatables.views import AutoTableMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView

from geoluminate.tables import ClientSideProcessing

from ..models import Sample
from ..tables import SampleTable
from .base import BaseListView, ProjectBaseView

list_view = BaseListView.as_view(
    template_name="project/list.html",
    table=SampleTable,
    # filter=ProjectFilter,
)


class SampleList(TemplateView, AutoTableMixin):
    template_name = "auto_datatables/base.html"
    table = SampleTable


class SampleDetail(ProjectBaseView):
    model = Sample
    template_name = "sample/detail.html"
    contributor_key = "samples"

    panels = [
        dict(
            title=_("About"),
            template_name="project/partials/about.html",
            icon="fas fa-circle-info",
        ),
        dict(
            title=_("Contributors"),
            template_name="project/partials/contributors.html",
            icon="fas fa-users",
        ),
        dict(
            title=_("Timeline"),
            template_name="project/partials/timeline.html",
            icon="fas fa-timeline",
        ),
        dict(
            title=_("Map"),
            template_name="geoluminate/components/map.html",
            icon="fas fa-map-location-dot",
        ),
        dict(
            title=_("Samples"),
            template_name="partials/sample_list.html",
            icon="fas fa-database",
        ),
        dict(
            title=_("Measurements"),
            template_name="partials/sample_list.html",
            icon="fas fa-flask-vial",
        ),
        dict(
            title=_("Discussion"),
            template_name="geoluminate/components/comments.html",
            icon="fas fa-comments",
        ),
        dict(
            title=_("Attachments"),
            template_name="geoluminate/components/comments.html",
            icon="fas fa-paperclip",
        ),
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
