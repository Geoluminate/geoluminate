from django.contrib import admin

from .models import Contribution, Dataset, Date, Description, Identifier


class DescriptionInline(admin.TabularInline):
    model = Description
    extra = 0
    fields = ["type", "text"]


class DateInline(admin.TabularInline):
    model = Date
    extra = 0
    fields = ["type", "date"]


class IdentifierInline(admin.TabularInline):
    model = Identifier
    field = ["scheme", "identifier"]
    extra = 0


class ContributionInline(admin.TabularInline):
    model = Contribution
    extra = 0
    fields = ["contributor", "roles"]


@admin.register(Dataset)
class DatasetAdmin(admin.ModelAdmin):
    # inlines = [DescriptionInline, DateInline, IdentifierInline]
    inlines = [ContributionInline, DescriptionInline]
    search_fields = ("pk", "title")
    list_display = ("title", "created", "modified")
    frontend_editable_fields = ("title",)
    fields = ("title", "project", "image", "reference", "visibility")


admin.site.register(Contribution)
admin.site.register(Description)
admin.site.register(Date)
admin.site.register(Identifier)
