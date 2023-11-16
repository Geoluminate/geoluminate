from django.core.files.base import ContentFile
from django.utils.text import slugify
from django.utils.translation import gettext as _
from django.views.generic import DetailView, TemplateView, UpdateView
from django_downloadview.views import VirtualDownloadView
from formset.views import FileUploadMixin, FormViewMixin
from lxml import etree

from geoluminate.contrib.contributors.views import ContributionListView
from geoluminate.contrib.core import utils
from geoluminate.plugins import dataset
from geoluminate.utils import icon

from .filters import DatasetFilter
from .forms import DatasetForm
from .models import Dataset
from .views import DatasetDetailView


# @dataset.page("activity", icon=icon("activity"))
@dataset.page("measurements", icon=icon("measurement"))
@dataset.page("samples", icon=icon("sample"))
# @dataset.page("visualize", icon="fas fa-chart-line")
# @dataset.page("timeline", icon=icon("timeline"))
@dataset.page("overview", icon="fas fa-book-open")
class DatasetOverview(DatasetDetailView, FileUploadMixin, FormViewMixin, UpdateView):
    model = Dataset
    template_name = "geoluminate/plugins/overview.html"

    def has_edit_permission(self):
        """TODO: Add permissions."""
        # return self.request.user.is_superuser
        return self.get_object().has_role(self.request.user, "Creator")
        return super().has_edit_permission()


@dataset.page("contributors", icon=icon("contributors"))
class DatasetContributorsView(DatasetDetailView, ContributionListView):
    def get_queryset(self, *args, **kwargs):
        return self.get_object().contributors.select_related("profile")

    # def get_queryset(self, *args, **kwargs):
    #     return self.get_object().contributors.select_related("profile")


@dataset.action("flag", icon="fas fa-flag")
@dataset.action("download", icon="fas fa-file-zipper")
@dataset.action("metadata", icon="fas fa-file-code")
class XMLDownload(DatasetDetailView, VirtualDownloadView):
    def get_file(self):
        obj = self.get_object()

        # defining an XML parser that removes blank text so we can pretty print the output
        parser = etree.XMLParser(remove_blank_text=True)
        root = etree.fromstring(utils.generate_xml(obj), parser)

        # Prettify the XML
        prettified_xml = etree.tostring(root, pretty_print=True, encoding="utf-8").decode("utf-8")

        return ContentFile(prettified_xml, name=f"metadata.xml")
