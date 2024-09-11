from django.urls import include, path

from .plugins import sample
from .views import SampleEditView, SampleListView, SampleTypeDetailView, SampleTypeListView

urlpatterns = [
    path("samples/", SampleTypeListView.as_view(), name="sample-type-list"),
    path("samples/<slug:subclass>/", SampleListView.as_view(), name="sample-list"),
    path("samples/<slug:subclass>/about/", SampleTypeDetailView.as_view(), name="sample-type-detail"),
    *SampleEditView.get_urls(),
    path("s/<uuid:pk>/", include(sample.urls), name="sample-detail"),
]
