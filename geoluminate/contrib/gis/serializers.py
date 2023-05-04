from collections import OrderedDict

from rest_framework.serializers import (
    LIST_SERIALIZER_KWARGS,
    ListSerializer,
)
from rest_framework_gis.serializers import GeoFeatureModelSerializer


class FeatureCollectionSerializer(ListSerializer):
    @property
    def data(self):
        return super(ListSerializer, self).data

    def to_representation(self, data):
        """
        Add GeoJSON compatible formatting to a serialized queryset list
        """
        return OrderedDict(
            (
                ("type", "FeatureCollection"),
                ("features", data.feature_collection()["features"]),
            )
        )


class FeatureSerializer(GeoFeatureModelSerializer):
    @classmethod
    def many_init(cls, *args, **kwargs):
        child_serializer = cls(*args, **kwargs)
        list_kwargs = {"child": child_serializer}
        list_kwargs.update({key: value for key, value in kwargs.items() if key in LIST_SERIALIZER_KWARGS})
        meta = getattr(cls, "Meta", None)
        list_serializer_class = getattr(meta, "list_serializer_class", FeatureCollectionSerializer)
        return list_serializer_class(*args, **list_kwargs)

    def to_representation(self, data):
        data = data.features()
        return data.get().feature
