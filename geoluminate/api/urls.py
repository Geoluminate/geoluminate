from django.urls import include, path
from django.shortcuts import redirect

app_name = 'api'
urlpatterns = [
    path('v1/', include("geoluminate.api.v1.urls")),
    path('', lambda request: redirect('/api/v1', permanent=True))
]
