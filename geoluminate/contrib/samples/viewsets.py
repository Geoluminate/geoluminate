from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.viewsets import ReadOnlyModelViewSet

from geoluminate.api.utils import NestedViewset, api_doc

from .models import BaseSample
from .serializers import SampleGeojsonSerializer, SampleSerializer


@extend_schema_view(
    list=extend_schema(description=api_doc(BaseSample, "list")),
)
class SampleViewset(ReadOnlyModelViewSet):
    serializer_class = SampleSerializer
    geojson_serializer = SampleGeojsonSerializer

    queryset = (
        BaseSample.objects.prefetch_related("contributors", "descriptions", "keywords")
        .select_related("dataset", "dataset__project")
        .all()
    )

    @method_decorator(cache_page(60 * 15))  # Cache for 15 minutes
    def list(self, request, *args, **kwargs):
        import time

        now = time.time()
        x = super().list(request, *args, **kwargs)
        print(time.time() - now)
        return x


class NestedSamples(NestedViewset, SampleViewset):
    """Adds the NestedViewSetMixin to the SampleViewset to make sure that the queryset on nested routes is correctly filtered by the parent lookup fields."""

    # pagination_class = None
    parent_lookup_kwargs = {
        "dataset_uuid": "dataset__uuid",
    }
