from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.utils.functional import cached_property

# from rest_framework.authtoken.models import Token
from django.utils.translation import gettext as _
from django.utils.translation import gettext_lazy as _
from fairdm_geo.location.utils import bbox_for_dataset
from licensing.fields import LicenseField
from shortuuid.django_fields import ShortUUIDField

from fairdm.utils.choices import Visibility

from ..vocabularies import FairDMDates, FairDMDescriptions, FairDMIdentifiers, FairDMRoles
from .abstract import AbstractDate, AbstractDescription, AbstractIdentifier, BaseModel


class Dataset(BaseModel):
    """A dataset is a collection of samples, measurements and associated metadata. The Dataset model
    is the second level model in the FairDM schema heirarchy and all geographic sites,
    samples and sample measurements MUST relate back to a dataset."""

    CONTRIBUTOR_ROLES = FairDMRoles.from_collection("Dataset")
    DATE_TYPES = FairDMDates.from_collection("Dataset")
    DESCRIPTION_TYPES = FairDMDescriptions.from_collection("Dataset")
    # IDENTIFIER_TYPES = choices.DataCiteIdentifiers
    VISIBILITY_CHOICES = Visibility

    id = ShortUUIDField(
        editable=False,
        unique=True,
        prefix="d",
        verbose_name="UUID",
        primary_key=True,
    )

    visibility = models.IntegerField(
        _("visibility"),
        choices=VISIBILITY_CHOICES,
        default=VISIBILITY_CHOICES.PRIVATE,
        help_text=_("Visibility within the application."),
    )

    # GENERIC RELATIONS
    contributors = GenericRelation("contributors.Contribution", related_query_name="dataset")

    # RELATIONS
    project = models.ForeignKey(
        "fairdm_core.Project",
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

    _metadata = {
        "title": "name",
        "description": "get_meta_description",
        "type": "research.dataset",
    }

    class Meta:
        verbose_name = _("dataset")
        verbose_name_plural = _("datasets")
        default_related_name = "datasets"
        ordering = ["modified"]

    class Config:
        form_class = "fairdm.core.forms.DatasetForm"
        fields = [
            ("name",),
        ]
        fieldsets = [
            (
                None,
                {
                    "fields": [
                        ("name",),
                    ],
                },
            ),
        ]

    @property
    def measurements(self):
        return Measurement.objects.filter(sample__dataset=self)

    @cached_property
    def bbox(self):
        return bbox_for_dataset(self)


class DatasetDescription(AbstractDescription):
    VOCABULARY = FairDMDescriptions.from_collection("Dataset")
    related = models.ForeignKey("Dataset", on_delete=models.CASCADE)


class DatasetDate(AbstractDate):
    VOCABULARY = FairDMDates.from_collection("Dataset")
    related = models.ForeignKey("Dataset", on_delete=models.CASCADE)


class DatasetIdentifier(AbstractIdentifier):
    VOCABULARY = FairDMIdentifiers()
    related = models.ForeignKey("Dataset", on_delete=models.CASCADE)


# r"""
#  _______    ___       __  .______       _______  .___  ___.
# |   ____|  /   \     |  | |   _  \     |       \ |   \/   |
# |  |__    /  ^  \    |  | |  |_)  |    |  .--.  ||  \  /  |
# |   __|  /  /_\  \   |  | |      /     |  |  |  ||  |\/|  |
# |  |    /  _____  \  |  | |  |\  \----.|  '--'  ||  |  |  |
# |__|   /__/     \__\ |__| | _| `._____||_______/ |__|  |__|
# """
