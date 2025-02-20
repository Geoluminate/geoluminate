"""Utility functions for importing data into the fairdm database."""

import numpy as np
import pandas as pd

# define a one to one map of field names per model. The per measurement end user can override these mappings to
# customize the import process for their data.
from django import forms
from django.db import models, transaction
from django.forms import modelform_factory
from polymorphic_treebeard.forms import movepolynodeform_factory
from quantityfield.fields import QuantityFieldMixin

from fairdm.models import Sample


def import_form_factory(model, *args, **kwargs):
    """Create a model form factory for the given model."""

    # make sure that all QuantityFields are converted to NumberInput fields
    # the default widget for a QuantityField expects a tuple of (value, units) so we need to override this
    widgets = {}
    for field in model._meta.fields:
        if issubclass(field.__class__, QuantityFieldMixin):
            widgets[field.name] = forms.NumberInput
        # elif isinstance(field, DecimalQuantityField):
        #     widgets[field.name] = forms.TextInput

    # if the user has passed in a custom widget mapping, update the widgets dictionary with the custom mapping
    user_widgets = kwargs.pop("widgets", {})
    widgets.update(user_widgets)
    # del kwargs["widgets"]

    if issubclass(model, Sample):
        form_class = movepolynodeform_factory(model, *args, widgets=widgets, **kwargs)
    else:
        form_class = modelform_factory(model, *args, widgets=widgets, **kwargs)

    for field in form_class.base_fields.values():
        field.required = False

    return form_class


class FairDMBaseImporter:
    df_init_kwargs = {}
    pandas_importer_func = "read_excel"
    models = {}
    import_order = []
    multi_value_fields = []
    multi_value_field_separator = ";"

    def __init__(self, io, dataset=None):
        self.io = io
        self.dataset = dataset
        self.df = self.read_dataframe()
        self.samples = self.dataset.samples.all()
        # self.measurements = self.dataset.measurements.all()

    def get_init_kwargs(self):
        """Return the initial kwargs for the dataframe read method."""
        return self.df_init_kwargs

    def read_dataframe(self):
        func = getattr(pd, self.pandas_importer_func)
        return func(self.io, **self.get_init_kwargs()).replace({np.nan: None})

    def process_import(self):
        import_errors = {}
        with transaction.atomic():
            for index, row in self.df.iterrows():
                errors = self.process_row(index, row.to_dict())
                if errors:
                    import_errors[index + 1] = errors

            if import_errors:
                self.errors = import_errors
                transaction.set_rollback(True)
                # raise ValueError("Errors occurred during import.")

        return import_errors

    def process_row(self, index, row):
        row["dataset"] = self.dataset
        model_errors = {}
        import_order = self.get_model_import_order()
        for model in import_order:
            errors = self.process_model(model, self.models[model], row, index)
            if errors:
                model_errors.update(errors)
        return model_errors

    def process_model(self, model, options, row, index):
        """Processes a single model per row in the import file. (Called by process_row)"""
        form_class = options.get("form_class") or self.get_model_form(model, options.get("form_kwargs", {}))

        cprow = self.modify_row(row, model, options)

        cprow.setdefault("local_id", index + 1)
        cprow.setdefault("_position", self.get_default_child_position(model))

        if cprow.get("parent"):
            cprow["_ref_node_id"] = cprow["parent"].pk

        form = form_class(data=cprow)
        if form.is_valid():
            form = self.before_form_save(form)
            instance = form.save()
            instance = self.after_form_save(instance)
            # instance.save()
            row[model] = instance
        else:
            return form.errors

    # def prepare_row(self, row, model, options):

    def modify_row(self, row, model, options):
        field_map = options.get("field_map", {})

        row = row.copy()
        self.clean_multi_value_fields(row, model)
        for field, mapped_field in field_map.items():
            row[field] = row.get(mapped_field)

        # for f in model._meta.fields:
        #     if issubclass(DecimalQuantityField, f.__class__) and row.get(f.name) is not None:
        #         row[f.name] = str(row.get(f.name))

        return row

    def clean_multi_value_fields(self, row, model):
        """Cleans up multi-value fields in the row data."""
        sep = self.multi_value_field_separator
        for field in self.multi_value_fields:
            if isinstance(field, tuple):
                field, sep = field
            if value := row.get(field):
                row[field] = [item.strip() for item in value.split(";") if item.strip()]
            else:
                row[field] = []

    def before_form_save(self, form):
        """Perform additional operations before saving the form. (e.g. modifying data).

        You can customize this method on a per model basis by defining a method with the following signature:

        def before_{model_name}_form_save(self, form):
            return form

        """
        model = form._meta.model
        save_func = getattr(self, f"before_{model.__name__.lower()}_form_save", None)
        if save_func:
            return save_func(form)
        return form

    def after_form_save(self, instance):
        """Perform additional operations after saving the form. (e.g. modifying data).

        You can customize this method on a per model basis by defining a method with the following signature:

        def after_{model_name}_form_save(self, instance):
            return instance

        """
        model = instance._meta.model
        save_func = getattr(self, f"after_{model.__name__.lower()}_form_save", None)
        if save_func:
            return save_func(instance)
        return instance

    def get_model_form(self, model, options):
        """Returns a model form for the given model and options."""
        return import_form_factory(model, **options)

    def get_model_import_order(self):
        """Inspects the field_map kwarg of all models to see if any one model depends on another for import. The models are then sorted based on import requirements."""
        sorted_models = []
        remaining_models = dict(self.models)  # Copy the original dictionary

        while remaining_models:
            # Find models whose parents are all in the sorted list or have no parents
            to_add = []
            for model, opts in remaining_models.items():
                # find any field dependencies that are models
                dependencies = [
                    m
                    for m in opts.get("field_map", {}).values()
                    if not isinstance(m, str) and issubclass(m, models.Model)
                ]

                # make sure all dependencies are included in the importer
                if not all(dep in self.models for dep in dependencies):
                    raise ValueError(f"Model {model} has unresolvable dependencies: {dependencies}")

                # parents = opts.get("parent", [])
                if all(dep in sorted_models for dep in dependencies):
                    to_add.append(model)

            if not to_add:
                raise ValueError("The import options contain a cycle or unresolvable dependencies.")

            # Add the found models to the sorted list and remove them from remaining_models
            for model in to_add:
                sorted_models.append(model)
                del remaining_models[model]

        return sorted_models

    def get_default_child_position(self, model):
        """Returns the default position for a child node in the Sample tree."""
        if getattr(model, "node_order_by", False):
            return "sorted-sibling"
        return "first-child"

    def create_template(self):
        """Creates a template for the import file from the importer configuration."""

        for model, options in self.models.items():
            fields = model._meta.get_fields()
            for field in fields:
                x = 1

    def debug_structure(self):
        """Pretty print the importer, including fields for each model."""

        for model, options in self.models.items():
            opts = options.copy()

            print(rf"\{model._meta.verbose_name}\n")
            parents = opts.pop("parents", {})
            field_map = opts.pop("field_map", {})
            form_class = opts.get("form_class") or self.get_model_form(model, opts)

            for fname, field in form_class.base_fields.items():
                ftype = field.widget.__class__.__name__
                if fname in field_map:
                    fname = f"{field_map[fname]} ({fname})"
                print(f"{fname:<{35}}{ftype}")


class SampleImporter(FairDMBaseImporter):
    sample = Sample
    sample_options = {}
