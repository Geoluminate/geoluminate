from django.urls import path

from .views import DataExportView, DataImportView, DatasetPackageDownloadView, MetadataDownloadView

urlpatterns = [
    path("dataset/<str:pk>/import/", DataImportView.as_view(), name="dataset-import-view"),
    path("dataset/<str:pk>/export/", DataExportView.as_view(), name="dataset-export-view"),
    path("dataset/<str:pk>/package/", DatasetPackageDownloadView.as_view(), name="dataset-download"),
    path("dataset/<str:pk>/metadata/", MetadataDownloadView.as_view(), name="dataset-metadata-download"),
    # path("dataset/<str:pk>/upload/", DatasetUpload.as_view(), name="dataset-upload"),
]
