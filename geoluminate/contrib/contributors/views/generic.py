from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.base import Model as Model
from django.urls import reverse
from django.utils.translation import gettext as _
from django.views.generic.detail import SingleObjectMixin
from django_contact_form.views import ContactFormView

from geoluminate.core.views.mixins import ListPluginMixin
from geoluminate.views import BaseDetailView, BaseEditView, BaseListView

from ..filters import ContributorFilter
from ..forms.forms import ContributionForm, UserProfileForm
from ..models import Contributor


class ContributorListView(BaseListView):
    title = _("Contributors")
    base_template = "contributors/contributor_list.html"
    object_template = "contributors/contributor_row.html"
    queryset = Contributor.objects.non_polymorphic()
    filterset_class = ContributorFilter
    list_filter_top = ["name", "o"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["object_template"] = self.object_template
        return context


class ContributorDetailView(BaseDetailView):
    base_template = "contributors/contributor_detail.html"
    model = Contributor
    form_class = UserProfileForm
    sidebar_components = [
        ("contributors/sidebar/basic_info.html", "name,about"),
        ("core/sidebar/summary.html", None),
    ]
    extra_context = {
        "menu": "ContributorDetailMenu",
    }

    def get_object(self):
        # note: we are using base_objects here to get the base model (Sample) instance
        obj = self.base.model.base_objects.get(pk=self.kwargs.get("pk"))
        self.real = obj.get_real_instance()
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["real"] = self.real
        context[self.real._meta.model_name] = self.real
        base_fields = [f.name for f in self.base.model._meta.fields]
        context["additional_fields"] = [f.name for f in self.real._meta.fields if f.name not in base_fields]
        if "sample_ptr" in context["additional_fields"]:
            context["additional_fields"].remove("sample_ptr")
        # context["sidebar_fields"] = self.get_sidebar_fields(self.real.__class__)
        return context

    def has_edit_permission(self):
        """Returns True if the user has permission to edit the profile. This is determined by whether the profile belongs to the current user."""
        return self.request.user.is_authenticated and self.request.user == self.get_object()


class ContributorFormView(BaseEditView):
    model = Contributor
    form_class = UserProfileForm
    template_name = "contributors/contributor_form.html"


class ContributorContactView(
    LoginRequiredMixin,
    SingleObjectMixin,
    ContactFormView,
):
    """Contact form for a contributor."""

    model = Contributor

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    @property
    def recipient_list(self):
        email = [self.get_object().preferred_email]
        return email


class ContributorsPlugin(ListPluginMixin):
    template_name = "contributors/contribution_list.html"
    object_template = "contributors/contribution_card.html"
    icon = "contributors"
    title = name = _("Contributors")
    # filterset_class = ContributionFilter

    def get_queryset(self, *args, **kwargs):
        self.related_object = self.get_object()
        return self.related_object.contributions.all()

    def get_create_url(self):
        # return Contribution().get_create_url(self.kwargs)
        # letter = self.base.model._meta.model_name[0]
        # return reverse("contribution-create", kwargs={**self.kwargs, "model": letter})
        return reverse("contribution-create", kwargs={**self.kwargs})


class ContributionCRUDView(BaseEditView):
    title = _("Update contributor")
    # model = AbstractContribution
    form_class = ContributionForm
    lookup_url_kwarg = "contribution_pk"
    # url_base = "contribution"
    related_name = "object"

    def get_form(self, data=None, files=None, **kwargs):
        form = super().get_form(data, files, **kwargs)
        form.fields["roles"].widget.choices = self.model.CONTRIBUTOR_ROLES().choices
        return form
