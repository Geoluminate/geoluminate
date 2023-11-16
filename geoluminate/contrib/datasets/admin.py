from django.contrib import admin

from geoluminate.contrib.contributors.admin import GenericContributionInline
from geoluminate.contrib.core.admin import DescriptionInline, FuzzyDatesInline

from .models import Dataset


class DatasetsInline(admin.StackedInline):
    model = Dataset
    extra = 1


@admin.register(Dataset)
class DatasetAdmin(admin.ModelAdmin):
    inlines = [DescriptionInline, FuzzyDatesInline, GenericContributionInline]
    search_fields = ("uuid", "title")
    list_display = ("title", "created", "modified")
