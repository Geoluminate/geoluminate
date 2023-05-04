from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_access_policy.access_view_set_mixin import AccessViewSetMixin
from rest_framework import viewsets
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly
from rest_framework.response import Response
from rest_framework_gis.filters import DistanceToPointFilter

from geoluminate.contrib.api.access_policies import CoreAccessPolicy
from geoluminate.contrib.api.v1.serializers import CoreSerializer, SiteSerializer
from geoluminate.models import GeoluminateSite

# from geoluminate.contrib.api.utils import DistanceToPointOrderingFilter
from geoluminate.utils.drf import DjangoFilterBackend

from .serializers import GeoFeatureSerializer


class SiteViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = SiteSerializer

    # Don't try to set queryset as a class attribute, it will break when building docs because it wants to access ContentTypes for some reason
    def get_queryset(self):
        return GeoluminateSite.objects.all()


class DataViewSet(AccessViewSetMixin, viewsets.ModelViewSet):
    # __doc__ = "Endpoint to request a set of {} data.".format(
    #     settings.GEOLUMINATE['database']['name']
    # )
    access_policy = CoreAccessPolicy
    permission_classes = [
        DjangoModelPermissionsOrAnonReadOnly,
    ]
    # queryset = DATABASE.objects.all().prefetch_related("references")
    serializer_class = CoreSerializer
    distance_filter_field = "geom"
    distance_ordering_filter_field = "geom"
    filterset_fields = [
        "references",
    ]
    filter_backends = (
        # DistanceToPointOrderingFilter,
        DistanceToPointFilter,
        DjangoFilterBackend,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.__class__.__name__ = DATABASE._meta.verbose_name

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
