from geoluminate.contrib.samples.models import Sample
from geoluminate.factories import SampleFactory

from .abstract_factory import TestAbstractFactory


class TestProjectFactory(TestAbstractFactory):
    def setUp(self):
        self.obj = SampleFactory()
        self.model = Sample

    def test_obj_additional_fields_creation(self):
        self.assertIsNotNone(self.obj.title)
        self.assertIsNotNone(self.obj.summary)
        self.assertIsNotNone(self.obj.visibility)
