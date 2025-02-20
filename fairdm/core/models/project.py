from django.contrib.contenttypes.fields import GenericRelation
from django.db import models

# from rest_framework.authtoken.models import Token
from django.utils.translation import gettext as _
from django.utils.translation import gettext_lazy as _
from shortuuid.django_fields import ShortUUIDField

from fairdm.utils.choices import Visibility

from ..choices import ProjectStatus
from ..vocabularies import FairDMDates, FairDMDescriptions, FairDMIdentifiers, FairDMRoles
from .abstract import AbstractDate, AbstractDescription, AbstractIdentifier, BaseModel


class Project(BaseModel):
    """A project is a collection of datasets and associated metadata. The Project model
    is the top level model in the FairDM schema hierarchy and all datasets, samples,
    and measurements should relate back to a project."""

    CONTRIBUTOR_ROLES = FairDMRoles.from_collection("Project")
    DATE_TYPES = FairDMDates.from_collection("Project")
    DESCRIPTION_TYPES = FairDMDescriptions.from_collection("Project")
    # IDENTIFIER_TYPES = choices.DataCiteIdentifiers
    STATUS_CHOICES = ProjectStatus
    VISIBILITY = Visibility

    id = ShortUUIDField(
        editable=False,
        unique=True,
        prefix="p",
        verbose_name="UUID",
        primary_key=True,
    )

    visibility = models.IntegerField(
        _("visibility"),
        choices=VISIBILITY,
        default=VISIBILITY.PRIVATE,
        help_text=_("Visibility within the application."),
    )
    funding = models.JSONField(
        verbose_name=_("funding"),
        help_text=_("Related funding information."),
        null=True,
        blank=True,
    )
    status = models.IntegerField(_("status"), choices=STATUS_CHOICES, default=STATUS_CHOICES.CONCEPT)
    contributors = GenericRelation("contributors.Contribution")

    # RELATIONS
    owner = models.ForeignKey(
        "contributors.Organization",
        help_text=_("The organization that owns the project."),
        on_delete=models.PROTECT,
        related_name="owned_projects",
        verbose_name=_("owner"),
        null=True,
        blank=True,
    )

    _metadata = {
        "title": "name",
        "description": "get_meta_description",
        "image": "get_meta_image",
        "type": "research.project",
    }

    class Meta:
        verbose_name = _("project")
        verbose_name_plural = _("projects")
        default_related_name = "projects"
        ordering = ["-modified"]


class ProjectDescription(AbstractDescription):
    VOCABULARY = FairDMDescriptions.from_collection("Project")
    related = models.ForeignKey("Project", on_delete=models.CASCADE)


class ProjectDate(AbstractDate):
    VOCABULARY = FairDMDates.from_collection("Project")
    related = models.ForeignKey("Project", on_delete=models.CASCADE)


class ProjectIdentifier(AbstractIdentifier):
    VOCABULARY = FairDMIdentifiers()
    related = models.ForeignKey("Project", on_delete=models.CASCADE)
