import factory
from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyChoice

from geoluminate.contrib.datasets import models as dataset_models
from geoluminate.contrib.measurements import models as meas_models
from geoluminate.contrib.projects import models as project_models
from geoluminate.core.choices import Visibility
from geoluminate.models import Dataset, Measurement, Project, Sample

from .contributors import ContributorFactoryList
from .core import DateFactory, DescriptionFactory
from .utils import ReusableFactoryList, randint


class ProjectFactory(DjangoModelFactory):
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


class DatasetFactory(DjangoModelFactory):
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
    # contributions = ReusableFactoryList(
    #     ContributionFactory,
    #     model=dataset_models.Contribution,
    #     choices=dataset_models.Contribution.CONTRIBUTOR_ROLES.values,
    # )
    contributions = factory.RelatedFactoryList(
        "geoluminate.factories.contributors.ContributionFactory",
        model=dataset_models.Contribution,
        factory_related_name="object",
        size=randint(1, 4),
        roles_choices=dataset_models.Contribution.CONTRIBUTOR_ROLES.values,
    )
    # contributions = ContributorFactoryList(
    #     dataset_models.Contribution,
    #     roles_choices=dataset_models.Contribution.CONTRIBUTOR_ROLES.values,
    # )

    # license = factory.Faker("random_instance", model=License)

    samples = factory.RelatedFactoryList(
        "geoluminate.factories.SampleFactory",
        factory_related_name="dataset",
        size=randint(10, 20),
    )

    class Meta:
        model = Dataset


class SampleFactory(DjangoModelFactory):
    """A factory for creating Sample objects."""

    dataset = factory.SubFactory("geoluminate.factories.contrib.DatasetFactory", samples=None)

    name = factory.Faker("sentence", nb_words=2, variable_nb_words=True)

    # status = FuzzyChoice(Sample.status_vocab.values)

    # descriptions = ReusableFactoryList(
    #     DescriptionFactory,
    #     model=sample_models.Description,
    #     choices=list(sample_models.Description.type_vocab.values),
    # )
    # dates = ReusableFactoryList(
    #     DateFactory,
    #     model=sample_models.Date,
    #     choices=list(sample_models.Date.type_vocab.values),
    # )
    # contributions = ContributorFactoryList(
    #     sample_models.Contribution,
    #     roles_choices=sample_models.Contribution.CONTRIBUTOR_ROLES.values,
    # )

    # measurements = factory.RelatedFactoryList(
    #     "geoluminate.factories.MeasurementFactory",
    #     factory_related_name="sample",
    #     size=randint(2, 5),
    # )

    class Meta:
        model = Sample

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        """Create an instance of the model, and save it to the database."""
        # if cls._meta.django_get_or_create:
        # return cls._get_or_create(model_class, *args, **kwargs)

        return model_class.add_root(*args, **kwargs)

        manager = cls._get_manager(model_class)
        return manager.create(*args, **kwargs)


class MeasurementFactory(DjangoModelFactory):
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
