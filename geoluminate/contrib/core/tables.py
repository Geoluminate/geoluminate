import django_tables2 as tables
from django.utils.translation import gettext_lazy as _
from easy_icons import icon

from .models import Measurement, Sample


class SampleTable(tables.Table):
    id = tables.Column(verbose_name="UUID", visible=False)
    name = tables.Column(verbose_name=_("Sample name"), linkify=True)
    has_children = tables.BooleanColumn(verbose_name=_("Has children"), accessor="numchild")
    has_parent = tables.BooleanColumn(verbose_name=_("Has parent"), accessor="depth")
    dataset = tables.Column(linkify=True)
    # dataset_link = tables.Column(accessor="dataset", linkify=True, visible=False)

    class Meta:
        model = Sample
        fields = ["id", "name", "path", "status", "has_children", "has_parent"]

    def render_has_parent(self, value, record):
        return "✔" if value > 1 else "✘"

    def value_has_parent(self, value):
        return value > 1

    def render_dataset(self, value):
        return icon("dataset")

    def value_dataset(self, value):
        return value.pk

    # def value_dataset_link(self, value):
    #     return f'=HYPERLINK("{value.get_absolute_url()}", "📁 View online")'


class MeasurementTable(tables.Table):
    id = tables.Column(verbose_name="ID", linkify=True)
    sample = tables.Column(linkify=True)

    class Meta:
        model = Measurement
        fields = ["id", "sample"]
