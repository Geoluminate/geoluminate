# import tzinfo from datetime

from random import randint

import factory

from geoluminate.contrib.core.tests.factories import (
    ContributionFactory,
    DescriptionFactory,
    KeyDateFactory,
)
from geoluminate.contrib.datasets.tests.factories import DatasetFactory

from ..models import Project


class ProjectFactory(factory.django.DjangoModelFactory):
    """A factory for creating Project objects."""

    class Meta:
        model = Project

    image = factory.django.ImageField(color="blue", width=1200, height=630)

    title = factory.Faker("sentence", nb_words=8, variable_nb_words=True)
    status = factory.Faker("pyint", min_value=0, max_value=4)
    descriptions = factory.RelatedFactoryList(
        DescriptionFactory, factory_related_name="content_object", size=randint(1, 4)
    )
    key_dates = factory.RelatedFactoryList(KeyDateFactory, factory_related_name="content_object", size=randint(1, 3))
    contributors = factory.RelatedFactoryList(
        ContributionFactory, factory_related_name="content_object", size=randint(1, 5)
    )
    datasets = factory.RelatedFactoryList(DatasetFactory, size=randint(2, 8))
