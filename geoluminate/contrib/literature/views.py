import datatables

# from crossref.models import Work
# from crossref.views import WorksByYearMixin
from datatables.views import DatatablesReadOnlyView
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView
from django_filters.views import FilterView
from literature.models import Author, Literature

from geoluminate.utils import get_filter_params

from .api.serialize import AuthorSerializer
from .filters import PublicationFilter


class PublicationList(FilterView):
    model = Literature
    template_name = "literature/list.html"
    partial_template = "literature/partials/publication_list.html"
    publication_template = "crossref/publication.html"

    paginate_by = 50
    filterset_class = PublicationFilter

    def get_template_names(self):
        if self.request.htmx:
            return [self.partial_template]
        else:
            return [self.template_name]  # The actual form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.filterset_class:
            context["parameters"] = get_filter_params(self.request.GET.copy())
        context["pub_template"] = self.publication_template
        return context


class PublicationDetail(DetailView):
    template_name = "literature/details.html"
    model = Literature


@datatables.register
class AuthorList(DatatablesReadOnlyView):
    model = Author
    queryset = Author.objects.with_work_counts().filter(as_lead__gt=0)
    search_fields = ("family", "given")
    fields = [
        "get_absolute_url",
        "family",
        "given",
        "ORCID",
        "id",
        "as_lead",
        "as_supporting",
    ]
    ordering_fields = ["-as_lead", "-as_supporting"]
    base_serializer = AuthorSerializer
    invisible_fields = [
        "id",
    ]
    hyperlink_fields = [
        "get_absolute_url",
    ]
    datatables = dict(
        dom="<'#tableToolBar' if> <'#tableBody' tr>",
        rowId="id",
        scrollY="100vh",
        deferRender=True,
        scroller=True,
    )


class AuthorDetail(DetailView):
    template_name = "main/author_detail.html"
    model = Author


class HTMXDetail(DetailView):
    """Shortcut for calling Detail view with model=Publication from `urls.py`."""

    model = Literature

    def get_template_names(self):
        return [f"literature/hx/{self.template_name}"]


HX = HTMXDetail.as_view