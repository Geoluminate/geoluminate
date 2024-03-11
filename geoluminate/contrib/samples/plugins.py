from django.views.generic import TemplateView

from geoluminate.contrib.contributors.views import ContributorsPlugin
from geoluminate.plugins import PluginRegistry
from geoluminate.utils import icon
from geoluminate.views import BaseTableView

from .models import Location, Sample
from .tables import SampleTable
from .views import LocationView, SampleDetail

sample = PluginRegistry("samples", base=SampleDetail)
location = PluginRegistry("locations", base=LocationView)


@sample.page("overview", icon=icon("overview"))
class SampleOverview(SampleDetail, TemplateView):
    model = Sample
    template_name = "geoluminate/plugins/overview.html"


# # @sample.page("measurements", icon=icon("measurement"))
@sample.page("contributors", icon=icon("contributors"))
class SampleContributors(SampleDetail, ContributorsPlugin):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).select_related("profile")


# LOCATION PLUGINS
@location.page("overview", icon=icon("overview"))
class LocationOverview(LocationView, TemplateView):
    model = Location
    base_template = "samples/location_detail.html"
    template_name = "geoluminate/plugins/map.html"


@location.page("samples", icon=icon("samples"))
class LocationSamples(LocationView, BaseTableView):
    table = SampleTable
