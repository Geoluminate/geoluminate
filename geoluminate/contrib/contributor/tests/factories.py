# import tzinfo from datetime

from random import randint

import factory

from geoluminate.contrib.user.factories import UserFactory

from ..models import Contribution, Contributor


class ProfileFactory(factory.django.DjangoModelFactory):
    """A factory for creating Contributor objects."""

    class Meta:
        model = Contributor
        django_get_or_create = ("user",)

    user = factory.SubFactory(UserFactory)
    image = factory.django.ImageField(color="blue", width=150, height=150)

    name = factory.Faker("name")
    about = factory.Faker("html_paragraphs", nb=lambda: randint(3, 6), nb_sentences=12)


class ContributionFactory(factory.django.DjangoModelFactory):
    """A factory for creating Contribution objects."""

    class Meta:
        model = Contribution

    roles = factory.Faker("choice_list", choices=Contribution.CONTRIBUTOR_ROLES)
    profile = factory.SubFactory(ProfileFactory)
