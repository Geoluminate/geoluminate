from cms.admin.placeholderadmin import FrontendEditableAdminMixin
from django.contrib import admin

# import GenericTabularInline
from django.contrib.contenttypes.admin import GenericStackedInline

from .models import Description, FuzzyDate


class BaseAdmin(FrontendEditableAdminMixin, admin.ModelAdmin):
    pass


class FuzzyDatesInline(GenericStackedInline):
    model = FuzzyDate
    extra = 1


class DescriptionInline(GenericStackedInline):
    model = Description
    extra = 1


@admin.register(FuzzyDate)
class FuzzyDateAdmin(admin.ModelAdmin):
    pass
