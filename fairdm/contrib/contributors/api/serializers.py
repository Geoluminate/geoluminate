from rest_framework.serializers import ModelSerializer
from rest_framework_nested.serializers import NestedHyperlinkedModelSerializer
from rest_polymorphic.serializers import PolymorphicSerializer

from fairdm.contrib.contributors.models import Contributor, ContributorIdentifier, Organization, Person


class IdentifierSerializer(ModelSerializer):
    class Meta:
        model = ContributorIdentifier
        fields = ["type", "value"]


class PersonSerializer(NestedHyperlinkedModelSerializer):
    identifiers = IdentifierSerializer(many=True)

    class Meta:
        model = Person
        fields = ["id", "name", "first_name", "last_name", "identifiers"]


class OrganizationSerializer(NestedHyperlinkedModelSerializer):
    identifiers = IdentifierSerializer(many=True)

    class Meta:
        model = Organization
        fields = ["id", "name", "identifiers"]


class ContributorSerializer(NestedHyperlinkedModelSerializer):
    # web_url = serializers.HyperlinkedIdentityField(view_name="contributor-detail")
    identifiers = IdentifierSerializer(many=True)

    class Meta:
        model = Contributor
        fields = ["id", "name", "identifiers"]
        # fields = ["url", "name"]


class ContributorPolymorphicSerializer(PolymorphicSerializer):
    resource_type_field_name = "type"
    model_serializer_mapping = {
        Contributor: ContributorSerializer,
        Person: PersonSerializer,
        Organization: OrganizationSerializer,
    }

    def to_resource_type(self, model_or_instance):
        return model_or_instance._meta.object_name.lower()
