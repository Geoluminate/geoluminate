from django.utils.translation import gettext as _

from geoluminate.contrib.core.view_mixins import ListPluginMixin
from geoluminate.utils import icon, label
from geoluminate.views import BaseDetailView, BaseEditView, BaseListView, BaseTableView

from .forms import SampleForm
from .models import Sample
from .tables import SampleTable


class SampleListView(BaseListView):
    title = _("Datasets")
    queryset = Sample.objects.prefetch_related("contributors").order_by("-created")
    # filterset_class = DatasetFilter


class SampleDetailView(BaseDetailView):
    base_template = "samples/sample_detail.html"
    model = Sample
    title = _("Sample")
    sidebar_fields = [
        "name",
        "parent",
        "dataset",
        "location",
        "status",
    ]

    def get_object(self):
        # note: we are using base_objects here to get the base model (Sample) instance
        obj = self.base.model.base_objects.get(pk=self.kwargs.get("pk"))
        self.real = obj.get_real_instance()
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["real"] = self.real
        context[self.real._meta.model_name] = self.real
        base_fields = [f.name for f in self.base.model._meta.fields]
        context["additional_fields"] = [f.name for f in self.real._meta.fields if f.name not in base_fields]
        if "sample_ptr" in context["additional_fields"]:
            context["additional_fields"].remove("sample_ptr")
        return context

    def get_meta_title(self, context):
        return f"{self.real}"


class SampleEditView(BaseEditView):
    model = Sample
    form_class = SampleForm
    related_name = "dataset"


class SamplePlugin(ListPluginMixin):
    title = name = _("Samples")
    icon = icon("sample")
    # model = Sample
    template_name = "contributors/contribution_list.html"
    object_template = "samples/sample_card.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["sample_poly_choices"] = Sample.get_polymorphic_choices()
        print(context)
        return context

    def get_queryset(self, *args, **kwargs):
        return self.get_object().samples.all()


class SampleTableView(BaseTableView):
    table = SampleTable
    table_view_name = "sample-list"


class SampleTablePlugin(BaseTableView):
    table = SampleTable
    template_name = "geoluminate/base/table_view.html"
    title = name = label("sample")["verbose_name_plural"]
    icon = icon("sample")
