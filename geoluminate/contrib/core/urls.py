from django.urls import include, path
from django.utils.text import slugify
from django.views.generic import TemplateView

from geoluminate.utils import get_measurement_models

patterns = []
for model in get_measurement_models():
    app = model._meta.app_label
    name = model._meta.model_name
    route = f"{slugify(app)}/{slugify(name)}/"

    patterns.append(path(route, TemplateView.as_view(), name=f"{app}_{name}"))


app_name = "core"
urlpatterns = [path("measurements/", include(patterns))]
