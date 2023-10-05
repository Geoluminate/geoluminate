from django.contrib import admin

from geoluminate.contrib.contributors.admin import ContributionInline
from geoluminate.contrib.core.admin import DescriptionInline, KeyDatesInline
from geoluminate.contrib.datasets.admin import DatasetsInline

# from jazzmin import templatetags
from .models import Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    # inlines = [DescriptionInline, KeyDatesInline, ContributionInline, DatasetsInline]
    search_fields = ("uuid", "title")

    list_display = (
        "title",
        "status",
        "created",
    )
