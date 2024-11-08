from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.utils.translation import gettext_lazy as _
from easy_thumbnails.fields import ThumbnailerImageField
from shortuuid.django_fields import ShortUUIDField

from geoluminate.core.choices import Visibility
from geoluminate.core.models import Abstract
from geoluminate.core.utils import default_image_path, inherited_choices_factory

from .choices import ProjectDates, ProjectDescriptions, ProjectStatus, RAiDPositions, RAiDRoles


class Project(Abstract):
    """A project is a collection of datasets and associated metadata. The Project model
    is the top level model in the Geoluminate schema hierarchy and all datasets, samples,
    and measurements should relate back to a project."""

    CONTRIBUTOR_ROLES = inherited_choices_factory("ContributorRoles", RAiDPositions, RAiDRoles)
    DATE_TYPES = ProjectDates()
    DESCRIPTION_TYPES = ProjectDescriptions()
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
    image = ThumbnailerImageField(
        verbose_name=_("image"),
        blank=True,
        null=True,
        upload_to=default_image_path,
    )
    title = models.CharField(_("title"), max_length=255)
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
    options = models.JSONField(
        verbose_name=_("options"),
        help_text=_("Item options."),
        null=True,
        blank=True,
    )

    # GENERIC RELATIONS
    descriptions = GenericRelation("core.Description")
    dates = GenericRelation("core.Date")
    identifiers = GenericRelation("core.Identifier")
    contributors = GenericRelation("contributors.Contribution")

    # RELATIONS
    owner = models.ForeignKey(
        "contributors.Organization",
        on_delete=models.PROTECT,
        related_name="owned_projects",
        verbose_name=_("owner"),
        null=True,
        blank=True,
    )
    keywords = models.ManyToManyField(
        "research_vocabs.Concept",
        verbose_name=_("keywords"),
        help_text=_("Controlled keywords for enhanced discoverability"),
        blank=True,
    )

    _metadata = {
        "title": "title",
        "description": "get_meta_description",
        "image": "get_meta_image",
        "type": "research.project",
    }

    class Meta:
        verbose_name = _("project")
        verbose_name_plural = _("projects")
        default_related_name = "projects"
        ordering = ["-modified"]
