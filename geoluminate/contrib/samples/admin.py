from django.contrib.gis import admin

from geoluminate.contrib.core.admin import DescriptionInline, KeyDatesInline

# from jazzmin import templatetags
from .models import Location, Sample


@admin.register(Sample)
class SampleAdmin(admin.ModelAdmin):
    # inlines = [KeyDatesInline]
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
