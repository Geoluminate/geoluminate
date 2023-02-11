# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import adminactions.actions as actions
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.admin import site
from django.urls import include, path

# register all adminactions
actions.add_to_site(site)


urlpatterns = [
    path("", include("geoluminate.contrib.gis.urls")),
    path("admin/doc/", include("django.contrib.admindocs.urls")),
    path("admin/translate/", include("jazzmin_translate.urls")),
    path("tellme/", include("tellme.urls")),
    path("plate/", include("django_spaghetti.urls")),
    path("adminactions/", include("adminactions.urls")),
    path("", include("geoluminate.urls")),
]


if settings.DEBUG:

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
