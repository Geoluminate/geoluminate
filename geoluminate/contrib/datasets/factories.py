# import tzinfo from datetime

from random import randint

import factory

from geoluminate.contrib.core.factories import AbstractFactory

from .models import Dataset


class DatasetFactory(AbstractFactory):
    """A factory for creating Dataset objects."""

    project = factory.SubFactory("geoluminate.factories.ProjectFactory", datasets=None)

    samples = factory.RelatedFactoryList(
        "geoluminate.factories.SampleFactory",
        factory_related_name="dataset",
        size=lambda: randint(10, 20),
    )

    class Meta:
        model = Dataset
