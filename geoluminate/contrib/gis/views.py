from django.utils.translation import gettext as _

from geoluminate.views import BaseDetailView, BaseEditView

from .forms import LocationForm
from .models import Location


class LocationDetailView(BaseDetailView):
    base_template = "location/location_detail.html"
    model = Location
    title = _("Location")
    form_class = LocationForm


class LocationEditView(BaseEditView):
    model = Location
    form_class = LocationForm
    related_name = "sample"
