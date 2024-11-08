from django.contrib.contenttypes.fields import GenericRelation
from django.utils.translation import gettext_lazy as _
from easy_thumbnails.fields import ThumbnailerImageField
from licensing.fields import LicenseField
from shortuuid.django_fields import ShortUUIDField

from geoluminate.contrib.measurements.models import Measurement
from geoluminate.core.choices import Visibility
from geoluminate.core.models import Abstract
from geoluminate.core.utils import default_image_path
from geoluminate.db import models

from . import choices


class Dataset(Abstract):
    """A dataset is a collection of samples, measurements and associated metadata. The Dataset model
    is the second level model in the Geoluminate schema heirarchy and all geographic sites,
    samples and sample measurements MUST relate back to a dataset."""

    CONTRIBUTOR_ROLES = choices.DataciteContributorRoles()
    DATE_TYPES = choices.DatasetDates()
    DESCRIPTION_TYPES = choices.DatasetDescriptions()
    IDENTIFIER_TYPES = choices.DataCiteIdentifiers
    VISIBILITY_CHOICES = Visibility

    id = ShortUUIDField(
        editable=False,
        unique=True,
        prefix="d",
        verbose_name="UUID",
        primary_key=True,
    )
    image = ThumbnailerImageField(
        verbose_name=_("image"),
        blank=True,
        null=True,
        upload_to=default_image_path,
    )
    title = models.CharField(_("title"), help_text=_("The title of the dataset."), max_length=255)
    visibility = models.IntegerField(
        _("visibility"),
        choices=VISIBILITY_CHOICES,
        default=VISIBILITY_CHOICES.PRIVATE,
        help_text=_("Visibility within the application."),
    )

    # GENERIC RELATIONS
    descriptions = GenericRelation("core.Description")
    dates = GenericRelation("core.Date")
    identifiers = GenericRelation("core.Identifier")
    contributors = GenericRelation("contributors.Contribution", related_query_name="dataset")

    # RELATIONS
    project = models.ForeignKey(
        "projects.Project",
        verbose_name=_("project"),
        help_text=_("The project associated with the dataset."),
        related_name="datasets",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    reference = models.OneToOneField(
        "literature.LiteratureItem",
        help_text=_("The data publication associated with this dataset."),
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
    license = LicenseField(null=True, blank=True)
    keywords = models.ManyToManyField(
        "research_vocabs.Concept",
        verbose_name=_("keywords"),
        help_text=_("Controlled keywords for enhanced discoverability"),
        blank=True,
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

    def measurements(self):
        return Measurement.objects.filter(sample__dataset=self)
