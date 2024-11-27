import django_filters as df
from django.utils.translation import gettext_lazy as _
from literature.models import LiteratureItem, Tag


class LiteratureFilterset(df.FilterSet):
    o = df.OrderingFilter(
        fields=(
            ("title", "title"),
            ("issued", "issued"),
            ("created", "created"),
        ),
        field_labels={
            "title": _("Title"),
            "issued": _("Year published"),
            "created": _("Date added"),
        },
    )

    status = df.ChoiceFilter(
        field_name="review__status",
        choices=[("completed", _("Completed")), ("open", _("Open"))],
        label=_("Review status"),
    )

    title = df.CharFilter(label=_("Title"), lookup_expr="icontains")
    author = df.CharFilter(field_name="item__author", lookup_expr="icontains", label=_("Author"))
    # issued = df.NumberFilter(method="filter_issued")
    journal = df.CharFilter(field_name="item__container-title", lookup_expr="icontains", label=_("Journal"))
    doi = df.CharFilter(field_name="item__DOI", lookup_expr="icontains", label=_("DOI"))
    publisher = df.CharFilter(field_name="item__publisher", lookup_expr="icontains", label=_("Publisher"))
    keywords = df.ModelMultipleChoiceFilter(to_field_name="name", queryset=Tag.objects.all(), label=_("Keywords"))

    class Meta:
        model = LiteratureItem
        fields = [
            "o",
            "status",
            "type",
            "doi",
            "title",
            "author",
        ]

    # def filter_issued(self, queryset, name, value):
    # this doesn't work because django-partial-date doesn't subclass django's DateField...
    # return queryset.filter(issued__year=value)
