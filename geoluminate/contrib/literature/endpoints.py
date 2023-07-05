from geoluminate import api

from .models import Publication


@api.register
class PublicationEndpoint(api.Endpoint):
    model = Publication
    url = "publications"
