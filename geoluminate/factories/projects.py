import factory
from factory.fuzzy import FuzzyChoice

from geoluminate.contrib.projects.models import Contribution, Date, Description, Project

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

    object = factory.SubFactory("geoluminate.factories.ProjectFactory", contributions=None)

    roles = factory.Faker("random_sample", elements=Contribution.CONTRIBUTOR_ROLES.values)

    class Meta:
        model = Contribution


class ProjectFactory(AbstractFactory):
    """A factory for creating Project objects."""

    class Meta:
        model = Project

    title = factory.Faker("sentence", nb_words=8, variable_nb_words=True)
    visibility = FuzzyChoice(Visibility.values)

    status = factory.Faker("pyint", min_value=0, max_value=4)
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
    datasets = factory.RelatedFactoryList(
        "geoluminate.factories.DatasetFactory",
        factory_related_name="project",
        size=randint(1, 3),
    )

    contributions = factory.RelatedFactoryList(
        ContributionFactory,
        factory_related_name="object",
        size=randint(1, 5),
    )
