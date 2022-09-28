import json
import logging

from django.db.models import JSONField 
from django.contrib import admin
from django.forms import widgets


logger = logging.getLogger(__name__)
class PrettyJSONWidget(widgets.Textarea):

    def format_value(self, value):

        value = json.dumps(json.loads(value), indent=2, sort_keys=True)
        self.attrs['onfocus'] = 'this.style.height = "";this.style.height = this.scrollHeight + 3 +  "px"'
        self.attrs['onfocusout'] = 'this.style.height = "";'
        return value

