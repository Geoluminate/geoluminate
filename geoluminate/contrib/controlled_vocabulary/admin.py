# user/admin.py

from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from django.utils.safestring import mark_safe
from django.utils.translation import gettext as _
from modeltranslation.admin import TranslationAdmin
from treebeard.admin import TreeAdmin
from treebeard.forms import movenodeform_factory

from .models import ControlledVocabulary


class PassThroughFilter(SimpleListFilter):
    title = ""
    parameter_name = "vocabulary"
    template = "admin/hidden_filter.html"

    def lookups(self, request, model_admin):
        return ((request.GET.get(self.parameter_name), ""),)

    def queryset(self, request, queryset):
        if self.value():
            return queryset.get(label=self.value()).get_descendants()


@admin.register(ControlledVocabulary)
class ControlledVocabularyAdmin(TreeAdmin, TranslationAdmin):
    form = movenodeform_factory(ControlledVocabulary)
    group_fieldsets = True
    list_display = ["label", "name", "description", "entry_count", "entries"]
    list_filter = [PassThroughFilter, "name"]
    fieldsets = (
        (
            "General",
            {
                "fields": (
                    ("_position", "_ref_node_id"),
                    "label",
                )
            },
        ),
        (
            "Name",
            {"fields": ["name"]},
        ),
        (
            "Description",
            {"fields": ["description"]},
        ),
    )

    def changelist_view(self, request, extra_context=None):
        if not request.GET.get("vocabulary"):
            self.change_list_template = "admin/change_list.html"
        return super().changelist_view(request, extra_context)

    def get_queryset(self, request):
        if request.GET.get("vocabulary"):
            return super().get_queryset(request)
        return ControlledVocabulary.get_root_nodes()

    def entry_count(self, obj):
        return obj.get_descendant_count()

    entry_count.short_description = _("Entry Count")  # type: ignore[attr-defined]

    def entries(self, obj):
        label = _("View Entries")
        return mark_safe(f"<a href='?vocabulary={obj.label}' class='btn btn-primary'>{label}</a>")  # noqa: S308

    entries.short_description = _("Entries")  # type: ignore[attr-defined]
