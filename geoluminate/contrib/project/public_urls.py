from django.urls import include, path

from . import views

urlpatterns = [
    path(
        "projects/",
        include(
            [
                path("", views.ProjectList.as_view(), name="project_list"),
                path("<uuid:uuid>/", views.ProjectDetail.as_view(), name="project_detail"),
            ]
        ),
    ),
    path(
        "datasets/",
        include(
            [
                path("", views.DatasetList.as_view(), name="dataset_list"),
                path("<uuid:uuid>/", views.DatasetDetail.as_view(), name="dataset_detail"),
            ]
        ),
    ),
    path(
        "samples/",
        include(
            [
                path("", views.SampleList.as_view(), name="sample_list"),
                path("<uuid:uuid>/", views.SampleDetail.as_view(), name="sample_detail"),
            ]
        ),
    ),
    path(
        "measurements/",
        include(
            [
                path("", views.SampleList.as_view(), name="measurement_list"),
            ]
        ),
    ),
]
