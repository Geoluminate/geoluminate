from django import forms
from django.apps import apps
from django.core.files.base import ContentFile
from django.forms import modelform_factory
from django.template.loader import render_to_string
from django.utils.module_loading import import_string
from django.utils.translation import gettext as _
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import FormView
from django_downloadview import VirtualDownloadView
from meta.views import MetadataMixin

from geoluminate.core.view_mixins import HTMXMixin, TableMixin
from geoluminate.menus import DatasetMenu, ProjectMenu, SampleMenu
from geoluminate.views import BaseCRUDView, BaseListView

from .filters import DatasetFilter, ProjectFilter
from .forms import DatasetForm, ProjectForm, SampleForm
from .models import Dataset, Measurement, Project, Sample


class ProjectCRUDView(BaseCRUDView):
    model = Project
    form_class = ProjectForm
    menu = ProjectMenu
    filterset_class = ProjectFilter
    sidebar_fields = {
        None: ["name", "created", "modified"],
    }


class DatasetCRUDView(BaseCRUDView):
    model = Dataset
    form_class = DatasetForm
    menu = DatasetMenu
    filterset_class = DatasetFilter
    paginate_by = 10
    sidebar_fields = {
        None: ["name", "project", "created", "modified"],
    }

    def get_form(self, data=None, files=None, **kwargs):
        kwargs["request"] = self.request
        return super().get_form(data, files, **kwargs)


class SampleCRUDView(BaseCRUDView):
    url_base = "sample"
    form_class = SampleForm
    menu = SampleMenu
    sidebar_exclude = [
        "sample_ptr",
        "polymorphic_ctype",
        "created",
        "modified",
        "options",
        "path",
        "depth",
        "numchild",
        "image",
    ]

    @property
    def model(self):
        if sample_type := self.request.GET.get("type"):
            return apps.get_model(sample_type)
        return Sample

    def get_form_class(self):
        if hasattr(self.model.Config, "form_class"):
            return import_string(self.model.Config.form_class)

        return modelform_factory(self.model, form=SampleForm)

    def get_form(self, data=None, files=None, **kwargs):
        kwargs["request"] = self.request
        if data:
            data = data.copy()
            data["type"] = self.model._meta.label
            data["_position"] = "first-child"
            data["dataset"] = self.request.GET.get("dataset")
        return super().get_form(data, files, **kwargs)

    def form_valid(self, form):
        # form.instance.save()
        return super().form_valid(form)

    def get_sidebar_fields(self):
        klass = self.model
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

        if len(result):
            return {None: result["sample"]}
        sample = result.pop("sample")
        last_key = list(result.keys())[-1]

        combined_fields = sample + result[last_key]

        del result[last_key]
        result = {last_key: combined_fields, **result}

        return result


class SampleListView(TableMixin, BaseListView):
    title = _("Samples")
    base_model = Sample


class MeasurementListView(TableMixin, BaseListView):
    base_model = Measurement
    title = _("Samples")


class SamplesDownloadView(VirtualDownloadView):
    def get_file(self):
        """Return :class:`django.core.files.base.ContentFile` object."""
        return ContentFile(b"Hello world!\n", name="hello-world.txt")


class MetadataDownloadView(SingleObjectMixin, VirtualDownloadView):
    model = Dataset
    template_name = "publishing/gfz_schema.xml"

    def get_file(self):
        dataset = self.get_object()
        content = render_to_string(self.template_name, {"dataset": dataset})
        return ContentFile(content, name=f"{dataset}.xml")


class UploadForm(forms.Form):
    docfile = forms.FileField(label="Select a file")


class DatasetUpload(HTMXMixin, MetadataMixin, FormView):
    title = _("Upload")
    template_name = "geoluminate/import.html"
    template_name = "geoluminate/object_form.html"
    form_class = UploadForm
    extra_context = {"title": _("Upload")}

    def process_import(self, dataset, import_file):
        # importer = HeatFlowParentImporter(import_file, dataset)
        # errors = importer.process_import()
        # dataset = Dataset.objects.get(pk=pk)
        # import_file = self.request.FILES["docfile"]
        # importer = HeatFlowParentImporter(import_file, dataset)
        # errors = importer.process_import()
        # if errors:
        # context["errors"] = errors
        # else:
        # message user
        # self.message_user(request, "Import successful")
        # return redirect(admin_urlname(context["opts"], "changelist"))
        return {}

    def form_valid(self, form):
        result = self.process_import(self.dataset, form.cleaned_data["docfile"])
        return super().form_valid(form)
