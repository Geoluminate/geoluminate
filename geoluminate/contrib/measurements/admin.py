from django.contrib import admin
from polymorphic.admin import PolymorphicChildModelAdmin, PolymorphicChildModelFilter, PolymorphicParentModelAdmin

from geoluminate.contrib.measurements.models import Measurement
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


@admin.register(Measurement)
class MeasurementParentAdmin(PolymorphicParentModelAdmin):
    model = Measurement
    child_models = get_subclasses(Measurement)
    list_filter = (PolymorphicChildModelFilter,)


class MeasurementAdmin(PolymorphicChildModelAdmin):
    show_in_index = True
    base_model = Measurement
    inlines = [DescriptionInline, DateInline]
