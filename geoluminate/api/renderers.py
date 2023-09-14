from drf_orjson_renderer.renderers import ORJSONRenderer


class GeoJSONRenderer(ORJSONRenderer):
    format: str = "geojson"

    # not working in swagger docs
    # swagger is requesting application/json
    json_media_type: str = "application/geo+json"
    media_type: str = json_media_type
    html_media_type: str = "text/html"
