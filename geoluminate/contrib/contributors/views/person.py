from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import gettext as _
from django.views.generic import TemplateView
from formset.views import EditCollectionView

from geoluminate.views import BaseMixin


class AccountEdit(BaseMixin, LoginRequiredMixin, EditCollectionView):
    template_name = "user/settings/base.html"

    def get_object(self):
        return self.request.user


class CodeOfConduct(BaseMixin, LoginRequiredMixin, TemplateView):
    template_name = "user/agreements/code_of_conduct.html"
    title = _("Code of Conduct")

    def get_object(self):
        return self.request.user


class TermsOfUse(BaseMixin, LoginRequiredMixin, TemplateView):
    template_name = "geoluminate/generic/code_of_conduct.html"
    title = _("Terms of Use")

    def get_object(self):
        return self.request.user
