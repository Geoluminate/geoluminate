from django.contrib import admin

from geoluminate.contrib.contributors.admin import GenericContributionInline
from geoluminate.contrib.core.admin import (
    BaseAdmin,
    DescriptionInline,
    FuzzyDatesInline,
)

from .models import Dataset


class DatasetsInline(admin.StackedInline):
    model = Dataset
    extra = 1


@admin.register(Dataset)
class DatasetAdmin(BaseAdmin):
    inlines = [DescriptionInline, FuzzyDatesInline, GenericContributionInline]
    search_fields = ("uuid", "title")
    list_display = ("title", "created", "modified")
    frontend_editable_fields = (
        "title",
        "summary",
    )
