from django.contrib.gis import admin
from django.urls import include, path, re_path
from rosetta import views

from .views import (
    ApplicationView,
    LanguageView,
    TranslationIndexView,
    create_locale_file,
)

admin_translate_urls = [
    path(
        "",
        TranslationIndexView.as_view(),
        name="jazzmin_translate.index",
    ),
    re_path(
        r"^(?P<lang_id>[\w\-_\.]+)/$",
        LanguageView.as_view(),
        name="jazzmin_translate.language",
    ),
    re_path(
        r"^(?P<lang_id>[\w\-_\.]+)/create/$",
        create_locale_file,
        name="jazzmin_translate.create-file",
    ),
    re_path(
        r"^(?P<lang_id>[\w\-_\.]+)/(?P<app_name>[\w\-_\.]+)/$",
        ApplicationView.as_view(),
        name="jazzmin_translate.application",
    ),
    re_path(
        r"^(?P<lang_id>[\w\-_\.]+)/(?P<app_name>[\w\-_\.]+)/download/$",
        views.TranslationFileDownload.as_view(),
        name="jazzmin_translate.download-file",
    ),
    re_path(
        r"^translate/$",
        views.translate_text,
        name="rosetta.translate_text",
    ),
]

urlpatterns = [
    path("actions/", include("adminactions.urls")),
    path("docs/", include("django.contrib.admindocs.urls")),
    path("translate/", include(admin_translate_urls)),
    path("postgres-metrics/", include("postgres_metrics.urls")),
    path("entity-relationships/", include("django_spaghetti.urls")),
    path("", admin.site.urls),
]
