from cms.sitemaps import CMSSitemap
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path
from drf_auto_endpoint.router import router as drf_router

from . import views

# these URLS don't require translation capabilities
NON_I18N_URLS = [
    path("sitemap.xml", sitemap, {"sitemaps": {"cmspages": CMSSitemap}}),
    path("api/", include("geoluminate.contrib.api.urls")),
    path("select2/", include("django_select2.urls")),
    path("comments/", include("fluent_comments.urls")),
    path("admin/literature/api/", include(drf_router.urls), name="admin_api"),
    path(
        "model-field-select2/",
        views.ModelFieldSelect2View.as_view(),
        name="geoluminate_select2",
    ),
    # path("tellme/", include("tellme.urls")),
    # path("vocabularies/", include("controlled_vocabulary.urls")),
    # *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
    # *static(settings.STATIC_URL, document_root=settings.STATIC_ROOT),
]

I18N_URLS = [
    path("invitations/", include("invitations.urls", namespace="invitations")),
    path("accounts/", include("allauth.urls")),
    path("admin/", include("geoluminate.contrib.admin.urls")),
    path("database/", views.DatabaseTableView.as_view(), name="database_table"),
    path("literature/", include("literature.urls")),
    # path("literature/", include("geoluminate.contrib.literature.urls")),
    path("", include("geoluminate.contrib.user.urls")),
    path("", include("geoluminate.contrib.gis.urls")),
    path("", include("cms.urls")),
]


# urlpatterns = (
#     NON_I18N_URLS
#     + I18N_URLS
#     + [path("", include("cms.urls"))]  # must be last
#     + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#     + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
# )
