from django.contrib import admin
from solo.admin import SingletonModelAdmin
from .models import Configuration
from .forms import PrettyJSONWidget
from django.db.models import JSONField 
    
@admin.register(Configuration)
class ConfigurationAdmin(SingletonModelAdmin):
    formfield_overrides = {
        JSONField: {'widget': PrettyJSONWidget}
    }
    
# Register your models here.
# admin.site.register(Configuration, SingletonModelAdmin)