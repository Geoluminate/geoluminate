import django_filters as df
from django import forms
from django.utils.translation import gettext_lazy as _
from django_filters import rest_framework as df

from .widgets import ModelFieldSelect2MultiWidget, ModelFieldSelect2Widget


class BaseListFilter(df.FilterSet):
    """Filter that includes a title and ordering field which can be used to filter a list. These two filters are
    displayed at the top of the list itself and will not be displayed in the sidebar. A second form helper is used to
    render the top filters. This class should be used as a base class for all list filters in the project.
    """

    title = df.CharFilter(
        label=False,
        lookup_expr="icontains",
        widget=forms.TextInput(attrs={"placeholder": _("Search by title")}),
    )

    o = df.OrderingFilter(
        label=False,
        fields=(
            ("created", "created"),
            ("modified", "modified"),
        ),
        field_labels={
            "created": _("Created"),
            "modified": _("Modified"),
        },
        widget=forms.Select,
        empty_label=_("Order by"),
    )

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.sidebar = FormHelper()
    #     self.top_helper = FormHelper()
    #     self.top_helper.layout = Layout(
    #         Div(
    #             Div("title", css_class="flex-grow-1"),
    #             Div("o"),
    #             css_class="d-flex",
    #         )
    #     )


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
