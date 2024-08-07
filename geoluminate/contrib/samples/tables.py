from django.utils.safestring import mark_safe

from geoluminate.api.v1.serializers import SampleSerializer
from geoluminate.tables import GeoluminateTable, ScrollerTable

from .models import BaseSample


class SampleTable(GeoluminateTable):
    config_class = ScrollerTable
    model = BaseSample
    serializer_class = SampleSerializer
    details_template = '<a href="${data}"><i class="fa-solid fa-file-lines"></i></a>'
    absolute_url_template = '<a href="${data}"><i class="fa-solid fa-file-lines"></i></a>'
    location_template = '<a href="${data}"><i class="fa-solid fa-map-location-dot"></i></a>'
    parent_template = '<a href="${data}"><i class="fa-solid fa-sitemap"></i></a>'
    dataset_template = '<a href="${data}"><i class="fa-solid fa-folder-open"></i></a>'
    visible_fields = [
        "absolute_url",
        # "details",
        # "dataset",
        # "location",
        "title",
        "feature_type",
        "medium",
        "specimen_type",
        # "parent",
    ]
    search_fields = ["title"]
    ordering_fields = ["title", "feature_type", "medium", "specimen_type"]
    extra_field_attributes = {
        # "location": {
        #     "title": mark_safe(f'<i class="{icon("map")}"></i>'),
        #     "class": "text-center",
        # },
        "absolute_url": {
            "title": mark_safe('<i class="fa-solid fa-file-lines"></i>'),
            "class": "text-center",
        },
        # "details": {
        #     "title": mark_safe('<i class="fa-solid fa-file-lines"></i>'),
        #     "class": "text-center",
        # },
        # "parent": {
        #     "title": mark_safe('<i class="fa-solid fa-sitemap"></i>'),
        #     "class": "text-center",
        # },
        # "dataset": {
        #     "title": mark_safe(f'<i class="{icon("dataset")}"></i>'),
        #     "class": "text-center",
        # },
    }
