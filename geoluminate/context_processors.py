import json

from geoluminate.models import GlobalConfiguration


def global_config(request):
    return {
        "config": GlobalConfiguration.get_solo(),
        "config_json": json.dumps(GlobalConfiguration.objects.values()[0]),
    }
