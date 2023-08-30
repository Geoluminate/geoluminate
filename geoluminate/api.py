# import improperlyconfigured
from django.core.exceptions import ImproperlyConfigured

# import redirect
from django.shortcuts import redirect
from drf_auto_endpoint.endpoints import Endpoint
from drf_auto_endpoint.router import EndpointRouter
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

API = EndpointRouter()


class BaseViewSet(ReadOnlyModelViewSet):
    """Base viewset for all endpoints."""

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        if request.accepted_renderer.format == "html":
            # return Response({"data": response.data}, template_name=self.get_template())
            return redirect(self.get_object().get_absolute_url())
        return response

    def get_template(self):
        """Return the template for this endpoint."""
        return f"api/{self.endpoint.singular_model_name}.html"

    def get_queryset(self):
        """Return the queryset for this endpoint."""
        return self.endpoint.model.objects.all()


class Endpoint(Endpoint):
    # base_serializer = HyperlinkedModelSerializer
    include_str = False
    read_only = True
    base_viewset = BaseViewSet


def check_filter_fields_are_indexed(endpoint):
    """Check that all filter fields are indexed. If not, raise an error."""
    model = endpoint.model
    for field in endpoint.filter_fields:
        if not model._meta.get_field(field).db_index:
            raise ImproperlyConfigured(
                f"You have specified '{field}' in filter_fields on the API endpoint "
                f"{endpoint} but that field has no database index. This will likely cause "
                "performance issues with large databases. Please add an index to this "
                "field or remove it from the filter_fields attribute."
            )


def check_search_fields_are_indexed(endpoint):
    """Check that all filter fields are indexed. If not, raise an error."""
    model = endpoint.model
    for field in endpoint.search_fields:
        if not model._meta.get_field(field).db_index:
            raise ImproperlyConfigured(
                f"You have specified '{field}' in search_fields on the API endpoint "
                f"{endpoint} but that field has no database index. This will likely cause "
                "performance issues with large databases. Please add an index to this "
                "field or remove it from the search_fields attribute."
            )


def register(wrapped=None, **kwargs):
    def _endpoint_wrapper(endpoint_class):
        if endpoint_class.filter_fields:
            # Check that all filter fields are indexed
            check_search_fields_are_indexed(endpoint_class)
        if endpoint_class.search_fields:
            # Check that all search fields are indexed
            check_filter_fields_are_indexed(endpoint_class)
        API.register(endpoint=endpoint_class(base_viewset=BaseViewSet), **kwargs)
        return endpoint_class

    if wrapped is not None:
        return _endpoint_wrapper(wrapped)
    return _endpoint_wrapper
