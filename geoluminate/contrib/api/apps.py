from django.apps import AppConfig


class ApiConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    label = "geoluminate_api"
    name = "geoluminate.contrib.api"
