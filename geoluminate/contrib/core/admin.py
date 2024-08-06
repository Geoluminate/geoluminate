from django.contrib import admin
from taggit.models import Tag


class InvisibleAdmin(admin.ModelAdmin):
    def has_module_permission(self, request):
        return False


admin.site.unregister(Tag)
