from typing import Any

from auto_datatables.views import AutoTableMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import models
from django.forms import ModelForm, modelform_factory
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView, ListView, TemplateView
from django.views.generic.edit import CreateView
from formset.views import EditCollectionView, FormView
from meta.views import MetadataMixin


class BaseListView(ListView, AutoTableMixin):
    table = None
    filter = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filter"] = self.filter
        context["table"] = self.table
        context["title"] = self.model._meta.verbose_name_plural.title()
        return context


class ProjectBaseView(MetadataMixin, DetailView):
    slug_field = "uuid"
    slug_url_kwarg = "uuid"
    contributor_key = ""
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


class ContributionView(LoginRequiredMixin, FormView, CreateView):
    """A view that lists associated objects and allows for adding new ones."""

    title = ""
    model = None  # must be the model used to collect a list of objects
    form_fields = []
    form_class = ModelForm  # must be a model form where Meta.model is the model to be created against the object
    create_button_text = _("Create new")
    creator_perms = []
    creator_roles = []

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = self.title
        context["object_list"] = self.get_related_objects()
        return context

    def get_form_class(self):
        """Create a new form class using only the specified form fields."""
        fields = ["title", "project"]
        return modelform_factory(
            model=self.form_class.Meta.model,
            form=self.form_class,
            fields=self.form_fields or self.form_class.Meta.fields,
        )

    def get_related_objects(self):
        """Return a queryset of all objects associated with the Project object."""
        return self.get_object().get_projects()

    def get_success_url(self):
        return reverse_lazy(self.success_url, kwargs={"uuid": self.object.uuid})

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # kwargs["instance"] = Project(
        #     contributors=[self.get_object()],
        # )
        return kwargs


class Example(ContributionView):
    # model = Project  # for the list of objects
    # add_form = DatasetForm
    add_form_fields = ["title"]
