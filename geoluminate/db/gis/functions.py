from django.contrib.gis.db.models.functions import AsGeoJSON, GeoFunc
from django.db.models import F, FloatField, JSONField, Value
from django.db.models.functions import Cast, JSONObject


def AsGeoFeature(*args):
    return JSONObject(
        type=Value("Feature"),
        id=F("pk"),
        geometry=Cast(AsGeoJSON("geom"), output_field=JSONField()),
        properties=JSONObject(**{p: F(p) for p in args}),
    )


class Lat(GeoFunc):
    function = "ST_X"
    output_field = FloatField()


class Lon(GeoFunc):
    function = "ST_Y"
    output_field = FloatField()


class OrientedEnvelope(GeoFunc):
    function = "ST_OrientedEnvelope"
    output_field = FloatField()
