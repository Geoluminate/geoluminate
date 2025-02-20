# from django.views.decorators.vary import vary_on_cookie, vary_on_headers
from django.views.generic import TemplateView

# import GenericAPIView from rest_framework.generics
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_pandas import PandasView

from fairdm.contrib.identity.models import Authority, Database
from fairdm.registry import registry

from .serializers import AuthoritySerializer, DatabaseSerializer


class DatasetSamplesView(PandasView):
    """Returns a list of all samples associated with a dataset. This view is intended to be used in conjunction with the /api/v1/dataset/{pk}/samples/ endpoint to provide a more detailed view of the samples associated with a dataset."""

    def get(self, request, *args, **kwargs):
        return Response({})


class TOSView(TemplateView):
    template_name = "fairdm/pages/api/tos.html"


class MeasurementMetadataView(GenericAPIView):
    """Returns metadata that specificly describes each type of meaurement collected within this database. This is supplemental to the OpenAPI schema available at /api/v1/schema/."""

    def get(self, request, *args, **kwargs):
        return Response({})


class IdentitityAPIView(APIView):
    """Metadata regarding the the underlying database and governing authority that is responsible for the data within this API and web portal."""

    # @method_decorator(cache_page(60 * 60 * 2))
    def get(self, request, *args, **kwargs):
        context = {
            "database": DatabaseSerializer(Database.get_solo(), context={"request": request}).data,
            "authority": AuthoritySerializer(Authority.get_solo(), context={"request": request}).data,
            "samples": registry.samples,
            "measurements": registry.measurements,
        }
        return Response(context)
