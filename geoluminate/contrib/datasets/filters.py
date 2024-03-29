import django_filters as df
from django import forms
from django.utils.translation import gettext_lazy as _
from formset.widgets import SelectizeMultiple
from taggit.models import Tag

from .models import Dataset


class ListFilterTop(df.FilterSet):
    title = df.CharFilter(
        lookup_expr="icontains",
        widget=forms.TextInput(attrs={"placeholder": _("Search by title")}),
    )

    # status = df.ChoiceFilter(
    #     field_name="status",
    #     lookup_expr="exact",
    #     choices=Dataset.STATUS_CHOICES.choices,
    #     widget=forms.Select,
    #     empty_label=_("Project status"),
    # )

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


class DatasetFilter(ListFilterTop):
    # tags = df.MultipleChoiceFilter(
    #     label="Dataset Has",
    #     field_name="tags",
    #     lookup_expr="icontains",
    #     choices=HAS_TAGS,
    #     widget=SelectizeMultiple(),
    # )
    keywords = df.ModelMultipleChoiceFilter(
        queryset=Tag.objects.all(),
        widget=SelectizeMultiple(),
    )

    class Meta:
        model = Dataset
        fields = ["title", "o", "license", "keywords"]
