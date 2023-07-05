from django.conf import settings
from django.contrib.sites.models import Site
from django.utils.encoding import force_str
from django.utils.translation import gettext_lazy as _
from filer.fields.image import FilerImageField
from solo.models import SingletonModel

from geoluminate.db import models


class GlobalConfiguration(SingletonModel):
    site = models.OneToOneField(Site, blank=True, null=True, on_delete=models.SET_NULL)  # type: ignore[var-annotated]
    logo = FilerImageField(
        related_name="+",
        verbose_name=_("Logo"),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    icon = FilerImageField(
        related_name="+",
        verbose_name=_("Icon"),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    custodian = models.OneToOneField(
        to=settings.AUTH_USER_MODEL,
        limit_choices_to={
            "is_staff": True,
        },
        verbose_name=_("custodian"),
        related_name="custodian",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )

    # Visibility related settings
    lockdown_enabled = models.BooleanField(
        _("Access rights"),
        choices=((True, _("Admin only")), (False, _("Public"))),
        help_text=_("Locks down the entire application so that only administrators can log in."),
        default=False,
    )

    class Meta:
        db_table = "global_config"
        verbose_name = _("Configuration")

    def __str__(self):
        return force_str(_("Configuration"))
