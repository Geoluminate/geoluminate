from django.utils.translation import gettext as _

from geoluminate.contrib.core.view_mixins import ListPluginMixin
from geoluminate.utils import icon
from geoluminate.views import BaseDetailView, BaseFormView, BaseListView

from .filters import ProjectFilter
from .forms import ProjectForm
from .models import Project


class ProjectListView(BaseListView):
    title = _("Projects")
    base_template = "projects/project_list.html"
    object_template = "projects/project_card.html"
    model = Project
    queryset = Project.objects.all().order_by("-created")
    filterset_class = ProjectFilter


class ProjectDetailView(BaseDetailView):
    base_template = "projects/project_detail.html"
    title = _("Project")
    model = Project
    form_class = ProjectForm

    def has_edit_permission(self):
        return True
        # return super().has_edit_permission()

    def has_create_permission(self):
        return True


class ProjectPlugin(ListPluginMixin):
    template_name = "geoluminate/plugins/base_list.html"
    object_template = "projects/project_card.html"
    title = name = _("Projects")
    icon = icon("project")
    description = _("The following projects are associated with the this contributor.")

    def get_queryset(self, *args, **kwargs):
        return self.get_object().projects.all()


class AddProjectView(BaseFormView):
    model = Project
    title = _("Create a new project")
    help_text = None
    form_class = ProjectForm


class ProjectFormView(BaseFormView):
    model = Project
    form_class = ProjectForm
    template_name = "contributors/contributor_form.html"
    success_url = "."
