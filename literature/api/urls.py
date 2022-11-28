from .views import LiteratureView, AuthorView, CoreNestedViewSet, NestedAuthorList
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers

router = DefaultRouter()
router.register('literature', LiteratureView)
router.register('authors', AuthorView)


lit_router = routers.NestedSimpleRouter(router, r'literature', lookup='lit')
lit_router.register('data', CoreNestedViewSet, basename='literature-data')
lit_router.register('authors', NestedAuthorList, basename='literature-authors')
