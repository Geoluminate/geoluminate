from django.contrib.gis.db.models.functions import Centroid
from django.views.generic import TemplateView, UpdateView
from formset.views import FileUploadMixin, FormViewMixin

from geoluminate.contrib.contributors.models import Contribution, Contributor
from geoluminate.contrib.contributors.views import (
    ContributionListView,
    ContributorListView,
)
from geoluminate.contrib.datasets.views import DatasetListView
from geoluminate.plugins import project
from geoluminate.utils import icon
from geoluminate.views import BaseListView

from .forms import ProjectForm
from .models import Project
from .views import ProjectDetailView, ProjectListView


# @project.page("timeline", icon=icon("timeline"))
@project.page("datasets", icon=icon("dataset"))
class ProjectDatasetsView(ProjectDetailView, DatasetListView):
    template_name = "datasets/plugin_list.html"

    def get_queryset(self, *args, **kwargs):
        # MAKE SURE THIS DISTINGUISHES BETWEEN PUBLIC AND PRIVATE DATASETS
        return self.get_object().datasets.all()


@project.page("overview", icon=icon("overview"))
class ProjectOverview(ProjectDetailView, FileUploadMixin, FormViewMixin, UpdateView):
    model = Project
    template_name = "geoluminate/plugins/overview.html"


@project.page("contributors", icon=icon("contributors"))
class ProjectContributorsView(ProjectDetailView, ContributionListView):
    header = "Project Contributors"
    # def get_queryset(self, *args, **kwargs):
    #     # get all Contributor objects that are associated with this project
    #     return self.get_object().contributors.select_related("profile")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filter"] = False
        return context

    def get_queryset(self, *args, **kwargs):
        return self.get_object().contributors.select_related("profile")


@project.action("flag", icon="fas fa-flag")
@project.action("download", icon="fas fa-file-zipper")
class XMLDownload(ProjectDetailView, TemplateView):
    template_name = "geoluminate/placeholder.html"


@project.page("activity", icon=icon("activity"))
class ContributorActivityView(ProjectDetailView, TemplateView):
    template_name = "geoluminate/plugins/activity_stream.html"