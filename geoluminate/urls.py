from cms.sitemaps import CMSSitemap
from django.contrib.sitemaps.views import sitemap
from django.shortcuts import redirect
from django.urls import include, path

from . import views

urlpatterns = [
    path("sitemap.xml", sitemap, {"sitemaps": {"cmspages": CMSSitemap}}),
    path(
        "model-field-select2/",
        views.ModelFieldSelect2View.as_view(),
        name="geoluminate_select2",
    ),
    path("api/", lambda request: redirect("swagger-ui", permanent=False)),
    path("accounts/", include("allauth.urls")),
    path("admin/", include("geoluminate.contrib.admin.urls")),
    path("comments/", include("fluent_comments.urls")),
    path("database/", views.DatabaseTableView.as_view(), name="database_table"),
    path("datatables/", include("datatables.urls")),
    path("glossary/", views.GlossaryView.as_view(), name="glossary"),
    path("institutions/", include("ror.urls")),
    path("invitations/", include("invitations.urls", namespace="invitations")),
    path("literature/", include("geoluminate.contrib.literature.urls")),
    path("select2/", include("django_select2.urls")),
    path("tellme/", include("tellme.urls")),
    path("vocabularies/", include("controlled_vocabulary.urls")),
    path("", include("geoluminate.contrib.user.urls")),
    path("", include("geoluminate.contrib.gis.urls")),
    path("", include("cms.urls")),
]
