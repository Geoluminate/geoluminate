from django.urls import include, path

from geoluminate.plugins import location, sample

from .views import list_view

app_name = "samples"
urlpatterns = [
    path("samples/", list_view, name="list"),
    path("s/<uuid:uuid>/", include(sample.urls)),
    # path("l/<uuid:uuid>/", include(location.urls)),
]

# print(location.urls)
