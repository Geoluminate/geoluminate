from cms.sitemaps import CMSSitemap
from django.urls import path, include
from django.contrib.sitemaps.views import sitemap
from .views import (
    ModelFieldSelect2View,
    WorldMap,
    SiteView,
    DatabaseTableView
)

urlpatterns = [
    path("sitemap.xml", sitemap, {"sitemaps": {"cmspages": CMSSitemap}}),
    path(
        'model-field-select2/',
        ModelFieldSelect2View.as_view(),
        name='geoluminate_select2'),
    path('database/', DatabaseTableView.as_view(), name='database_table'),
    path('sites/', WorldMap.as_view(), name='world_map'),
    path('sites/<pk>/', SiteView.as_view(), name='site'),
    path("select2/", include("django_select2.urls")),
    path('', include('user.urls')),
    path('comments/', include('fluent_comments.urls')),
    path('admin/', include('geoluminate.admin_tools.urls')),
    path('literature/', include('literature.urls')),
    path('', include("cms.urls")),
]
