from django.urls import include, path

from . import views
from .models import Dataset, Project, Sample
from .views import dataset, project, sample
from .views.base import list_view

app_name = "core"
urlpatterns = [
    path(
        "projects/",
        include(
            [
                path("", list_view(model=Project), name="project-list"),
                path("<uuid:uuid>/", views.ProjectDetail.as_view(), name="project-detail"),
                # path("<uuid:uuid>/map/", views.ProjectDetail.as_view(), name="project-detail-map"),
            ]
        ),
    ),
    path(
        "datasets/",
        include(
            [
                path("", list_view(model=Dataset), name="dataset_list"),
                path("<uuid:uuid>/", views.DatasetDetail.as_view(), name="dataset-detail"),
            ]
        ),
    ),
    path(
        "samples/",
        include(
            [
                path("", sample.list_view, name="sample_list"),
                path("<uuid:uuid>/", views.SampleDetail.as_view(), name="sample_detail"),
            ]
        ),
    ),
    path(
        "measurements/",
        include(
            [
                path("", sample.list_view, name="measurement_list"),
            ]
        ),
    ),
]
