from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from geoluminate.contrib.core.admin import BaseAdmin

from .models import Invitation, Manager, Membership, Organization


class ManagerInline(admin.StackedInline):
    model = Manager
    extra = 0
    verbose_name_plural = _("Manager")


class AdminInline(admin.StackedInline):
    model = Membership
    extra = 0


@admin.register(Organization)
class OrganizationAdmin(BaseAdmin):
    # inlines = [ManagerInline, AdminInline]
    pass


admin.site.register(Membership)
admin.site.register(Manager)
admin.site.register(Invitation)
