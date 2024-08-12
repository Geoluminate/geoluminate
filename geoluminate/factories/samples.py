import factory
from factory.fuzzy import FuzzyChoice

from geoluminate.contrib.samples.models import Contribution, Date, Description, Location, Sample

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


class LocationFactory(factory.django.DjangoModelFactory):
    name = factory.Faker("sentence", nb_words=2, variable_nb_words=True)
    point = factory.Faker("geo_point")
    elevation = factory.Faker("pyfloat", min_value=-12000, max_value=10000)
    samples = factory.RelatedFactoryList(
        "geoluminate.factories.SampleFactory",
        factory_related_name="location",
        size=randint(2, 8),
    )

    class Meta:
        model = Location


class ContributionFactory(AbstractContributionFactory):
    """A factory for creating ProjectDate objects."""

    object = factory.SubFactory("geoluminate.factories.SampleFactory", contributions=None)
    roles = FuzzyChoice(Contribution.CONTRIBUTOR_ROLES.values)

    class Meta:
        model = Contribution


class SampleFactory(factory.django.DjangoModelFactory):
    """A factory for creating Sample objects."""

    # used when SampleFactory is called directly in order to create a dataset. samples is set to none so that DatasetFactory doesn't try to create new samples.
    dataset = factory.SubFactory("geoluminate.factories.DatasetFactory", samples=None)

    name = factory.Faker("sentence", nb_words=2, variable_nb_words=True)

    location = factory.SubFactory(LocationFactory, samples=None)
    status = FuzzyChoice(Sample.status_vocab.values)
    feature_type = FuzzyChoice(Sample.feature_type_vocab.values)
    medium = FuzzyChoice(Sample.medium_vocab.values)
    specimen_type = FuzzyChoice(Sample.specimen_type_vocab.values)

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

    measurements = factory.RelatedFactoryList(
        "geoluminate.factories.MeasurementFactory",
        factory_related_name="sample",
        size=randint(2, 5),
    )

    class Meta:
        model = Sample
