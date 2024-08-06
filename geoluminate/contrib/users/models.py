from django.apps import apps
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Count
from django.utils.translation import gettext_lazy as _

from geoluminate.contrib.contributors.models import Contributor

from .managers import UserManager

USER_OPTIONS = {
    "allow_messages": True,
    "contact": True,
}


class User(AbstractUser, Contributor):
    """A custom user model with email as the primary identifier. The fields align with the W3C Organization and Person
    schema.org types. See https://schema.org/Person"""

    objects = UserManager()  # type: ignore[var-annotated]

    email = models.EmailField(_("email address"), unique=True)

    # settings = models.JSONField(default=dict, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    username = Contributor.__str__
    # polymorphic_primary_key_name = "id"

    def save(self, *args, **kwargs):
        if not self.pk:
            self.name = f"{self.first_name} {self.last_name}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_provider(self, provider: str):
        qs = self.socialaccount_set.filter(provider=provider)  # type: ignore[attr-defined]
        return qs.get() if qs else None


def forwards():
    EmailAddress = apps.get_model("account.EmailAddress")
    User = apps.get_model(settings.AUTH_USER_MODEL)
    user_email_field = getattr(settings, "ACCOUNT_USER_MODEL_EMAIL_FIELD", "email")

    def get_users_with_multiple_primary_email():
        user_pks = []
        for email_address_dict in (
            EmailAddress.objects.filter(primary=True).values("user").annotate(Count("user")).filter(user__count__gt=1)
        ):
            user_pks.append(email_address_dict["user"])
        return User.objects.filter(pk__in=user_pks)

    def unset_extra_primary_emails(user):
        qs = EmailAddress.objects.filter(user=user, primary=True)
        primary_email_addresses = list(qs)
        if not primary_email_addresses:
            return
        primary_email_address = primary_email_addresses[0]
        if user_email_field:
            for address in primary_email_addresses:
                if address.email.lower() == getattr(user, user_email_field, "").lower():
                    primary_email_address = address
                    break
        qs.exclude(pk=primary_email_address.pk).update(primary=False)

    for user in get_users_with_multiple_primary_email().iterator():
        unset_extra_primary_emails(user)
