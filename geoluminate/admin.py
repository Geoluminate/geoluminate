from django.contrib import admin
from solo.admin import SingletonModelAdmin
from geoluminate.models import GlobalConfiguration
from django.utils.translation import gettext_lazy as _
from django.contrib.sites.models import Site
# from django_reverse_admin import ReverseModelAdmin
from cms.admin.placeholderadmin import FrontendEditableAdminMixin
from django.contrib.sites.models import Site


class SiteInline(admin.StackedInline):
    model = Site
    can_delete = False


@admin.register(GlobalConfiguration)
class ConfigurationAdmin(FrontendEditableAdminMixin, SingletonModelAdmin):
    frontend_editable_fields = ("logo", "icon")
    fieldsets = (
        # (_("Site"), {"classes": ("placeholder form-group",), "fields": ()}),
        (_("Site"), {"fields": ('site',)}),

        (_('Custodian'), {
            'fields': ('custodian',),
        }),
        (_('Files'), {
            'fields': ('logo', 'icon'),
        }),
    )
    # inline_type = 'tabular'

    # inline_reverse = [{
    #     'field_name': 'site',
    #     'admin_class': SiteInline
    # }]


admin.site.unregister(Site)


@admin.register(Site)
class DjangoSiteAdmin(FrontendEditableAdminMixin, admin.ModelAdmin):
    frontend_editable_fields = ("name",)
