from django.urls import include, path

from . import views
from .views import dataset, project, sample

urlpatterns = [
    path(
        "projects/",
        include(
            [
                path("", project.list_view, name="project_list"),
                path("<uuid:uuid>/", views.ProjectDetail.as_view(), name="project_detail"),
            ]
        ),
    ),
    path(
        "datasets/",
        include(
            [
                path("", dataset.list_view, name="dataset_list"),
                path("<uuid:uuid>/", views.DatasetDetail.as_view(), name="dataset_detail"),
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
