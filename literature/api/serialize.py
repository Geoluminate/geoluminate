from rest_framework import serializers
from literature.models import Publication
from crossref.models import Author
from rest_framework_nested.relations import NestedHyperlinkedRelatedField
from rest_framework_nested.serializers import NestedHyperlinkedModelSerializer
from geoluminate.api.v1.serializers import CoreSerializer
from geoluminate.utils import DATABASE
from django.utils.translation import gettext_lazy as _
from rest_framework.utils.serializer_helpers import (
    ReturnDict,
    ReturnList,
)

# class AuthorSerializer(serializers.HyperlinkedModelSerializer):


class AuthorSerializer(serializers.ModelSerializer):
    as_lead = serializers.IntegerField(
        read_only=True,
        # source='as_lead',
        label=_('as lead author'),
        help_text=_(
            "The number of times an author is listed first on a publication within this database."),
    )
    as_supporting = serializers.IntegerField(
        read_only=True,
        # source='as_supporting',
        label=_('as Co-author'),
        help_text=_(
            "The number of times an author is listed as co-author on a publication within this database."),
    )

    class Meta:
        model = Author
        fields = '__all__'


# class LiteratureSerializer(serializers.HyperlinkedModelSerializer):
class LiteratureSerializer(serializers.ModelSerializer):
    # author = AuthorSerializer(read_only=True, many=True)
    subject = serializers.StringRelatedField(many=True)
    author_count = serializers.IntegerField(
        source='author.count',
        read_only=True
    )

    data = serializers.HyperlinkedIdentityField(
        view_name='literature-core-list',
        lookup_url_kwarg='lit_pk',
    )

    class Meta:
        model = Publication
        exclude = ['last_queried_crossref', 'source', 'pdf', 'owner', 'author']


class CoreNestedListSerializer(serializers.ListSerializer):
    @property
    def data(self):
        ret = super().data
        return ReturnDict(
            count=len(ret),
            description="Test description",
            data=ret,
            serializer=self)


class CoreNestedSerializer(NestedHyperlinkedModelSerializer, CoreSerializer):
    parent_lookup_kwargs = {
        'pub_pk': 'references__pk',
    }

    # class Meta(CoreSerializer.Meta):
    #     list_serializer_class = CoreNestedListSerializer
