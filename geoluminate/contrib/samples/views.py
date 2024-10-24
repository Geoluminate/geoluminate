from django.forms import modelform_factory
from django.http import HttpResponseRedirect
from django.utils.translation import gettext as _
from django.views.generic import TemplateView
from django_tables2 import tables
from django_tables2.views import SingleTableMixin

from geoluminate.core.views.mixins import ListPluginMixin, PolymorphicSubclassBaseView, PolymorphicSubclassMixin
from geoluminate.views import BaseDetailView, BaseListView, BaseUpdateView

from .forms import SampleForm
from .models import Sample


class SampleTypeListView(PolymorphicSubclassMixin, BaseListView):
    title = _("Sample Types")
    model = Sample
    filterset_fields = ["status"]
    list_url = "sample-list"
    detail_url = "sample-type-detail"


class SampleTypeDetailView(PolymorphicSubclassBaseView, TemplateView):
    """Lists all the measurement types available in the database."""

    base_model = Sample

    def get(self, request, *args, **kwargs):
        self.model = self.get_model()
        return super().get(request, *args, **kwargs)

    def get_template_names(self):
        return ["samples/sample_type_detail.html"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = _("Sample Type Detail")
        context["model"] = self.model
        context["metadata"] = self.model.get_metadata()
        return context


class SampleListView(PolymorphicSubclassBaseView, BaseListView):
    title = _("Datasets")
    base_model = Sample
    # queryset = Sample.objects.prefetch_related("contributors").order_by("-created")
    # filterset_class = DatasetFilter


class SampleDetailView(BaseDetailView):
    base_template = "samples/sample_detail.html"
    model = Sample
    title = _("Sample")
    sidebar_exclude = ["sample_ptr", "polymorphic_ctype", "created", "modified", "options", "path", "depth", "numchild"]
    extra_context = {
        "menu": "SampleDetailMenu",
    }

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.real = self.object.get_real_instance()
        return super().get(request, *args, **kwargs)

    # def get_object(self):
    #     # note: we are using base_objects here to get the base model (Sample) instance
    #     obj = self.base.model.base_objects.get(pk=self.kwargs.get("pk"))
    #     self.real = obj.get_real_instance()
    #     return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["real"] = self.real
        context[self.real._meta.model_name] = self.real
        base_fields = [f.name for f in self.base.model._meta.fields]
        context["additional_fields"] = [f.name for f in self.real._meta.fields if f.name not in base_fields]
        if "sample_ptr" in context["additional_fields"]:
            context["additional_fields"].remove("sample_ptr")
        context["sidebar_fields"] = self.get_sidebar_fields(self.real.__class__)
        return context

    def get_sidebar_fields(self, klass):
        declared_fields = set(self.sidebar_exclude)

        result = {}

        # Loop through the real model's MRO
        for base in reversed(klass.__mro__):
            # Only process Django models that are subclasses of models.Model
            if hasattr(base, "_meta") and issubclass(base, Sample):
                declared_in_base = []
                # for field in base._meta.get_fields():
                for field in base._meta.local_fields:
                    # Check if field is already declared by a parent class
                    if field.name not in declared_fields:
                        # Mark this field as declared
                        declared_fields.add(field.name)
                        declared_in_base.append(field.name)

                if declared_in_base:
                    result[base._meta.verbose_name] = declared_in_base

        sample = result.pop("Sample")
        last_key = list(result.keys())[-1]

        combined_fields = sample + result[last_key]

        del result[last_key]
        result = {last_key: combined_fields, **result}

        return result

    # def get_meta_title(self, context):
    #     real_name = self.real._meta.verbose_name
    #     return f"{real_name} - {self.real}"


class SampleEditView(BaseUpdateView):
    model = Sample
    form_class = SampleForm
    related_name = "dataset"

    def get_object(self):
        # note: we are using base_objects here to get the base model (Sample) instance
        base_obj = self.model.objects.get(pk=self.kwargs.get("pk"))
        self.obj = base_obj.get_real_instance()
        return self.obj

    def get_form_class(self):
        return modelform_factory(self.obj._meta.model, form=SampleForm, fields=self.get_fields())

    def get_fields(self):
        fields = self.request.GET.get("fields", None)
        if not fields:
            return None
        fields = fields.split(",")

        return [f for f in fields if self.object._meta.get_field(f).editable]

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        """If the form is valid, redirect to the supplied URL."""
        if not self.request.htmx:
            return HttpResponseRedirect(self.get_success_url())
        else:
            fields = self.get_fields()


class SampleTable(tables.Table):
    name = tables.columns.Column(linkify=True)

    class Meta:
        model = Sample
        fields = ["name", "status", "numchild"]


class SamplePlugin(SingleTableMixin, ListPluginMixin):
    model = Sample
    title = name = _("Samples")
    icon = "sample.svg"
    template_name = "measurements/measurement_list.html"
    # template_name = "contributors/contribution_list.html"
    object_template = "samples/sample_card.html"

    table_class = SampleTable

    def get_table_data(self):
        return self.get_queryset()

    def get_queryset(self, *args, **kwargs):
        return self.base_object.samples.filter(depth=1)
