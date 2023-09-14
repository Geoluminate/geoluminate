import django_filters as df
from django.forms import widgets
from taggit.models import Tag

from . import models


# create a filter for the Project model that filters on title, tags, and status
class ProjectFilter(df.FilterSet):
    status = df.MultipleChoiceFilter(
        choices=models.Project.STATUS_CHOICES.choices, widget=widgets.CheckboxSelectMultiple
    )

    class Meta:
        model = models.Project
        fields = [
            "status",
            "tags",
        ]


class DatasetFilter(df.FilterSet):
    keywords = df.ModelMultipleChoiceFilter(queryset=Tag.objects.all(), widget=widgets.CheckboxSelectMultiple)

    class Meta:
        model = models.Dataset
        fields = [
            "keywords",
        ]
