import adminactions.actions as actions
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.admin import site
from django.urls import include, path, re_path
from django.views import defaults as default_views
from django.views.i18n import JavaScriptCatalog

from fairdm.core.utils import UUID_RE_PATTERN
from fairdm.utils.views import DirectoryView, HomeView

# from .admin import admin_measurement_view
# register all adminactions
actions.add_to_site(site)

urlpatterns = [
    path(settings.ADMIN_URL, admin.site.urls),
    path(r"jsi18n/", JavaScriptCatalog.as_view(), name="javascript-catalog"),
    path("django-literature/", include("literature.urls")),
    path("", HomeView.as_view(), name="home"),
    path("", include("fairdm.core.urls")),
    path("", include("fairdm.contrib.contributors.urls")),
    path("", include("fairdm.contrib.import_export.urls")),
    path("", include("fairdm.contrib.generic.urls")),
    path("", include("fairdm.utils.urls")),
    path("api/", include("fairdm.contrib.api.urls")),
    path("vocabularies/", include("research_vocabs.urls")),
    path("account/", include("account_management.urls")),
    path("account/", include("allauth.urls")),
    path("invitations/", include("invitations.urls", namespace="invitations")),
    path("contact/", include("django_contact_form.urls")),
    path("select2/", include("django_select2.urls")),
    path("activity/", include("actstream.urls")),
    path("admin_tools/", include("admin_tools.urls")),
    path("comments/", include("fluent_comments.urls")),
    path("i18n/", include("django.conf.urls.i18n")),
    path("comments/", include("django_comments_xtd.urls")),
    path("", include("pwa.urls")),  # MUST be an empty string as the URL prefix
    re_path(UUID_RE_PATTERN, DirectoryView.as_view(), name="directory"),
]


# adds the debug toolbar to templates if installed
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path(
            "500/",
            default_views.server_error,
        ),
    ]

    if "debug_toolbar" in settings.INSTALLED_APPS:
        from debug_toolbar.toolbar import debug_toolbar_urls

        urlpatterns += debug_toolbar_urls()


# urlpatterns += [path("", include("cms.urls"))]  # must be last
