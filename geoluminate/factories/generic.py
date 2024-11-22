import random

import factory
import faker

# from django.contrib.gis.geos import Point
from research_vocabs.models import Concept

from geoluminate.contrib.generic.models import Date, Description

from .utils import randint


class GeoluminateProvider(faker.providers.BaseProvider):
    def geo_point(self, **kwargs):
        coords = faker.Faker().format("latlng", **kwargs)
        return "POINT({} {})".format(*coords)

    def html_paragraphs(self, nb=5, **kwargs):
        if callable(nb):
            nb = nb()
        pg_list = [faker.Faker().format("paragraph", **kwargs) for _ in range(nb)]
        return "<p>" + "</p><p>".join(pg_list) + "</p>"

    def multiline_text(self, nb=5, **kwargs):
        """Generate a multi-line string of paragraphs."""
        if callable(nb):
            nb = nb()
        pg_list = [faker.Faker().format("paragraph", **kwargs) for _ in range(nb)]
        return "\n\n".join(pg_list)

    def partial_date(self, **kwargs):
        date = faker.Faker().format("date_object", **kwargs)
        fmts = ["%Y", "%Y-%m", "%Y-%m-%d"]
        return date.strftime(random.choice(fmts))

    def random_instance(self, model=None, queryset=None):
        if not model and not queryset:
            raise ValueError("Must provide either a model or a queryset")
        qs = queryset or model.objects.all()
        return qs.order_by("?").first()


factory.Faker.add_provider(GeoluminateProvider)


class GenericFactory(factory.django.DjangoModelFactory):
    class Params:
        choices = None

    @factory.lazy_attribute_sequence
    def type(self, n):
        if not self.choices:
            raise ValueError("Must provide choices when building!")
        return self.choices[n % len(self.choices)]


class DescriptionFactory(GenericFactory):
    """A factory for creating Description objects."""

    class Meta:
        model = Description

    value = factory.Faker("multiline_text", nb=randint(3, 6), nb_sentences=12)


class DateFactory(GenericFactory):
    """A factory for creating Date objects."""

    class Meta:
        model = Date

    value = factory.Faker("partial_date")


class KeywordsFactory(factory.django.DjangoModelFactory):
    """A factory for creating Keywords objects."""

    class Meta:
        model = Concept


class Descriptions(factory.RelatedFactoryList):
    def __init__(self, choices: list, **kwargs):
        super().__init__(DescriptionFactory, "content_object", size=randint(1, len(choices)), choices=choices, **kwargs)


class Dates(factory.RelatedFactoryList):
    def __init__(self, choices: list, **kwargs):
        super().__init__(DateFactory, "content_object", size=randint(1, len(choices)), choices=choices, **kwargs)
