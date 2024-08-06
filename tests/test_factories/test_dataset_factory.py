from geoluminate.contrib.datasets.models import Dataset
from geoluminate.factories import DatasetFactory

from .abstract_factory import TestAbstractFactory


class TestDatasetFactory(TestAbstractFactory):
    def setUp(self):
        self.obj = DatasetFactory()
        self.model = Dataset

    def test_obj_additional_fields_creation(self):
        self.assertIsNotNone(self.obj.title)
        self.assertIsNotNone(self.obj.visibility)
