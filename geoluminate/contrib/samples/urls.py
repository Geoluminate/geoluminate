from django.urls import include, path

from . import views
from .plugins import location, sample

app_name = "samples"
urlpatterns = [
    path("samples/", views.SampleList.as_view(), name="list"),
    path("samples/", views.SampleCreate.as_view(), name="create"),
    path("s/<uuid:uuid>/", include(sample.urls)),
    path("s/<uuid:uuid>/edit/", views.SampleEdit.as_view(), name="edit"),
    path("l/<int:lon>/<int:lat>/", include(location.urls)),
]
