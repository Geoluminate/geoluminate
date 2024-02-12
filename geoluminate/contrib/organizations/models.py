from django.utils.translation import gettext_lazy as _

# from .managers import LocationManager
from organizations.abstract import (
    AbstractOrganization,
    AbstractOrganizationInvitation,
    AbstractOrganizationOwner,
    AbstractOrganizationUser,
)

from geoluminate import models


class Organization(AbstractOrganization):
    """Core organization model"""

    data = models.JSONField(
        verbose_name=_("data"),
        help_text=_("JSON format respresentation of the organization after the ROR schema."),
        default=dict,
    )

    class Meta:
        default_related_name = "affiliations"


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
