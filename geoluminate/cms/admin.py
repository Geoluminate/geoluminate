from django.contrib import admin
from cms.extensions import PageExtensionAdmin
from .models import Icon
from django.utils.html import mark_safe


@admin.register(Icon)
class IconExtensionAdmin(PageExtensionAdmin):
    list_display = ['_icon', 'css_class']

    class Media:
        js = (
            'https://kit.fontawesome.com/a08181010c.js',
        )

    def _icon(self, obj):
        return mark_safe(f"<i class='{obj.icon}'></i>")
    _icon.admin_display_name = 'Icon'

    def css_class(self, obj):
        return obj.icon
