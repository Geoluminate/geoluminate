import django_filters as df
from django import forms
from django.utils.translation import gettext_lazy as _


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
