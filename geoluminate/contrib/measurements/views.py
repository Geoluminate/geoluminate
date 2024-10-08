from django.utils.translation import gettext as _
from django.views.generic import TemplateView
from django_tables2 import SingleTableMixin, tables

from geoluminate.core.view_mixins import ListPluginMixin, PolymorphicSubclassBaseView, PolymorphicSubclassMixin
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


class MeasurementTable(tables.Table):
    sample = tables.columns.Column(linkify=True)

    corr_HP_flag = tables.columns.BooleanColumn()

    class Meta:
        model = Measurement
        fields = [
            "sample",
            "q",
            "q_uncertainty",
            "corr_HP_flag",
        ]

    # def render_sample(self, record):
    #     return record.sample.get_type()["verbose_name"]


class MeasurementPlugin(SingleTableMixin, ListPluginMixin):
    title = name = _("Measurements")
    icon = "measurement.svg"
    template_name = "measurements/measurement_list.html"
    object_template = "measurements/measurement/card.html"
    model = Measurement
    table_class = MeasurementTable

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["measurement_poly_choices"] = Measurement.get_polymorphic_choices()
        return context

    def get_table_data(self):
        return self.get_queryset()

    def get_queryset(self, *args, **kwargs):
        measurement_type = self.request.GET.get("measurement_type")
        measurement_type = "HeatFlowSite"
        from django.apps import apps

        mtype = apps.get_model("heat_flow.ParentHeatFlow")
        return mtype.objects.filter(sample__dataset=self.get_object()).select_related("sample__dataset")
