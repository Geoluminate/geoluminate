from django.urls import reverse
from django.utils.translation import gettext as _

from geoluminate.core.views.mixins import ListPluginMixin
from geoluminate.menus import DatasetMenu
from geoluminate.views import BaseCRUDView

from .filters import DatasetFilter
from .forms import DatasetForm
from .models import Dataset


class DatasetCRUDView(BaseCRUDView):
    model = Dataset
    form_class = DatasetForm
    menu = DatasetMenu
    filterset_class = DatasetFilter
    paginate_by = 10
    sidebar_fields = [
        (
            None,
            {
                "fields": ["title", "project", "created", "modified"],
            },
        ),
    ]

    def get_form(self, data=None, files=None, **kwargs):
        kwargs["request"] = self.request
        # if self.role.value == "create":
        # kwargs["initial"] = {"project": self.request.GET.get("project")}
        return super().get_form(data, files, **kwargs)


class DatasetPlugin(ListPluginMixin):
    title = name = _("Datasets")
    icon = "dataset"
    model = Dataset
    forms = [DatasetForm]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["create_view_url"] = (
            reverse(f"{context['model_name']}-create") + "?" + f"project={self.kwargs.get('pk')}"
        )
        context["forms"] = [f(request=self.request) for f in self.forms]
        return context

    def get_queryset(self, *args, **kwargs):
        return self.base_object.datasets.all()
