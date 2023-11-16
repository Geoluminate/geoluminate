from django.urls import include, path

from geoluminate.plugins import dataset

from .views import (
    AddLiteratureView,
    DatasetCreateView,
    DatasetListView,
    LiteratureListView,
)

app_name = "datasets"
urlpatterns = [
    path("datasets/new/", DatasetCreateView.as_view(), name="add"),
    path("datasets/", DatasetListView.as_view(), name="list"),
    path("d/<uuid:uuid>/", include(dataset.urls)),
    path("literature/new/", AddLiteratureView.as_view(), name="literature_create"),
    path("literature/", LiteratureListView.as_view(), name="literature_list"),
]
