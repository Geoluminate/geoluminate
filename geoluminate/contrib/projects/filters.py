import django_filters as df
from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Project


class ListFilterTop(df.FilterSet):
    title = df.CharFilter(
        lookup_expr="icontains",
        widget=forms.TextInput(attrs={"placeholder": "Find a project..."}),
    )

    status = df.ChoiceFilter(
        field_name="status",
        lookup_expr="exact",
        choices=Project.STATUS_CHOICES.choices,
        widget=forms.Select,
        empty_label=_("Project status"),
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
        # initial="-created",
    )


class ProjectFilter(ListFilterTop):
    # has_tags = df.MultipleChoiceFilter(
    #     label="Project Has",
    #     field_name="tags",
    #     lookup_expr="icontains",
    #     choices=HAS_TAGS,
    #     widget=SelectizeMultiple(),
    #     # widget=forms.SelectMultiple(attrs={"size": len(HAS_TAGS)}),
    # )
    # needs_tags = df.MultipleChoiceFilter(
    #     label="Project Needs",
    #     field_name="tags",
    #     lookup_expr="icontains",
    #     required=False,
    #     choices=NEEDS_TAGS,
    #     widget=SelectizeMultiple(),
    #     # widget=forms.SelectMultiple(attrs={"size": len(NEEDS_TAGS)}),
    # )

    class Meta:
        model = Project
        fields = ["title", "status", "o", "visibility", "o"]
