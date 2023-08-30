from rest_framework import serializers

from ..models import ControlledVocabulary


class VocabularySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ControlledVocabulary
        fields = "__all__"
