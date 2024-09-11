import factory
from factory.fuzzy import FuzzyChoice
from licensing.models import License

from geoluminate.contrib.datasets import models as dataset_models
from geoluminate.contrib.measurements import models as meas_models
from geoluminate.contrib.projects import models as project_models
from geoluminate.contrib.samples import models as sample_models
from geoluminate.models import Dataset, Measurement, Project, Sample

from ...core.choices import Visibility
from .contributors import ContributorFactoryList
from .core import AbstractFactory, DateFactory, DescriptionFactory
from .utils import ReusableFactoryList, randint


class ProjectFactory(AbstractFactory):
    """A factory for creating Project objects."""

    class Meta:
        model = Project

    title = factory.Faker("sentence", nb_words=8, variable_nb_words=True)
    visibility = FuzzyChoice(Visibility.values)

    status = factory.Faker("pyint", min_value=0, max_value=4)
    datasets = factory.RelatedFactoryList(
        "geoluminate.factories.DatasetFactory",
        factory_related_name="project",
        size=randint(1, 3),
    )

    descriptions = ReusableFactoryList(
        DescriptionFactory,
        model=project_models.Description,
        choices=list(
            project_models.Description.type_vocab.values,
        ),
    )
    dates = ReusableFactoryList(
        DateFactory,
        model=project_models.Date,
        choices=list(project_models.Date.type_vocab.values),
    )
    contributions = ContributorFactoryList(
        project_models.Contribution,
        roles_choices=project_models.Contribution.CONTRIBUTOR_ROLES.values,
    )


class DatasetFactory(AbstractFactory):
    """A factory for creating Dataset objects."""

    project = factory.SubFactory("geoluminate.factories.ProjectFactory", datasets=None)
    title = factory.Faker("sentence", nb_words=8, variable_nb_words=True)
    visibility = FuzzyChoice(Visibility.values)

    descriptions = ReusableFactoryList(
        DescriptionFactory,
        model=dataset_models.Description,
        choices=list(
            dataset_models.Description.type_vocab.values,
        ),
    )
    dates = ReusableFactoryList(
        DateFactory,
        model=dataset_models.Date,
        choices=list(dataset_models.Date.type_vocab.values),
    )
    contributions = ContributorFactoryList(
        dataset_models.Contribution,
        roles_choices=dataset_models.Contribution.CONTRIBUTOR_ROLES.values,
    )

    license = factory.Faker("random_instance", model=License)

    samples = factory.RelatedFactoryList(
        "geoluminate.factories.SampleFactory",
        factory_related_name="dataset",
        size=randint(10, 20),
    )

    class Meta:
        model = Dataset


class SampleFactory(factory.django.DjangoModelFactory):
    """A factory for creating Sample objects."""

    # used when SampleFactory is called directly in order to create a dataset. samples is set to none so that DatasetFactory doesn't try to create new samples.
    dataset = factory.SubFactory("geoluminate.factories.contrib.DatasetFactory", samples=None)

    name = factory.Faker("sentence", nb_words=2, variable_nb_words=True)

    status = FuzzyChoice(Sample.status_vocab.values)

    descriptions = ReusableFactoryList(
        DescriptionFactory,
        model=sample_models.Description,
        choices=list(sample_models.Description.type_vocab.values),
    )
    dates = ReusableFactoryList(
        DateFactory,
        model=sample_models.Date,
        choices=list(sample_models.Date.type_vocab.values),
    )
    contributions = ContributorFactoryList(
        sample_models.Contribution,
        roles_choices=sample_models.Contribution.CONTRIBUTOR_ROLES.values,
    )

    measurements = factory.RelatedFactoryList(
        "geoluminate.factories.MeasurementFactory",
        factory_related_name="sample",
        size=randint(2, 5),
    )

    class Meta:
        model = Sample


class MeasurementFactory(factory.django.DjangoModelFactory):
    """A factory for creating Measurement objects."""

    sample = factory.SubFactory("geoluminate.factories.SampleFactory", measurements=None)

    descriptions = ReusableFactoryList(
        DescriptionFactory,
        model=meas_models.Description,
        choices=list(meas_models.Description.type_vocab.values),
    )
    dates = ReusableFactoryList(
        DateFactory,
        model=meas_models.Date,
        choices=list(meas_models.Date.type_vocab.values),
    )
    contributions = ContributorFactoryList(
        meas_models.Contribution,
        roles_choices=meas_models.Contribution.CONTRIBUTOR_ROLES.values,
    )

    class Meta:
        model = Measurement


class ReviewFactory(AbstractFactory):
    """A factory for creating Dataset objects."""

    project = factory.SubFactory("geoluminate.factories.ProjectFactory", datasets=None)

    samples = factory.RelatedFactoryList(
        "geoluminate.factories.SampleFactory",
        factory_related_name="dataset",
        size=randint(10, 20),
    )

    class Meta:
        model = Dataset
