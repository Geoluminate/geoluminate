from django.urls import include, path

from .plugins import sample
from .views import SampleEditView, SampleTableView

urlpatterns = [
    path("samples/", SampleTableView.as_view(), name="sample-list"),
    *SampleEditView.get_urls(),
    path("s/<uuid:pk>/", include(sample.urls), name="sample-detail"),
]
