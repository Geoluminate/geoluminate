from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from geoluminate.views import BaseDetailView, BaseTableView

from .models import Location, Sample
from .tables import SampleTable

list_view = BaseTableView.as_view(table=SampleTable, table_view_name="sample-list")


class SampleDetail(BaseDetailView):
    model = Sample


class LocationView(BaseDetailView):
    model = Location
