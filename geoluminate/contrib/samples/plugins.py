from geoluminate.contrib.contributors.views import ContributorsPlugin
from geoluminate.core.plugins import Discussion, Images, Map
from geoluminate.core.utils import icon, label
from geoluminate.plugins import PluginRegistry

from .models import Sample
from .views import SampleDetailView, SamplePlugin

sample = PluginRegistry(base=SampleDetailView)


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
