from django.contrib.gis import admin
from .models import Site
from .db_functions import Lat, Lon


class SiteAdminMixin(admin.OSMGeoAdmin):
    geom_field = 'geom'

    def get_queryset(self, request):
        """Modified to annotate 'lat' and 'lon' coordinates to the
        admin queryset."""
        qs = super().get_queryset(request)
        if '__' in self.geom_field:
            qs = qs.select_related(self.geom_field.split('__')[0])
        return qs.annotate(lat=Lat(self.geom_field), lon=Lon(self.geom_field))

    def lon(self, obj):
        return round(obj.lat, 5)
    lon.admin_order_field = 'lon'

    def lat(self, obj):
        return round(obj.lon, 5)
    lat.admin_order_field = 'lat'
