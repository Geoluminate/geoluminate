import django_filters as df
from django import forms
from django.forms import widgets
from django.utils.translation import gettext_lazy as _
from django_select2.forms import Select2MultipleWidget
from formset.widgets import Selectize, SelectizeMultiple
from literature.models import Literature
from taggit.models import Tag

from geoluminate.contrib.core.choices import HAS_TAGS, NEEDS_TAGS
from geoluminate.contrib.users.models import Contributor

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
        model = Literature
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
        model = Literature
        fields = [
            "title",
            "o",
        ]
