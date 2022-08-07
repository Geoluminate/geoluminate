from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class RangeField(models.FloatField):

    def __init__(self, *args, **kwargs):

        validators = kwargs.pop('validators', [])

        if kwargs.get('max_value') is not None:
            validators.append(MaxValueValidator(kwargs.pop('max_value')))

        if kwargs.get('min_value') is not None:
            validators.append(MinValueValidator(kwargs.pop('min_value')))

        super().__init__(validators=validators, *args, **kwargs)