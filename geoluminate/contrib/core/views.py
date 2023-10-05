from auto_datatables.views import AutoTableMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import include, path, resolve, reverse, reverse_lazy
from django.utils.decorators import classonlymethod
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView, ListView, TemplateView
from django.views.generic.base import ContextMixin, TemplateResponseMixin
from django.views.generic.edit import CreateView
from el_pagination.views import AjaxListView
from formset.views import FormView
from meta.views import MetadataMixin

from .forms import GenericDescriptionForm


class HTMXBase:
    base_template = ""

    def get_base_template(self, **kwargs):
        requesting_app_name = self.request.resolver_match.app_name
        names = [f"{requesting_app_name}/base.html", "base.html"]
        if self.base_template:
            names.insert(0, self.base_template)
        return names

    def get_template_names(self):
        if self.request.htmx:
            htmx_template = super().get_template_names()[0]
            return htmx_template
        names = self.get_base_template()
        return names

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["template_name"] = super().get_template_names()
        return context


class HTMXMixin(TemplateResponseMixin, ContextMixin):
    base_template = ""

    def get_base_template(self, **kwargs):
        requesting_app_name = self.request.resolver_match.app_name
        names = [f"{requesting_app_name}/base.html", "base.html"]
        if self.base_template:
            names.insert(0, self.base_template)
        return names

    def get_template_names(self):
        if self.request.htmx:
            htmx_template = super().get_template_names()[0]
            return htmx_template
        names = self.get_base_template()
        return names

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["template_name"] = super().get_template_names()
        return context


class CoreListView(HTMXMixin, AjaxListView):
    object_template = ""
    object_template_suffix = "_card"
    template_name = "core/object_list.html"
    page_template = "core/object_list_page.html"
    object_template = "core/object.html"
    base_template = "core/base_list.html"

    def get_object_template(self, **kwargs):
        """Return the template name used for each object in the object_list for loop."""
        opts = self.object_list.model._meta
        return (
            f"{opts.app_label}/{opts.object_name.lower()}{self.template_name_suffix}{self.object_template_suffix}.html"
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["object_template"] = self.object_template or self.get_object_template()
        return context


list_view = CoreListView.as_view


class HTMXListView(ListView):
    page_template_suffix = "_page"
    page_template = ""
    base_template = ""

    def get_page_template(self, **kwargs):
        """Return the template name used for this request.

        Only called if *page_template* is not given as a kwarg of
        *self.as_view*.
        """
        meta = self.object_list.model._meta
        return f"{meta.app_label}/{meta.object_name.lower()}{self.template_name_suffix}{self.page_template_suffix}.html"

    def get_base_template(self, **kwargs):
        opts = self.object_list.model._meta
        model_app_name = opts.app_label
        requesting_app_name = self.request.resolver_match.app_name

        template_name = f"{opts.model_name}{self.template_name_suffix}"

        names = [
            f"{requesting_app_name}/{template_name}_base.html",
            f"{requesting_app_name}/base{self.template_name_suffix}.html",
            f"{model_app_name}/{template_name}_base.html",
            f"{model_app_name}/base{self.template_name_suffix}.html",
        ]
        return names

    def get_template_names(self):
        """Switch the templates for HTMX requests."""
        if self.request.htmx:
            print("HTMX request")
            # retrieve only the partial page template
            page_template = self.page_template or self.get_page_template()
            print("Page template:", page_template)
            return page_template
        names = super().get_template_names()
        print("Base template:", names)
        return names

    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.GET.get("contributor_only"):
            qs = qs.filter(contributors__profile=self.request.user.profile)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_template"] = self.get_page_template()
        return context


class BaseListView(ListView, AutoTableMixin):
    table = None
    filter = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filter"] = self.filter
        context["table"] = self.table
        context["title"] = self.model._meta.verbose_name_plural.title()
        return context


class BaseDetailView(MetadataMixin, HTMXMixin, DetailView):
    navigation = []
    slug_field = "uuid"
    slug_url_kwarg = "uuid"
    app_name = ""
    view_name = ""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["navigation"] = self.get_navigation()
        return context

    def get_navigation(self):
        nav = []
        for item in self.navigation:
            item = {k: v for k, v in zip(["icon", "title", "template_name"], item)}
            view_name = self.view_name
            if self.app_name:
                view_name = f"{self.app_name}:{view_name}"
            item["url"] = reverse_lazy(view_name, kwargs={"uuid": self.object.uuid})
            nav.append(item)
            print(item)
        return nav

    @classonlymethod
    def as_view(cls, **initkwargs):
        # instead of adding a single view, loop through the navigation and create a view and a path for each item.
        # We will then return a list of paths than can be dropped into a url conf.
        prefix = initkwargs.pop("prefix", cls.model._meta.model_name)
        view_name = initkwargs.pop("name", f"{prefix}-detail")
        extra_context = initkwargs.pop("extra_context", {})
        urls = []
        for i, item in enumerate(cls.navigation):
            # item = (icon, title, template_name)

            item = {k: v for k, v in zip(["icon", "title", "template_name"], item)}
            name = slugify(item["title"])
            item["view_name"] = f"{prefix}-{name}"
            view = super().as_view(
                template_name=item.get("template_name", ""),
                view_name=item["view_name"],
                **initkwargs,
                extra_context={**extra_context, **item},
            )
            if i == 0:
                urls.append(path("", view, name=view_name))
            urls.append(path(name + "/", view, name=item["view_name"]))

        return include(urls)


class ProjectBaseView(MetadataMixin, DetailView):
    slug_field = "uuid"
    slug_url_kwarg = "uuid"
    panels = []
    tables = {}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tables"] = self.tables
        context["panels"] = self.get_panels()
        if self.object:
            context["meta"] = self.object.as_meta()
        return context

    def get_panels(self):
        panels = []
        for panel in self.panels:
            panels.append(
                {
                    k: v
                    for k, v in zip(
                        [
                            "icon",
                            "title",
                            "template_name",
                        ],
                        panel,
                    )
                }
            )
        return panels

    def get_queryset(self):
        return super().get_queryset().prefetch_related("contributors")


class MapView(HTMXMixin, TemplateView):
    template_name = "core/map.html"

    def get_geojson(self):
        raise NotImplementedError

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["geojson"] = self.get_geojson()
        return context


class DescriptionFormView(DetailView, FormView):
    template_name = "core/description_form.html"
    form_class = GenericDescriptionForm
    success_url = "/"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # if getattr(self, "object", None):
        kwargs["content_object"] = self.get_object()
        return kwargs

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class GenericCreateView(LoginRequiredMixin, HTMXMixin, FormView, CreateView):
    base_template = "base_create_view.html"
    template_name = "core/base_form.html"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # kwargs["obj"] = self.object
        return kwargs

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        response = super().form_valid(form)
        # add the current user a contributor with the Project Leader and Contact Person roles
        if hasattr(self.object, "contributors"):
            self.object.contributors.create(profile=self.request.user.profile, roles="ProjectLeader,ContactPerson")
        return response

    def get_success_url(self):
        model_name = self.object._meta.model.__name__.lower()
        return reverse(f"{model_name}-edit", kwargs={"uuid": self.object.uuid})


create_view = GenericCreateView.as_view
