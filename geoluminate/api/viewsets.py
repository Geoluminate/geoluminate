from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_access_policy.access_view_set_mixin import AccessViewSetMixin
from rest_framework import viewsets
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly
from rest_framework.response import Response
from rest_framework_gis.filters import DistanceToPointFilter
from rest_framework_nested.viewsets import NestedViewSetMixin

from geoluminate.api.access_policies import CoreAccessPolicy
from geoluminate.utils.drf import DjangoFilterBackend

# from .serializers import GeoFeatureSerializer
from geoluminate.utils.gis.serializers import GeoFeatureSerializer


class BaseViewSet(AccessViewSetMixin, viewsets.ModelViewSet):
    access_policy = CoreAccessPolicy
    permission_classes = [
        DjangoModelPermissionsOrAnonReadOnly,
    ]


class GeoJsonViewset(BaseViewSet):
    distance_filter_field = "point"
    distance_ordering_filter_field = "point"
    filter_backends = (
        DistanceToPointFilter,
        DjangoFilterBackend,
    )

    @method_decorator(cache_page(60 * 60 * 2))
    def list(self, request, *args, **kwargs):
        if self.is_geojson():
            qs = self.filter_queryset(self.get_queryset())
            serializer = GeoFeatureSerializer(qs, many=True)
            return Response(serializer.data)
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        """Overriding the default docstring"""
        instance = self.get_object()
        if self.is_geojson():
            instance = self.get_queryset().filter(pk=self.get_object().pk)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def is_geojson(self):
        if self.request.accepted_renderer:
            return self.request.accepted_renderer.format == "geojson"


class ViewsetMixin(NestedViewSetMixin, viewsets.ReadOnlyModelViewSet):
    """A viewset mixin that allows allows both nested and base API routes to be processed by the same viewset. Default lookup is uuid."""

    lookup_field = "uuid"

    def get_queryset(self):
        if self.is_base_viewset():
            return self.queryset
        return super().get_queryset()

    def initialize_request(self, request, *args, **kwargs):
        if self.is_base_viewset():
            return viewsets.ReadOnlyModelViewSet.initialize_request(self, request, *args, **kwargs)
        return super().initialize_request(request, *args, **kwargs)

    def is_base_viewset(self):
        """Determines if this is a base viewset (e.g. a simple list or detail view) or a nested viewset."""
        return not self.kwargs or self.kwargs.get("pk", False)
