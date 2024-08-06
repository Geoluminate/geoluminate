import django_filters as df
from django import forms
from django.utils.translation import gettext_lazy as _
from formset.widgets import Selectize
from literature.models import LiteratureItem

from geoluminate.contrib.contributors.models import Contributor

from .models import Review


class ListFilterTop(df.FilterSet):
    title = df.CharFilter(
        lookup_expr="icontains",
        widget=forms.TextInput(attrs={"placeholder": "Find a review..."}),
    )

    status = df.ChoiceFilter(
        field_name="status",
        lookup_expr="exact",
        choices=Review.STATUS_CHOICES.choices,
        widget=forms.Select,
        empty_label=_("Review status"),
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


class ReviewFilter(ListFilterTop):
    reviewer = df.ChoiceFilter(
        label=_("Reviewer"),
        lookup_expr="exact",
        choices=Contributor.objects.all().values_list("id", "name"),
        widget=Selectize,
        empty_label=_("Reviewer"),
    )

    class Meta:
        model = LiteratureItem
        fields = ["title", "status", "o", "reviewer"]


class ListFilterTop(df.FilterSet):
    title = df.CharFilter(
        lookup_expr="icontains",
        widget=forms.TextInput(attrs={"placeholder": "Find a review..."}),
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


class LiteratureFilter(ListFilterTop):
    title = df.CharFilter(
        lookup_expr="icontains",
        widget=forms.TextInput(attrs={"placeholder": "Find literature..."}),
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

    class Meta:
        model = LiteratureItem
        fields = [
            "title",
            "o",
        ]
