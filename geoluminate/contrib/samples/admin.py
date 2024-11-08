from django.contrib import admin
from django.db import models
from django.utils.translation import gettext as _
from django_select2.forms import Select2MultipleWidget, Select2Widget
from polymorphic.admin import PolymorphicChildModelFilter
from polymorphic_treebeard.admin import PolymorphicTreeAdmin, PolymorphicTreeChildAdmin

from .models import Sample


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
    base_model = Sample
    base_fieldsets = (
        (
            _("Basic information"),
            {
                "fields": (
                    ("name", "status"),
                    "internal_id",
                    "dataset",
                    "keywords",
                    "options",
                )
            },
        ),
        (
            _("Position"),
            {"fields": (("_position", "_ref_node_id"),)},
        ),
    )
    # show_in_index = True
    formfield_overrides = {
        models.ForeignKey: {"widget": Select2Widget},
        models.ManyToManyField: {"widget": Select2MultipleWidget},
    }
