from allauth.account.models import EmailAddress
from allauth.socialaccount.forms import DisconnectForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.utils.translation import gettext as _
from django.views.generic import RedirectView, TemplateView
from formset.views import FormView

from geoluminate.contrib.organizations.forms import OrganisationFormCollection
from geoluminate.contrib.organizations.models import Organization
from geoluminate.views import HTMXMixin


class ProfileRedirectView(LoginRequiredMixin, RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return reverse("contributor:detail", args=(self.request.user.profile.uuid,))


class AffiliationView(HTMXMixin, FormView):
    model = Organization
    form_class = OrganisationFormCollection
    template_name = "user/edit_affiliations.html"

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data["title"] = _("Edit Affiliations")
        return context_data


# ------------------ ACCOUNT SETTINGS ------------------


class Account(LoginRequiredMixin, TemplateView):
    template_name = "user/account.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["can_add_email"] = EmailAddress.objects.can_add_email(self.request.user)
        context["forms"] = [
            (_("Password Reset"), "account/password_reset.html", DisconnectForm(request=self.request)),
        ]
        return context
