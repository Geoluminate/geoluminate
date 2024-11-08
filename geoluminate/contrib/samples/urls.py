from django.urls import include, path

from geoluminate.plugins import plugins

from .views import SampleCRUDView, SampleListView, SampleTypeDetailView, SampleTypeListView

urlpatterns = [
    *SampleCRUDView.get_urls(),
    path("samples/", SampleTypeListView.as_view(), name="sample-type-list"),
    path("samples/<slug:subclass>/", SampleListView.as_view(), name="sample-list"),
    path("samples/<slug:subclass>/about/", SampleTypeDetailView.as_view(), name="sample-type-detail"),
    path("sample/<str:pk>/", include(plugins.get_urls("sample"))),
]
