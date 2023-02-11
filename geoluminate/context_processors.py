from geoluminate.models import GlobalConfiguration
from django.core import serializers
import json


def global_config(request):
    return {
        'config': GlobalConfiguration.get_solo(),
        'config_json': json.dumps(GlobalConfiguration.objects.values()[0])
    }
