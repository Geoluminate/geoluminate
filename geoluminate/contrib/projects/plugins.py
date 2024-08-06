from django.utils.translation import gettext as _
from django.views.generic import UpdateView
from formset.views import FileUploadMixin, FormViewMixin

from geoluminate.contrib.contributors.views import ContributorsPlugin
from geoluminate.contrib.core.plugins import ActivityStream, Discussion, Map
from geoluminate.contrib.datasets.views import DatasetPlugin
from geoluminate.plugins import PluginRegistry
from geoluminate.utils import icon

from .models import Project
from .views import ProjectDetailView

project = PluginRegistry(base=ProjectDetailView)


@project.page("overview", icon=icon("overview"))
class ProjectOverview(FileUploadMixin, FormViewMixin, UpdateView):
    model = Project
    title = _("Project")
    template_name = "geoluminate/plugins/overview.html"


project.register_page(ContributorsPlugin)
project.register_page(DatasetPlugin)
# project.register_page(Map)


@project.page()
class ProjectMap(Map):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for dataset in self.get_object().datasets.all():
            context["map_source_list"].update(self.serialize_dataset_samples(dataset))
        return context


project.register_page(Discussion)
project.register_page(ActivityStream)


@project.action("flag", icon="fas fa-flag")
@project.action("download", icon="fas fa-file-zipper")
class XMLDownload(ProjectDetailView):
    pass
