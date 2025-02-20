from io import StringIO

from django import forms
from django.contrib import messages
from django.core.files.base import ContentFile
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.utils.translation import gettext as _
from django.views.decorators.http import require_POST
from django.views.generic.detail import BaseDetailView, SingleObjectMixin
from django.views.generic.edit import FormView
from django_downloadview import VirtualDownloadView
from meta.views import MetadataMixin

from fairdm.contrib.import_export.utils import build_metadata
from fairdm.core.models import Dataset
from fairdm.registry import registry
from fairdm.utils.view_mixins import HTMXMixin

from .forms import ExportForm, ImportForm
from .utils import DataPackage, get_export_formats, get_import_formats


class BaseImportExportView(BaseDetailView, FormView):
    """
    A base view for importing and exporting data with django-import-export.
    Handles common functionality like file format detection and resource initialization.
    """

    from_encoding = "utf-8-sig"
    model = Dataset
    form_class = None
    success_url = None
    template_name = "import_export/import.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context["export_formats"] = self.export_formats
        context["import_formats"] = self.import_formats
        context["data_type"] = self.get_resource_model()._meta.verbose_name_plural
        return context

    @property
    def export_formats(self):
        return {fmat().get_title(): fmat for fmat in get_export_formats()}

    @property
    def import_formats(self):
        return get_import_formats()

    def dispatch(self, request, *args, **kwargs):
        self.resource_model = self.get_resource_model()
        return super().dispatch(request, *args, **kwargs)

    def get_resource(self):
        config = registry.get_model(self.resource_model)
        return config["config"].get_resource_class()(dataset=self.get_object())

    def get_resource_model(self):
        """
        Retrieves the model class based on the 'type' query parameter.

        If no 'type' parameter is provided, the method defaults to the first registered model
        in the registry.

        Returns:
            django.db.models.Model: The Django model class corresponding to the requested type.

        Raises:
            ValueError: If the provided 'type' does not match any registered models.
        """
        self.dtype = self.request.GET.get("type")

        if not self.dtype:
            # Default to the first registered model if no type is provided
            if not registry.all:
                raise ValueError("No models are registered in the FairDMRegistry.")
            self.meta = registry.samples[0]
            self.dtype = f"{self.meta['app_label']}.{self.meta['model']}"  # Ensures dtype is still assigned
        else:
            # Retrieve the model metadata from the registry
            result = registry.get(*self.dtype.split("."))
            if not result:
                raise ValueError(f"This data type is not supported: {self.dtype}")
            self.meta = result[0]

        return self.meta["class"]

    def get_resource_qs(self):
        return self.resource_model.objects.filter(dataset=self.get_object())

    def get_dataset_format(self, file):
        extension = file.name.split(".")[-1].lower()
        fmt = self.import_formats.get(extension)
        if fmt is None:
            raise ValueError(f"Unsupported file format: {extension}")
        return fmt(encoding=self.from_encoding)

    def form_invalid(self, form):
        # Override to handle invalid form submission
        return render(self.request, self.template_name, {"form": form})


class DataImportView(MetadataMixin, BaseImportExportView):
    form_class = ImportForm

    def form_valid(self, form):
        file = form.cleaned_data["file"]
        result = self.handle_import(file)

        if (result and result.has_errors()) or result.has_validation_errors():
            messages.error(self.request, "There were errors in the import.")
            raise ValueError(result.errors)
        else:
            messages.success(self.request, "Data imported successfully.")
        # raise ValueError("Data imported successfully.")
        return super().form_valid(form)

    # @method_decorator(require_POST)
    def handle_import(self, file):
        # Process and import the data
        resource = self.get_resource()
        input_format = self.get_dataset_format(file)
        if not input_format:
            return None

        encoding = None if input_format.is_binary() else self.from_encoding
        # Open the file in text mode and read the content
        file_content = file.read()  # Decode bytes to string

        dataset = input_format.create_dataset(file_content)
        return resource.import_data(dataset, dry_run=False)

    def get_success_url(self):
        return self.get_object().get_absolute_url()

    def get_meta_title(self, context):
        return _("Import") + " " + self.get_resource_model()._meta.verbose_name_plural


@method_decorator(require_POST, name="dispatch")
class DataExportView(VirtualDownloadView, BaseImportExportView):
    form_class = ExportForm

    def get_file(self):
        if self.request.POST.get("template"):
            qs = self.resource_model.objects.none()
        else:
            qs = self.get_resource_qs()

        tablib_dataset = self.get_resource().export(queryset=qs)
        return ContentFile(
            content=tablib_dataset.export(self.format),
            name=self.get_basename(),
        )

    def post(self, request, *args, **kwargs):
        """Handle GET requests: stream a file."""
        form = self.form_class(request.POST)
        if form.is_valid():
            self.format = form.cleaned_data["format"]
            self.format_class = self.get_format()
            return self.render_to_response(content_type=self.format_class.get_content_type())

        raise ValueError(f"Unsupported export format {self.request.GET.get('format')}.")

    def get_basename(self):
        return f"{self.resource_model._meta.verbose_name_plural}.{self.format_class.get_extension()}"

    def get_format(self):
        return self.export_formats[self.format]()


class DatasetPackageDownloadView(SingleObjectMixin, VirtualDownloadView):
    model = Dataset

    def get_file(self):
        """Return :class:`django.core.files.base.ContentFile` object."""
        return DataPackage(self.get_object(), self.request).build_package()

    def get_basename(self):
        return f"{self.get_object()}.zip"

    def get_content_type(self, file):
        """Define the MIME type for the ZIP file."""
        return "application/zip"


class MetadataDownloadView(SingleObjectMixin, VirtualDownloadView):
    model = Dataset
    template_name = "publishing/datacite44.xml"

    def get_file(self):
        return StringIO(build_metadata(self.get_object(), self.request))

    def get_basename(self):
        return f"{self.get_object()}.xml"


class UploadForm(forms.Form):
    docfile = forms.FileField(label="Select a file")


class DatasetUpload(HTMXMixin, MetadataMixin, FormView):
    title = _("Upload")
    template_name = "fairdm/import.html"
    template_name = "fairdm/object_form.html"
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


# 'Traceback (most recent call last):\n  File "c:\\Users\\jennings\\AppData\\Local\\pypoetry\\Cache\\virtualenvs\\global-heat-flow-database-GuOryC2t-py3.11\\Lib\\site-packages\\import_export\\resources.py", line 748, in import_row\n    self.import_instance(instance, row, **kwargs)\n  File "c:\\Users\\jennings\\AppData\\Local\\pypoetry\\Cache\\virtualenvs\\global-heat-flow-database-GuOryC2t-py3.11\\Lib\\site-packages\\import_export\\resources.py", line 480, in import_instance\n    self.import_field(field, instance, row, **kwargs)\n  File "c:\\Users\\jennings\\AppData\\Local\\pypoetry\\Cache\\virtualenvs\\global-heat-flow-database-GuOryC2t-py3.11\\Lib\\site-packages\\import_export\\resources.py", line 432, in import_field\n    field.save(instance, row, is_m2m, **kwargs)\n  File "c:\\Users\\jennings\\AppData\\Local\\pypoetry\\Cache\\virtualenvs\\global-heat-flow-database-GuOryC2t-py3.11\\Lib\\site-packages\\import_export\\fields.py", line 136, in save\n    setattr(instance, attrs[-1], cleaned)\nAttributeError: \'NoneType\' object has no attribute \'sample\'\n'
