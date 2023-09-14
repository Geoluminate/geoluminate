from cms.sitemaps import CMSSitemap
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.gis import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path
from django.views.generic import TemplateView

# these URLS don't require translation capabilities
NON_I18N_URLS = [
    path("sitemap.xml", sitemap, {"sitemaps": {"cmspages": CMSSitemap}}),
    path("comments/", include("fluent_comments.urls")),
    path("api/", include("geoluminate.api.urls")),
]

I18N_URLS = [
    path(
        "public/",
        include(
            [
                path("", include("geoluminate.contrib.core.public_urls")),
                path("explorer/", TemplateView.as_view(template_name="geoluminate/pages/map.html"), name="viewer"),
                path("glossary/", include("glossary.urls")),
                path("literature/", include("literature.urls")),
            ]
        ),
    ),
    path("invitations/", include("invitations.urls", namespace="invitations")),
    # path("admin/", include("geoluminate.contrib.admin.urls")),
    path("contact/", include("django_contact_form.urls")),
    path("", include("geoluminate.contrib.user.urls")),
    path("", include("geoluminate.contrib.core.urls")),
    path("admin/docs/", include("django.contrib.admindocs.urls")),
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
