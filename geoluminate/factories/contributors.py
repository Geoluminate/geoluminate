import random

import factory
from factory import Faker, post_generation

from geoluminate.contrib.users.models import User

from ..contrib.contributors.models import Contributor
from ..contrib.organizations.models import Membership, Organization
from .core import randint


class GenericContributorFactory(factory.django.DjangoModelFactory):
    """Creates a Contributor object with no relationship to a User or Organization."""

    name = factory.Faker("name")
    about = factory.Faker("multiline_text", nb=randint(3, 5), nb_sentences=12)
    alternative_names = factory.List([factory.Faker("name") for _ in range(random.randint(1, 3))])
    lang = factory.Faker("language_code")

    class Meta:
        model = Contributor


class AbstractContributionFactory(factory.django.DjangoModelFactory):
    """A factory for creating relationships between contributors and objects in the database.Should not be used directly but as a subfactory for other model factories that require contributor relationships."""

    contributor = Faker("random_instance", model=Contributor)


class UserFactory(GenericContributorFactory):
    email = factory.LazyAttribute(lambda o: f"{o.first_name}.{o.last_name}@fakeuser.org")
    first_name = Faker("first_name")
    last_name = Faker("last_name")

    # organization = factory.RelatedFactoryList(
    #     "geoluminate.factories.OrganizationMembershipFactory",
    #     factory_related_name="user",
    #     size=randint(1, 4),
    # )

    @post_generation
    def password(self, create: bool, extracted, **kwargs):
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
        model = User
        django_get_or_create = ["email"]


class OrganizationFactory(GenericContributorFactory):
    """Create an organization and associates it with a Contributor profile."""

    name = factory.Faker("company")
    alternative_names = factory.List([factory.Faker("company") for _ in range(random.randint(0, 3))])

    class Meta:
        model = Organization


class OrganizationMembershipFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Membership

    user = factory.SubFactory("geoluminate.factories.UserFactory", organization=None)
    organization = factory.SubFactory(
        "geoluminate.factories.OrganizationFactory",
    )
    is_admin = factory.Faker("boolean", chance_of_getting_true=10)
