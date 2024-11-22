from django.contrib import admin
from django.db import models
from django.utils.translation import gettext as _
from django_select2.forms import Select2MultipleWidget, Select2Widget
from polymorphic.admin import PolymorphicChildModelAdmin, PolymorphicChildModelFilter, PolymorphicParentModelAdmin
from polymorphic_treebeard.admin import PolymorphicTreeAdmin, PolymorphicTreeChildAdmin

from geoluminate.contrib.core.models import Measurement
from geoluminate.core.utils import get_subclasses

from .models import Dataset, Project, Sample


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    search_fields = ("pk", "name")
    list_display = (
        "name",
        "status",
        "created",
    )
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "image",
                    "name",
                    "status",
                    # "description",
                )
            },
        ),
        (
            "Details",
            {
                "fields": (
                    "owner",
                    "visibility",
                    "keywords",
                )
            },
        ),
    )


@admin.register(Dataset)
class DatasetAdmin(admin.ModelAdmin):
    # inlines = [DescriptionInline, DateInline, IdentifierInline]
    search_fields = ("pk", "name")
    list_display = ("name", "created", "modified")
    fieldsets = ((None, {"fields": ("name", "project", "image", "reference", "visibility")}),)
    formfield_overrides = {
        models.ManyToManyField: {"widget": Select2MultipleWidget},
        models.ForeignKey: {"widget": Select2Widget},
        models.OneToOneField: {"widget": Select2Widget},
    }


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


@admin.register(Measurement)
class MeasurementParentAdmin(PolymorphicParentModelAdmin):
    model = Measurement
    child_models = get_subclasses(Measurement)
    list_filter = (PolymorphicChildModelFilter,)


class MeasurementAdmin(PolymorphicChildModelAdmin):
    show_in_index = True
    base_model = Measurement
