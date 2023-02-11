from django.urls import path, re_path
from rosetta import views

from .views import (
    ApplicationView,
    LanguageView,
    TranslationIndexView,
    create_locale_file,
)

app_name = "jazzmin_translate"
urlpatterns = [
    path(
        "",
        TranslationIndexView.as_view(),
        name="index",
    ),
    re_path(
        r"^(?P<lang_id>[\w\-_\.]+)/$",
        LanguageView.as_view(),
        name="language",
    ),
    re_path(
        r"^(?P<lang_id>[\w\-_\.]+)/create/$",
        create_locale_file,
        name="create-file",
    ),
    re_path(
        r"^(?P<lang_id>[\w\-_\.]+)/(?P<app_name>[\w\-_\.]+)/$",
        ApplicationView.as_view(),
        name="application",
    ),
    re_path(
        r"^(?P<lang_id>[\w\-_\.]+)/(?P<app_name>[\w\-_\.]+)/download/$",
        views.TranslationFileDownload.as_view(),
        name="download-file",
    ),
    re_path(
        r"^translate/$",
        views.translate_text,
        name="rosetta.translate_text",
    ),
]
