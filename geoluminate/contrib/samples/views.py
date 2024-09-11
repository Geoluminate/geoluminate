from django.utils.translation import gettext as _
from django.views.generic import TemplateView

from geoluminate.core.view_mixins import ListPluginMixin, PolymorphicSubclassBaseView, PolymorphicSubclassMixin
from geoluminate.utils import icon
from geoluminate.views import BaseDetailView, BaseEditView, BaseListView

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

        return result

    def get_meta_title(self, context):
        real_name = self.real._meta.verbose_name
        return f"{real_name} - {self.real}"


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
