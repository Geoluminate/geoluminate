from django.contrib.gis import admin

from .functions import Lat, Lon


class SiteAdminMixin(admin.GISModelAdmin):
    geom_field = "point"

    def get_queryset(self, request):
        """Modified to annotate 'lat' and 'lon' coordinates to the
        admin queryset."""
        qs = super().get_queryset(request)
        if "__" in self.geom_field:
            qs = qs.select_related(self.geom_field.split("__")[0])
        return qs.annotate(lat=Lat(self.geom_field), lon=Lon(self.geom_field))
