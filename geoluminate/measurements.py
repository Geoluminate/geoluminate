from django.urls import include, path, reverse_lazy
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView
from rest_framework_nested import routers
from simple_menu import MenuItem

from geoluminate.api.v1.viewsets import MeasurementViewset


class MeasurementRegistry:
    def __init__(self):
        self.registry = {}
        self.router = routers.SimpleRouter()

    def register(self, model, **kwargs):
        """Register a measurement schema"""
        app_label = model._meta.app_label
        model_name = slugify(model._meta.model_name)
        slug = slugify(model._meta.verbose_name)
        self.registry[model_name] = {
            "model": model,
            "view_name": f"{slugify(app_label)}-{model_name}",
            "endpoint": self.build_endpoint(model, model_name, slug, **kwargs),
            "kwargs": kwargs,
        }

    def build_view(self, model, **kwargs):
        """Builds a view from the view class."""
        return

    def build_endpoint(self, model, name, slug, **kwargs):
        """Builds an endpoint from the view class."""
        basename = name
        self.router.register(slug, MeasurementViewset(model), basename=basename)
        return basename + "-list"

    @property
    def menu(self):
        children = []
        for mtype in self.registry.values():
            children.append(
                MenuItem(
                    title=mtype["model"]._meta.verbose_name_plural.title(),
                    url=reverse_lazy(mtype["view_name"]),
                ),
            )
        return children

    def get_urls(self):
        urls = []
        for mtype in self.registry.values():
            view = TemplateView.as_view(template_name="geoluminate/placeholder.html")
            # append the plugin with the route
            urls.append(path("", view, name=mtype["view_name"]))
        return urls

    @property
    def urls(self):
        if not hasattr(self, "_urls"):
            self._urls = self.get_urls()
        return self._urls


measurements = MeasurementRegistry()
