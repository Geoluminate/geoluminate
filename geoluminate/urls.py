from cms.sitemaps import CMSSitemap
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.gis import admin
from django.contrib.sitemaps.views import sitemap
from django.shortcuts import redirect
from django.urls import include, path
from django.views.generic import TemplateView

from geoluminate.measurements import measurements

from .admin import admin_measurement_view
from .views import DashboardRedirect

# these URLS don't require translation capabilities
NON_I18N_URLS = [
    path("sitemap.xml", sitemap, {"sitemaps": {"cmspages": CMSSitemap}}),
    path("comments/", include("fluent_comments.urls")),
    path("api/", include("geoluminate.api.urls")),
]


I18N_URLS = [
    # path(
    #     "public/",
    #     include(
    #         [
    path("explorer/", TemplateView.as_view(template_name="geoluminate/components/map.html"), name="viewer"),
    path("glossary/", include("glossary.urls")),
    # path("literature/", include("literature.urls")),
    #         ]
    #     ),
    # ),
    path("", include("geoluminate.contrib.datasets.urls")),
    path("", include("geoluminate.contrib.reviews.urls")),
    path("", include("geoluminate.contrib.projects.urls")),
    path("", include("geoluminate.contrib.samples.urls")),
    path("", include("geoluminate.contrib.contributors.urls")),
    path("", include("geoluminate.contrib.core.urls")),
    path("measurements/", include(measurements.urls)),
    path("", include("geoluminate.contrib.users.urls")),
    # path("dashboard/", redirect("user:profile"), name="dashboard"),
    # path('activity/', include('actstream.urls')),
    path("invitations/", include("invitations.urls", namespace="invitations")),
    path("contact/", include("django_contact_form.urls")),
    path("select2/", include("django_select2.urls")),
    path("admin/docs/", include("django.contrib.admindocs.urls")),
    path("admin/measurements/", admin_measurement_view, name="admin_measurements"),
    path("admin/", admin.site.urls),
]

urlpatterns = NON_I18N_URLS + I18N_URLS


# adds the debug toolbar to templates if installed
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns.insert(0, path("__debug__/", include(debug_toolbar.urls)))


urlpatterns += [path("", include("cms.urls"))]  # must be last
