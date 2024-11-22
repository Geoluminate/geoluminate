from django.utils.translation import gettext as _

from geoluminate.core.view_mixins import PolymorphicSubclassBaseView
from geoluminate.views import BaseListView

from .models import Measurement, Sample


class SampleTypeListView(PolymorphicSubclassMixin, BaseListView):
    title = _("Sample Types")
    template_name = "geoluminate/base/polymorphic_subclass_list.html"
    model = Sample
    filterset_fields = ["status"]
    list_url = "sample-list"
    detail_url = "sample-type-detail"

    def get_template_names(self, template_names=None):
        names = super().get_template_names(template_names)
        return names


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


class MeasurementTypeListView(PolymorphicSubclassMixin, BaseListView):
    """Lists all the measurement types available in the database."""

    title = _("Measurement Types")
    model = Measurement
    filterset_fields = ["id"]
    list_url = "measurement-list"
    detail_url = "measurement-type-detail"


class MeasurementTypeDetailView(TemplateView):
    """Lists all the measurement types available in the database."""

    base_model = Measurement

    def get_template_names(self):
        return ["measurements/measurement_type_detail.html"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = _("Measurement Type Detail")
        context["model"] = self.model
        context["metadata"] = self.model.get_metadata()
        return context


class SampleDetailView(BaseDetailView):
    base_template = "samples/sample_detail.html"
    model = Sample
    title = _("Sample")

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
