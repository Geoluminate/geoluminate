import adminactions.actions as actions
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib.admin import site
from django.urls import include, path
from django.views import defaults as default_views

from geoluminate.urls import I18N_URLS, NON_I18N_URLS

# register all adminactions
actions.add_to_site(site)

urlpatterns = [
    *NON_I18N_URLS,
    *i18n_patterns(*I18N_URLS),
]

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
    path("500/", default_views.server_error),
]
