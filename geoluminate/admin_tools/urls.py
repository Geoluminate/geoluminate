from cms.sitemaps import CMSSitemap
from django.contrib.gis import admin
from django.urls import path, include
from django.contrib.sitemaps.views import sitemap


urlpatterns = [
    # path('docs/', include('django.contrib.admindocs.urls')),
    path('grappelli/', include('grappelli.urls')),
    # path('ckeditor5/', include('django_ckeditor_5.urls')),
    path('', admin.site.urls),
]
