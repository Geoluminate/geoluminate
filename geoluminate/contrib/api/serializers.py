from parler_rest.serializers import TranslatableModelSerializer, TranslatedFieldsField
from rest_flex_fields.serializers import FlexFieldsSerializerMixin
from rest_framework import serializers
from rest_framework.fields import Field as Field
from rest_framework.serializers import HyperlinkedIdentityField, HyperlinkedModelSerializer, ModelSerializer

from geoluminate.contrib.generic.models import Date
from geoluminate.contrib.identity.models import Authority, Database
from geoluminate.models import Dataset, Project, Sample

from .utils import BaseSerializerMixin


class DescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Date
        fields = ["type", "value"]


class DateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Date
        fields = ["type", "value"]


class ProjectSerializer(FlexFieldsSerializerMixin, ModelSerializer):
    web = HyperlinkedIdentityField(view_name="project-detail")
    dates = DateSerializer(many=True)
    # descriptions = serializers

    class Meta:
        model = Project
        depth = 1
        exclude = ["visibility", "options"]
        # fields = ["web", "name", "created", "modified", "dates", "datasets"]
        expandable_fields = {
            "dates": (DateSerializer, {"many": True}),
            "datasets": (
                "geoluminate.contrib.api.serializers.DatasetSerializer",
                {"many": True},
            ),
        }


class ProjectAPISerializer(BaseSerializerMixin, ProjectSerializer, HyperlinkedModelSerializer):
    pass


class DatasetSerializer(BaseSerializerMixin, HyperlinkedModelSerializer):
    web = HyperlinkedIdentityField(view_name="dataset-detail")
    dates = DateSerializer(many=True)

    # sample_types = serializers.SerializerMethodField()
    # sample_count = serializers.SerializerMethodField()
    license = serializers.StringRelatedField()

    class Meta:
        model = Dataset
        exclude = ["visibility"]
        expandable_fields = {"project": ProjectSerializer}

    def get_sample_types(self, obj):
        return obj.sample_types


class SampleSerializer(FlexFieldsSerializerMixin, BaseSerializerMixin, HyperlinkedModelSerializer):
    web = HyperlinkedIdentityField(view_name="sample-detail")

    class Meta:
        model = Sample
        fields = ["name", "depth", "web"]


class MeasurementSerializer(BaseSerializerMixin, serializers.ModelSerializer):
    sample = SampleSerializer(
        fields=[
            "type",
            "name",
            "details",
            "parent",
            "dataset",
        ]
    )

    class Meta:
        fields = "__all__"
        # extra_kwargs = {
        #     "details": {"lookup_field": "pk"},
        #     "sample": {"lookup_field": "pk"},
        # }


class DatabaseSerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=Database)
    # image = serializers.ImageField()

    class Meta:
        model = Database
        exclude = ["id"]


class AuthoritySerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=Authority)

    class Meta:
        model = Authority
        exclude = ["id"]


class IdentitySerializer(serializers.Serializer):
    database = DatabaseSerializer()
    authority = AuthoritySerializer()
