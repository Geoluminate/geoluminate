# user/admin.py
# from allauth.socialaccount.models import Account
from typing import Any

from django.contrib import admin
from django.contrib.contenttypes.admin import GenericStackedInline

# from jazzmin import templatetags
from .models import Contribution, Contributor, Organizational, Personal


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
    list_filter = ["type"]


# @admin.register(Organizational)
# class OrganizationalContributorAdmin(admin.ModelAdmin):
#     list_display = ["type", "organization"]


# @admin.register(Personal)
# class PersonalContributorAdmin(admin.ModelAdmin):
#     list_display = ["type", "user"]


@admin.register(Contribution)
class ContributionAdmin(admin.ModelAdmin):
    pass
