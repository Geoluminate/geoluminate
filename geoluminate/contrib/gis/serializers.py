from rest_framework import serializers
from rest_framework.fields import Field as Field

from geoluminate.api.serializers import BaseSerializerMixin

from .models import Location


class LocationSerializer(BaseSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = Location
        exclude = ["id", "created", "elevation"]
