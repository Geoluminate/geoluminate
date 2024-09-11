from django.utils.translation import gettext as _
from django.views.generic import TemplateView

from geoluminate.core.view_mixins import PolymorphicSubclassBaseView, PolymorphicSubclassMixin
from geoluminate.views import BaseListView

from .models import Measurement


class MeasurementTypeListView(PolymorphicSubclassMixin, BaseListView):
    """Lists all the measurement types available in the database."""

    title = _("Measurement Types")
    model = Measurement
    filterset_fields = ["id"]
    list_url = "measurement-list"
    detail_url = "measurement-type-detail"


class MeasurementTypeDetailView(TemplateView):
    """Lists all the measurement types available in the database."""

    base_model = Measurement

    def get_template_names(self):
        return ["measurements/measurement_type_detail.html"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = _("Measurement Type Detail")
        context["model"] = self.model
        context["metadata"] = self.model.get_metadata()
        return context


class MeasurementListView(PolymorphicSubclassBaseView, BaseListView):
    base_model = Measurement
