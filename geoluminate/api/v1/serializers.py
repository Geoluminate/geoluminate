from rest_framework import serializers

from geoluminate.api.serializers import BaseSerializerMixin
from geoluminate.contrib.datasets.serializers import DatasetSerializer
from geoluminate.contrib.projects.serializers import ProjectSerializer
from geoluminate.contrib.samples.serializers import SampleSerializer


class MeasurementSerializer(BaseSerializerMixin, serializers.ModelSerializer):
    sample = SampleSerializer(
        fields=[
            "type",
            "title",
            "details",
            "parent",
            "dataset",
        ]
    )

    class Meta:
        fields = "__all__"
        # extra_kwargs = {
        #     "details": {"lookup_field": "pk"},
        #     "sample": {"lookup_field": "pk"},
        # }


__all__ = [
    "ProjectSerializer",
    "DatasetSerializer",
    "SampleSerializer",
    "MeasurementSerializer",
]
