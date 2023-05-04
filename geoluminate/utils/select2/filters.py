from django_filters import rest_framework as df

from .widgets import ModelFieldSelect2MultiWidget, ModelFieldSelect2Widget


class Select2ChoiceFilterBase:
    def __init__(self, model, field, *args, **kwargs):
        kwargs.update(
            queryset=model.objects.filter(**{f"{field}__isnull": False}),
            to_field_name=field,
            widget=self.widget(
                search_fields=[
                    f"{field}__{kwargs.pop('select2_lookup_expr','icontains')}",
                ]
            ),
        )
        super().__init__(*args, **kwargs)


class Select2ChoiceFilter(Select2ChoiceFilterBase, df.ModelChoiceFilter):
    """A subclass of `django_filters.ModelChoiceFilter` that supports
    Select2 querying of possible values."""

    widget = ModelFieldSelect2Widget


class Select2MultipleChoiceFilter(Select2ChoiceFilterBase, df.ModelMultipleChoiceFilter):
    """Same as `Select2ChoiceFilter` but allows selection of multiple values"""

    widget = ModelFieldSelect2MultiWidget
