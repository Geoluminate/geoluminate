from rest_framework import routers
from geoluminate.utils import DATABASE
from geoluminate.api.v1.views import DataViewSet
from django.utils.text import slugify

router = routers.DefaultRouter()
router.register(slugify(DATABASE._meta.verbose_name), DataViewSet)
