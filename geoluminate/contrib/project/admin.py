from django.contrib import admin

from .models import Dataset, Project, Sample


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    pass


@admin.register(Dataset)
class DatasetAdmin(admin.ModelAdmin):
    list_display = ("id",)


@admin.register(Sample)
class SampleAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "type",
        "name",
        "created",
    )
