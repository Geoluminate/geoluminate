from django.contrib.gis import admin
from django.contrib.gis.db import models

from geoluminate.contrib.core.admin import DescriptionInline, FuzzyDatesInline

# from jazzmin import templatetags
from .models import Location, Sample


@admin.register(Sample)
class SampleAdmin(admin.ModelAdmin):
    # inlines = [FuzzyDatesInline]
    list_display = (
        "id",
        "type",
        "title",
        "created",
    )


@admin.register(Location)
class LocationAdmin(admin.OSMGeoAdmin):
    list_display = (
        "name",
        "latitude",
        "longitude",
        "elevation",
    )

    def get_queryset(self, request):
        return (
            super().get_queryset(request)
            # .annotate(latitude=models.functions.Y("point"), longitude=models.functions.X("point"))
        )
