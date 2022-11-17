from django.urls import path, include
from drf_auto_endpoint.router import router

urlpatterns = [
    path('', include(router.urls)),
]
