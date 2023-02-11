from rest_framework import serializers
from geoluminate.gis.serializers import FeatureSerializer
from django.apps import apps
from geoluminate.utils import DATABASE


class GeoFeatureSerializer(FeatureSerializer):

    class Meta:
        model = DATABASE
        geo_field = 'geom'
        exclude = ['references', 'last_modified']


class CoreSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.CharField()  # required for datatables
    lat = serializers.SerializerMethodField()
    lon = serializers.SerializerMethodField()

    def get_lat(self, obj):
        return obj.geom.coords[1]

    def get_lon(self, obj):
        return obj.geom.coords[0]

    class Meta:
        model = DATABASE
        datatables_always_serialize = ('id',)
        exclude = ['date_added', 'geom']
