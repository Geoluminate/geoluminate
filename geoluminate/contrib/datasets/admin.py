from django.contrib import admin

from geoluminate.contrib.contributors.admin import ContributionInline
from geoluminate.contrib.core.admin import DescriptionInline, KeyDatesInline

# from jazzmin import templatetags
from .models import Dataset, Review


class DatasetsInline(admin.StackedInline):
    model = Dataset
    extra = 1


@admin.register(Dataset)
class DatasetAdmin(admin.ModelAdmin):
    # inlines = [DescriptionInline, KeyDatesInline, ContributionInline]
    search_fields = ("uuid", "title")
    list_display = ("title", "created", "modified")


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    pass
