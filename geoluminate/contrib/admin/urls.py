from django.contrib.gis import admin
from django.urls import include, path

urlpatterns = [
    path("actions/", include("adminactions.urls")),
    path("docs/", include("django.contrib.admindocs.urls")),
    path("translate/", include("jazzmin_translate.urls")),
    # path("grappelli/", include("grappelli.urls")),
    path("postgres-metrics/", include("postgres_metrics.urls")),
    path("entity-relationships/", include("django_spaghetti.urls")),

    path("", admin.site.urls),
]
