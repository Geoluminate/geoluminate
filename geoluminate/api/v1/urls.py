from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)
from geoluminate.utils import get_api_routers
from rest_framework import routers
router = routers.DefaultRouter()

urls = []
for r in get_api_routers():
    urls.append(path('', include(r.urls)))
#     router.registry.extend(r.registry)

urlpatterns = [
    path('', SpectacularSwaggerView.as_view(
        url_name='schema'), name='swagger-ui'),
    path('', include(urls)),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('auth/', include('rest_framework.urls', namespace='rest_framework')),
]

# urlpatterns.extend(urls)
