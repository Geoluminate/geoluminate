from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import ArrayField
from django.contrib.sites.models import Site
from django.db import models
from django.utils.encoding import force_str
from django.utils.module_loading import import_string
from django.utils.translation import gettext_lazy as _
from django_better_admin_arrayfield.models.fields import ArrayField
from filer.fields.image import FilerImageField
from solo.models import SingletonModel


class GlobalConfiguration(SingletonModel):

    site = models.OneToOneField(Site, blank=True, null=True, on_delete=models.SET_NULL)
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
        to=get_user_model(),
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
        help_text=_(
            "Locks down the entire application so that only administrators can log in."
        ),
        default=False,
    )
    remote_addr_exceptions = ArrayField(
        verbose_name=_("Remote address exceptions"),
        help_text=_(
            "A list of remote IP adresses that are permitted to access the application when lockdown is enabled."
        ),
        base_field=models.GenericIPAddressField(),
        default=list,
        blank=True,
    )
    trusted_proxies = ArrayField(
        verbose_name=_("Trusted proxies"),
        help_text=_("A list of trusted proxies."),
        base_field=models.GenericIPAddressField(),
        default=list,
        blank=True,
    )
    enable_api = models.BooleanField(
        _("Status"),
        choices=((True, _("Enabled")), (False, _("Disabled"))),
        help_text=_("Enable or disable access to the database API."),
        default=True,
    )

    class Meta:
        db_table = "global_config"
        verbose_name = _("Configuration")

    def __str__(self):
        return force_str(_("Configuration"))


# imports the abstract base class specified in the settings
Base = import_string(getattr(settings, "GEOLUMINATE")["base_model"])


class Geoluminate(Base):
    hide_from_api = False
    pass
