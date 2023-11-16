from django.views.generic import TemplateView, UpdateView
from formset.views import FileUploadMixin, FormViewMixin

from geoluminate.contrib.contributors.views import ContributionListView
from geoluminate.contrib.datasets.views import DatasetListView
from geoluminate.plugins import location, sample
from geoluminate.utils import icon
from geoluminate.views import BaseDetailView, BaseListView, BaseTableView

from .models import Location, Sample
from .tables import SampleTable
from .views import LocationView, SampleDetail


@sample.page("overview", icon=icon("overview"))
class SampleOverview(SampleDetail, TemplateView):
    model = Sample
    template_name = "geoluminate/plugins/overview.html"


@sample.page("measurements", icon=icon("measurement"))
@sample.page("contributors", icon=icon("contributors"))
class SampleContributorsView(SampleDetail, ContributionListView):
    def get_queryset(self, *args, **kwargs):
        # get all Contributor objects that are associated with this project
        return self.get_object().contributors.select_related("profile")


# LOCATION PLUGINS
@location.page("overview", icon=icon("overview"))
class LocationOverview(LocationView, TemplateView):
    model = Location
    base_template = "samples/location_detail.html"
    template_name = "geoluminate/plugins/map.html"


@location.page("samples", icon=icon("samples"))
class LocationSamples(LocationView, BaseTableView):
    table = SampleTable
