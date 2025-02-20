# import django_filters as df
from django import forms
from django.utils.translation import gettext_lazy as _
from django_filters import rest_framework as df

from .models import Dataset, Measurement, Project, Sample


class BaseListFilter(df.FilterSet):
    """Filter that includes a title and ordering field which can be used to filter a list. These two filters are
    displayed at the top of the list itself and will not be displayed in the sidebar. A second form helper is used to
    render the top filters. This class should be used as a base class for all list filters in the project.
    """

    o = df.OrderingFilter(
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


class ProjectFilter(BaseListFilter):
    class Meta:
        model = Project
        fields = {
            "name": ["icontains"],
            "status": ["exact"],
        }


class DatasetFilter(BaseListFilter):
    class Meta:
        model = Dataset
        fields = {
            "name": ["icontains"],
            "license": ["exact"],
        }


# class PolyFilter(BaseListFilter):
# type_choices = None

# @property
# def qs(self):
#     qs = super().qs
#     if not self.request or not self.request.GET.get("type"):
#         return qs

#     poly_subclass_name = self.request.GET.get("type")
#     model_class = apps.get_model(poly_subclass_name)
#     return qs.instance_of(model_class)

# def __init__(self, data=None, *args, **kwargs):
#     # if filterset is bound, use initial values as defaults
#     if data is not None:
#         # get a mutable copy of the QueryDict
#         data = data.copy()
#         if not data.get("type"):
#             data["type"] = self.type_choices[0][0]

#     super().__init__(data, *args, **kwargs)

# def filter_type(self, queryset, name, value):
#     model_class = apps.get_model(value)
#     return queryset.instance_of(model_class)


class SampleFilter(BaseListFilter):
    # type = df.ChoiceFilter(
    #     method="filter_type",
    #     choices=type_choices,
    #     required=True,
    #     empty_label=None,
    # )
    name = df.CharFilter(lookup_expr="icontains")

    class Meta:
        model = Sample
        fields = ["name", "status"]


class MeasurementFilter(BaseListFilter):
    name = df.CharFilter(lookup_expr="icontains")

    # type = df.ChoiceFilter(
    #     method="filter_type",
    #     choices=type_choices,
    #     required=True,
    #     empty_label=None,
    # )

    class Meta:
        fields = ["name"]
        model = Measurement
