from rest_framework import serializers
from publications import models
from crossref.serialize import PublicationSerializer

class PublicationSerializer(PublicationSerializer):

    class Meta(PublicationSerializer.Meta):
        exclude = ['verified_by','bibtex','pdf','owner']