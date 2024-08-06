from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import gettext as _
from formset.views import EditCollectionView

from geoluminate.views import BaseMixin

from ..forms.collections import ProfileEditForm, UserIdentifierForm


class Base(BaseMixin, LoginRequiredMixin, EditCollectionView):
    template_name = "user/settings/base.html"

    def get_object(self):
        return self.request.user


class UpdateProfile(Base):
    title = _("Public Profile")
    description = _("The following information is publicly available to all visitors of this portal.")
    collection_class = ProfileEditForm


class UpdateAffiliations(Base):
    template_name = "user/settings/profile_identifiers.html"
    title = _("Affiliations")
    collection_class = ProfileEditForm

    def get_object(self):
        return self.request.user


class UpdateIdentifiers(Base):
    template_name = "user/settings/profile_identifiers.html"
    collection_class = UserIdentifierForm
    title = _("Persistent Identifiers")
