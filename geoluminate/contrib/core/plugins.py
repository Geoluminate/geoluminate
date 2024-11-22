from django.urls import reverse
from django.utils.translation import gettext as _

from geoluminate import plugins

# from geoluminate.core.plugins import TablePlugin
from geoluminate.core.view_mixins import ListPluginMixin

from .forms import DatasetForm
from .models import Dataset, Project
from .views import MeasurementListView, SampleListView


@plugins.register(to=["contributor"])
class ProjectPlugin(ListPluginMixin):
    title = name = _("Projects")
    icon = "project"
    model = Project

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["create_view_url"] = (
            reverse(f"{context['base_model_name']}-create") + "?" + f"related={self.kwargs.get('pk')}"
        )
        return context

    def get_queryset(self, *args, **kwargs):
        return self.base_object.projects.all()


@plugins.register(to=["project", "contributor"])
class DatasetPlugin(ListPluginMixin):
    title = name = _("Datasets")
    icon = "dataset"
    model = Dataset
    forms = [DatasetForm]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["create_view_url"] = (
            reverse(f"{context['base_model_name']}-create") + "?" + f"project={self.kwargs.get('pk')}"
        )
        context["forms"] = [f(request=self.request) for f in self.forms]
        return context

    def get_queryset(self, *args, **kwargs):
        return self.base_object.datasets.all()


@plugins.register(to=["dataset"])
class SamplePlugin(SampleListView):
    title = name = _("Samples")
    icon = "sample"
    extra_context = {"can_add": True}

    def get_queryset(self, *args, **kwargs):
        return self.base_object.samples.instance_of(self.model)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["create_view_url"] = reverse("sample-create")
        return context


@plugins.register(to=["dataset", "sample"])
class MeasurementPlugin(MeasurementListView):
    title = name = _("Measurements")
    icon = "measurement"

    def get_queryset(self, *args, **kwargs):
        return self.base_object.measurements.instance_of(self.model)
