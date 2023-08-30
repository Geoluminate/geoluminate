from cms.sitemaps import CMSSitemap
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path
from django.utils.text import slugify
from django.views import defaults as default_views
from django.views.generic import TemplateView

from geoluminate.admin import admin_site
from geoluminate.contrib.user import views
from geoluminate.views import placeholder_view

PUBLIC_URL = slugify(settings.GEOLUMINATE["database"]["acronym"]) + "/"

# these URLS don't require translation capabilities
NON_I18N_URLS = [
    path("sitemap.xml", sitemap, {"sitemaps": {"cmspages": CMSSitemap}}),
    path("comments/", include("fluent_comments.urls")),
    path("api/", include("geoluminate.contrib.api.urls")),
    # path("vocabularies/", include("controlled_vocabulary.urls")),
]

I18N_URLS = [
    path(
        PUBLIC_URL,
        include(
            [
                path("", include("geoluminate.contrib.project.public_urls")),
                path("explorer/", TemplateView.as_view(template_name="geoluminate/components/map.html"), name="viewer"),
                path("glossary/", include("glossary.urls")),
                path("literature/", include("literature.urls")),
            ]
        ),
    ),
    path("invitations/", include("invitations.urls", namespace="invitations")),
    path("admin/", include("geoluminate.contrib.admin.urls")),
    path("contact/", include("django_contact_form.urls")),
    path("", include("geoluminate.contrib.user.urls")),
    path("", include("geoluminate.contrib.project.urls")),
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
