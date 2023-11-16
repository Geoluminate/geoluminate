# import tzinfo from datetime

from random import randint

import factory

from geoluminate.contrib.core import factories

# from geoluminate.contrib.users.factories import UserFactory
from .models import Contribution, Contributor, Organizational, Personal


class ContributorFactory(factory.django.DjangoModelFactory):
    """A factory for creating Contributor objects."""

    name = factory.Faker("name")
    about = factory.Faker("html_paragraphs", nb=lambda: randint(3, 6), nb_sentences=12)

    class Meta:
        model = Contributor


class OrganisationalContributorFactory(ContributorFactory):
    # organization = factory.RelatedFactory("geoluminate.factories.OrganizationFactory", factory_related_name="profile")
    name = factory.SelfAttribute("organization.name")
    organization = factory.SubFactory("geoluminate.factories.OrganizationFactory", profile=None)

    class Meta:
        model = Organizational


class PersonalContributorFactory(ContributorFactory):
    # user = factory.RelatedFactory("geoluminate.factories.UserFactory", factory_related_name="profile")
    user = factory.SubFactory("geoluminate.factories.UserFactory", profile=None)
    name = factory.SelfAttribute("organization.name")

    class Meta:
        model = Personal


class ContributionFactory(factory.django.DjangoModelFactory):
    """A factory for creating Contribution objects."""

    class Meta:
        model = Contribution

    roles = factory.Faker("choice_list", choices=Contribution.CONTRIBUTOR_ROLES)
    # profile = factory.SubFactory(PersonalContributorFactory)
    profile = factory.Iterator(Contributor.objects.all())
