from django.contrib import admin
from django.utils.translation import gettext as _
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
    list_display = ["sample_type", "name", "created"]
    exclude = ["options"]
    list_filter = (PolymorphicChildModelFilter,)

    def sample_type(self, obj):
        return obj._meta.verbose_name

    sample_type.short_description = "Type"


class SampleAdmin(PolymorphicTreeChildAdmin):
    # show_in_index = True
    base_model = Sample
    inlines = [DescriptionInline, DateInline]

    fieldsets = [
        (
            _("Basic information"),
            {
                "fields": (
                    ("name", "status"),
                    "internal_id",
                    "dataset",
                )
            },
        ),
    ]
