import django_filters as df
from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Contributor


class ListFilterTop(df.FilterSet):
    name = df.CharFilter(
        lookup_expr="icontains",
        widget=forms.TextInput(attrs={"placeholder": "Find a contributor..."}),
    )

    o = df.OrderingFilter(
        fields=(
            ("created", "created"),
            ("modified", "modified"),
        ),
        field_labels={
            "created": _("Created"),
            "modified": _("Modified"),
        },
        label=_("Sort by"),
        widget=forms.Select,
        empty_label=_("Order by"),
    )


class ContributorFilter(ListFilterTop):
    type = df.ChoiceFilter(
        choices=[
            ("active", "Active"),
            ("persons", "Persons"),
            ("organizations", "Organizations"),
        ],
        label=_("Type"),
        method="filter_type",
        widget=forms.Select,
        empty_label=_("Type"),
    )

    class Meta:
        model = Contributor
        fields = ["name", "o", "type"]

    def filter_type(self, queryset, name, value):
        if value == "active":
            return queryset.active()
        elif value == "persons":
            return queryset.persons()
        elif value == "organizations":
            return queryset.organizations()
        return queryset


# class ContributionFilter(df.FilterSet):
#     class Meta:
#         model = Contribution
#         fields = {
#             "roles": ["icontains"],
#         }
