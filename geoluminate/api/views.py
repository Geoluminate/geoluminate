from django.views.generic import TemplateView

# import GenericAPIView from rest_framework.generics
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response


class TOSView(TemplateView):
    template_name = "geoluminate/generic/api/tos.html"


class MeasurementMetadataView(GenericAPIView):
    """Returns metadata that specificly describes each type of meaurement collected within this database. This is supplemental to the OpenAPI schema available at /api/v1/schema/."""

    def get(self, request, *args, **kwargs):
        return Response({})
