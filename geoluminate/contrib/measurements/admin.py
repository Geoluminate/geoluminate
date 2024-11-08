from django.contrib import admin
from polymorphic.admin import PolymorphicChildModelAdmin, PolymorphicChildModelFilter, PolymorphicParentModelAdmin

from geoluminate.contrib.measurements.models import Measurement
from geoluminate.core.utils import get_subclasses


@admin.register(Measurement)
class MeasurementParentAdmin(PolymorphicParentModelAdmin):
    model = Measurement
    child_models = get_subclasses(Measurement)
    list_filter = (PolymorphicChildModelFilter,)


class MeasurementAdmin(PolymorphicChildModelAdmin):
    show_in_index = True
    base_model = Measurement
