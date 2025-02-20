from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.base import Model as Model
from django.utils.translation import gettext as _
from django.views.generic import TemplateView
from formset.views import EditCollectionView
from meta.views import MetadataMixin

from fairdm.menus import ContributorMenu
from fairdm.views import BaseCRUDView

from ..filters import ContributorFilter
from ..forms.forms import UserProfileForm
from ..models import Contributor, Person


class ContributorCRUDView(BaseCRUDView):
    model = Contributor
    form_class = UserProfileForm
    menu = ContributorMenu
    ncols = 5
    filterset_class = ContributorFilter

    def user_can_edit(self):
        user = self.request.user
        return True


class PersonCRUDView(BaseCRUDView):
    model = Person
    form_class = UserProfileForm
    menu = ContributorMenu
    ncols = 5
    filterset_class = ContributorFilter

    def user_can_edit(self):
        user = self.request.user
        return True


class AccountEdit(MetadataMixin, LoginRequiredMixin, EditCollectionView):
    template_name = "user/settings/base.html"

    def get_object(self):
        return self.request.user


class CodeOfConduct(MetadataMixin, LoginRequiredMixin, TemplateView):
    template_name = "user/agreements/code_of_conduct.html"
    title = _("Code of Conduct")

    def get_object(self):
        return self.request.user


class TermsOfUse(MetadataMixin, LoginRequiredMixin, TemplateView):
    template_name = "fairdm/pages/code_of_conduct.html"
    title = _("Terms of Use")

    def get_object(self):
        return self.request.user
