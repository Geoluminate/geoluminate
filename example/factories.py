import factory

from fairdm.factories import SampleFactory

from .models import CustomSample


class CustomSampleFactory(SampleFactory):
    char_field = factory.Faker("word")
    text_field = factory.Faker("text")
    integer_field = factory.Faker("random_int")
    big_integer_field = factory.Faker("random_int")
    positive_integer_field = factory.Faker("random_int")
    positive_small_integer_field = factory.Faker("random_int")
    small_integer_field = factory.Faker("random_int")
    boolean_field = factory.Faker("boolean")
    date_field = factory.Faker("date")
    date_time_field = factory.Faker("date_time")
    time_field = factory.Faker("time")
    decimal_field = factory.Faker("pydecimal", left_digits=3, right_digits=2, positive=True)
    float_field = factory.Faker("random_int")

    class Meta:
        model = CustomSample
