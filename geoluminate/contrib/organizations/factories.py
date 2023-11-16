import factory

from .models import Organization


class OrganizationFactory(factory.django.DjangoModelFactory):
    """A factory for creating Project objects."""

    class Meta:
        model = Organization

    name = factory.Faker("company")
    profile = factory.RelatedFactory(
        "geoluminate.factories.ContributorFactory",
        factory_related_name="organization",
        type="Organizational",
        name=factory.LazyAttribute(lambda o: o.factory_parent.name),
    )
