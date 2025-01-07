from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.base import Model as Model
from django.utils.translation import gettext as _
from django.views.generic import TemplateView
from formset.views import EditCollectionView

from geoluminate.menus import ContributorMenu
from geoluminate.views import BaseCRUDView, MetadataMixin

from ..filters import ContributorFilter
from ..forms.forms import UserProfileForm
from ..models import Contributor, Person


class ContributorCRUDView(BaseCRUDView):
    model = Contributor
    form_class = UserProfileForm
    menu = ContributorMenu
    ncols = 5
    filterset_class = ContributorFilter
    sidebar_fields = [
        (
            _("Basic Information"),
            {
                "fields": ["name", "created", "modified"],
            },
        ),
    ]


class PersonCRUDView(BaseCRUDView):
    model = Person
    form_class = UserProfileForm
    menu = ContributorMenu
    ncols = 5
    filterset_class = ContributorFilter
    sidebar_fields = [
        (
            _("Basic Information"),
            {
                "fields": ["name", "created", "modified"],
            },
        ),
    ]


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
    template_name = "geoluminate/generic/code_of_conduct.html"
    title = _("Terms of Use")

    def get_object(self):
        return self.request.user
