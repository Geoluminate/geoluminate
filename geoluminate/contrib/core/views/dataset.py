from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import modelform_factory
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView, ListView, TemplateView
from django.views.generic.edit import CreateView
from formset.views import EditCollectionView, FormView

from geoluminate.tables import ClientSideProcessing

from ..filters import DatasetFilter
from ..forms import DatasetFormCollection
from ..models import Dataset
from ..tables import DatasetTable, SampleTable
from .base import BaseListView, CoreListView, GenericCreateView, ProjectBaseView


class DatasetListView(CoreListView):
    model = Dataset


list_view = DatasetListView.as_view()


class DatasetDetail(ProjectBaseView):
    model = Dataset
    template_name = "dataset/detail.html"

    panels = [
        {
            "title": _("About"),
            "template_name": "project/partials/about.html",
            "icon": "fas fa-circle-info",
        },
        {
            "title": _("Descriptions"),
            "template_name": "core/description_list.html",
            "icon": "fas fa-users",
        },
        {
            "title": _("Contributors"),
            "template_name": "project/partials/contributors.html",
            "icon": "fas fa-users",
        },
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
        # dict(
        #     title=_("Samples"),
        #     template_name="partials/sample_list.html",
        #     icon="fas fa-database",
        # ),
        # dict(
        #     title=_("Measurements"),
        #     template_name="partials/sample_list.html",
        #     icon="fas fa-flask-vial",
        # ),
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


class DatasetEdit(LoginRequiredMixin, DatasetDetail, FormView):
    collection_class = DatasetFormCollection


edit_view = DatasetDetail.as_view(extra_context={"edit": True})
add_view = GenericCreateView.as_view(model=Dataset, fields=["title"])
