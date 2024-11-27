from django.urls import include, path
from neapolitan.views import Role

from geoluminate.plugins import plugins

from .views import (
    DatasetCRUDView,
    DatasetUpload,
    MeasurementListView,
    MetadataDownloadView,
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
    path("dataset/<str:pk>/metadata/", MetadataDownloadView.as_view(), name="dataset-metadata-download"),
    path("dataset/<str:pk>/upload/", DatasetUpload.as_view(), name="dataset-upload"),
    *SampleCRUDView.get_urls(roles=[Role.CREATE, Role.DETAIL, Role.UPDATE, Role.DELETE]),
    path("sample/<str:pk>/", include(plugins.get_urls("sample"))),
    path("sample/", SampleListView.as_view(), name="sample-list"),
    path("measurement/", MeasurementListView.as_view(), name="measurement-list"),
]
