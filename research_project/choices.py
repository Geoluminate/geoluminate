from django.db import models
from django.utils.translation import gettext_lazy as _


class ProjectStatus(models.IntegerChoices):
    INACTIVE = 0, _('Inactive')
    ACTIVE = 1, _('Active')
