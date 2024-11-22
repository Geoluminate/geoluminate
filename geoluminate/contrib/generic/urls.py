from django.urls import include, path

from .views import DatesCRUDView, DescriptionCRUDView

urlpatterns = [
    path("edit/<str:object_id>/", include(DescriptionCRUDView.get_urls())),
    path("edit/<str:object_id>/", include(DatesCRUDView.get_urls())),
]
