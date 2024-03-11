from rest_framework.fields import Field as Field
from rest_framework_gis.serializers import (
    GeoFeatureModelSerializer,
    GeometrySerializerMethodField,
)
from rest_framework_nested.relations import NestedHyperlinkedIdentityField
from rest_framework_nested.serializers import NestedHyperlinkedModelSerializer
from taggit.serializers import TagListSerializerField

from geoluminate.models import Dataset, Location, Project, Sample

from ...serializers import BaseSerializerMixin
from . import base


class BaseNestedSerializer(BaseSerializerMixin, NestedHyperlinkedModelSerializer):
    pass


class NestedProjectSerializer(base.ProjectSerializer, BaseNestedSerializer):
    datasets = NestedHyperlinkedIdentityField(
        view_name="dataset-list",
        lookup_field="uuid",
        lookup_url_kwarg="project_uuid",
    )

    tags = TagListSerializerField()

    class Meta:
        model = Project
        exclude = ["options", "visibility"]
        extra_kwargs = {"details": {"lookup_field": "uuid"}}


class NestedDatasetSerializer(BaseNestedSerializer):
    parent_lookup_kwargs = {
        "project_uuid": "project__uuid",
    }
    samples = NestedHyperlinkedIdentityField(
        view_name="sample-list",
        lookup_field="uuid",
        lookup_url_kwarg="dataset_uuid",
    )

    class Meta:
        model = Dataset
        exclude = ["options", "visibility"]
        extra_kwargs = {
            "details": {"lookup_field": "uuid"},
            "project": {"lookup_field": "uuid"},
        }


class NestedLocationSerializer(BaseNestedSerializer):
    parent_lookup_kwargs = {
        "dataset_uuid": "dataset__uuid",
    }

    class Meta:
        model = Location
        exclude = ["created"]

        # extra_kwargs = {"url": {"lookup_field": "uuid"}}
        # extra_kwargs = {"details": {"lookup_field": "uuid"}, "samples": {"lookup_field": "uuid"}}
        extra_kwargs = {
            "details": {"lookup_field": "uuid"},
            "dataset": {"lookup_field": "uuid"},
        }


class NestedSampleSerializer(BaseNestedSerializer):
    parent_lookup_kwargs = {
        "dataset_uuid": "dataset__uuid",
    }
    location = NestedLocationSerializer(fields=["name", "point"])

    class Meta:
        model = Sample
        # fields = "__all__"
        exclude = ["created"]
        extra_kwargs = {
            "details": {"lookup_field": "uuid"},
            "dataset": {"lookup_field": "uuid"},
        }


class NestedMeasurementSerializer(BaseNestedSerializer):
    sample = NestedSampleSerializer(
        fields=[
            "type",
            "title",
            "location",
            "details",
            "parent",
            "dataset",
        ]
    )

    class Meta:
        fields = "__all__"
        extra_kwargs = {
            "details": {"lookup_field": "uuid"},
            "sample": {"lookup_field": "uuid"},
        }


class NestedSampleGeojsonSerializer(GeoFeatureModelSerializer):
    parent_lookup_kwargs = {
        "dataset_uuid": "dataset__uuid",
    }
    geom = GeometrySerializerMethodField()

    def get_geom(self, obj):
        return obj.location.point

    class Meta:
        model = Sample
        geo_field = "geom"
        id_field = "uuid"
        fields = ["uuid", "type", "title", "geom"]
        extra_kwargs = {
            "details": {"lookup_field": "uuid"},
            "dataset": {"lookup_field": "uuid"},
        }


class NestedLocationGeojsonSerializer(NestedLocationSerializer, GeoFeatureModelSerializer):
    class Meta(NestedLocationSerializer.Meta):
        geo_field = "point"
        id_field = "uuid"
