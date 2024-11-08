from django.contrib import admin

from .models import Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    search_fields = ("pk", "title")
    list_display = (
        "title",
        "status",
        "created",
    )
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "image",
                    "title",
                    "status",
                    # "description",
                )
            },
        ),
        (
            "Details",
            {
                "fields": (
                    "owner",
                    "visibility",
                    "keywords",
                )
            },
        ),
    )
