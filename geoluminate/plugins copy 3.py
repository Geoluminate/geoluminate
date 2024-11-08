from django.apps import apps
from django.db.models.base import Model as Model
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.urls import path
from django.utils.text import slugify
from django.views.generic.detail import SingleObjectTemplateResponseMixin
from flex_menu import MenuItem

from geoluminate.core.views.mixins import (
    HTMXMixin,
    MetadataMixin,
)
from geoluminate.menus import ContributorMenu, DatasetMenu, ProjectMenu, SampleMenu
from geoluminate.models import Contributor, Dataset, Project, Sample


class PluggableView(MetadataMixin, HTMXMixin, SingleObjectTemplateResponseMixin):
    menu = None
    core_mapping = {
        "p": "projects.Project",
        "d": "datasets.Dataset",
        "s": "samples.Sample",
        "m": "measurements.Measurement",
        "c": "contributors.Contributor",
    }

    def dispatch(self, request, *args, **kwargs):
        pk = self.kwargs.get("pk")
        if mtype := self.core_mapping.get(pk[0], None):
            self.base_model = apps.get_model(mtype)
        else:
            raise Http404("Object does not exist")
        if hasattr(self.base_model, "polymorphic_model_marker"):
            self.base_object = get_object_or_404(self.base_model.objects.non_polymorphic(), pk=pk)
        else:
            self.base_object = get_object_or_404(self.base_model, pk=pk)

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["base_model"] = self.base_model
        context["base_model_name"] = self.base_model._meta.verbose_name
        context["base_model_name_plural"] = self.base_model._meta.verbose_name_plural
        context["base_object"] = self.base_object
        context[self.base_model._meta.model_name] = self.base_object
        context["menu"] = self.menu
        return context


class PluginRegistry:
    """PluginRegistry is used to manage a registry of plugins for the detail view of a core obejct within the Geoluminate database. A plugin, in this context, is represented by a view class, which is a class that defines how a certain type of page or action should be displayed or handled in a web application."""

    def __init__(self, model, menu=None):
        self.base = PluggableView
        self.registry = []
        self.menu = menu
        self.model_name = model._meta.model_name

    def append_to_registry(self, view_class, name="", **kwargs):
        """Append a view to the registry."""
        name = slugify(name)
        view_name = f"{self.model_name}-{name}"
        self.registry.append(
            {
                "name": name,
                "route": f"{name}/",
                "view_class": view_class,
                "view_name": view_name,
                "kwargs": kwargs,
            }
        )
        return view_name

    def append_to_urls(self, view_class, name, **kwargs):
        """Append a view to the urls."""
        name = slugify(name)
        view_name = f"{self.model_name}-{name}"
        self.urls.append(path(f"{name}/", view_class.as_view(base=self.base, **kwargs), name=view_name))
        return view_name

    def register_page(self, view_class, name="", *args, **kwargs):
        """Register a page view and add it as an item to the page menu."""
        view_class = type(f"{view_class.__name__}Plugin", (view_class, self.base), {})
        name = name or getattr(view_class, "name", None)
        view_name = self.append_to_registry(view_class, name, **kwargs)
        # self.append_to_urls(view_class, name, **kwargs)
        self.build_menu_item(view_class, view_name, name, **kwargs)

    def page(self, *args, **kwargs):
        """Decorator to register a page view and add it as an item to the page menu.

        Usage:

        @dataset.page("overview", icon="fas fa-book-open")
        class SomeView(BaseAppView, TemplateView):
            template_name = "some_template.html"
        """

        def decorator(view_class):
            self.register_page(view_class, *args, **kwargs)
            return view_class

        return decorator

    def build_menu_item(self, view_class, view_name, name=None, **kwargs):
        """Creates a menu item from the view class."""
        name = name or getattr(view_class, "name", None)
        self.menu.append(
            MenuItem(
                name=kwargs.get("title", name),
                view_name=view_name,
                icon=kwargs.get("icon", getattr(view_class, "icon", None)),
                # check=lambda request: view_class.has_permission(request),
            )
        )

    def get_urls(self):
        urls = []
        for i, plugin in enumerate(self.registry):
            view_kwargs = plugin["kwargs"].get("view_kwargs", {})
            view_class = plugin["view_class"]
            if hasattr(view_class, "get_urls"):
                crud_urls = view_class.get_urls()
                for pattern in crud_urls:
                    pattern.name = f"{self.model_name}-{pattern.name}"
                    pattern.pattern.name = pattern.name
                    urls.append(pattern)
                # for neapolitan.views.CRUDView
                urls.extend(view_class.get_urls())
                continue
            view = plugin["view_class"].as_view(menu=self.menu, **view_kwargs)
            # duplicate the first plugin with a blank route to use as the default view
            if i == 0:
                urls.append(path("", view, name=f"{self.model_name}-detail"))
            urls.append(path(plugin["route"], view, name=plugin["view_name"]))
        return urls

    @property
    def urls(self):
        if not hasattr(self, "_urls"):
            self._urls = self.get_urls()
        return self._urls


project = PluginRegistry(model=Project, menu=ProjectMenu)

dataset = PluginRegistry(model=Dataset, menu=DatasetMenu)

sample = PluginRegistry(model=Sample, menu=SampleMenu)

contributor = PluginRegistry(model=Contributor, menu=ContributorMenu)
