from django.db import models
from django.utils.translation import gettext_lazy as _


class StatusChoices(models.IntegerChoices):
    IN_PROGRESS = 0, _("In progress")
    SUBMITTED = 1, _("Submitted")
    ACCEPTED = 2, _("Accepted")
