from typing import Any

from django.db import models
from django.utils.translation import gettext_lazy as _

from geoluminate.views import BaseCreateView, BaseDetailView, BaseListView

from .filters import ProjectFilter
from .forms import ProjectForm
from .models import Project


class ProjectListView(BaseListView):
    model = Project
    queryset = Project.objects.all().order_by("-created")

    filterset_class = ProjectFilter


class ProjectDetailView(BaseDetailView):
    model = Project
    # queryset = Project.objects.all().order_by("-created")
    form_class = ProjectForm
    # template_name = "contributors/contributor_form.html"

    def get_queryset(self):
        return super().get_queryset().order_by("-created")

    def has_edit_permission(self):
        """TODO: Add permissions."""
        # return self.request.user.is_superuser
        return None


class AddProjectView(BaseCreateView):
    model = Project
    title = _("Create a new project")
    help_text = None
    form_class = ProjectForm
