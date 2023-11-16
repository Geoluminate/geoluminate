from django.contrib import admin

from geoluminate.contrib.contributors.admin import GenericContributionInline
from geoluminate.contrib.core.admin import DescriptionInline, FuzzyDatesInline
from geoluminate.contrib.datasets.admin import DatasetsInline

# from jazzmin import templatetags
from .models import Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    inlines = [DescriptionInline, FuzzyDatesInline, GenericContributionInline, DatasetsInline]
    search_fields = ("uuid", "title")

    list_display = (
        "title",
        "status",
        "created",
    )
