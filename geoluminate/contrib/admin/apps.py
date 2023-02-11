from django.apps import AppConfig


class GeoluminateAdminConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "geoluminate.contrib.admin"
    verbose_name = "Geoluminate Admin"
    label = "geoluminate_admin"
