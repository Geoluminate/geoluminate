from django.conf import settings

# from django.contrib.gis.db.models import Collect
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _

from geoluminate import models
from geoluminate.contrib.core.models import Abstract

# from geoluminate.utils import icon
from . import choices


class Project(Abstract):
    """A project is a collection of datasets and associated metadata. The Project model
    is the top level model in the Geoluminate schema hierarchy and all datasets, samples,
    and measurements should relate back to a project."""

    DESCRIPTION_TYPES = choices.ProjectDescriptions

    STATUS_CHOICES = choices.ProjectStatus

    # objects = PublicObjectsManager()

    status = models.IntegerField(_("status"), choices=STATUS_CHOICES.choices, default=STATUS_CHOICES.CONCEPT)

    _metadata = {
        "title": "title",
        "description": "get_meta_description",
        "image": "get_meta_image",
        "type": "research.project",
    }

    class Meta:
        verbose_name = _("project")
        verbose_name_plural = _("projects")
        app_label = "geoluminate"

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
