from django.urls import include, path

from .plugins import location, sample
from .views import LocationEditView, SampleEditView, SampleTableView

urlpatterns = [
    path("samples/", SampleTableView.as_view(), name="sample-list"),
    *SampleEditView.get_urls(),
    path("s/<uuid:pk>/", include(sample.urls), name="sample-detail"),
    *LocationEditView.get_urls(),
    path("l/<lon>/<lat>/", include(location.urls)),
]
