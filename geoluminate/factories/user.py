from collections.abc import Sequence
from typing import Any

import factory
from allauth.account.signals import user_signed_up
from django.contrib.auth import get_user_model
from factory import Faker, post_generation
from factory.django import DjangoModelFactory

from .core import randint


class UserFactory(DjangoModelFactory):
    email = factory.LazyAttribute(lambda o: f"{o.first_name}.{o.last_name}@fakeuser.org")
    first_name = Faker("first_name")
    last_name = Faker("last_name")

    profile = factory.RelatedFactory(
        "geoluminate.factories.PersonalContributorFactory",
        factory_related_name="user",
        user=None,
    )

    organization = factory.RelatedFactoryList(
        "geoluminate.factories.OrganizationMembershipFactory",
        factory_related_name="user",
        size=randint(1, 4),
    )

    @post_generation
    def password(self, create: bool, extracted: Sequence[Any], **kwargs):
        password = (
            extracted
            if extracted
            else Faker(
                "password",
                length=42,
                special_chars=True,
                digits=True,
                upper_case=True,
                lower_case=True,
            ).evaluate(None, None, extra={"locale": None})
        )
        self.set_password(password)

    class Meta:
        model = get_user_model()
        django_get_or_create = ["email"]
