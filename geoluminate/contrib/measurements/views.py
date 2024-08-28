from django.utils.translation import gettext as _

from geoluminate.contrib.core.view_mixins import PolymorphicSubclassMixin
from geoluminate.views import BaseListView

from .models import Measurement


class MeasurementTypeListView(PolymorphicSubclassMixin, BaseListView):
    title = _("Measurement Types")
    model = Measurement
    filterset_fields = ["id"]
