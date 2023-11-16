# import tzinfo from datetime

from random import randint

import factory

from geoluminate.contrib.core.factories import AbstractFactory

from .models import Project


class ProjectFactory(AbstractFactory):
    """A factory for creating Project objects."""

    class Meta:
        model = Project

    status = factory.Faker("pyint", min_value=0, max_value=4)
    datasets = factory.RelatedFactoryList(
        "geoluminate.factories.DatasetFactory",
        factory_related_name="project",
        size=lambda: randint(2, 8),
    )
