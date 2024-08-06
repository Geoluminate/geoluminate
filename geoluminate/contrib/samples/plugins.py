from django.views.generic import TemplateView

from geoluminate.contrib.contributors.views import ContributorsPlugin
from geoluminate.contrib.core.plugins import Discussion, Images, Map
from geoluminate.plugins import PluginRegistry
from geoluminate.utils import icon, label
from geoluminate.views import BaseTableView

from .models import Location, Sample
from .tables import SampleTable
from .views import LocationDetailView, SampleDetailView, SamplePlugin

sample = PluginRegistry(base=SampleDetailView)
location = PluginRegistry(base=LocationDetailView)


@sample.page("overview", icon=icon("overview"))
class SampleOverview:
    model = Sample
    template_name = "geoluminate/plugins/overview.html"
    title = label("sample")["verbose_name"]


# # @sample.page("measurements", icon=icon("measurement"))
sample.register_page(ContributorsPlugin)
sample.register_page(Map)
sample.register_page(SamplePlugin, title="Sub-samples")
sample.register_page(Images)
sample.register_page(Discussion)
# sample.register_page(ActivityStream)


# LOCATION PLUGINS
@location.page("overview", icon=icon("overview"))
class LocationOverview(LocationDetailView, TemplateView):
    model = Location
    base_template = "samples/location_detail.html"
    template_name = "geoluminate/plugins/map.html"


@location.page("samples", icon=icon("samples"))
class LocationSamples(LocationDetailView, BaseTableView):
    table = SampleTable
