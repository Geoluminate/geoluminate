from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_nested.relations import NestedHyperlinkedRelatedField
from rest_framework_nested.serializers import NestedHyperlinkedModelSerializer

from ..models import Contributor

User = get_user_model()


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class ProfileSerializer(NestedHyperlinkedModelSerializer):
    web_url = serializers.HyperlinkedIdentityField(view_name="community:profile")

    class Meta:
        model = Contributor
        fields = ["url", "web_url", "name"]
