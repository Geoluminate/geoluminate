import adminactions.actions as actions

# from cms.sitemaps import CMSSitemap
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.admin import site
from django.urls import include, path
from django.views import defaults as default_views
from django.views.decorators.cache import cache_page
from django.views.generic import TemplateView

from geoluminate.measurements import measurements
from geoluminate.views import HomeView

# from .admin import admin_measurement_view
# register all adminactions
actions.add_to_site(site)

# these URLS don't require translation capabilities
NON_I18N_URLS = [
    path("comments/", include("fluent_comments.urls")),
    path("api/", include("geoluminate.api.urls")),
    path("i18n/", include("django.conf.urls.i18n")),
]


I18N_URLS = [
    path(settings.ADMIN_URL, admin.site.urls),
    path("", HomeView.as_view(), name="home"),
    path(
        "explorer/",
        cache_page(60 * 5)(TemplateView.as_view(template_name="geoluminate/components/map.html")),
        name="viewer",
    ),
    path("", include("geoluminate.contrib.datasets.urls")),
    path("", include("geoluminate.contrib.reviews.urls")),
    path("", include("geoluminate.contrib.projects.urls")),
    path("", include("geoluminate.contrib.samples.urls")),
    path("", include("geoluminate.contrib.measurements.urls")),
    path("", include("geoluminate.contrib.contributors.urls")),
    path("", include("geoluminate.contrib.organizations.urls")),
    path("", include("geoluminate.contrib.core.urls")),  # must be before actstream.urls
    path("vocabularies/", include("research_vocabs.urls")),
    path("measurements/", include(measurements.urls)),
    path("account/", include("allauth.urls")),
    path("", include("geoluminate.contrib.users.urls")),
    path("invitations/", include("invitations.urls", namespace="invitations")),
    path("contact/", include("django_contact_form.urls")),
    path("select2/", include("django_select2.urls")),
    path("activity/", include("actstream.urls")),
    path("admin_tools/", include("admin_tools.urls")),
    # path("admin/measurements/", admin_measurement_view, name="admin_measurements"),
]
urlpatterns = NON_I18N_URLS + I18N_URLS


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
