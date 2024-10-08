from django.utils.translation import gettext as _

from geoluminate.core.views.mixins import ListPluginMixin
from geoluminate.views import BaseDetailView, BaseEditView, BaseListView

from .filters import ProjectFilter
from .forms import ProjectForm
from .models import Project


class ProjectListView(BaseListView):
    title = _("Projects")
    queryset = Project.objects.all().order_by("-created")
    filterset_class = ProjectFilter


class ProjectDetailView(BaseDetailView):
    base_template = "projects/project_detail.html"
    title = _("Project")
    model = Project
    form_class = ProjectForm
    extra_context = {
        "menu": "ProjectDetailMenu",
    }


class ProjectEditView(BaseEditView):
    model = Project
    form_class = ProjectForm


class ProjectPlugin(ListPluginMixin):
    title = name = _("Projects")
    icon = "project.svg"

    def get_queryset(self, *args, **kwargs):
        return self.get_object().projects.all()
