from django.core.files.base import ContentFile
from django.views.generic import UpdateView
from django_downloadview.views import VirtualDownloadView
from lxml import etree

from geoluminate.contrib.contributors.views import ContributorsPlugin
from geoluminate.contrib.measurements.views import MeasurementPlugin
from geoluminate.contrib.samples.views import SamplePlugin
from geoluminate.core import utils
from geoluminate.core.plugins import ActivityStream, Discussion
from geoluminate.plugins import dataset

from .views import DatasetDetailView


@dataset.page("overview", icon="overview")
class DatasetOverview(UpdateView):
    template_name = "geoluminate/plugins/overview.html"


dataset.register_page(ContributorsPlugin)
dataset.register_page(SamplePlugin)
dataset.register_page(MeasurementPlugin)
dataset.register_page(Discussion)
dataset.register_page(ActivityStream)


# @dataset.action("flag", icon="fas fa-flag")
# @dataset.action("download", icon="fas fa-file-zipper")
# @dataset.action("metadata", icon="fas fa-file-code")
class XMLDownload(DatasetDetailView, VirtualDownloadView):
    def get_file(self):
        obj = self.get_object()

        # defining an XML parser that removes blank text so we can pretty print the output
        parser = etree.XMLParser(remove_blank_text=True)
        root = etree.fromstring(utils.generate_xml(obj), parser)  # noqa: S320

        # Prettify the XML
        prettified_xml = etree.tostring(root, pretty_print=True, encoding="utf-8").decode("utf-8")

        return ContentFile(prettified_xml, name="metadata.xml")
