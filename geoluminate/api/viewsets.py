from rest_access_policy.access_view_set_mixin import AccessViewSetMixin
from rest_framework import viewsets
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly
from rest_framework_nested.viewsets import NestedViewSetMixin

from geoluminate.api.access_policies import CoreAccessPolicy


class BaseViewSet(AccessViewSetMixin, viewsets.ModelViewSet):
    access_policy = CoreAccessPolicy
    permission_classes = [
        DjangoModelPermissionsOrAnonReadOnly,
    ]


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
