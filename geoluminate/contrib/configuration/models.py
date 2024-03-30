from django.db import models
from django.utils.encoding import force_str
from django.utils.translation import gettext_lazy as _
from research_vocabs.fields import TaggableConcepts
from solo.models import SingletonModel


class Configuration(SingletonModel):
    # name = models.CharField(
    #     _("Site Name"),
    #     max_length=255,
    #     default="",
    # )

    logo = models.ImageField(
        _("Logo"),
        null=True,
        blank=True,
    )
    icon = models.ImageField(
        _("Icon"),
        null=True,
        blank=True,
    )

    keywords = TaggableConcepts(
        verbose_name=_("Keywords"),
        help_text=_("Controlled keywords for enhanced discoverability"),
        blank=True,
    )

    database = models.JSONField(
        _("database"),
        default=dict,
    )

    authority = models.JSONField(
        _("authority"),
        default=dict,
    )

    theme = models.JSONField(
        _("theme"),
        default=dict,
    )

    class Meta:
        verbose_name = _("Site Configuration")

    def __str__(self):
        return force_str(_("Site Configuration"))
