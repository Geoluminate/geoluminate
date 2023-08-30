from rest_framework import viewsets

from ..models import ControlledVocabulary
from .serializers import VocabularySerializer


class ControlledVocabularyViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = VocabularySerializer
    queryset = ControlledVocabulary.objects.all()
