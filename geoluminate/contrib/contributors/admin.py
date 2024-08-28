from django.contrib import admin
from django.db import models
from fluent_comments.models import FluentComment
from image_uploader_widget.widgets import ImageUploaderWidget
from polymorphic.admin import PolymorphicChildModelFilter, PolymorphicParentModelAdmin
from threadedcomments.models import ThreadedComment

# from django_select2.forms import Select2AdminMixin
from geoluminate.contrib.organizations.models import Organization
from geoluminate.contrib.users.models import User

from .models import Contributor, Identifier


class ContributionInline(admin.StackedInline):
    # model = Contribution
    extra = 1
    fields = ("profile", "roles")


class ContributorInline(admin.StackedInline):
    model = Contributor
    fields = ["profile"]
    extra = 0


class IdentifierInline(admin.TabularInline):
    model = Identifier
    field = ["scheme", "identifier"]
    extra = 0


@admin.register(Contributor)
class ContributorAdmin(PolymorphicParentModelAdmin):
    base_model = Contributor
    child_models = (Contributor, User, Organization)
    list_display = ["_name", "profile"]
    search_fields = ["name"]
    inlines = [IdentifierInline]
    list_filter = (PolymorphicChildModelFilter,)

    formfield_overrides = {
        models.ImageField: {"widget": ImageUploaderWidget},
    }

    def _name(self, obj):
        return obj.name or "-"


admin.site.register(Identifier)
admin.site.unregister(ThreadedComment)
admin.site.unregister(FluentComment)
