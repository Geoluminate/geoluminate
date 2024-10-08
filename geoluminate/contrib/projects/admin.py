from django.contrib import admin

from .models import Date, Description, Project


class DescriptionInline(admin.TabularInline):
    model = Description
    extra = 0
    fields = ["type", "text"]
    # max_num = len(Description.TYPE_CHOICES)


class DateInline(admin.TabularInline):
    model = Date
    extra = 0
    fields = ["type", "date"]


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    inlines = [
        DescriptionInline,
        DateInline,
    ]
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


admin.site.register(Description)
