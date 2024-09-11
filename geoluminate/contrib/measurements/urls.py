from django.urls import path

from .views import MeasurementListView, MeasurementTypeDetailView, MeasurementTypeListView

urlpatterns = [
    path("measurements/", MeasurementTypeListView.as_view(), name="measurement-type-list"),
    path("measurements/<slug:subclass>/", MeasurementListView.as_view(), name="measurement-list"),
    path("measurements/<slug:subclass>/explore/", MeasurementTypeDetailView.as_view(), name="measurement-type-detail"),
]
