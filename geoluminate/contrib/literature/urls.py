from django.urls import include, path
from drf_auto_endpoint.router import register, router

from . import views
from .models import Publication

# from .menus import PublicationMenu
# router.register(model=Publication, url="publication")


app_name = "literature"
urlpatterns = [
    # path("api/", include(router.urls)),
    # path("", views.PublicationList.as_view(), name="list"),
    # path("authors/", views.AuthorList.as_view(), name="author_list"),
    # path("authors/<pk>/", views.AuthorDetail.as_view(), name="author_detail"),
    # path("<pk>/", views.PublicationDetail.as_view(), name="detail"),
    # path('<pk>/', include(PublicationMenu().get_url_patterns())),
]
