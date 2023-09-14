import random

import factory
import faker
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.gis.geos import Point
from django.db import models
from django.utils import timezone
from factory.fuzzy import FuzzyChoice

# from faker import factory.Faker as provider
from geoluminate.contrib.core.models import (
    Contribution,
    Dataset,
    Description,
    KeyDate,
    Location,
    Project,
    Sample,
)
from geoluminate.contrib.user.models import Contributor, User


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


def randint(min_value, max_value):
    return lambda: random.randint(min_value, max_value)


class UserFactory(factory.django.DjangoModelFactory):
    """A factory for creating User objects."""

    class Meta:
        model = get_user_model()
        django_get_or_create = ("email",)

    email = factory.LazyAttribute(lambda o: f"{o.first_name}.{o.last_name}@fakeuser.org")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")


class ProfileFactory(factory.django.DjangoModelFactory):
    """A factory for creating Contributor objects."""

    class Meta:
        model = Contributor
        django_get_or_create = ("user",)

    user = factory.SubFactory(UserFactory)
    image = factory.django.ImageField(color="blue", width=150, height=150)

    name = factory.Faker("name")
    about = factory.Faker("html_paragraphs", nb=randint(3, 6), nb_sentences=12)


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


class ContributionFactory(factory.django.DjangoModelFactory):
    """A factory for creating Contribution objects."""

    class Meta:
        model = Contribution

    roles = factory.Faker("choice_list", choices=Contribution.CONTRIBUTOR_ROLES)
    profile = factory.SubFactory(ProfileFactory)


class DatasetFactory(factory.django.DjangoModelFactory):
    """A factory for creating Dataset objects."""

    # project = factory.Iterator(Project.objects.all())
    # reference = factory.SubFactory(ReferenceFactory)
    title = factory.Faker("sentence", nb_words=8, variable_nb_words=True)
    descriptions = factory.RelatedFactoryList(
        DescriptionFactory, factory_related_name="content_object", size=randint(1, 4)
    )
    key_dates = factory.RelatedFactoryList(KeyDateFactory, factory_related_name="content_object", size=randint(1, 3))
    contributors = factory.RelatedFactoryList(
        ContributionFactory, factory_related_name="content_object", size=randint(1, 5)
    )
    # samples = factory.RelatedFactoryList(SampleFactory, size=randint(10, 20))

    class Meta:
        model = Dataset


class LocationFactory(factory.django.DjangoModelFactory):
    name = factory.Faker("sentence", nb_words=2, variable_nb_words=True)
    point = factory.Faker("geo_point")
    elevation = factory.Faker("pyfloat", min_value=-12000, max_value=10000)

    class Meta:
        model = Location


class SampleFactory(factory.django.DjangoModelFactory):
    """A factory for creating Sample objects."""

    # dataset = factory.Iterator(Dataset.objects.all())

    dataset = factory.SubFactory(DatasetFactory)

    location = factory.SubFactory(LocationFactory)
    type = FuzzyChoice(settings.GEOLUMINATE_SAMPLE_TYPES)
    title = factory.Faker("sentence", nb_words=2, variable_nb_words=True)
    description = factory.Faker("html_paragraphs", nb=randint(3, 6), nb_sentences=12)
    acquired = factory.Faker("date_time", tzinfo=timezone.get_current_timezone())
    comment = factory.Faker("text")

    class Meta:
        model = Sample


class ProjectFactory(factory.django.DjangoModelFactory):
    """A factory for creating Project objects."""

    class Meta:
        model = Project

    image = factory.django.ImageField(color="blue", width=1200, height=630)

    title = factory.Faker("sentence", nb_words=8, variable_nb_words=True)
    status = factory.Faker("pyint", min_value=0, max_value=4)
    descriptions = factory.RelatedFactoryList(
        DescriptionFactory, factory_related_name="content_object", size=randint(1, 4)
    )
    key_dates = factory.RelatedFactoryList(KeyDateFactory, factory_related_name="content_object", size=randint(1, 3))
    contributors = factory.RelatedFactoryList(
        ContributionFactory, factory_related_name="content_object", size=randint(1, 5)
    )
    datasets = factory.RelatedFactoryList(DatasetFactory, size=randint(2, 8))
    # created_by = factory.Iterator(User.objects.all())


class MeasurementFactory(factory.django.DjangoModelFactory):
    """A factory for creating Measurement objects."""

    sample = factory.SubFactory(SampleFactory)
