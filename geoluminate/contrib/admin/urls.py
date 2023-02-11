from django.contrib.gis import admin
from django.urls import include, path

urlpatterns = [
    path("grappelli/", include("grappelli.urls")),
    path("postgres-metrics/", include("postgres_metrics.urls")),
    path("", admin.site.urls),
]
