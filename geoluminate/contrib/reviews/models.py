import random

from django.conf import settings
from django.contrib.gis.db.models import Collect
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _

from geoluminate import models
from geoluminate.contrib.core.models import Abstract


class Review(models.Model):
    """Stores information about each review"""

    STATUS_CHOICES = [
        (0, _("In progress")),
        (1, _("Completed")),
        (2, _("Accepted")),
    ]

    status = models.PositiveSmallIntegerField(
        verbose_name=_("status"),
        help_text=_("Status of the review"),
        choices=STATUS_CHOICES,
        default=0,
    )
    literature = models.OneToOneField(
        to="literature.Literature",
        help_text=_("Literature being reviewed"),
        on_delete=models.SET_NULL,
        null=True,
    )
    dataset = models.OneToOneField(
        to="datasets.Dataset",
        help_text=_("Dataset being reviewed"),
        on_delete=models.SET_NULL,
        null=True,
    )
    reviewer = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        help_text=_("User reviewing this publication"),
        on_delete=models.SET_NULL,
        null=True,
    )
    # submitter = models.ForeignKey(
    #     to=settings.AUTH_USER_MODEL,
    #     help_text=_("User submitting this review"),
    #     on_delete=models.SET_NULL,
    #     null=True,
    # )

    submitted = models.DateTimeField(
        verbose_name=_("date submitted"),
        help_text=_("Date the user submitted correction for final approval by site admins"),
        null=True,
        blank=True,
    )
    accepted = models.DateTimeField(
        verbose_name=_("date accepted"),
        help_text=_("Date the review was accepted by site admins and incorporated into the production database"),
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"Review of {self.dataset} by {self.reviewer}"

    # def get_absolute_url(self):
    # return reverse("review", kwargs={"pk": self.pk})

    # def status(self):
    #     if self.accepted:
    #         return "Accepted"
    #     elif self.submitted:
    #         return "Submitted"
    #     else:
    #         return "Draft"
