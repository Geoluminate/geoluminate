import unittest
from unittest.mock import patch
from faker import Faker
from geoluminate.contrib.user.models import User
from geoluminate.contrib.project.factories import GeoDjangoPointProvider
from django.contrib.gis.geos import Point


class TestGeoDjangoPointProvider(unittest.TestCase):
    """
    This class contains unit tests for the `GeoDjangoPointProvider` class.
    """

    def setUp(self):
        """
        Set up the test case.
        """
        self.fake = Faker()
        self.fake.add_provider(GeoDjangoPointProvider)

    def test_geo_point_returns_point(self):
        """
        Test that the `geo_point` method returns a `Point` object.
        """
        point = self.fake.geo_point()
        self.assertIsInstance(point, Point)

    @patch.object(Faker, 'latlng')
    def test_geo_point_calls_latlng(self, mock_latlng):
        """
        Test that the `geo_point` method calls the `latlng` method of the `Faker` object.
        """
        self.fake.geo_point()
        mock_latlng.assert_called_once()

    @patch.object(Point, '__init__')
    def test_geo_point_creates_point(self, mock_point_init):
        """
        Test that the `geo_point` method creates a `Point` object with the correct coordinates.
        """
        lat, lng = self.fake.latitude(), self.fake.longitude()
        self.fake.geo_point()
        mock_point_init.assert_called_once_with(x=lng, y=lat, srid=4326)