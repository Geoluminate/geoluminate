from django.contrib import admin

# import GenericTabularInline
from django.contrib.contenttypes.admin import GenericStackedInline, GenericTabularInline
from django.contrib.gis import admin

from geoluminate.contrib.contributor.admin import ContributionInline

from .models import (
    Dataset,
    Description,
    KeyDate,
    Location,
    Project,
    Sample,
)


class KeyDatesInline(GenericStackedInline):
    model = KeyDate
    extra = 1


class DescriptionInline(GenericStackedInline):
    model = Description
    extra = 1


class DatasetsInline(admin.StackedInline):
    model = Dataset
    extra = 1


@admin.register(KeyDate)
class KeyDateAdmin(admin.ModelAdmin):
    pass


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    inlines = [DescriptionInline, KeyDatesInline, ContributionInline, DatasetsInline]
    search_fields = ("uuid", "title")

    list_display = (
        "title",
        "status",
        "created",
    )


@admin.register(Dataset)
class DatasetAdmin(admin.ModelAdmin):
    inlines = [DescriptionInline, KeyDatesInline, ContributionInline]
    search_fields = ("uuid", "title")
    list_display = ("title", "created", "modified")


@admin.register(Sample)
class SampleAdmin(admin.ModelAdmin):
    inlines = [KeyDatesInline]
    list_display = (
        "id",
        "type",
        "name",
        "created",
    )


@admin.register(Location)
class LocationAdmin(admin.OSMGeoAdmin):
    list_display = (
        "name",
        "point",
        "elevation",
    )
