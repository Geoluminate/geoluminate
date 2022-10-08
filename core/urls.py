from cms.sitemaps import CMSSitemap
from django.contrib.gis import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from django.conf.urls.i18n import i18n_patterns

urlpatterns = [
    path("sitemap.xml", sitemap, {"sitemaps": {"cmspages": CMSSitemap}}),
    path("accounts/", include("allauth.urls")),
    path('', include('user.urls')),
    path('comments/', include('fluent_comments.urls')),   
    path('taggit_autosuggest/', include('taggit_autosuggest.urls')),
    path('admin/doc/', include('django.contrib.admindocs.urls')),
    path('grappelli/', include('grappelli.urls')),
    path("ckeditor5/", include('django_ckeditor_5.urls')),
    path("admin/", admin.site.urls), 
    path('literature/', include('publications.urls')),
    path('', include("cms.urls")),
]
