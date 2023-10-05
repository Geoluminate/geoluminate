from django.db import models
from django.utils.translation import gettext_lazy as _


class ProjectStatus(models.IntegerChoices):
    CONCEPT = 0, _("Concept")
    PLANNING = 1, _("Planning")
    # SEARCHING_FOR_FUNDING = 3, _("Searching for funding")
    # SEARCHING_FOR_COLLABORATORS = 4, _("Searching for collaborators")
    IN_PROGRESS = 2, _("In progress")
    COMPLETE = 3, _("Complete")


class ProjectTags(models.TextChoices):
    """A class for storing choices for tags on the Project model."""

    COLLABORATORS_WANTED = "Collaborators wanted", _("Looking for collaborators")
    FUNDING_REQUIRED = "Funding required", _("Looking for funding")
    HAS_FUNDING = "Has funding", _("Has funding")
    POSITIONS_OPEN = "Positions open", _("Positions open")
    EQUIPMENT_REQUIRED = "Equipment required", _("Looking for tools")
