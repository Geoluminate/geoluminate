import factory

from geoluminate.db.models import Project

from .core import AbstractFactory, randint


class ProjectFactory(AbstractFactory):
    """A factory for creating Project objects."""

    class Meta:
        model = Project

    status = factory.Faker("pyint", min_value=0, max_value=4)
    datasets = factory.RelatedFactoryList(
        "geoluminate.factories.DatasetFactory",
        factory_related_name="project",
        size=randint(2, 8),  # type: ignore
    )
