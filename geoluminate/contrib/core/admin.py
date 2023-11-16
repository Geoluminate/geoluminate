from django.contrib import admin

# import GenericTabularInline
from django.contrib.contenttypes.admin import GenericStackedInline
from django.contrib.gis import admin

from .models import Description, FuzzyDate


class FuzzyDatesInline(GenericStackedInline):
    model = FuzzyDate
    extra = 1


class DescriptionInline(GenericStackedInline):
    model = Description
    extra = 1


@admin.register(FuzzyDate)
class FuzzyDateAdmin(admin.ModelAdmin):
    pass
