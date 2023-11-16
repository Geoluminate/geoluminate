from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework_nested.viewsets import NestedViewSetMixin

from geoluminate.contrib.datasets.viewsets import DatasetViewset, NestedDatasets
from geoluminate.contrib.projects.viewsets import NestedProjects, ProjectViewset
from geoluminate.contrib.samples.viewsets import NestedSamples, SampleViewset

from . import serializers


def MeasurementViewset(model):
    class MeasurementViewset(ReadOnlyModelViewSet):
        queryset = model.objects.all()
        serializer_class = serializers.MeasurementSerializer

        def get_serializer_class(self):
            serializer = self.serializer_class
            serializer.Meta.model = self.queryset.model
            return serializer

    return MeasurementViewset


__all__ = [
    "ProjectViewset",
    "NestedProjects",
    "DatasetViewset",
    "NestedDatasets",
    "SampleViewset",
    "NestedSamples",
    "MeasurementViewset",
]
