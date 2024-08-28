"""Utility functions for importing data into the geoluminate database."""

import pandas as pd

# define a one to one map of field names per model. The per measurement end user can override these mappings to
# customize the import process for their data.
from django import forms
from django.forms import modelform_factory
from polymorphic_treebeard.forms import movepolynodeform_factory
from quantityfield.fields import QuantityField

from .models import Sample


def import_form_factory(model, *args, **kwargs):
    """Create a model form factory for the given model."""

    # make sure that all QuantityFields are converted to NumberInput fields
    # the default widget for a QuantityField expects a tuple of (value, units) so we need to override this
    widgets = {}
    for field in model._meta.fields:
        if isinstance(field, QuantityField):
            widgets[field.name] = forms.NumberInput

    # if the user has passed in a custom widget mapping, update the widgets dictionary with the custom mapping
    if kwargs.get("widgets"):
        widgets.update(kwargs["widgets"])
        del kwargs["widgets"]

    if issubclass(model, Sample):
        return movepolynodeform_factory(model, widgets=widgets)
    form_class = modelform_factory(model, *args, widgets=widgets, **kwargs)

    for field in form_class.base_fields.values():
        field.required = False

    return form_class


class GeoluminateImporter:
    def __init__(self, file_obj):
        self.obj = file_obj
        self.df = pd.DataFrame(file_obj)

    def read_data(self):
        pass

    def import_data(self):
        project = self.save_project_data()
        dataset = self.save_dataset_data()
        sample = self.save_sample_data()
        measurement = self.save_measurement_data()
        print(project, dataset, sample, measurement)
