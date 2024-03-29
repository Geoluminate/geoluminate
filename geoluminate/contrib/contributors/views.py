# from cms.toolbar.toolbar import CMSToolbar
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.base import Model as Model
from django.forms import BaseModelForm
from django.utils.translation import gettext as _
from django.views.generic.detail import SingleObjectMixin
from django_contact_form.views import ContactFormView

from geoluminate.contrib.core.view_mixins import ListPluginMixin
from geoluminate.utils import icon
from geoluminate.views import BaseDetailView, BaseFormView, BaseListView

from .filters import ContributorFilter
from .forms import ContributionForm, UserProfileForm
from .models import Contribution, Contributor


class ContributorListView(BaseListView):
    title = _("Contributors")
    base_template = "contributors/contributor_list.html"
    object_template = "contributors/contributor_card.html"
    model = Contributor
    filterset_class = ContributorFilter
    list_filter_top = ["name", "o"]


class ContributorDetailView(BaseDetailView):
    base_template = "contributors/contributor_detail.html"
    model = Contributor
    form_class = UserProfileForm
    sidebar_components = [
        ("contributors/sidebar/basic_info.html", "name,about"),
        ("core/sidebar/summary.html", None),
    ]

    def has_edit_permission(self):
        """Returns True if the user has permission to edit the profile. This is determined by whether the profile belongs to the current user."""
        return self.request.user.is_authenticated and self.request.user.profile == self.get_object()


class ContributorFormView(BaseFormView):
    model = Contributor
    form_class = UserProfileForm
    template_name = "contributors/contributor_form.html"

    def get_form_class(self):
        form_class = super().get_form_class()
        if fields := self.get_fields():
            # set the fields of the form to the fields specified in the query string
            # the fields must be a subset of the fields in the form
            if not all(field in form_class.Meta.fields for field in fields):
                raise ValueError("Invalid fields specified in query string.")
            form_class.Meta.fields = fields
        return form_class

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["fields"] = self.get_fields()
        return context

    def get_fields(self):
        if fields := self.request.GET.get("edit_fields"):
            return fields.split(",")

    def form_invalid(self, form):
        print("form INVALID")
        print(form.errors.as_data())

        response = super().form_invalid(form)
        return response

    def form_valid(self, form: BaseModelForm):
        self.request.htmx = False
        return super().form_valid(form)


class ContributorContactView(
    LoginRequiredMixin,
    SingleObjectMixin,
    ContactFormView,
):
    """Contact form for a contributor."""

    model = Contributor
    slug_field = "uuid"
    slug_url_kwarg = "uuid"

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    @property
    def recipient_list(self):
        email = [self.get_object().preferred_email]
        print(email)
        return email


# CONTRIBUTION VIEWS
class ContributionEditView(BaseFormView):
    model = Contribution
    form_class = ContributionForm
    title = _("Add contributor")

    def get_object(self, queryset):
        obj = super().get_object(queryset)
        contributor = obj.contributions.get(uuid=self.kwargs.get("contribution"))
        return contributor


class ContributorsPlugin(ListPluginMixin):
    template_name = "contributors/contributions_list.html"
    object_template = "contributors/contribution_card.html"
    columns = 3
    icon = icon("contributors")
    title = name = _("Contributors")
    description = _("The following personal and organizational contributors are associated with the current project.")
    # filterset_class = ContributionFilter

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["all_contributor_roles"] = Contribution.CONTRIBUTOR_ROLES
        return context

    def get_queryset(self, *args, **kwargs):
        return self.get_object().contributors.select_related("profile")
