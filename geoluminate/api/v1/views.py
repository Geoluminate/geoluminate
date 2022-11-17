from rest_framework import viewsets
from geoluminate.api.v1.serializers import CoreSerializer
from rest_framework_gis.filters import DistanceToPointFilter
# from geoluminate.api.utils import DistanceToPointOrderingFilter
from geoluminate.rest_framework.utils import DjangoFilterBackend
from rest_framework.response import Response
from rest_access_policy.access_view_set_mixin import AccessViewSetMixin
from geoluminate.access_policies import CoreAccessPolicy
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly
from geoluminate.utils import DATABASE
from django.apps import apps
from .serializers import GeoFeatureSerializer
from django.utils.translation import gettext_lazy as _
from geoluminate.utils import DATABASE
from rest_framework.views import get_view_name
from rest_framework_datatables_editor.filters import DatatablesFilterBackend


class CoreViewSet(AccessViewSetMixin, viewsets.ModelViewSet):
    __doc__ = f"Endpoint to request a set of {DATABASE._meta.verbose_name} data."

    access_policy = CoreAccessPolicy
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly, ]
    queryset = DATABASE.objects.all().prefetch_related('references')
    serializer_class = CoreSerializer
    distance_filter_field = 'geom'
    distance_ordering_filter_field = 'geom'
    filterset_fields = ['references', ]
    filter_backends = (
        DatatablesFilterBackend,
        # DistanceToPointOrderingFilter,
        DistanceToPointFilter, DjangoFilterBackend
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__class__.__name__ = DATABASE._meta.verbose_name

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
        if getattr(self.request, 'accepted_renderer'):
            return self.request.accepted_renderer.format == 'geojson'
