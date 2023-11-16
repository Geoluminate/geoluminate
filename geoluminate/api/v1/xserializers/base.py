from rest_framework import serializers
from rest_framework.fields import Field as Field
from rest_framework.utils.model_meta import FieldInfo
from rest_framework_gis.serializers import (
    GeoFeatureModelSerializer,
    GeometrySerializerMethodField,
)
from rest_framework_nested.relations import NestedHyperlinkedIdentityField
from rest_framework_nested.serializers import NestedHyperlinkedModelSerializer
from taggit.serializers import TaggitSerializer, TagListSerializerField

from geoluminate.api.serializers import BaseSerializerMixin
from geoluminate.contrib.contributors.models import Contribution
from geoluminate.contrib.core.models import Description, FuzzyDate
from geoluminate.db.models import Contributor, Dataset, Location, Project, Sample


class ContributorSerializer(BaseSerializerMixin):
    class Meta:
        model = Contributor
        fields = ["name"]


class ContributionSerializer(serializers.HyperlinkedModelSerializer):
    # profile = ContributorSerializer(source="profile")

    class Meta:
        model = Contribution
        fields = ["contributor", "roles"]


class DescriptionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Description
        fields = ["type", "text"]


class FuzzyDateSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = FuzzyDate
        fields = ["type", "date"]


class ProjectSerializer(BaseSerializerMixin):
    datasets = NestedHyperlinkedIdentityField(
        view_name="dataset-list",
        lookup_field="uuid",
        lookup_url_kwarg="project_uuid",
    )
    contributors = ContributionSerializer(many=True, read_only=True)
    descriptions = DescriptionSerializer(many=True, read_only=True)
    key_dates = FuzzyDateSerializer(many=True, read_only=True)

    tags = TagListSerializerField()

    class Meta:
        model = Project
        exclude = ["options", "is_public"]
        extra_kwargs = {"details": {"lookup_field": "uuid"}}


class DatasetSerializer(BaseSerializerMixin):
    parent_lookup_kwargs = {
        "project_uuid": "project__uuid",
    }

    samples = NestedHyperlinkedIdentityField(
        view_name="sample-list",
        lookup_field="uuid",
        lookup_url_kwarg="dataset_uuid",
    )
    contributors = ContributionSerializer(many=True, read_only=True)
    descriptions = DescriptionSerializer(many=True, read_only=True)
    key_dates = FuzzyDateSerializer(many=True, read_only=True)
    keywords = TagListSerializerField()

    class Meta:
        model = Dataset
        exclude = ["options", "is_public"]
        extra_kwargs = {"details": {"lookup_field": "uuid"}, "project": {"lookup_field": "uuid"}}

    def get_bbox(self, obj):
        return obj.bbox()


class LocationSerializer(BaseSerializerMixin):
    parent_lookup_kwargs = {
        "dataset_uuid": "dataset__uuid",
    }

    class Meta:
        model = Location
        exclude = ["created"]

        # extra_kwargs = {"url": {"lookup_field": "uuid"}}
        # extra_kwargs = {"details": {"lookup_field": "uuid"}, "samples": {"lookup_field": "uuid"}}
        extra_kwargs = {"details": {"lookup_field": "uuid"}, "dataset": {"lookup_field": "uuid"}}


class SampleSerializer(BaseSerializerMixin):
    parent_lookup_kwargs = {
        "dataset_uuid": "dataset__uuid",
    }
    # location = LocationSerializer()

    class Meta:
        model = Sample
        # fields = "__all__"
        exclude = ["created"]
        extra_kwargs = {"details": {"lookup_field": "uuid"}, "dataset": {"lookup_field": "uuid"}}


class MeasurementSerializer(BaseSerializerMixin):
    # sample = SampleSerializer(
    #     fields=[
    #         "type",
    #         "title",
    #         "location",
    #         "details",
    #         "parent",
    #         "dataset",
    #     ]
    # )
    # sample = SampleSerializer()

    class Meta:
        fields = "__all__"
        extra_kwargs = {"details": {"lookup_field": "uuid"}, "sample": {"lookup_field": "uuid"}}


class SampleGeojsonSerializer(GeoFeatureModelSerializer):
    parent_lookup_kwargs = {
        "dataset_uuid": "dataset__uuid",
    }
    geom = GeometrySerializerMethodField()

    def get_geom(self, obj):
        return obj.location.point

    class Meta:
        model = Sample
        geo_field = "geom"
        id_field = "uuid"
        fields = ["uuid", "type", "title", "geom"]
        extra_kwargs = {"details": {"lookup_field": "uuid"}, "dataset": {"lookup_field": "uuid"}}


class LocationGeojsonSerializer(LocationSerializer, GeoFeatureModelSerializer):
    class Meta(LocationSerializer.Meta):
        geo_field = "point"
        id_field = "uuid"
