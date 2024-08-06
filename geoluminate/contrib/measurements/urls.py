from django.urls import path

from . import views

app_name = "measurements"
urlpatterns = [
    path("samples/", views.SampleTableView.as_view(), name="list"),
]
