from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_access_policy.access_view_set_mixin import AccessViewSetMixin
from rest_framework import viewsets
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly
from rest_framework.response import Response
from rest_framework_gis.filters import DistanceToPointFilter

from geoluminate.contrib.api.access_policies import CoreAccessPolicy

# from .serializers import GeoFeatureSerializer
from geoluminate.contrib.gis.serializers import GeoFeatureSerializer
from geoluminate.utils.drf import DjangoFilterBackend


class BaseViewSet(AccessViewSetMixin, viewsets.ModelViewSet):
    # __doc__ = "Endpoint to request a set of {} data.".format(
    #     settings.GEOLUMINATE['database']['name']
    # )
    access_policy = CoreAccessPolicy
    permission_classes = [
        DjangoModelPermissionsOrAnonReadOnly,
    ]


class GeoJsonViewset(BaseViewSet):
    distance_filter_field = "geom"
    distance_ordering_filter_field = "geom"
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