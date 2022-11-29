from django.shortcuts import render
from kepler.models import Configuration
from django.http import JsonResponse
from django.views.generic import TemplateView
import json
# Create your views here.


class KeplerFullPageView(TemplateView):
    template_name = 'kepler/viewer.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        appconfig = Configuration.get_solo()

        context['config'] = json.dumps({
            'default_config': appconfig.build_config(),
            'mapbox_token': appconfig.mapbox_token,
            'lang': self.get_lang_code(appconfig.lang),
            'theme': appconfig.theme,
        })

        return context

    def get_lang_code(self, default):
        if self.locale_is_supported():
            return self.request.LANGUAGE_CODE
        else:
            return default

    def locale_is_supported(self):
        return self.request.LANGUAGE_CODE in [x[0]
                                              for x in Configuration.KEPLER_LANG_CODES]
