from django.contrib import admin
from parler.admin import TranslatableAdmin
from solo.admin import SingletonModelAdmin

from .models import Authority, Database


@admin.register(Authority)
class AuthorityIdentityAdmin(TranslatableAdmin, SingletonModelAdmin):
    fields = (
        ("logo", "icon"),
        ("name", "short_name"),
        "url",
        "contact",
        "description",
    )


@admin.register(Database)
class DatabaseIdentityAdmin(TranslatableAdmin, SingletonModelAdmin):
    fields = (
        ("logo", "icon"),
        ("name", "short_name"),
        "description",
        "keywords",
    )
