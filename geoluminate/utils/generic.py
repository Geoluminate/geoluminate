from django.db import models


def choices_from_qs(qs, field):
    """Return a list of choices from a queryset"""
    return [(k, k) for k in (qs.order_by(field).values_list(field, flat=True).distinct())]


def get_choices(model, field):
    """Return a list of choices from a model"""

    def func():
        return [(k, k) for k in (model.objects.order_by(field).values_list(field, flat=True).distinct())]

    return func


def max_length_from_choices(choices):
    """Return the max length from a list of choices"""
    return max([len(choice[0]) for choice in choices])
