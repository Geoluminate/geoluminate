from allauth.account.models import EmailAddress
from client_side_image_cropping import ClientsideCroppingWidget, DcsicAdminMixin
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.db import models
from django.utils.translation import gettext as _
from django.utils.translation import gettext_lazy as _
from django_select2.forms import Select2MultipleWidget
from image_uploader_widget.widgets import ImageUploaderWidget
from polymorphic.admin import PolymorphicChildModelAdmin, PolymorphicChildModelFilter, PolymorphicParentModelAdmin

from geoluminate.contrib.contributors.models import Contributor

# from django_select2.forms import Select2AdminMixin
from .models import Contributor, Identifier, Organization, Person


class AccountEmailInline(admin.TabularInline):
    model = EmailAddress
    fields = ["email", "primary", "verified"]
    extra = 0


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
    child_models = (Contributor, Person, Organization)
    list_display = ["_name", "profile"]
    search_fields = ["name"]
    inlines = [IdentifierInline]
    list_filter = (PolymorphicChildModelFilter,)

    formfield_overrides = {
        models.ImageField: {"widget": ImageUploaderWidget},
    }

    def _name(self, obj):
        return obj.name or "-"


@admin.register(Person)
class UserAdmin(BaseUserAdmin, PolymorphicChildModelAdmin, DcsicAdminMixin):
    base_model = Contributor
    show_in_index = True

    inlines = [AccountEmailInline]
    list_display = [
        "first_name",
        "last_name",
        "email",
        # "is_superuser",
        "is_staff",
        "is_active",
        "last_login",
        "date_joined",
    ]
    list_filter = ("is_staff", "is_superuser", "is_active", "groups")
    exclude = ("username",)
    formfield_overrides = {
        models.ManyToManyField: {"widget": Select2MultipleWidget},
        models.ImageField: {
            "widget": ClientsideCroppingWidget(
                width=1200,
                height=1200,
                preview_width=150,
                preview_height=150,
                # format="webp",  # "jpeg", "png", "webp
            )
        },
        # models.JSONField: {"widget": FlatJSONWidget},
    }
    # fieldsets for modifying user
    fieldsets = (
        (
            "Basic info",
            {
                "fields": (
                    "image",
                    ("first_name", "last_name"),
                    "name",
                    "email",
                    "alternative_names",
                    "links",
                    "profile",
                )
            },
        ),
        (
            _("Account"),
            {
                "fields": (
                    "password",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                )
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "groups",
                    # "user_permissions",
                )
            },
        ),
    )

    # fieldsets for creating new user
    add_fieldsets = (
        (
            None,
            {
                "fields": (
                    ("first_name", "last_name"),
                    "email",
                    "password1",
                    "password2",
                )
            },
        ),
    )

    search_fields = ("email",)
    ordering = ("last_name",)


admin.site.register(Identifier)


@admin.register(Organization)
class OrganizationAdmin(PolymorphicChildModelAdmin):
    base_model = Contributor
    show_in_index = True
    list_display = ["name"]
    search_fields = ["name"]
