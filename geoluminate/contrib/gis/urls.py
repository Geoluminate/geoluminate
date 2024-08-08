from django.urls import include, path

from .plugins import location
from .views import LocationEditView

urlpatterns = [
    *LocationEditView.get_urls(),
    path("l/<lon>/<lat>/", include(location.urls)),
]
