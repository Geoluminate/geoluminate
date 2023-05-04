from django.urls import path
from rest_framework import routers

from .views import MapView, SiteView

router = routers.DefaultRouter()

urlpatterns = [
    path("database/<pk>/", SiteView.as_view(), name="site"),
    path("viewer/", MapView.as_view(), name="viewer"),
]
