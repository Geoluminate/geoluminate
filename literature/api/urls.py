from .views import LiteratureView, AuthorListView, CoreNestedViewSet
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from geoluminate.utils import DATABASE
from django.utils.text import slugify


router = DefaultRouter()
router.register(r'literature', LiteratureView)
router.register(r'authors', AuthorListView)


lit_router = routers.NestedSimpleRouter(
    router, r'literature', lookup='lit')
lit_router.register(
    slugify(DATABASE._meta.verbose_name),
    CoreNestedViewSet,
    basename='literature-core')
# lit = routers.NestedSimpleRouter(router, r'clients', lookup='client')
# core_router.register(r'maildrops', MailDropViewSet, basename='maildrops')
