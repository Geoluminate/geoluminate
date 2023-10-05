from django.contrib import admin

# import GenericTabularInline
from django.contrib.contenttypes.admin import GenericStackedInline
from django.contrib.gis import admin

from .models import Description, KeyDate


class KeyDatesInline(GenericStackedInline):
    model = KeyDate
    extra = 1


class DescriptionInline(GenericStackedInline):
    model = Description
    extra = 1


@admin.register(KeyDate)
class KeyDateAdmin(admin.ModelAdmin):
    pass
