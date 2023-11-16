from django.db.models.query import QuerySet
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.serializers import BaseSerializer
from rest_framework.viewsets import ReadOnlyModelViewSet

from geoluminate.api.utils import NestedViewset, api_doc

from .models import Sample
from .serializers import SampleGeojsonSerializer, SampleSerializer


@extend_schema_view(
    list=extend_schema(description=api_doc(Sample, "list")),
)
class SampleViewset(ReadOnlyModelViewSet):
    lookup_field = "uuid"
    serializer_class = SampleSerializer
    geojson_serializer = SampleGeojsonSerializer

    queryset = (
        Sample.objects.prefetch_related("contributors", "descriptions", "key_dates", "keywords")
        .select_related("dataset", "dataset__project")
        .all()
    )


class NestedSamples(NestedViewset, SampleViewset):
    """Adds the NestedViewSetMixin to the SampleViewset to make sure that the queryset on nested routes is correctly filtered by the parent lookup fields."""

    # pagination_class = None
    parent_lookup_kwargs = {
        "dataset_uuid": "dataset__uuid",
    }
