from django.urls import include, path

from .plugins import sample
from .views import SampleEditView, SampleTypeListView

urlpatterns = [
    path("samples/", SampleTypeListView.as_view(), name="sample-list"),
    # path("samples/", SampleTableView.as_view(), name="sample-list"),
    *SampleEditView.get_urls(),
    path("s/<uuid:pk>/", include(sample.urls), name="sample-detail"),
]
