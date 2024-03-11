from django.views.generic import FormView

from geoluminate.views import BaseDetailView, BaseTableView

from .models import Location, Sample
from .tables import SampleTable


class SampleList(BaseTableView):
    table = SampleTable
    table_view_name = "sample-list"


class SampleDetail(BaseDetailView):
    base_template = "samples/sample_detail.html"
    model = Sample
    my_long_str = "aascascascoinasivlabsiu hawef uhaweif aiwefu haiweuf aweuf awieufh poawef awef pawef o awef pa wef a awef awef awef "


class SampleEdit(BaseDetailView, FormView):
    base_template = "samples/sample_edit.html"
    model = Sample


class SampleCreate(BaseDetailView, FormView):
    base_template = "samples/sample_create.html"
    model = Sample


class LocationView(BaseDetailView):
    base_template = "samples/location_detail.html"
    model = Location
