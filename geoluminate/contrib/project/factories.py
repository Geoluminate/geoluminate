import factory
from django.contrib.gis.geos import Point
from faker.providers import BaseProvider

from geoluminate.contrib.user.models import User

from . import models


# Define a custom provider for generating GeoDjango points
class GeoDjangoPointProvider(BaseProvider):
    """
    A custom provider for generating GeoDjango points.
    """

    def geo_point(self, **kwargs):
        """
        Generate a GeoDjango point with random latitude and longitude coordinates.

        Args:
        **kwargs: Additional keyword arguments to be passed to the Faker latlng() method.

        Returns:
        Point: A GeoDjango Point object with random latitude and longitude coordinates.
        """
        faker = factory.faker.faker.Faker()
        coords = faker.latlng(**kwargs)
        return Point(x=float(coords[1]), y=float(coords[0]), srid=4326)


# Add the GeoDjangoPointProvider to the Faker provider list
factory.Faker.add_provider(GeoDjangoPointProvider)


# Define a factory for creating Project objects
class ProjectFactory(factory.django.DjangoModelFactory):
    """
    A factory for creating Project objects.
    """

    class Meta:
        model = models.Project

    name = factory.Faker("sentence", nb_words=8, variable_nb_words=True)

    # a description factory field that generates multiple paragraphs of random text
    # description = factory.Faker("parargraphs", nb=4, variable_nb_sentences=True)
    description = factory.Faker("paragraph", nb_sentences=3, variable_nb_sentences=True)
    lead = factory.Iterator(User.objects.all())
    status = factory.Faker("pyint", min_value=0, max_value=1)
    start_date = factory.Faker("date_time")
    end_date = factory.Faker("date_time")
    projected_start_date = factory.Faker("date_time")
    projected_end_date = factory.Faker("date_time")
    # inherit_license = factory.Faker("pybool")
    funding = factory.Faker("pydict", value_types=["str", "int", "float", "bool"])
    created_by = factory.Iterator(User.objects.all())


# Define a factory for creating Dataset objects
class DatasetFactory(factory.django.DjangoModelFactory):
    """
    A factory for creating Dataset objects.
    """

    project = factory.Iterator(models.Project.objects.all())
    name = factory.Faker("sentence", nb_words=8, variable_nb_words=True)
    description = factory.Faker("paragraph", nb_sentences=3, variable_nb_sentences=True)
    start_date = factory.Faker("date_time")
    end_date = factory.Faker("date_time")
    projected_start_date = factory.Faker("date_time")
    projected_end_date = factory.Faker("date_time")

    class Meta:
        model = models.Dataset


# Define a factory for creating Sample objects
class SampleFactory(factory.django.DjangoModelFactory):
    """
    A factory for creating Sample objects.
    """

    dataset = factory.Iterator(models.Dataset.objects.all())
    type = factory.Faker("pystr", min_chars=1, max_chars=255)
    name = factory.Faker("words", nb=6, ext_word_list=None)
    acquired = factory.Faker("date_time")
    comment = factory.Faker("text")
    elevation = factory.Faker("pyfloat", min_value=-12000, max_value=10000)
    geom = factory.Faker("geo_point")

    class Meta:
        model = models.Sample

    class Meta:
        model = models.Sample
