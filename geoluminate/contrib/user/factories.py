# import tzinfo from datetime

import factory
from django.contrib.auth import get_user_model

from geoluminate.contrib.project.models import Site

from .models import Profile


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = get_user_model()
        django_get_or_create = ("email",)

    email = factory.LazyAttribute(lambda o: f"{o.first_name}.{o.last_name}@fakeuser.org")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")


class ProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Profile
        django_get_or_create = ("user",)

    user = factory.SubFactory(UserFactory)
    name = factory.Faker("name")
    about = factory.Faker("paragraph", nb_sentences=5, variable_nb_sentences=True)
    # location = factory.Faker("city")
    # birth_date = factory.Faker("date_of_birth", minimum_age=18, maximum_age=100)
    # avatar = factory.django.ImageField(color="blue")
