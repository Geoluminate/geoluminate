from geoluminate.contrib.contributors.views import ContributorsPlugin
from geoluminate.contrib.core.plugins import Discussion, Images, Map
from geoluminate.plugins import PluginRegistry
from geoluminate.utils import icon, label

from .models import BaseSample
from .views import SampleDetailView, SamplePlugin

sample = PluginRegistry(base=SampleDetailView)


@sample.page("overview", icon=icon("overview"))
class SampleOverview:
    model = BaseSample
    template_name = "geoluminate/plugins/overview.html"
    title = label("sample")["verbose_name"]


# # @sample.page("measurements", icon=icon("measurement"))
sample.register_page(ContributorsPlugin)
sample.register_page(Map)
sample.register_page(SamplePlugin, title="Sub-samples")
sample.register_page(Images)
sample.register_page(Discussion)
# sample.register_page(ActivityStream)
