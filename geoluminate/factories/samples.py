import factory
from factory.fuzzy import FuzzyChoice

from geoluminate.db.models import Location, Sample

from .core import AbstractFactory, randint


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


class SampleFactory(AbstractFactory):
    """A factory for creating Sample objects."""

    # user when SampleFactory is called directly in order to create a dataset. samples is set to none so that DatasetFactory doesn't try to create new samples.
    dataset = factory.SubFactory("geoluminate.factories.DatasetFactory", samples=None)

    location = factory.SubFactory(LocationFactory, samples=None)
    status = FuzzyChoice(Sample.STATUS.values)
    feature_type = FuzzyChoice(Sample.FEATURE_TYPES.values)
    medium = FuzzyChoice(Sample.SAMPLING_MEDIA.values)
    specimen_type = FuzzyChoice(Sample.SPECIMEN_TYPE.values)

    description = factory.Faker("multiline_text", nb=randint(3, 6), nb_sentences=12)

    comment = factory.Faker("text")

    class Meta:
        model = Sample


class MeasurementFactory(factory.django.DjangoModelFactory):
    """A factory for creating Measurement objects."""

    sample = factory.Iterator(Sample.objects.all())
