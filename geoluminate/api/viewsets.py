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
    """A viewset mixin that allows both nested and base API routes to be processed by the same viewset. Default lookup is uuid."""

    lookup_field = "uuid"

    def get_queryset(self):
        if self.is_nested():
            return super().get_queryset()
        return self.queryset

    def get_serializer_class(self):
        if renderer := getattr(self.request, "accepted_renderer", None):
            if renderer.format == "geojson":
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
