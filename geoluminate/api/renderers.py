from drf_orjson_renderer.renderers import ORJSONRenderer
from rest_framework_datatables_editor import renderers


class GeoJSONRenderer(ORJSONRenderer):
    format: str = "geojson"
    json_media_type: str = "application/geo+json"
    media_type: str = json_media_type
    html_media_type: str = "text/html"
