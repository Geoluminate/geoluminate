from rest_framework_nested.serializers import NestedHyperlinkedModelSerializer

from geoluminate.contrib.contributors.models import Contributor


class ProfileSerializer(NestedHyperlinkedModelSerializer):
    # web_url = serializers.HyperlinkedIdentityField(view_name="contributor:detail")

    class Meta:
        model = Contributor
        fields = ["name"]
        # fields = ["url", "name"]
