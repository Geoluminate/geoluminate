from django.contrib.gis import admin
from polymorphic.admin import PolymorphicChildModelAdmin, PolymorphicChildModelFilter, PolymorphicParentModelAdmin

from geoluminate.contrib.measurements.models import BaseMeasurement
from geoluminate.utils import get_subclasses

from .models import Date, Description


class DescriptionInline(admin.TabularInline):
    model = Description
    fields = ["type", "text"]
    extra = 0
    max_num = 2


class DateInline(admin.TabularInline):
    model = Date
    extra = 0
    fields = ["type", "date"]


@admin.register(BaseMeasurement)
class MeasurementParentAdmin(PolymorphicParentModelAdmin):
    # class MeasurementParentAdmin(admin.ModelAdmin):
    model = BaseMeasurement
    child_models = get_subclasses(BaseMeasurement, include_self=False)
    list_filter = (PolymorphicChildModelFilter,)


class MeasurementAdmin(PolymorphicChildModelAdmin):
    base_model = BaseMeasurement
    inlines = [DescriptionInline, DateInline]
