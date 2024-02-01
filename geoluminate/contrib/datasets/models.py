import random

from django.conf import settings
from django.contrib.gis.db.models import Collect
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _

from geoluminate import models
from geoluminate.contrib.core.models import Abstract

from . import choices


class Dataset(Abstract):
    """A dataset is a collection of samples, measurements and associated metadata. The Dataset model
    is the second level model in the Geoluminate schema heirarchy and all geographic sites,
    samples and sample measurements MUST relate back to a dataset."""

    DESCRIPTION_TYPES = choices.DataCiteDescriptionTypes

    reference = models.OneToOneField(
        "literature.Literature",
        help_text=_(
            "The data publication to which this dataset belongs. If the dataset has not been formally published, leave"
            " this field blank."
        ),
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )
    related_literature = models.ManyToManyField(
        "literature.Literature",
        help_text=_("Any literature that is related to this dataset."),
        related_name="related_datasets",
        related_query_name="related_dataset",
        blank=True,
    )
    project = models.ForeignKey(
        "projects.Project",
        verbose_name=_("project"),
        help_text=_("The project that this dataset belongs to."),
        related_name="datasets",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )

    # to be set when a reviewer marks this as complete
    approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        help_text=_("The user who approved this dataset."),
        null=True,
        blank=True,
        related_name="approved_%(class)ss",
        on_delete=models.SET_NULL,
    )

    _metadata = {
        "title": "title",
        "description": "get_meta_description",
        "type": "research.dataset",
    }

    class Meta:
        verbose_name = _("dataset")
        verbose_name_plural = _("datasets")

    @property
    def resource_type(self):
        """Returns the resource type as per the DataCite schema. Geoluminate datasets are always of type 'Dataset'."""
        return "Dataset"

    @property
    def locations(self):
        return self.samples.prefetch_related("location").values("location__point")

    @cached_property
    def GeometryCollection(self):
        """Returns a GeometryCollection of all the samples in the dataset"""
        return self.locations.aggregate(collection=Collect("location__point"))["collection"]

    @cached_property
    def centroid(self):
        """Returns the centroid of the dataset as a Point"""
        return self.GeometryCollection.centroid

    @cached_property
    def bbox(self):
        """Returns the bounding box of the dataset as a list of coordinates in the format [xmin, ymin, xmax, ymax]."""
        return self.GeometryCollection.extent

    @cached_property
    def status(self):
        return random.choice(["In progress", "Completed", "Accepted", "Published"])

    def get_status_display(self):
        return self.status

    def get_collection_start(self):
        """Returns the key date specifying the start of the collection "CollectionStart" OR the earliest collection date for a related sample"""
        try:
            return self.key_dates.get(type=FuzzyDate.DateTypes.CollectionStart)
        except FuzzyDate.DoesNotExist:
            return None
