from rest_framework import serializers
from rest_framework.fields import Field as Field
from rest_framework_gis.serializers import (
    GeoFeatureModelSerializer,
    GeometrySerializerMethodField,
)
from rest_framework_nested.serializers import NestedHyperlinkedModelSerializer

from geoluminate.api.serializers import BaseSerializerMixin

from .models import Location, Sample


class LocationSerializer(BaseSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = Location
        exclude = ["id", "created", "elevation"]


class SampleSerializer(BaseSerializerMixin, NestedHyperlinkedModelSerializer):
    location = LocationSerializer()
    absolute_url = serializers.SerializerMethodField()

    class Meta:
        model = Sample
        exclude = ["options"]
        extra_kwargs = {
            "details": {"lookup_field": "uuid"},
            "project": {"lookup_field": "uuid"},
            "dataset": {"lookup_field": "uuid"},
            "sample": {"lookup_field": "uuid"},
            "parent": {"lookup_field": "uuid"},
            "location": {"lookup_field": "uuid"},
        }

    def get_absolute_url(self, obj):
        return obj.get_absolute_url()


class SampleGeojsonSerializer(BaseSerializerMixin, GeoFeatureModelSerializer):
    geom = GeometrySerializerMethodField()

    def get_geom(self, obj):
        return obj.location.point

    class Meta:
        model = Sample
        geo_field = "geom"
        id_field = "uuid"
        fields = ["uuid", "feature_type", "title", "geom"]
        extra_kwargs = {
            "details": {"lookup_field": "uuid"},
            "project": {"lookup_field": "uuid"},
            "dataset": {"lookup_field": "uuid"},
            "sample": {"lookup_field": "uuid"},
            "parent": {"lookup_field": "uuid"},
            "location": {"lookup_field": "uuid"},
        }
