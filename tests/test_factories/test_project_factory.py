from fairdm.core.models import Project
from fairdm.factories import ProjectFactory

from .abstract_factory import TestAbstractFactory


class TestProjectFactory(TestAbstractFactory):
    def setUp(self):
        self.obj = ProjectFactory()
        self.model = Project

    def test_obj_additional_fields_creation(self):
        self.assertIsNotNone(self.obj.title)
        self.assertIsNotNone(self.obj.visibility)
