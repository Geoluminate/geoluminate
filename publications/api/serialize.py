from rest_framework import serializers
from publications import models
from crossref import serialize

class PublicationSerializer(serialize.WorkSerializer):
    pass
    # class Meta(PublicationSerializer.Meta):
    #     exclude = ['bibtex','pdf','owner']