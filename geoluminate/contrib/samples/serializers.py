from rest_framework import serializers
from rest_framework.fields import Field as Field
from rest_framework_gis.serializers import GeoFeatureModelSerializer, GeometrySerializerMethodField
from rest_framework_nested.serializers import NestedHyperlinkedModelSerializer

from geoluminate.api.serializers import BaseSerializerMixin

from .models import BaseSample, Location


class LocationSerializer(BaseSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = Location
        exclude = ["id", "created", "elevation"]


class SampleSerializer(BaseSerializerMixin, NestedHyperlinkedModelSerializer):
    location = LocationSerializer()
    absolute_url = serializers.SerializerMethodField()

    class Meta:
        model = BaseSample
        exclude = ["options"]

    def get_absolute_url(self, obj):
        return obj.get_absolute_url()


class SampleGeojsonSerializer(BaseSerializerMixin, GeoFeatureModelSerializer):
    geom = GeometrySerializerMethodField()

    def get_geom(self, obj):
        return obj.location.point

    class Meta:
        model = BaseSample
        geo_field = "geom"
        id_field = "pk"
        fields = ["pk", "feature_type", "title", "geom"]
