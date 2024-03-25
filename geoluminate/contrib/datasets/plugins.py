from django.core.files.base import ContentFile
from django.views.generic import UpdateView
from django_downloadview.views import VirtualDownloadView
from formset.views import FileUploadMixin, FormViewMixin
from lxml import etree

from geoluminate.contrib.contributors.utils import current_user_has_role
from geoluminate.contrib.contributors.views import ContributorsPlugin
from geoluminate.contrib.core import utils
from geoluminate.contrib.core.plugins import ActivityStream, Discussion, Map
from geoluminate.contrib.samples.tables import SampleTable
from geoluminate.plugins import PluginRegistry
from geoluminate.utils import icon
from geoluminate.views import BaseTableView

from .views import DatasetDetailView

dataset = PluginRegistry("datasets", base=DatasetDetailView)


@dataset.page("overview", icon=icon("overview"))
class DatasetOverview(FileUploadMixin, FormViewMixin, UpdateView):
    template_name = "geoluminate/plugins/overview.html"

    def has_edit_permission(self):
        return current_user_has_role(self.request, self.object, "Creator")


dataset.register_page(ContributorsPlugin)


@dataset.page("samples", icon=icon("sample"))
class DatasetSamplesView(DatasetDetailView, BaseTableView):
    table = SampleTable
    template_name = "auto_datatables/base.html"


dataset.register_page(Map)
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
