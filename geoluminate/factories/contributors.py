import factory

from ..contrib.contributors.models import Contribution, Contributor
from .core import randint


class UnclaimedContributorFactory(factory.django.DjangoModelFactory):
    """Creates a Contributor object with no relationship to a User or Organization."""

    name = factory.Faker("name")
    about = factory.Faker("multiline_text", nb=randint(3, 5), nb_sentences=12)

    class Meta:
        model = Contributor


class OrganizationalContributorFactory(UnclaimedContributorFactory):
    """Creates a Contributor object associated with an Organization."""

    name = factory.SelfAttribute("organization.name")
    about = factory.Faker("multiline_text", nb=randint(3, 5), nb_sentences=12)
    organization = factory.SubFactory("geoluminate.factories.OrganizationFactory", profile=None)

    class Meta:
        model = Contributor


class PersonalContributorFactory(UnclaimedContributorFactory):
    """Creates a Contributor object associated with a User."""

    name = factory.LazyAttribute(lambda o: f"{o.user.first_name} {o.user.last_name}")
    about = factory.Faker("multiline_text", nb=randint(3, 5), nb_sentences=12)
    user = factory.SubFactory("geoluminate.factories.UserFactory", profile=None)

    class Meta:
        model = Contributor


class ContributionFactory(factory.django.DjangoModelFactory):
    """A factory for creating relationships between contributors and objects in the database.Should not be used directly but as a subfactory for other model factories that require contributor relationships."""

    class Meta:
        model = Contribution

    roles = factory.Faker("choice_list", choices=Contribution.CONTRIBUTOR_ROLES)

    profile = factory.Iterator(Contributor.objects.all())

    # @factory.lazy_attribute
    # def profile(self):

    #     return [random.choice(Contributor.objects.all())]
