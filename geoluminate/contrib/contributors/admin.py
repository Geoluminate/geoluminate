from django.contrib import admin
from django.contrib.contenttypes.admin import GenericStackedInline
from django.db.models import Count

from geoluminate.contrib.core.admin import BaseAdmin

from .models import Contribution, Contributor


class GenericContributionInline(GenericStackedInline):
    model = Contribution
    extra = 1
    fields = ("profile", "roles")


class ContributionInline(admin.StackedInline):
    model = Contribution
    extra = 1
    fields = ("profile", "roles")


class ContributorInline(admin.StackedInline):
    model = Contributor
    fields = ["about"]
    extra = 0


@admin.register(Contributor)
class ContributorAdmin(BaseAdmin):
    list_display = ["name", "about", "projects", "datasets", "samples"]
    search_fields = ["name"]
    frontend_editable_fields = ["image", "name", "about", "status"]
    # list_filter = ["type"]
    inlines = [ContributionInline]

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .annotate(
                dataset_count=Count(Contributor.get_contribution_by_type("geoluminate.Dataset")),
                project_count=Count(Contributor.get_contribution_by_type("geoluminate.Project")),
                sample_count=Count(Contributor.get_contribution_by_type("geoluminate.Sample")),
            )
        )

    def datasets(self, obj):
        return obj.dataset_count

    def projects(self, obj):
        return obj.project_count

    def samples(self, obj):
        return obj.sample_count


# c = ContributorAdmin(Contributor, admin.site)
# print(c.get_urls())


@admin.register(Contribution)
class ContributionAdmin(BaseAdmin):
    pass
