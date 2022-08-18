from cms.sitemaps import CMSSitemap
from django.contrib.gis import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from django.conf.urls.i18n import i18n_patterns

urlpatterns = i18n_patterns(
    path("sitemap.xml", sitemap, {"sitemaps": {"cmspages": CMSSitemap}}),
    path("accounts/", include("allauth.urls")),
    path('', include('user.urls')),
    path('comments/', include('fluent_comments.urls')),   
    path('taggit_autosuggest/', include('taggit_autosuggest.urls')),
    path('admin/doc/', include('django.contrib.admindocs.urls')),
    path('grappelli/', include('grappelli.urls')),
    path("admin/", admin.site.urls), 
    path('', include("cms.urls")),
)
