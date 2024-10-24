import pytest

from geoluminate.contrib.datasets.models import Dataset
from geoluminate.factories import DatasetFactory


@pytest.fixture
@pytest.mark.django_db
def dataset():
    yield DatasetFactory(project=None, samples=None)


@pytest.mark.django_db
class TestDatasetFactory:
    def test_factory_create(self, dataset):
        assert isinstance(dataset, Dataset)
        assert dataset.contributors.count() > 0
