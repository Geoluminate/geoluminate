from rest_framework.fields import Field as Field
from rest_framework.serializers import HyperlinkedModelSerializer
from rest_framework_gis.serializers import (
    GeoFeatureModelSerializer,
    GeometrySerializerMethodField,
)

from geoluminate.db.models import Dataset, Location, Project, Sample

from . import base


class ProjectSerializer(base.ProjectSerializer, HyperlinkedModelSerializer):
    class Meta:
        model = Project
        exclude = ["options", "visibility"]


class DatasetSerializer(base.DatasetSerializer, HyperlinkedModelSerializer):
    class Meta:
        model = Dataset
        exclude = ["options", "visibility"]

    def get_bbox(self, obj):
        return obj.bbox()


class LocationSerializer(base.LocationSerializer, HyperlinkedModelSerializer):
    class Meta:
        model = Location
        exclude = ["created"]


class SampleSerializer(base.SampleSerializer, HyperlinkedModelSerializer):
    class Meta:
        model = Sample
        exclude = ["created"]


class MeasurementSerializer(base.MeasurementSerializer, HyperlinkedModelSerializer):
    class Meta:
        fields = "__all__"


class SampleGeojsonSerializer(GeoFeatureModelSerializer):
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
        extra_kwargs = {"details": {"lookup_field": "uuid"}, "dataset": {"lookup_field": "uuid"}}


class LocationGeojsonSerializer(LocationSerializer, GeoFeatureModelSerializer):
    class Meta(LocationSerializer.Meta):
        geo_field = "point"
        id_field = "uuid"
