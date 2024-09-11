from django.db import models
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFit
from research_vocabs.fields import ConceptField

from geoluminate.core.choices import Visibility
from geoluminate.core.models import Abstract, AbstractContribution, AbstractDate, AbstractDescription
from geoluminate.core.utils import inherited_choices_factory

# from geoluminate.utils import icon
from .choices import ProjectDates, ProjectDescriptions, ProjectStatus, RAiDPositions, RAiDRoles


def project_image_path(instance, filename):
    """Returns the path to the image file for the project."""
    return f"projects/{instance.pk}/cover-image.webp"


class Project(Abstract):
    """A project is a collection of datasets and associated metadata. The Project model
    is the top level model in the Geoluminate schema hierarchy and all datasets, samples,
    and measurements should relate back to a project."""

    VISIBILITY = Visibility
    DESCRIPTION_TYPES = ProjectDescriptions

    STATUS_CHOICES = ProjectStatus

    # RAiD core metadata fields
    owner = models.ForeignKey(
        "organizations.Organization",
        on_delete=models.PROTECT,
        related_name="owned_projects",
        verbose_name=_("owner"),
        null=True,
        blank=True,
    )

    image = ProcessedImageField(
        verbose_name=_("image"),
        # help_text=_("Upload an image that represents your project."),
        processors=[ResizeToFit(1200, 630)],
        format="WEBP",
        options={"quality": 80},
        blank=True,
        null=True,
        upload_to=project_image_path,
    )
    title = models.CharField(_("title"), max_length=255)
    contributors = models.ManyToManyField(
        "contributors.Contributor",
        through="projects.Contribution",
        verbose_name=_("contributors"),
        help_text=_("The contributors to this project."),
    )

    funding = models.JSONField(
        verbose_name=_("funding"),
        help_text=_("Related funding information."),
        null=True,
        blank=True,
    )

    visibility = models.IntegerField(
        _("visibility"),
        choices=VISIBILITY,
        default=VISIBILITY.PRIVATE,
        help_text=_("Visibility within the application."),
    )

    # Geoluminate specific fields
    status = models.IntegerField(_("status"), choices=STATUS_CHOICES, default=STATUS_CHOICES.CONCEPT)

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

    @property
    def locations(self):
        """Returns a queryset of all locations associated with samples related to this project."""
        # this might need a distinct call
        return self.datasets.prefetch_related("samples__location").annotate(geom=models.F("samples__location__point"))

    @cached_property
    def GeometryCollection(self):
        """Returns a GeometryCollection of all the samples in the dataset"""
        return self.locations.aggregate(collection=models.Collect("geom"))["collection"]

    @cached_property
    def bbox(self):
        """Returns the bounding box of the dataset as a list of coordinates in the format [xmin, ymin, xmax, ymax]."""
        return self.GeometryCollection.extent

    @classmethod
    def contributor_roles(cls):
        return Contribution.CONTRIBUTOR_ROLES

    def get_summary(self):
        """Used to fill out the summary panel in the project detail view sidebar."""
        summary = [
            {
                "label": _("Total datasets"),
                "value": self.datasets.count(),
                "icon": "dataset",
            },
            {
                "label": _("Unique locations"),
                "value": self.datasets.filter(samples__location__isnull=False).count(),
                "icon": "location",
            },
            {
                "label": _("Samples collected"),
                "value": self.datasets.filter(samples__isnull=False).count(),
                "icon": "sample",
            },
            # {
            #     "label": _("Measurements made"),
            #     "value": self.datasets.filter(samples__measurements=False).count(),
            #     "icon": "measurement",
            # },
        ]
        return summary

    def add_contributors(self, *profiles, roles=None):
        """Adds the given profiles as contributors to the object."""
        for profile in profiles:
            self.contributors.create(profile=profile, roles=roles)

    def in_progress(self):
        """Returns True if the project is in progress"""
        return self.status == self.STATUS_CHOICES.IN_PROGRESS


class Description(AbstractDescription):
    type = ConceptField(verbose_name=_("type"), vocabulary=ProjectDescriptions)
    object = models.ForeignKey(to=Project, on_delete=models.CASCADE)


class Date(AbstractDate):
    type = ConceptField(verbose_name=_("type"), vocabulary=ProjectDates)
    object = models.ForeignKey(to=Project, on_delete=models.CASCADE)


class Contribution(AbstractContribution):
    """A contribution to a project."""

    RAID_POSITIONS = RAiDPositions
    RAID_ROLES = RAiDRoles

    CONTRIBUTOR_ROLES = inherited_choices_factory("ContributorRoles", RAID_POSITIONS, RAID_ROLES)

    object = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="contributions",
        verbose_name=_("project"),
    )

    # roles = ArrayField(
    #     models.CharField(
    #         max_length=len(max(CONTRIBUTOR_ROLES.values, key=len)),
    #         choices=CONTRIBUTOR_ROLES.choices,
    #     ),
    #     verbose_name=_("roles"),
    #     help_text=_("Assigned roles for this contributor."),
    #     size=len(CONTRIBUTOR_ROLES.choices),
    # )
