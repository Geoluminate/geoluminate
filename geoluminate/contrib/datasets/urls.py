from django.urls import include, path

from geoluminate.plugins import plugins

from .views import DatasetCRUDView

urlpatterns = [
    *DatasetCRUDView.get_urls(),
    path("dataset/<str:pk>/", include(plugins.get_urls("dataset"))),
]
