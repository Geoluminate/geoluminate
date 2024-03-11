from django.contrib import admin

from geoluminate.contrib.contributors.admin import GenericContributionInline
from geoluminate.contrib.core.admin import BaseAdmin, DescriptionInline, FuzzyDatesInline
from geoluminate.contrib.datasets.admin import DatasetsInline

# from jazzmin import templatetags
from .models import Project


@admin.register(Project)
class ProjectAdmin(BaseAdmin):
    inlines = [DescriptionInline, FuzzyDatesInline, GenericContributionInline, DatasetsInline]
    search_fields = ("uuid", "title")
    frontend_editable_fields = ("title", "summary", "status", "tags")
    list_display = (
        "title",
        "status",
        "created",
    )
