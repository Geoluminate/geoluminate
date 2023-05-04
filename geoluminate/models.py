from django.conf import settings
from django.contrib.gis.db import models
from django.contrib.sites.models import Site
from django.utils.encoding import force_str
from django.utils.translation import gettext_lazy as _
from filer.fields.image import FilerImageField
from literature.fields import LiteratureM2M
from meta.models import ModelMeta
from model_utils import FieldTracker
from model_utils.models import TimeStampedModel
from polymorphic.models import PolymorphicModel
from solo.models import SingletonModel

from geoluminate.contrib.gis.managers import SiteManager
from geoluminate.db.fields import PIDField, RangeField


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
    # remote_addr_exceptions = ArrayField(
    #     verbose_name=_("Remote address exceptions"),
    #     help_text=_(
    #         "A list of remote IP adresses that are permitted to access the application when lockdown is enabled."
    #     ),
    #     base_field=models.GenericIPAddressField(),
    #     default=list,
    #     blank=True,
    # )
    # trusted_proxies = ArrayField(
    #     verbose_name=_("Trusted proxies"),
    #     help_text=_("A list of trusted proxies."),
    #     base_field=models.GenericIPAddressField(),
    #     default=list,
    #     blank=True,
    # )
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


class Geoluminate(ModelMeta, PolymorphicModel, TimeStampedModel):
    pid = PIDField()

    IGSN = models.IntegerField(
        "IGSN",
        help_text=_("An International Generic Sample Number for the site."),
        blank=True,
        null=True,
    )

    name = models.CharField(
        verbose_name=_("name"),
        null=True,
        help_text=_("Specified site name for the related database entry"),
        max_length=255,
    )

    geom = models.PointField(null=True, blank=True)

    elevation = RangeField(
        _("elevation (m)"),
        help_text=_("elevation with reference to mean sea level (m)"),
        max_value=9000,
        min_value=-12000,
        blank=True,
        null=True,
    )

    literature = LiteratureM2M(
        help_text=_("Associated literature."),
        blank=True,
    )

    acquired = models.DateTimeField(
        _("date acquired"),
        help_text=_("Date and time of acquisition."),
        null=True,
    )

    comment = models.TextField(
        _("comment"),
        help_text=_("General comments regarding the site and/or measurement"),
        blank=True,
        null=True,
    )

    tracker = FieldTracker()

    _metadata = {
        # "title": "get_meta_title",
        "description": "description",
        "year": "year",
    }

    hide_from_api = False

    class Meta:
        verbose_name = "Geoluminate"
        verbose_name_plural = "Geoluminate"

        permissions = [
            (
                "geoluminate_database_admin",
                _("Can create, view, update or delete any model associated with the research database"),
            ),
        ]


class GeoluminateSite(Geoluminate):
    objects = SiteManager.as_manager()

    class Meta:
        verbose_name = _("Site")
        verbose_name_plural = _("Sites")
        proxy = True
