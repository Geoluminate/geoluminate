from django.urls import reverse
from django.utils.translation import gettext as _

from geoluminate.core.views.mixins import ListPluginMixin
from geoluminate.menus import ProjectMenu
from geoluminate.views import BaseCRUDView

from .filters import ProjectFilter
from .forms import ProjectForm
from .models import Project


class ProjectCRUDView(BaseCRUDView):
    model = Project
    form_class = ProjectForm
    menu = ProjectMenu
    filterset_class = ProjectFilter
    sidebar_fields = [
        (
            _("Basic Information"),
            {
                "fields": ["title", "created", "modified"],
            },
        ),
    ]


class ProjectPlugin(ListPluginMixin):
    title = name = _("Projects")
    icon = "project.svg"
    model = Project

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["create_view_url"] = (
            reverse(f"{context['model_name']}-create") + "?" + f"related={self.kwargs.get('pk')}"
            # + f"?next={self.request.path}"
        )
        return context

    def get_queryset(self, *args, **kwargs):
        return self.base_object.projects.all()
