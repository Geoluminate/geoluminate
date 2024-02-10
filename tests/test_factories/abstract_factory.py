from django.test import TestCase


class TestAbstractFactory(TestCase):
    def setUp(self):
        self.obj = None
        self.model = None

    def test_obj_creation(self):
        self.assertIsInstance(self.obj, self.model)
        self.assertIsNotNone(self.obj.title)
        self.assertIsNotNone(self.obj.summary)
        self.assertIsNotNone(self.obj.visibility)

    def test_obj_has_descriptions(self):
        self.assertTrue(1 <= len(self.obj.descriptions.count()) <= 4)

    def test_obj_has_key_dates(self):
        self.assertTrue(1 <= len(self.obj.key_dates.count()) <= 3)

    def test_obj_has_contributors(self):
        self.assertTrue(2 <= len(self.obj.contributors.count()) <= 5)

    def test_additional_model_field_creation(self):
        self.assertIsNotNone(self.obj.status)

    def test_project_has_datasets(self):
        self.assertTrue(2 <= len(self.obj.datasets.count()) <= 8)
