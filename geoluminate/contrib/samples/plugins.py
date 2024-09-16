from geoluminate.contrib.contributors.views import ContributorsPlugin
from geoluminate.core.plugins import Discussion, Images
from geoluminate.core.utils import label
from geoluminate.plugins import sample

from .models import Sample
from .views import SamplePlugin


@sample.page("overview", icon="overview")
class SampleOverview:
    model = Sample
    template_name = "geoluminate/plugins/overview.html"
    title = label("sample")["verbose_name"]


sample.register_page(ContributorsPlugin)
sample.register_page(SamplePlugin, title="Sub-samples")
sample.register_page(Images)
sample.register_page(Discussion)
# sample.register_page(ActivityStream)
