from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.base import Model as Model
from django.views.generic.detail import SingleObjectMixin
from django_contact_form.views import ContactFormView

from geoluminate.views import BaseCRUDView

from ..forms.forms import ContributionForm
from ..models import Contributor


class ContributorContactView(LoginRequiredMixin, SingleObjectMixin, ContactFormView):
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


class ContributionCRUDView(BaseCRUDView):
    form_class = ContributionForm
    lookup_url_kwarg = "contribution_pk"

    def get_form(self, data=None, files=None, **kwargs):
        form = super().get_form(data, files, **kwargs)
        form.fields["roles"].widget.choices = self.model.CONTRIBUTOR_ROLES().choices
        return form
