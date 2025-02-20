import pytest

from fairdm.core.models import Dataset
from fairdm.factories import DatasetFactory


@pytest.fixture
@pytest.mark.django_db
def dataset():
    yield DatasetFactory(project=None, samples=None)


@pytest.mark.django_db
class TestDatasetFactory:
    def test_factory_create(self, dataset):
        assert isinstance(dataset, Dataset)
        assert dataset.contributors.count() > 0
