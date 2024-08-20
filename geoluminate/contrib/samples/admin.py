from django.contrib import admin
from polymorphic.admin import PolymorphicChildModelFilter
from polymorphic_treebeard.admin import PolymorphicTreeAdmin, PolymorphicTreeChildAdmin

from .models import Date, Description, Sample


class DescriptionInline(admin.TabularInline):
    model = Description
    fields = ["type", "text"]
    extra = 0
    max_num = 2


class DateInline(admin.TabularInline):
    model = Date
    extra = 0
    fields = ["type", "date"]


@admin.register(Sample)
class BaseSampleAdmin(PolymorphicTreeAdmin):
    base_model = Sample
    child_models = Sample.get_subclasses()
    list_display = ["id", "name", "created"]
    exclude = ["options"]
    list_filter = (PolymorphicChildModelFilter,)


class SampleAdmin(PolymorphicTreeChildAdmin):
    # show_in_index = True
    base_model = Sample
    inlines = [DescriptionInline, DateInline]
