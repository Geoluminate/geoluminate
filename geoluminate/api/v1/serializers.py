from rest_framework import serializers

from geoluminate.api.serializers import BaseSerializerMixin
from geoluminate.contrib.datasets.serializers import DatasetSerializer
from geoluminate.contrib.projects.serializers import ProjectSerializer
from geoluminate.contrib.samples.serializers import SampleSerializer


class MetaMixin:
    # any field that defines a hyperlink to a model containing a uuid field must be specified here
    extra_kwargs = {
        "details": {"lookup_field": "uuid"},
        "project": {"lookup_field": "uuid"},
        "dataset": {"lookup_field": "uuid"},
        "sample": {"lookup_field": "uuid"},
        "parent": {"lookup_field": "uuid"},
        "location": {"lookup_field": "uuid"},
    }


class MeasurementSerializer(BaseSerializerMixin, serializers.ModelSerializer):
    sample = SampleSerializer(
        fields=[
            "type",
            "title",
            "location",
            "details",
            "parent",
            "dataset",
        ]
    )
    # sample = SampleSerializer()

    class Meta(MetaMixin):
        fields = "__all__"
        extra_kwargs = {
            "details": {"lookup_field": "uuid"},
            "sample": {"lookup_field": "uuid"},
        }


__all__ = [
    "ProjectSerializer",
    "DatasetSerializer",
    "SampleSerializer",
    "MeasurementSerializer",
]
