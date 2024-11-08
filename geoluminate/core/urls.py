from django.urls import include, path

from .views import generic, literature

urlpatterns = [
    path("edit/<str:base_pk>/", include(generic.DescriptionCRUDView.get_urls())),
    path("edit/<str:base_pk>/", include(generic.DatesCRUDView.get_urls())),
    path("activity/follow-object/<str:pk>", generic.follow_unfollow, name="follow-object"),
    path("contact/", generic.GenericContactForm.as_view(), name="contact"),
    path("references/", literature.ReferenceListView.as_view(), name="reference-list"),
]
