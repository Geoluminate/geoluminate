import random

# from django.contrib.gis.db.models import Collect
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFit
from licensing.fields import LicenseField
from research_vocabs.fields import ConceptField

from geoluminate.contrib.core.choices import Visibility
from geoluminate.contrib.core.models import (
    Abstract,
    AbstractContribution,
    AbstractDate,
    AbstractDescription,
    AbstractIdentifier,
)
from geoluminate.contrib.projects.choices import ProjectDates
from geoluminate.db import models

from . import choices
from .datacite import DataCiteIdentifiers


def dataset_image_path(instance, filename):
    """Returns the path to the image file for the dataset."""
    return f"datasets/{instance.pk}/cover-image.webp"


class Dataset(Abstract):
    """A dataset is a collection of samples, measurements and associated metadata. The Dataset model
    is the second level model in the Geoluminate schema heirarchy and all geographic sites,
    samples and sample measurements MUST relate back to a dataset."""

    VISIBILITY_CHOICES = Visibility

    project = models.ForeignKey(
        "projects.Project",
        verbose_name=_("project"),
        help_text=_("The project that this dataset belongs to."),
        related_name="datasets",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )

    image = ProcessedImageField(
        verbose_name=_("image"),
        # help_text=_("Upload an image that represents your project."),
        processors=[ResizeToFit(1200, 630)],
        format="WEBP",
        options={"quality": 80},
        blank=True,
        null=True,
        upload_to=dataset_image_path,
    )
    title = models.CharField(_("title"), max_length=255)
    reference = models.OneToOneField(
        "literature.LiteratureItem",
        help_text=_(
            "The data publication to which this dataset belongs. If the dataset has not been formally published, leave"
            " this field blank."
        ),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    related_literature = models.ManyToManyField(
        "literature.LiteratureItem",
        help_text=_("Any literature that is related to this dataset."),
        related_name="related_datasets",
        related_query_name="related_dataset",
        blank=True,
    )

    contributors = models.ManyToManyField(
        "contributors.Contributor",
        verbose_name=_("contributors"),
        help_text=_("The contributors to this dataset."),
        related_query_name="dataset",
        through="datasets.Contribution",
        blank=True,
    )

    license = LicenseField(null=True, blank=True)

    visibility = models.IntegerField(
        _("visibility"),
        choices=VISIBILITY_CHOICES,
        default=VISIBILITY_CHOICES.PRIVATE,
        help_text=_("Visibility within the application."),
    )

    _metadata = {
        "title": "title",
        "description": "get_meta_description",
        "type": "research.dataset",
    }

    class Meta:
        verbose_name = _("dataset")
        verbose_name_plural = _("datasets")
        default_related_name = "datasets"

    @property
    def resource_type(self):
        """Returns the resource type as per the DataCite schema. Geoluminate datasets are always of type 'Dataset'."""
        return "Dataset"

    @property
    def locations(self):
        return self.samples.prefetch_related("location").values("location__point")

    # @cached_property
    # def GeometryCollection(self):
    #     """Returns a GeometryCollection of all the samples in the dataset"""
    #     return self.locations.aggregate(collection=Collect("location__point"))["collection"]

    # @cached_property
    # def centroid(self):
    #     """Returns the centroid of the dataset as a Point"""
    #     return self.GeometryCollection.centroid

    # @cached_property
    # def bbox(self):
    #     """Returns the bounding box of the dataset as a list of coordinates in the format [xmin, ymin, xmax, ymax]."""
    #     return self.GeometryCollection.extent

    @cached_property
    def status(self):
        return random.choice(["In progress", "Completed", "Accepted", "Published"])

    def get_status_display(self):
        return self.status


class Description(AbstractDescription):
    type = ConceptField(verbose_name=_("type"), vocabulary=choices.DatasetDescriptions)
    object = models.ForeignKey(to=Dataset, on_delete=models.CASCADE)


class Date(AbstractDate):
    type = ConceptField(verbose_name=_("type"), vocabulary=ProjectDates)

    object = models.ForeignKey(to=Dataset, on_delete=models.CASCADE)


class Identifier(AbstractIdentifier):
    IdentifierLookup = {}
    SCHEME_CHOICES = DataCiteIdentifiers
    scheme = models.CharField(_("scheme"), max_length=16, choices=SCHEME_CHOICES)
    object = models.ForeignKey(to=Dataset, on_delete=models.CASCADE)


class Contribution(AbstractContribution):
    """A contribution to a project."""

    CONTRIBUTOR_ROLES = choices.DataciteContributorRoles()

    object = models.ForeignKey(
        Dataset,
        on_delete=models.CASCADE,
        related_name="contributions",
        verbose_name=_("dataset"),
    )
