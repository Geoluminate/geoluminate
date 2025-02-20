from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class FairDMImportExportConfig(AppConfig):
    name = "fairdm.contrib.import_export"
    label = "fairdm_import_export"
    verbose_name = _("Import / Export")
