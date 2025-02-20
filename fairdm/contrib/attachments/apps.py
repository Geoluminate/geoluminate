from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class FairDMAttchmentsConfig(AppConfig):
    name = "fairdm.contrib.attachments"
    label = "fairdm_attachments"
    verbose_name = _("Attachments")
