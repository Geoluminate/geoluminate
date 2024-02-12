from django.utils.translation import gettext_lazy as _

from geoluminate.views import BaseDetailView, BaseFormView, BaseListView

from .filters import ProjectFilter
from .forms import ProjectForm
from .models import Project


class ProjectListView(BaseListView):
    model = Project
    queryset = Project.objects.all().order_by("-created")
    filterset_class = ProjectFilter
    object_template = "projects/project_card.html"


class ProjectDetailView(BaseDetailView):
    model = Project
    form_class = ProjectForm
    # template_name = "contributors/contributor_form.html"

    def get_queryset(self):
        return super().get_queryset().order_by("-created")

    def has_edit_permission(self):
        """TODO: Add permissions."""
        return super().has_edit_permission()


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
