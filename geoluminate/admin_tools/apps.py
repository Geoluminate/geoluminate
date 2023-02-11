from django.apps import AppConfig


class CoreAdminConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'geoluminate.admin_tools'
    verbose_name = 'GeoLuminate Admin'
    label = 'geoluminate_admin'
