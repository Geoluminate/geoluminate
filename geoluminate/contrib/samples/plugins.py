from django.views.generic import TemplateView

from geoluminate.contrib.contributors.views import ContributorsPlugin
from geoluminate.plugins import PluginRegistry
from geoluminate.utils import icon, label
from geoluminate.views import BaseTableView

from .models import Location, Sample
from .tables import SampleTable
from .views import LocationView, SampleDetail

sample = PluginRegistry("samples", base=SampleDetail)
location = PluginRegistry("locations", base=LocationView)


@sample.page("overview", icon=icon("overview"))
class SampleOverview:
    model = Sample
    template_name = "geoluminate/plugins/overview.html"
    title = label("sample")["verbose_name"]


# # @sample.page("measurements", icon=icon("measurement"))
sample.register_page(ContributorsPlugin)


# LOCATION PLUGINS
@location.page("overview", icon=icon("overview"))
class LocationOverview(LocationView, TemplateView):
    model = Location
    base_template = "samples/location_detail.html"
    template_name = "geoluminate/plugins/map.html"


@location.page("samples", icon=icon("samples"))
class LocationSamples(LocationView, BaseTableView):
    table = SampleTable
