from rest_framework.fields import Field as Field
from rest_framework.serializers import HyperlinkedModelSerializer
from rest_framework_nested.serializers import NestedHyperlinkedModelSerializer

from geoluminate.api.serializers import BaseSerializerMixin

from .models import Dataset


class DatasetSerializer(BaseSerializerMixin, HyperlinkedModelSerializer):
    class Meta:
        model = Dataset
        exclude = ["options", "visibility"]
        extra_kwargs = {
            "details": {"lookup_field": "uuid"},
            "project": {"lookup_field": "uuid"},
            "dataset": {"lookup_field": "uuid"},
            "sample": {"lookup_field": "uuid"},
            "parent": {"lookup_field": "uuid"},
            "location": {"lookup_field": "uuid"},
        }
