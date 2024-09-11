import random

import factory
from factory import Faker, post_generation

from ..contrib.contributors.models import Contributor
from ..contrib.organizations.models import Membership, Organization
from .utils import randint


class GenericContributorFactory(factory.django.DjangoModelFactory):
    """Creates a Contributor object with no relationship to a Personal or Organization."""

    name = factory.Faker("name")
    about = factory.Faker("multiline_text", nb=randint(3, 5), nb_sentences=12)
    alternative_names = factory.List([factory.Faker("name") for _ in range(random.randint(1, 3))])
    lang = factory.Faker("language_code")

    class Meta:
        model = Contributor


class ContributionFactory(factory.django.DjangoModelFactory):
    """A factory for creating relationships between contributors and objects in the database.Should not be used directly but as a subfactory for other model factories that require contributor relationships."""

    class Params:
        generate_contributors = False
        roles_choices = None

    class Meta:
        django_get_or_create = ["contributor", "object"]

    @factory.lazy_attribute
    def roles(self):
        # parent_meta = self.factory_parent._Resolver__step.builder.factory_meta
        # parent_model = parent_meta.model
        max_roles = len(self.roles_choices)
        return random.sample(self.roles_choices, k=random.randint(1, max_roles))

    @factory.lazy_attribute
    def contributor(self):
        if self.generate_contributors:
            create_contributors(10, 5, 5)
            # self.__class__._contributor_cache = Contributor.objects.all()
            self.generate_contributors = False
        if not hasattr(self.__class__, "_contributor_cache"):
            self.__class__._contributor_cache = Contributor.objects.all()
        return random.choice(self._contributor_cache)

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        """Create an instance of the model, and save it to the database."""
        model_class = kwargs.pop("model", model_class)
        if cls._meta.django_get_or_create:
            return cls._get_or_create(model_class, *args, **kwargs)

        manager = cls._get_manager(model_class)
        return manager.create(*args, **kwargs)


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
        model = Personal
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


def create_contributors(n_active, n_organizations, n_inactive):
    """Create a set of users and organizations."""
    users = UserFactory.create_batch(n_active)
    inactive = GenericContributorFactory.create_batch(n_inactive)
    orgs = OrganizationFactory.create_batch(n_organizations)

    return users, inactive, orgs
    # OrganizationMembershipFactory.create_batch(n_organizations)


class ContributorFactoryList(factory.RelatedFactoryList):
    def __init__(self, model, **kwargs):
        related_factory = factory.make_factory(model, FACTORY_CLASS=ContributionFactory)
        factory_related_name = "object"
        super().__init__(related_factory, factory_related_name, **kwargs)
