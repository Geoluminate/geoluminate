import factory

from ..contrib.organizations.models import Membership, Organization


class OrganizationFactory(factory.django.DjangoModelFactory):
    """Create an organization and associates it with a Contributor profile."""

    class Meta:
        model = Organization

    name = factory.Faker("company")
    profile = factory.RelatedFactory(
        "geoluminate.factories.OrganizationalContributorFactory",
        factory_related_name="organization",
        organization=None,
    )


class OrganizationMembershipFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Membership

    user = factory.SubFactory("geoluminate.factories.UserFactory", organization=None)
    organization = factory.SubFactory(
        "geoluminate.factories.OrganizationFactory",
    )
    is_admin = factory.Faker("boolean", chance_of_getting_true=10)
