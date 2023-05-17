# import tzinfo from datetime

import factory
from django.contrib.auth import get_user_model
from django.contrib.gis.geos import Point
from faker.providers import BaseProvider

from geoluminate.contrib.controlled_vocabulary.models import ControlledVocabulary
from geoluminate.models import Geoluminate


class VocabularyIterator(factory.Iterator):
    def __init__(self, label, *args, **kwargs):
        iterator = ControlledVocabulary.objects.get(label=label).get_descendants()
        super().__init__(iterator, *args, **kwargs)


class GeoDjangoPointProvider(BaseProvider):
    def geo_point(self, **kwargs):
        faker = factory.faker.faker.Faker()
        coords = faker.latlng(**kwargs)
        return Point(x=float(coords[1]), y=float(coords[0]), srid=4326)


factory.Faker.add_provider(GeoDjangoPointProvider)


class UserFactory(factory.Factory):
    class Meta:
        model = get_user_model()

    email = factory.LazyAttribute(lambda o: f"{o.first_name}.{o.last_name}@fakeuser.org")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")


class GeoluminateFactory(factory.Factory):
    class Meta:
        model = Geoluminate

    name = factory.Faker("name")
    acquired = factory.Faker("date_time")
    comment = factory.Faker("text")
    elevation = factory.Faker("pyint", min_value=0, max_value=10000)
    geom = factory.Faker("geo_point")
