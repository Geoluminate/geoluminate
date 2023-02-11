from django.urls import include, path
from django.utils.text import slugify
from rest_framework import routers

from .views import MapView, SiteView

# from geoluminate.contrib.api.v1.views import DataViewSet
# from geoluminate.utils import DATABASE


router = routers.DefaultRouter()
# router.register(slugify(DATABASE._meta.verbose_name), DataViewSet)

urlpatterns = [
    path("database/<pk>/", SiteView.as_view(), name="site"),
    path("viewer/", MapView.as_view(), name="viewer"),
]
