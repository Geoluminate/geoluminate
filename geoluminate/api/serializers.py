from django.contrib.sites.models import Site
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_field
from rest_flex_fields.serializers import FlexFieldsSerializerMixin
from rest_framework import serializers

# from .serializers import GeoFeatureSerializer


class BaseSerializerMixin(FlexFieldsSerializerMixin):
    URI = serializers.SerializerMethodField()

    @extend_schema_field(OpenApiTypes.URI)
    def get_URI(self, obj):
        current_site = Site.objects.get_current()
        return f"http://{current_site.domain}{obj.get_absolute_url()}"

    def get_field_names(self, declared_fields, info):
        """Returns a case-insensitive, sorted list of field names."""
        fields = super().get_field_names(declared_fields, info)
        return sorted(fields, key=str.casefold)
