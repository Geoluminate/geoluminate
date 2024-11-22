from django.urls import include, path
from neapolitan.views import Role

from geoluminate.plugins import plugins

from .views import (
    DatasetCRUDView,
    MeasurementListView,
    ProjectCRUDView,
    SampleCRUDView,
    SampleListView,
    SamplesDownloadView,
)

# re_path(UUID_RE_PATTERN, DirectoryView.as_view(), name="directory"),

urlpatterns = [
    *ProjectCRUDView.get_urls(),
    path("project/<str:pk>/", include(plugins.get_urls("project"))),
    *DatasetCRUDView.get_urls(),
    path("dataset/<str:pk>/", include(plugins.get_urls("dataset"))),
    path("sample/download/", SamplesDownloadView.as_view(), name="samples-download"),
    *SampleCRUDView.get_urls(roles=[Role.CREATE, Role.DETAIL, Role.UPDATE, Role.DELETE]),
    path("sample/<str:pk>/", include(plugins.get_urls("sample"))),
    path("sample/", SampleListView.as_view(), name="sample-list"),
    path("measurement/", MeasurementListView.as_view(), name="measurement-list"),
]
