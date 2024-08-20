from allauth.account.models import EmailAddress
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from polymorphic.admin import PolymorphicChildModelAdmin

from geoluminate.contrib.contributors.admin import IdentifierInline
from geoluminate.contrib.contributors.models import Contributor
from geoluminate.contrib.users.models import User


class AccountEmailInline(admin.TabularInline):
    model = EmailAddress
    fields = ["email", "primary", "verified"]
    extra = 0


@admin.register(User)
class UserAdmin(BaseUserAdmin, PolymorphicChildModelAdmin):
    base_model = Contributor
    show_in_index = True
    # The forms to add and change user instances
    # form = UserAdminChangeForm
    # add_form = UserAdminCreationForm
    inlines = [AccountEmailInline, IdentifierInline]
    list_display = [
        "first_name",
        "last_name",
        "email",
        "is_superuser",
        "is_staff",
        "is_active",
        "last_login",
        "date_joined",
    ]
    list_filter = ("is_staff", "is_superuser")
    # fieldsets for modifying user
    fieldsets = (
        (
            "Basic info",
            {
                "fields": (
                    "image",
                    ("first_name", "last_name"),
                    "email",
                    "password",
                )
            },
        ),
        (
            "Permissions",
            {"fields": (("is_active", "is_staff"), "groups", "user_permissions")},
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
    # filter_horizontal = ()
