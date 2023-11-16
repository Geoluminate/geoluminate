import random

import factory
import faker
from django.contrib.gis.geos import Point
from django.db import models
from django.utils import timezone

from geoluminate.contrib.core.models import Description, FuzzyDate

from .choices import DiscoveryTags


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


class FuzzyDateFactory(factory.django.DjangoModelFactory):
    """A factory for creating FuzzyDate objects."""

    class Meta:
        model = FuzzyDate

    type = factory.Iterator(FuzzyDate.DateTypes)
    date = factory.Faker("date_time", tzinfo=timezone.get_current_timezone())


class AbstractFactory(factory.django.DjangoModelFactory):
    title = factory.Faker("sentence", nb_words=8, variable_nb_words=True)
    descriptions = factory.RelatedFactoryList(
        DescriptionFactory, factory_related_name="content_object", size=randint(1, 4)
    )
    key_dates = factory.RelatedFactoryList(FuzzyDateFactory, factory_related_name="content_object", size=randint(1, 3))
    contributors = factory.RelatedFactoryList(
        "geoluminate.factories.ContributionFactory", factory_related_name="content_object", size=randint(2, 5)
    )
    # tags = factory.Faker("choice_list", choices=DiscoveryTags)
