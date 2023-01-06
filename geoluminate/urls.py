from cms.sitemaps import CMSSitemap
from django.urls import path, include
from django.shortcuts import redirect
from django.contrib.sitemaps.views import sitemap
from . import views

urlpatterns = [
    path("api/", include("geoluminate.api.urls")),
]

urlpatterns += [
    path("sitemap.xml", sitemap, {"sitemaps": {"cmspages": CMSSitemap}}),
    path(
        'model-field-select2/',
        views.ModelFieldSelect2View.as_view(),
        name='geoluminate_select2'),
    path('api/', lambda request: redirect('swagger-ui', permanent=False)),
    path("accounts/", include('allauth.urls')),
    path('admin/', include('geoluminate.admin_tools.urls')),
    # path('admin/', include('smuggler.urls')),
    path('comments/', include('fluent_comments.urls')),
    path('database/', views.DatabaseTableView.as_view(), name='database_table'),
    path('database/<pk>/', views.SiteView.as_view(), name='site'),
    path('datatables/', include('datatables.urls')),
    path('glossary/', views.GlossaryView.as_view(), name='glossary'),
    path('institutions/', include('ror.urls')),
    path("invitations/", include('invitations.urls', namespace='invitations')),
    path('literature/', include('literature.urls')),
    path('rosetta/', include('rosetta.urls')),
    path("select2/", include("django_select2.urls")),
    path('viewer/', views.WorldMap.as_view(), name='viewer'),
    # path('vocabularies/', include('controlled_vocabulary.urls')),
    path('', include('user.urls')),
    path('', include("cms.urls")),
]
