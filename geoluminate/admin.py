# from django_reverse_admin import ReverseModelAdmin
from cms.admin.placeholderadmin import FrontendEditableAdminMixin
from django.contrib import admin
from django.contrib.postgres.fields import ArrayField
from django.contrib.sites.models import Site
from django.db import models
from django.forms.widgets import RadioSelect
from django.utils.translation import gettext_lazy as _
from solo.admin import SingletonModelAdmin

from geoluminate.core.forms.fields import DynamicArrayField
from geoluminate.models import GlobalConfiguration


class SiteInline(admin.StackedInline):
    model = Site
    can_delete = False


@admin.register(GlobalConfiguration)
class ConfigurationAdmin(FrontendEditableAdminMixin, SingletonModelAdmin):
    frontend_editable_fields = ("logo", "icon")
    fieldsets = (
        # (_("Site"), {"classes": ("placeholder form-group",), "fields": ()}),
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
        (
            _("Advanced"),
            {
                "fields": ("remote_addr_exceptions", "trusted_proxies"),
            },
        ),
    )

    formfield_overrides = {
        ArrayField: {
            "form_class": DynamicArrayField,
        },
        models.BooleanField: {"widget": RadioSelect},
    }


admin.site.unregister(Site)


@admin.register(Site)
class DjangoSiteAdmin(FrontendEditableAdminMixin, admin.ModelAdmin):
    frontend_editable_fields = ("name",)


# @admin.register(Choice)
# class ControlledVocabularyAdmin(admin.ModelAdmin):
#     list_display = ['type', 'code', 'name', '_description']
#     list_filter = ['type', ]
#     search_fields = ['name', ]

#     def _description(self, obj):
#         if obj.description:
#             return obj.description[:50] + '...'
#     _description.admin_order_field = 'description'
#     _description.verbose_name = _('description')
