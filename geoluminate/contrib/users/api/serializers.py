from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_nested.relations import NestedHyperlinkedRelatedField
from rest_framework_nested.serializers import NestedHyperlinkedModelSerializer

from geoluminate.contrib.contributors.models import Contributor


class ProfileSerializer(NestedHyperlinkedModelSerializer):
    web_url = serializers.HyperlinkedIdentityField(view_name="contributor:detail")

    class Meta:
        model = Contributor
        fields = ["url", "web_url", "name"]
