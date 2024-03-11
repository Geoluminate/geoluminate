from django.contrib.gis.db import models

# from django.contrib.gis.utils import LayerMapping
from django.contrib.postgres.aggregates import JSONBAgg

from geoluminate.db.gis.functions import AsGeoFeature

# DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "data"))


class LocationManager(models.QuerySet):
    def with_distance(self, point):
        return self.annotate(distance=models.Distance("geom", point))

    def get_feature(self, *args, **kwargs):
        return self.annotate(feature=AsGeoFeature(*args)).get(*args, **kwargs)

    def features(self, *args):
        if not args:
            args = [f.name for f in self.model._meta.fields]
        return self.annotate(feature=AsGeoFeature(*args))

    def feature_collection(self, *args):
        return self.features(*args).aggregate(features=JSONBAgg("feature"))

    def as_feature_collection(self, *args):
        """Converts a queryset in a geojson spec FeatureCollection"""
        return dict(type="FeatureCollection", **self.feature_collection())
