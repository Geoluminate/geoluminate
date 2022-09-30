from rest_framework import viewsets
from publications.models import Publication
from rest_framework_extensions.cache.decorators import cache_response
from publications.api.serialize import PublicationSerializer

class PublicationModelViewSet(viewsets.ModelViewSet):
    """API endpoint to request a set of publications from the World Heat Flow Database."""
    queryset = Publication.objects.all()
    serializer_class = PublicationSerializer

    def get_queryset(self):
        return super().get_queryset().prefetch_related('author')


