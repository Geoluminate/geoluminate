from django.urls import path

from .views import UpdateCoreObjectBasicInfo, UpdateDatesView, UpdateKeywordsView

urlpatterns = [
    # path("edit/<str:object_id>/", include(DescriptionCRUDView.get_urls())),
    path("edit/<str:pk>/dates/", UpdateDatesView.as_view(), name="date-collection-update"),
    path("edit/<str:pk>/descriptions/", UpdateCoreObjectBasicInfo.as_view(), name="description-formset"),
    path("edit/<str:pk>/keywords/", UpdateKeywordsView.as_view(), name="update-keywords"),
]
