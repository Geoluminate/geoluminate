from django.utils.translation import gettext as _
from django.views.generic import TemplateView

from geoluminate.contrib.contributors.views import ContributorsPlugin
from geoluminate.contrib.datasets.views import DatasetPlugin
from geoluminate.core.plugins import ActivityStream, Discussion
from geoluminate.plugins import project

from .models import Project


@project.page("overview", icon="overview")
class ProjectOverview(TemplateView):
    model = Project
    title = _("Project")
    template_name = "core/plugins/overview.html"


project.register_page(ContributorsPlugin)
project.register_page(DatasetPlugin)
project.register_page(Discussion)
project.register_page(ActivityStream)


# @project.action("flag", icon="fas fa-flag")
# @project.action("download", icon="fas fa-file-zipper")
# class XMLDownload(ProjectDetailView):
#     pass
