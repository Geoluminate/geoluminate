from typing import Any

from auto_datatables.views import AutoTableMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import models
from django.forms import BaseModelForm, ModelForm, modelform_factory
from django.http import HttpResponse
from django.urls import resolve, reverse, reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView, ListView, TemplateView
from django.views.generic.base import ContextMixin, TemplateResponseMixin
from django.views.generic.edit import CreateView, ModelFormMixin, UpdateView
from el_pagination.views import AjaxListView
from formset.views import EditCollectionView, FormView
from meta.views import MetadataMixin

from ..forms import GenericDescriptionForm


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


class BaseDetailView(HTMXMixin, DetailView):
    navigation = []
    base_template = "core/base_detail_view.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["navigation"] = self.navigation
        return context


class ProjectBaseView(MetadataMixin, DetailView):
    slug_field = "uuid"
    slug_url_kwarg = "uuid"
    panels = []
    tables = {}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tables"] = self.tables
        context["panels"] = self.panels
        if self.object:
            context["meta"] = self.object.as_meta()
        return context

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


class DescriptionFormView(FormView):
    template_name = "core/description_form.html"
    form_class = GenericDescriptionForm
    success_url = reverse_lazy("core:home")

    def get_object(self):
        return self.request.user.profile

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["instance"] = self.get_object()
        return kwargs

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class GenericCreateView(LoginRequiredMixin, FormView, CreateView):
    def get_success_url(self):
        model_name = self.object._meta.model.__name__.lower()
        return reverse(f"{model_name}-edit", kwargs={"uuid": self.object.uuid})
