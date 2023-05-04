from cms.sitemaps import CMSSitemap
from django.contrib.sitemaps.views import sitemap
from django.shortcuts import redirect
from django.urls import include, path
from django.views.generic import TemplateView

from . import views

# urlpatterns required by third party applications
external_urlpatterns = [
    path("sitemap.xml", sitemap, {"sitemaps": {"cmspages": CMSSitemap}}),
    path(
        "model-field-select2/",
        views.ModelFieldSelect2View.as_view(),
        name="geoluminate_select2",
    ),
    path("accounts/", include("allauth.urls")),
    path("comments/", include("fluent_comments.urls")),
    # path("institutions/", include("ror.urls")),
    path("invitations/", include("invitations.urls", namespace="invitations")),
    path("select2/", include("django_select2.urls")),
    # path("tellme/", include("tellme.urls")),
    # path("vocabularies/", include("controlled_vocabulary.urls")),
]

# urlpatterns defined by geoluminate
internal_urlpatterns = [
    # path("api/", lambda request: redirect("swagger-ui", permanent=False)),
    path("api/", include("geoluminate.contrib.api.urls")),
    path("admin/", include("geoluminate.contrib.admin.urls")),
    path("database/", views.DatabaseTableView.as_view(), name="database_table"),
    path("history/", TemplateView.as_view(template_name="placeholder.html"), name="database_history"),
    path("literature/", include("geoluminate.contrib.literature.urls")),
    path("", include("geoluminate.contrib.user.urls")),
    path("", include("geoluminate.contrib.gis.urls")),
]

urlpatterns = external_urlpatterns + internal_urlpatterns

urlpatterns.append(path("", include("cms.urls")))
