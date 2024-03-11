from django.views.generic import UpdateView
from formset.views import FileUploadMixin, FormViewMixin

from geoluminate.contrib.contributors.views import ContributorsPlugin
from geoluminate.contrib.core.plugins import ActivityStream, Discussion, Map
from geoluminate.contrib.datasets.views import DatasetPlugin
from geoluminate.plugins import PluginRegistry
from geoluminate.utils import icon

from .models import Project
from .views import ProjectDetailView

project = PluginRegistry("projects", base=ProjectDetailView)


@project.page("overview", icon=icon("overview"))
class ProjectOverview(ProjectDetailView, FileUploadMixin, FormViewMixin, UpdateView):
    model = Project
    template_name = "geoluminate/plugins/overview.html"


project.register_page(ContributorsPlugin)
project.register_page(DatasetPlugin)
project.register_page(Map)
project.register_page(Discussion)
project.register_page(ActivityStream)


@project.action("flag", icon="fas fa-flag")
@project.action("download", icon="fas fa-file-zipper")
class XMLDownload(ProjectDetailView):
    pass
