from django.contrib import admin

# import GenericTabularInline
from django.contrib.contenttypes.admin import GenericStackedInline, GenericTabularInline

from .models import Contributor, Dataset, Description, KeyDate, Project, Sample


class KeyDatesInline(GenericStackedInline):
    model = KeyDate
    extra = 1


class DescriptionInline(GenericStackedInline):
    model = Description
    extra = 1


class ContributorInline(GenericStackedInline):
    model = Contributor
    extra = 1
    fields = ("profile", "roles")


class DatasetsInline(admin.StackedInline):
    model = Dataset
    extra = 1


@admin.register(KeyDate)
class KeyDateAdmin(admin.ModelAdmin):
    pass


@admin.register(Contributor)
class ContributionTypeAdmin(admin.ModelAdmin):
    pass


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    inlines = [DescriptionInline, KeyDatesInline, ContributorInline, DatasetsInline]
    list_display = (
        "id",
        "title",
        "status",
        "created",
    )


@admin.register(Dataset)
class DatasetAdmin(admin.ModelAdmin):
    inlines = [DescriptionInline, KeyDatesInline, ContributorInline]
    list_display = ("id", "title", "created", "modified")


@admin.register(Sample)
class SampleAdmin(admin.ModelAdmin):
    inlines = [KeyDatesInline]
    list_display = (
        "id",
        "type",
        "title",
        "created",
    )
