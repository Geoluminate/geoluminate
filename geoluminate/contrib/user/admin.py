# user/admin.py
# from allauth.socialaccount.models import Account
from allauth.account.models import EmailAddress
from allauth.socialaccount.models import SocialAccount
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from import_export.admin import ImportExportActionModelAdmin

from geoluminate.contrib.user.models import User

# from jazzmin import templatetags
from .forms import UserAdminChangeForm, UserAdminCreationForm


class SocialAccountInline(admin.StackedInline):
    model = SocialAccount
    fields = ["uid", "provider", "extra_data"]
    readonly_fields = ["uid", "provider", "extra_data"]
    extra = 0


class AccountEmailInline(admin.StackedInline):
    model = EmailAddress
    fields = [("primary", "verified"), "email"]
    extra = 0


@admin.register(User)
class UserAdmin(BaseUserAdmin, ImportExportActionModelAdmin):
    # The forms to add and change user instances
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm
    inlines = [AccountEmailInline, SocialAccountInline]
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
    list_filter = (
        "is_staff",
        "is_superuser",
    )

    # fieldsets for modifying user
    fieldsets = (
        (
            "Basic info",
            {
                "fields": (
                    "first_name",
                    "last_name",
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
            {"fields": ("last_name", "first_name", "email", "password1", "password2")},
        ),
    )

    search_fields = ("email",)
    ordering = ("last_name",)
    # filter_horizontal = ()
