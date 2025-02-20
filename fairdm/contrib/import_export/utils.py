import io
import zipfile

from defusedxml import minidom
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.template.loader import render_to_string
from import_export.formats.base_formats import DEFAULT_FORMATS

from fairdm.registry import registry


def get_formats():
    """Returns the available formats."""
    return getattr(settings, "IMPORT_EXPORT_FORMATS", DEFAULT_FORMATS)


def get_export_formats():
    """Returns the available export formats."""
    return getattr(settings, "EXPORT_FORMATS", get_formats())


def get_import_formats():
    """Returns the available import formats."""
    formats = getattr(settings, "IMPORT_FORMATS", get_formats())
    return {f().get_title(): f for f in formats if f().can_import()}


export_choices = {f().get_title(): f().get_title() for f in get_export_formats() if f().can_export()}

import_choices = {f: f for f in get_import_formats()}

# import_file_extensions = {f().get_title(): f().get_extension() for f in get_import_formats() if f().can_import()}

# export_file_extensions = {f().get_title(): f().get_extension() for f in get_export_formats()}


def build_metadata(dataset, request):
    template_name = "publishing/datacite44.xml"
    uri = request.build_absolute_uri(dataset.get_absolute_url())
    xml = render_to_string(template_name, {"dataset": dataset, "uri": uri}, request=request)
    dom = minidom.parseString(xml)
    return dom.toprettyxml(indent="  ")


def build_export_for_datatype(dataset, queryset, fmt="csv"):
    """Create an export for a given dataset and datatype that can be included in a ZIP file."""
    model = queryset.model
    config = registry.get_model(model)
    resource = config["config"].get_resource_class()(dataset=dataset)
    # fmt = get_export_formats()[1]()
    tablib_dataset = resource.export(queryset=queryset)
    return tablib_dataset.export(fmt)


class DataPackage:
    def __init__(self, dataset, request):
        self.dataset = dataset
        self.request = request

    def build_package(self):
        buffer = io.BytesIO()
        with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
            # Add files to the ZIP
            self.add_license(zip_file)
            self.add_readme(zip_file)
            self.add_metadata(zip_file)
            self.add_samples(zip_file)
            self.add_measurements(zip_file)

        buffer.seek(0)  # Rewind the buffer for reading
        return buffer

    def add_license(self, zip_file):
        """Add the license for the dataset."""
        if self.dataset.license:
            zip_file.writestr("license.txt", self.dataset.license.text)

    def add_readme(self, zip_file):
        """Add a readme file to the ZIP."""
        zip_file.writestr("readme.txt", "This is a dynamically generated ZIP file.")

    def add_metadata(self, zip_file):
        """Add XML metadata files to the ZIP."""
        zip_file.writestr("metadata.xml", build_metadata(self.dataset, self.request))

    def add_samples(self, zip_file):
        """Add the samples to the ZIP."""

        # get a list of all sample types collected by this dataset
        sample_types = self.dataset.samples.values_list("polymorphic_ctype", flat=True)

        ctypes = ContentType.objects.filter(id__in=sample_types)

        # for each sample type, create a separate export file
        for model_ctype in ctypes:
            model = model_ctype.model_class()
            qs = model.objects.filter(dataset=self.dataset)
            export = build_export_for_datatype(self.dataset, qs)
            zip_file.writestr(f"samples/{model._meta.verbose_name_plural}.csv", export)

    def add_measurements(self, zip_file):
        """Add the measurements to the ZIP."""
        # get a list of all sample types collected by this dataset
        measurements = self.dataset.measurements.values_list("polymorphic_ctype", flat=True)

        ctypes = ContentType.objects.filter(id__in=measurements)

        # for each measurements type, create a separate export file
        for model_ctype in ctypes:
            model = model_ctype.model_class()
            qs = model.objects.filter(dataset=self.dataset)
            export = build_export_for_datatype(self.dataset, qs)
            zip_file.writestr(f"measurements/{model._meta.verbose_name_plural}.csv", export)
