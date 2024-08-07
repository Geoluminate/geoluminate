from django.apps import apps


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


def object_from_letter(letter):
    """Return an object from a letter"""
    type_map = {
        "p": "projects.Project",
        "d": "datasets.Dataset",
        "s": "samples.BaseSample",
    }
    return apps.get_model(type_map.get(letter))
