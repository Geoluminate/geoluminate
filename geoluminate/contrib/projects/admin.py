from django.contrib import admin

from geoluminate.contrib.core.admin import InvisibleAdmin

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
    frontend_editable_fields = (
        "title",
        "status",
    )
    list_display = (
        "title",
        "status",
        "created",
    )


admin.site.register(Description, InvisibleAdmin)
