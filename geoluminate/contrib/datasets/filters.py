import django_filters as df
from django import forms
from django.forms import widgets
from django_select2.forms import Select2MultipleWidget
from taggit.models import Tag

from geoluminate.contrib.core.choices import HAS_TAGS, NEEDS_TAGS

from .models import Dataset


class DatasetFilter(df.FilterSet):
    title = df.CharFilter(
        lookup_expr="icontains",
        widget=forms.TextInput(attrs={"placeholder": "Find a dataset..."}),
    )
    # tags = df.MultipleChoiceFilter(choices=Dataset.DISCOVERY_TAGS, widget=widgets.CheckboxSelectMultiple)

    # tags = df.MultipleChoiceFilter(required=False, choices=Dataset.DISCOVERY_TAGS, widget=widgets.Select)
    tags = df.MultipleChoiceFilter(
        label="Dataset Has",
        field_name="tags",
        lookup_expr="icontains",
        choices=HAS_TAGS,
        widget=forms.SelectMultiple(attrs={"size": len(HAS_TAGS)}),
    )
    keywords = df.ModelMultipleChoiceFilter(queryset=Tag.objects.all(), widget=Select2MultipleWidget)

    class Meta:
        model = Dataset
        fields = ["title", "keywords", "tags"]


class ReviewFilter(df.FilterSet):
    class Meta:
        model = Dataset
        fields = ["title"]
        # model = Review
        # fields = ["submitted", "accepted"]
