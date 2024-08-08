from django.views.generic import TemplateView

from geoluminate.plugins import PluginRegistry
from geoluminate.utils import icon

from .models import Location
from .views import LocationDetailView

location = PluginRegistry(base=LocationDetailView)


# LOCATION PLUGINS
@location.page("overview", icon=icon("overview"))
class LocationOverview(LocationDetailView, TemplateView):
    model = Location
    base_template = "location/location_detail.html"
    template_name = "geoluminate/plugins/map.html"


# @location.page("samples", icon=icon("samples"))
# class LocationSamples(LocationDetailView, BaseTableView):
#     table = SampleTable
