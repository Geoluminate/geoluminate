import factory

from geoluminate.contrib.measurements.models import BaseMeasurement, Contribution, Date, Description

from .contributors import AbstractContributionFactory
from .core import AbstractDateFactory, AbstractDescriptionFactory, randint

DESCRIPTION_TYPES = list(Description.type_vocab.values)
DATE_TYPES = list(Date.type_vocab.values)


class DescriptionFactory(AbstractDescriptionFactory):
    """A factory for creating ProjectDescription objects."""

    type = factory.Iterator(DESCRIPTION_TYPES)

    class Meta:
        model = Description


class DateFactory(AbstractDateFactory):
    """A factory for creating ProjectDate objects."""

    type = factory.Iterator(DATE_TYPES)

    class Meta:
        model = Date


class ContributionFactory(AbstractContributionFactory):
    """A factory for creating ProjectDate objects."""

    roles = factory.Faker("random_sample", elements=Contribution.CONTRIBUTOR_ROLES.values)

    class Meta:
        model = Contribution


class MeasurementFactory(factory.django.DjangoModelFactory):
    """A factory for creating BaseMeasurement objects."""

    sample = factory.SubFactory("geoluminate.factories.SampleFactory", measurements=None)

    descriptions = factory.RelatedFactoryList(
        DescriptionFactory,
        factory_related_name="object",
        size=randint(1, len(DESCRIPTION_TYPES)),
    )
    dates = factory.RelatedFactoryList(
        DateFactory,
        factory_related_name="object",
        size=randint(1, len(DATE_TYPES)),
    )

    contributions = factory.RelatedFactoryList(
        ContributionFactory,
        factory_related_name="object",
        size=randint(1, 5),
    )

    class Meta:
        model = BaseMeasurement
