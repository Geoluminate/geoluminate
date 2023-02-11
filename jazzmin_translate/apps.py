from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class JazzminTranslateConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "jazzmin_translate"
    verbose_name = _("Jazzmin Translate")
