from django.contrib import admin
from django.db import models
from django_select2.forms import Select2MultipleWidget, Select2Widget

from .models import Dataset


@admin.register(Dataset)
class DatasetAdmin(admin.ModelAdmin):
    # inlines = [DescriptionInline, DateInline, IdentifierInline]
    search_fields = ("pk", "title")
    list_display = ("title", "created", "modified")
    fieldsets = ((None, {"fields": ("title", "project", "image", "reference", "visibility")}),)
    formfield_overrides = {
        models.ManyToManyField: {"widget": Select2MultipleWidget},
        models.ForeignKey: {"widget": Select2Widget},
        models.OneToOneField: {"widget": Select2Widget},
    }
