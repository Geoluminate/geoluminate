import factory
from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyChoice
from licensing.models import License

from geoluminate.core.choices import Visibility
from geoluminate.models import Dataset, Measurement, Project, Sample

from .core import Dates, Descriptions
from .utils import randint


class ProjectFactory(DjangoModelFactory):
    """A factory for creating Project objects."""

    class Meta:
        model = Project

    image = factory.django.ImageField(width=1200, height=1200)
    title = factory.Faker("sentence", nb_words=8, variable_nb_words=True)
    visibility = FuzzyChoice(Project.VISIBILITY.values)
    status = factory.Faker("pyint", min_value=0, max_value=4)
    datasets = factory.RelatedFactoryList(
        "geoluminate.factories.DatasetFactory",
        factory_related_name="project",
        size=randint(1, 3),
    )

    descriptions = Descriptions(choices=Project.DESCRIPTION_TYPES.values)
    dates = Dates(choices=Project.DATE_TYPES.values)
    contributions = factory.RelatedFactoryList(
        "geoluminate.factories.contributors.ContributionFactory",
        factory_related_name="content_object",
        size=randint(1, 5),
        roles_choices=Project.CONTRIBUTOR_ROLES.values,
    )


class DatasetFactory(DjangoModelFactory):
    """A factory for creating Dataset objects."""

    project = factory.SubFactory("geoluminate.factories.ProjectFactory", datasets=None)
    image = factory.django.ImageField(width=1200, height=1200)
    title = factory.Faker("sentence", nb_words=8, variable_nb_words=True)
    visibility = FuzzyChoice(Visibility.values)

    descriptions = Descriptions(choices=Dataset.DESCRIPTION_TYPES.values)
    dates = Dates(choices=Dataset.DATE_TYPES.values)
    contributions = factory.RelatedFactoryList(
        "geoluminate.factories.contributors.ContributionFactory",
        factory_related_name="content_object",
        size=randint(1, 5),
        roles_choices=Dataset.CONTRIBUTOR_ROLES.values,
    )

    license = factory.Faker("random_instance", model=License)

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
    descriptions = Descriptions(choices=Sample.DESCRIPTION_TYPES.values)
    dates = Dates(choices=Sample.DATE_TYPES.values)
    contributions = factory.RelatedFactoryList(
        "geoluminate.factories.contributors.ContributionFactory",
        factory_related_name="content_object",
        size=randint(1, 5),
        roles_choices=Sample.CONTRIBUTOR_ROLES.values,
    )
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
        return model_class.add_root(*args, **kwargs)


class MeasurementFactory(DjangoModelFactory):
    """A factory for creating Measurement objects."""

    sample = factory.SubFactory("geoluminate.factories.SampleFactory", measurements=None)

    # descriptions = ReusableFactoryList(
    #     DescriptionFactory,
    #     model=meas_models.Description,
    #     choices=list(meas_models.Description.type_vocab.values),
    # )
    # dates = ReusableFactoryList(
    #     DateFactory,
    #     model=meas_models.Date,
    #     choices=list(meas_models.Date.type_vocab.values),
    # )
    # contributions = ContributorFactoryList(
    #     meas_models.Contribution,
    #     roles_choices=meas_models.Contribution.CONTRIBUTOR_ROLES.values,
    # )

    class Meta:
        model = Measurement
