from django.db import models
from django.utils.translation import gettext_lazy as _
from model_utils import FieldTracker
from organizations.abstract import AbstractOrganizationInvitation, AbstractOrganizationOwner, AbstractOrganizationUser
from organizations.base import OrganizationBase, OrgMeta
from polymorphic.models import PolymorphicModelBase

from geoluminate.contrib.contributors.models import Contributor


class PolymorphicOrgMeta(OrgMeta, PolymorphicModelBase):
    pass


class Organization(Contributor, OrganizationBase, metaclass=PolymorphicOrgMeta):
    """Core organization model"""

    # location = None
    # types = []
    # domains = []
    # city = ""
    # country = ""
    # external_ids
    # links = []

    data = models.JSONField(
        verbose_name=_("data"),
        help_text=_("JSON format respresentation of the organization after the ROR schema."),
        default=dict,
    )
    tracker = FieldTracker()

    class Meta:
        default_related_name = "affiliations"

    def save(self, *args, **kwargs):
        if self.tracker.has_changed("data"):
            self.name = self.data.get("name", self.name)
        super().save(*args, **kwargs)


class Membership(AbstractOrganizationUser):
    """Links a user to an organization"""

    class Meta:
        verbose_name = _("membership")
        verbose_name_plural = _("memberships")


class Manager(AbstractOrganizationOwner):
    """Identifies a single user to manage an Organization"""

    class Meta:
        verbose_name = _("manager")
        verbose_name_plural = _("managers")


class Invitation(AbstractOrganizationInvitation):
    """Stores invitations for adding users to organizations"""

    class Meta:
        verbose_name = _("invitation")
        verbose_name_plural = _("invitations")
