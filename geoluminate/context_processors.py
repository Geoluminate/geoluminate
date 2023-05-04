import json

from django.conf import settings

from geoluminate.models import GlobalConfiguration


def global_config(request):
    return {
        "config": GlobalConfiguration.get_solo(),
        "geoluminate": settings.GEOLUMINATE,
        "config_json": json.dumps(GlobalConfiguration.objects.values()[0]),
        "ACCOUNT_ALLOW_REGISTRATION": settings.ACCOUNT_ALLOW_REGISTRATION,
    }
