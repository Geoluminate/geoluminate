from django.urls import path

from . import views

# from .menus import PublicationMenu

app_name = "literature"
urlpatterns = [
    path("", views.PublicationList.as_view(), name="list"),
    path("authors/", views.AuthorList.as_view(), name="author_list"),
    path("authors/<pk>/", views.AuthorDetail.as_view(), name="author_detail"),
    path("<pk>/", views.PublicationDetail.as_view(), name="detail"),
    # path('<pk>/', include(PublicationMenu().get_url_patterns())),
]
