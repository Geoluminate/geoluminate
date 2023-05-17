from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from geoluminate.api import PUBLIC
from geoluminate.contrib.api.serializers import HyperlinkedModelSerializer
from geoluminate.utils import get_database_models

for model in get_database_models():
    if not model.hide_from_api and not model._meta.proxy:
        # model is not a proxy model
        PUBLIC.register(model, base_serializer=HyperlinkedModelSerializer)


# PUBLIC.register(GeoluminateSite)

urlpatterns = [
    path(
        "",
        SpectacularSwaggerView.as_view(template_name="geoluminate/spectacular.html", url_name="schema"),
        name="swagger-ui",
    ),
    path("", include(PUBLIC.urls)),
    # path("", include(drf_router.urls)),
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path("auth/", include("rest_framework.urls", namespace="rest_framework")),
    path("literature/", include(("literature.api.urls", "literature"), namespace="literature_api")),
]

# urlpatterns.extend(urls)
