import random

import factory
from django.contrib.contenttypes.models import ContentType
from factory import Faker, post_generation

from ..contrib.contributors.models import Contributor
from .utils import randint


class ContributorFactory(factory.django.DjangoModelFactory):
    """Creates a Contributor object with no relationship to a Personal or Organization."""

    image = factory.django.ImageField(width=1200, height=1200, color="blue")
    profile = factory.Faker("multiline_text", nb=randint(3, 5), nb_sentences=12)
    alternative_names = factory.List([factory.Faker("name") for _ in range(random.randint(1, 3))])
    lang = factory.List([factory.Faker("language_code") for _ in range(random.randint(0, 3))])

    class Meta:
        model = Contributor


class ContributionFactory(factory.django.DjangoModelFactory):
    """A factory for creating relationships between contributors and objects in the database.Should not be used directly but as a subfactory for other model factories that require contributor relationships."""

    class Params:
        generate_contributors = False
        roles_choices = None
        max_persons = 10

    class Meta:
        model = "contributors.Contribution"
        django_get_or_create = ["contributor", "object_id", "content_type"]

    content_type = factory.LazyAttribute(lambda o: ContentType.objects.get_for_model(o.content_object))
    object_id = factory.SelfAttribute("content_object.id")

    @factory.lazy_attribute
    def roles(self):
        max_roles = len(self.roles_choices)
        return random.sample(self.roles_choices, k=random.randint(1, max_roles))

    @factory.lazy_attribute
    def contributor(self):
        if self.generate_contributors or not Contributor.objects.exists():
            PersonFactory.create_batch(self.max_persons)
            # self.generate_contributors = False
        if not hasattr(self.__class__, "_contributor_cache"):
            self.__class__._contributor_cache = Contributor.objects.all()
        return random.choice(self._contributor_cache)

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        """Create an instance of the model, and save it to the database."""
        if cls._meta.django_get_or_create:
            return cls._get_or_create(model_class, *args, **kwargs)

        manager = cls._get_manager(model_class)
        return manager.create(*args, **kwargs)


class PersonFactory(ContributorFactory):
    name = factory.LazyAttribute(lambda o: f"{o.first_name} {o.last_name}")
    email = factory.LazyAttribute(lambda o: f"{o.first_name}.{o.last_name}@fakeuser.org")
    first_name = Faker("first_name")
    last_name = Faker("last_name")
    is_active = factory.Faker("boolean", chance_of_getting_true=75)
    organization = factory.RelatedFactoryList(
        "fairdm.factories.OrganizationMembershipFactory",
        factory_related_name="person",
        size=randint(1, 4),
    )

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
        model = "contributors.Person"
        django_get_or_create = ["email"]


class OrganizationFactory(ContributorFactory):
    """Create an organization and associates it with a Contributor profile."""

    name = factory.Faker("company")
    alternative_names = factory.List([factory.Faker("company") for _ in range(random.randint(0, 3))])

    class Meta:
        model = "contributors.Organization"


class OrganizationMembershipFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "contributors.OrganizationMember"

    person = factory.SubFactory("fairdm.factories.PersonFactory")
    organization = factory.SubFactory("fairdm.factories.OrganizationFactory")
    # is_admin = factory.Faker("boolean", chance_of_getting_true=10)


def create_contributors(n_active, n_organizations, n_inactive):
    """Create a set of users and organizations."""
    return PersonFactory.create_batch(n_active)
