from django.contrib.gis.gdal.envelope import Envelope
from django.contrib.gis.geos import GEOSGeometry
from django.utils.translation import gettext_lazy as _
from literature.models import Author
from rest_framework import serializers
from rest_framework_nested.serializers import NestedHyperlinkedModelSerializer

from geoluminate.contrib.api.v1.serializers import CoreSerializer

from ..models import Publication


class AuthorSerializer(serializers.HyperlinkedModelSerializer):
    as_lead = serializers.IntegerField(
        read_only=True,
        # source='as_lead',
        label=_("as lead author"),
        help_text=_("The number of times an author is listed first on a publication within this database."),
    )
    as_supporting = serializers.IntegerField(
        read_only=True,
        # source='as_supporting',
        label=_("as Co-author"),
        help_text=_("The number of times an author is listed as co-author on a publication within this database."),
    )

    class Meta:
        model = Author
        fields = "__all__"


class LiteratureSerializer(serializers.HyperlinkedModelSerializer):
    subject = serializers.StringRelatedField(many=True)
    author_count = serializers.IntegerField(source="author.count", read_only=True)
    authors = serializers.HyperlinkedIdentityField(
        view_name="literature-authors-list",
        lookup_url_kwarg="lit_pk",
    )
    data = serializers.HyperlinkedIdentityField(
        view_name="literature-data-list",
        lookup_url_kwarg="lit_pk",
    )
    bbox = serializers.ListField(read_only=True)
    # bbox = serializers.SerializerMethodField()

    class Meta:
        model = Publication
        exclude = ["last_queried_crossref", "source", "pdf", "owner", "author"]

    def get_bbox(self, obj):
        if obj.bbox:
            return GEOSGeometry(Envelope(obj.bbox).wkt).json
        return {}


class CoreNestedListSerializer(serializers.ListSerializer):
    pass
    # @property
    # def data(self):
    #     ret = super().data
    #     return ReturnDict(
    #         count=len(ret),
    #         description="Test description",
    #         data=ret,
    #         serializer=self)


class AuthorNestedSerializer(NestedHyperlinkedModelSerializer, AuthorSerializer):
    parent_lookup_kwargs = {
        "pub_pk": "author__pk",
    }


class CoreNestedSerializer(NestedHyperlinkedModelSerializer, CoreSerializer):
    parent_lookup_kwargs = {
        "pub_pk": "references__pk",
    }

    # class Meta(CoreSerializer.Meta):
    #     list_serializer_class = CoreNestedListSerializer
