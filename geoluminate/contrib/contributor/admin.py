# user/admin.py
# from allauth.socialaccount.models import Account
from django.contrib import admin
from django.contrib.contenttypes.admin import GenericStackedInline

# from jazzmin import templatetags
from .models import Contribution, Contributor


class ContributionInline(GenericStackedInline):
    model = Contribution
    extra = 1
    fields = ("profile", "roles")


class ContributorInline(admin.StackedInline):
    model = Contributor
    fields = ["about"]
    extra = 0


@admin.register(Contributor)
class ContributorAdmin(admin.ModelAdmin):
    list_display = ["user", "about"]
    search_fields = ["user__email", "user__first_name", "user__last_name"]


@admin.register(Contribution)
class ContributionAdmin(admin.ModelAdmin):
    pass
