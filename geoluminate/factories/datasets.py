import factory
from licensing.models import License

from ..contrib.datasets.models import Dataset
from .core import AbstractFactory, randint


class DatasetFactory(AbstractFactory):
    """A factory for creating Dataset objects."""

    project = factory.SubFactory("geoluminate.factories.ProjectFactory", datasets=None)

    license = factory.Iterator(License.objects.all())

    samples = factory.RelatedFactoryList(
        "geoluminate.factories.SampleFactory",
        factory_related_name="dataset",
        size=randint(10, 20),
    )

    class Meta:
        model = Dataset
