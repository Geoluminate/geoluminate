from rest_framework import serializers
from rest_framework.fields import Field as Field
from rest_framework_nested.serializers import NestedHyperlinkedModelSerializer

from geoluminate.api.serializers import BaseSerializerMixin

from .models import Sample


class SampleSerializer(BaseSerializerMixin, NestedHyperlinkedModelSerializer):
    absolute_url = serializers.SerializerMethodField()

    class Meta:
        model = Sample
        exclude = ["options"]

    def get_absolute_url(self, obj):
        return obj.get_absolute_url()
