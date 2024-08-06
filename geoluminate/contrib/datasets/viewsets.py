from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.viewsets import ReadOnlyModelViewSet

from geoluminate.api.utils import NestedViewset, api_doc

from .models import Dataset
from .serializers import DatasetSerializer


@extend_schema_view(
    list=extend_schema(description=api_doc(Dataset, "list")),
)
class DatasetViewset(ReadOnlyModelViewSet):
    serializer_class = DatasetSerializer
    queryset = Dataset.objects.prefetch_related("contributors", "descriptions", "keywords").all()


class NestedDatasets(NestedViewset, DatasetViewset):
    """Adds the NestedViewSetMixin to the DatasetViewset to make sure that the queryset on nested routes is correctly filtered by the parent lookup fields."""

    pass
