from django.core.files.base import ContentFile
from django.views.generic import UpdateView
from django_downloadview.views import VirtualDownloadView
from formset.views import FileUploadMixin, FormViewMixin
from lxml import etree

from geoluminate.contrib.contributors.views import ContributorsPlugin
from geoluminate.contrib.samples.views import SamplePlugin
from geoluminate.core import utils
from geoluminate.core.plugins import ActivityStream, Discussion, Map
from geoluminate.plugins import PluginRegistry
from geoluminate.utils import icon

from .views import DatasetDetailView

dataset = PluginRegistry(base=DatasetDetailView)


@dataset.page("overview", icon=icon("overview"))
class DatasetOverview(FileUploadMixin, FormViewMixin, UpdateView):
    template_name = "geoluminate/plugins/overview.html"


dataset.register_page(ContributorsPlugin)


dataset.register_page(SamplePlugin)


@dataset.page()
class DatasetMap(Map):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["map_source_list"].update(self.serialize_dataset_samples(self.get_object()))

        return context


# dataset.register_page(Map)
dataset.register_page(Discussion)
dataset.register_page(ActivityStream)


@dataset.action("flag", icon="fas fa-flag")
@dataset.action("download", icon="fas fa-file-zipper")
@dataset.action("metadata", icon="fas fa-file-code")
class XMLDownload(DatasetDetailView, VirtualDownloadView):
    def get_file(self):
        obj = self.get_object()

        # defining an XML parser that removes blank text so we can pretty print the output
        parser = etree.XMLParser(remove_blank_text=True)
        root = etree.fromstring(utils.generate_xml(obj), parser)  # noqa: S320

        # Prettify the XML
        prettified_xml = etree.tostring(root, pretty_print=True, encoding="utf-8").decode("utf-8")

        return ContentFile(prettified_xml, name="metadata.xml")
