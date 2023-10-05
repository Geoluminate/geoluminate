# import tzinfo from datetime

from random import randint

import factory

from geoluminate.contrib.core.tests.factories import (
    ContributionFactory,
    DescriptionFactory,
    KeyDateFactory,
)

from ..models import Dataset


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
