from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import modelform_factory
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView
from django.views.generic.edit import CreateView
from formset.views import EditCollectionView, FormView
from meta.views import MetadataMixin


class ProjectBaseView(MetadataMixin, EditCollectionView):
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
    form_fields = []
    model = None
    create_button_text = _("Create new")
    creation_contributor_perms = []
    creation_contributor_roles = []

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = self.title
        context["object_list"] = self.get_queryset()
        return context

    def get_form_class(self):
        return modelform_factory(
            model=self.form_class.Meta.model,
            # form=self.form_class,
            fields=self.form_fields or self.form_class.Meta.fields,
        )

    def get_success_url(self):
        return reverse_lazy(self.success_url, kwargs={"uuid": self.object.uuid})
