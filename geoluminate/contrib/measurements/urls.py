from django.urls import path

from .views import MeasurementTypeListView

urlpatterns = [
    path("measurements/", MeasurementTypeListView.as_view(), name="measurement-list"),
]
