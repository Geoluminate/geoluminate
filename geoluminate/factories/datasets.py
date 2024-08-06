import factory
from factory.fuzzy import FuzzyChoice
from licensing.models import License

from geoluminate.contrib.datasets.models import Contribution, Dataset, Date, Description

from ..contrib.core.choices import Visibility
from .contributors import AbstractContributionFactory
from .core import AbstractDateFactory, AbstractDescriptionFactory, AbstractFactory, randint

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

    object = factory.SubFactory("geoluminate.factories.DatasetFactory", contributions=None)

    roles = factory.Faker("random_sample", elements=Contribution.CONTRIBUTOR_ROLES().values)

    class Meta:
        model = Contribution


class DatasetFactory(AbstractFactory):
    """A factory for creating Dataset objects."""

    project = factory.SubFactory("geoluminate.factories.ProjectFactory", datasets=None)
    title = factory.Faker("sentence", nb_words=8, variable_nb_words=True)
    visibility = FuzzyChoice(Visibility.values)

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
        size=randint(2, 5),
    )

    license = factory.Faker("random_instance", model=License)

    samples = factory.RelatedFactoryList(
        "geoluminate.factories.SampleFactory",
        factory_related_name="dataset",
        size=randint(10, 20),
    )

    class Meta:
        model = Dataset
