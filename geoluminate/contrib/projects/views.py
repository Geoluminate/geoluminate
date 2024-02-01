from typing import Any

from django.db import models
from django.utils.translation import gettext_lazy as _

from geoluminate.views import BaseDetailView, BaseFormView, BaseListView

from .filters import ProjectFilter
from .forms import ProjectForm
from .models import Project


class ProjectListView(BaseListView):
    model = Project
    queryset = Project.objects.all().order_by("-created")
    filterset_class = ProjectFilter

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # from formset.templatetags.formsetify import _formsetify

        # form = _formsetify(context["filter"].form)

        # # print(form.__dict__)
        # form_id = "id_%s" % form.__class__
        # print(form_id)
        return context


class ProjectDetailView(BaseDetailView):
    model = Project
    # queryset = Project.objects.all().order_by("-created")
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
