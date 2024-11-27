from logging import getLogger

from django.template import TemplateDoesNotExist
from django.template.loader import render_to_string
from rest_framework import viewsets
from rest_framework.renderers import BrowsableAPIRenderer
from rest_framework_nested.viewsets import NestedViewSetMixin

logger = getLogger(__name__)


class BrowsableAPIRendererWithoutForms(BrowsableAPIRenderer):
    """Renders the browsable api, but excludes the forms."""

    def get_rendered_html_form(self, data, view, method, request):
        return None

    def get_filter_form(self, data, view, request):
        return None


# class DatatablesReadOnlyModelViewSet(EditorModelMixin, viewsets.ReadOnlyModelViewSet):
#     pass


def public_api(endpoints):
    """A filter function that will exclude urls generated by this package
    from being included in any API documentation generated using
    `drf-spectacular <https://github.com/tfranzel/drf-spectacular>`_.

    You can use this function by placing it in your `SPECTACULAR_SETTINGS`
    config dictionary under `PREPROCCESSING_HOOKS`. E.g.

    .. code:: python


    "PREPROCESSING_HOOKS": [
        "datatables.spectacular.preprocessing_filter_spec"
    ],


    """
    filtered = []
    for path, path_regex, method, callback in endpoints:
        # Remove all but DRF API endpoints
        if path.startswith("/api/"):
            filtered.append((path, path_regex, method, callback))
        # filtered.append((path, path_regex, method, callback))
    return filtered


def api_doc(model, path):
    """
    Returns a rendered string of the API documentation for a given model and path.

    This function attempts to render a template with the name in the format of
    "api/docs/{model_name}_{path}.md", where {model_name} is the lowercased name
    of the model's class and {path} is the provided path argument. The template
    is rendered with a context that includes the model instance and the geoluminate
    settings.

    If the template does not exist, a warning is logged and an empty string is returned.

    Args:
        model (django.db.models.Model): The model instance for which to render the API documentation.
        path (str): The path to append to the template name.

    Returns:
        str: The rendered template as a string, or an empty string if the template does not exist.

    Example:
        Let's say we have a model named 'Book' and we want to get the API documentation for it.
        We can do it like this:

        >>> from myapp.models import Book
        >>> book = Book.objects.first()
        >>> api_doc(book, "detail")
        This will attempt to render the template "api/docs/book_detail.md".
        If the template exists, it will return the rendered template as a string.
        If the template does not exist, it will log a warning and return an empty string.
    """
    try:
        template = f"api/docs/{model._meta.model_name.lower()}_{path}.md"
        return render_to_string(template, context={"model": model})
    except TemplateDoesNotExist:
        logger.warning(f"Template {template} does not exist.")
    return ""


class BaseSerializerMixin:
    default_namespace = "api"

    def build_url_field(self, field_name, model_class):
        field_class, field_kwargs = super().build_url_field(field_name, model_class)
        field_kwargs["view_name"] = f"{self.default_namespace}:{field_kwargs['view_name']}"
        return field_class, field_kwargs

    def build_relational_field(self, field_name, relation_info):
        field_class, field_kwargs = super().build_relational_field(field_name, relation_info)
        field_kwargs["view_name"] = f"{self.default_namespace}:{field_kwargs['view_name']}"
        return field_class, field_kwargs

    def get_field_names(self, declared_fields, info):
        """Returns a case-insensitive, sorted list of field names."""
        fields = super().get_field_names(declared_fields, info)
        return sorted(fields, key=str.casefold)


class NestedViewset(NestedViewSetMixin):
    """Subclass the default NestedViewSetMixin to make prevent a key error when generatin the schema with DRF Spectacular."""

    def initialize_request(self, request, *args, **kwargs):
        if getattr(self, "swagger_fake_view", False):
            return request
        return super().initialize_request(request, *args, **kwargs)

    def get_serializer_class(self):
        if hasattr(self, "request"):  # noqa: SIM102
            if (renderer := getattr(self.request, "accepted_renderer", None)) and renderer.format == "geojson":
                return self.geojson_serializer
        return super().get_serializer_class()

    def paginate_queryset(self, queryset, view=None):
        if (renderer := getattr(self.request, "accepted_renderer", None)) and renderer.format == "geojson":
            return None
        return self.paginator.paginate_queryset(queryset, self.request, view=self)


class ViewsetMixin(NestedViewSetMixin, viewsets.ReadOnlyModelViewSet):
    """A viewset mixin that allows both nested and base API routes to be processed by the same viewset."""

    def get_queryset(self):
        if self.is_nested():
            return super().get_queryset()
        return self.queryset

    def get_serializer_class(self):
        if (renderer := getattr(self.request, "accepted_renderer", None)) and renderer.format == "geojson":
            if self.is_nested():
                self.pagination_class = None
            return self.geojson_serializer
        return super().get_serializer_class()

    def initialize_request(self, request, *args, **kwargs):
        if self.is_nested():
            return super().initialize_request(request, *args, **kwargs)
        return viewsets.ReadOnlyModelViewSet.initialize_request(self, request, *args, **kwargs)

    def is_nested(self):
        """Returns true if the following conditions are met:

        a) multiple kwargs are present in the url
        b) a single kwarg is present in the url and that kwargs is the lookup field

        """
        return len(self.kwargs) > 1 or self.kwargs.get(self.lookup_field, False)