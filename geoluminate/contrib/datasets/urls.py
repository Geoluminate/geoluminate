from django.urls import include, path

from geoluminate.contrib.contributors.urls import contribution_patterns
from geoluminate.plugins import dataset

from .views import DatasetCreateView, DatasetFormView, DatasetListView

app_name = "datasets"
urlpatterns = [
    path("datasets/new/", DatasetCreateView.as_view(), name="add"),
    path("datasets/", DatasetListView.as_view(), name="list"),
    path("d/<uuid:uuid>/", include(dataset.urls)),
    path("d/<uuid:uuid>/edit/", DatasetFormView.as_view(), name="edit"),
    path("d/<uuid:uuid>/", include((contribution_patterns, "contribution"))),
]
