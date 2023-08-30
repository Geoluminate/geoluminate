# from django_reverse_admin import ReverseModelAdmin
from cms.admin.placeholderadmin import FrontendEditableAdminMixin
from cms.models import Page, Placeholder, Title
from django.conf import settings
from django.contrib import admin
from django.contrib.postgres.fields import ArrayField
from django.contrib.sites.models import Site
from django.db import models
from django.forms.widgets import RadioSelect
from django.utils.translation import gettext_lazy as _
from solo.admin import SingletonModelAdmin

from geoluminate.models import GlobalConfiguration

admin.site.site_title = getattr(settings, "GEOLUMINATE", {})["database"]["name"]


class CMSAdmin(admin.AdminSite):
    site_header = "Django CMS"
    site_title = "Django CMS"
    index_template = "admin/cms/index.html"
    index_title = "Content Management"


# admin.site.unregister(Page)
admin_site = CMSAdmin(name="cms_admin")
admin_site.register(Page)


class GeoluminateAdminMixin:
    def has_add_permission(self, request):
        return super().has_add_permission(request) or request.user.is_db_admin()

    def has_change_permission(self, request, obj=None):
        return super().has_add_permission(request, obj) or request.user.is_db_admin()

    def has_view_permission(self, request, obj=None):
        return super().has_add_permission(request, obj) or request.user.is_db_admin()

    def has_delete_permission(self, request, obj=None):
        return super().has_add_permission(request, obj) or request.user.is_db_admin()


class SiteInline(admin.StackedInline):
    model = Site
    can_delete = False


@admin.register(GlobalConfiguration)
class ConfigurationAdmin(FrontendEditableAdminMixin, SingletonModelAdmin):
    frontend_editable_fields = ("logo", "icon")
    fieldsets = (
        (
            _("Site"),
            {"fields": ("site", "lockdown_enabled", "custodian")},
        ),
        (
            "API",
            {"fields": ("enable_api",)},
        ),
        (
            _("Brand"),
            {
                "fields": ("logo", "icon"),
            },
        ),
        # (
        #     _("Advanced"),
        #     {
        #         "fields": ("remote_addr_exceptions", "trusted_proxies"),
        #     },
        # ),
    )

    formfield_overrides = {
        models.BooleanField: {"widget": RadioSelect},
    }


admin.site.unregister(Site)


@admin.register(Site)
class DjangoSiteAdmin(FrontendEditableAdminMixin, admin.ModelAdmin):
    frontend_editable_fields = ("name",)
