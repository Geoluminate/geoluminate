from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from polymorphic.admin import PolymorphicChildModelAdmin

from geoluminate.contrib.contributors.models import Contributor

from .models import Invitation, Manager, Membership, Organization


class ManagerInline(admin.StackedInline):
    model = Manager
    extra = 0
    verbose_name_plural = _("Manager")


class AdminInline(admin.StackedInline):
    model = Membership
    extra = 0


@admin.register(Organization)
class OrganizationAdmin(PolymorphicChildModelAdmin):
    base_model = Contributor
    show_in_index = True
    inlines = [ManagerInline, AdminInline]
    list_display = ["name"]
    search_fields = ["name"]


admin.site.register(Membership)
admin.site.register(Manager)
admin.site.register(Invitation)
