import random

import factory
import faker
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.gis.geos import Point
from django.db import models
from django.utils import timezone
from factory.fuzzy import FuzzyChoice

from geoluminate.contrib.contributors.tests.factories import ContributionFactory

# from faker import factory.Faker as provider
from geoluminate.contrib.core.models import Description, KeyDate
from geoluminate.contrib.samples.models import Location

# from geoluminate.contrib.datasets.tests.factories import DatasetFactory


def randint(min_value, max_value):
    return lambda: random.randint(min_value, max_value)


class GeoluminateProvider(faker.providers.BaseProvider):
    def geo_point(self, **kwargs):
        coords = faker.Faker().format("latlng", **kwargs)
        return Point(x=float(coords[1]), y=float(coords[0]), srid=4326)

    def choice_list(self, **kwargs):
        choices = kwargs.get("choices")
        if issubclass(choices, models.Choices):
            choices = choices.values
        return random.sample(choices, k=random.randint(1, len(choices)))

    def html_paragraphs(self, nb=5, **kwargs):
        if callable(nb):
            nb = nb()
        pg_list = [faker.Faker().format("paragraph", **kwargs) for _ in range(nb)]
        return "<p>" + "</p><p>".join(pg_list) + "</p>"


factory.Faker.add_provider(GeoluminateProvider)


class DescriptionFactory(factory.django.DjangoModelFactory):
    """A factory for creating Description objects."""

    class Meta:
        model = Description

    type = factory.Iterator(Description.DESCRIPTION_TYPES)
    text = factory.Faker("html_paragraphs", nb=randint(3, 6), nb_sentences=12)


class KeyDateFactory(factory.django.DjangoModelFactory):
    """A factory for creating KeyDate objects."""

    class Meta:
        model = KeyDate

    type = factory.Iterator(KeyDate.DateTypes)
    date = factory.Faker("date_time", tzinfo=timezone.get_current_timezone())


class LocationFactory(factory.django.DjangoModelFactory):
    name = factory.Faker("sentence", nb_words=2, variable_nb_words=True)
    point = factory.Faker("geo_point")
    elevation = factory.Faker("pyfloat", min_value=-12000, max_value=10000)

    class Meta:
        model = Location


# class SampleFactory(factory.django.DjangoModelFactory):
#     """A factory for creating Sample objects."""

#     # dataset = factory.Iterator(Dataset.objects.all())

#     dataset = factory.SubFactory(DatasetFactory)

#     location = factory.SubFactory(LocationFactory)
#     type = FuzzyChoice(settings.GEOLUMINATE_SAMPLE_TYPES)
#     title = factory.Faker("sentence", nb_words=2, variable_nb_words=True)
#     description = factory.Faker("html_paragraphs", nb=randint(3, 6), nb_sentences=12)
#     acquired = factory.Faker("date_time", tzinfo=timezone.get_current_timezone())
#     comment = factory.Faker("text")

#     class Meta:
#         model = Sample


# class MeasurementFactory(factory.django.DjangoModelFactory):
#     """A factory for creating Measurement objects."""

#     sample = factory.SubFactory(SampleFactory)
