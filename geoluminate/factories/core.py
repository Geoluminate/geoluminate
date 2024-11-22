import random

import factory
from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyChoice
from licensing.models import License

from geoluminate.core.choices import Visibility
from geoluminate.models import Dataset, Measurement, Project, Sample

from .generic import Dates, Descriptions
from .utils import TreeFactory, randint


class ProjectFactory(DjangoModelFactory):
    """A factory for creating Project objects."""

    class Meta:
        model = Project

    image = factory.django.ImageField(width=1200, height=1200)
    name = factory.Faker("sentence", nb_words=8, variable_nb_words=True)
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
    name = factory.Faker("sentence", nb_words=8, variable_nb_words=True)
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


class SampleFactory(TreeFactory):
    """A factory for creating Sample objects."""

    dataset = factory.SubFactory("geoluminate.factories.core.DatasetFactory", samples=None)

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

    @factory.post_generation
    def children(instance, create, extracted, **kwargs):
        """Post-generation hook to recursively generate child nodes."""
        if not create:
            return

        max_depth = kwargs.pop("max_depth", 1)
        max_children = kwargs.pop("max_children", 1)

        if instance.depth >= max_depth:
            return

        num_children = random.randint(2, max_children)

        SampleFactory.create_batch(
            num_children,
            parent=instance,
            children__max_depth=max_depth,
            children__max_children=max_children,
        )


class MeasurementFactory(DjangoModelFactory):
    """A factory for creating Measurement objects."""

    sample = factory.SubFactory("geoluminate.factories.SampleFactory", measurements=None)

    # contributions = ContributorFactoryList(
    #     meas_models.Contribution,
    #     roles_choices=meas_models.Contribution.CONTRIBUTOR_ROLES.values,
    # )

    class Meta:
        model = Measurement
