from django.contrib import admin
from django.utils.translation import gettext_lazy as _

# AutoNumberInput,
# ButtonGroup,
# IconGroup,
# TagTypeFormField,
from solo.admin import SingletonModelAdmin

from .forms import SiteConfigForm
from .models import Configuration


@admin.register(Configuration)
class SiteConfigurationAdmin(SingletonModelAdmin):
    form = SiteConfigForm
    fieldsets = (
        (
            _("Site"),
            {"fields": ("name",)},
        ),
        (
            _("Brand"),
            {
                "fields": (
                    "logo",
                    "icon",
                )
            },
        ),
        (
            _("Database"),
            {
                "fields": ("database",),
            },
        ),
        (
            _("Authority"),
            {
                "fields": ("authority",),
            },
        ),
        (
            _("Theme Customization"),
            {
                "fields": ("theme",),
            },
        ),
    )
