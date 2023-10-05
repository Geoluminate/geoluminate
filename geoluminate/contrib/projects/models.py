from django.conf import settings
from django.utils.translation import gettext_lazy as _

from geoluminate import models
from geoluminate.contrib.core.models import Abstract

from . import choices


class Project(Abstract):
    """A project is a collection of datasets and associated metadata. The Project model
    is the top level model in the Geoluminate schema hierarchy and all datasets, samples,
    and measurements should relate back to a project."""

    STATUS_CHOICES = choices.ProjectStatus

    # objects = PublicObjectsManager()

    status = models.IntegerField(_("status"), choices=STATUS_CHOICES.choices, default=STATUS_CHOICES.CONCEPT)

    # flags
    add_dataset_contributors = models.BooleanField(
        _("add dataset contributors"),
        help_text=_(
            "All contributors to datasets associated with this project should be automatically added as a project"
            " member."
        ),
        default=True,
    )
    is_public = models.BooleanField(
        _("visibility"),
        help_text=_("Choose whether this project is publicly discoverable."),
        choices=(
            (True, _("Public")),
            (False, _("Private")),
        ),
        default=False,
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

    def add_contributors(self, *profiles, roles=None):
        """Adds the given profiles as contributors to the object."""
        for profile in profiles:
            self.contributors.create(profile=profile, roles=roles)

    def in_progress(self):
        """Returns True if the project is in progress"""
        return self.status == self.STATUS_CHOICES.IN_PROGRESS

    def get_contributors(self):
        """Returns all contributors of the project"""
        return None
