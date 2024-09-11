from django.contrib import admin
from django.db import models
from django.utils.translation import gettext_lazy as _
from parler.models import TranslatableModel, TranslatedFields
from solo.models import SingletonModel


class Authority(SingletonModel, TranslatableModel):
    url = models.URLField(
        _("URL"),
        blank=True,
        null=True,
    )
    contact = models.EmailField(
        _("Contact"),
        blank=True,
        null=True,
    )
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

    translations = TranslatedFields(
        name=models.CharField(_("Name"), max_length=255),
        short_name=models.CharField(_("Short Name"), max_length=255, blank=True, null=True),
        description=models.TextField(_("Description")),
    )

    class Meta:
        verbose_name = _("Governing Authority")

    # def __str__(self):
    #     return force_str(self.name)


class Database(SingletonModel, TranslatableModel):
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
    keywords = models.ManyToManyField(
        "research_vocabs.Concept",
        verbose_name=_("Keywords"),
        help_text=_("A set of keywords from controlled vocabularies describing the database."),
        blank=True,
    )

    translations = TranslatedFields(
        name=models.CharField(_("Name"), max_length=255),
        short_name=models.CharField(_("Short Name"), max_length=255, blank=True, null=True),
        description=models.TextField(_("Description")),
    )

    class Meta:
        verbose_name = _("Database")

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        name = self.safe_translation_getter("name", default="Geoluminate")
        admin.site.site_header = name
        admin.site.site_title = name
        # try:
        #     admin.site.site_header = self.name
        #     admin.site.site_title = self.name
        # except TranslationDoesNotExist:
        #     return ""

    def __str__(self):
        return "Database"


# class Configuration(SingletonModel):
#     logo = models.ImageField(
#         _("Logo"),
#         null=True,
#         blank=True,
#     )
#     icon = models.ImageField(
#         _("Icon"),
#         null=True,
#         blank=True,
#     )
#     theme = models.JSONField(
#         _("theme"),
#         default=dict,
#     )

#     class Meta:
#         verbose_name = _("Site Configuration")

#     def __str__(self):
#         return force_str(_("Site Configuration"))
