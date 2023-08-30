from rest_framework import serializers
from rest_framework_nested.relations import NestedHyperlinkedIdentityField
from rest_framework_nested.serializers import NestedHyperlinkedModelSerializer
from taggit.serializers import TaggitSerializer, TagListSerializerField

from geoluminate.contrib.user.api.serializers import ProfileSerializer

from ..models import Contributor, Dataset, Description, KeyDate, Project, Sample, Site


class ContributorRoleSerializer(serializers.HyperlinkedModelSerializer):
    # profile = serializers.HyperlinkedIdentityField(view_name="profile", lookup_field="pk")

    contributor = ProfileSerializer(source="profile")

    class Meta:
        model = Contributor
        fields = ["contributor", "roles"]


class DescriptionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Description
        fields = ["type", "description"]


class KeyDateSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = KeyDate
        fields = ["type", "date"]


class ProjectSerializer(serializers.HyperlinkedModelSerializer):
    web_url = serializers.HyperlinkedIdentityField(view_name="project_detail", lookup_field="uuid")

    datasets = NestedHyperlinkedIdentityField(
        view_name="dataset-list",
        lookup_field="uuid",
        lookup_url_kwarg="project_uuid",
    )
    contributors = ContributorRoleSerializer(many=True, read_only=True)
    descriptions = DescriptionSerializer(many=True, read_only=True)
    key_dates = KeyDateSerializer(many=True, read_only=True)

    tags = TagListSerializerField()

    class Meta:
        model = Project
        # fields = ["url", "uuid"]
        exclude = ["created_by", "is_public"]
        extra_kwargs = {"url": {"lookup_field": "uuid"}}


class DatasetSerializer(NestedHyperlinkedModelSerializer):
    parent_lookup_kwargs = {
        "project_uuid": "project__uuid",
    }

    web_url = serializers.HyperlinkedIdentityField(view_name="dataset_detail", lookup_field="uuid")

    bbox = serializers.SerializerMethodField(
        help_text="Bounding box of the dataset in WGS84 (EPSG:4326) coordinates. Format: [minx, miny, maxx, maxy]."
    )

    sites = NestedHyperlinkedIdentityField(
        view_name="site-list",
        lookup_field="uuid",
        lookup_url_kwarg="dataset_uuid",
    )
    samples = NestedHyperlinkedIdentityField(
        view_name="sample-list",
        lookup_field="uuid",
        lookup_url_kwarg="dataset_uuid",
    )
    contributors = ContributorRoleSerializer(many=True, read_only=True)
    descriptions = DescriptionSerializer(many=True, read_only=True)
    key_dates = KeyDateSerializer(many=True, read_only=True)
    keywords = TagListSerializerField()

    class Meta:
        model = Dataset
        fields = "__all__"
        extra_kwargs = {"url": {"lookup_field": "uuid"}, "project": {"lookup_field": "uuid"}}

    def get_bbox(self, obj):
        return obj.bbox()


class SampleSerializer(NestedHyperlinkedModelSerializer):
    parent_lookup_kwargs = {
        "dataset_uuid": "dataset__uuid",
    }
    web_url = serializers.HyperlinkedIdentityField(view_name="sample_detail", lookup_field="uuid")

    class Meta:
        model = Sample
        fields = "__all__"
        extra_kwargs = {"url": {"lookup_field": "uuid"}, "dataset": {"lookup_field": "uuid"}}


class SiteSerializer(NestedHyperlinkedModelSerializer):
    parent_lookup_kwargs = {
        "dataset_uuid": "dataset__uuid",
    }

    class Meta:
        model = Site
        fields = "__all__"
        extra_kwargs = {"url": {"lookup_field": "uuid"}}


class MeasurementSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        fields = "__all__"
        extra_kwargs = {"url": {"lookup_field": "uuid"}}
