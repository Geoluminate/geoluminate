from allauth.account.models import EmailAddress
from client_side_image_cropping import ClientsideCroppingWidget, DcsicAdminMixin
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.db import models
from django.utils.translation import gettext as _
from django_select2.forms import Select2MultipleWidget
from polymorphic.admin import PolymorphicChildModelAdmin

from geoluminate.contrib.contributors.admin import IdentifierInline
from geoluminate.contrib.contributors.models import Contributor
from geoluminate.contrib.users.models import User


class AccountEmailInline(admin.TabularInline):
    model = EmailAddress
    fields = ["email", "primary", "verified"]
    extra = 0


@admin.register(User)
class UserAdmin(BaseUserAdmin, PolymorphicChildModelAdmin, DcsicAdminMixin):
    base_model = Contributor
    show_in_index = True

    inlines = [AccountEmailInline, IdentifierInline]
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
                width=300,
                height=300,
                preview_width=150,
                preview_height=150,
                format="webp",  # "jpeg", "png", "webp
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
