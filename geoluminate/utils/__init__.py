from django.apps import apps
from django_fake_model import models as f

from geoluminate.conf import settings
from geoluminate.db.models import Base


def get_database_models():
    """Get a list of all models in the project that subclass from `geoluminate.db.models.Base`."""
    return [m for m in apps.get_models() if issubclass(m, Base)]


def get_filter_params(request):
    """Returns curent filter params as a string"""
    params = request.GET.copy()
    params.pop("page", True)
    if params:
        return "&" + params.urlencode()
    else:
        return ""


# def get_core_database():
#     """Fetches the geoluminate database model defined by `settings.CORE_DATABASE`"""
#     return getattr(settings, "GEOLUMINATE_DATABASE", None)


def get_db_name():
    return getattr(settings, "DATABASE_NAME")


# db_string = get_core_database()
# if db_string:
#     DATABASE = apps.get_model(get_core_database())
#     db_name = DATABASE._meta.verbose_name
# else:

#     class Database(f.FakeModel):
#         class Meta:
#             verbose_name = "You need to specify this model in your settings"

#     DATABASE = Database
#     # DATABASE = None
#     db_name = "undefined"
