from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.views.generic import UpdateView
from extra_views import InlineFormSetView

from geoluminate.views import BaseMixin

from ..forms.collections import ProfileEditForm, UserIdentifierForm
from ..forms.person import UserProfileForm
from ..models import Identifier

helper = FormHelper()
helper = FormHelper()
helper.add_input(Submit("submit", "Save"))
helper.render_required_fields = True
helper.template = "bootstrap5/table_inline_formset.html"


class Base(BaseMixin, LoginRequiredMixin, UpdateView):
    template_name = "user/settings/base.html"
    model = get_user_model()

    def get_object(self):
        return self.request.user


class UpdateProfile(Base):
    title = _("Edit Profile")
    description = _("The following information is publicly available to all visitors of this portal.")
    form_class = UserProfileForm

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def form_invalid(self, form):
        response = super().form_invalid(form)
        return response

    def form_valid(self, form):
        response = super().form_valid(form)
        return response

    def get_success_url(self):
        return self.request.META.get("HTTP_REFERER", reverse_lazy("account-management"))  # Fallback to a default URL


class UpdateAffiliations(Base):
    template_name = "user/settings/profile_identifiers.html"
    title = _("Affiliations")
    collection_class = ProfileEditForm

    def get_object(self):
        return self.request.user


class UpdateIdentifiers(BaseMixin, InlineFormSetView):
    title = _("Persistent Identifiers")
    model = get_user_model()
    inline_model = Identifier
    form_class = UserIdentifierForm
    template_name = "user/settings/base.html"
    success_url = reverse_lazy("contributor-identifiers")
    factory_kwargs = {"extra": 1, "max_num": None, "can_order": False, "can_delete": True}

    def get_object(self):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["helper"] = helper
        return context
